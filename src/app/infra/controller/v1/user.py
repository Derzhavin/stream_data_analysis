from app.core.use_case import UserInteractor

from app.infra.viewmodel.input import (
    User as UserIn
)
from app.infra.repository import UserRepository
from app.infra.service import UserAuthService

from app.configs.database import (
    get_db_connection
)

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

UserRouter = APIRouter(prefix='/v1/users')


@UserRouter.post("/login", tags=['users'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_repository = UserRepository(next(get_db_connection()))
    user_auth_service = UserAuthService()
    user_interactor = UserInteractor(user_repository, user_auth_service)

    request_model = {
        'username': form_data.username,
        'password': form_data.password
    }
    response_model = user_interactor.authorize_user(**request_model)

    if not response_model['status']:
        raise HTTPException(status_code=400, detail=response_model['error'])

    view_out = {
        'access_token': response_model['access_token'],
        'token_type': "bearer"
    }
    return view_out


async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl='/v1/users/login'))):
    user_repository = UserRepository(next(get_db_connection()))
    user_auth_service = UserAuthService()
    user_interactor = UserInteractor(user_repository, user_auth_service)

    request_model = {
        'access_token': token
    }
    response_model = user_interactor.authenticate_user(**request_model)

    if not response_model['status']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = response_model['user']
    return user


@UserRouter.post("/register", tags=['users'])
async def register_user(user_in: UserIn):
    user_repository = UserRepository(next(get_db_connection()))
    user_auth_service = UserAuthService()
    user_interactor = UserInteractor(user_repository, user_auth_service)

    request_model = user_in.dict()
    response_model = user_interactor.register_user(**request_model)

    if not response_model['status']:
        return status.HTTP_409_CONFLICT

    return status.HTTP_201_CREATED


@UserRouter.get("/private", tags=['users'])
async def private(username: str = Depends(get_current_user)):
    return username
