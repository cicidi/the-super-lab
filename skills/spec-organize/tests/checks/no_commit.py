"""Forbidden committed paths (reference/, raw/*.md in tree scan)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_no_commit_tree(features_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not features_root.is_dir():
        return findings
    for path in features_root.rglob("*"):
        rel = path.as_posix()
        if path.name.startswith("._"):
            continue
        parts = path.parts
        if "reference" in parts:
            findings.append(
                Finding(
                    "no_commit",
                    rel,
                    "committed reference/ type is forbidden",
                )
            )
        if path.is_file() and path.suffix == ".md" and "/raw/" in rel:
            findings.append(
                Finding(
                    "no_commit",
                    rel,
                    "raw/ markdown must not be committed (link when promoted)",
                )
            )
    return findings
