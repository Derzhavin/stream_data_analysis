from app.core.entity import User as UserModel

from abc import ABC, abstractmethod


class IUserRepository(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_user(self, user: UserModel) -> bool:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str):
        pass
