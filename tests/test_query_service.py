from app.services.query_service import run_query


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