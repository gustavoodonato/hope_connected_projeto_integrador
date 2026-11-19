from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class DeleteUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: int, requester_id: int) -> User:
        if str(user_id) != str(requester_id):
            raise ForbiddenAction("apagar outro usuário")
        return self.repo.delete_user(user_id)