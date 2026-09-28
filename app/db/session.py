from sqlalchemy.engine import Engine

from app.core.settings import get_settings
from app.db.config import DatabaseConfig
from app.db.connection import create_database_engine


def get_database_engine() -> Engine:
    settings = get_settings()

    config = DatabaseConfig(
        database_url=settings.database_url,
    )

    return create_database_engine(config)