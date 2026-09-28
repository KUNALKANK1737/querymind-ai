from sqlalchemy.engine import Engine

from app.sql.executor import execute_sql
from app.sql.validator import validate_sql

DEFAULT_MAX_ROWS = 1000


def execute_safe_sql(
    engine: Engine,
    sql: str,
    max_rows: int = DEFAULT_MAX_ROWS,
) -> list[dict]:
    validated_sql = validate_sql(sql)

    results = execute_sql(engine, validated_sql)

    return results[:max_rows]