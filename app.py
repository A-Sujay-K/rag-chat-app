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
        streaming=True,
        similarity_top_k=3,
        system_prompt=(
            "You are a helpful, accurate, and friendly assistant. "
            "Answer the user's questions based ONLY on the provided context from their documents. "
            "If the answer is not in the context, say: "
            "'I don't have enough information in the provided documents to answer that question.' "
            "Always cite which document the information came from when possible. "
            "Be concise but thorough."
        ),
    )

    # Persist per-session so each user gets their own chat history
    cl.user_session.set("chat_engine", chat_engine)

    await cl.Message(
        content=(
            f"✅ **Ready!** Ask me anything about your documents.\n\n"
            f"*Running on `{LLM_PROVIDER}` LLM with `{EMBEDDING_PROVIDER}` embeddings.*"
        )
    ).send()


@cl.on_message
