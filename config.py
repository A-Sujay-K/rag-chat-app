"""
config.py — Centralized configuration loader.

All settings are loaded from a .env file (or environment variables).
No hardcoded values exist anywhere else in the project.
"""

import os
from dotenv import load_dotenv

load_dotenv()

