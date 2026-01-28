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
