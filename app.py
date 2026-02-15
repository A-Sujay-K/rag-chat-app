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
async def on_message(message: cl.Message):
    """Handle each user message: stream response + show sources."""
    chat_engine = cl.user_session.get("chat_engine")

    if chat_engine is None:
        await cl.Message(
            content=(
                "⚠️ Chat engine not initialized. "
                "Please refresh the page or check the setup instructions."
            )
        ).send()
        return

    # Create an empty message to stream into
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Stream the LLM response token by token
        streaming_response = await chat_engine.astream_chat(message.content)

        full_response = ""
        async for token in streaming_response.async_response_gen():
            full_response += token
            await msg.stream_token(token)

        # ── Source Attribution ────────────────────────────────────
        source_nodes = streaming_response.source_nodes
        if source_nodes:
            text_elements = []
            source_names = []

            for i, node in enumerate(source_nodes):
                # Try to extract a meaningful source name
                metadata = node.node.metadata or {}
                file_name = metadata.get("file_name", f"Chunk {i + 1}")
                page_label = metadata.get("page_label", "")

                if page_label:
                    source_name = f"📄 {file_name} (p. {page_label})"
                else:
                    source_name = f"📄 {file_name}"

                # Avoid duplicate names
                if source_name in source_names:
                    source_name = f"{source_name} [{i + 1}]"

                text_elements.append(
                    cl.Text(
                        content=node.node.get_content(),
                        name=source_name,
                        display="side",
                    )
                )
                source_names.append(source_name)

