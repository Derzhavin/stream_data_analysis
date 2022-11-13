from app.core.entity import User as UserModel
from app.core.entity import Post as PostModel
from app.core.entity import Comment as CommentModel

from abc import ABC, abstractmethod


class ICommentRepository(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_comment(self, comment: CommentModel, post: PostModel, user: UserModel) -> bool:
        pass

    @abstractmethod
    def list(self, skip: int, limit: int):
        pass
