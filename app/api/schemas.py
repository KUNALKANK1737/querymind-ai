from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    results: list[dict]
class ErrorResponse(BaseModel):
    error: str
    detail: str