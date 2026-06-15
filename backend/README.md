# Clinical FAQ AI Agent — Backend

An AI-powered system that answers clinical research questions using **RAG (Retrieval-Augmented Generation)**.

## Features
- 📄 RAG pipeline with FAISS vector database
- 🤖 LLM integration with Google Gemini 1.5 Flash
- 🛡️ Guardrail layer for safe, grounded responses
- ⚡ FastAPI REST API with async support
- 🌐 CORS enabled for React frontend

## Tech Stack
| Layer | Technology |
|---|---|
| Framework | FastAPI |
| LLM | Google Gemini 1.5 Flash |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector DB | FAISS |
| Orchestration | LangChain |
| Server | Uvicorn |

## Project Structure
```
backend/
├── main.py              # FastAPI app (entry point)
├── rag_pipeline.py      # RAG implementation (FAISS + embeddings)
├── llm_service.py       # Gemini LLM integration
├── sample_documents.py  # Clinical knowledge base (8 documents)
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment config
└── faiss_index/         # FAISS vector store (auto-created)
```

## Setup

### Prerequisites
- Python 3.9+
- Google Gemini API Key ([get one here](https://aistudio.google.com))

### Installation
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the backend folder:
```
GOOGLE_API_KEY=your_api_key_here
```

### Run Locally
```bash
python main.py
```
Backend runs on **http://localhost:8000**

## API Endpoints

### POST `/chat`
Chat with the AI agent.
```json
Request:  { "question": "What is a Phase II clinical trial?" }
Response: {
  "answer": "...",
  "sources": ["Clinical Trial Guidelines 101"],
  "safe": true,
  "confidence": "high",
  "processing_time_ms": 1200
}
```

### GET `/health`
Health check — returns RAG pipeline status.

### GET `/docs`
Interactive Swagger UI documentation.

## How It Works
```
User Question
     │
     ▼
FAISS Similarity Search (top 4 chunks)
     │
     ▼
Context + Question → Gemini Prompt
     │
     ▼
Gemini 1.5 Flash generates grounded answer
     │
     ▼
Safety Check → Return response
```

## Testing
```bash
# Test RAG pipeline
python rag_pipeline.py

# Test LLM service
python llm_service.py

# Test API (after starting server)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a Phase II trial?"}'
```

## Deployment
Deploy on [Render](https://render.com) using the `render.yaml` config.

## Author
Clinical AI Agent Project
