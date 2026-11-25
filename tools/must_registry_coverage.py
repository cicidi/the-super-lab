#!/usr/bin/env python3
"""TST-A coverage: must_registry method/check vs implemented TST-B modules."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "skills/spec-organize/tests/must_registry.yaml"
CHECKS = ROOT / "skills/spec-organize/tests/checks"

# Helper checks (IMPL-Z): they back a rule only in part, check a NICE rule, or
# check tooling, so they are not a scorer of any MUST item. Each needs a reason.
HELPER = {
    "audience_authority": "NICE: audience field vs authority table",
    "counts": "NICE: counts stated in a tracker match its rows (ARD-BB)",
    "diagram_steps": "NICE: figure step count matches its section (ARD-CA)",
    "figure_tree": "orphan SVGs (figure not cited in its directory); the figure MUST is fact-match, judged by the LLM",
    "figures": "part of the figure MUST; the fact-match half needs the LLM judge",
    "impl_tasks": "part of MUST-K (done line, two-way edges); execution order and read-before-write need the LLM judge",
    "paired_html": "hand-maintained HTML matches its md (ARD-AK); the HTML freshness MUST is llm-scored, TST-R checks the reader",
    "registry_provenance": "tooling: registry items resolve to their source",
    "section_refs": "NICE: section references resolve",
    "struck_links": "part of the ARD-BM edits rule (llm-scored): body links to struck ARDs",
    "test_trace": "tooling: every parent PRD id appears in the test plan's Traceability table",
    "translation_banner": "part of the translation-copy MUST (llm-scored): the banner half; no_commit catches committed copies",
}

# Every module under checks/ except package and shared plumbing.
NOT_CHECKS = {"__init__", "runners"}
IMPLEMENTED = {
    p.stem for p in CHECKS.glob("*.py") if not p.name.startswith("._") and p.stem not in NOT_CHECKS
}


def check_names(raw: str) -> list[str]:
    """A registry `check:` may list several modules: `index_book,anchors`."""
    return [name.strip() for name in raw.split(",") if name.strip()]


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
        names = check_names(i.get("check", ""))
        if not names:
            bad_check.append(i["id"])
            continue
        for name in names:
            if name not in IMPLEMENTED:
                missing_mod.append(f"{i['id']}:{name}")
    print(f"items={len(items)} python={len(python)} llm={len(llm)}")
    if bad_check:
        print("python items missing check:", ", ".join(bad_check))
    if missing_mod:
        print("unknown check modules:", ", ".join(missing_mod))
    mapped = {name for i in python for name in check_names(i.get("check", ""))}
    unused = IMPLEMENTED - mapped - set(HELPER)
    stale = sorted(set(HELPER) & mapped)
    if stale:
        print("HELPER lists mapped modules:", ", ".join(stale))
    if unused:
        print("note: TST-B modules not yet mapped in registry:", ", ".join(sorted(unused)))
    sys.exit(1 if bad_check or missing_mod or stale else 0)


if __name__ == "__main__":
    main()
