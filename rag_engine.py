"""
rag_engine.py — Core RAG pipeline.

Handles document ingestion, vector storage, and index loading.
Supports toggling between local (Ollama + HuggingFace) and cloud (OpenAI)
providers via config.py.
"""

import os
import chromadb
