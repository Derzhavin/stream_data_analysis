from app.core.entity import Comment as CommentModel
from app.core.service import ISentimentCommentEstimator
from app.infra.background import estimate_sentiment_batch


class SentimentCommentEstimator(ISentimentCommentEstimator):

    def estimate(self, comment: CommentModel):
        id = comment.id
        content = comment.content
        estimate_sentiment_batch.apply_async(args=[(id, content)])