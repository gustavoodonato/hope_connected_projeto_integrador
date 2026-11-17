import pytest

from src.modules.user.app.get_user.get_user_usercase import GetUserUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


@pytest.fixture
def usecase():
    return GetUserUsecase(UserRepositoryMock())


class Test_GetUserUsecase:
    def test_get_own_aacd(self, usecase):
        user = usecase(user_id=123, requester_id=123)

        assert user.id == 123
        assert user.nome == "Murilo"
        assert user.role == RoleEnum.AACD
        assert user.phone is None
        assert user.endereco is None

    def test_get_own_fornecedor(self, usecase):
        user = usecase(user_id=456, requester_id=456)

        assert user.nome == "Lucas"
        assert user.role == RoleEnum.FORNECEDOR
        assert user.phone == "55444446666"
        assert user.endereco.cidade == "São Caetano do Sul"

    def test_ids_as_text_and_number_are_equivalent(self, usecase):
        user = usecase(user_id="456", requester_id=456)
        assert user.id == 456

    def test_get_other_user_is_forbidden(self, usecase):
        with pytest.raises(ForbiddenAction):
            usecase(user_id=456, requester_id=123)

    def test_fornecedor_cannot_get_another_fornecedor(self, usecase):
        with pytest.raises(ForbiddenAction):
            usecase(user_id=789, requester_id=456)

    def test_forbidden_comes_before_not_found(self, usecase):
        with pytest.raises(ForbiddenAction):
            usecase(user_id=999, requester_id=123)

    def test_user_not_found(self, usecase):
        with pytest.raises(NoItemsFound):
            usecase(user_id=999, requester_id=999)