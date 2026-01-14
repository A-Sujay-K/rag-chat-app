"""
rag_engine.py — Core RAG pipeline.

Handles document ingestion, vector storage, and index loading.
Supports toggling between local (Ollama + HuggingFace) and cloud (OpenAI)
providers via config.py.
"""

import os
import chromadb

from config import (
    LLM_PROVIDER,
    EMBEDDING_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_EMBEDDING_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    HF_EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    DATA_DIR,
    CHROMA_DB_DIR,
    CHROMA_COLLECTION,
)

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
