import os
from functools import lru_cache
from kombu import Queue


def route_task(name):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class BaseConfig:
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@0.0.0.0:5672//")
    result_backend: str = os.environ.get("CELERY_RESULT_BACKEND", "rpc://")

    CELERY_TASK_QUEUES: list = (
        Queue("celery"),
        Queue("comments"),
    )

    CELERY_TASK_ROUTES = ()
    include = [
        'app.infra.background.sentiment_estimation_task'
    ]
    worker_concurrency = 1
    worker_max_tasks_per_child = 1000
    worker_prefetch_multiplier = 100
    DB_USER: str = 'admin'
    DB_PASSWORD = 'password'
    DB_HOST = "0.0.0.0"
    DB_PORT = '5432'
    DB_NAME = 'stream_analysis'

    NN_SENTIMENT_ESTIMATION_MODEL_PATH = f'{os.path.dirname(__file__)}/../../../../neural_networks/sentiment_estimation/sentiment_estimation_BERT.pt'
    NN_SENTIMENT_ESTIMATION_MODULE_PATH = f'{os.path.dirname(__file__)}/../../../../neural_networks/sentiment_estimation/BERT/SentimentEstimator.py'
    NN_SENTIMENT_ESTIMATION_CLASS = 'SentimentEstimator'


class DevelopmentConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
    }
    config_name = os.environ.get("CELERY_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
