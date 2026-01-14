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

