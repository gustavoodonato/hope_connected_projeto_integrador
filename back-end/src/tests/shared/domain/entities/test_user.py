import pytest
from pydantic import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from src.shared.domain.entities.user import User
from src.shared.domain.entities.adress import Adress
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError


@pytest.fixture
def senha_hash():
    return generate_password_hash("senha123")


@pytest.fixture
def endereco():
    return Adress(
        cep="01023-330",
        logradouro="Rua catapimbas da silva",
        numero="323",
        complemento=None,
        bairro="Vila Assunção",
        cidade="São Caetano",
        estado="sp",
    )


class Test_User:
    def test_fornecedor_creation_success(self, endereco, senha_hash):
        user = User(
            id=123,
            nome="username_test",
            email="teste@teste.com",
            senha_hash=senha_hash,
            role=RoleEnum.FORNECEDOR,
            phone="11222223333",
            endereco=endereco,
        )
        assert user.id == 123
        assert user.senha_hash != "senha123"
        assert check_password_hash(user.senha_hash, "senha123")
        assert not check_password_hash(user.senha_hash, "senha_errada")
        assert user.endereco.cep == "01023330"
        assert user.endereco.estado == "SP"

    def test_aacd_creation_success_without_address(self, senha_hash):
        user = User(
            nome="funcionario_aacd",
            email="func@aacd.org.br",
            senha_hash=senha_hash,
            role=RoleEnum.AACD,
        )
        assert user.phone is None
        assert user.endereco is None

    def test_fornecedor_without_endereco(self, senha_hash):
        with pytest.raises(EntityError):
            User(
                nome="fornecedor",
                email="loja@teste.com",
                senha_hash=senha_hash,
                role=RoleEnum.FORNECEDOR,
                phone="11222223333",
            )

    def test_fornecedor_without_phone(self, endereco, senha_hash):
        with pytest.raises(EntityError):
            User(
                nome="fornecedor",
                email="loja@teste.com",
                senha_hash=senha_hash,
                role=RoleEnum.FORNECEDOR,
                endereco=endereco,
            )

    def test_user_without_senha_hash(self):
        with pytest.raises(EntityError):
            User(
                nome="usuario",
                email="teste@teste.com",
                role=RoleEnum.AACD,
            )

    def test_user_invalid_email(self, senha_hash):
        with pytest.raises(EntityError):
            User(
                nome="usuario",
                email="email_invalido",
                senha_hash=senha_hash,
                role=RoleEnum.AACD,
            )

    def test_user_invalid_role(self, senha_hash):
        with pytest.raises(EntityError):
            User(
                nome="usuario",
                email="teste@teste.com",
                senha_hash=senha_hash,
                role="ROLE_INVALIDA",
            )

    def test_adress_invalid_cep(self):
        with pytest.raises(ValidationError):
            Adress(
                cep="0102333",
                logradouro="Rua A",
                numero="1",
                bairro="Centro",
                cidade="São Paulo",
                estado="SP",
            )