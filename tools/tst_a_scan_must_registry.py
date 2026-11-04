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


def main() -> None:
    n = 0
    for path in SOURCES:
        if not path.exists():
            print(f"missing: {path}")
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if PAT.search(line) and line.strip() and not line.strip().startswith("|"):
                n += 1
                print(f"{path.relative_to(ROOT)}:{i}: {line.strip()[:120]}")
    print(f"\n# candidate lines: {n} (manual curate → must_registry.yaml)")


if __name__ == "__main__":
    main()
