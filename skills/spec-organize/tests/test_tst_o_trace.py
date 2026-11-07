"""TST-O: every parent PRD id is anchored in at least one design document."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SDD = ROOT / "docs/features/spec-driven-development"

PRD_ID = re.compile(r"PRD-[A-Z]+")


def md_files(base: Path) -> list[Path]:
    """Committed markdown only: skip AppleDouble `._*` and caches."""
    return [
        p
        for p in base.rglob("*.md")
        if not p.name.startswith("._") and "__pycache__" not in p.parts
    ]


def test_every_parent_prd_id_has_design_anchor():
    prd = "\n".join(p.read_text(encoding="utf-8") for p in md_files(SDD / "prd"))
    prd_ids = set(PRD_ID.findall(prd))
    assert prd_ids, "parent PRD has no PRD-* ids"

    designs = md_files(SDD / "design") + md_files(SDD / "features")
    designs = [p for p in designs if "design" in p.parts]
    design_text = "\n".join(p.read_text(encoding="utf-8") for p in designs)

    missing = sorted(prd_ids - set(PRD_ID.findall(design_text)))
    assert not missing, f"PRD ids with no design anchor: {missing}"
