"""Each IMPL task has a done line (ARD-AT)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding, _parse_frontmatter

_DONE = re.compile(r"Done when|Verify:|完成标准")


def check_impl_tasks(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm or fm.get("type") != "impl-plan":
        return []
    parts = re.split(r"(?m)^## (IMPL-[A-Z]+)\b", raw)
    findings: list[Finding] = []
    for i in range(1, len(parts), 2):
        ident, body = parts[i], parts[i + 1] if i + 1 < len(parts) else ""
        if not _DONE.search(body):
            findings.append(
                Finding("impl_tasks", str(path), f"{ident} needs Done when, Verify, or 完成标准")
            )
    return findings
