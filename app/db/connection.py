from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.db.config import DatabaseConfig


def create_database_engine(config: DatabaseConfig) -> Engine:
    return create_engine(
        config.database_url,
        pool_pre_ping=True,
    )