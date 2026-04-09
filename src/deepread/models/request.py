from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """
    Schema for the incoming questions to the /api/query endpoint.
    """
    question: str = Field(..., description="The specific question the user wants answered based on their documents.")
