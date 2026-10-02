from fastapi import APIRouter

from app.api.schemas import QueryRequest, QueryResponse
from app.services.query_service import run_query

router = APIRouter(prefix="/api/v1", tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    result = run_query(request.question)

    return QueryResponse(**result)