import os
import tempfile
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException
from deepread.core.config import settings
from deepread.core.logger import logger
from deepread.rag.reader.pdf_reader import load_pdf
from deepread.rag.chunking.chunker import chunk_documents
from deepread.rag.embeddings.embedding_model import get_embedding_model
from deepread.rag.vector_store.vectordb import insert_into_vector_store, delete_by_source

_ALLOWED_CONTENT_TYPES = {"application/pdf"}
_ALLOWED_EXTENSIONS = {".pdf"}


async def ingest_file(file: UploadFile) -> dict:
    """
    Service orchestrator for the document ingestion pipeline.

    Validates that the uploaded file is a PDF, then processes it through the
    RAG pipeline: read -> chunk -> embed -> store. Source metadata (original
    filename and upload timestamp) is injected into every chunk so that the
    retriever and LLM can produce accurate citations during query time.

    Args:
        file (UploadFile): The incoming multipart file from the API endpoint.

    Returns:
        dict: Ingestion result with status, filename, message, and file_size.

    Raises:
        HTTPException 400: If the file is not a PDF.
        Exception: If any stage of the RAG pipeline fails.
    """
    logger.info(f"Starting ingestion for file: {file.filename}")


    ext = os.path.splitext(file.filename or "")[1].lower()
    content_type = file.content_type or ""
    if ext not in _ALLOWED_EXTENSIONS and content_type not in _ALLOWED_CONTENT_TYPES:
        logger.warning(
            f"Rejected non-PDF upload: {file.filename} (type={content_type})"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Only PDF files are supported. Got: '{file.filename}'",
        )

    content = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        logger.info(f"Orchestrating RAG extraction for {file.filename}")

        raw_docs = load_pdf(tmp_path)
        chunked_docs = chunk_documents(raw_docs)

        upload_ts = datetime.now(timezone.utc).isoformat()
        for doc in chunked_docs:
            doc.metadata["source"] = file.filename
            doc.metadata["upload_timestamp"] = upload_ts

        delete_by_source(file.filename)

        embedding_model = get_embedding_model()
        insert_into_vector_store(chunked_docs, embedding_model)

        logger.info(f"Successfully finished ingestion pipeline for: {file.filename}")

        return {
            "status": "success",
            "filename": file.filename,
            "message": (
                f"File successfully ingested and vectorized into "
                f"{len(chunked_docs)} searchable chunks."
            ),
            "file_size": len(content),
        }

    except HTTPException:
        raise  # re-raise validation errors as-is
    except Exception as e:
        logger.error(f"Pipeline error for {file.filename}: {str(e)}")
        raise Exception(f"Failed to process the document through pipeline: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

