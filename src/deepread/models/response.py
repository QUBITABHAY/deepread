from pydantic import BaseModel, Field

class QueryResponse(BaseModel):
    """
    Schema for the generated response payloads from the /api/query endpoint.
    """
    answer: str = Field(..., description="The generated LLM answer based on the RAG context.")

class UploadResponse(BaseModel):
    """
    Schema representing the status of an uploaded document hitting /api/upload.
    """
    status: str = Field(..., description="The state of the document ingestion pipeline ('success', 'error').")
    filename: str = Field(..., description="The original name of the document uploaded.")
    message: str = Field(..., description="Detailed response indicating the pipeline stage finished.")
    file_size: int = Field(..., description="Byte size of the ingested file.")
