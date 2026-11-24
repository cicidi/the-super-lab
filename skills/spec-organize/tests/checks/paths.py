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


def _declares_type(text: str) -> bool:
    """True when frontmatter claims a committed type, i.e. the file is a document."""
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    block = text[3:end] if end != -1 else ""
    m = re.search(r"^type:\s*['\"]?([a-z-]+)", block, re.MULTILINE)
    return bool(m and m.group(1) in COMMITTED_TYPES)


def _type_folder(path: Path) -> tuple[str, str] | None:
    """(feature_dir, type_dir) when path is docs/features/.../<f>/<type>/<file>.md."""
    parts = path.parts
    if "docs" not in parts or "features" not in parts:
        return None
    rest = parts[parts.index("features") + 1 :]
    if len(rest) < 3 or rest[-2] not in COMMITTED_TYPES:
        return None
    return rest[-3], rest[-2]


def _canonical_name(name: str, feature_dir: str, type_dir: str) -> bool:
    prefix = re.escape(f"{feature_dir}-{type_dir}")
    part = SEQ_PART if type_dir in SEQ_TYPES else NOUN_PART
    return bool(re.match(rf"^{prefix}(?:-{part})?\.md$", name))


def supporting_type(path: Path, text: str | None = None) -> str | None:
    """Type folder of a supporting file (DSGN-B), else None.

    A supporting file is an .md in a type folder whose frontmatter declares no
    committed `type:`. A file with the canonical document name stays a document,
    so a missing frontmatter block on it is still reported.
    """
    loc = _type_folder(path)
    if loc is None or _canonical_name(path.name, *loc):
        return None
    if text is None:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return None
    return None if _declares_type(text) else loc[1]


def is_supporting_file(path: Path, text: str | None = None) -> bool:
    return supporting_type(path, text) is not None


def check_committed_path(path: Path, docs_root: Path | None = None) -> list[Finding]:
    """Validate a file under docs/features/ looks like a committed entry."""
    findings: list[Finding] = []
    rel = path.as_posix()
    parts = path.parts
    loc = _type_folder(path)
    if loc is None:
        return findings
    feature_dir, type_dir = loc
    name = path.name
    if not _canonical_name(name, feature_dir, type_dir) and not is_supporting_file(path):
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
