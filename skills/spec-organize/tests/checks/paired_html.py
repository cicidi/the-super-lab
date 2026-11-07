"""Hand-maintained HTML must match its markdown source (ARD-AK)."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from checks.frontmatter import Finding

_PAIRED = re.compile(
    r'<meta\s+name="spec-paired"\s+content="hand-maintained"\s*/?>',
    re.I,
)
_SOURCE = re.compile(r'<meta\s+name="spec-source"\s+content="([^"]+)"\s*/?>', re.I)
_SHA = re.compile(
    r'<meta\s+name="spec-source-sha256"\s+content="([^"]+)"\s*/?>',
    re.I,
)
_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def check_paired_html(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    docs = root / "docs"
    if not docs.is_dir():
        return findings
    for html in docs.rglob("*.html"):
        text = html.read_text(encoding="utf-8", errors="replace")
        if not _PAIRED.search(text):
            if html.with_suffix(".md").is_file():
                findings.append(
                    Finding(
                        "paired_html_stale",
                        str(html.relative_to(root)),
                        "same-name html has no hand-maintained declaration",
                    )
                )
            continue
        rel = str(html.relative_to(root))
        src_m = _SOURCE.search(text)
        sha_m = _SHA.search(text)
        if not src_m or not sha_m:
            findings.append(
                Finding(
                    "paired_html_stale",
                    rel,
                    "hand-maintained HTML missing spec-source or spec-source-sha256",
                )
            )
            continue
        src = root / src_m.group(1)
        if not src.is_file():
            findings.append(
                Finding("paired_html_stale", rel, f"spec-source missing: {src_m.group(1)}")
            )
            continue
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if digest != sha_m.group(1).strip().lower():
            findings.append(
                Finding(
                    "paired_html_stale",
                    rel,
                    "spec-source-sha256 does not match the markdown",
                )
            )
            continue
        md_dates = _DATE.findall(_change_log(src.read_text(encoding="utf-8", errors="replace")))
        html_dates = set(_DATE.findall(text))
        missing = [d for d in md_dates if d not in html_dates]
        if missing:
            findings.append(
                Finding(
                    "paired_html_stale",
                    rel,
                    "hand-maintained changelog misses markdown dates: " + ", ".join(missing),
                )
            )
    return findings


def _change_log(md: str) -> str:
    m = re.search(r"(?ms)^## Change Log\s*(.*)\Z", md)
    return m.group(1) if m else ""
