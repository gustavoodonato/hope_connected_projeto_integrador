from typing import Optional

from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: int, requester_id: int, nome: Optional[str] = None, phone: Optional[str] = None, endereco: Optional[Adress] = None) -> User:
        if str(user_id) != str(requester_id):
            raise ForbiddenAction("alterar outro usuário")

        user = self.repo.get_user(user_id)

        mudancas = {}
        if nome is not None:
            mudancas["nome"] = nome
        if phone is not None:
            mudancas["phone"] = phone
        if endereco is not None:
            mudancas["endereco"] = endereco

        atualizado = User(**{**user.model_dump(), **mudancas})
        return self.repo.update_user(atualizado)