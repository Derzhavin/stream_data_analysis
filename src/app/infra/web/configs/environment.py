from functools import lru_cache
from pydantic import BaseSettings


class EnvironmentSettings(BaseSettings):
    API_VERSION: str = 1
    APP_NAME: str = 'stream_analysis'
    DATABASE_DIALECT: str = 'postgresql'
    DATABASE_HOSTNAME: str = '0.0.0.0'
    DATABASE_NAME: str = 'stream_analysis'
    DATABASE_PASSWORD: str = 'password'
    DATABASE_PORT: int = 5432
    DATABASE_USERNAME: str = 'admin'

    DEBUG_MODE: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()