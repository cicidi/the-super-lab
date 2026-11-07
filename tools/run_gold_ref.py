#!/usr/bin/env python3
"""Run per-file spec checks on an external gold snapshot (ARD-BD / TST-T).

The private spec is not copied into this repo. A manifest names the source
checkout and the commits. If the source path is not on this machine, exit 0.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "skills/spec-organize/tests"


def _runners():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "run_spec_checks", ROOT / "tools" / "run_spec_checks.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.run_file


def _manifest(slug: str) -> dict:
    path = TESTS / "gold" / "refs" / slug / "manifest.yaml"
    if not path.is_file():
        print(f"missing manifest: {path}", file=sys.stderr)
        sys.exit(1)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else "smb-balance"
    data = _manifest(slug)
    source = Path(str(data.get("source", ""))).expanduser()
    if not source.is_dir():
        print(f"skip TST-T: source not on this machine ({source})")
        return
    commit = str(data.get("gold_commit", "")).strip()
    if not commit:
        print("skip TST-T: manifest has no gold_commit")
        return
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "gold.tar"
        subprocess.run(
            ["git", "-C", str(source), "archive", "--format=tar", "-o", str(archive), commit],
            check=True,
        )
        tree = Path(tmp) / "tree"
        tree.mkdir()
        subprocess.run(["tar", "-xf", str(archive), "-C", str(tree)], check=True)
        findings = []
        run_file = _runners()
        for md in tree.rglob("*.md"):
            findings.extend(run_file(md, md.read_text(encoding="utf-8", errors="replace")))
        allowed = {str(x) for x in data.get("allow", [])}
        unexpected = [f for f in findings if f.check not in allowed]
        print(f"{slug} {commit}: {len(unexpected)} outside allow")
        for f in unexpected:
            print(f"{f.check}\t{f.path}\t{f.message}")
        if unexpected:
            sys.exit(1)


if __name__ == "__main__":
    main()
