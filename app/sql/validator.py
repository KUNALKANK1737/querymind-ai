import sqlglot
from sqlglot import exp


class SQLValidationError(ValueError):
    """Raised when SQL fails QueryMind safety validation."""


def validate_sql(sql: str) -> str:
    if not sql.strip():
        raise SQLValidationError("SQL query cannot be empty.")

    try:
        statements = sqlglot.parse(sql, read="postgres")
    except sqlglot.errors.ParseError as exc:
        raise SQLValidationError("Invalid SQL syntax.") from exc

    if len(statements) != 1:
        raise SQLValidationError("Only one SQL statement is allowed.")

    statement = statements[0]

    if not isinstance(statement, exp.Select):
        raise SQLValidationError("Only SELECT queries are allowed.")

    return sql.strip()