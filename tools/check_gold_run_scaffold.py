#!/usr/bin/env python3
"""Verify gold v1 run/exemplar scaffold (TST-C prep; no model outputs required)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "skills/spec-organize/tests/gold/v1"

REQUIRED = (
    GOLD / "TST-C-RUNBOOK.md",
    GOLD / "runs/README.md",
    GOLD / "runs/_template/interview.md",
    GOLD / "exemplar/README.md",
    GOLD / "POS-FIXTURE-REFERENCE.md",
)


def main() -> None:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.is_file()]
    if missing:
        for m in missing:
            print(f"missing: {m}", file=sys.stderr)
        sys.exit(1)
    print("ok: gold v1 run scaffold")


if __name__ == "__main__":
    main()
