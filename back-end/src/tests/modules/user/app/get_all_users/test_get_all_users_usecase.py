import pytest
from src.modules.user.app.get_all_users.get_all_users_usecase import GetAllUsersUsecase
from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidToken
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

@pytest.fixture
def repo():
    return UserRepositoryMock()

@pytest.fixture
def usecase(repo):
    return GetAllUsersUsecase(repo)

class Test_GetAllUsersUsecase:
    def test_aacd_lists_fornecedores(self, usecase):
        users = usecase(requester_id=123)

        assert {u.nome for u in users} == {"Lucas", "Julio"}
        assert all(u.role == RoleEnum.FORNECEDOR for u in users)

    def test_list_does_not_include_aacd(self, usecase):
        users = usecase(requester_id=123)
        assert "Murilo" not in {u.nome for u in users}

    def test_new_fornecedor_appears_in_the_list(self, usecase, repo):
        repo.create_user(User(
            nome="Nova Loja", email="nova@loja.com", senha_hash="hash",
            role=RoleEnum.FORNECEDOR, phone="11999998888",
            endereco=Adress(cep="01023330", logradouro="Rua A", numero="1",
                            bairro="Centro", cidade="São Paulo", estado="SP")))

        assert len(usecase(requester_id=123)) == 3

    def test_empty_list_when_there_is_no_fornecedor(self, usecase, repo):
        repo.users = [repo.get_user(123)]
        assert usecase(requester_id=123) == []

    def test_fornecedor_cannot_list(self, usecase):
        with pytest.raises(ForbiddenAction):
            usecase(requester_id=456)

    def test_requester_that_does_not_exist(self, usecase):
        with pytest.raises(InvalidToken):
            usecase(requester_id=999)