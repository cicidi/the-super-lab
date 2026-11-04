#!/usr/bin/env python3
"""Smoke-check spec-driven-development-reader.html after build (DSGN-N deliverable)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "docs/features/spec-driven-development/spec-driven-development-reader.html"

REQUIRED_PANELS = (
    "p-prd",
    "p-design",
    "p-impl",
    "p-test",
    "p-dh",
    "c-pipeline",
    "c-standard",
)

REQUIRED_SNIPPETS = (
    "SDD reader ·",
    "SPEC-HTML-STANDARD",
    "mermaid.min.js",
    "Human-readable spec",
    'id="p-prd"',
    "Canonical:",
)


def main() -> None:
    if not READER.is_file():
        print(f"missing: {READER}", file=sys.stderr)
        sys.exit(1)
    html = READER.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SNIPPETS if s not in html]
    for pid in REQUIRED_PANELS:
        if f'id="{pid}"' not in html:
            missing.append(f"panel {pid}")
    if missing:
        for m in missing:
            print(f"missing in reader: {m}", file=sys.stderr)
        sys.exit(1)
    print(f"ok: {READER.relative_to(ROOT)} ({READER.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
