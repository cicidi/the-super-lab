"""Required section headings by type (DSGN-E summary)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from checks.frontmatter import _parse_frontmatter

REQUIRED: dict[str, tuple[str, ...]] = {
    "design": (
        "Problem Statement",
        "Solution",
        "Design",
        "Out of Scope",
    ),
    "impl-plan": ("Global Constraints",),
    "test-plan": (
        "Test Cases",
        "Test Execution Order",
        "Expected Pass Threshold",
    ),
    "decision-history": ("Decision Log",),
}


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_sections(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm:
        return []
    t = fm.get("type", "")
    need = REQUIRED.get(t)
    if not need:
        return []
    rel = str(path)
    findings: list[Finding] = []
    for title in need:
        if f"## {title}" not in raw:
            findings.append(Finding("sections", rel, f"missing required section: ## {title}"))
    return findings
