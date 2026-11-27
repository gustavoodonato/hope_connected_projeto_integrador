from src.modules.user.app.get_all_users.get_all_users_viewmodel import GetAllUsersViewmodel
from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum

def fornecedor(id_, nome, cidade="São Paulo"):
    return User(
        id=id_, nome=nome, email=f"{nome.lower()}@loja.com", senha_hash="hash_secreto",
        role=RoleEnum.FORNECEDOR, phone="11999998888",
        endereco=Adress(cep="01023330", logradouro="Rua A", numero="1",
                        bairro="Centro", cidade=cidade, estado="SP"))


class Test_GetAllUsersViewmodel:
    def test_to_dict(self):
        result = GetAllUsersViewmodel([fornecedor(1, "Ana"), fornecedor(2, "Bia", "Santo André")]).to_dict()

        assert result["total"] == 2
        assert result["users"][0] == {"id": 1, "nome": "Ana", "cidade": "São Paulo", "estado": "SP"}
        assert result["users"][1]["cidade"] == "Santo André"

    def test_only_public_fields(self):
        result = GetAllUsersViewmodel([fornecedor(1, "Ana")]).to_dict()
        assert set(result["users"][0].keys()) == {"id", "nome", "cidade", "estado"}

    def test_never_exposes_contact_or_password(self):
        texto = str(GetAllUsersViewmodel([fornecedor(1, "Ana")]).to_dict())

        assert "ana@loja.com" not in texto
        assert "11999998888" not in texto
        assert "hash_secreto" not in texto
        assert "senha_hash" not in texto

    def test_empty_list(self):
        result = GetAllUsersViewmodel([]).to_dict()

        assert result["users"] == []
        assert result["total"] == 0