"""Every parent PRD id must be traceable from the feature's test plan (MUST-AA)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

PRD_ID = re.compile(r"PRD-[A-Z]+")


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_test_trace(feature: Path) -> list[Finding]:
    prd_dir = feature / "prd"
    plan = feature / f"test-plan/{feature.name}-test-plan.md"
    if not prd_dir.is_dir() or not plan.is_file():
        return []
    ids: set[str] = set()
    for p in prd_dir.rglob("*.md"):
        if not p.name.startswith("._"):
            ids |= set(PRD_ID.findall(p.read_text(encoding="utf-8")))
    covered = set(PRD_ID.findall(plan.read_text(encoding="utf-8")))
    return [
        Finding("test_trace", str(plan), f"{i} has no test-plan coverage")
        for i in sorted(ids - covered)
    ]
