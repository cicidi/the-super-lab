"""TST-P: the design carries a sub-problem ownership table with traceable evidence."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HLD = ROOT / "docs/features/spec-driven-development/design/spec-driven-development-design.md"

SECTION = "子问题归属"
ALLOWED = {"AI 查", "人决定", "AI 查完人决定"}


def table_rows(text: str) -> list[list[str]]:
    """Rows of the first markdown table after the ownership heading."""
    idx = text.find(SECTION)
    assert idx != -1, f"{HLD.name} has no `{SECTION}` section (PIPE-L)"
    rows = []
    for line in text[idx:].splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        rows.append(cells)
    return rows[1:]  # drop header


def test_ownership_table_present_and_valid():
    rows = table_rows(HLD.read_text(encoding="utf-8"))
    assert rows, "ownership table has no data rows"
    for cells in rows:
        assert len(cells) == 3, f"row needs 子问题 / 归属 / 依据: {cells}"
        problem, owner, evidence = cells
        assert problem, "empty sub-problem"
        assert owner in ALLOWED, f"owner must be one of {sorted(ALLOWED)}, got {owner!r}"
        assert re.search(r"raw/|https?://|ARD-[A-Z]+", evidence), (
            f"evidence not traceable for {problem!r}: {evidence!r}"
        )
