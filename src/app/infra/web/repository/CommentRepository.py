from app.core.entity import (
    User as UserModel,
    Post as PostModel,
    Comment as CommentModel
)
from app.core.repository import ICommentRepository

from sqlalchemy.orm import Session


class CommentRepository(ICommentRepository):

    def __init__(self, db: Session):
        super(CommentRepository, self).__init__()
        self.db = db

    def list(self, skip: int = 0, limit: int = 5):
        query = self.db.query(CommentModel)
        total = query.count()
        items = query.limit(limit).offset(skip).all()

        return items, total
    
    def create_comment(self, comment: CommentModel, post: PostModel, user: UserModel) -> bool:
        try:
            post.comments.append(comment)
            user.comments.append(comment)
            self.db.commit()
        except Exception as ex:
            return False
        return True
