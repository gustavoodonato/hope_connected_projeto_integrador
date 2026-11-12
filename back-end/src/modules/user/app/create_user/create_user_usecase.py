from typing import Optional
from werkzeug.security import generate_password_hash

from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound

DOMINIO_AACD = "@aacd.org.br"  # confirme o domínio real


def definir_role(email: str) -> RoleEnum:
    if email.lower().endswith(DOMINIO_AACD):
        return RoleEnum.AACD
    return RoleEnum.FORNECEDOR


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, nome: str, email: str, senha: str, phone: Optional[str] = None, endereco: Optional[Adress] = None) -> User:
        if len(senha) < 6:
            raise EntityError("senha")

        try:
            self.repo.get_user_by_email(email)
        except NoItemsFound:
            pass
        else:
            raise DuplicatedItem("email")

        user = User(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
            role=definir_role(email),
            phone=phone,
            endereco=endereco,
        )
        return self.repo.create_user(user)