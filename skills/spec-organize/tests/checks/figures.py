"""Figure citations: SVG next to the citing md, named <stem>-fig-<slug>.svg, static (ARD-CA)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding

_FENCE = re.compile(r"^```.*?^```", re.M | re.S)
_CITE = re.compile(r"^!\[[^\]]*\]\(([^)\s]+\.svg)\)\s*$", re.M)
_UNSAFE = re.compile(r"<script\b|\son\w+\s*=", re.I)
_RECT = re.compile(r"<rect\b([^>]*)>", re.I)
_EDGE = re.compile(r"<(?:path|line|polyline)\b[^>]*marker-end=", re.I)
MAX_NODES = 9
MAX_EDGES = 12


def _attr(attrs: str, name: str) -> float:
    m = re.search(rf'\b{name}="([\d.]+)"', attrs)
    return float(m.group(1)) if m else 0.0


def figure_counts(svg: str) -> tuple[int, int]:
    nodes = sum(
        1
        for m in _RECT.finditer(svg)
        if _attr(m.group(1), "width") >= 60 and _attr(m.group(1), "height") >= 40
    )
    return nodes, len(_EDGE.findall(svg))


def check_figures(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    body = _FENCE.sub("", raw)
    rel = str(path)
    findings: list[Finding] = []
    for m in _CITE.finditer(body):
        src = m.group(1)
        target = path.parent / src
        if "/" in src or "\\" in src:
            findings.append(Finding("figures", rel, f"{src}: figure must sit next to the citing md"))
            continue
        if not re.fullmatch(rf"{re.escape(path.stem)}-fig-[a-z0-9]+(?:-[a-z0-9]+)*\.svg", src):
            findings.append(Finding("figures", rel, f"{src}: name must be {path.stem}-fig-<slug>.svg"))
        if not target.is_file():
            findings.append(Finding("figures", rel, f"{src}: file missing"))
            continue
        svg = target.read_text(encoding="utf-8")
        if _UNSAFE.search(svg):
            findings.append(Finding("figures", rel, f"{src}: script or event handler in SVG"))
        nodes, edges = figure_counts(svg)
        if nodes > MAX_NODES or edges > MAX_EDGES:
            findings.append(
                Finding(
                    "figures",
                    rel,
                    f"{src}: {nodes} nodes / {edges} edges (max {MAX_NODES} / {MAX_EDGES})",
                    level="nice",
                )
            )
    return findings
