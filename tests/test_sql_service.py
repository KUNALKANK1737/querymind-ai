import pytest

from app.db.session import get_database_engine
from app.sql.service import execute_safe_sql
from app.sql.validator import SQLValidationError


def test_execute_safe_select():
    engine = get_database_engine()

    result = execute_safe_sql(
        engine,
        "SELECT COUNT(*) AS customer_count FROM customers",
    )

    assert result == [{"customer_count": 100}]


def test_block_unsafe_sql():
    engine = get_database_engine()

    with pytest.raises(SQLValidationError):
        execute_safe_sql(
            engine,
            "DELETE FROM customers",
        )
        
def test_limit_result_rows():
    engine = get_database_engine()

    result = execute_safe_sql(
        engine,
        "SELECT customer_id FROM customers ORDER BY customer_id",
        max_rows=10,
    )

    assert len(result) == 10
    assert result[0]["customer_id"] == 1
    assert result[-1]["customer_id"] == 10
    