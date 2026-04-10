import os
import tempfile
from fastapi import UploadFile
from deepread.core.config import settings
from deepread.core.logger import logger
from deepread.rag.reader.pdf_reader import load_pdf
from deepread.rag.chunking.chunker import chunk_documents
from deepread.rag.embeddings.embedding_model import get_embedding_model
from deepread.rag.vector_store.vectordb import insert_into_vector_store

async def ingest_file(file: UploadFile) -> dict:
    """
    Service orchestrator for the document ingestion pipeline.
    Processes the raw file through RAG processes without storing it permanently.
    """
    logger.info(f"Starting ingestion for file: {file.filename}")
    
    content = await file.read()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Process through the Retrieval-Augmented Generation (RAG) pipeline
    try:
        logger.info(f"Orchestrating RAG extraction for {file.filename}")
        
        raw_docs = load_pdf(tmp_path)
        chunked_docs = chunk_documents(raw_docs)
        embedding_model = get_embedding_model()
        insert_into_vector_store(chunked_docs, embedding_model)
        
        logger.info(f"Successfully finished ingestion pipeline for: {file.filename}")
        
        return {
            "status": "success",
            "filename": file.filename,
            "message": "File successfully ingested and vectorized.",
            "file_size": len(content)
        }
        
    except Exception as e:
        logger.error(f"Pipeline error for {file.filename}: {str(e)}")
        raise Exception(f"Failed to process the document through pipeline: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
