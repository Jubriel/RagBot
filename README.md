Sure thing, Jubriel. Here’s a direct, no-fluff draft of your `README.md` file for this WebSocket-based chatbot:

---

# 🧠 Story ChatBot System

This is a LangChain-based WebSocket chatbot system designed for interactive conversation, document retrieval, and smart response generation using local FAISS vector storage and Ollama models.

---

## 📋 Features

* **LangChain-powered Agent Executor** with custom tools.
* **FAISS VectorStore** document retrieval with contextual chunking.
* **Local LLM (Ollama)** for chat response, metadata tagging, and summarization.
* **Dynamic Metadata & Summary Generation** based on conversation history.
* **Multi-Session User Management** via in-memory storage (`ChatMessageHistory`).
* **WebSocket Endpoint Ready** (expects integration with FastAPI or similar server).

---

## 🏗️ System Architecture

```
               +--------------------+
               |   WebSocket Client |
               +---------+----------+
                         |
                         v
               +--------------------+
               |  ChatBot Endpoint  |
               +---------+----------+
                         |
                         v
       +-----------------------------------+
       |     StoryTeller (Agent Executor)   |
       +----------------+-----------------+
                        |
            +-----------+-----------+
            |                       |
  +---------v---------+   +---------v---------+
  |  FAISS VectorStore|   |   Ollama LLM      |
  +------------------+   +------------------+
```

---

## 🧩 Components

### 1. **VectorStoreManager**

* Loads or builds a FAISS index from:

  * Web pages (`PAGE_URLS`)
  * Local PDF (`orwellanimalfarm.pdf`)
* Saves index to disk for reuse.

### 2. **Custom Tools**

* **`retrieve`**: Pulls relevant documents from the vector store for agent context.
* **`date_time`**: Adds timestamps to conversation context.
* **`get_metadata`**: Generates a tag & priority label for chat history.
* **`get_summary`**: Condenses chat history into a brief summary.

### 3. **StoryTeller Class**

* Manages chat history per user (`user_id`).
* Handles vectorstore retrieval and chat response.
* Uses LangChain AgentExecutor for tool-using LLM.
* Offers methods to:

  * `chat(user_id, query)`
  * `load_history(user_id)`
  * `clear_chat_history(user_id)`

---

## ⚙️ Setup Instructions

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Environment Variables**:
   Create a `.env` file:

```env
OLLAMA_HOST=http://localhost:11434
```

3. **Run FAISS Setup**:
   The vectorstore is built or loaded automatically on first run.

4. **Integrate WebSocket Endpoint**:
   This bot expects to be connected to a WebSocket endpoint (e.g., FastAPI):

```python
from fastapi import FastAPI, WebSocket
from storyteller_module import StoryTeller

app = FastAPI()
bot = StoryTeller()

@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    user_id = "some_unique_id"  # customize this
    while True:
        data = await websocket.receive_text()
        response = bot.chat(user_id, data)
        await websocket.send_text(response)
```

---

## 🗂️ Project Structure

```
.
├── storyteller.py     # Main chatbot class and logic
├── config.py          # Configuration settings and constants
├── contextual.py      # Contextual chunking logic
├── orwellanimalfarm.pdf  # Sample document
├── digit_index/       # FAISS index directory (auto-created)
├── .env               # Environment variables
└── README.md          # This file
```

---

## ⚠️ Notes

* FAISS loading uses `allow_dangerous_deserialization=True`. Ensure trusted environment only.
* Ollama server must be running locally (`OLLAMA_HOST`).
* PDF loader depends on `UnstructuredPDFLoader` from `langchain_community`.
* WebSocket setup is not included here but expected to be handled separately (example provided).

---

## 📌 TODOs

* [ ] Improve error handling on WebSocket layer.
* [ ] Add persistent chat history storage (DB or file-based).
* [ ] Expand document sources (dynamic URLs, multiple PDFs).
* [ ] Include authentication for WebSocket clients.

---

## 👤 Author

Built by **Jubriel**, AI/ML Engineer.
Traditional, skeptical, forward-looking. No nonsense.

---

Let me know if you want this as an actual file or extended for deployment instructions (Docker, etc.).
