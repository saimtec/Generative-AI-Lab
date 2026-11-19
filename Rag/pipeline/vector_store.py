from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS


def build_faiss_index(
    chunks: List[Document],
    embeddings,
    index_directory: Path,
) -> FAISS:
    """Create and persist a FAISS index from document chunks."""
    index_directory = Path(index_directory)
    index_directory.mkdir(parents=True, exist_ok=True)

    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(str(index_directory))
    return vector_store


def load_faiss_index(index_directory: Path, embeddings) -> FAISS:
    """Load an existing FAISS index."""
    index_directory = Path(index_directory)
    if not (index_directory / "index.faiss").exists():
        raise FileNotFoundError(
            f"FAISS index not found in {index_directory}. Run build_index.py first."
        )

    return FAISS.load_local(
        str(index_directory),
        embeddings,
        allow_dangerous_deserialization=True,
    )
