from fastapi import APIRouter, HTTPException

from app.api.schemas import ErrorResponse, QueryRequest, QueryResponse
from app.services.query_service import run_query
from app.sql.validator import SQLValidationError

router = APIRouter(prefix="/api/v1", tags=["query"])


@router.post(
    "/query",
    response_model=QueryResponse,
    responses={400: {"model": ErrorResponse}},
)
def query(request: QueryRequest) -> QueryResponse:
    try:
        result = run_query(request.question)
    except SQLValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return QueryResponse(**result)