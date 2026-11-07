#!/usr/bin/env python3
"""Assert fixtures/pos/* trees pass per-file TST-B checkers (no false positives)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POS = ROOT / "skills/spec-organize/tests/fixtures/pos"
TESTS = ROOT / "skills/spec-organize/tests"
sys.path.insert(0, str(TESTS))

from checks.runners import run_file  # noqa: E402


def main() -> None:
    if not POS.is_dir():
        print(f"missing: {POS}", file=sys.stderr)
        sys.exit(1)
    errors: list[str] = []
    count = 0
    for fixture in sorted(POS.iterdir()):
        if not fixture.is_dir():
            continue
        for path in sorted(fixture.rglob("*.md")):
            if path.name.startswith("._"):
                continue
            count += 1
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"{path}: not utf-8")
                continue
            for f in run_file(path, text):
                errors.append(f"{fixture.name}: {f.check} {f.path} — {f.message}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)
    print(f"ok: {count} pos markdown file(s)")


if __name__ == "__main__":
    main()
