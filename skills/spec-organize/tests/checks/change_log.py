"""Change Log must be last major section (DSGN-E)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from checks.frontmatter import _parse_frontmatter

HEADING = re.compile(r"^## +(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_change_log(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    if not _parse_frontmatter(raw):
        return []
    headings = HEADING.findall(raw)
    if not headings:
        return []
    if headings[-1].strip() != "Change Log":
        return [
            Finding(
                "change_log",
                str(path),
                f"last ## section must be Change Log, got `{headings[-1]}`",
            )
        ]
    return []
