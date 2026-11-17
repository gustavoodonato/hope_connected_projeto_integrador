import pytest

from src.modules.user.app.get_user.get_user_controller import GetUserController
from src.modules.user.app.get_user.get_user_usercase import GetUserUsecase
from src.shared.domain.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


@pytest.fixture
def controller():
    return GetUserController(GetUserUsecase(UserRepositoryMock()))


def make_request(user_id, requester_id="__omitir__"):
    """Monta o request como o adaptador do Flask faria."""
    headers = {} if requester_id == "__omitir__" else {"X-Requester-Id": requester_id}
    return HttpRequest(headers=headers, query_params={"user_id": user_id})


class Test_GetUserController:
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

    def test_missing_requester_header(self, controller):
        response = controller(make_request("123"))
        assert response.status_code == 400

    def test_non_numeric_requester(self, controller):
        response = controller(make_request("123", "abc"))
        assert response.status_code == 400

    def test_unexpected_error_returns_500(self):
        def usecase_quebrado(**kwargs):
            raise RuntimeError("falha inesperada")

        controller = GetUserController(usecase_quebrado)
        response = controller(make_request("123", "123"))

        assert response.status_code == 500