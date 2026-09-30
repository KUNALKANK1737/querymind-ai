from app.db.session import get_database_engine
from app.llm.prompt import build_sql_generation_prompt
from app.schema.introspector import introspect_database


def test_build_sql_generation_prompt():
    engine = get_database_engine()
    schema = introspect_database(engine)

    prompt = build_sql_generation_prompt(
        question="Which state has the highest number of customers?",
        schema=schema,
    )

    assert "Which state has the highest number of customers?" in prompt
    assert "Table: customers" in prompt
    assert "customer_id" in prompt
    assert "Table: orders" in prompt
    assert "Foreign key:" in prompt
    assert "SELECT" in prompt