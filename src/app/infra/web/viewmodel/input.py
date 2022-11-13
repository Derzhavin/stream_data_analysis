from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class Post(BaseModel):
    title: str
    content: str


class Comment(BaseModel):
    post_id: int
    content: str
