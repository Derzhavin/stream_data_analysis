from app.core.entity import User as UserModel

from abc import ABC, abstractmethod


class IUserRepository(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_user(self, user: UserModel):
        pass

    @abstractmethod
    def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    def is_username_exists(self, username: str):
        pass
