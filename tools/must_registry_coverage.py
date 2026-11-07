#!/usr/bin/env python3
"""TST-A coverage: must_registry method/check vs implemented TST-B modules."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "skills/spec-organize/tests/must_registry.yaml"
CHECKS = ROOT / "skills/spec-organize/tests/checks"

IMPLEMENTED = {
    "frontmatter",
    "paths",
    "sections",
    "decision_log",
    "change_log",
    "ids",
    "size",
    "parent_complete",
    "collision",
    "index_book",
    "no_commit",
    "book",
    "publish_nav",
    "test_trace",
    "registry_provenance",
}


def _parse_items(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    cur: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("  - id:"):
            if cur:
                items.append(cur)
            cur = {"id": line.split(":", 1)[1].strip()}
        elif cur and line.strip().startswith("method:"):
            cur["method"] = line.split(":", 1)[1].strip()
        elif cur and line.strip().startswith("check:"):
            raw = line.split(":", 1)[1].strip()
            cur["check"] = raw.strip("'\"")
        elif cur and line.strip().startswith("text:"):
            cur["text"] = line.split(":", 1)[1].strip()
    if cur:
        items.append(cur)
    return items


def main() -> None:
    text = REG.read_text(encoding="utf-8")
    items = _parse_items(text)
    python = [i for i in items if i.get("method") == "python"]
    llm = [i for i in items if i.get("method") != "python"]
    bad_check: list[str] = []
    missing_mod: list[str] = []
    for i in python:
        name = i.get("check", "")
        if not name:
            bad_check.append(i["id"])
            continue
        if name not in IMPLEMENTED:
            missing_mod.append(f"{i['id']}:{name}")
        elif not (CHECKS / f"{name}.py").is_file() and name != "paths":
            missing_mod.append(f"{i['id']}:{name} (no module)")
    print(f"items={len(items)} python={len(python)} llm={len(llm)}")
    if bad_check:
        print("python items missing check:", ", ".join(bad_check))
    if missing_mod:
        print("unknown check modules:", ", ".join(missing_mod))
    mapped = {i.get("check") for i in python if i.get("check")}
    unused = IMPLEMENTED - mapped
    if unused:
        print("note: TST-B modules not yet mapped in registry:", ", ".join(sorted(unused)))
    sys.exit(1 if bad_check or missing_mod else 0)


if __name__ == "__main__":
    main()
