#!/usr/bin/env python3
"""Unit tests for SDD site markdown → HTML rendering helpers."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_sdd_reader import inline_figures, md_to_html  # noqa: E402
from build_sdd_site import _badge_levels, _callout_label  # noqa: E402


class TestMdFigures(unittest.TestCase):
    def test_image_line_becomes_figure_placeholder(self) -> None:
        html = md_to_html("![整体结构](a-fig-x.svg)\n")
        self.assertIn('<figure class="fig">', html)
        self.assertIn('data-svg="a-fig-x.svg"', html)
        self.assertIn("<figcaption>整体结构</figcaption>", html)

    def test_anchor_line_passthrough(self) -> None:
        html = md_to_html('<a id="4-ai-文档"></a><a id="dsgn-a"></a>\n')
        self.assertIn('id="dsgn-a"', html)
        self.assertIn('id="4-ai-文档"', html)
        self.assertNotIn("&lt;a", html)
        unsafe = md_to_html('<a id="x" onclick="y"></a>\n')
        self.assertIn("&lt;a", unsafe)
        self.assertNotIn("onclick=\"y\">", unsafe)

    def test_inline_figures_inlines_and_scopes_ids(self) -> None:
        svg = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="t">
  <defs><marker id="arrow"/></defs>
  <title id="t">Loop</title>
  <line marker-end="url(#arrow)"/>
</svg>"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a-fig-x.svg").write_text(svg, encoding="utf-8")
            page = (
                '<figure class="fig">'
                '<div class="fig-svg" data-svg="a-fig-x.svg"></div>'
                "<figcaption>x</figcaption></figure>"
            )
            out = inline_figures(page, root / "a.md")
            self.assertIn('id="a-fig-x-arrow"', out)
            self.assertIn("url(#a-fig-x-arrow)", out)
            self.assertIn('aria-labelledby="a-fig-x-t"', out)
            self.assertNotIn("<?xml", out)
            self.assertNotIn("data-svg", out)

    def test_missing_svg_exits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = '<div class="fig-svg" data-svg="missing.svg"></div>'
            with self.assertRaises(SystemExit) as ctx:
                inline_figures(page, root / "a.md")
            self.assertIn("missing", str(ctx.exception))

    def test_svg_with_script_exits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.svg").write_text("<svg><script>alert(1)</script></svg>", encoding="utf-8")
            page = '<div class="fig-svg" data-svg="bad.svg"></div>'
            with self.assertRaises(SystemExit):
                inline_figures(page, root / "a.md")


class TestBuiltSite(unittest.TestCase):
    def test_built_site_figures(self) -> None:
        html_root = ROOT / "docs/book/html"
        features = ROOT / "docs/features"
        pages = [p for p in html_root.rglob("*.html") if not p.name.startswith("._")]
        for page in pages:
            text = page.read_text(encoding="utf-8")
            self.assertNotIn('data-svg="', text, page)
            self.assertNotIn("&lt;a id=", text, page)
        for svg in features.rglob("*-fig-*.svg"):
            if svg.name.startswith("._") or "raw" in svg.parts:
                continue
            doc = svg.parent / (svg.stem.split("-fig-")[0] + ".md")
            page = html_root / doc.relative_to(features).with_suffix(".html")
            if not page.is_file():
                page = html_root / "spec-driven-development/spec-driven-development-reader.html"
            count = page.read_text(encoding="utf-8").count(f'aria-labelledby="{svg.stem}-')
            self.assertEqual(count, 1, f"{svg.name} in {page}")


class TestDocTransforms(unittest.TestCase):
    def test_level_badges(self) -> None:
        body = "<p>这条是 MUST，<code>MUST</code> 不变；NICE；MUST NOT</p>"
        out = _badge_levels(body)
        self.assertEqual(out.count("lvl--must"), 2)
        self.assertEqual(out.count("lvl--nice"), 1)
        self.assertIn("<code>MUST</code>", out)

    def test_callout_labels(self) -> None:
        self.assertEqual(_callout_label("<p><strong>警告：</strong>x</p>"), "WARN")
        self.assertEqual(_callout_label("<p><strong>例子：</strong>x</p>"), "EXAMPLE")
        self.assertEqual(_callout_label("<p>UNKNOWN</p>"), "UNVERIFIED")
        self.assertEqual(_callout_label("<p>普通说明</p>"), "NOTE")
        self.assertEqual(_callout_label("<p><strong>保真：</strong>例如有风险</p>"), "NOTE")


if __name__ == "__main__":
    unittest.main()