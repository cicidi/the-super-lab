#!/usr/bin/env python3
"""Every page of the one site is reachable from docs/book/html/index.html (ARD-BG)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs/book/html"
HREF = re.compile(r'href="([^"#:?]+\.html)(?:#[^"]*)?"')


def unreachable(site: Path = SITE) -> list[Path]:
    pages = {p.resolve() for p in site.rglob("*.html")}
    seen: set[Path] = set()
    stack = [(site / "index.html").resolve()]
    while stack:
        page = stack.pop()
        if page in seen or page not in pages:
            continue
        seen.add(page)
        stack += [(page.parent / h).resolve() for h in HREF.findall(page.read_text(encoding="utf-8"))]
    return sorted(pages - seen)


def main() -> None:
    if not (SITE / "index.html").is_file():
        sys.exit(f"missing {SITE / 'index.html'}")
    orphans = unreachable()
    for p in orphans:
        print(f"not reachable from index.html: {p.relative_to(ROOT)}", file=sys.stderr)
    if orphans:
        sys.exit(1)
    print(f"ok: every page reachable from {SITE.relative_to(ROOT)}/index.html")


if __name__ == "__main__":
    main()
