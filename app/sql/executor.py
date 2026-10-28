from sqlalchemy import text
from sqlalchemy.engine import Engine


def execute_sql(
    engine: Engine,
    sql: str,
    timeout_ms: int | None = None,
) -> list[dict]:
    with engine.connect() as connection:
        if timeout_ms is not None:
            connection.execute(
                text("SET statement_timeout = :timeout_ms"),
                {"timeout_ms": timeout_ms},
            )

        result = connection.execute(text(sql))

        return [dict(row._mapping) for row in result]