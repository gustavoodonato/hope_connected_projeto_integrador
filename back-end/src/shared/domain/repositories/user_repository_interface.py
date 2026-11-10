from abc import ABC, abstractmethod
from typing import List
from src.shared.domain.entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, new_user: User) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass