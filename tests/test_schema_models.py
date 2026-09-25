from app.schema.models import (
    ColumnSchema,
    DatabaseSchema,
    ForeignKeySchema,
    TableSchema,
)


def test_database_schema_models():
    customer_table = TableSchema(
        name="customers",
        columns=[
            ColumnSchema(
                name="customer_id",
                data_type="INTEGER",
                nullable=False,
            ),
            ColumnSchema(
                name="name",
                data_type="VARCHAR",
                nullable=False,
            ),
        ],
        primary_keys=["customer_id"],
        foreign_keys=[],
    )

    schema = DatabaseSchema(tables=[customer_table])

    assert len(schema.tables) == 1
    assert schema.tables[0].name == "customers"
    assert schema.tables[0].primary_keys == ["customer_id"]