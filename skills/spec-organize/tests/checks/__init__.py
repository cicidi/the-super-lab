"""Mechanical spec checks (TST-B). See parent test-plan."""

from checks.decision_log import check_decision_log
from checks.frontmatter import check_frontmatter
from checks.paths import check_committed_path
from checks.sections import check_sections

__all__ = [
    "check_frontmatter",
    "check_committed_path",
    "check_decision_log",
    "check_sections",
]
