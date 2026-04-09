from fastapi import APIRouter
from pydantic import BaseModel
from deepread.core.logger import logger

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query(question: QueryRequest):
    logger.info(f"Received query request: {question.question}")
    # Call RAG model here
    answer = f"Mock answer to: {question.question}"
    logger.info("Generated answer for query")
    return {"answer": answer}
