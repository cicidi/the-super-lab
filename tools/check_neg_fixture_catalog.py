#!/usr/bin/env python3
"""Ensure fixtures/neg/* dirs match tools/run_neg_fixtures.py CASES list."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEG = ROOT / "skills/spec-organize/tests/fixtures/neg"
RUNNER = ROOT / "tools/run_neg_fixtures.py"


def main() -> None:
    if not NEG.is_dir():
        print(f"missing: {NEG}", file=sys.stderr)
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("run_neg_fixtures", RUNNER)
    if spec is None or spec.loader is None:
        print("failed to load run_neg_fixtures.py", file=sys.stderr)
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    in_runner = {name for name, _check, _fn in mod.CASES}
    on_disk = {p.name for p in NEG.iterdir() if p.is_dir()}
    extra_disk = on_disk - in_runner
    missing_disk = in_runner - on_disk
    if extra_disk or missing_disk:
        if extra_disk:
            print(f"neg dirs not in runner: {sorted(extra_disk)}", file=sys.stderr)
        if missing_disk:
            print(f"runner cases missing dirs: {sorted(missing_disk)}", file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(on_disk)} neg fixtures synced with runner")


if __name__ == "__main__":
    main()
