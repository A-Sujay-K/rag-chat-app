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


@cl.on_chat_start
async def on_chat_start():
    """Initialize the RAG chat engine when a new session begins."""
    await cl.Message(
        content="⏳ Loading knowledge base... Please wait."
    ).send()

    try:
        configure_settings()
        index = load_index()
    except Exception as e:
        await cl.Message(
            content=(
                f"❌ **Failed to load the knowledge base.**\n\n"
                f"```\n{e}\n```\n\n"
                f"Make sure you have run `python ingest.py` first and that "
                f"your provider ({LLM_PROVIDER}/{EMBEDDING_PROVIDER}) is configured correctly."
            )
        ).send()
        return

    # Create a chat engine with context mode for conversational RAG
    chat_engine = index.as_chat_engine(
        chat_mode="context",
