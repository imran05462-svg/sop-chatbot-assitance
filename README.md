# 🤖 SOP Support Assistant Bot

A **Retrieval-Augmented Generation (RAG)** chatbot that answers questions strictly from uploaded SOP documents — using local Hugging Face embeddings and a cloud LLM.

---

## 🗂️ Project Structure

```
hackthon/
├── sop-asst-backend/
│   ├── main.py          # FastAPI app (/upload, /chat endpoints)
│   ├── ingestion.py     # PDF/DOCX/TXT parsing + chunking
│   ├── retriever.py     # HuggingFace embeddings + FAISS search
│   └── llm.py           # LLM via Hugging Face Inference API
├── sop-asst-frontend/
│   └── app.py           # Streamlit chat UI
├── requirements.txt
├── .env                 # API keys (not committed)
└── .env.example         # Template for environment variables
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI |
| Embeddings | `all-MiniLM-L6-v2` (Hugging Face, runs **locally**) |
| Vector Store | FAISS (CPU) |
| LLM | `meta-llama/Meta-Llama-3-8B-Instruct` via HF Inference API |
| File Parsing | pypdf, python-docx |

---

## 🚀 Getting Started

### 1. Create & Activate Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate      # Windows
source venv/bin/activate     # Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your key:
```bash
HF_API_KEY=hf_your_huggingface_token_here
```
Get a free token at 👉 https://huggingface.co/settings/tokens

### 4. Start the Backend
```bash
uvicorn sop-asst-backend.main:app --reload
```

### 5. Start the Frontend (in a new terminal)
```bash
streamlit run sop-asst-frontend/app.py
```

---

## 💡 How to Use

1. **Upload** a PDF, DOCX, or TXT SOP document in the sidebar
2. Click **Process Document** to embed and index it
3. **Ask questions** in the chat — the bot will answer strictly from your document

---

## 📋 Response Format

Every answer is structured as:

```
## Problem Understanding
## Resolution Steps
## Verification
## Escalation
```

> If the question is not covered in the uploaded document, the bot will respond:
> **"This question does not belong to the provided document."**

---

## 📝 Notes

- Re-upload and reprocess your document after restarting the backend
- The `faiss_index.bin` and `chunk_mapping.json` files are saved locally
- Linting errors in VS Code for `faiss`, `streamlit`, etc. are IDE path issues only — the app runs correctly inside the venv
