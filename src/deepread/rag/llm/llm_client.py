import os
import re
from typing import List
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from groq import RateLimitError, AuthenticationError
from deepread.core.config import settings
from deepread.core.logger import logger
from deepread.rag.prompts.templates import get_rag_prompt


def _format_context(docs: List[Document]) -> str:
    """
    Formats retrieved chunks into a labelled context string so the LLM can
    cite exact source file and page numbers in its answer.

    Example output:
        [Source: attention_paper.pdf | Page: 3]
        The proposed model is called the Transformer...
    """
    formatted: list[str] = []
    for doc in docs:
        meta = doc.metadata or {}
        source_name = os.path.basename(str(meta.get("source", "Unknown")))
        page = meta.get("page", "?")
        header = f"[Source: {source_name} | Page: {page}]"
        formatted.append(f"{header}\n{doc.page_content.strip()}")
    return "\n\n".join(formatted)


def _extract_retry_after(error_message: str) -> str:
    """Tries to parse a human-readable wait time from a Groq 429 message."""
    match = re.search(r"try again in (\d+m\d+s|\d+s|\d+ seconds?)", error_message)
    return match.group(1) if match else "a few minutes"


def generate_response(question: str, context_docs: List[Document]) -> str:
    """
    Connects to Groq to generate a research-paper-grounded answer.

    Error handling:
      - RateLimitError (429): returns a friendly retry message - no 500 crash.
      - AuthenticationError: returns a clear key-missing message.
      - All other exceptions: logged and re-raised.

    Args:
        question: The user's query.
        context_docs: Top retrieved chunks from the vector DB.

    Returns:
        The LLM's answer string, or a friendly error string on rate limit / auth issues.
    """
    logger.info(f"Generating LLM response using Groq model: {settings.LLM_MODEL}")

    if not settings.GROQ_API_KEY:
        logger.error("GROQ_API_KEY is not set in the environment.")
        return "Error: GROQ_API_KEY is missing. Please add it to your .env file and restart."

    if not context_docs:
        logger.warning("No context documents found - returning no-context message.")
        return (
            "No relevant content was found in the uploaded document(s) for your question. "
            "Please upload a PDF and make sure your question relates to its content."
        )

    try:
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.LLM_MODEL,
            temperature=0.0,
        )

        context_text = _format_context(context_docs)
        prompt = get_rag_prompt()
        chain = prompt | llm

        response = chain.invoke({"context": context_text, "question": question})
        logger.info("Successfully received generated response from Groq.")
        return response.content

    except RateLimitError as e:
        wait = _extract_retry_after(str(e))
        logger.warning(f"Groq rate limit hit for model '{settings.LLM_MODEL}': {e}")
        return (
            f"**Rate limit reached** for model `{settings.LLM_MODEL}`.\n\n"
            f"Groq's free tier has a daily token quota. Please try again in **{wait}**.\n\n"
            f"_Tip: Set `LLM_MODEL=llama-3.1-8b-instant` in your `.env` for a higher-quota model._"
        )

    except AuthenticationError:
        logger.error("Groq authentication failed - check GROQ_API_KEY.")
        return "Error: Authentication failed. Please check that your GROQ_API_KEY is correct."

    except Exception as e:
        logger.error(f"Error communicating with LLM: {str(e)}")
        raise Exception(f"LLM Generation Error: {str(e)}")
