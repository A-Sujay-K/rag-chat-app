import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'ollama')
DATA_DIR = os.getenv('DATA_DIR', './data')

EMBEDDING_PROVIDER = os.getenv('EMBEDDING_PROVIDER', 'huggingface')
CHROMA_DB_DIR = os.getenv('CHROMA_DB_DIR', './chroma_db')
CHROMA_COLLECTION = os.getenv('CHROMA_COLLECTION', 'rag_documents')
