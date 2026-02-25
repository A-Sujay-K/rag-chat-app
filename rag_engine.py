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
        os.makedirs(DATA_DIR, exist_ok=True)
        raise FileNotFoundError(
            f"No documents found. Please add files to the '{DATA_DIR}/' folder."
        )

    # Check that there are actual files in the directory
    has_files = any(
        f
        for _, _, files in os.walk(DATA_DIR)
        for f in files
        if any(f.endswith(ext) for ext in SUPPORTED_EXTENSIONS)
    )
    if not has_files:
        raise FileNotFoundError(
            f"No supported files found in '{DATA_DIR}/'. "
            f"Add PDFs, text files, code, or Word documents and try again."
        )

    print(f"📂 Scanning '{DATA_DIR}' for documents...")

    reader = SimpleDirectoryReader(
        input_dir=DATA_DIR,
        recursive=True,
        required_exts=SUPPORTED_EXTENSIONS,
    )
    documents = reader.load_data()
    print(f"📄 Loaded {len(documents)} document chunks from {DATA_DIR}")

    # Clear existing collection to avoid duplicates on re-ingestion
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    try:
        chroma_client.delete_collection(CHROMA_COLLECTION)
        print("🗑️  Cleared previous vector store")
    except Exception:
        pass  # Collection doesn't exist yet — that's fine

    vector_store = _get_chroma_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("🔢 Embedding and indexing documents...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )

    print("✅ Ingestion complete! Vector store saved to disk.")
    return index


