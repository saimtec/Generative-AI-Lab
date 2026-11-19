from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


def load_pdf_file(pdf_path: Path) -> List[Document]:
    """Load one PDF and return one LangChain Document per page."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    documents = PyPDFLoader(str(pdf_path)).load()

    for document in documents:
        document.metadata["source_file"] = pdf_path.name
        document.metadata["file_type"] = "pdf"

    return documents


def load_pdf_directory(pdf_directory: Path) -> List[Document]:
    """Load every PDF in a directory recursively."""
    pdf_directory = Path(pdf_directory)
    if not pdf_directory.is_dir():
        raise FileNotFoundError(f"PDF directory not found: {pdf_directory}")

    pdf_files = sorted(pdf_directory.glob("**/*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {pdf_directory}")

    documents: List[Document] = []
    for pdf_file in pdf_files:
        documents.extend(load_pdf_file(pdf_file))

    return documents
