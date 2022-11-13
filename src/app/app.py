from fastapi import FastAPI

from app.configs.environment import get_environment_variables
from app.core.entity.Base import init_db
from app.infra.controller.v1 import IndexRouter, UserRouter


def create_app():
    env = get_environment_variables()

    app = FastAPI(
        title=env.APP_NAME,
        version=env.API_VERSION,
    )
    app.include_router(IndexRouter)
    app.include_router(UserRouter)

    init_db()

    return app


app = create_app()