import os
from functools import lru_cache
from kombu import Queue


def route_task(name):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class BaseConfig:
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "rpc://")

    CELERY_TASK_QUEUES: list = (
        Queue("celery"),
        Queue("comments"),
    )

    CELERY_TASK_ROUTES = ()
    CELERY_INCLUDE = [
        'app.infra.background.sentiment_estimation_task'
    ]

    DB_USER: str = 'admin'
    DB_PASSWORD = 'password'
    DB_HOST = "0.0.0.0"
    DB_PORT = '5432'
    DB = 'stream_analysis'
    DB_MIN_CONN = 1
    DB_MAX_CONN = 1

    NN_SENTIMENT_ESTIMATION_MODEL_PATH = '/home/denis/stream_data_analysis/src/sentiment_estimation1.pt'


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
