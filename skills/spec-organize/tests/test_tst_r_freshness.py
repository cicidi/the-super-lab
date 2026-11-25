"""TST-R: the committed reader equals a fresh build from its source markdown.

Content, not mtime: a fresh checkout gives every file the same arbitrary mtime.
Line 1 is the build marker (git sha) and is ignored.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

import build_sdd_reader  # noqa: E402


def _body(text: str) -> str:
    return text.split("\n", 1)[1]


def test_reader_matches_fresh_build():
    reader = build_sdd_reader.OUT
    assert reader.exists(), f"missing {reader}"
    committed = reader.read_text(encoding="utf-8")
    assert _body(committed) == _body(build_sdd_reader.render()), (
        "reader is stale; run python3 tools/build_sdd_reader.py"
    )
