from app.schema.models import DatabaseSchema


def build_sql_generation_prompt(
    question: str,
    schema: DatabaseSchema,
) -> str:
    schema_lines = []

    for table in schema.tables:
        schema_lines.append(f"Table: {table.name}")

        for column in table.columns:
            nullable = "NULL" if table_column_nullable(column) else "NOT NULL"
            schema_lines.append(
                f"  - {column.name}: {column.data_type} ({nullable})"
            )

        if table.primary_keys:
            schema_lines.append(
                f"  Primary key: {', '.join(table.primary_keys)}"
            )

        for foreign_key in table.foreign_keys:
            schema_lines.append(
                "  Foreign key: "
                f"{foreign_key.column} -> "
                f"{foreign_key.referenced_table}.{foreign_key.referenced_column}"
            )

    schema_text = "\n".join(schema_lines)

    return f"""
You are a PostgreSQL SQL generation assistant.

Your task is to convert the user's natural-language question
into a single read-only PostgreSQL SELECT query.

Database schema:
{schema_text}

Rules:
1. Generate only one SELECT statement.
2. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE,
   CREATE, or other data-modifying statements.
3. Use only tables and columns present in the provided schema.
4. Use PostgreSQL syntax.
5. Return only the SQL query without markdown fences or explanations.

User question:
{question}
""".strip()


def table_column_nullable(column) -> bool:
    return column.nullable
