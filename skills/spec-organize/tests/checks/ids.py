"""Letter-prefix ID rules (SPEC-STANDARD / DSGN-F)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Bare numeric or pseudo-prefix permanent IDs (sample patterns)
# Permanent requirement-style IDs with numeric suffix (not norm examples in prose).
BAD = re.compile(
    r"^\s*(?:[-*]|\d+\.)?\s*\*\*(?:PRD|DSGN|ARD|IMPL|TST)-\d+\*\*"
    r"|^\s*\|\s*(?:PRD|DSGN|ARD|IMPL|TST)-\d+\s*\|"
)


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_ids(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    if "docs/features/" not in path.as_posix():
        return []
    findings: list[Finding] = []
    for i, line in enumerate(raw.splitlines(), 1):
        m = BAD.search(line)
        if m:
            findings.append(
                Finding("ids", str(path), f"line {i}: forbidden ID pattern `{m.group(0)}`")
            )
    return findings
