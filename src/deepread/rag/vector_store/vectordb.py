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
    Initializes and returns a singleton connection to the local Chroma vector DB.
    """
    global _vector_store

    if _vector_store is None:
        logger.info(f"Connecting to local Chroma DB at '{settings.VECTOR_DB_PATH}'")
        try:
            embedding_model = get_embedding_model()
            os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
            _vector_store = Chroma(
                persist_directory=settings.VECTOR_DB_PATH,
                embedding_function=embedding_model,
            )
            logger.info("Chroma Vector Store bound successfully.")
        except ImportError as e:
            logger.error("Missing dependency for ChromaDB.")
            raise Exception("Missing 'chromadb' package.") from e
        except Exception as e:
            logger.error(f"Failed to initialize Chroma DB: {str(e)}")
            raise Exception(f"Vector DB init error: {str(e)}")

    return _vector_store


def delete_by_source(filename: str) -> int:
    """
    Deletes all chunks in the vector store whose 'source' metadata matches
    *filename*.

    Returns the number of IDs deleted (0 if the file was not previously indexed).
    """
    store = get_vector_store()
    try:
        result = store._collection.get(where={"source": filename})
        ids = result.get("ids", [])
        if ids:
            store._collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} stale chunks for '{filename}'.")
        else:
            logger.info(f"No prior chunks found for '{filename}' - skipping delete.")
        return len(ids)
    except Exception as e:
        logger.warning(f"Could not delete old chunks for '{filename}': {str(e)}")
        return 0


def get_retriever(sources: list[str] | None = None, top_k: int | None = None):
    """
    Returns a configured Chroma retriever.

    If *sources* is a non-empty list of filenames, retrieval is restricted to
    chunks whose 'source' metadata is in that list - preventing cross-paper
    contamination during multi-paper sessions or after stale ingestions.

    Args:
        sources: List of original filenames to filter by (e.g. ["paper.pdf"]).
        top_k: Number of chunks to return; defaults to settings.RETRIEVER_TOP_K.
    """
    _top_k = top_k or settings.RETRIEVER_TOP_K
    store = get_vector_store()

    search_kwargs: dict = {
        "k": _top_k,
        "fetch_k": 30,
        "lambda_mult": 0.6,
    }

    if sources:

        if len(sources) == 1:
            search_kwargs["filter"] = {"source": sources[0]}
        else:
            search_kwargs["filter"] = {"source": {"$in": sources}}
        logger.info(f"Retriever restricted to sources: {sources}")

    return store.as_retriever(search_type="mmr", search_kwargs=search_kwargs)


def insert_into_vector_store(documents: List[Document], embedding_model=None):
    """
    Ingests a list of Document chunks into the VectorDB.
    Always call delete_by_source() before this to avoid duplicates.
    """
    logger.info(f"Ingesting {len(documents)} document chunks into Vector DB.")
    try:
        vector_store = get_vector_store()
        vector_store.add_documents(documents)
        logger.info("Successfully ingested and persisted chunks into Vector DB.")
    except Exception as e:
        logger.error(f"Error inserting documents to vector store: {str(e)}")
        raise Exception(f"Vector DB insertion error: {str(e)}")

