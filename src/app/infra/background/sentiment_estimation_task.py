from app.infra.background.configs.celery_config import settings as celery_settings
from app.infra.background.sentiment_estimation import BERTGRUSentiment, SentimentEstimator
from celery import current_app as current_celery_app
from celery_batches import Batches, SimpleRequest
from typing import List, Tuple
import math
from celery import shared_task
import psycopg2


class SentimentEstimationTask(Batches):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.estimator = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.estimator:
            if not self.estimator:
                self.estimator = SentimentEstimator(
                    model_path=celery_settings.NN_SENTIMENT_ESTIMATION_MODEL_PATH
                )
        return self.run(*args, **kwargs)


@shared_task(ignore_result=False,
          bind=True,
          flush_every=10,
          flush_interval=0.1,
          base=SentimentEstimationTask,
          path=('app.infra.background.sentiment_estimation', 'SentimentEstimator'),
          name=f'{__name__}, SentimentEstimator')
def estimate_sentiment_batch(self, simple_request: SimpleRequest):
    """
    Essentially the run method of PredictTask
    """
    comments: List[Tuple[int, str]] = simple_request[0].args[0]

    comment_ids, contents = zip(*comments)
    float_predictions = self.estimator.predict(contents)
    int_predictions = list(map(lambda e: math.ceil(e * 10), float_predictions))

    ids_sentiments = [(comment_id, prediction) for comment_id, prediction in  zip(comment_ids, int_predictions)]

    db_pool = current_celery_app.db_pool
    try:
        conn = db_pool.getconn()

        sql_expr = """UPDATE comments as T
                      SET sentiment = S.sentiment
                      FROM (VALUES %s) AS S(id, sentiment)
                      WHERE S.id = T.id"""

        cursor = conn.cursor()
        cursor.execute(sql_expr, ids_sentiments)
        cursor.close()
        conn.commit()
    except Exception as e:
        print('Failed to update comments table')
    finally:
        db_pool.putconn(conn)