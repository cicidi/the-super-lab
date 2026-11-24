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
# Part suffixes (ARD-G, ARD-BQ): an aspect noun for prd/design/test-plan/how-to,
# a zero-padded sequence plus phase/period name for impl-plan/decision-history.
NOUN_PART = r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*"
SEQ_PART = r"[0-9]{2,}-[a-z0-9]+(?:-[a-z0-9]+)*"
SEQ_TYPES = frozenset({"impl-plan", "decision-history"})


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def _declares_type(path: Path) -> bool:
    """True when frontmatter claims a committed type, i.e. the file is a document.

    A .md without such frontmatter in a type folder is a supporting file (DSGN-B).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    block = text[3:end] if end != -1 else ""
    m = re.search(r"^type:\s*['\"]?([a-z-]+)", block, re.MULTILINE)
    return bool(m and m.group(1) in COMMITTED_TYPES)


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
    feature_dir = rest[-3]
    prefix = re.escape(f"{feature_dir}-{type_dir}")
    part = SEQ_PART if type_dir in SEQ_TYPES else NOUN_PART
    if not re.match(rf"^{prefix}(?:-{part})?\.md$", name) and (
        ENTRY_RE.match(name) or _declares_type(path)
    ):
        shape = "NN-<name>" if type_dir in SEQ_TYPES else "<noun>"
        findings.append(
            Finding(
                "paths",
                rel,
                f"filename must be {feature_dir}-{type_dir}.md or "
                f"{feature_dir}-{type_dir}-{shape}.md, got {name}",
            )
        )
    if "reference" in parts:
        findings.append(Finding("paths", rel, "committed reference/ type is forbidden"))
    return findings
