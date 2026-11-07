"""TST-K: the eval report carries run identity, config, and both scores."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

REQUIRED = ["run_id", "branch", "commit", "gold version", "judge", "score 1", "score 2"]


def test_report_contains_required_fields(tmp_path):
    out = tmp_path / "report.html"
    run = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/render_eval_report.py"),
            "--out",
            str(out),
            "--run-id",
            "test-run",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    page = out.read_text(encoding="utf-8")
    for field in REQUIRED:
        assert field.lower() in page.lower(), f"report missing {field}"
    assert "test-run" in page
    assert re.search(r"score 1 — MUST.*?(\d+)/(\d+)", page, flags=re.S), "score 1 missing"


def test_report_run_rows_match_registry(tmp_path):
    out = tmp_path / "report.html"
    subprocess.run(
        [sys.executable, str(ROOT / "tools/render_eval_report.py"), "--out", str(out)],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    page = out.read_text(encoding="utf-8")
    assert page.count("<tr>") >= 28, "expected a row per MUST item"
