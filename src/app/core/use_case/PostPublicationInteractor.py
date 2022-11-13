from app.core.repository import IPostRepository, IUserRepository
from app.core.entity import (
    Post as PostModel,
    User as UserModel
)


class PostPublicationInteractor:

    def __init__(self, post_repository: IPostRepository, user_repository: IUserRepository):
        self.__post_repository = post_repository
        self.__user_repository = user_repository

    def publish_post(self, **kwargs) -> dict:
        username = kwargs.get('username')
        title = kwargs.get('title')
        content = kwargs.get('content')
        response_model = {'status': False}

        user: UserModel = self.__user_repository.get_user_by_username(username)
        post = PostModel(content=content, title=title)

        if not self.__post_repository.create_post(post, user):
            response_model['error'] = 'unexpected error'
            return response_model

        response_model['status'] = True
        return response_model
