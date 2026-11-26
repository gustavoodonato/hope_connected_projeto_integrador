from datetime import datetime, timedelta, timezone
import jwt
import pytest
from src.modules.user.app.get_user.get_user_controller import GetUserController
from src.modules.user.app.get_user.get_user_usercase import GetUserUsecase
from src.shared.domain.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.token_handler import TokenHandler
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.auth import auth


@pytest.fixture
def controller():
    return GetUserController(GetUserUsecase(UserRepositoryMock()))


def make_request(user_id, requester_id=None):
    """Monta o request como o adaptador do Flask faria."""
    headers = auth(requester_id) if requester_id is not None else {}
    return HttpRequest(headers=headers, query_params={"user_id": user_id})


class Test_GetUserController:
    # --- sucesso ---
    def test_get_own_aacd(self, controller):
        response = controller(make_request("123", "123"))

        assert response.status_code == 200
        assert response.body["nome"] == "Murilo"
        assert response.body["email"] == "muriloso123@gmail.com"
        assert response.body["endereco"] is None

    def test_get_own_fornecedor(self, controller):
        response = controller(make_request("456", "456"))

        assert response.status_code == 200
        assert response.body["nome"] == "Lucas"
        assert response.body["phone"] == "55444446666"
        assert response.body["endereco"]["cidade"] == "São Caetano do Sul"

    def test_response_never_has_password(self, controller):
        response = controller(make_request("456", "456"))

        assert "senha_hash" not in response.body
        assert "senha" not in response.body

    def test_get_other_user_is_forbidden(self, controller):
        response = controller(make_request("456", "123"))
        assert response.status_code == 403

    def test_forbidden_does_not_leak_data(self, controller):
        response = controller(make_request("456", "123"))
        assert "Lucas" not in str(response.body)

    def test_user_not_found(self, controller):
        response = controller(make_request("999", "999"))
        assert response.status_code == 404

    def test_non_numeric_user_id(self, controller):
        response = controller(make_request("abc", "123"))
        assert response.status_code == 400

    def test_missing_token(self, controller):
        assert controller(make_request("123")).status_code == 401

    def test_invalid_token(self, controller):
        request = HttpRequest(headers={"Authorization": "Bearer lixo"},
                              query_params={"user_id": "123"})
        assert controller(request).status_code == 401

    def test_expired_token(self, controller):
        token = TokenHandler.generate(123, expira_em_minutos=-1)
        request = HttpRequest(headers={"Authorization": f"Bearer {token}"},
                              query_params={"user_id": "123"})
        assert controller(request).status_code == 401

    def test_forged_token(self, controller):
        futuro = datetime.now(timezone.utc) + timedelta(minutes=5)
        falso = jwt.encode({"sub": "123", "exp": futuro},
                           "outra-chave-qualquer-com-32-caracteres!", algorithm="HS256")
        request = HttpRequest(headers={"Authorization": f"Bearer {falso}"},
                              query_params={"user_id": "123"})
        assert controller(request).status_code == 401

    def test_old_header_no_longer_works(self, controller):
        request = HttpRequest(headers={"X-Requester-Id": "123"},
                              query_params={"user_id": "123"})
        assert controller(request).status_code == 401

    # --- erro inesperado ---
    def test_unexpected_error_returns_500(self):
        def usecase_quebrado(**kwargs):
            raise RuntimeError("falha inesperada")

        controller = GetUserController(usecase_quebrado)
        response = controller(make_request("123", "123"))

        assert response.status_code == 500