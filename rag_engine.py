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


def get_llm():
    """Return the configured LLM instance."""
    if LLM_PROVIDER == "openai":
        from llama_index.llms.openai import OpenAI

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai. "
                "Set it in your .env file."
            )
        return OpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.1,
        )
    else:
        from llama_index.llms.ollama import Ollama

        return Ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            request_timeout=120.0,
        )


def get_embed_model():
    """Return the configured embedding model instance."""
    if EMBEDDING_PROVIDER == "openai":
        from llama_index.embeddings.openai import OpenAIEmbedding

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai. "
                "Set it in your .env file."
            )
        return OpenAIEmbedding(
            model=OPENAI_EMBEDDING_MODEL,
            api_key=OPENAI_API_KEY,
        )
    else:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding

        return HuggingFaceEmbedding(model_name=HF_EMBEDDING_MODEL)


def configure_settings():
    """Apply the LLM and embedding model to the global LlamaIndex Settings."""
    Settings.llm = get_llm()
    Settings.embed_model = get_embed_model()
    Settings.chunk_size = CHUNK_SIZE
    Settings.chunk_overlap = CHUNK_OVERLAP


def _get_chroma_vector_store() -> ChromaVectorStore:
    """Create or connect to the persistent ChromaDB vector store."""
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)
    return ChromaVectorStore(chroma_collection=chroma_collection)


def ingest_documents() -> VectorStoreIndex:
    """
    Read all supported files from DATA_DIR, chunk them, embed them,
    and store the resulting vectors in ChromaDB.

    Returns the built VectorStoreIndex.
    """
    configure_settings()

    if not os.path.isdir(DATA_DIR):
