"""One per-file runner list for lint and score (section 6)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.anchors import check_anchors
from checks.audience_authority import check_audience_authority
from checks.change_log import check_change_log
from checks.code_citation_base import check_code_citation_base
from checks.counts import check_counts
from checks.decision_log import check_decision_log
from checks.diagram_steps import check_diagram_steps
from checks.frontmatter import check_frontmatter
from checks.ids import check_ids
from checks.impl_tasks import check_impl_tasks
from checks.open_questions import check_open_questions
from checks.paths import check_committed_path
from checks.resolved_refs import check_resolved_refs
from checks.section_refs import check_section_refs
from checks.sections import check_sections
from checks.size import check_size
from checks.translation_banner import check_translation_banner

_TRANSLATION = re.compile(r"^.+\.[a-z]{2}(?:-[a-z]{2})?\.md$")

RUNNERS = [
    check_frontmatter,
    check_committed_path,
    check_sections,
    check_decision_log,
    check_change_log,
    check_ids,
    check_size,
    check_audience_authority,
    check_open_questions,
    check_anchors,
    check_code_citation_base,
    check_impl_tasks,
    check_translation_banner,
    check_section_refs,
    check_counts,
    check_resolved_refs,
    check_diagram_steps,
]


def run_file(path: Path, text: str) -> list:
    """Translation copies are banner-only (ARD-AU)."""
    if _TRANSLATION.match(path.name):
        return check_translation_banner(path, text)
    findings = []
    for fn in RUNNERS:
        findings.extend(fn(path, text))
    return findings
