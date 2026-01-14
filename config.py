"""
config.py — Centralized configuration loader.

All settings are loaded from a .env file (or environment variables).
No hardcoded values exist anywhere else in the project.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Provider Toggles ──────────────────────────────────────────────
# Set to "openai" or "ollama"
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama").lower().strip()
# Set to "openai" or "huggingface"
EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower().strip()

# ── OpenAI ────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# ── Ollama ────────────────────────────────────────────────────────
