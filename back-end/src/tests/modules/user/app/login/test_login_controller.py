import pytest
from src.modules.user.app.login.login_controller import LoginController
from src.modules.user.app.login.login_usecase import LoginUsecase
from src.shared.domain.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.token_handler import TokenHandler
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

@pytest.fixture
def controller():
    return LoginController(LoginUsecase(UserRepositoryMock()))


def req(**corpo):
    return HttpRequest(body=corpo)


class Test_LoginController:
    # --- sucesso ---
    def test_login_aacd(self, controller):
        response = controller(req(email="muriloso123@gmail.com", senha="senha123"))

        assert response.status_code == 200
        assert response.body["user"]["nome"] == "Murilo"
        assert response.body["token_type"] == "Bearer"

    def test_login_fornecedor(self, controller):
        response = controller(req(email="luquinhas24@gmail.com", senha="senha123"))

        assert response.status_code == 200
        assert response.body["user"]["id"] == 456
        assert response.body["user"]["role"] == "Fornecedor"   # use o valor do seu RoleEnum

    def test_token_belongs_to_the_user(self, controller):
        response = controller(req(email="luquinhas24@gmail.com", senha="senha123"))
        assert TokenHandler.decode(response.body["token"]) == 456

    def test_response_never_has_password(self, controller):
        response = controller(req(email="luquinhas24@gmail.com", senha="senha123"))
        assert "senha_hash" not in str(response.body)

    # --- credenciais ---
    def test_wrong_password(self, controller):
        response = controller(req(email="muriloso123@gmail.com", senha="errada"))
        assert response.status_code == 401
        assert "token" not in str(response.body)

    def test_unknown_email(self, controller):
        response = controller(req(email="naoexiste@gmail.com", senha="senha123"))
        assert response.status_code == 401

    def test_unknown_email_and_wrong_password_look_the_same(self, controller):
        a = controller(req(email="naoexiste@gmail.com", senha="senha123"))
        b = controller(req(email="muriloso123@gmail.com", senha="errada"))
        assert a.status_code == b.status_code
        assert a.body == b.body

    # --- parâmetros inválidos ---
    @pytest.mark.parametrize("faltando", ["email", "senha"])
    def test_missing_field(self, controller, faltando):
        corpo = {"email": "muriloso123@gmail.com", "senha": "senha123"}
        del corpo[faltando]
        assert controller(req(**corpo)).status_code == 400

    @pytest.mark.parametrize("campo", ["email", "senha"])
    def test_wrong_type(self, controller, campo):
        corpo = {"email": "muriloso123@gmail.com", "senha": "senha123", campo: 123}
        assert controller(req(**corpo)).status_code == 400

    def test_blank_password(self, controller):
        assert controller(req(email="muriloso123@gmail.com", senha="   ")).status_code == 400

    # --- erro inesperado ---
    def test_unexpected_error_returns_500(self):
        def usecase_quebrado(**kwargs):
            raise RuntimeError("falha inesperada")

        response = LoginController(usecase_quebrado)(req(email="a@a.com", senha="123456"))
        assert response.status_code == 500