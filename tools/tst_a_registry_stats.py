#!/usr/bin/env python3
"""Compare MUST registry size vs tst_a_scan candidate count (informational TST-A)."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "skills/spec-organize/tests/must_registry.yaml"
SCAN = ROOT / "tools/tst_a_scan_must_registry.py"

PAT = re.compile(r"(?i)(MUST NOT|MUST|禁止|不得)")


def _registry_count() -> int:
    return sum(1 for ln in REG.read_text(encoding="utf-8").splitlines() if ln.startswith("  - id:"))


def _scan_count() -> int:
    proc = subprocess.run(
        [sys.executable, str(SCAN)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return -1
    m = re.search(r"# candidates:\s*(\d+)", proc.stdout)
    return int(m.group(1)) if m else -1


def main() -> None:
    reg_n = _registry_count()
    scan_n = _scan_count()
    print(f"registry items: {reg_n}")
    print(f"scan candidates: {scan_n}")
    if scan_n >= 0 and reg_n < scan_n:
        print(f"note: registry may be missing up to {scan_n - reg_n} scan lines (manual curation expected)")
    print("ok")


if __name__ == "__main__":
    main()
