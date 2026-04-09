from fastapi import APIRouter
from pydantic import BaseModel
from deepread.core.logger import logger
from deepread.services.query import process_query

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def query(request: QueryRequest):
    logger.info(f"Received query request: {request.question}")
    
    # Send to query service layer
    answer = await process_query(request.question)
    
    return {"answer": answer}
