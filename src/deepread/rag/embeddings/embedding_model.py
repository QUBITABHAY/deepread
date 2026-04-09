from langchain_community.embeddings import HuggingFaceEmbeddings
from deepread.core.logger import logger

def get_embedding_model():
    """
    Initializes and returns the embedding model.
    We use HuggingFace's 'all-MiniLM-L6-v2' as a fast, free, local default.
    
    Returns:
        HuggingFaceEmbeddings: The initialized LangChain embedding model.
    """
    logger.info("Initializing HuggingFace Embedding model (all-MiniLM-L6-v2)...")
    
    try:
        model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        logger.info("Embedding model initialized successfully.")
        return model
        
    except ImportError as e:
        logger.error("Missing dependency for HuggingFace embeddings.")
        logger.error("Please run: uv add sentence_transformers")
        raise Exception("Missing 'sentence_transformers' package.") from e
        
    except Exception as e:
        logger.error(f"Failed to initialize embedding model: {str(e)}")
        raise Exception(f"Embedding model initialization error: {str(e)}")
