#!/usr/bin/env python3
"""Ensure spec-review cases with expected.yaml match cases/README.md mechanical list."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "skills/spec-review/tests/cases"
README = CASES / "README.md"

# Case slugs listed in cases/README.md table (mechanical scaffold).
DOCUMENTED = frozenset(
    {
        "mechanical-clean-pos",
        "mechanical-missing-test-cases",
        "mechanical-bad-ids",
        "mechanical-missing-frontmatter",
        "mechanical-bad-change-log",
        "mechanical-parent-incomplete",
    }
)


def main() -> None:
    if not README.is_file():
        print(f"missing: {README}", file=sys.stderr)
        sys.exit(1)
    on_disk = {
        p.name
        for p in CASES.iterdir()
        if p.is_dir() and (p / "expected.yaml").is_file()
    }
    if on_disk != set(DOCUMENTED):
        extra = on_disk - DOCUMENTED
        missing = DOCUMENTED - on_disk
        if extra:
            print(f"cases not in README: {sorted(extra)}", file=sys.stderr)
        if missing:
            print(f"README cases missing: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)
    text = README.read_text(encoding="utf-8")
    for slug in DOCUMENTED:
        if slug not in text:
            print(f"cases/README.md missing row for {slug}", file=sys.stderr)
            sys.exit(1)
    print(f"ok: {len(on_disk)} review cases synced with README")


if __name__ == "__main__":
    main()
