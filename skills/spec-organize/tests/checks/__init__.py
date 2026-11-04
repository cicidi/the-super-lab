"""Mechanical spec checks (TST-B). See parent test-plan."""

from checks.frontmatter import check_frontmatter
from checks.paths import check_committed_path

__all__ = ["check_frontmatter", "check_committed_path"]
