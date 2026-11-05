import pytest
from pydantic import ValidationError

from src.shared.domain.entities.user import User
from src.shared.domain.entities.adress import Adress
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.helpers.errors.domain_errors import EntityError


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
    def test_fornecedor_creation_success(self, endereco):
        user = User(
            id=123,
            nome="username_test",
            email="teste@teste.com",
            role=RoleEnum.FORNECEDOR,
            phone="11222223333",
            endereco=endereco,
        )
        assert user.id == 123
        assert user.nome == "username_test"
        assert user.email == "teste@teste.com"
        assert user.role == RoleEnum.FORNECEDOR
        assert user.phone == "11222223333"
        assert user.endereco.cep == "01023330"
        assert user.endereco.estado == "SP"

    def test_aacd_creation_success_without_address(self):
        user = User(
            nome="funcionario_aacd",
            email="func@aacd.org.br",
            role=RoleEnum.AACD,
        )
        assert user.phone is None
        assert user.endereco is None

    def test_fornecedor_without_endereco(self):
        with pytest.raises(EntityError):
            User(
                nome="fornecedor",
                email="loja@teste.com",
                role=RoleEnum.FORNECEDOR,
                phone="11222223333",
            )

    def test_fornecedor_without_phone(self, endereco):
        with pytest.raises(EntityError):
            User(
                nome="fornecedor",
                email="loja@teste.com",
                role=RoleEnum.FORNECEDOR,
                endereco=endereco,
            )

    def test_user_invalid_email(self):
        with pytest.raises(EntityError):
            User(
                nome="usuario",
                email="email_invalido",
                role=RoleEnum.AACD,
            )

    def test_user_invalid_role(self):
        with pytest.raises(EntityError):
            User(
                nome="usuario",
                email="teste@teste.com",
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