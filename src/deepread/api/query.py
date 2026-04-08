from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query(question: QueryRequest):
    # Call RAG model here
    answer = f"Mock answer to: {question.question}"
    return {"answer": answer}
