"""
ingest.py — CLI script to ingest documents into the vector store.

Usage:
    python ingest.py

This reads all supported files from the configured DATA_DIR,
chunks and embeds them, and stores the vectors in ChromaDB.
Run this once after adding or updating documents in the data/ folder.
"""

import sys
import time
from rag_engine import ingest_documents
from config import DATA_DIR, LLM_PROVIDER, EMBEDDING_PROVIDER


def main():
    print("=" * 60)
    print("  📚 RAG Document Ingestion Pipeline")
    print("=" * 60)
    print(f"  Data folder  : {DATA_DIR}")
    print(f"  LLM provider : {LLM_PROVIDER}")
    print(f"  Embed provider: {EMBEDDING_PROVIDER}")
    print("=" * 60)
    print()

    start = time.time()

    try:
        index = ingest_documents()
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        raise

    elapsed = time.time() - start
    print(f"\n⏱️  Completed in {elapsed:.1f} seconds")
    print(f"🚀 You can now run: chainlit run app.py -w")


if __name__ == "__main__":
    main()
