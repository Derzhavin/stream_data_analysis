from app.core.use_case import CommentPublicationInteractor
from app.infra.repository import (
    PostRepository,
    UserRepository,
    CommentRepository
)
from app.infra.viewmodel.input import Comment as CommentIn
from app.infra.controller.v1.user import get_current_user
from app.configs.database import (
    get_db_connection
)

from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page, Params

CommentRouter = APIRouter(prefix='/v1/comments')


@CommentRouter.post("/", tags=['comments'])
async def publish_comment(comment_in: CommentIn = Depends(), username: str = Depends(get_current_user)):
    db = next(get_db_connection())
    post_repository = PostRepository(db)
    user_repository = UserRepository(db)
    comment_repository = CommentRepository(db)
    comment_publication_interactor = CommentPublicationInteractor(
        comment_repository=comment_repository,
        post_repository=post_repository,
        user_repository=user_repository
    )

    request_model = comment_in.dict()
    request_model['username'] = username

    response_model = comment_publication_interactor.publish_comment(**request_model)

    if not response_model['status']:
        return status.HTTP_409_CONFLICT

    return status.HTTP_201_CREATED


@CommentRouter.get("/", tags=['comments'])
async def get_comments(page: int = 1, size: int = 5):
    db = next(get_db_connection())
    comment_repository = CommentRepository(db)

    skip = (page - 1) * size
    limit = size

    comments, total = comment_repository.list(skip, limit)

    params = Params()
    params.page = page
    params.size = size

    page = Page.create(comments, total, params)
    return page