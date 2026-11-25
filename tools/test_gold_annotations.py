#!/usr/bin/env python3
"""Minimal schema check for gold/v1/annotations.yaml (TST-D scaffold)."""

from __future__ import annotations

import re
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
    if "BAD-A" in text and "expected_fix:" not in text:
        sys.exit(1)
    for bad in ("BAD-B", "BAD-C", "BAD-D", "QUES-1", "ARD-BM"):
        if bad not in text:
            print(f"gold missing {bad}", file=sys.stderr)
            sys.exit(1)
    write = (ROOT / "skills/spec-write/SKILL.md").read_text(encoding="utf-8")
    for needle in ("QUES-A", "**挡住：**", "No strikethrough outside decision-history"):
        if needle not in write:
            print(f"spec-write missing {needle}", file=sys.stderr)
            sys.exit(1)
    review = (ROOT / "skills/spec-review/SKILL.md").read_text(encoding="utf-8")
    if "QUES-A" not in review or "carries strikethrough" not in review:
        print("spec-review missing QUES or strike rule", file=sys.stderr)
        sys.exit(1)
    reader = (ROOT / "docs/book/html/spec-driven-development/spec-driven-development-reader.html").read_text(encoding="utf-8")
    if "隐藏删除线" not in reader:
        print("reader missing strike toggle", file=sys.stderr)
        sys.exit(1)
    h2 = reader.split(".md-body h2{", 1)[1].split("}", 1)[0]
    h3 = reader.split(".md-body h3{", 1)[1].split("}", 1)[0]
    px = lambda css: float(re.search(r"font-size:([\d.]+)px", css).group(1))
    if px(h2) <= px(h3):
        print("reader heading scale is flat", file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(ids)} annotation(s); TST-U skill and reader")


if __name__ == "__main__":
    main()
