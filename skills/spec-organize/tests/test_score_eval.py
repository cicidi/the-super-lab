"""TST-E/L gate: the eval itself must stay green (score 1 full, score 2 >= 6).

Verdicts come from `judgments/*-deepseek-flash.yaml`, written by
tools/judge_deepseek.py: 3 independent runs, 3/3 agreement required.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_eval_gates_pass():
    run = subprocess.run(
        [sys.executable, str(ROOT / "tools/score_eval.py"), "--min-score2", "6"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    match = re.search(r"score1 = (\d+)/(\d+)", run.stdout)
    assert match, run.stdout
    passed, total = int(match.group(1)), int(match.group(2))
    assert passed == total, f"score 1 not full: {passed}/{total}"
