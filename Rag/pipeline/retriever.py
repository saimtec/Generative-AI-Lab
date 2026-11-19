from typing import Dict, List


def retrieve_documents(vector_store, query: str, top_k: int = 3) -> List[Dict]:
    """Retrieve the closest chunks and return source-aware results."""
    pairs = vector_store.similarity_search_with_score(query, k=top_k)

    results = []
    for rank, (document, score) in enumerate(pairs, start=1):
        results.append(
            {
                "rank": rank,
                "content": document.page_content,
                "metadata": document.metadata,
                "score": float(score),
            }
        )

    return results
