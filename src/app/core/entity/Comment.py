from app.core.entity.Base import EntityMeta

from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    ForeignKey,
    CheckConstraint
)


class Comment(EntityMeta):
    __tablename__ = "comments"

    id = Column(Integer)
    content = Column(String(1000), nullable=False)
    sentiment = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    CheckConstraint("0 < sentiment < 11", name="sentiment_range_check")
    PrimaryKeyConstraint(id)