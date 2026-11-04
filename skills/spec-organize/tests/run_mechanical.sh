#!/usr/bin/env bash
# TST-B local gate: spec checks + unit tests (no pytest install required if pytest missing).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
python3 tools/run_spec_checks.py docs/features/spec-driven-development
python3 tools/must_registry_coverage.py
export PYTHONPATH="$ROOT/skills/spec-organize/tests"
if python3 -m pytest --version >/dev/null 2>&1; then
  python3 -m pytest skills/spec-organize/tests/test_checks.py -q
else
  python3 -m unittest discover -s skills/spec-organize/tests -p 'test_*.py' -q
fi
