from sqlalchemy.orm import relationship

from app.core.entity.Base import EntityMeta

from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    ForeignKey
)


class Post(EntityMeta):
    __tablename__ = "posts"

    id = Column(Integer)
    title = Column(String(100), nullable=False)
    content = Column(String(10000), nullable=False)
    comments = relationship('Comment', backref='post')

    user_id = Column(Integer, ForeignKey("users.id"))

    PrimaryKeyConstraint(id)