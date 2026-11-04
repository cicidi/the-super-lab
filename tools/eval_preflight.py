#!/usr/bin/env python3
"""Preflight gold eval assets (TST-C prep) without calling models."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "skills/spec-organize/tests/gold/v1"
EVAL = ROOT / "skills/spec-organize/tests/eval.yaml"

REQUIRED = (
    GOLD / "requirement.md",
    GOLD / "context.md",
    GOLD / "annotations.yaml",
)

VARIANTS = (
    "budget-conflict",
    "missing-info",
    "midway-change",
    "family-disagree",
)


def main() -> None:
    missing: list[str] = []
    if not EVAL.is_file():
        missing.append(str(EVAL.relative_to(ROOT)))
    for p in REQUIRED:
        if not p.is_file():
            missing.append(str(p.relative_to(ROOT)))
    var_dir = GOLD / "context-variants"
    for name in VARIANTS:
        if not (var_dir / f"{name}.md").is_file():
            missing.append(f"context-variants/{name}.md")
    if missing:
        for m in missing:
            print(f"missing: {m}", file=sys.stderr)
        sys.exit(1)
    print("ok: gold v1 preflight")


if __name__ == "__main__":
    main()
