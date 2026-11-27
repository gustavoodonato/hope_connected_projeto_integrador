from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidToken, NoItemsFound

class GetAllUsersUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, requester_id: int) -> List[User]:
        try:
            requester = self.repo.get_user(requester_id)
        except NoItemsFound:
            raise InvalidToken()

        if requester.role != RoleEnum.AACD:
            raise ForbiddenAction("listar usuários")

        return [u for u in self.repo.get_all_users() if u.role == RoleEnum.FORNECEDOR]