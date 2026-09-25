from pydantic import BaseModel


class ColumnSchema(BaseModel):
    name: str
    data_type: str
    nullable: bool


class ForeignKeySchema(BaseModel):
    column: str
    referenced_table: str
    referenced_column: str


class TableSchema(BaseModel):
    name: str
    columns: list[ColumnSchema]
    primary_keys: list[str]
    foreign_keys: list[ForeignKeySchema]


class DatabaseSchema(BaseModel):
    tables: list[TableSchema]