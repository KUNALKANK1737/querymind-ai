from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    database_url: str