#!/usr/bin/env python3
"""Minimal schema check for gold/v1/annotations.yaml (TST-D scaffold)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANN = ROOT / "skills/spec-organize/tests/gold/v1/annotations.yaml"


def main() -> None:
    if not ANN.is_file():
        print(f"missing: {ANN}", file=sys.stderr)
        sys.exit(1)
    text = ANN.read_text(encoding="utf-8")
    if "version: v1" not in text:
        sys.exit(1)
    if "annotations:" not in text:
        sys.exit(1)
    ids = [ln.split("id:", 1)[1].strip() for ln in text.splitlines() if ln.strip().startswith("- id:")]
    if not ids:
        sys.exit(1)
    print(f"ok: {len(ids)} annotation(s)")


if __name__ == "__main__":
    main()
