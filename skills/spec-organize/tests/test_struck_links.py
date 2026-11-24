"""struck_ard_link: body links to struck ARDs are reported outside the decision-history."""

from checks.struck_links import check_struck_links, struck_ids

DH = """---
type: decision-history
---
# DH

## Decision Log

| ID | Date | Decision |
|----|------|----------|
| ARD-B | 2026-11-02 | live → see [ARD-A](#ard-a) |
| ~~ARD-A~~ | 2026-11-01 | ~~old~~ → [ARD-B](#ard-b) |

## Change Log

| Date | Change |
|------|--------|
| 2026-11-02 | struck [ARD-A](#ard-a) |
"""

PRD = """# PRD

Body cites [ARD-A](../decision-history/f-decision-history.md#ard-a) and
[ARD-B](../decision-history/f-decision-history.md#ard-b); a local [x](#ard-a).

## Change Log

| Date | Change |
|------|--------|
| 2026-11-02 | dropped [ARD-A](../decision-history/f-decision-history.md#ard-a) |
"""


def _tree(tmp_path):
    (tmp_path / "decision-history").mkdir()
    (tmp_path / "prd").mkdir()
    (tmp_path / "raw").mkdir()
    (tmp_path / "decision-history/f-decision-history.md").write_text(DH, encoding="utf-8")
    (tmp_path / "prd/f-prd.md").write_text(PRD, encoding="utf-8")
    (tmp_path / "raw/notes.md").write_text(PRD, encoding="utf-8")
    return tmp_path


def test_struck_ids_reads_decision_log_only():
    assert struck_ids(DH) == {"ard-a"}


def test_body_link_to_struck_ard_is_reported(tmp_path):
    findings = check_struck_links(_tree(tmp_path))
    assert [(f.check, f.path.rsplit("/", 1)[-1]) for f in findings] == [("struck_ard_link", "f-prd.md:3")]
    assert "ARD-A" in findings[0].message


def test_live_ard_link_is_clean(tmp_path):
    root = _tree(tmp_path)
    (root / "prd/f-prd.md").write_text(
        "[ARD-B](../decision-history/f-decision-history.md#ard-b)\n", encoding="utf-8"
    )
    assert check_struck_links(root) == []
