from app.core.repository import IUserRepository
from app.core.entity import User as UserModel
from app.core.service import IUserAuth


class UserAuthInteractor:

    def __init__(self, user_repository: IUserRepository, user_auth_service: IUserAuth):
        self.__user_repository = user_repository
        self.__user_auth_service = user_auth_service

    def register_user(self, **kwargs) -> dict:
        username = kwargs.get('username')
        plain_password = kwargs.get('password')
        response_model = {'status': False}

        hashed_password = self.__user_auth_service.generate_hashed_password(username, plain_password)
        user = UserModel(username=username, hashed_password=hashed_password)

        if not self.__user_repository.create_user(user):
            response_model['error'] = 'user exists'
            return response_model

        response_model['status'] = True
        return response_model

    def authorize_user(self, **kwargs) -> dict:
        username = kwargs.get('username')
        plain_password = kwargs.get('password')
        response_model = {'status': False}

        user = self.__user_repository.get_user_by_username(username)

        if not user:
            return response_model

        hashed_password = user.hashed_password

        if not self.__user_auth_service.verify_password(plain_password, hashed_password):
            response_model['error'] = 'incorrect user or password'
            return response_model

        auth_input_data = {"sub": user.username}
        auth_data = self.__user_auth_service.generate_auth_data(**auth_input_data)

        response_model.update(auth_data)
        response_model['user'] = user
        response_model['status'] = True
        return response_model

    def authenticate_user(self, **kwargs) -> dict:
        response_model = {'status': False}
        username = self.__user_auth_service.authenticate_user(**kwargs)

        if username == "":
            response_model['error'] = 'no such user'
            return response_model

        user = self.__user_repository.get_user_by_username(username)

        response_model['user'] = user
        response_model['status'] = True
        return response_model
