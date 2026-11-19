# RAG Pipeline

This folder separates a RAG application into focused modules.

```text
build_index.py    Loads PDFs, splits text, creates embeddings, saves FAISS
document_loader.py Reads PDFs into LangChain Document objects
text_splitter.py  Divides documents into overlapping chunks
embeddings.py     Loads the Hugging Face embedding model
vector_store.py   Builds or loads the FAISS index
retriever.py      Searches FAISS for relevant chunks
llm.py            Creates the Gemini chat model
rag_pipeline.py   Coordinates retrieval and answer generation
main.py           Command-line interface
app.py            Streamlit website interface
```

Run from the repository root:

```powershell
.venv\Scripts\python.exe -m Rag.pipeline.build_index
.venv\Scripts\python.exe -m Rag.pipeline.main
.venv\Scripts\python.exe -m streamlit run Rag/pipeline/app.py
```
