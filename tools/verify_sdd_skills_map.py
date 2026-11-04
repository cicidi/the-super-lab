#!/usr/bin/env python3
"""Verify paths linked from skills/SDD-DELIVERABLES.md exist."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "skills/SDD-DELIVERABLES.md"


def main() -> None:
    if not MAP.is_file():
        print(f"missing: {MAP}", file=sys.stderr)
        sys.exit(1)
    text = MAP.read_text(encoding="utf-8")
    links = re.findall(r"\]\(([^)]+)\)", text)
    missing: list[str] = []
    for rel in links:
        if rel.startswith("http"):
            continue
        path = ROOT / "skills" / rel if not rel.startswith("spec-") else ROOT / "skills" / rel
        # Links are like spec-pipeline/SKILL.md from within skills/
        path = (MAP.parent / rel).resolve()
        if not path.is_file():
            missing.append(rel)
    if missing:
        for m in missing:
            print(f"missing skill path: {m}", file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(links)} SDD-DELIVERABLES link(s)")


if __name__ == "__main__":
    main()
