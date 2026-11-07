#!/usr/bin/env python3
"""TST-G: compare run_spec_checks finding counts to committed baselines."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINES = ROOT / "skills/spec-organize/tests/tst_g_baselines.txt"
CHECKS = ROOT / "tools/run_spec_checks.py"


def _load_baselines() -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    for line in BASELINES.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "\t" not in s:
            raise ValueError(f"bad baseline line: {line!r}")
        rel, count_s = s.split("\t", 1)
        rows.append((rel.strip(), int(count_s.strip())))
    return rows


def _finding_count(rel_path: str) -> int:
    target = ROOT / rel_path
    if not target.exists():
        print(f"missing tree: {rel_path}", file=sys.stderr)
        sys.exit(1)
    proc = subprocess.run(
        [sys.executable, str(CHECKS), "--summary", rel_path],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    # run_spec_checks exits 1 when findings > 0; --summary still prints count
    out = proc.stdout.strip()
    if not out.isdigit():
        print(proc.stdout + proc.stderr, file=sys.stderr)
        sys.exit(1)
    return int(out)


def main() -> None:
    if "--help" in sys.argv or "-h" in sys.argv:
        print("usage: tst_g_real_tree.py [--help]")
        print("  Compares run_spec_checks --summary to tst_g_baselines.txt")
        sys.exit(0)
    if not BASELINES.is_file():
        print(f"missing: {BASELINES}", file=sys.stderr)
        sys.exit(1)
    failures = 0
    for rel, expected in _load_baselines():
        got = _finding_count(rel)
        if got != expected:
            print(f"TST-G FAIL {rel}: expected {expected} findings, got {got}", file=sys.stderr)
            failures += 1
        else:
            print(f"ok TST-G {rel} ({got} findings)")
    if failures:
        sys.exit(1)
    print(f"ok: {len(_load_baselines())} TST-G baseline(s)")


if __name__ == "__main__":
    main()
