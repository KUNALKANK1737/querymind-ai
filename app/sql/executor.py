from sqlalchemy import text
from sqlalchemy.engine import Engine


def execute_sql(engine: Engine, sql: str) -> list[dict]:
    with engine.connect() as connection:
        result = connection.execute(text(sql))

        return [dict(row._mapping) for row in result]