from .embeddings import create_embedding_model
from .rag_pipeline import RAGPipeline


def main():
    embeddings = create_embedding_model()
    pipeline = RAGPipeline(embeddings)

    print("RAG pipeline ready. Type 'exit' to stop.")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        result = pipeline.ask(question)
        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print(source)


if __name__ == "__main__":
    main()
