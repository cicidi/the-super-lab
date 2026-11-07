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


RAW_H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
_NUM = re.compile(r"^(?:\d+(?:\.\d+)*[.)]?\s+)(.+)$")
_PART = re.compile(r"^(.+)-design-.+\.md$")


def _bare(title: str) -> tuple[bool, str]:
    m = _NUM.match(title.strip())
    if m:
        return True, m.group(1).strip()
    return False, title.strip()


def _headings(raw: str) -> list[tuple[bool, str]]:
    return [_bare(h) for h in RAW_H2.findall(raw)]


def check_sections(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm:
        return []
    t = fm.get("type", "")
    if fm.get("role") == "open-questions":
        need = ("Open Questions",)
    else:
        need = REQUIRED.get(t)
    if not need:
        return []
    heads = _headings(raw)
    # Parent HLD-style designs are identified by their content, not by numbering.
    if t == "design" and re.search(r"^#{2,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?System Context\s*$", raw, re.M):
        return []
    rel = str(path)
    findings: list[Finding] = []
    part = _PART.match(path.name)
    if t == "design" and part:
        entry = f"{part.group(1)}-design.md"
        if entry not in raw:
            findings.append(Finding("sections", rel, f"design part must link back to {entry}"))
        return findings
    bare = [title for _numbered, title in heads]
    for numbered, title in heads:
        if numbered and title in need:
            findings.append(Finding("sections", rel, f"numbered required heading: ## {title}"))
    for title in need:
        if title not in bare:
            findings.append(Finding("sections", rel, f"missing required section: ## {title}"))
    return findings
