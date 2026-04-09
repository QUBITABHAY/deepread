import os
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from deepread.core.config import settings
from deepread.core.logger import logger
from deepread.rag.embeddings.embedding_model import get_embedding_model

_vector_store = None

def get_vector_store() -> Chroma:
    """
    Initializes and returns a connection to the local Chroma vector database.
    """
    global _vector_store
    
    if _vector_store is None:
        logger.info(f"Connecting to local Chroma DB at '{settings.VECTOR_DB_PATH}'")
        try:
            embedding_model = get_embedding_model()
            os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
            _vector_store = Chroma(
                persist_directory=settings.VECTOR_DB_PATH,
                embedding_function=embedding_model
            )
            logger.info("Chroma Vector Store bound successfully.")
            
        except ImportError as e:
            logger.error("Missing dependency for ChromaDB.")
            logger.error("Please run: uv add chromadb")
            raise Exception("Missing 'chromadb' package.") from e
        except Exception as e:
            logger.error(f"Failed to initialize Chroma DB: {str(e)}")
            raise Exception(f"Vector DB init error: {str(e)}")
            
    return _vector_store

def insert_into_vector_store(documents: List[Document], embedding_model=None):
    """
    Ingests a list of Document chunks into the VectorDB.
    """
    logger.info(f"Ingesting {len(documents)} document chunks into Vector DB.")
    try:
        vector_store = get_vector_store()
        vector_store.add_documents(documents)
        logger.info("Successfully ingested and persisted chunks into Vector DB.")
    except Exception as e:
        logger.error(f"Error inserting documents to vector store: {str(e)}")
        raise Exception(f"Vector DB insertion error: {str(e)}")
