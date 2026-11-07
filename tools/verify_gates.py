#!/usr/bin/env python3
"""One command for every SDD gate: pytest, tree checks, registry coverage, eval scores.

Exit 0 only when all four pass. Used by the /loop verification cycle.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "skills/spec-organize/tests"


def run(name: str, cmd: list[str], cwd: Path) -> bool:
    print(f"\n### {name}: {' '.join(cmd)}", flush=True)
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    lines = (proc.stdout + proc.stderr).strip().splitlines()
    highlights = [line for line in lines if line.startswith(("score1", "score2"))]
    for line in (highlights or lines[-4:]):
        print(f"  {line}")
    ok = proc.returncode == 0
    print(f"  => {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> None:
    results = [
        run("pytest", [sys.executable, "-m", "pytest", "-q"], TESTS),
        run(
            "spec checks",
            [sys.executable, "tools/run_spec_checks.py", "docs/features/spec-driven-development"],
            ROOT,
        ),
        run("registry coverage", [sys.executable, "tools/must_registry_coverage.py"], ROOT),
        run("eval scores", [sys.executable, "tools/score_eval.py", "--min-score2", "6"], ROOT),
    ]
    print(f"\n{'ALL GATES PASS' if all(results) else 'GATE FAILURE'}")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
