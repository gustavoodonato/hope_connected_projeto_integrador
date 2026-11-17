from src.modules.user.app.get_user.get_user_viewmodel import GetUserViewmodel
from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_GetUserViewmodel:
    def test_to_dict_aacd(self):
        user = User(id=1, nome="Ana", email="ana@aacd.org.br",
                    senha_hash="hash", role=RoleEnum.AACD)

        result = GetUserViewmodel(user).to_dict()

        assert result["id"] == 1
        assert result["nome"] == "Ana"
        assert result["email"] == "ana@aacd.org.br"
        assert result["role"] == RoleEnum.AACD.value
        assert result["phone"] is None
        assert result["endereco"] is None

    def test_to_dict_fornecedor(self):
        user = User(
            id=2, nome="Loja", email="loja@x.com", senha_hash="hash",
            role=RoleEnum.FORNECEDOR, phone="11999998888",
            endereco=Adress(cep="01023330", logradouro="Rua A", numero="1",
                            bairro="Centro", cidade="São Paulo", estado="SP"))

        result = GetUserViewmodel(user).to_dict()

        assert result["role"] == RoleEnum.FORNECEDOR.value
        assert result["phone"] == "11999998888"
        assert isinstance(result["endereco"], dict) 
        assert result["endereco"]["cidade"] == "São Paulo"

    def test_never_returns_password(self):
        user = User(id=1, nome="Ana", email="ana@aacd.org.br",
                    senha_hash="hash_secreto", role=RoleEnum.AACD)

        result = GetUserViewmodel(user).to_dict()

        assert "senha_hash" not in result
        assert "senha" not in result
        assert "hash_secreto" not in str(result)