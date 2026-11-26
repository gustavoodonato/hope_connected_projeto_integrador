import pytest
from datetime import datetime, timedelta, timezone
import jwt
from src.shared.helpers.token_handler import TokenHandler
from src.shared.helpers.auth import auth
from src.modules.user.app.update_user.update_user_controller import UpdateUserController
from src.modules.user.app.update_user.update_user_usecase import UpdateUserUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

ENDERECO = {"cep": "04567-000", "logradouro": "Rua B", "numero": "9",
            "bairro": "Moema", "cidade": "São Paulo", "estado": "sp"}


@pytest.fixture
def repo():
    return UserRepositoryMock()


@pytest.fixture
def controller(repo):
    return UpdateUserController(UpdateUserUsecase(repo))


def make_request(user_id, requester_id=None, body=None):
    headers = auth(requester_id) if requester_id is not None else {}
    return HttpRequest(body=body or {}, headers=headers, query_params={"user_id": user_id})


class Test_UpdateUserController:
    # --- sucesso ---
    def test_update_nome(self, controller, repo):
        response = controller(make_request("456", "456", {"nome": "Lucas Novo"}))

        assert response.status_code == 200
        assert response.body["nome"] == "Lucas Novo"
        assert repo.get_user(456).nome == "Lucas Novo"          # foi salvo
        assert response.body["email"] == "luquinhas24@gmail.com"   # o resto não mudou

    def test_update_phone_and_endereco(self, controller):
        response = controller(make_request("456", "456", {
            "phone": "11911112222", "endereco": ENDERECO}))

        assert response.status_code == 200
        assert response.body["phone"] == "11911112222"
        assert response.body["endereco"]["cep"] == "04567000"   # validator limpou o hífen
        assert response.body["endereco"]["estado"] == "SP"      # validator deixou maiúscula

    def test_update_aacd_nome(self, controller):
        response = controller(make_request("123", "123", {"nome": "Murilo Novo"}))
        assert response.status_code == 200
        assert response.body["endereco"] is None

    def test_email_and_role_cannot_be_changed(self, controller):
        response = controller(make_request("456", "456", {
            "nome": "Lucas Novo", "email": "novo@aacd.org.br", "role": "AACD"}))

        assert response.status_code == 200
        assert response.body["email"] == "luquinhas24@gmail.com"
        assert response.body["role"] == RoleEnum.FORNECEDOR.value

    def test_response_never_has_password(self, controller):
        response = controller(make_request("456", "456", {"nome": "Lucas Novo"}))
        assert "senha_hash" not in response.body

    # --- permissão e existência ---
    def test_update_other_user_is_forbidden(self, controller, repo):
        response = controller(make_request("456", "123", {"nome": "Invasor"}))

        assert response.status_code == 403
        assert repo.get_user(456).nome == "Lucas"               # nada mudou

    def test_user_not_found(self, controller):
        response = controller(make_request("999", "999", {"nome": "X"}))
        assert response.status_code == 404

    # --- parâmetros inválidos ---
    def test_non_numeric_user_id(self, controller):
        assert controller(make_request("abc", "123", {"nome": "X"})).status_code == 400

    def test_missing_token(self, controller):
        assert controller(make_request("456", body={"nome": "X"})).status_code == 401

    def test_empty_body(self, controller):
        assert controller(make_request("456", "456", {})).status_code == 400

    def test_only_ignored_fields(self, controller):
        # só email: nada que possa ser alterado
        assert controller(make_request("456", "456", {"email": "x@x.com"})).status_code == 400

    # --- campos inválidos ---
    def test_nome_wrong_type(self, controller):
        assert controller(make_request("456", "456", {"nome": 123})).status_code == 400

    def test_nome_blank(self, controller):
        assert controller(make_request("456", "456", {"nome": "   "})).status_code == 400

    def test_phone_wrong_type(self, controller):
        assert controller(make_request("456", "456", {"phone": 123})).status_code == 400

    def test_fornecedor_cannot_lose_phone(self, controller, repo):
        response = controller(make_request("456", "456", {"phone": ""}))

        assert response.status_code == 400
        assert repo.get_user(456).phone == "55444446666"        # nada mudou

    def test_endereco_not_a_dict(self, controller):
        assert controller(make_request("456", "456", {"endereco": "Rua A"})).status_code == 400

    def test_endereco_missing_field(self, controller):
        endereco = {k: v for k, v in ENDERECO.items() if k != "cidade"}
        assert controller(make_request("456", "456", {"endereco": endereco})).status_code == 400

    def test_invalid_cep(self, controller):
        endereco = {**ENDERECO, "cep": "123"}
        assert controller(make_request("456", "456", {"endereco": endereco})).status_code == 400

    # --- erro inesperado ---
    def test_unexpected_error_returns_500(self):
        def usecase_quebrado(**kwargs):
            raise RuntimeError("falha inesperada")

        controller = UpdateUserController(usecase_quebrado)
        response = controller(make_request("456", "456", {"nome": "X"}))

        assert response.status_code == 500

    def test_invalid_token(self, controller):
        request = HttpRequest(body={"nome": "X"}, headers={"Authorization": "Bearer lixo"},
                            query_params={"user_id": "456"})
        assert controller(request).status_code == 401

    def test_forged_token_changes_nothing(self, controller, repo):
        futuro = datetime.now(timezone.utc) + timedelta(minutes=5)
        falso = jwt.encode({"sub": "456", "exp": futuro},
                        "outra-chave-qualquer-com-32-caracteres!", algorithm="HS256")
        request = HttpRequest(body={"nome": "Invasor"}, headers={"Authorization": f"Bearer {falso}"},
                            query_params={"user_id": "456"})

        assert controller(request).status_code == 401
        assert repo.get_user(456).nome == "Lucas"

    def test_old_header_no_longer_works(self, controller, repo):
        request = HttpRequest(body={"nome": "Invasor"}, headers={"X-Requester-Id": "456"},
                            query_params={"user_id": "456"})

        assert controller(request).status_code == 401
        assert repo.get_user(456).nome == "Lucas"