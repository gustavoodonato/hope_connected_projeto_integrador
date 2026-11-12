from typing import Optional
from werkzeug.security import generate_password_hash
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.entities.adress import Adress
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound

