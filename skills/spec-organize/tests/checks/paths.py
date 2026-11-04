"""Path / filename checks for committed feature docs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

COMMITTED_TYPES = frozenset(
    {"prd", "design", "impl-plan", "test-plan", "decision-history", "how-to"}
)
ENTRY_RE = re.compile(
    r"^([a-z0-9]+(?:-[a-z0-9]+)*)-(prd|design|impl-plan|test-plan|decision-history|how-to)(?:-[a-z0-9-]+)?\.md$"
)


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_committed_path(path: Path, docs_root: Path | None = None) -> list[Finding]:
    """Validate a file under docs/features/ looks like a committed entry."""
    findings: list[Finding] = []
    rel = path.as_posix()
    parts = path.parts
    if "docs" not in parts or "features" not in parts:
        return findings
    try:
        fi = parts.index("features")
    except ValueError:
        return findings
    rest = parts[fi + 1 :]
    if len(rest) < 3:
        return findings
    # .../features/<f>/<type>/<file>.md or sub-feature .../features/<p>/features/<sub>/<type>/file
    type_dir = rest[-2] if len(rest) >= 2 else ""
    name = path.name
    if type_dir not in COMMITTED_TYPES:
        return findings
    if not ENTRY_RE.match(name):
        findings.append(
            Finding(
                "paths",
                rel,
                f"filename must match <f>-<type>… .md, got {name}",
            )
        )
    if "reference" in parts:
        findings.append(Finding("paths", rel, "committed reference/ type is forbidden"))
    return findings
