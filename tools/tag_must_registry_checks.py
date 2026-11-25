#!/usr/bin/env python3
"""Assign method:python and check names to must_registry items where obvious."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "skills/spec-organize/tests/must_registry.yaml"

# Ordered: first match on the item's `text:` wins; no match -> llm.
# Match on the rule's own wording, never on its MUST-* id (ids move on rescan).
RULES: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"^\*\*文件名规则"), "python", "paths"),
    (re.compile(r"^\*\*行数（MUST"), "python", "size"),
    (re.compile(r"必须写进 `\.gitignore`|^- 不能提交的路径没有被提交"), "python", "no_commit"),
    # A `check` may list several modules; score_eval merges their findings.
    (re.compile(r"INDEX 没有孤立文档"), "python", "index_book,anchors"),
    (re.compile(r"孤立文档.*死链"), "python", "index_book"),
    (re.compile(r"INDEX 和 book 已经同步"), "python", "index_book,book,publish_nav"),
    (re.compile(r"^\*\*frontmatter（MUST"), "python", "frontmatter"),
    (re.compile(r"^\*\*必需章节（MUST"), "python", "sections"),
    (re.compile(r"^\*\*引用代码（MUST"), "python", "code_citation_base"),
    (re.compile(r"^- \*\*parent\*\*（`docs/features/spec-driven-development/`"), "python", "parent_complete"),
    (re.compile(r"^\*\*未决问题清单（MUST"), "python", "open_questions,resolved_refs"),
    (re.compile(r"^\*\*Decision Log（MUST"), "python", "decision_log"),
    (re.compile(r"^\*\*Change Log（MUST"), "python", "change_log"),
    (re.compile(r"^\*\*凡是要被引用的都要编号"), "python", "ids"),
    (re.compile(r"必须和已有的名字比一比|新名字已经检查过撞车"), "python", "collision"),
]


def _text(blob: str) -> str:
    for ln in blob.splitlines():
        if ln.strip().startswith("text:"):
            return ln.split(":", 1)[1].strip().strip("'\"")
    return ""


def _tag(item_id: str, text_blob: str) -> tuple[str, str]:
    text = _text(text_blob)
    for pat, method, check in RULES:
        if pat.search(text):
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
        item_id = ""
        for ln in item_lines:
            if ln.strip().startswith("- id:") or ln.strip().startswith("id:"):
                item_id = ln.split(":", 1)[1].strip()
                break
        if not item_id and item_lines[0].startswith("  - id:"):
            item_id = item_lines[0].split(":", 1)[1].strip()
        method, check = _tag(item_id, blob)
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
