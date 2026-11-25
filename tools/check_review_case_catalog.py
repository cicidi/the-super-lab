#!/usr/bin/env python3
"""Ensure spec-review cases with expected.yaml match cases/README.md mechanical list."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "skills/spec-review/tests/cases"
README = CASES / "README.md"

CASE_ROW = re.compile(r"^\| `([\w-]+)` \|", re.M)


def documented() -> set[str]:
    """Case slugs listed in the cases/README.md table (the one list of cases)."""
    return set(CASE_ROW.findall(README.read_text(encoding="utf-8")))


def main() -> None:
    if not README.is_file():
        print(f"missing: {README}", file=sys.stderr)
        sys.exit(1)
    on_disk = {
        p.name
        for p in CASES.iterdir()
        if p.is_dir() and (p / "expected.yaml").is_file()
    }
    listed = documented()
    if on_disk != listed:
        extra = on_disk - listed
        missing = listed - on_disk
        if extra:
            print(f"cases not in README: {sorted(extra)}", file=sys.stderr)
        if missing:
            print(f"README cases missing: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(on_disk)} review cases synced with README")


if __name__ == "__main__":
    main()
