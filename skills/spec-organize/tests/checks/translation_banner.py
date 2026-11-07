"""A local translation names its source in the first 40 lines (ARD-AU)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding

_NAME = re.compile(r"^.+\.[a-z]{2}(?:-[a-z]{2})?\.md$")
_MARK = re.compile(r"为准|source of truth|authoritative", re.I)
_LINK = re.compile(r"\]\([^)]+\.md\)")


def check_translation_banner(path: Path, text: str | None = None) -> list[Finding]:
    if not _NAME.match(path.name):
        return []
    raw = text if text is not None else path.read_text(encoding="utf-8")
    head = "\n".join(raw.splitlines()[:40])
    if _MARK.search(head) and _LINK.search(head):
        return []
    return [
        Finding(
            "translation_banner",
            str(path),
            "translation must link the source and say it is authoritative",
        )
    ]
