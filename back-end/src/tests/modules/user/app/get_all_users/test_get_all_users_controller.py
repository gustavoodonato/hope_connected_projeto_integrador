from datetime import datetime, timedelta, timezone

import jwt
import pytest

from src.modules.user.app.get_all_users.get_all_users_controller import GetAllUsersController
from src.modules.user.app.get_all_users.get_all_users_usecase import GetAllUsersUsecase
from src.shared.domain.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.token_handler import TokenHandler
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.auth import auth


@pytest.fixture
def controller():
    return GetAllUsersController(GetAllUsersUsecase(UserRepositoryMock()))


def make_request(requester_id=None):
    headers = auth(requester_id) if requester_id is not None else {}
    return HttpRequest(headers=headers)


class Test_GetAllUsersController:
    # --- sucesso ---
    def test_aacd_lists_fornecedores(self, controller):
        response = controller(make_request(123))

        assert response.status_code == 200
        assert response.body["total"] == 2
        assert {u["nome"] for u in response.body["users"]} == {"Lucas", "Julio"}

    def test_response_never_leaks_contact_or_password(self, controller):
        texto = str(controller(make_request(123)).body)

        assert "luquinhas24@gmail.com" not in texto
        assert "55444446666" not in texto
        assert "senha_hash" not in texto

    # --- permissão ---
    def test_fornecedor_is_forbidden(self, controller):
        assert controller(make_request(456)).status_code == 403

    def test_token_of_a_user_that_does_not_exist(self, controller):
        assert controller(make_request(999)).status_code == 401

    # --- token ---
    def test_missing_token(self, controller):
        assert controller(make_request()).status_code == 401

    def test_invalid_token(self, controller):
        request = HttpRequest(headers={"Authorization": "Bearer lixo"})
        assert controller(request).status_code == 401

    def test_expired_token(self, controller):
        token = TokenHandler.generate(123, expira_em_minutos=-1)
        request = HttpRequest(headers={"Authorization": f"Bearer {token}"})
        assert controller(request).status_code == 401

    def test_forged_token(self, controller):
        futuro = datetime.now(timezone.utc) + timedelta(minutes=5)
        falso = jwt.encode({"sub": "123", "exp": futuro},
                           "outra-chave-qualquer-com-32-caracteres!", algorithm="HS256")
        request = HttpRequest(headers={"Authorization": f"Bearer {falso}"})
        assert controller(request).status_code == 401

    def test_old_header_no_longer_works(self, controller):
        request = HttpRequest(headers={"X-Requester-Id": "123"})
        assert controller(request).status_code == 401

    # --- erro inesperado ---
    def test_unexpected_error_returns_500(self):
        def usecase_quebrado(**kwargs):
            raise RuntimeError("falha inesperada")

        controller = GetAllUsersController(usecase_quebrado)
        assert controller(make_request(123)).status_code == 500