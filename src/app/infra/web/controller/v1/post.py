from app.core.use_case import PostPublicationInteractor
from app.infra.web.repository import PostRepository, UserRepository
from app.infra.web.viewmodel.input import Post as PostIn
from app.infra.web.controller.v1.user import get_current_user
from app.infra.web.configs.database import (
    get_db_connection
)

from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page, Params
from contextlib import closing

PostRouter = APIRouter(prefix='/v1/posts')


@PostRouter.post("/", tags=['posts'])
async def publish_post(post_in: PostIn = Depends(), username: str = Depends(get_current_user)):
    with closing(next(get_db_connection())) as db:
        post_repository = PostRepository(db)
        user_repository = UserRepository(db)
        post_publish_interactor = PostPublicationInteractor(post_repository, user_repository)

        request_model = post_in.dict()
        request_model['username'] = username

        response_model = post_publish_interactor.publish_post(**request_model)

        if not response_model['status']:
            return status.HTTP_409_CONFLICT

        return status.HTTP_201_CREATED


@PostRouter.get("/", tags=['posts'])
async def get_posts(page: int = 1, size: int = 5):
    with closing(next(get_db_connection())) as db:
        post_repository = PostRepository(db)

        skip = (page - 1) * size
        limit = size

        posts, total = post_repository.list(skip, limit)

        params = Params()
        params.page = page
        params.size = size

        page = Page.create(posts, total, params)
        return page
