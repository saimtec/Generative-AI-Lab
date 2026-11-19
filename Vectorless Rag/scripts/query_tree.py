"""Ask questions against a Gemini-generated tree index."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_tree(node: dict[str, Any], node_id: str = "root") -> list[dict[str, Any]]:
    """Turn nested nodes into a compact list that Gemini can select from."""
    result = [
        {
            "id": node_id,
            "title": node["title"],
            "summary": node["summary"],
            "pages": node["pages"],
        }
    ]
    for index, child in enumerate(node.get("children", []), start=1):
        result.extend(flatten_tree(child, f"{node_id}.{index}"))
    return result


def parse_json(response: str) -> dict[str, Any]:
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
    result = json.loads(match.group(1) if match else response.strip())
    if not isinstance(result, dict):
        raise ValueError("Gemini returned a non-object JSON response.")
    return result


def select_nodes(
    question: str, nodes: list[dict[str, Any]], model: ChatGoogleGenerativeAI
) -> list[str]:
    prompt = f"""
Select the smallest set of document sections needed to answer the question.
Return ONLY valid JSON in this shape:
{{"selected_ids": ["root.1", "root.5.2"]}}

Question: {question}

Available sections:
{json.dumps(nodes, indent=2)}
"""
    response = model.invoke(prompt)
    content = response.content
    if not isinstance(content, str):
        raise TypeError("Gemini returned a non-text selection response.")
    selected = parse_json(content).get("selected_ids")
    if not isinstance(selected, list) or not all(isinstance(item, str) for item in selected):
        raise ValueError("Gemini returned invalid selected_ids.")
    valid_ids = {node["id"] for node in nodes}
    unknown_ids = set(selected) - valid_ids
    if unknown_ids:
        raise ValueError(f"Gemini selected unknown node IDs: {sorted(unknown_ids)}")
    return selected


def pages_for_nodes(
    selected_ids: list[str], nodes: list[dict[str, Any]], pages: list[dict[str, Any]]
) -> str:
    selected_pages = {
        page_number
        for node in nodes
        if node["id"] in selected_ids
        for page_number in node["pages"]
    }
    page_lookup = {page["page"]: page["text"] for page in pages}
    missing_pages = selected_pages - page_lookup.keys()
    if missing_pages:
        raise ValueError(f"Tree referenced missing pages: {sorted(missing_pages)}")
    return "\n\n".join(
        f"[PAGE {page_number}]\n{page_lookup[page_number]}"
        for page_number in sorted(selected_pages)
    )


def answer_question(
    question: str, context: str, model: ChatGoogleGenerativeAI
) -> str:
    prompt = f"""
Answer the question using only the supplied document context.
If the context does not contain the answer, say that clearly.
Cite supporting pages like [page 3] or [pages 3-4].

Question: {question}

Document context:
{context}
"""
    response = model.invoke(prompt)
    if not isinstance(response.content, str):
        raise TypeError("Gemini returned a non-text answer.")
    return response.content


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    parser.add_argument("--tree", type=Path, default=Path("data/tree.json"))
    parser.add_argument("--pages", type=Path, default=Path("data/pages.json"))
    args = parser.parse_args()

    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is missing from the environment.")
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-flash"),
        temperature=0,
    )
    tree = load_json(args.tree)
    pages = load_json(args.pages)["pages"]
    nodes = flatten_tree(tree)
    selected_ids = select_nodes(args.question, nodes, model)
    context = pages_for_nodes(selected_ids, nodes, pages)
    print(f"Selected sections: {', '.join(selected_ids)}")
    print(answer_question(args.question, context, model))


if __name__ == "__main__":
    main()
