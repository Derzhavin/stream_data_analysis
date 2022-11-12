from abc import ABC, abstractmethod


class IUserAuthService(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def generate_hashed_password(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def generate_auth_data(self, **kwargs) -> dict:
        pass

    @abstractmethod
    def authenticate_user(self, **kwargs) -> str:
        pass