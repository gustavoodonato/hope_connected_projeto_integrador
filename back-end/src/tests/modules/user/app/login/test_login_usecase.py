import pytest

from src.modules.user.app.login.login_usecase import LoginUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import WrongCredentials
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


@pytest.fixture
def usecase():
    return LoginUsecase(UserRepositoryMock())


class Test_LoginUsecase:
    def test_login_aacd(self, usecase):
        user = usecase(email="muriloso123@gmail.com", senha="senha123")
        assert user.id == 123
        assert user.role == RoleEnum.AACD

    def test_login_fornecedor(self, usecase):
        user = usecase(email="luquinhas24@gmail.com", senha="senha123")
        assert user.id == 456
        assert user.role == RoleEnum.FORNECEDOR

    def test_wrong_password(self, usecase):
        with pytest.raises(WrongCredentials):
            usecase(email="muriloso123@gmail.com", senha="senha_errada")

    def test_unknown_email(self, usecase):
        with pytest.raises(WrongCredentials):
            usecase(email="naoexiste@gmail.com", senha="senha123")

    def test_empty_password(self, usecase):
        with pytest.raises(WrongCredentials):
            usecase(email="muriloso123@gmail.com", senha="")

    def test_unknown_email_and_wrong_password_look_the_same(self, usecase):
        with pytest.raises(WrongCredentials) as erro_email:
            usecase(email="naoexiste@gmail.com", senha="senha123")
        with pytest.raises(WrongCredentials) as erro_senha:
            usecase(email="muriloso123@gmail.com", senha="errada")

        assert str(erro_email.value) == str(erro_senha.value)