import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Rag.pipeline.embeddings import create_embedding_model
from Rag.pipeline.rag_pipeline import RAGPipeline


@st.cache_resource
def get_pipeline():
    return RAGPipeline(create_embedding_model())


st.set_page_config(page_title="RAG PDF Assistant", page_icon="📄")
st.title("RAG PDF Assistant")

question = st.text_input("Ask a question about the PDF documents")

if st.button("Ask") and question.strip():
    with st.spinner("Retrieving and generating answer..."):
        result = get_pipeline().ask(question)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")
    for source in result["sources"]:
        st.write(source)
