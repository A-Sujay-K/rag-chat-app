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

