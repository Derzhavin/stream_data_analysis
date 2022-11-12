from app.core.service import IUserAuthService
from app.configs import security as security_config

import datetime
from jose import jwt, JWTError
from passlib.context import CryptContext


class UserAuthService(IUserAuthService):
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def generate_hashed_password(self, username: str, password: str) -> str:
        return self.__pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.__pwd_context.verify(plain_password, hashed_password)

    def generate_auth_data(self, **input_data) -> dict:
        auth_data = input_data.copy()
        auth_data["expiration"] = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = jwt.encode(auth_data, security_config.SECRET_KEY, algorithm=security_config.ALGORITHM)
        auth_data['access_token'] = access_token

        return auth_data

    def authenticate_user(self, **kwargs) -> str:
        try:
            access_token = kwargs.get('access_token')
            payload = jwt.decode(access_token, security_config.SECRET_KEY, algorithms=[security_config.ALGORITHM])
            username: str = payload.get("sub")
        except JWTError:
            return ""

        return username
