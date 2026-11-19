from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHUNK_OVERLAP, CHUNK_SIZE


def split_documents(documents: List[Document]) -> List[Document]:
    """Split pages into overlapping retrieval chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No text chunks were created")

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index
        chunk.metadata["content_length"] = len(chunk.page_content)

    return chunks
