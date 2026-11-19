import pytest

from src.modules.user.app.delete_user.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserUsecase:
    def test_delete_own_user(self):
        repo = UserRepositoryMock()
        DeleteUserUsecase(repo)(user_id=456, requester_id=456)

        assert len(repo.users) == 2
        with pytest.raises(NoItemsFound):
            repo.get_user(456)

    def test_delete_other_user_is_forbidden(self):
        repo = UserRepositoryMock()
        with pytest.raises(ForbiddenAction):
            DeleteUserUsecase(repo)(user_id=456, requester_id=123)
        assert len(repo.users) == 3

    def test_forbidden_comes_before_not_found(self):
        with pytest.raises(ForbiddenAction):
            DeleteUserUsecase(UserRepositoryMock())(user_id=999, requester_id=123)

    def test_delete_user_not_found(self):
        with pytest.raises(NoItemsFound):
            DeleteUserUsecase(UserRepositoryMock())(user_id=999, requester_id=999)