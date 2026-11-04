"""Mechanical spec checks (TST-B). See parent test-plan."""

from checks.change_log import check_change_log
from checks.parent_complete import check_parent_complete
from checks.decision_log import check_decision_log
from checks.frontmatter import check_frontmatter
from checks.ids import check_ids
from checks.paths import check_committed_path
from checks.sections import check_sections
from checks.size import check_size

__all__ = [
    "check_change_log",
    "check_frontmatter",
    "check_committed_path",
    "check_decision_log",
    "check_ids",
    "check_sections",
    "check_size",
    "check_parent_complete",
]
