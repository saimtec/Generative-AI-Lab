import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAG_ROOT = PROJECT_ROOT / "Rag"

PDF_DIR = RAG_ROOT / "data" / "pdf"
FAISS_DIR = RAG_ROOT / "data" / "faiss_index"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

TOP_K = 3
GEMINI_MODEL = "gemini-2.5-flash"

load_dotenv(PROJECT_ROOT / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
