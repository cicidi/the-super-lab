"""Body links to struck ARDs: a struck Decision Log row is no longer a live decision.

For every decision-history under a feature tree, collect the ARD ids whose
Decision Log row is struck (`| ~~ARD-X~~ |`), then report each markdown link
`...#ard-x` that resolves to that decision-history from any OTHER file in the
tree. Change Log table rows (in the final `## Change Log` section) are history
and are ignored.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from checks.frontmatter import Finding

_STRUCK_ROW = re.compile(r"^\|\s*~~(ARD-[A-Z]+)~~\s*\|")
_LINK = re.compile(r"\]\(([^)\s#]*)#(ard-[a-z]+)\)")


def _md_files(root: Path) -> list[Path]:
    return [
        p
        for p in sorted(root.rglob("*.md"))
        if not p.name.startswith("._") and "raw" not in p.relative_to(root).parts
    ]


def struck_ids(text: str) -> set[str]:
    """ARD ids whose row in the `## Decision Log` section is struck through."""
    m = re.search(r"(?ms)^## Decision Log\s*$(.*?)(?=^## |\Z)", text)
    if not m:
        return set()
    return {r.group(1).lower() for line in m.group(1).splitlines() if (r := _STRUCK_ROW.match(line.strip()))}


def _change_log_start(lines: list[str]) -> int:
    """Index of the last `## Change Log` heading, or len(lines) when absent."""
    for i in range(len(lines) - 1, -1, -1):
        if re.match(r"^##\s+Change Log\s*$", lines[i]):
            return i
    return len(lines)


def check_struck_links(root: Path) -> list[Finding]:
    files = _md_files(root)
    struck: dict[str, set[str]] = {}
    for p in files:
        if p.parent.name == "decision-history":
            ids = struck_ids(p.read_text(encoding="utf-8", errors="replace"))
            if ids:
                struck[os.path.normpath(p.resolve())] = ids
    if not struck:
        return []
    findings: list[Finding] = []
    for p in files:
        here = os.path.normpath(p.resolve())
        if here in struck:
            continue
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        cl = _change_log_start(lines)
        for n, line in enumerate(lines, 1):
            if n - 1 > cl and line.lstrip().startswith("|"):
                continue
            for m in _LINK.finditer(line):
                if not m.group(1):
                    continue
                dest = os.path.normpath((p.parent / m.group(1)).resolve())
                if m.group(2) in struck.get(dest, ()):
                    findings.append(
                        Finding(
                            "struck_ard_link",
                            f"{p}:{n}",
                            f"links to struck {m.group(2).upper()} in {Path(dest).name}",
                        )
                    )
    return findings
