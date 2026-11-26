from datetime import datetime, timedelta, timezone
import jwt
import pytest
from src.modules.user.app.delete_user.delete_user_controller import DeleteUserController
from src.modules.user.app.delete_user.delete_user_usecase import DeleteUserUsecase
from src.shared.domain.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.token_handler import TokenHandler
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.auth import auth


@pytest.fixture
def repo():
    return UserRepositoryMock()


@pytest.fixture
def controller(repo):
    return DeleteUserController(DeleteUserUsecase(repo))


def make_request(user_id, requester_id=None):
    headers = auth(requester_id) if requester_id is not None else {}
    return HttpRequest(headers=headers, query_params={"user_id": user_id})


class Test_DeleteUserController:
    def test_delete_own_user(self, controller, repo):
        response = controller(make_request("456", "456"))

        assert response.status_code == 200
        assert response.body["id"] == 456
        assert response.body["message"] == "Usuário removido com sucesso"
        assert "senha_hash" not in response.body
        assert len(repo.users) == 2
        with pytest.raises(NoItemsFound):
            repo.get_user(456)

    def test_delete_other_user_is_forbidden(self, controller, repo):
        response = controller(make_request("456", "123"))

        assert response.status_code == 403
        assert len(repo.users) == 3

    def test_user_not_found(self, controller):
        assert controller(make_request("999", "999")).status_code == 404

    def test_non_numeric_user_id(self, controller):
        assert controller(make_request("abc", "123")).status_code == 400

    # --- token ---
    def test_missing_token(self, controller):
        assert controller(make_request("456")).status_code == 401

    def test_invalid_token(self, controller):
        request = HttpRequest(headers={"Authorization": "Bearer lixo"},
                              query_params={"user_id": "456"})
        assert controller(request).status_code == 401

    def test_expired_token(self, controller):
        token = TokenHandler.generate(456, expira_em_minutos=-1)
        request = HttpRequest(headers={"Authorization": f"Bearer {token}"},
                              query_params={"user_id": "456"})
        assert controller(request).status_code == 401

    def test_forged_token(self, controller, repo):
        futuro = datetime.now(timezone.utc) + timedelta(minutes=5)
        falso = jwt.encode({"sub": "456", "exp": futuro},
                           "outra-chave-qualquer-com-32-caracteres!", algorithm="HS256")
        request = HttpRequest(headers={"Authorization": f"Bearer {falso}"},
                              query_params={"user_id": "456"})

        assert controller(request).status_code == 401
        assert len(repo.users) == 3

    def test_old_header_no_longer_works(self, controller, repo):
        request = HttpRequest(headers={"X-Requester-Id": "456"},
                              query_params={"user_id": "456"})

        assert controller(request).status_code == 401
        assert len(repo.users) == 3

    def test_unexpected_error_returns_500(self):
        def usecase_quebrado(**kwargs):
            raise RuntimeError("falha inesperada")

        controller = DeleteUserController(usecase_quebrado)
        assert controller(make_request("456", "456")).status_code == 500