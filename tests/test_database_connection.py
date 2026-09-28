from sqlalchemy import text

from app.db.session import get_database_engine


def test_database_connection():
    engine = get_database_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1