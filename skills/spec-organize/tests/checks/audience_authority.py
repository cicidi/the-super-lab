"""A design that declares audience must say which facts it owns (ARD-AL)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding, _parse_frontmatter

_MARK = re.compile(r"authoritative|\bwins\b|权威|为准", re.I)


def check_audience_authority(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm or fm.get("type") != "design" or not fm.get("audience"):
        return []
    if _MARK.search(raw):
        return []
    return [
        Finding(
            "audience_authority",
            str(path),
            "audience is set but the design does not say what it is authoritative for",
        )
    ]
