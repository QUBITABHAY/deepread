from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """
    Schema for the incoming questions to the /api/query endpoint.
    """
    question: str = Field(..., description="The user's question about the uploaded document(s).")
    sources: list[str] = Field(
        default=[],
        description="Filenames of the uploaded papers to restrict retrieval to. Empty = search all.",
    )
