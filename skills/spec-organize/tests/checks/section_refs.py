"""§ links and non-overlapping step ranges (ARD-AZ)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding

_RANGE = re.compile(r"(?m)^##\s+.*?steps\s+(\d+)\s*[–-]\s*(\d+)")
_SEC = re.compile(r"\[§\s*(\d+)\]\(#([^)]+)\)")
_H = re.compile(r"(?m)^##\s+(?:(\d+)[.)]?\s+)?(.+)$")


def check_section_refs(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    rel = str(path)
    findings: list[Finding] = []
    ranges = [(int(a), int(b)) for a, b in _RANGE.findall(raw)]
    ranges.sort()
    for (a1, b1), (a2, b2) in zip(ranges, ranges[1:]):
        if a2 <= b1:
            findings.append(Finding("section_refs", rel, f"step ranges overlap: {a1}-{b1} and {a2}-{b2}"))
    numbers = {n for n, _title in _H.findall(raw) if n}
    for num, frag in _SEC.findall(raw):
        if num not in numbers and frag not in raw:
            findings.append(Finding("section_refs", rel, f"§{num} does not land on a heading"))
    return findings
