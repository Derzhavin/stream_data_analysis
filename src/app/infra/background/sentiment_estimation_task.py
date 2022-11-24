import importlib.util
import os

from app.infra.background.configs.celery_config import settings as celery_settings
# from app.infra.background.sentiment_estimation import BERTGRUSentiment, SentimentEstimator
from celery import current_app as current_celery_app
from celery_batches import Batches, SimpleRequest
from typing import List, Tuple
import math
from celery import shared_task
from contextlib import closing
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
            # self.estimator = SentimentEstimator(
            #     model_path=celery_settings.NN_SENTIMENT_ESTIMATION_MODEL_PATH
            # )
            spec = importlib.util.spec_from_file_location(self.path[0], self.path[1])
            module_import = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_import)

            model_obj = getattr(module_import, self.path[0])
            self.estimator = model_obj(model_path=celery_settings.NN_SENTIMENT_ESTIMATION_MODEL_PATH)
        return self.run(*args, **kwargs)


@shared_task(ignore_result=True,
          bind=True,
          flush_every=100,
          flush_interval=5,
          max_retries=0,
          base=SentimentEstimationTask,
          path=(celery_settings.NN_SENTIMENT_ESTIMATION_CLASS, celery_settings.NN_SENTIMENT_ESTIMATION_MODULE_PATH),
          name=f'{__name__}, {celery_settings.NN_SENTIMENT_ESTIMATION_CLASS}')
def estimate_sentiment_batch(self, simple_request: List[SimpleRequest]):
    comments = []
    for portion in simple_request:
        comments.extend(portion.args)

    comment_ids, contents = zip(*comments)
    float_predictions = self.estimator.predict(contents)
    int_predictions = list(map(lambda e: math.ceil(e * 10), float_predictions))

    ids_sentiments = [(comment_id, prediction) for comment_id, prediction in  zip(comment_ids, int_predictions)]

    try:
        with closing(psycopg2.connect(
                dbname=celery_settings.DB_NAME,
                user=celery_settings.DB_USER,
                password=celery_settings.DB_PASSWORD,
                host=celery_settings.DB_HOST
        )) as conn:
            sql_expr = """UPDATE comments as T
                          SET sentiment = S.sentiment
                          FROM (VALUES (%s,%s)) AS S(id, sentiment)
                          WHERE S.id = T.id"""

            cursor = conn.cursor()
            cursor.executemany(sql_expr, ids_sentiments)
            cursor.close()
            conn.commit()
    except Exception as e:
            print('Failed to update comments: ', e)