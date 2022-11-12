from sqlalchemy.orm import relationship

from app.core.entity.Base import EntityMeta

from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
)


class User(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer)
    username = Column(String(50), nullable=False)
    hashed_password = Column(String(256), nullable=False)
    comments = relationship('Comment', backref='user')
    posts = relationship('Post', backref='user')

    PrimaryKeyConstraint(id)