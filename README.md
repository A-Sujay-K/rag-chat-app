# 💬 Chat with Folder — RAG Application

A local **Retrieval-Augmented Generation** chat app that lets you have a conversation with your documents. Drop PDFs, text files, code, or Word documents into a folder and ask questions about them through a ChatGPT-like interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.14-orange)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.5-green)
![Chainlit](https://img.shields.io/badge/Chainlit-2.11-purple)

---

## ✨ Features

- **Chat with any folder** — PDFs, DOCX, TXT, Markdown, code files (Python, JS, Java, C++, and 20+ more)
- **Dual-mode** — Run fully local (Ollama + HuggingFace) or use cloud APIs (OpenAI GPT-4o)
- **Streaming responses** — Tokens appear in real-time, just like ChatGPT
- **Source attribution** — See exactly which document chunks were used to generate each answer
- **Conversational memory** — Ask follow-up questions naturally
- **Persistent storage** — ChromaDB saves vectors to disk; no re-ingestion needed on restart

---

## 📋 Prerequisites

- **Python 3.10+**
- **For local mode:** [Ollama](https://ollama.com/download) installed and running
- **For cloud mode:** An [OpenAI API key](https://platform.openai.com/api-keys)

---

## 🚀 Quick Start

### 1. Clone / navigate to the project

```bash
cd rag-chat-app
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your environment

```bash
copy .env.example .env     # Windows
# cp .env.example .env     # macOS/Linux
```

Edit `.env` to choose your provider:

| Setting | Local (default) | Cloud |
|---|---|---|
| `LLM_PROVIDER` | `ollama` | `openai` |
| `EMBEDDING_PROVIDER` | `huggingface` | `openai` |
| `OPENAI_API_KEY` | *(not needed)* | `sk-your-key` |

### 5. Add your documents

Drop your files into the `data/` folder. A sample file is included to get you started.

```
data/
├── your_report.pdf
├── meeting_notes.docx
├── codebase.py
└── sample_ai_overview.txt  ← included for testing
```

### 6. Ingest the documents

```bash
python ingest.py
```

This reads your files, chunks them, generates embeddings, and stores everything in ChromaDB. You only need to re-run this when you add or change documents.

### 7. Launch the chat

```bash
chainlit run app.py -w
```

Open your browser to **http://localhost:8000** and start chatting! 🎉

---

## 🔄 Switching Between Local and Cloud

**To use Ollama (local, free, private):**

1. Install Ollama: https://ollama.com/download
2. Pull a model:
   ```bash
   ollama pull llama3.1
   ```
3. Set in `.env`:
   ```env
   LLM_PROVIDER=ollama
   EMBEDDING_PROVIDER=huggingface
   ```

**To use OpenAI (cloud, paid, best quality):**

1. Get an API key from https://platform.openai.com/api-keys
2. Set in `.env`:
   ```env
   LLM_PROVIDER=openai
   EMBEDDING_PROVIDER=openai
   OPENAI_API_KEY=sk-your-key-here
   ```

> ⚠️ **Important:** If you switch embedding providers, you must re-run `python ingest.py` because different models produce different vector dimensions.

---

## 📁 Project Structure

```
rag-chat-app/
├── .env.example        # Configuration template
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── config.py           # Centralized settings loader
├── rag_engine.py       # Core RAG pipeline (ingest + load)
├── ingest.py           # CLI: ingest documents into vector store
├── app.py              # Chainlit chat application
├── chainlit.md         # Welcome message for the chat UI
├── data/               # ← Your documents go here
└── chroma_db/          # Auto-generated vector storage
```

---

## 🛠️ Configuration Reference

All settings live in `.env`. Here's what each one does:

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `ollama` | LLM backend: `ollama` or `openai` |
| `EMBEDDING_PROVIDER` | `huggingface` | Embedding backend: `huggingface` or `openai` |
| `OPENAI_API_KEY` | *(empty)* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI model to use |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | OpenAI embedding model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.1` | Ollama model name |
| `HF_EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Local HuggingFace model |
| `CHUNK_SIZE` | `512` | Text chunk size in tokens |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `DATA_DIR` | `./data` | Folder to read documents from |
| `CHROMA_DB_DIR` | `./chroma_db` | Persistent vector store path |
| `CHROMA_COLLECTION` | `rag_documents` | ChromaDB collection name |

---

## 📄 Supported File Types

| Category | Extensions |
|---|---|
| **Documents** | `.pdf` `.txt` `.md` `.docx` `.rtf` `.csv` |
| **Code** | `.py` `.js` `.ts` `.jsx` `.tsx` `.java` `.cpp` `.c` `.h` `.go` `.rs` `.rb` `.php` `.swift` `.kt` `.scala` `.r` `.sql` |
| **Config** | `.html` `.css` `.scss` `.xml` `.json` `.yaml` `.yml` `.toml` `.ini` `.cfg` `.sh` `.bat` `.ps1` |

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `No supported files found` | Add files to the `data/` folder and run `python ingest.py` |
| `OPENAI_API_KEY is required` | Set `LLM_PROVIDER=ollama` in `.env`, or add your OpenAI key |
| `Connection refused (Ollama)` | Make sure Ollama is running: `ollama serve` |
| `Timeout with Ollama` | Large models need time. Increase `request_timeout` in `rag_engine.py` or use a smaller model |
| `Dimension mismatch` | You changed embedding providers. Delete `chroma_db/` and re-run `python ingest.py` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in your virtual environment |

---

## 📝 License

MIT — use it however you like.
