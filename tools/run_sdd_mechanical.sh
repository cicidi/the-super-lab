#!/usr/bin/env bash
# Repo-root entry for the SDD mechanical gate (delegates to spec-organize harness).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec "$ROOT/skills/spec-organize/tests/run_mechanical.sh"
