import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from src.shared.domain.entities.user import User
from src.shared.domain.entities.adress import Adress
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user(123)

        assert user.id == 123
        assert user.nome == "Murilo"
        assert user.email == "muriloso123@gmail.com"
        assert check_password_hash(user.senha_hash, "senha123")
        assert user.phone is None
        assert user.endereco is None
        assert user.role == RoleEnum.AACD

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_user(user_id=999)

    def test_get_user_by_email(self):
        repo = UserRepositoryMock()
        user = repo.get_user_by_email("luquinhas24@gmail.com")

        assert user.id == 456
        assert user.nome == "Lucas"
        assert user.role == RoleEnum.FORNECEDOR
        assert check_password_hash(user.senha_hash, "senha123")

    def test_get_user_by_email_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_user_by_email("naoexiste@gmail.com")

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            id=987,
            nome="Gustavo",
            email="gustavao061@gmail.com",
            senha_hash=generate_password_hash("outrasenha"),
            phone="00999998888",
            endereco=Adress(
                cep="00111222",
                logradouro="Rua kasato maru",
                numero="200",
                complemento=None,
                bairro="Vila pires",
                cidade="Santo André",
                estado="SP",
            ),
            role=RoleEnum.FORNECEDOR,
        )

        repo.create_user(user)

        assert len(repo.users) == 4
        assert repo.users[-1].id == 987
        assert repo.users[-1].email == "gustavao061@gmail.com"
        assert repo.get_user_by_email("gustavao061@gmail.com").id == 987
