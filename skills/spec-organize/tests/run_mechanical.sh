#!/usr/bin/env bash
# TST-B local gate: spec checks + unit tests (no pytest install required if pytest missing).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
python3 tools/run_spec_checks.py docs/features/spec-driven-development
python3 tools/run_neg_fixtures.py
python3 tools/run_pos_fixtures.py
python3 tools/must_registry_coverage.py
python3 tools/tst_a_anchor_check.py
python3 tools/test_gold_annotations.py
python3 tools/validate_sdd_reader.py
python3 skills/spec-review/tests/run_case_checks.py
export PYTHONPATH="$ROOT/skills/spec-organize/tests"
PYTEST=(python3 -m pytest)
if ! python3 -m pytest --version >/dev/null 2>&1; then
  if [[ -x "$ROOT/.venv/bin/pytest" ]]; then
    PYTEST=("$ROOT/.venv/bin/pytest")
  else
    echo "pytest required: python3 -m venv .venv && .venv/bin/pip install pytest" >&2
    exit 1
  fi
fi
"${PYTEST[@]}" skills/spec-organize/tests/test_checks.py -q
