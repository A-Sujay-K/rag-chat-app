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
    StorageContext,
    Settings,
)
from llama_index.vector_stores.chroma import ChromaVectorStore


# ── Supported file extensions ─────────────────────────────────────
SUPPORTED_EXTENSIONS = [
    # Documents
    ".pdf", ".txt", ".md", ".docx", ".rtf", ".csv",
    # Code
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".cpp", ".c", ".h", ".hpp",
    ".go", ".rs", ".rb", ".php", ".swift",
    ".kt", ".scala", ".r", ".sql",
    ".html", ".css", ".scss", ".xml", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".sh", ".bat", ".ps1",
]


