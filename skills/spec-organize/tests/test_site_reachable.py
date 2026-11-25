"""ARD-BG: one site, one entry. An orphan page is reported."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from check_site_reachable import unreachable  # noqa: E402


def test_orphan_page_is_reported(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "index.html").write_text('<a href="a/p.html#x">p</a>', encoding="utf-8")
    (tmp_path / "a/p.html").write_text('<a href="../index.html">home</a>', encoding="utf-8")
    (tmp_path / "orphan.html").write_text("lost", encoding="utf-8")
    assert [p.name for p in unreachable(tmp_path)] == ["orphan.html"]


def test_committed_site_has_no_orphans():
    assert unreachable() == []
