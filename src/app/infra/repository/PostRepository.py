from app.core.entity import (
    Post as PostModel,
    User as UserModel
)
from app.core.repository import IPostRepository

from sqlalchemy.orm import Session
from typing import Union


class PostRepository(IPostRepository):

    def __init__(self, db: Session):
        super(PostRepository, self).__init__()
        self.db = db

    def create_post(self, post: PostModel, user: UserModel) -> bool:
        try:
            user.posts.append(post)
            self.db.commit()
        except:
            return False
        return True

    def list(self, skip: int = 0, limit: int = 5):
        query = self.db.query(PostModel)
        total = query.count()
        items = query.limit(limit).offset(skip).all()

        return items, total

    def get_post_by_id(self, post_id: int) -> Union[PostModel, None]:
        post = self.db.query(PostModel).filter(PostModel.id == post_id).first()

        if not post:
            return None
        return post
