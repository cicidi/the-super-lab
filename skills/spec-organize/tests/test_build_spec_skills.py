"""TST: SDD skill stamps match parent PRD version."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools/build_spec_skills.py"


def test_spec_bundle_check():
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout

def test_upsert_metadata_is_idempotent_without_duplicate_keys():
    sys.path.insert(0, str(ROOT / "tools"))
    import build_spec_skills as b

    front = "name: x\nmetadata:\n  triggers:\n    - a"
    once = b.upsert_metadata(front, "1.0.0", "2026-01-01", "abc")
    twice = b.upsert_metadata(once.rstrip(), "1.0.0", "2026-01-02", "def")
    for key in ("spec_bundle_version", "spec_built_at", "spec_git_sha"):
        assert twice.count(f"  {key}:") == 1, twice
