from .config import FAISS_DIR, PDF_DIR
from .document_loader import load_pdf_directory
from .embeddings import create_embedding_model
from .text_splitter import split_documents
from .vector_store import build_faiss_index


def build_index():
    print(f"Loading PDFs from: {PDF_DIR}")
    documents = load_pdf_directory(PDF_DIR)
    print(f"Loaded PDF pages: {len(documents)}")

    chunks = split_documents(documents)
    print(f"Created chunks: {len(chunks)}")

    embeddings = create_embedding_model()
    build_faiss_index(chunks, embeddings, FAISS_DIR)
    print(f"Saved FAISS index to: {FAISS_DIR}")


if __name__ == "__main__":
    build_index()
