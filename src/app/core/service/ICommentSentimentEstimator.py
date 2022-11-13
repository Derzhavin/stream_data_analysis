from app.core.entity import Comment as CommentModel

from abc import ABC, abstractmethod


class ISentimentCommentEstimator(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def estimate(self, comment: CommentModel):
        pass
