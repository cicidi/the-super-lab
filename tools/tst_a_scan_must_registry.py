#!/usr/bin/env python3
"""TST-A helper: scan SDD design sources for MUST/forbidden lines → must_registry draft."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "docs/features/spec-driven-development/features/document-standard/design/document-standard-design.md",
    ROOT / "docs/features/spec-driven-development/features/pipeline/design/pipeline-design.md",
    ROOT / "docs/features/spec-driven-development/design/spec-driven-development-design.md",
    # Appended last so earlier MUST-* ids keep their letters (ids never change).
    ROOT / "docs/features/spec-driven-development/features/document-standard/design/document-standard-design-spec-reader-html.md",
]

# A rule line sits inside a numbered clause (### DSGN-X / ### PIPE-X) and either
# carries a "（MUST" marker or says 必须/不得/禁止. Lines that only mention the word
# MUST (overviews, rejected options, test pointers) are not rules.
CLAUSE = re.compile(r"^#{3,4} (?:DSGN|PIPE)-[A-Z]")
SECTION = re.compile(r"^## ")
MARK = re.compile(r"[（(]MUST")
MODAL = re.compile(r"必须|不得|禁止")
NEGATED = re.compile(r"不是[^。]*必须")  # "不是 SDD 必须安装的" is not a rule
# A bold label line ending in "：**" opens a bullet list; it is a rule list only
# when the label carries MUST ("**MUST，做不到就算失败：**", "**不允许（MUST NOT）：**").
LABEL = re.compile(r"^\*\*[^*]+：\*\*$")


def rule_lines(text: str):
    """Yield (line_no, line) for MUST rule lines in numbered clauses."""
    in_clause = in_gate = False
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if CLAUSE.match(line):
            in_clause, in_gate = True, False
            if MARK.search(line):  # "#### DSGN-N-B — 内容不丢（MUST）": the whole clause is a rule
                yield i, line
            continue
        if SECTION.match(line):
            in_clause = in_gate = False
            continue
        if not in_clause or not stripped or stripped.startswith("|"):
            continue
        if LABEL.match(stripped):
            in_gate = "MUST" in stripped
            continue
        if NEGATED.search(line):
            continue
        if MARK.search(line) or MODAL.search(line) or (in_gate and stripped.startswith("- ")):
            yield i, line


def _letter(n: int) -> str:
    """MUST-A … MUST-Z, MUST-AA …"""
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(ord("A") + r) + s
    return s


def main() -> None:
    import sys

    write = "--write" in sys.argv
    items: list[dict] = []
    for path in SOURCES:
        if not path.exists():
            print(f"missing: {path}")
            continue
        rel = path.relative_to(ROOT).as_posix()
        for i, line in rule_lines(path.read_text(encoding="utf-8")):
            text = line.strip()[:500]
            print(f"{rel}:{i}: {text[:120]}")
            items.append(
                {
                    "id": f"MUST-{_letter(len(items))}",
                    "source": f"{rel}:{i}",
                    "text": text,
                    "method": "llm",
                    "check": "",
                }
            )
    print(f"\n# candidates: {len(items)}")
    if write and items:
        out = ROOT / "skills/spec-organize/tests/must_registry.yaml"
        lines = ["version: 1", "items:"]
        for it in items:
            lines.append(f"  - id: {it['id']}")
            lines.append(f"    source: {it['source']}")
            lines.append(f"    text: {it['text']!r}")
            lines.append(f"    method: {it['method']}")
            lines.append(f"    check: {it['check']!r}")
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
