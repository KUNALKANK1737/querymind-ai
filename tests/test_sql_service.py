from unittest.mock import Mock, patch

import pytest

from app.sql.service import execute_safe_sql
from app.sql.validator import SQLValidationError


def test_execute_safe_select():
    engine = Mock()

    with (
        patch(
            "app.sql.service.validate_sql",
            return_value="SELECT * FROM customers",
        ) as mock_validate,
        patch(
            "app.sql.service.execute_sql",
            return_value=[
                {"id": 1, "state": "Maharashtra"},
                {"id": 2, "state": "Gujarat"},
            ],
        ) as mock_execute,
    ):
        result = execute_safe_sql(
            engine,
            "SELECT * FROM customers",
        )

    assert result == [
        {"id": 1, "state": "Maharashtra"},
        {"id": 2, "state": "Gujarat"},
    ]

    mock_validate.assert_called_once_with(
        "SELECT * FROM customers"
    )
    mock_execute.assert_called_once_with(
        engine,
        "SELECT * FROM customers",
    )


def test_execute_safe_sql_rejects_invalid_sql():
    engine = Mock()

    with (
        patch(
            "app.sql.service.validate_sql",
            side_effect=SQLValidationError("Invalid SQL query."),
        ),
        patch("app.sql.service.execute_sql") as mock_execute,
        pytest.raises(SQLValidationError, match="Invalid SQL query."),
    ):
        execute_safe_sql(
            engine,
            "DROP TABLE customers",
        )

    mock_execute.assert_not_called()


def test_execute_safe_sql_limits_rows():
    engine = Mock()

    rows = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
    ]

    with (
        patch(
            "app.sql.service.validate_sql",
            return_value="SELECT * FROM customers",
        ),
        patch(
            "app.sql.service.execute_sql",
            return_value=rows,
        ),
    ):
        result = execute_safe_sql(
            engine,
            "SELECT * FROM customers",
            max_rows=2,
        )

    assert result == [
        {"id": 1},
        {"id": 2},
    ]