from typing import List
from langchain_core.documents import Document
from deepread.core.config import settings
from deepread.core.logger import logger
from deepread.rag.vector_store.vectordb import get_retriever, get_vector_store


def retrieve_documents(
    query: str,
    top_k: int | None = None,
    sources: list[str] | None = None,
) -> List[Document]:
    """
    Retrieves the most semantically relevant document chunks for *query*,
    restricted to *sources* if provided.

    Strategy:
      1. Primary: MMR via get_retriever() (with optional Chroma source filter).
      2. Fallback: cosine similarity with 30% threshold when MMR returns nothing.

    Args:
        query:   The user's question or expanded search string.
        top_k:   Max chunks to return; defaults to settings.RETRIEVER_TOP_K.
        sources: Filenames to restrict retrieval to.  None = search all.

    Returns:
        List of LangChain Document chunks.
    """
    _top_k = top_k or settings.RETRIEVER_TOP_K
    logger.info(
        f"Retrieving top {_top_k} chunks for query: '{query[:80]}... ' "
        f"(sources={sources})"
    )

    try:
        retriever = get_retriever(sources=sources, top_k=_top_k)
        docs = retriever.invoke(query)

        if not docs:
            logger.warning("MMR returned 0 results - falling back to similarity search.")
            store = get_vector_store()
            kwargs: dict = {"k": _top_k}
            if sources:
                kwargs["filter"] = (
                    {"source": sources[0]}
                    if len(sources) == 1
                    else {"source": {"$in": sources}}
                )
            results = store.similarity_search_with_relevance_scores(query, **kwargs)
            docs = [doc for doc, score in results if score > 0.3]
            logger.info(
                f"Similarity fallback returned {len(docs)} chunks "
                f"(filtered from {len(results)})."
            )

        logger.info(f"Retrieved {len(docs)} relevant chunks.")
        return docs

    except Exception as e:
        logger.error(f"Failed to retrieve documents: {str(e)}")
        raise Exception(f"Document retrieval error: {str(e)}")
