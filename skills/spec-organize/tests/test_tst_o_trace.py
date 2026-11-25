"""TST-O: every PRD requirement is cited inside a design rule clause.

A mention anywhere in a design (an Open Question, a Change Log row) is not a
trace. The id must appear in the body of a `DSGN-*` or `PIPE-*` clause, and the
two PRDs are matched per feature because both start at PRD-A.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SDD = ROOT / "docs/features/spec-driven-development"
DS = SDD / "features/document-standard"

PARENT_PRD = SDD / "prd/spec-driven-development-prd.md"
READER_PRD = DS / "prd/document-standard-prd-spec-reader-html.md"
PARENT_DESIGNS = [
    SDD / "design/spec-driven-development-design.md",
    SDD / "design/spec-driven-development-design-skill-contracts.md",
    SDD / "features/pipeline/design/pipeline-design.md",
    DS / "design/document-standard-design.md",
]
READER_DESIGNS = [DS / "design/document-standard-design-spec-reader-html.md"]
DEFERRED = {"PRD-G"}  # parent PRD-G is deferred (ARD-N)

DEFINED = re.compile(r"^(?:\*\*|\| |- \*\*)(PRD-[A-Z]+)\b", re.M)
PRD_ID = re.compile(r"\bPRD-[A-Z]+\b")
CLAUSE = re.compile(r"^(#{2,4}) .*?\b(?:DSGN|PIPE)-[A-Z]")
HEADING = re.compile(r"^(#{1,4}) ")


def defined_ids(prd: Path) -> set[str]:
    return set(DEFINED.findall(prd.read_text(encoding="utf-8")))


def clause_citations(design: Path) -> set[str]:
    """PRD ids cited in the body of DSGN-*/PIPE-* clauses (and their sub-clauses)."""
    cited: set[str] = set()
    depth = 0  # heading level of the open clause; 0 = outside any clause
    for line in design.read_text(encoding="utf-8").splitlines():
        head = HEADING.match(line)
        if head:
            level = len(head.group(1))
            clause = CLAUSE.match(line)
            if clause:
                depth = depth if depth and level > depth else level
            elif depth and level <= depth:
                depth = 0
            continue
        if depth:
            cited |= set(PRD_ID.findall(line))
    return cited


def missing(prd: Path, designs: list[Path], skip: set[str] = frozenset()) -> list[str]:
    cited: set[str] = set()
    for d in designs:
        cited |= clause_citations(d)
    return sorted(defined_ids(prd) - cited - skip)


def test_parent_prd_traced_to_design_clauses():
    assert defined_ids(PARENT_PRD), "parent PRD defines no PRD-* ids"
    gaps = missing(PARENT_PRD, PARENT_DESIGNS, DEFERRED)
    assert not gaps, f"parent PRD ids not cited in any DSGN/PIPE clause: {gaps}"


def test_reader_prd_traced_to_reader_design_clauses():
    assert defined_ids(READER_PRD), "reader PRD defines no PRD-* ids"
    gaps = missing(READER_PRD, READER_DESIGNS)
    assert not gaps, f"reader PRD ids not cited in any DSGN-N clause: {gaps}"


def test_mention_outside_a_clause_is_not_a_trace(tmp_path):
    prd = tmp_path / "prd.md"
    prd.write_text("**PRD-A**：x\n\n**PRD-B**：y\n", encoding="utf-8")
    design = tmp_path / "design.md"
    design.write_text(
        "## Design\n\n### DSGN-A — rule\n\ncovers PRD-A\n\n## Open Questions\n\nPRD-B later\n",
        encoding="utf-8",
    )
    assert missing(prd, [design]) == ["PRD-B"]
