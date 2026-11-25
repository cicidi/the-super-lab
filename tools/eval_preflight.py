#!/usr/bin/env python3
"""Preflight gold eval assets (TST-C prep) without calling models."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/features/spec-driven-development"
EVAL = ROOT / "skills/spec-organize/tests/eval.yaml"

REQUIRED = (
    SPEC / "prd/spec-driven-development-prd.md",
    SPEC / "design/spec-driven-development-design.md",
    SPEC / "decision-history/spec-driven-development-decision-history.md",
    SPEC / "impl-plan/spec-driven-development-impl-plan.md",
    SPEC / "test-plan/spec-driven-development-test-plan.md",
    ROOT / "skills/spec-organize/tests/gold/v1/annotations.yaml",
)


def main() -> None:
    missing: list[str] = []
    if not EVAL.is_file():
        missing.append(str(EVAL.relative_to(ROOT)))
    for p in REQUIRED:
        if not p.is_file():
            missing.append(str(p.relative_to(ROOT)))
    if missing:
        for m in missing:
            print(f"missing: {m}", file=sys.stderr)
        sys.exit(1)
    print("ok: gold spec is spec-driven-development")


if __name__ == "__main__":
    main()
