"""TST-E: generated gold runs must clear score 1; score 2 is reported, not floored.

Selection: the newest bundle with at least 3 repetitions (the official TST-C
trial), falling back to the newest bundle. Assertions:

- score 1 (mechanical) is strict: every repetition must pass — a stochastic
  generator has no excuse for a structural violation.
- score 2 (quality) has no fixed floor (ARD-R): it only must not drop below
  the previous run of the same gold version, which this test does not compare.

Run artifacts are gitignored, so this test skips when no run exists.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
RUNS = Path(__file__).resolve().parent / "runs"
sys.path.insert(0, str(ROOT / "tools"))

from score_run import score_run  # noqa: E402


def repetitions(bundle: Path) -> list[Path]:
    return sorted(p for p in bundle.iterdir() if p.is_dir() and p.name.startswith("run"))


def select_bundle() -> Path | None:
    bundles = sorted(
        (p for p in RUNS.glob("*/gold") if p.is_dir()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for bundle in bundles:
        if len(repetitions(bundle)) >= 3:
            return bundle
    return bundles[0] if bundles else None


def test_latest_gold_run_scores():
    bundle = select_bundle()
    if bundle is None:
        pytest.skip("no gold run artifacts (runs/ is gitignored; run tools/run_gold_eval.py)")
    for run in repetitions(bundle):
        passed, total, score, findings, hits = score_run(run)
        assert passed == total, f"{bundle.parent.name}/{run.name}: score 1 {passed}/{total}; {findings}"
