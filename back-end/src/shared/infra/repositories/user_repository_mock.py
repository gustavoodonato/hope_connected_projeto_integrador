from typing import List
from werkzeug.security import generate_password_hash
from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        senha_hash = generate_password_hash("senha123")
        
        self.users = [
            User(
                id=123,
                nome="Murilo",
                email="muriloso123@gmail.com",
                senha_hash=senha_hash,
                phone=None,
                endereco=None,
                role=RoleEnum.AACD,
            ),
            User(
                id=456,
                nome="Lucas",
                email="luquinhas24@gmail.com",
                senha_hash=senha_hash,
                phone="55444446666",
                endereco=Adress(
                    cep="00111222",
                    logradouro="Rua catapimbas da silva",
                    numero="323",
                    complemento=None,
                    bairro="Vila Assunção",
                    cidade="São Caetano do Sul",
                    estado="SP",
                ),
                role=RoleEnum.FORNECEDOR,
            ),
            User(
                id=789,
                nome="Julio",
                email="juliao323@gmail.com",
                senha_hash=senha_hash,
                phone="22333334444",
                endereco=Adress(
                    cep="00111222",
                    logradouro="Rua belterra",
                    numero="291",
                    complemento=None,
                    bairro="Santo amaro",
                    cidade="São Paulo",
                    estado="SP",
                ),
                role=RoleEnum.FORNECEDOR,
            ),
        ]

    def create_user(self, new_user: User) -> User:
        self.users.append(new_user)
        return new_user

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if str(user.id) == str(user_id):
                return user
        raise NoItemsFound("user_id")

    def get_user_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user
        raise NoItemsFound("email")