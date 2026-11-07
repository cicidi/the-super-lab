"""Publishing nav must not point outside the committed tree (DSGN-D)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

MD_REF = re.compile(r"([A-Za-z0-9_./-]+\.md)")


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_publish_nav(repo_root: Path) -> list[Finding]:
    """MkDocs/Pages publishing is optional; with no config there is nothing to check."""
    config = repo_root / "mkdocs.yml"
    if not config.is_file():
        return []
    findings: list[Finding] = []
    for ref in MD_REF.findall(config.read_text(encoding="utf-8")):
        candidates = [repo_root / "docs" / ref, repo_root / ref]
        if not any(c.exists() for c in candidates):
            findings.append(Finding("publish_nav", "mkdocs.yml", f"nav points at missing doc: {ref}"))
    return findings
