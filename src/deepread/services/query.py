from langchain_groq import ChatGroq
from deepread.core.config import settings
from deepread.core.logger import logger
from deepread.rag.retriver.retriver import retrieve_documents
from deepread.rag.llm.llm_client import generate_response



_EXPANSION_PROMPT = """\
You are helping improve search recall in a research paper RAG system.
Given the user's question below, produce exactly 3 alternative phrasings \
that use academic terminology likely to appear in a research paper.
Return ONLY the 3 alternatives, one per line, no numbering, no explanation.

User question: {question}"""


def _expand_query(question: str) -> list[str]:
    """
    Returns up to 3 academically-phrased alternatives for *question*.

    Alternatives are returned as separate strings so the retriever can embed
    each one independently and then merge the results - which is more effective
    than concatenating them into one long string (long queries degrade embedding
    quality).

    Falls back to [question] (single-item list) on any API error.
    """
    try:
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=0.3,
        )
        response = llm.invoke(_EXPANSION_PROMPT.format(question=question))
        alternatives = [
            line.strip()
            for line in response.content.strip().splitlines()
            if line.strip()
        ][:3]  # cap at 3
        logger.info(f"Query expansion produced {len(alternatives)} alternatives.")
        return [question] + alternatives
    except Exception as e:
        logger.warning(f"Query expansion failed, using original: {str(e)}")
        return [question]




async def process_query(question: str, sources: list[str] | None = None) -> str:
    """
    Service orchestrator for handling user questions against uploaded papers.

    Pipeline:
      1. Expand the query into academic alternatives (improves recall).
      2. Retrieve the top-K chunks for each alternative independently, then
         merge and deduplicate by document ID.
      3. Generate a grounded, cited answer via Groq LLM.

    Args:
        question: The raw user question from the UI.
        sources:  Filenames of the papers to restrict retrieval to.
                  Prevents cross-contamination from other uploads in the DB.

    Returns:
        The LLM's research-grounded answer string.
    """
    logger.info(f"Processing query: '{question}' (sources={sources})")

    try:
        queries = _expand_query(question)

        seen_ids: set[str] = set()
        all_docs = []
        for q in queries:
            docs = retrieve_documents(q, sources=sources or None)
            for doc in docs:
                # Use page_content hash as a dedup key
                doc_id = str(hash(doc.page_content))
                if doc_id not in seen_ids:
                    seen_ids.add(doc_id)
                    all_docs.append(doc)

        logger.info(
            f"Merged {len(all_docs)} unique chunks from {len(queries)} query variants."
        )

        # Cap at RETRIEVER_TOP_K * 2 to stay within LLM context limits
        cap = settings.RETRIEVER_TOP_K * 2
        context_docs = all_docs[:cap]

        answer = generate_response(question, context_docs)
        logger.info("Successfully generated answer for query.")
        return answer

    except Exception as e:
        logger.error(f"Error processing query '{question}': {str(e)}")
        raise Exception(f"Failed to process query: {str(e)}")
