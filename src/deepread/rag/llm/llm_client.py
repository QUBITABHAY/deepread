from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from deepread.core.config import settings
from deepread.core.logger import logger

from deepread.rag.prompts.templates import get_rag_prompt

def generate_response(question: str, context_docs: List[Document]) -> str:
    """
    Connects to the Groq API to generate an answer based purely on the provided context.
    
    Args:
        question (str): The user's query.
        context_docs (List[Document]): The top retrieved chunks from the vector database.
        
    Returns:
        str: The LLM's generated answer.
    """
    logger.info(f"Generating LLM response using Groq model: {settings.LLM_MODEL}")
    
    if not settings.GROQ_API_KEY:
        logger.error("GROQ_API_KEY is not set in the environment.")
        raise ValueError("GROQ_API_KEY is currently missing.")
        
    try:
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.LLM_MODEL,
            temperature=0.1
        )
        
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        prompt = get_rag_prompt()
        
        chain = prompt | llm
        
        response = chain.invoke({
            "context": context_text,
            "question": question
        })
        
        logger.info("Successfully received generated response from Groq.")
        return response.content
        
    except Exception as e:
        logger.error(f"Error communicating with LLM: {str(e)}")
        raise Exception(f"LLM Generation Error: {str(e)}")
