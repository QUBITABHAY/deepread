from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from deepread.core.config import settings
from deepread.core.logger import logger

def chunk_documents(
    documents: List[Document],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> List[Document]:
    """
    Splits a list of LangChain Document objects into smaller chunks using
    RecursiveCharacterTextSplitter, tuned for academic research papers.

    Separators are ordered so that double newlines (section/paragraph breaks
    common in PDF-extracted text) are tried first, improving semantic
    coherence of each chunk.

    `add_start_index=True` injects the byte-offset of each chunk into its
    metadata, which lets the LLM report approximate locations (page/section).

    Args:
        documents (List[Document]): Extracted pages/documents from the reader.
        chunk_size (int | None): Override; defaults to settings.CHUNK_SIZE.
        chunk_overlap (int | None): Override; defaults to settings.CHUNK_OVERLAP.

    Returns:
        List[Document]: A new list of chunked Document objects.
    """
    _chunk_size = chunk_size or settings.CHUNK_SIZE
    _chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    logger.info(
        f"Chunking {len(documents)} documents "
        f"(chunk_size={_chunk_size}, overlap={_chunk_overlap})..."
    )

    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=_chunk_size,
            chunk_overlap=_chunk_overlap,
            length_function=len,
            add_start_index=True,
            separators=["\n\n", "\n", " ", ""],
        )

        chunked_docs = text_splitter.split_documents(documents)
        logger.info(
            f"Successfully split documents into {len(chunked_docs)} semantic chunks."
        )

        return chunked_docs

    except Exception as e:
        logger.error(f"Error during document chunking: {str(e)}")
        raise Exception(f"Failed to chunk documents: {str(e)}")

