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
]

PAT = re.compile(
    r"(?i)(MUST NOT|MUST|禁止|不得|never delete L1|Detect → Report → Ask)"
)


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
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if PAT.search(line) and line.strip() and not line.strip().startswith("|"):
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
