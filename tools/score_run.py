#!/usr/bin/env python3
"""TST-E: score one generated gold run (a feature spec) on the applicable rules.

  python3 tools/score_run.py skills/spec-organize/tests/runs/<id>/gold/run1

Score 1 counts the mechanical MUST checks that apply to a standalone feature
spec (frontmatter, sections, change log, decision log, ids, size). Repo-level
checks (INDEX, registry provenance, publish nav) do not apply to a run.

Score 2 uses the annotation subset that a run can satisfy, over the same
formula: (good hits - bad violations) * 10 / applicable annotations.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "skills/spec-organize/tests"))

from checks.change_log import check_change_log  # noqa: E402
from checks.decision_log import check_decision_log  # noqa: E402
from checks.frontmatter import check_frontmatter  # noqa: E402
from checks.ids import check_ids  # noqa: E402
from checks.sections import check_sections  # noqa: E402
from checks.size import check_size  # noqa: E402
from score_eval import PREDICATES  # noqa: E402

CHECKS = {
    "frontmatter": check_frontmatter,
    "sections": check_sections,
    "change_log": check_change_log,
    "decision_log": check_decision_log,
    "ids": check_ids,
    "size": check_size,
}

APPLICABLE_GOOD = {
    "GOOD-A": "letter_ids",
    "GOOD-B": "prd_anchor",
    "GOOD-C": "five_types",
    "GOOD-D": "change_log_last",
    "GOOD-E": "ownership",
}
APPLICABLE_BAD = {
    "BAD-B": "no_size_overflow",
    "BAD-D": "dh_newest_first",
}


def score_run(run: Path) -> tuple[int, int, float, dict[str, int], dict[str, bool]]:
    """Return (passed, total, score2, findings, annotation_hits) for one run."""
    docs = sorted(p for p in run.rglob("*.md") if not p.name.startswith("._"))
    findings: dict[str, int] = {name: 0 for name in CHECKS}
    for doc in docs:
        for name, fn in CHECKS.items():
            findings[name] += len(fn(doc))
    passed = sum(1 for n in CHECKS if findings[n] == 0)
    total = len(APPLICABLE_GOOD) + len(APPLICABLE_BAD)
    plus = minus = 0
    hits: dict[str, bool] = {}
    for ident, check in APPLICABLE_GOOD.items():
        hits[ident] = PREDICATES[check](run)
        plus += 1 if hits[ident] else 0
    for ident, check in APPLICABLE_BAD.items():
        hits[ident] = PREDICATES[check](run)
        minus += 0 if hits[ident] else 1
    return passed, len(CHECKS), (plus - minus) * 10 / total, findings, hits


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: score_run.py <run-dir>")
    run = Path(sys.argv[1])
    if not run.is_absolute():
        run = ROOT / run
    if not any(not p.name.startswith("._") for p in run.rglob("*.md")):
        sys.exit(f"no markdown under {run}")

    passed, total, score, findings, hits = score_run(run)
    print("# score 1 — applicable mechanical MUSTs")
    for name, count in findings.items():
        print(f"{'PASS' if count == 0 else 'FAIL'}\t{name}\t{count} finding(s)")
    print(f"\nscore1 = {passed}/{total}  gate={'PASS' if passed == total else 'FAIL'}")

    print("\n# score 2 — annotations applicable to a run")
    for ident in APPLICABLE_GOOD:
        print(f"{'+' if hits[ident] else ' '}\t{ident}\t{APPLICABLE_GOOD[ident]}")
    for ident in APPLICABLE_BAD:
        print(f"{' ' if hits[ident] else '-'}\t{ident}\t{APPLICABLE_BAD[ident]}")
    cap = 10 * len(APPLICABLE_GOOD) / (len(APPLICABLE_GOOD) + len(APPLICABLE_BAD))
    print(f"\nscore2 = {score:.1f}/10  gate={'PASS' if score >= 6 else 'FAIL'} (min 6.0, max {cap:.1f})")
    sys.exit(0 if passed == total and score >= 6 else 1)


if __name__ == "__main__":
    main()
