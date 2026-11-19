import pytest

from src.modules.user.app.update_user.update_user_usecase import UpdateUserUsecase
from src.shared.domain.entities.adress import Adress
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:
    def test_update_nome_keeps_the_rest(self):
        repo = UserRepositoryMock()
        antes = repo.get_user(456)

        user = UpdateUserUsecase(repo)(user_id=456, requester_id=456, nome="Lucas Novo")

        assert user.nome == "Lucas Novo"
        assert user.email == antes.email
        assert user.role == antes.role
        assert user.senha_hash == antes.senha_hash
        assert user.endereco == antes.endereco
        assert repo.get_user(456).nome == "Lucas Novo"   # foi salvo

    def test_update_endereco_and_phone(self):
        repo = UserRepositoryMock()
        novo = Adress(cep="04567-000", logradouro="Rua B", numero="9",
                      bairro="Moema", cidade="São Paulo", estado="sp")

        user = UpdateUserUsecase(repo)(user_id=456, requester_id=456,
                                       phone="11911112222", endereco=novo)

        assert user.phone == "11911112222"
        assert user.endereco.cep == "04567000"
        assert user.endereco.estado == "SP"

    def test_update_aacd_nome(self):
        user = UpdateUserUsecase(UserRepositoryMock())(
            user_id=123, requester_id=123, nome="Murilo Novo")
        assert user.nome == "Murilo Novo"
        assert user.endereco is None

    def test_update_other_user_is_forbidden(self):
        repo = UserRepositoryMock()
        with pytest.raises(ForbiddenAction):
            UpdateUserUsecase(repo)(user_id=456, requester_id=123, nome="Invasor")
        assert repo.get_user(456).nome == "Lucas"        # nada mudou

    def test_forbidden_comes_before_not_found(self):
        # id inexistente pedido por outra conta: 403 e não 404
        with pytest.raises(ForbiddenAction):
            UpdateUserUsecase(UserRepositoryMock())(user_id=999, requester_id=123, nome="X")

    def test_update_user_not_found(self):
        with pytest.raises(NoItemsFound):
            UpdateUserUsecase(UserRepositoryMock())(user_id=999, requester_id=999, nome="X")

    def test_fornecedor_cannot_lose_phone(self):
        repo = UserRepositoryMock()
        with pytest.raises(EntityError):
            UpdateUserUsecase(repo)(user_id=456, requester_id=456, phone="")
        assert repo.get_user(456).phone == "55444446666"   # nada mudou