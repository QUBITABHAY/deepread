from fastapi import APIRouter
from deepread.core.logger import logger
from deepread.services.query import process_query
from deepread.models.request import QueryRequest
from deepread.models.response import QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    logger.info(f"Received query request: {request.question}")

    answer = await process_query(request.question, sources=request.sources)

    return QueryResponse(answer=answer)
