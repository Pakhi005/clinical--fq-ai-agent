# main.py - FastAPI Backend for Clinical FAQ AI Agent
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# -- Lifespan: startup + shutdown ----------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize RAG pipeline on startup"""
    print("\nStarting Clinical FAQ AI Agent backend...")
    from rag_pipeline import rag
    from llm_service import llm_service
    from sample_documents import CLINICAL_DOCS

    try:
        rag.load_vector_store()
        print("RAG pipeline loaded from disk")
    except FileNotFoundError:
        print("Vector store not found - creating from sample documents...")
        rag.load_documents_from_text(CLINICAL_DOCS)
        rag.create_vector_store()
        print("Vector store created successfully")

    # Store instances on app state so routes can access them
    app.state.rag = rag
    app.state.llm_service = llm_service

    print("Backend ready. Listening on http://localhost:8000")
    yield
    print("Shutting down...")


# -- App setup -----------------------------------------------------------------
app = FastAPI(
    title="Clinical FAQ AI Agent",
    description="RAG-powered AI assistant for clinical research questions",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS - allow React dev server and any deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -- Request / Response Models -------------------------------------------------
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000,
                          description="The clinical research question")
    top_k: int = Field(default=4, ge=1, le=8,
                       description="Number of documents to retrieve")


class SourceDocument(BaseModel):
    source: str
    relevance_score: float
    preview: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    source_documents: list[SourceDocument]
    safe: bool
    confidence: str
    processing_time_ms: int


class HealthResponse(BaseModel):
    status: str
    rag_status: dict
    version: str


# -- Routes --------------------------------------------------------------------
@app.get("/", tags=["Info"])
async def root():
    """API root - basic info"""
    return {
        "name": "Clinical FAQ AI Agent",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    """Health check endpoint"""
    rag = app.state.rag
    return HealthResponse(
        status="ok",
        rag_status=rag.get_stats(),
        version="1.0.0"
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    - Retrieves relevant documents from the FAISS vector store
    - Sends them as context to Gemini for a grounded answer
    - Returns the answer with sources and safety flags
    """
    rag = app.state.rag
    llm_service = app.state.llm_service

    start_time = time.time()

    # 1. Validate question
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # 2. Retrieve context
    try:
        context_docs = rag.retrieve_context(question, k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(e)}")

    # 3. Generate answer
    try:
        result = llm_service.generate_answer(question, context_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

    # 4. Build response
    elapsed_ms = int((time.time() - start_time) * 1000)

    source_documents = [
        SourceDocument(
            source=doc["source"],
            relevance_score=doc["relevance_score"],
            preview=doc["content"][:300] + "..." if len(doc["content"]) > 300 else doc["content"]
        )
        for doc in context_docs
    ]

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        source_documents=source_documents,
        safe=result["safe"],
        confidence=result["confidence"],
        processing_time_ms=elapsed_ms
    )


@app.get("/documents/stats", tags=["Documents"])
async def document_stats():
    """Get stats about loaded documents"""
    rag = app.state.rag
    return rag.get_stats()


# -- Entry point ---------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
