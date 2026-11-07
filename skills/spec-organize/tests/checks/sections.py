"""Required section headings by type (DSGN-E summary)."""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

from checks.frontmatter import _parse_frontmatter

REQUIRED: dict[str, tuple[str, ...]] = {
    "prd": (
        "Overview",
        "Goals and Success Metrics",
        "User Stories",
        "Functional Requirements",
        "Out of Scope",
        "Resources Needed",
    ),
    "design": (
        "Problem Statement",
        "Solution",
        "User Stories",
        "Implementation Decisions",
        "Design",
        "Testing Decisions",
        "Out of Scope",
        "Further Notes",
        "Alternatives Considered",
        "Drawbacks",
        "Risks and Mitigations",
        "Open Questions",
        "Reversibility",
    ),
    "impl-plan": ("Global Constraints", "Acceptance Criteria"),
    "test-plan": (
        "Test Cases",
        "Test Execution Order",
        "Expected Pass Threshold",
    ),
    "decision-history": ("Decision Log", "Evidence Appendix"),
}


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


HEADING = re.compile(r"^##\s+(?:\d+(?:\.\d+)*[.)]?\s+)?(.+?)\s*$", re.M)


def _headings(raw: str) -> list[str]:
    return [h.strip() for h in HEADING.findall(raw)]


def check_sections(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm:
        return []
    t = fm.get("type", "")
    need = REQUIRED.get(t)
    if not need:
        return []
    heads = _headings(raw)
    # Parent HLD-style designs are identified by their content, not by numbering.
    if t == "design" and re.search(r"^#{2,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?System Context\s*$", raw, re.M):
        return []
    rel = str(path)
    findings: list[Finding] = []
    for title in need:
        if not any(h == title for h in heads):
            findings.append(Finding("sections", rel, f"missing required section: ## {title}"))
    return findings
