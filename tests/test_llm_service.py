from app.db.session import get_database_engine
from app.llm.ollama import OllamaClient
from app.llm.service import generate_sql
from app.schema.introspector import introspect_database


def test_generate_sql_from_question():
    engine = get_database_engine()
    schema = introspect_database(engine)
    client = OllamaClient()

    sql = generate_sql(
        question="Which state has the highest number of customers?",
        schema=schema,
        client=client,
    )

    assert sql
    assert "SELECT" in sql.upper()
    assert "CUSTOMERS" in sql.upper()
    assert "STATE" in sql.upper()