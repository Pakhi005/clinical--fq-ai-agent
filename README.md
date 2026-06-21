# Clinical FAQ AI Agent 🧬

LINK : https://ethical-ai-loan-predictor.streamlit.app/

An **end-to-end RAG system** that answers clinical research questions using **LangChain + FAISS + Google Gemini + React**.

## 🏗️ Architecture

```
User Question (React)
       │
       ▼
FastAPI Backend (port 8000)
       │
       ├─► FAISS Vector Search → Top 4 relevant chunks
       │
       └─► Gemini 1.5 Flash → Grounded Answer
                  │
                  ▼
       Safety Check → JSON Response
                  │
                  ▼
       React Chat UI (port 3000)
```

## 📁 Project Structure

```
clinical-ai-agent/
├── backend/
│   ├── main.py              # FastAPI app (entry point)
│   ├── rag_pipeline.py      # FAISS + HuggingFace embeddings
│   ├── llm_service.py       # Gemini LLM integration
│   ├── sample_documents.py  # 8 clinical knowledge documents
│   ├── requirements.txt     # Python deps
│   ├── render.yaml          # Render.com deployment
│   └── .env                 # API key (NOT committed)
│
└── frontend/
    ├── src/
    │   ├── App.js           # Main chat component
    │   ├── App.css          # Premium dark-mode UI
    │   └── index.js         # React entry point
    └── public/
        └── index.html
```

## 🚀 Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Add your Gemini API key to .env
echo GOOGLE_API_KEY=your_key_here > .env

python main.py
```

Backend runs at **http://localhost:8000**

### 2. Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs at **http://localhost:3000**

## 🔑 Get Gemini API Key

1. Visit https://aistudio.google.com
2. Click "Get API Key" → "Create API Key"
3. Add to `backend/.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

## ✨ Skills Demonstrated

| Skill | Implementation |
|---|---|
| RAG Architecture | LangChain + FAISS + Sentence Transformers |
| Vector Database | FAISS with `all-MiniLM-L6-v2` embeddings |
| LLM Integration | Google Gemini 1.5 Flash via LangChain |
| REST API | FastAPI with Pydantic models |
| Frontend | React with dark-mode premium UI |
| Safety/Guardrails | Multi-layer answer validation |

## 📡 API Reference

### `POST /chat`
```json
Request:  { "question": "What is Phase II trial?", "top_k": 4 }
Response: {
  "answer": "...",
  "sources": ["Clinical Trial Guidelines 101"],
  "safe": true,
  "confidence": "high",
  "processing_time_ms": 1250
}
```

### `GET /health`
Returns backend and RAG status.

### `GET /docs`
Interactive Swagger UI.

## 🌐 Deployment

- **Backend**: [Render.com](https://render.com) (uses `render.yaml`)
- **Frontend**: [Vercel](https://vercel.com) (`npm run build`)

## 📚 Interview Talking Points

> **"What does this project demonstrate?"**
> End-to-end RAG system: PDF/text ingestion → HuggingFace embeddings → FAISS retrieval → Gemini grounded generation → React UI with source citations.

> **"Why RAG instead of just LLM?"**
> RAG grounds answers in actual documents, reducing hallucinations. Critical for clinical information where accuracy matters.

> **"How do you prevent bad answers?"**
> Multi-layer safety: (1) Only answer from retrieved context, (2) Admit uncertainty if context is insufficient, (3) Flag unsafe medical advice patterns.
