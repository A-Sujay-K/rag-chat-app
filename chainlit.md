# 💬 Chat with Folder

Welcome to your personal document assistant! This app uses **Retrieval-Augmented Generation (RAG)** to answer questions based on the files you've loaded.

### How it works

1. 📂 You dropped your documents into the `data/` folder
2. 🔢 They were chunked, embedded, and stored as vectors
3. 🔍 When you ask a question, the most relevant chunks are retrieved
4. 🤖 The AI generates an answer using *only* your documents as context

### Tips

- **Be specific** — "What does section 3.2 say about pricing?" works better than "Tell me about pricing"
- **Follow up** — The chat remembers your conversation, so you can ask clarifying questions
- **Check sources** — Click the 📄 source panels on the right to see the exact text used

---

*Powered by LlamaIndex · ChromaDB · Chainlit*
