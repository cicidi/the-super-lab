"""Markdown anchor targets must exist (ARD-AP)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding

_FENCE = re.compile(r"```.*?```", re.S)
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_H = re.compile(r"^#{1,6}\s+(.+)$", re.M)
_AID = re.compile(r'<a\s+id="([^"]+)"', re.I)


def _slug(title: str) -> str:
    s = title.strip().lower().replace(" — ", "--").replace(" – ", "--")
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s


def _ids(text: str) -> set[str]:
    found = {_slug(m.group(1)) for m in _H.finditer(text)}
    found.update(_AID.findall(text))
    return found


def check_anchors(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    body = _FENCE.sub("", raw)
    findings: list[Finding] = []
    own = _ids(raw)
    cache: dict[Path, set[str]] = {path: own}
    for m in _LINK.finditer(body):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:")) or "#" not in target:
            continue
        file_part, _, frag = target.partition("#")
        if not frag or "…" in frag or "..." in frag:
            continue
        dest = path if not file_part else (path.parent / file_part).resolve()
        if dest.suffix != ".md":
            continue
        if not dest.is_file():
            findings.append(Finding("anchors", str(path), f"missing anchor file: {file_part}"))
            continue
        if dest not in cache:
            cache[dest] = _ids(dest.read_text(encoding="utf-8", errors="replace"))
        if frag not in cache[dest]:
            findings.append(Finding("anchors", str(path), f"dead anchor: {frag}"))
    return findings
