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


def _trace_table_ids(plan_text: str) -> set[str]:
    """IDs in the first column of the Traceability table. Prose mentions do not count."""
    m = re.search(r"^## Traceability\b[^\n]*\n(.*?)(?=^## |\Z)", plan_text, re.M | re.S)
    if not m:
        return set()
    found: set[str] = set()
    for line in m.group(1).splitlines():
        if not line.startswith("|"):
            continue
        cell = line.strip().strip("|").split("|", 1)[0]
        cell = cell.replace("*", "").strip()
        if PRD_ID.fullmatch(cell):
            found.add(cell)
    return found


def check_test_trace(feature: Path) -> list[Finding]:
    prd_dir = feature / "prd"
    plan = feature / f"test-plan/{feature.name}-test-plan.md"
    if not prd_dir.is_dir() or not plan.is_file():
        return []
    ids: set[str] = set()
    for p in prd_dir.rglob("*.md"):
        if not p.name.startswith("._"):
            ids |= set(PRD_ID.findall(p.read_text(encoding="utf-8")))
    covered = _trace_table_ids(plan.read_text(encoding="utf-8"))
    return [
        Finding("test_trace", str(plan), f"{i} has no test-plan coverage")
        for i in sorted(ids - covered)
    ]
