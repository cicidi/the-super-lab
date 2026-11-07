"""TST-R: the human-readable reader is not older than its source markdown."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SDD = ROOT / "docs/features/spec-driven-development"
READER = SDD / "spec-driven-development-reader.html"


def test_reader_is_not_stale():
    assert READER.exists(), f"missing {READER}"
    sources = [
        p
        for p in SDD.rglob("*.md")
        if not p.name.startswith("._")
        and "__pycache__" not in p.parts
        and "raw" not in p.parts
    ]
    assert sources, "no source markdown found"
    newest = max(p.stat().st_mtime for p in sources)
    assert READER.stat().st_mtime >= newest, (
        "reader is older than its sources; run python3 tools/build_sdd_reader.py"
    )
