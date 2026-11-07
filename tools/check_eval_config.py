#!/usr/bin/env python3
"""Validate skills/spec-organize/tests/eval.yaml shape (TST-J prep; no PyYAML required)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "skills/spec-organize/tests/eval.yaml"

REQUIRED_TOP = ("judge:", "gold:", "target:", "grill:", "checkers:")
REQUIRED_SNIPPETS = (
    "version:",
    "models:",  # gold.models and checkers.models lines both contain models:
    "repo:",
    "feature:",
    "skills:",
)


def main() -> None:
    if not EVAL.is_file():
        print(f"missing: {EVAL}", file=sys.stderr)
        sys.exit(1)
    text = EVAL.read_text(encoding="utf-8")
    missing = [k for k in REQUIRED_TOP if k not in text]
    if missing:
        for k in missing:
            print(f"eval.yaml: missing section {k}", file=sys.stderr)
        sys.exit(1)
    for snip in REQUIRED_SNIPPETS:
        if snip not in text:
            print(f"eval.yaml: missing key line containing {snip!r}", file=sys.stderr)
            sys.exit(1)
    if text.count("models:") < 2:
        print("eval.yaml: expected gold.models and checkers.models", file=sys.stderr)
        sys.exit(1)
    print("ok: eval.yaml schema")


if __name__ == "__main__":
    main()
