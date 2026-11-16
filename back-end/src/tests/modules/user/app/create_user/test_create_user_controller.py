import pytest

from src.modules.user.app.create_user.create_user_controller import CreateUserController
from src.modules.user.app.create_user.create_user_usecase import CreateUserUsecase
from src.shared.domain.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


ENDERECO = {"cep": "01023330", "logradouro": "Rua A", "numero": "1",
            "bairro": "Centro", "cidade": "São Paulo", "estado": "SP"}


@pytest.fixture
def controller():
    return CreateUserController(CreateUserUsecase(UserRepositoryMock()))


def fornecedor(**alteracoes):
    corpo = {"nome": "IBM", "email": "ibm@gmail.com", "senha": "654321",
             "phone": "88999994444", "endereco": dict(ENDERECO)}
    corpo.update(alteracoes)
    return corpo


class Test_CreateUserController:
    def test_created_aacd(self, controller):
        response = controller(HttpRequest(body={
            "nome": "Ana", "email": "ana@aacd.org.br", "senha": "123456"}))

        assert response.status_code == 201
        assert response.body["email"] == "ana@aacd.org.br"
        assert response.body["endereco"] is None
        assert "senha_hash" not in response.body

    def test_created_fornecedor(self, controller):
        response = controller(HttpRequest(body=fornecedor()))

        assert response.status_code == 201
        assert response.body["phone"] == "88999994444"
        assert response.body["endereco"]["cidade"] == "São Paulo"

    @pytest.mark.parametrize("campo", ["nome", "email", "senha"])
    def test_missing_required_field(self, controller, campo):
        corpo = fornecedor()
        del corpo[campo]
        assert controller(HttpRequest(body=corpo)).status_code == 400

    @pytest.mark.parametrize("campo", ["nome", "email", "senha"])
    def test_wrong_type_required_field(self, controller, campo):
        response = controller(HttpRequest(body=fornecedor(**{campo: 123})))
        assert response.status_code == 400

    def test_wrong_type_phone(self, controller):
        response = controller(HttpRequest(body=fornecedor(phone=123)))
        assert response.status_code == 400

    def test_endereco_not_a_dict(self, controller):
        response = controller(HttpRequest(body=fornecedor(endereco="Rua A")))
        assert response.status_code == 400

    def test_endereco_missing_field(self, controller):
        endereco = dict(ENDERECO)
        del endereco["cidade"]
        response = controller(HttpRequest(body=fornecedor(endereco=endereco)))
        assert response.status_code == 400

    def test_invalid_cep(self, controller):
        endereco = {**ENDERECO, "cep": "123"}
        response = controller(HttpRequest(body=fornecedor(endereco=endereco)))
        assert response.status_code == 400

    def test_fornecedor_without_phone(self, controller):
        corpo = fornecedor()
        del corpo["phone"]
        assert controller(HttpRequest(body=corpo)).status_code == 400

    def test_fornecedor_without_endereco(self, controller):
        corpo = fornecedor()
        del corpo["endereco"]
        assert controller(HttpRequest(body=corpo)).status_code == 400

    def test_short_password(self, controller):
        response = controller(HttpRequest(body=fornecedor(senha="123")))
        assert response.status_code == 400

    def test_duplicated_email(self, controller):
        response = controller(HttpRequest(body=fornecedor(email="muriloso123@gmail.com")))
        assert response.status_code == 409
