# Generative AI Lab

This repository is my hands-on Generative AI learning workspace. It contains
small experiments, notebooks, and working examples that I build while learning
how modern AI applications are designed.

The focus is on understanding the fundamentals first and then connecting them
into more useful systems.

## What is included

### LangChain

Examples covering model integration, messages, tool calling, structured output,
middleware, and memory.

### LangGraph

Examples of graph-based applications, chatbots, and human-feedback workflows.

### RAG

Traditional retrieval-augmented generation examples using documents and PDFs.

### Vectorless RAG

A tree-based RAG system that:

1. Extracts text from a document while preserving page numbers.
2. Uses Gemini to create a table-of-contents-style JSON tree.
3. Selects relevant sections for a user question.
4. Retrieves the original pages.
5. Generates an answer with page citations.

### MCP

Small Model Context Protocol servers and clients, including tool-based examples.

### Planned work

- Deep agent workflows
- Multi-agent systems
- Long-term and short-term memory
- LLM evaluation and benchmarking
- Tracing and observability
- Reliable tool use and structured outputs

## Repository layout

```text
.
├── Langchain/       # LangChain experiments
├── Langgraph/       # LangGraph workflows
├── MCP/             # Model Context Protocol examples
├── Rag/             # Traditional RAG experiments
├── Vectorless Rag/  # Tree-based vectorless RAG
├── data/            # Local data; ignored by Git
└── pyproject.toml   # Project dependencies
```

## Requirements

- Python 3.11 or newer
- A virtual environment
- API keys for the providers used by an example

Install the project dependencies with:

```powershell
uv sync
```

Create a local `.env` file when an example needs an API key. Keep credentials
out of notebooks and source code. The `.env` file, PDFs, local data, and
generated files are ignored by Git.

## Running the vectorless RAG example

Run these commands from the repository root in PowerShell:

```powershell
& ".\.venv\Scripts\python.exe" "Vectorless Rag\scripts\extract_pages.py" "Vectorless Rag\PDF\your-paper.pdf" -o "Vectorless Rag\data\pages.json"
```

```powershell
& ".\.venv\Scripts\python.exe" "Vectorless Rag\scripts\build_tree.py" "Vectorless Rag\data\pages.json" -o "Vectorless Rag\data\tree.json"
```

```powershell
& ".\.venv\Scripts\python.exe" "Vectorless Rag\scripts\query_tree.py" "What is the main contribution of this research?"
```

## Learning approach

Each folder is a practical step in the learning process. The examples are kept
small so that the code can be read, run, changed, and tested instead of being
treated as a black box.
