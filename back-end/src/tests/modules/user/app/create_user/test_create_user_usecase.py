import pytest
from werkzeug.security import check_password_hash

from src.modules.user.app.create_user.create_user_usecase import CreateUserUsecase
from src.shared.domain.entities.adress import Adress
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


@pytest.fixture
def repo():
    return UserRepositoryMock()


@pytest.fixture
def endereco():
    return Adress(cep="01023330", logradouro="Rua A", numero="1",
                  bairro="Centro", cidade="São Paulo", estado="SP")


class Test_CreateUserUsecase:
    def test_create_fornecedor(self, repo, endereco):
        user = CreateUserUsecase(repo)(
            nome="Ana", email="ana@loja.com", senha="123456",
            phone="11999998888", endereco=endereco)

        assert user.role == RoleEnum.FORNECEDOR
        assert user.phone == "11999998888"
        assert user.endereco.cidade == "São Paulo"
        assert user.id == 790
        assert len(repo.users) == 4

    def test_create_aacd_without_phone_and_endereco(self, repo):
        user = CreateUserUsecase(repo)(
            nome="Bia", email="bia@aacd.org.br", senha="123456")

        assert user.role == RoleEnum.AACD
        assert user.phone is None
        assert user.endereco is None

    def test_aacd_domain_is_case_insensitive(self, repo):
        user = CreateUserUsecase(repo)(
            nome="Bia", email="Bia@AACD.org.br", senha="123456")
        assert user.role == RoleEnum.AACD

    def test_similar_domain_is_fornecedor(self, repo, endereco):
        user = CreateUserUsecase(repo)(
            nome="Caio", email="caio@naoeaacd.org.br", senha="123456",
            phone="11999998888", endereco=endereco)
        assert user.role == RoleEnum.FORNECEDOR

    def test_password_is_saved_as_hash(self, repo):
        user = CreateUserUsecase(repo)(
            nome="Bia", email="bia@aacd.org.br", senha="123456")

        assert user.senha_hash != "123456"
        assert check_password_hash(user.senha_hash, "123456")
        assert not check_password_hash(user.senha_hash, "senha_errada")

    def test_duplicated_email(self, repo):
        with pytest.raises(DuplicatedItem):
            CreateUserUsecase(repo)(
                nome="Outro", email="muriloso123@gmail.com", senha="123456")
        assert len(repo.users) == 3

    def test_short_password(self, repo):
        with pytest.raises(EntityError):
            CreateUserUsecase(repo)(
                nome="Ana", email="ana@aacd.org.br", senha="12345")
        assert len(repo.users) == 3

    def test_fornecedor_without_phone(self, repo, endereco):
        with pytest.raises(EntityError):
            CreateUserUsecase(repo)(
                nome="Ana", email="ana@loja.com", senha="123456",
                endereco=endereco)

    def test_fornecedor_without_endereco(self, repo):
        with pytest.raises(EntityError):
            CreateUserUsecase(repo)(
                nome="Ana", email="ana@loja.com", senha="123456",
                phone="11999998888")