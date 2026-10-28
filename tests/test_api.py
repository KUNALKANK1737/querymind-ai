from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.sql.validator import SQLValidationError

client = TestClient(app)


def test_query_endpoint():
    with patch(
        "app.api.routes.run_query",
        return_value={
            "question": "Which state has the highest number of customers?",
            "sql": "SELECT state, COUNT(*) FROM customers GROUP BY state",
            "results": [
                {"state": "Maharashtra", "count": 42},
            ],
        },
    ):
        response = client.post(
            "/api/v1/query",
            json={
                "question": "Which state has the highest number of customers?"
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == (
        "Which state has the highest number of customers?"
    )
    assert data["sql"]
    assert data["results"]


def test_query_endpoint_returns_400_for_invalid_sql():
    with patch(
        "app.api.routes.run_query",
        side_effect=SQLValidationError(
            "Only SELECT queries are allowed."
        ),
    ):
        response = client.post(
            "/api/v1/query",
            json={"question": "Delete all customers"},
        )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Only SELECT queries are allowed."