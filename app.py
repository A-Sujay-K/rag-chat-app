"""
app.py — Chainlit chat application for RAG.

Run with:
    chainlit run app.py -w

Features:
    - Streaming token-by-token responses
    - Source document attribution with side panels
    - Conversational memory (follow-up questions work)
    - Automatic provider detection from .env
"""

import chainlit as cl
from rag_engine import load_index, configure_settings
from config import LLM_PROVIDER, EMBEDDING_PROVIDER


