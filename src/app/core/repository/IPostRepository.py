from app.core.entity import Post as PostModel
from app.core.entity import User as UserModel

from abc import ABC, abstractmethod
from typing import List
from typing import Union

class IPostRepository(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_post(self, post: PostModel, user: UserModel) -> bool:
        pass

    @abstractmethod
    def list(self, skip: int, limit: int) -> List[PostModel]:
        pass

    @abstractmethod
    def get_post_by_id(self, post_id: int) -> Union[PostModel, None]:
        pass
