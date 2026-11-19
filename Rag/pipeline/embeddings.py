from langchain_huggingface import HuggingFaceEmbeddings

from .config import EMBEDDING_MODEL


def create_embedding_model() -> HuggingFaceEmbeddings:
    """Create the model used for both document and query embeddings."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
