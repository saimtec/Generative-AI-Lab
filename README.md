# Generative AI Lab

This repository contains my hands-on Generative AI learning projects. It
includes small notebooks and practical examples built while learning how
language models, tools, agents, workflows, retrieval systems, and evaluations
work.

The code is intentionally organised by topic so each example can be opened,
read, changed, and run independently.

## Topics

- LangChain fundamentals and model integration
- Tool calling and structured output
- LangGraph workflows and human feedback
- Retrieval-augmented generation
- Model Context Protocol (MCP)
- Agents and deep-agent workflows
- Multi-agent systems
- Memory and state management
- LLM evaluation and observability

## Repository layout

```text
.
├── Langchain/       # LangChain notebooks and examples
├── Langgraph/       # LangGraph workflows
├── MCP/             # MCP servers and clients
├── Rag/             # RAG experiments
├── experiments/     # Additional experiments
├── pyproject.toml   # Project dependencies
└── requirement.txt  # Alternative dependency list
```

## Requirements

- Python 3.11 or newer
- Git
- An API key for the model provider used by an example
- `uv` is recommended for dependency management

## Installation

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/saimtec/Generative-AI-Lab.git
Set-Location "Generative-AI-Lab"
```

Create the environment and install dependencies:

```powershell
uv sync
```

If you do not use `uv`, create a virtual environment and install the
dependencies from `requirement.txt`.

## API configuration

Copy `.env.example` to `.env`:

```powershell
Copy-Item ".env.example" ".env"
```

Then add your own keys to `.env`. Never put real keys in notebooks, Python
files, or commits.

### Gemini

```env
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_GENAI_MODEL=gemini-2.5-flash
```

### Groq

```env
GROQ_API_KEY=your_groq_api_key
```

### OpenAI

```env
OPENAI_API_KEY=your_openai_api_key
```

### Ollama

Ollama runs locally and normally does not require an API key:

```env
OLLAMA_MODEL=your_local_model
OLLAMA_HOST=http://localhost:11434
```

Start Ollama separately and make sure the selected model is installed.

### Optional LangSmith tracing

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=generative-ai-lab
```

Only add optional variables when the example requires them.

## Running examples

### Jupyter notebooks

```powershell
uv run jupyter notebook
```

Open the notebook for the topic you want to study and run its cells from top
to bottom.

### Python examples

Run a Python file from the repository root:

```powershell
uv run python "MCP\main.py"
```

The exact command may differ between examples. Check the first cells of the
related notebook or the file itself for provider and environment requirements.

## Keeping data private

Local API keys, PDFs, downloaded documents, generated indexes, caches, and
other local data are ignored by Git. Check `.gitignore` before adding new
datasets or generated files.

## Learning approach

The projects are built progressively: start with model calls, then learn tools
and structured responses, followed by workflows, retrieval, agents, and
evaluation. Each example is meant to be a starting point for experimentation,
not a finished production framework.
