import pytest
from sqlalchemy.exc import DBAPIError

from app.db.session import get_database_engine
from app.sql.executor import execute_sql


def test_execute_sql():
    engine = get_database_engine()

    result = execute_sql(
        engine,
        """
        SELECT COUNT(*) AS customer_count
        FROM customers
        """,
    )

    assert result == [{"customer_count": 100}]
def test_execute_analytics_query():
    engine = get_database_engine()

    result = execute_sql(
        engine,
        """
        SELECT state, COUNT(*) AS customer_count
        FROM customers
        GROUP BY state
        ORDER BY customer_count DESC
        """,
    )

    assert len(result) > 0
    assert "state" in result[0]
    assert "customer_count" in result[0]
def test_query_timeout():
    engine = get_database_engine()

    with pytest.raises(DBAPIError):
        execute_sql(
            engine,
            "SELECT pg_sleep(2)",
            timeout_ms=100,
        )