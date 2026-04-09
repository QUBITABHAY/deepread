from langchain_core.prompts import ChatPromptTemplate

RAG_SYSTEM_PROMPT = """You are an expert research AI assistant. Answer the user's question based strictly on the provided context below. If the answer cannot be deduced from the context, state that you don't know.

Context:
{context}"""

def get_rag_prompt() -> ChatPromptTemplate:
    """
    Returns the standard ChatPromptTemplate for the RAG pipeline.
    Expects 'context' and 'question' as input variables.
    """
    return ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_PROMPT),
        ("human", "{question}")
    ])
