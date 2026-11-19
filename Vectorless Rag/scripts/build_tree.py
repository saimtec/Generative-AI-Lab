"""Build a hierarchical JSON index from page-preserving PDF text using Gemini."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def read_pages(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["pages"]


def page_text_for_prompt(pages: list[dict[str, Any]]) -> str:
    return "\n\n".join(f"[PAGE {page['page']}]\n{page['text']}" for page in pages)


def parse_json(response: str) -> dict[str, Any]:
    """Parse plain JSON or JSON wrapped in a Markdown code fence."""
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
    candidate = match.group(1) if match else response.strip()
    result = json.loads(candidate)
    if not isinstance(result, dict):
        raise ValueError("Gemini returned JSON, but the root value was not an object.")
    return result


def build_tree(pages: list[dict[str, Any]], model_name: str) -> dict[str, Any]:
    model = ChatGoogleGenerativeAI(model=model_name, temperature=0)
    prompt = f"""
Create a hierarchical table-of-contents tree for this research paper.

Rules:
- Return ONLY valid JSON. Do not use Markdown fences.
- Use this exact shape:
  {{
    "title": "document title",
    "summary": "one sentence summary",
    "pages": [1, 2],
    "children": [
      {{
        "title": "section title",
        "summary": "one sentence summary",
        "pages": [3, 4],
        "children": []
      }}
    ]
  }}
- Use integers for page numbers.
- Include every meaningful section and subsection.
- Assign each section the pages where its content appears.
- Do not invent sections or page numbers.

Paper pages:
{page_text_for_prompt(pages)}
"""
    response = model.invoke(prompt)
    content = response.content
    if not isinstance(content, str):
        raise TypeError("Gemini returned a non-text response.")
    return parse_json(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", type=Path, default=Path("data/pages.json"), nargs="?")
    parser.add_argument("-o", "--output", type=Path, default=Path("data/tree.json"))
    args = parser.parse_args()

    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is missing from the environment.")

    model_name = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-flash")
    tree = build_tree(read_pages(args.pages), model_name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(tree, indent=2), encoding="utf-8")
    print(f"Saved tree index to {args.output}")


if __name__ == "__main__":
    main()
