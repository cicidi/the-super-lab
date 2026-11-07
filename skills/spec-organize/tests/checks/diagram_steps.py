"""A steps a–b sequence diagram has b−a+1 messages (ARD-BE)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding

_H = re.compile(r"(?m)^##\s+(.+)$")
_STEPS = re.compile(r"steps\s+(\d+)\s*[–-]\s*(\d+)", re.I)
_MSG = re.compile(r"(?m)^[ \t]*\S+.*?-{1,2}>>?\s*\S+")


def check_diagram_steps(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(?=##\s+)", raw)
    findings: list[Finding] = []
    for part in parts:
        hm = _H.search(part)
        if not hm:
            continue
        sm = _STEPS.search(hm.group(1))
        if not sm or "sequenceDiagram" not in part:
            continue
        block = re.search(r"```mermaid\s+sequenceDiagram.*?```", part, re.S)
        if not block:
            continue
        count = len(_MSG.findall(block.group(0)))
        expect = int(sm.group(2)) - int(sm.group(1)) + 1
        if count != expect:
            findings.append(
                Finding(
                    "diagram_steps",
                    str(path),
                    f"steps {sm.group(1)}-{sm.group(2)} has {count} messages, expected {expect}",
                )
            )
    return findings
