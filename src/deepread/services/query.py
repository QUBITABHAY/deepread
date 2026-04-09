from deepread.core.logger import logger
from deepread.rag.retriver.retriver import retrieve_documents
from deepread.rag.llm.llm_client import generate_response

async def process_query(question: str) -> str:
    """
    Service orchestrator for handling user questions.
    Routes the question through the retriever to find relevant context,
    then generates an answer using the LLM.
    """
    logger.info(f"Processing query: {question}")
    
    try:
        context_docs = retrieve_documents(question)
        answer = generate_response(question, context_docs)
        logger.info("Successfully generated answer for query.")
        return answer
        
    except Exception as e:
        logger.error(f"Error processing query '{question}': {str(e)}")
        raise Exception(f"Failed to process query: {str(e)}")
