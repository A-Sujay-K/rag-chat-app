"""
rag_engine.py — Core RAG pipeline.
"""
import os


from config import LLM_PROVIDER, DATA_DIR


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings


SUPPORTED_EXTENSIONS = ['.pdf', '.txt', '.md', '.docx']


def configure_settings():
    pass


def ingest_documents():
    pass
