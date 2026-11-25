"""TST-E/L gate: the eval itself must stay green (score 1 full).

Score 2 has no fixed floor (ARD-R): a human compares it with the previous run of
the same gold version; run results are not committed, except `judgments/` (ARD-CJ).

Verdicts come from `judgments/*-deepseek-flash.yaml`, written by
tools/judge_deepseek.py: 5 independent runs, at least 4 agreeing (ARD-CJ).
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_eval_gates_pass():
    run = subprocess.run(
        [sys.executable, str(ROOT / "tools/score_eval.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    match = re.search(r"score1 = (\d+)/(\d+)", run.stdout)
    assert match, run.stdout
    passed, total = int(match.group(1)), int(match.group(2))
    assert passed == total, f"score 1 not full: {passed}/{total}"
