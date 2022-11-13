from fastapi import APIRouter

IndexRouter = APIRouter(prefix='/v1')


@IndexRouter.get("/", tags=['root'])
async def index():
    return {"message": "Aloha from v.1!"}