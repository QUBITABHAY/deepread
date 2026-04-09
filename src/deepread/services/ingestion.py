import os
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
    Handles saving the raw file and routing it through RAG processes.
    """
    logger.info(f"Starting ingestion for file: {file.filename}")
    
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)
    
    file_path = os.path.join(settings.STORAGE_DIR, file.filename)
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        logger.info(f"Saved {file.filename} to {file_path} for processing.")
    except Exception as e:
        logger.error(f"Failed to save {file.filename} to disk: {str(e)}")
        raise Exception(f"File save error: {str(e)}")

    # Process through the Retrieval-Augmented Generation (RAG) pipeline
    try:
        logger.info(f"Orchestrating RAG extraction for {file_path}")
        
        # Pipeline execution (Stubbed until rag/ is implemented)
        raw_docs = load_pdf(file_path)
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
