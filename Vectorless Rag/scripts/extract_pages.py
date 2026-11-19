"""Extract searchable text from a PDF while preserving page numbers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pymupdf


def clean_text(text: str) -> str:
    """Remove layout noise while keeping paragraph and line boundaries."""
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(line for line in lines if line))


def extract_pages(pdf_path: Path) -> list[dict[str, object]]:
    """Return one text record for each PDF page."""
    with pymupdf.open(pdf_path) as document:
        return [
            {"page": page_number, "text": clean_text(page.get_text())}
            for page_number, page in enumerate(document, start=1)
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("data/pages.json"))
    args = parser.parse_args()

    pages = extract_pages(args.pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps({"source": str(args.pdf), "pages": pages}, indent=2),
        encoding="utf-8",
    )
    print(f"Extracted {len(pages)} pages to {args.output}")


if __name__ == "__main__":
    main()
