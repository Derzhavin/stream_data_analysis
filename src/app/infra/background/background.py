from psycopg2 import pool as pg_pool
from celery import current_app as current_celery_app
from celery.result import AsyncResult

from app.infra.background.configs.celery_config import settings as celery_settings


def create_background_app():
    background_app = current_celery_app
    background_app.db_pool = pg_pool.SimpleConnectionPool(
                                  minconn=celery_settings.DB_MIN_CONN,
                                  maxconn=celery_settings.DB_MAX_CONN,
                                  user=celery_settings.DB_USER,
                                  password=celery_settings.DB_PASSWORD,
                                  host=celery_settings.DB_HOST,
                                  port=celery_settings.DB_PORT,
                                  database=celery_settings.DB)

    background_app.config_from_object(celery_settings, namespace='CELERY')
    background_app.conf.update(task_track_started=True)
    background_app.conf.update(task_serializer='pickle')
    background_app.conf.update(result_serializer='pickle')
    background_app.conf.update(accept_content=['pickle', 'json'])
    background_app.conf.update(result_persistent=True)
    background_app.conf.update(worker_send_task_events=False)
    background_app.conf.update(worker_prefetch_multiplier=1)

    return background_app


def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result
