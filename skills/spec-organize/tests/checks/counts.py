"""Tracker row counts match the prose (ARD-BB)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding, _parse_frontmatter

_ALL = re.compile(r"all\s+(\d+)\s+questions", re.I)
_ROW = re.compile(r"^###\s+QUES-[A-Z]+\b", re.M)


def check_counts(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm or fm.get("role") != "open-questions":
        return []
    rows = len(_ROW.findall(raw))
    findings: list[Finding] = []
    for n in _ALL.findall(raw):
        if int(n) != rows:
            findings.append(
                Finding("counts", str(path), f"all {n} questions but {rows} QUES rows")
            )
    return findings
