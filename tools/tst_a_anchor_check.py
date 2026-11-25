#!/usr/bin/env python3
"""TST-A helper: verify each must_registry.yaml `source:` line still holds the rule `text`."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "skills/spec-organize/tests/must_registry.yaml"


def _load_items(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    cur: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("  - id:"):
            if cur:
                items.append(cur)
            cur = {"id": line.split(":", 1)[1].strip()}
        elif not cur:
            continue
        elif line.strip().startswith("source:"):
            cur["source"] = line.split(":", 1)[1].strip()
        elif line.strip().startswith("text:"):
            cur["text"] = str(yaml.safe_load(line.split(":", 1)[1]) or "")
    if cur:
        items.append(cur)
    return items


_MARKER = re.compile(r"^(?:#{1,6}|[-*+]|\d+[.)])\s+")


def _norm(line: str) -> str:
    """Stripped line without a leading heading or list marker."""
    return _MARKER.sub("", line.strip()).strip()


def main() -> None:
    items = _load_items(REG.read_text(encoding="utf-8"))
    missing: list[str] = []
    for it in items:
        src = it.get("source", "")
        if ":" not in src:
            missing.append(f"{it['id']}: bad source {src!r}")
            continue
        rel, line_s = src.rsplit(":", 1)
        try:
            line_no = int(line_s)
        except ValueError:
            missing.append(f"{it['id']}: bad line {line_s!r}")
            continue
        path = ROOT / rel
        if not path.is_file():
            missing.append(f"{it['id']}: missing file {rel}")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if line_no < 1 or line_no > len(lines):
            missing.append(f"{it['id']}: line {line_no} out of range ({rel})")
            continue
        cited, want = _norm(lines[line_no - 1]), _norm(it.get("text", ""))
        # The scanner truncates `text` at 500 chars, so a prefix match is a match.
        if not want or not cited.startswith(want):
            missing.append(f"{it['id']}: drifted, {rel}:{line_no} does not hold the rule text")
    if missing:
        for m in missing:
            print(m, file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(items)} registry anchors")


if __name__ == "__main__":
    main()
