from unittest.mock import Mock, patch

from app.schema.introspector import introspect_database


def test_introspect_database():
    mock_engine = Mock()

    inspector = Mock()
    inspector.get_table_names.return_value = ["customers"]

    inspector.get_columns.return_value = [
        {
            "name": "id",
            "type": "INTEGER",
            "nullable": False,
        },
        {
            "name": "name",
            "type": "VARCHAR",
            "nullable": False,
        },
        {
            "name": "state",
            "type": "VARCHAR",
            "nullable": True,
        },
    ]

    inspector.get_pk_constraint.return_value = {
        "constrained_columns": ["id"],
    }

    inspector.get_foreign_keys.return_value = []

    with patch(
        "app.schema.introspector.inspect",
        return_value=inspector,
    ):
        schema = introspect_database(mock_engine)

    assert len(schema.tables) == 1

    table = schema.tables[0]

    assert table.name == "customers"
    assert len(table.columns) == 3
    assert table.primary_keys == ["id"]
    assert table.foreign_keys == []

    assert table.columns[0].name == "id"
    assert table.columns[0].data_type == "INTEGER"
    assert table.columns[0].nullable is False