"""Decision Log shape (SPEC-STANDARD / DSGN-E)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from checks.frontmatter import _parse_frontmatter


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_decision_log(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    rel = str(path)
    fm = _parse_frontmatter(raw)
    if not fm or fm.get("type") != "decision-history":
        return []
    findings: list[Finding] = []
    if "## Decision Log" not in raw:
        findings.append(Finding("decision_log", rel, "missing ## Decision Log section"))
        return findings
    header = ""
    for line in raw.splitlines():
        if re.search(r"\|\s*ID\s*\|", line):
            header = line
            break
    if not header or not re.search(r"\|\s*Date\s*\|", header) or not re.search(r"\|\s*Decision\s*\|", header):
        findings.append(
            Finding("decision_log", rel, "Decision Log table must have ID | Date | Decision")
        )
        return findings
    cells = [c.strip().lower() for c in header.strip().strip("|").split("|")]
    if any(c in {"status", "supersedes"} for c in cells):
        findings.append(Finding("decision_log", rel, "Status and Supersedes columns are forbidden"))
    if len(cells) > 4 or (len(cells) == 4 and cells[3] != "ready"):
        findings.append(Finding("decision_log", rel, "optional 4th column must be Ready"))
    return findings
