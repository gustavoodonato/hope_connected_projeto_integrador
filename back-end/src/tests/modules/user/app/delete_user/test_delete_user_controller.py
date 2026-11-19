import pytest

from src.modules.user.app.delete_user.delete_user_controller import DeleteUserController
from src.modules.user.app.delete_user.delete_user_usecase import DeleteUserUsecase
from src.shared.domain.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


@pytest.fixture
def repo():
    return UserRepositoryMock()


@pytest.fixture
def controller(repo):
    return DeleteUserController(DeleteUserUsecase(repo))


def make_request(user_id, requester_id="__omitir__"):
    headers = {} if requester_id == "__omitir__" else {"X-Requester-Id": requester_id}
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

    def test_missing_requester_header(self, controller):
        assert controller(make_request("456")).status_code == 400

    def test_non_numeric_requester(self, controller):
        assert controller(make_request("456", "abc")).status_code == 400

    def test_unexpected_error_returns_500(self):
        def usecase_quebrado(**kwargs):
            raise RuntimeError("falha inesperada")

        controller = DeleteUserController(usecase_quebrado)
        assert controller(make_request("456", "456")).status_code == 500