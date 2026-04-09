from typing import List
from langchain_core.documents import Document
from deepread.core.logger import logger
from deepread.rag.vector_store.vectordb import get_vector_store

def retrieve_documents(query: str, top_k: int = 4) -> List[Document]:
    """
    Retrieves the most semantically relevant document chunks for a given query.
    
    Args:
        query (str): The user's question or search term.
        top_k (int): The maximum number of document chunks to return.
        
    Returns:
        List[Document]: A list of LangChain Document chunks.
    """
    logger.info(f"Retrieving top {top_k} documents for query: '{query}'")
    
    try:
        # 1. Get the initialized vector database
        vector_store = get_vector_store()
        
        # 2. Build the retriever and fetch results
        retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
        docs = retriever.invoke(query)
        
        logger.info(f"Retrieved {len(docs)} relevant chunks from Vector DB.")
        
        return docs
        
    except Exception as e:
        logger.error(f"Failed to retrieve documents: {str(e)}")
        raise Exception(f"Document retrieval error: {str(e)}")
