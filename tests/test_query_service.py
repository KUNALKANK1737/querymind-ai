from unittest.mock import Mock, patch

import pytest

from app.services.query_service import (
    MAX_CORRECTION_ATTEMPTS,
    run_query,
)
from app.sql.validator import SQLValidationError


def test_run_query_end_to_end():
    response = run_query(
        "Which state has the highest number of customers?"
    )

    assert response["question"] == (
        "Which state has the highest number of customers?"
    )
    assert response["sql"]
    assert "SELECT" in response["sql"].upper()
    assert response["results"]
    assert "state" in response["results"][0]


def test_run_query_self_corrects_failed_sql():
    corrected_sql = (
        "SELECT state, COUNT(*) FROM customers GROUP BY state"
    )

    with (
        patch(
            "app.services.query_service.get_database_engine",
            return_value=Mock(),
        ),
        patch(
            "app.services.query_service.introspect_database",
            return_value=Mock(),
        ),
        patch(
            "app.services.query_service.generate_sql",
            return_value="SELECT invalid_column FROM customers",
        ),
        patch(
            "app.services.query_service.correct_sql",
            return_value=corrected_sql,
        ),
        patch(
            "app.services.query_service.execute_safe_sql",
            side_effect=[
                SQLValidationError(
                    "Column invalid_column does not exist."
                ),
                [{"state": "Maharashtra", "count": 42}],
            ],
        ),
    ):
        result = run_query(
            "Which state has the highest number of customers?"
        )

    assert result["sql"] == corrected_sql
    assert result["results"] == [
        {"state": "Maharashtra", "count": 42}
    ]


def test_run_query_stops_after_max_correction_attempts():
    with (
        patch(
            "app.services.query_service.get_database_engine",
            return_value=Mock(),
        ),
        patch(
            "app.services.query_service.introspect_database",
            return_value=Mock(),
        ),
        patch(
            "app.services.query_service.generate_sql",
            return_value="SELECT invalid_column FROM customers",
        ),
        patch(
            "app.services.query_service.correct_sql",
            return_value="SELECT another_invalid_column FROM customers",
        ) as mock_correct,
        patch(
            "app.services.query_service.execute_safe_sql",
            side_effect=SQLValidationError("Invalid SQL query."),
        ) as mock_execute,
    ):
        with pytest.raises(SQLValidationError):
            run_query(
                "Which state has the highest number of customers?"
            )

    assert mock_execute.call_count == MAX_CORRECTION_ATTEMPTS + 1
    assert mock_correct.call_count == MAX_CORRECTION_ATTEMPTS


def test_run_query_does_not_retry_unexpected_errors():
    with (
        patch(
            "app.services.query_service.get_database_engine",
            return_value=Mock(),
        ),
        patch(
            "app.services.query_service.introspect_database",
            return_value=Mock(),
        ),
        patch(
            "app.services.query_service.generate_sql",
            return_value="SELECT 1",
        ),
        patch(
            "app.services.query_service.execute_safe_sql",
            side_effect=TypeError("Unexpected programming error"),
        ),
        patch(
            "app.services.query_service.correct_sql",
        ) as mock_correct,
    ):
        with pytest.raises(
            TypeError,
            match="Unexpected programming error",
        ):
            run_query("Return a simple result")

    mock_correct.assert_not_called()