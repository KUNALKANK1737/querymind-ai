
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_database_engine
from app.llm.ollama import OllamaClient
from app.llm.service import correct_sql, generate_sql
from app.schema.introspector import introspect_database
from app.sql.service import execute_safe_sql
from app.sql.validator import SQLValidationError

MAX_CORRECTION_ATTEMPTS = 2


def run_query(question: str) -> dict:
    engine = get_database_engine()
    schema = introspect_database(engine)
    client = OllamaClient()

    sql = generate_sql(
        question=question,
        schema=schema,
        client=client,
    )

    for attempt in range(MAX_CORRECTION_ATTEMPTS + 1):
        try:
            results = execute_safe_sql(
                engine=engine,
                sql=sql,
            )

            return {
                "question": question,
                "sql": sql,
                "results": results,
            }

        except (SQLValidationError, SQLAlchemyError) as exc:
            if attempt >= MAX_CORRECTION_ATTEMPTS:
                raise

            sql = correct_sql(
                question=question,
                failed_sql=sql,
                error=str(exc),
                schema=schema,
                client=client,
            )

    raise RuntimeError("Query execution failed unexpectedly.")
