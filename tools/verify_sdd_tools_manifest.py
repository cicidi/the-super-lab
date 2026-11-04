#!/usr/bin/env python3
"""Verify tools listed in README-SDD.md exist under tools/."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "tools/README-SDD.md"
TOOLS = ROOT / "tools"
EXTRA = (
    TOOLS / "run_sdd_mechanical.sh",
    ROOT / "skills/spec-organize/tests/run_mechanical.sh",
    ROOT / "skills/spec-review/tests/run_case_checks.py",
    ROOT / "skills/SDD-DELIVERABLES.md",
    ROOT / "tools/verify_sdd_skills_map.py",
)


def main() -> None:
    if not README.is_file():
        print(f"missing: {README}", file=sys.stderr)
        sys.exit(1)
    text = README.read_text(encoding="utf-8")
    names = set(re.findall(r"`([a-z0-9_]+\.py)`", text))
    names.discard("run_case_checks.py")  # lives under skills/
    missing = [n for n in sorted(names) if not (TOOLS / n).is_file()]
    if missing:
        for n in missing:
            print(f"missing tool: tools/{n}", file=sys.stderr)
        sys.exit(1)
    for path in EXTRA:
        if not path.is_file():
            print(f"missing: {path.relative_to(ROOT)}", file=sys.stderr)
            sys.exit(1)
    print(f"ok: {len(names)} tools from README-SDD + harness entrypoints")


if __name__ == "__main__":
    main()
