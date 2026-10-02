from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_query_endpoint():
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