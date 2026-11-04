#!/usr/bin/env python3
"""Report must_registry.yaml coverage: python vs llm and checker name usage (TST-A helper)."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "skills/spec-organize/tests/must_registry.yaml"
CHECKS_DIR = ROOT / "skills/spec-organize/tests/checks"


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
        elif line.strip().startswith("method:"):
            cur["method"] = line.split(":", 1)[1].strip()
        elif line.strip().startswith("check:"):
            raw = line.split(":", 1)[1].strip()
            cur["check"] = raw.strip("'\"")
    if cur:
        items.append(cur)
    return items


def main() -> None:
    if not REG.is_file():
        print(f"missing: {REG}", file=sys.stderr)
        sys.exit(1)
    items = _load_items(REG.read_text(encoding="utf-8"))
    python_items = [i for i in items if i.get("method") == "python"]
    llm_items = [i for i in items if i.get("method") == "llm"]
    other = len(items) - len(python_items) - len(llm_items)

    check_names = sorted(
        p.stem
        for p in CHECKS_DIR.glob("*.py")
        if p.name != "__init__.py"
    )
    used = Counter(i.get("check", "") for i in python_items)
    missing_check = [i for i in python_items if not i.get("check")]
    unused_checks = [c for c in check_names if c not in used]

    print(f"registry: {REG.relative_to(ROOT)}")
    print(f"items: {len(items)}  python: {len(python_items)}  llm: {len(llm_items)}  other: {other}")
    if python_items:
        print("python checks:")
        for name, n in sorted(used.items()):
            label = name or "(empty)"
            print(f"  {label}: {n}")
    if missing_check:
        print("python items without check:", ", ".join(i["id"] for i in missing_check))
        sys.exit(1)
    if unused_checks:
        print("check modules not referenced in registry:", ", ".join(unused_checks))
    print("ok")


if __name__ == "__main__":
    main()
