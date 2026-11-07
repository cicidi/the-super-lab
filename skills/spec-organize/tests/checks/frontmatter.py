"""Frontmatter MUST checks (SPEC-STANDARD)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REQUIRED = ("feature", "type", "state")
VALID_TYPES = frozenset(
    {"prd", "design", "impl-plan", "test-plan", "decision-history", "how-to"}
)
VALID_STATE = frozenset({"draft", "final"})


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def _parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([a-zA-Z0-9_]+):\s*(.*)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


def check_frontmatter(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    rel = str(path)
    fm = _parse_frontmatter(raw)
    findings: list[Finding] = []
    if fm is None:
        findings.append(Finding("frontmatter", rel, "missing YAML frontmatter block"))
        return findings
    for key in REQUIRED:
        if key not in fm or not fm[key]:
            findings.append(Finding("frontmatter", rel, f"missing required key: {key}"))
    if "status" in fm:
        findings.append(Finding("frontmatter", rel, "use health not status"))
    t = fm.get("type", "")
    if t and t not in VALID_TYPES:
        findings.append(Finding("frontmatter", rel, f"invalid type: {t}"))
    st = fm.get("state", "")
    if st and st not in VALID_STATE:
        findings.append(Finding("frontmatter", rel, f"invalid state: {st}"))
    if fm.get("state") == "final" and not fm.get("final_date"):
        findings.append(Finding("frontmatter", rel, "final state requires final_date"))
    return findings
