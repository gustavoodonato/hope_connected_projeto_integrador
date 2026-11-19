from src.modules.user.app.update_user.update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_UpdateUserViewmodel:
    def test_to_dict_fornecedor(self):
        user = User(
            id=2, nome="Loja", email="loja@x.com", senha_hash="hash",
            role=RoleEnum.FORNECEDOR, phone="11999998888",
            endereco=Adress(cep="01023330", logradouro="Rua A", numero="1",
                            bairro="Centro", cidade="São Paulo", estado="SP"))

        result = UpdateUserViewmodel(user).to_dict()

        assert result["id"] == 2
        assert result["phone"] == "11999998888"
        assert isinstance(result["endereco"], dict)
        assert result["endereco"]["cidade"] == "São Paulo"

    def test_to_dict_aacd(self):
        user = User(id=1, nome="Ana", email="ana@aacd.org.br",
                    senha_hash="hash", role=RoleEnum.AACD)

        result = UpdateUserViewmodel(user).to_dict()

        assert result["phone"] is None
        assert result["endereco"] is None

    def test_never_returns_password(self):
        user = User(id=1, nome="Ana", email="ana@aacd.org.br",
                    senha_hash="hash_secreto", role=RoleEnum.AACD)

        result = UpdateUserViewmodel(user).to_dict()

        assert "senha_hash" not in result
        assert "hash_secreto" not in str(result)