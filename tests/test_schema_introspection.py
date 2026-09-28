from app.db.session import get_database_engine
from app.schema.introspector import introspect_database


def test_introspect_querymind_database():
    engine = get_database_engine()

    schema = introspect_database(engine)

    table_names = {table.name for table in schema.tables}

    expected_tables = {
        "customers",
        "categories",
        "products",
        "orders",
        "order_items",
        "payments",
        "addresses",
    }

    assert expected_tables.issubset(table_names)