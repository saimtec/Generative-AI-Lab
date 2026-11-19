from pathlib import Path
from typing import Dict, List, Optional

from langchain_core.messages import HumanMessage

from .config import FAISS_DIR, TOP_K
from .llm import create_gemini_llm
from .retriever import retrieve_documents
from .vector_store import load_faiss_index


class RAGPipeline:
    """One object that loads the index, retrieves context, and calls Gemini."""

    def __init__(
        self,
        embeddings,
        index_directory: Optional[Path] = None,
        llm=None,
    ):
        self.embeddings = embeddings
        self.index_directory = Path(index_directory or FAISS_DIR)
        self.vector_store = load_faiss_index(self.index_directory, embeddings)
        self.llm = llm or create_gemini_llm()

    def ask(self, question: str, top_k: int = TOP_K) -> Dict:
        retrieved = retrieve_documents(self.vector_store, question, top_k)

        if not retrieved:
            return {
                "answer": "No relevant context found.",
                "sources": [],
                "context": "",
            }

        context = "\n\n".join(result["content"] for result in retrieved)
        sources = [
            {
                "source": result["metadata"].get(
                    "source_file",
                    result["metadata"].get("source", "unknown"),
                ),
                "page": result["metadata"].get("page", "unknown"),
                "chunk_index": result["metadata"].get("chunk_index", "unknown"),
                "distance": result["score"],
            }
            for result in retrieved
        ]

        prompt = f"""Answer the question using only the context below.
If the context is insufficient, say that it does not contain enough information.

Context:
{context}

Question:
{question}

Answer:"""

        response = self.llm.invoke([HumanMessage(content=prompt)])

        return {
            "answer": response.content,
            "sources": sources,
            "context": context,
        }
