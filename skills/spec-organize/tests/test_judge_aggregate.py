"""ARD-CJ: 5 judge runs, 4 must agree; non-pass items leave room for Claude's audit."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import judge_deepseek as j  # noqa: E402


def _runs(*verdicts):
    return [{"items": [{"id": "MUST-A", "verdict": v, "evidence": "e"}]} for v in verdicts]


def test_four_of_five_pass_is_pass():
    (row,) = j.aggregate(_runs("pass", "pass", "pass", "pass", "fail"))
    assert row["verdict"] == "pass" and "claude_audit" not in row


def test_three_of_five_is_disputed_and_needs_audit():
    (row,) = j.aggregate(_runs("pass", "pass", "pass", "fail", "fail"))
    assert row["verdict"] == "disputed" and row["claude_audit"] is None


def test_missing_vote_counts_as_fail():
    runs = _runs("pass", "pass", "pass", "pass") + [{"items": []}]
    (row,) = j.aggregate(runs)
    assert row["votes"].count("fail") == 1 and row["verdict"] == "pass"


def test_default_is_five_runs():
    assert j.RUNS == 5
