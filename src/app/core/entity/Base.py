from sqlalchemy.ext.declarative import declarative_base
from app.configs.database import Engine

# Base Entity Model Schema
EntityMeta = declarative_base()


def init_db():
    EntityMeta.metadata.create_all(bind=Engine)
