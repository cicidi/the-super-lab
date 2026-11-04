"""Hard line caps by type (DSGN-B summary in SPEC-STANDARD)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from checks.frontmatter import _parse_frontmatter

CAPS: dict[str, int] = {
    "prd": 800,
    "design": 1000,
    "impl-plan": 1000,
    "test-plan": 800,
    "decision-history": 1000,
    "how-to": 600,
}


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def check_size(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm:
        return []
    t = fm.get("type", "")
    cap = CAPS.get(t)
    if cap is None:
        return []
    lines = len(raw.splitlines())
    if lines > cap:
        return [
            Finding(
                "size",
                str(path),
                f"{lines} lines exceeds hard cap {cap} for type `{t}`",
            )
        ]
    return []
