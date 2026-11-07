"""Open-question tracker shape (ARD-AO)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding, _parse_frontmatter

_ENTRY = re.compile(r"^###\s+QUES-[A-Z]+\b", re.M)
_Q = re.compile(r"\*\*Question\.\*\*", re.I)
_A = re.compile(r"\*\*Answer(?: so far)?\.\*\*", re.I)
_O = re.compile(r"\*\*(?:Owner|Who answered)(?: \([^)]*\))?\.\*\*", re.I)


def check_open_questions(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm or fm.get("role") != "open-questions":
        return []
    rel = str(path)
    findings: list[Finding] = []
    if "## Open Questions" not in raw:
        findings.append(Finding("open_questions", rel, "tracker requires ## Open Questions"))
    if not _ENTRY.search(raw):
        findings.append(Finding("open_questions", rel, "tracker entry must be ### QUES-<letter>"))
    if not _Q.search(raw) or not _A.search(raw) or not _O.search(raw):
        findings.append(
            Finding("open_questions", rel, "tracker entry needs Question, Answer, and Owner")
        )
    return findings
