from app.core.entity.Base import EntityMeta

from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    ForeignKey
)


class Comment(EntityMeta):
    __tablename__ = "comments"

    id = Column(Integer)
    content = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    PrimaryKeyConstraint(id)