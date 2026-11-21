"""Tree-level figure checks: orphan SVGs (MUST) and diagram-design geometry (NICE)."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from checks.frontmatter import Finding

_CITE = re.compile(r"!\[[^\]]*\]\(([^)\s]+\.svg)\)")


def _verify_geometry_script() -> Path | None:
    home = os.environ.get("DIAGRAM_DESIGN_HOME")
    candidates = [Path(home) / "scripts/verify_geometry.py"] if home else []
    candidates.append(Path.home() / ".cursor/skills/diagram-design/scripts/verify_geometry.py")
    return next((p for p in candidates if p.is_file()), None)


def _figures(base: Path) -> list[Path]:
    return sorted(
        p
        for p in base.rglob("*-fig-*.svg")
        if not p.name.startswith("._") and "raw" not in p.parts
    )


def check_figure_tree(root: Path) -> list[Finding]:
    base = root / "docs/features" if (root / "docs/features").is_dir() else root
    findings: list[Finding] = []
    figures = _figures(base)
    for svg in figures:
        cited = any(
            svg.name in _CITE.findall(md.read_text(encoding="utf-8"))
            for md in svg.parent.glob("*.md")
            if not md.name.startswith("._")
        )
        if not cited:
            findings.append(Finding("figure_tree", str(svg), "figure not cited by any md in its directory"))
    script = _verify_geometry_script()
    if script is None:
        if figures:
            print("# skipped: figure geometry (diagram-design not installed)", file=sys.stderr)
        return findings
    for svg in figures:
        proc = subprocess.run(
            [sys.executable, str(script), str(svg)],
            capture_output=True,
            text=True,
            check=False,
        )
        for line in proc.stdout.splitlines():
            if line.startswith(svg.name + ":"):
                findings.append(Finding("figure_geometry", str(svg), line.split(":", 2)[-1].strip(), level="nice"))
    return findings
