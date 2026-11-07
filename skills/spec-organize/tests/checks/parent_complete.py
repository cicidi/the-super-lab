"""Parent initiative five committed types (parent HLD §8 / TST-N)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

TYPES = ("prd", "design", "impl-plan", "test-plan", "decision-history")


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_parent_complete(feature_root: Path) -> list[Finding]:
    """`<f>` = `docs/features/<f>/` parent (may contain `features/` subdir)."""
    if feature_root.name == "features" or not feature_root.is_dir():
        return []
    rel = feature_root.as_posix()
    if "/docs/features/" not in rel:
        return []
    findings: list[Finding] = []
    slug = feature_root.name
    for t in TYPES:
        dirp = feature_root / t
        if not dirp.is_dir():
            findings.append(Finding("parent_complete", rel, f"missing directory `{t}/`"))
            continue
        if not any(dirp.glob(f"{slug}-{t}*.md")):
            findings.append(
                Finding("parent_complete", rel, f"missing entry `{t}/{slug}-{t}.md` (or part)")
            )
    return findings
