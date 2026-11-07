"""Book summaries must link canonical paths, never be the only home of a fact (DSGN-D)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

LINK = re.compile(r"\]\((\.\./features/[^)#]+\.md)\)")


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_book(repo_root: Path) -> list[Finding]:
    """No book directory means no assembled summary to police."""
    book = repo_root / "docs/book"
    if not book.is_dir():
        return []
    findings: list[Finding] = []
    for page in sorted(book.rglob("*.md")):
        if page.name.startswith("._"):
            continue
        text = page.read_text(encoding="utf-8", errors="ignore")
        for link in LINK.findall(text):
            if not (page.parent / link).resolve().exists():
                findings.append(
                    Finding("book", str(page), f"summary links missing canonical path: {link}")
                )
    return findings
