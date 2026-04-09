import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from deepread.core.logger import logger

def load_pdf(file_path: str) -> List[Document]:
    """
    Loads a PDF file from the local file system and extracts its content.
    Uses LangChain's PyPDFLoader to convert pages into Document objects.
    
    Args:
        file_path (str): The absolute or relative path to the saved PDF.
        
    Returns:
        List[Document]: A list of LangChain Document objects representing the pages.
    """
    if not os.path.exists(file_path):
        logger.error(f"Cannot load PDF. File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
        
    logger.info(f"Loading and extracting text from PDF: {file_path}")
    
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        logger.info(f"Successfully extracted {len(documents)} pages from the PDF.")
        return documents
        
    except Exception as e:
        logger.error(f"Error parsing PDF at '{file_path}': {str(e)}")
        raise Exception(f"Failed to parse PDF document: {str(e)}")
