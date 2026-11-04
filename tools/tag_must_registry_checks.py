#!/usr/bin/env python3
"""Assign method:python and check names to must_registry items where obvious."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "skills/spec-organize/tests/must_registry.yaml"

RULES: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"文件名.*必须|`<f>-<type>|禁止.*reference/", re.I), "python", "paths"),
    (re.compile(r"硬 cap|行数\s*>`|删 L1 凑 cap", re.I), "python", "size"),
    (re.compile(r"DSGN-K|\*\*Collision\*\*|collision 已查", re.I), "python", "collision"),
    (re.compile(r"orphan|dead link|INDEX.*同步", re.I), "python", "index_book"),
    (re.compile(r"ID immutable|凡有序号即 ID|前缀}-\{字母\}|禁止.*裸数字", re.I), "python", "ids"),
    (re.compile(r"Decision Log|倒序", re.I), "python", "decision_log"),
    (re.compile(r"Change Log", re.I), "python", "change_log"),
    (re.compile(r"Commit = no|不得.*进入 git|reference/", re.I), "python", "no_commit"),
    (
        re.compile(r"final_date|health:\s|frontmatter.*必须|Required frontmatter", re.I),
        "python",
        "frontmatter",
    ),
    (re.compile(r"Required sections|必备章节", re.I), "python", "sections"),
    (
        re.compile(r"五篇均在|parent.*五篇|prd.*design.*decision-history.*impl-plan.*test-plan", re.I),
        "python",
        "parent_complete",
    ),
]


def _tag(text_blob: str) -> tuple[str, str]:
    for pat, method, check in RULES:
        if pat.search(text_blob):
            return method, check
    return "llm", ""


def main() -> None:
    lines = REG.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    item_lines: list[str] = []

    def flush_item() -> None:
        nonlocal item_lines
        if not item_lines:
            return
        blob = "\n".join(item_lines)
        method, check = _tag(blob)
        for ln in item_lines:
            if ln.strip().startswith("method:"):
                out.append(f"    method: {method}")
            elif ln.strip().startswith("check:"):
                out.append(f"    check: {check!r}")
            else:
                out.append(ln)
        item_lines = []

    for line in lines:
        if line.startswith("  - id:"):
            flush_item()
            item_lines = [line]
        elif item_lines:
            item_lines.append(line)
        else:
            out.append(line)
    flush_item()
    REG.write_text("\n".join(out) + "\n", encoding="utf-8")
    tagged = sum(1 for ln in out if ln.strip().startswith("method: python"))
    print(f"updated {REG}; python-tagged items: {tagged}")


if __name__ == "__main__":
    main()
