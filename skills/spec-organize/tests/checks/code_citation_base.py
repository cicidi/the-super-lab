"""A file:line citation names the commit it was read at (ARD-AQ)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding, _parse_frontmatter

_FENCE = re.compile(r"```.*?```", re.S)
_CITE = re.compile(r"\b[\w./-]+\.(?:py|js|ts|tsx|java|go|rs|sh|yml|yaml):\d+")
_HEX = re.compile(r"\b[0-9a-f]{7,40}\b", re.I)


def check_code_citation_base(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm or fm.get("type") not in {"design", "impl-plan"}:
        return []
    body = _FENCE.sub("", raw)
    if not _CITE.search(body):
        return []
    if _HEX.search(body):
        return []
    return [
        Finding(
            "code_citation_base",
            str(path),
            "file:line citation needs a 7-40 hex commit in the same file",
        )
    ]
