from langchain_core.prompts import ChatPromptTemplate

RAG_SYSTEM_PROMPT = """You are an expert AI assistant helping a user understand a document they uploaded. 
Use the context snippets provided below, which are extracted from the user's document, to answer their question. 
If the question is general (like "What is this document about?"), summarize the provided context to give them an idea.
If the specific answer cannot be deduced from the context, state that the information is not present in the document.

Context extracted from the document:
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
