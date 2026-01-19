import sys
import time
from rag_engine import ingest_documents

def main():
    print('Starting ingestion...')
    ingest_documents()

if __name__ == '__main__':
    main()
