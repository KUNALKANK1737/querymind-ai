from app.db.session import get_database_engine
from app.llm.ollama import OllamaClient
from app.llm.service import generate_sql
from app.schema.introspector import introspect_database
from app.sql.service import execute_safe_sql


def run_query(question: str) -> dict:
    engine = get_database_engine()

    schema = introspect_database(engine)

    client = OllamaClient()

    sql = generate_sql(
        question=question,
        schema=schema,
        client=client,
    )

    results = execute_safe_sql(
        engine=engine,
        sql=sql,
    )

    return {
        "question": question,
        "sql": sql,
        "results": results,
    }