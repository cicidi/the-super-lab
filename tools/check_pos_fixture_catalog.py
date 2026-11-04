#!/usr/bin/env python3
"""Ensure fixtures/pos/* matches documented pos fixture set."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POS = ROOT / "skills/spec-organize/tests/fixtures/pos"

# Keep in sync with fixtures/README.md pos list.
DOCUMENTED = frozenset({"valid-test-plan", "valid-decision-history"})


def main() -> None:
    if not POS.is_dir():
        print(f"missing: {POS}", file=sys.stderr)
        sys.exit(1)
    on_disk = {p.name for p in POS.iterdir() if p.is_dir()}
    if on_disk != set(DOCUMENTED):
        extra = on_disk - DOCUMENTED
        missing = DOCUMENTED - on_disk
        if extra:
            print(f"undocumented pos dirs: {sorted(extra)}", file=sys.stderr)
        if missing:
            print(f"documented pos dirs missing: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(on_disk)} pos fixtures synced with README")


if __name__ == "__main__":
    main()
