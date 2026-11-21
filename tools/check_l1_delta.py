#!/usr/bin/env python3
"""TST-X (IMPL-T): L1 content must not shrink between two git versions.

  python3 tools/check_l1_delta.py [--base REF] [--head REF] [--repo DIR] [path]

base defaults to HEAD~1; head defaults to the working tree; path defaults to docs/features/.
Fails when a numbered heading (PRD/DSGN/PIPE/IMPL/TST/ARD/QUES) disappears from a doc, or a
doc has fewer MUST sentences — unless a line added to a decision-history between base and
head names that ID or that doc (MUST-D: dropping L1 to pass a check is a defect).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID_HEAD = re.compile(r"^#{2,4}\s+((?:PRD|DSGN|PIPE|IMPL|TST|ARD|QUES)-[A-Z]+)\b", re.M)
MUST_LINE = re.compile(r"\bMUST\b|必须|禁止|不得")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def _keep(rel: str) -> bool:
    parts = Path(rel).parts
    return rel.endswith(".md") and "raw" not in parts and not Path(rel).name.startswith("._")


def docs_at(repo: Path, ref: str | None, path: str) -> dict[str, str]:
    if ref is None:
        base = repo / path
        files = [p.relative_to(repo).as_posix() for p in base.rglob("*.md")] if base.is_dir() else []
        return {f: (repo / f).read_text(encoding="utf-8") for f in files if _keep(f)}
    names = _git(repo, "ls-tree", "-r", "--name-only", ref, "--", path).splitlines()
    return {f: _git(repo, "show", f"{ref}:{f}") for f in names if _keep(f)}


def ids(text: str) -> set[str]:
    return set(ID_HEAD.findall(text))


def must_count(text: str) -> int:
    return sum(1 for line in FENCE.sub("", text).splitlines() if MUST_LINE.search(line))


def added_decision_lines(repo: Path, base: str, head: str | None, path: str) -> str:
    refs = [base] if head is None else [base, head]
    diff = _git(repo, "diff", *refs, "--", path)
    out, in_dh = [], False
    for line in diff.splitlines():
        if line.startswith("diff --git"):
            in_dh = "decision-history" in line
        elif in_dh and line.startswith("+") and not line.startswith("+++"):
            out.append(line[1:])
    if head is None:
        for rel in _git(repo, "ls-files", "--others", "--exclude-standard", "--", path).splitlines():
            if "decision-history" in rel and _keep(rel):
                out.append((repo / rel).read_text(encoding="utf-8"))
    return "\n".join(out)


def check(repo: Path, base: str, head: str | None, path: str) -> list[str]:
    old, new = docs_at(repo, base, path), docs_at(repo, head, path)
    excused = added_decision_lines(repo, base, head, path)
    findings = []
    for rel, text in sorted(old.items()):
        now = new.get(rel, "")
        stem = Path(rel).stem
        for ident in sorted(ids(text) - ids(now)):
            if ident not in excused and stem not in excused:
                findings.append(f"l1_delta\t{rel}\t{ident} heading removed without an ARD")
        before, after = must_count(text), must_count(now)
        if after < before and stem not in excused:
            findings.append(f"l1_delta\t{rel}\tMUST sentences {before} -> {after} without an ARD")
    return findings


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path", nargs="?", default="docs/features")
    ap.add_argument("--base", default="HEAD~1")
    ap.add_argument("--head", default=None)
    ap.add_argument("--repo", default=str(ROOT))
    args = ap.parse_args()
    findings = check(Path(args.repo), args.base, args.head, args.path)
    for f in findings:
        print(f)
    print(f"\n# findings: {len(findings)}")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
