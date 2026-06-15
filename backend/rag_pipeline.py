# rag_pipeline.py - LangChain 0.3 compatible
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()


class RAGPipeline:
    def __init__(self, index_path="faiss_index"):
        self.index_path = index_path
        print("Loading embedding model (first run may take a minute)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("Embedding model ready")
        self.vectorstore = None
        self.documents = []

    def load_documents_from_text(self, documents_list):
        """Load documents from list of dicts (title + content)"""
        loaded_docs = []
        for doc in documents_list:
            doc_obj = Document(
                page_content=doc["content"],
                metadata={"source": doc["title"]}
            )
            loaded_docs.append(doc_obj)

        self.documents = loaded_docs
        print(f"Loaded {len(loaded_docs)} documents")
        return loaded_docs

    def load_documents_from_pdf(self, pdf_folder):
        """Load documents from PDF files"""
        from PyPDF2 import PdfReader

        docs = []
        if not os.path.exists(pdf_folder):
            print(f"PDF folder '{pdf_folder}' not found. Skipping.")
            return docs

        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(pdf_folder, filename)
                print(f"Loading {filename}...")
                reader = PdfReader(pdf_path)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text and text.strip():
                        docs.append(Document(
                            page_content=text,
                            metadata={"source": f"{filename} (page {page_num + 1})"}
                        ))

        self.documents = docs
        print(f"Loaded {len(docs)} pages from PDFs")
        return docs

    def chunk_documents(self, chunk_size=600, chunk_overlap=120):
        """Split documents into overlapping chunks"""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = splitter.split_documents(self.documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks

    def create_vector_store(self):
        """Create FAISS index and persist to disk"""
        if not self.documents:
            raise ValueError("No documents loaded. Call load_documents_from_text() first.")

        chunks = self.chunk_documents()
        print("Building FAISS index...")
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.vectorstore.save_local(self.index_path)
        print(f"Vector store saved to '{self.index_path}/'")
        return self.vectorstore

    def load_vector_store(self):
        """Load existing FAISS index from disk"""
        if os.path.exists(self.index_path):
            self.vectorstore = FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Vector store loaded from '{self.index_path}/'")
            return self.vectorstore
        raise FileNotFoundError(f"No vector store at '{self.index_path}'")

    def retrieve_context(self, query: str, k: int = 4) -> list:
        """Return top-k relevant chunks for a query"""
        if self.vectorstore is None:
            self.load_vector_store()

        results = self.vectorstore.similarity_search_with_score(query, k=k)
        docs = []
        for doc, score in results:
            relevance = max(0.0, round(1.0 - float(score) / 2.0, 3))
            docs.append({
                "content": doc.page_content.strip(),
                "source": doc.metadata.get("source", "Unknown"),
                "relevance_score": relevance
            })
        return docs

    def get_stats(self) -> dict:
        if self.vectorstore is None:
            return {"status": "not_loaded", "total_vectors": 0}
        return {
            "status": "loaded",
            "total_vectors": self.vectorstore.index.ntotal,
            "index_path": self.index_path
        }


# Singleton
rag = RAGPipeline()


if __name__ == "__main__":
    from sample_documents import CLINICAL_DOCS
    rag.load_documents_from_text(CLINICAL_DOCS)
    rag.create_vector_store()

    queries = [
        "What are the types of clinical trials?",
        "What is informed consent?",
        "What is a serious adverse event?"
    ]
    for q in queries:
        print(f"\nQ: {q}")
        for i, doc in enumerate(rag.retrieve_context(q, k=2), 1):
            print(f"  {i}. [{doc['relevance_score']:.3f}] {doc['source']}")
            print(f"     {doc['content'][:180]}...")
