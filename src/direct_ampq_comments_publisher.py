from app.infra.web.service import SentimentCommentEstimator
from app.infra.web.configs.database import get_db_connection
from app.core.use_case import CommentPublicationInteractor
from app.infra.web.repository import (
    PostRepository,
    UserRepository,
    CommentRepository
)

import time

COMMENTS_NUM = 100
CONTENT = "Throughout the rest of its running time, “Black Adam” leans into the inevitability of Adam’s evolution toward good-guy status, condensing the transformation of the title character in the first two “Terminator” films (there are even comic bits where people try to teach Adam sarcasm and the Geneva Conventions). \"Black Adam\" then stirs in dollops of a macho sentimentality that used to be common in old Hollywood dramas about loners who needed to get involved in a cause in order to reset their moral compasses or recognize their own worth. But the sharp edge that the film brings to the early parts of its story never dulls."

db = next(get_db_connection())
post_repository = PostRepository(db)
user_repository = UserRepository(db)
comment_repository = CommentRepository(db)
sentiment_comment_estimator = SentimentCommentEstimator()
comment_publication_interactor = CommentPublicationInteractor(
    comment_repository=comment_repository,
    post_repository=post_repository,
    user_repository=user_repository,
    sentiment_comment_estimator=sentiment_comment_estimator
)
request_model = {
    "username": "denis",
    "post_id": 1,
    "content": CONTENT
}
while True:
    begin_t = time.time()
    response_model = comment_publication_interactor.publish_comment(**request_model)
    end_t = time.time()
    delta_t = end_t - begin_t

    print(f' time: {delta_t * 1000:.0f} ms')