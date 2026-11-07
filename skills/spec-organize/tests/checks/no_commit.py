"""Forbidden committed paths (reference/, raw/*.md in tree scan)."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def _tracked(root: Path) -> tuple[Path, set[str]] | None:
    """(repo toplevel, tracked paths) or None when this is not a git checkout."""
    try:
        top = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    if not top:
        return None
    return Path(top), {line for line in out.splitlines() if line}


def check_no_commit_tree(features_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not features_root.is_dir():
        return findings
    repo = features_root.parents[1] if len(features_root.parents) > 1 else features_root
    info = _tracked(repo)
    top, tracked = info if info else (None, None)
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
            # raw/ may exist locally; only *tracked* raw markdown is a violation.
            rel_to_top = path.relative_to(top).as_posix() if top else rel
            if tracked is None or rel_to_top in tracked:
                findings.append(
                    Finding(
                        "no_commit",
                        rel,
                        "raw/ markdown must not be committed (link when promoted)",
                    )
                )
    return findings
