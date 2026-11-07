"""TST-Q: execution stops at a mock MCP call; the log is the evidence."""

import subprocess
import sys
from pathlib import Path

MOCK = Path(__file__).resolve().parent / "mock-mcp"


def test_mock_call_logs_and_has_no_real_effects():
    run = subprocess.run(
        [sys.executable, str(MOCK / "client.py")],
        cwd=MOCK,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0, run.stderr
    lines = [line for line in run.stdout.splitlines() if line.startswith("tool=")]
    assert len(lines) >= 2, run.stdout
    assert all("mock" in line for line in lines), lines


def test_mock_modules_do_not_reach_the_network():
    source = "\n".join(p.read_text(encoding="utf-8") for p in MOCK.glob("*.py"))
    for forbidden in ("import socket", "import requests", "import urllib", "import http"):
        assert forbidden not in source, f"mock must not use {forbidden}"
