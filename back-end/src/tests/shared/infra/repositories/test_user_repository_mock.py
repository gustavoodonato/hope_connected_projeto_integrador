import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.entities.adress import Adress

class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user(int(123))

        assert user.id == int(123)
        assert user.nome == "Murilo"
        assert user.email == "muriloso123@gmail.com"
        assert user.phone == None
        assert user.endereco == None
        assert user.role == RoleEnum.AACD

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_user(user_id=int(999))

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            id=int(987),
            nome="Gustavo",
            email="gustavao061@gmail.com",
            phone="00999998888",
            endereco=Adress(
                cep="00111222",
                logradouro="Rua kasato maru",
                numero="200",
                complemento=None,
                bairro="Vila pires",
                cidade="Santo André",
                estado="SP"
            ),
            role=RoleEnum.FORNECEDOR,
        )

        repo.create_user(user)

        assert repo.users[3].id == int(987)
        assert repo.users[3].email == "gustavao061@gmail.com"
