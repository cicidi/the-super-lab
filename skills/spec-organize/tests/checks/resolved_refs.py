"""A QUES citation's nearby status matches the tracker (ARD-BC)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding

_LINK = re.compile(r"\[QUES-([A-Z]+)\]\(([^)#]+)(?:#[^)]+)?\)")
_OPEN = re.compile(r"未决|open", re.I)
_CLOSED = re.compile(r"已决|closed|resolved", re.I)


def _status(chunk: str) -> str | None:
    if _OPEN.search(chunk):
        return "open"
    if _CLOSED.search(chunk):
        return "closed"
    return None


def check_resolved_refs(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    for m in _LINK.finditer(raw):
        letter, rel_file = m.group(1), m.group(2)
        window = raw[m.end() : m.end() + 80]
        here = _status(window)
        if here is None:
            continue
        dest = (path.parent / rel_file).resolve()
        if not dest.is_file():
            continue
        other = dest.read_text(encoding="utf-8", errors="replace")
        entry = re.search(rf"(?ms)^###\s+QUES-{letter}\b.*?(?=^###\s+|\Z)", other)
        if not entry:
            continue
        there = _status(entry.group(0))
        if there and there != here:
            findings.append(
                Finding(
                    "resolved_refs",
                    str(path),
                    f"QUES-{letter} is {here} here and {there} in the tracker",
                )
            )
    return findings
