from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from app.schema.models import (
    ColumnSchema,
    DatabaseSchema,
    ForeignKeySchema,
    TableSchema,
)


def introspect_database(engine: Engine) -> DatabaseSchema:
    inspector = inspect(engine)

    tables = []

    for table_name in inspector.get_table_names():
        columns = [
            ColumnSchema(
                name=column["name"],
                data_type=str(column["type"]),
                nullable=column["nullable"],
            )
            for column in inspector.get_columns(table_name)
        ]

        primary_keys = inspector.get_pk_constraint(table_name).get(
            "constrained_columns",
            [],
        )

        foreign_keys = [
            ForeignKeySchema(
                column=column,
                referenced_table=foreign_key["referred_table"],
                referenced_column=foreign_key["referred_columns"][0],
            )
            for foreign_key in inspector.get_foreign_keys(table_name)
            for column in foreign_key["constrained_columns"]
        ]

        tables.append(
            TableSchema(
                name=table_name,
                columns=columns,
                primary_keys=primary_keys,
                foreign_keys=foreign_keys,
            )
        )

    return DatabaseSchema(tables=tables)