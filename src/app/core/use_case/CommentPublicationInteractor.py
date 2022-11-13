from app.core.repository import (
    IUserRepository,
    IPostRepository,
    ICommentRepository,
)
from app.core.entity import (
    Post as PostModel,
    User as UserModel,
    Comment as CommentModel
)


class CommentPublicationInteractor:

    def __init__(self, comment_repository: ICommentRepository, post_repository: IPostRepository, user_repository: IUserRepository):
        self.__comment_repository = comment_repository
        self.__post_repository = post_repository
        self.__user_repository = user_repository

    def publish_comment(self, **kwargs) -> dict:
        username = kwargs.get('username')
        post_id = kwargs.get('post_id')
        content = kwargs.get('content')
        response_model = {'status': False}

        post: PostModel = self.__post_repository.get_post_by_id(post_id)

        if not post:
            response_model['error'] = 'no such post'
            return response_model

        user: UserModel = self.__user_repository.get_user_by_username(username)

        if not user:
            response_model['error'] = 'no such user'
            return response_model

        comment = CommentModel(content=content, sentiment=10)
        self.__comment_repository.create_comment(comment=comment, post=post, user=user)

        response_model['status'] = True
        return response_model
