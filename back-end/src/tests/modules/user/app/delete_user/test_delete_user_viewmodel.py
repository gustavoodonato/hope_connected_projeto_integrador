from src.modules.user.app.delete_user.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_DeleteUserViewmodel:
    def test_to_dict(self):
        user = User(id=1, nome="Ana", email="ana@aacd.org.br",
                    senha_hash="hash", role=RoleEnum.AACD)

        result = DeleteUserViewmodel(user).to_dict()

        assert result["id"] == 1
        assert result["nome"] == "Ana"
        assert result["email"] == "ana@aacd.org.br"
        assert result["message"] == "Usuário removido com sucesso"

    def test_never_returns_sensitive_data(self):
        user = User(
            id=2, nome="Loja", email="loja@x.com", senha_hash="hash_secreto",
            role=RoleEnum.FORNECEDOR, phone="11999998888",
            endereco=Adress(cep="01023330", logradouro="Rua A", numero="1",
                            bairro="Centro", cidade="São Paulo", estado="SP"))

        result = DeleteUserViewmodel(user).to_dict()

        assert "senha_hash" not in result
        assert "hash_secreto" not in str(result)
        assert "phone" not in result
        assert "endereco" not in result