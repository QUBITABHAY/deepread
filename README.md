# DeepRead

The Research AI Assistant is a Retrieval-Augmented Generation (RAG) system designed to transform dense academic research papers into actionable, searchable, and analytical knowledge. By leveraging Large Language Models (LLMs) and vector databases, this tool allows users to ask complex questions about their research documents and receive contextually grounded answers, saving significant time on literature review and analysis.

# Architecture

```
┌──────────────────────────────┐
│          Browser (UI)        │
│          (Gradio)            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        FastAPI Backend       │
│   (Routing + Orchestration)  │
└──────────────┬───────────────┘
               │
     ┌─────────┼─────────┐
     │         │         │
     ▼         ▼         ▼
┌──────────┐ ┌──────────────┐ ┌──────────────┐
│ Ingestion│ │ Query Layer  │ │  Cache Layer │
└────┬─────┘ └──────┬───────┘ └──────┬───────┘
     │              │                │
     ▼              ▼                ▼
┌──────────┐  ┌──────────────┐  ┌──────────┐
│  Reader  │  │ Query Rewrite│  │  Redis   │
│(PDF/Text)│  │ / Expansion  │  │  Cache   │
└────┬─────┘  └──────┬───────┘  └──────────┘
     │               │
     ▼               ▼
┌──────────┐   ┌──────────────┐
│ Chunking │   │  Retriever   │
└────┬─────┘   └──────┬───────┘
     │                │
     ▼                ▼
┌──────────┐   ┌──────────────┐
│Embedding │──▶│  Vector DB   │
└──────────┘   └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │     LLM      │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │   Response   │
               └──────────────┘
```

# Folder Structure

```
deepread/
│
├── README.md
├── pyproject.toml
├── uv.lock
│
└── src/
    └── deepread/
        │
        ├── main.py                # FastAPI entry point
        │
        ├── api/                  # Routes / endpoints
        │   ├── upload.py
        │   ├── query.py
        │   └── health.py
        │
        ├── core/                 # Config & settings
        │   ├── config.py
        │   └── logger.py
        │
        ├── services/             # Business logic
        │   ├── ingestion.py
        │   ├── query.py
        │   └── cache.py
        │
        ├── rag/                  # RAG pipeline (important)
        │   ├── reader/
        │   │   ├── pdf_reader.py
        │   │   └── text_reader.py
        │   │
        │   ├── chunking/
        │   │   └── chunker.py
        │   │
        │   ├── embeddings/
        │   │   └── embedding_model.py
        │   │
        │   ├── retriever/
        │   │   └── retriever.py
        │   │
        │   ├── vector_store/
        │   │   └── vectordb.py
        │   │
        │   ├── llm/
        │   │   └── llm_client.py
        │   │
        │   └── prompts/
        │       └── templates.py
        │
        ├── models/               # Pydantic schemas
        │   ├── request.py
        │   └── response.py
        │
        ├── db/                   # DB / vector store init
        │   └── connection.py
        │
        └── utils/                # helpers
            └── helpers.py
```
