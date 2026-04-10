from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from deepread.core.logger import logger

def chunk_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Splits a list of LangChain Document objects into smaller chunks using 
    RecursiveCharacterTextSplitter. This is essential to fit documents
    within the LLM context window and improve retrieval granularity.
    
    Args:
        documents (List[Document]): The extracted pages/documents from the reader.
        chunk_size (int): The maximum character length of each chunk.
        chunk_overlap (int): How many characters to overlap between sequential chunks.
        
    Returns:
        List[Document]: A new list of chunked Document objects.
    """
    logger.info(f"Chunking {len(documents)} documents (chunk_size={chunk_size}, overlap={chunk_overlap})...")
    
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
        chunked_docs = text_splitter.split_documents(documents)
        logger.info(f"Successfully split documents into {len(chunked_docs)} semantic chunks.")
        
        return chunked_docs
        
    except Exception as e:
        logger.error(f"Error during document chunking: {str(e)}")
        raise Exception(f"Failed to chunk documents: {str(e)}")
