from werkzeug.security import check_password_hash
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound, WrongCredentials

class LoginUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str, senha: str) -> User:
        try:
            user = self.repo.get_user_by_email(email)
        except NoItemsFound:
            raise WrongCredentials()

        if not check_password_hash(user.senha_hash, senha):
            raise WrongCredentials()

        return user