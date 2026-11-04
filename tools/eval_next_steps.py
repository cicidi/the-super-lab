#!/usr/bin/env python3
"""Print TST-C+ next steps after eval_preflight (no model calls)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "tools/eval_preflight.py"

STEPS = """
Runbook: skills/spec-organize/tests/gold/v1/TST-C-RUNBOOK.md

TST-C+ checklist (configure skills/spec-organize/tests/eval.yaml first):
  1. Set judge.model and three gold.models for parallel iPhone runs.
  2. Run spec-organize with requirement.md + context.md; grill.skills: [].
  3. Write outputs under gold/v1/runs/<model>/ + interview.md (see runs/_template/).
  4. TST-D: distill exemplar/ + extend annotations.yaml; bump gold.version if needed.
  5. Score with must_registry (python) + judge (llm); report to tests/reports/.
Mechanical gate (always): ./tools/run_sdd_mechanical.sh
"""


def main() -> None:
    proc = subprocess.run([sys.executable, str(PREFLIGHT)], cwd=ROOT)
    if proc.returncode != 0:
        sys.exit(proc.returncode)
    print(STEPS.strip())
    print("ok: preflight passed; complete eval.yaml before TST-C")


if __name__ == "__main__":
    main()
