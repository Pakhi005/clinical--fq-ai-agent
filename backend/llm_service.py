# llm_service.py - LangChain 0.3 + Gemini 1.5 Flash
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from rag_pipeline import rag

load_dotenv()

CLINICAL_PROMPT = """You are ClinicalBot, an expert AI assistant specializing in clinical research and trials.

Answer questions ONLY using the provided context. If the answer is not in the context, say:
"I don't have enough information to answer that accurately. Please consult a healthcare professional or visit clinicaltrials.gov."

Do NOT make up information. Do NOT give specific medical advice.

Context:
{context}

Question: {question}

Answer (use bullet points or numbered lists where helpful):"""


class LLMService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("WARNING: GOOGLE_API_KEY not set in backend/.env")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3,
            max_output_tokens=1024,
        )
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=CLINICAL_PROMPT
        )

    def generate_answer(self, question: str, context_docs: list) -> dict:
        if not context_docs:
            return {
                "answer": "I couldn't find relevant information in the knowledge base.",
                "sources": [], "safe": True, "confidence": "low"
            }

        context_text = "\n\n---\n\n".join(
            f"[{doc['source']}]\n{doc['content']}"
            for doc in context_docs
        )

        prompt_str = self.prompt.format(context=context_text, question=question)

        try:
            response = self.llm.invoke(prompt_str)
            answer = response.content
            safety = self._safety_check(answer)
            return {
                "answer": answer,
                "sources": list(dict.fromkeys(d["source"] for d in context_docs)),
                "safe": safety["safe"],
                "confidence": safety["confidence"]
            }
        except Exception as e:
            err = str(e)
            print(f"LLM error: {err}")
            if "api" in err.lower() or "key" in err.lower() or "credential" in err.lower():
                msg = "API key issue. Please check your GOOGLE_API_KEY in backend/.env"
            else:
                msg = "An error occurred generating the answer. Please try again."
            return {"answer": msg, "sources": [], "safe": False, "confidence": "none"}

    def _safety_check(self, answer: str) -> dict:
        lower = answer.lower()
        unsafe = ["take this medication", "you should take", "i recommend you take",
                  "diagnose you with", "you have the condition"]
        if any(p in lower for p in unsafe):
            return {"safe": False, "confidence": "low"}
        if any(p in lower for p in ["don't have enough", "i don't know", "not in the context"]):
            return {"safe": True, "confidence": "low"}
        if 80 < len(answer) < 3000:
            return {"safe": True, "confidence": "high"}
        return {"safe": True, "confidence": "medium"}


# Singleton
llm_service = LLMService()


if __name__ == "__main__":
    from sample_documents import CLINICAL_DOCS
    try:
        rag.load_vector_store()
    except FileNotFoundError:
        rag.load_documents_from_text(CLINICAL_DOCS)
        rag.create_vector_store()

    q = "What is a Phase II clinical trial?"
    ctx = rag.retrieve_context(q)
    result = llm_service.generate_answer(q, ctx)
    print(f"\nQ: {q}")
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")
    print(f"Confidence: {result['confidence']}")
