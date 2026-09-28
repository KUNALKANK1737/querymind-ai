import pytest

from app.sql.validator import SQLValidationError, validate_sql


def test_validate_select_query():
    sql = "SELECT * FROM customers"

    assert validate_sql(sql) == sql


@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO customers (name) VALUES ('Test')",
        "UPDATE customers SET name = 'Test'",
        "DELETE FROM customers",
        "DROP TABLE customers",
        "ALTER TABLE customers ADD COLUMN test VARCHAR(10)",
        "TRUNCATE TABLE customers",
    ],
)
def test_reject_non_select_queries(sql):
    with pytest.raises(SQLValidationError):
        validate_sql(sql)


def test_reject_multiple_statements():
    sql = "SELECT * FROM customers; SELECT * FROM orders;"

    with pytest.raises(SQLValidationError):
        validate_sql(sql)


def test_reject_invalid_sql():
    sql = "SELECTTT FROM customers"

    with pytest.raises(SQLValidationError):
        validate_sql(sql)


def test_reject_empty_sql():
    with pytest.raises(SQLValidationError):
        validate_sql("   ")