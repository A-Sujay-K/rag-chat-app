import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'ollama')
DATA_DIR = os.getenv('DATA_DIR', './data')
