"""INDEX dead links and orphan committed entries (DSGN-D)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from checks.paths import COMMITTED_TYPES, ENTRY_RE

LINK_RE = re.compile(r"\]\((features/[^)#]+\.md)\)")


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def _committed_relative(path: Path, docs_dir: Path) -> str | None:
    rel = path.relative_to(docs_dir).as_posix()
    parts = path.parts
    if "features" not in parts:
        return None
    if path.name.startswith("._") or "/raw/" in rel or ".scratch" in rel:
        return None
    if path.parent.name not in COMMITTED_TYPES:
        return None
    if not ENTRY_RE.match(path.name):
        return None
    return rel


def check_index_book(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    docs = repo_root / "docs"
    index = docs / "INDEX.md"
    if not index.is_file():
        findings.append(Finding("index_book", "docs/INDEX.md", "missing INDEX.md"))
        return findings
    text = index.read_text(encoding="utf-8")
    linked: set[str] = set()
    for m in LINK_RE.finditer(text):
        rel = m.group(1)
        linked.add(rel)
        target = docs / rel
        if not target.is_file():
            findings.append(
                Finding("index_book", "docs/INDEX.md", f"dead link: {rel}")
            )
    features = docs / "features"
    if not features.is_dir():
        return findings
    for path in sorted(features.rglob("*.md")):
        rel = _committed_relative(path, docs)
        if rel is None:
            continue
        if rel not in linked and rel not in text:
            findings.append(
                Finding("index_book", rel, "committed entry not linked from INDEX.md")
            )
    return findings
