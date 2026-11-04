#!/usr/bin/env python3
"""TST-K scaffold: template markers + optional local report HTML under reports/."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "tools/eval_report_template.html"
REPORTS = ROOT / "skills/spec-organize/tests/reports"
SCHEMA = REPORTS / "REPORT-SCHEMA.md"

MARKERS = (
    "run_id",
    "branch",
    "gold_version",
    "eval_config",
    "score1",
    "score2",
    "tst_f_variant",
    "checker_verdicts",
)


def _missing_markers(text: str) -> list[str]:
    return [m for m in MARKERS if f"eval-report:{m}=" not in text]


def main() -> None:
    if not SCHEMA.is_file():
        print(f"missing: {SCHEMA}", file=sys.stderr)
        sys.exit(1)
    if not TEMPLATE.is_file():
        print(f"missing: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    tpl = TEMPLATE.read_text(encoding="utf-8")
    miss = _missing_markers(tpl)
    if miss:
        for m in miss:
            print(f"template missing marker: eval-report:{m}=", file=sys.stderr)
        sys.exit(1)
    checked = 0
    if REPORTS.is_dir():
        for path in sorted(REPORTS.glob("*.html")):
            text = path.read_text(encoding="utf-8")
            bad = _missing_markers(text)
            if bad:
                print(f"{path.name}: missing markers {bad}", file=sys.stderr)
                sys.exit(1)
            checked += 1
    print(f"ok: eval report template ({checked} local report html checked)")


if __name__ == "__main__":
    main()
