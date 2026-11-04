"""TST-B: mechanical checks vs fixtures."""

from pathlib import Path

from checks.change_log import check_change_log
from checks.decision_log import check_decision_log
from checks.frontmatter import check_frontmatter
from checks.ids import check_ids
from checks.paths import check_committed_path
from checks.sections import check_sections
from checks.size import check_size

ROOT = Path(__file__).resolve().parent
FIX = ROOT / "fixtures"


def test_neg_missing_frontmatter():
    p = FIX / "neg" / "missing-frontmatter" / "bad-entry.md"
    assert any(f.check == "frontmatter" for f in check_frontmatter(p))


def test_neg_bad_filename():
    p = (
        FIX
        / "neg"
        / "bad-filename"
        / "docs"
        / "features"
        / "demo"
        / "design"
        / "wrong-name.md"
    )
    assert any(f.check == "paths" for f in check_committed_path(p))


def test_neg_bad_ids():
    p = (
        FIX / "neg" / "bad-ids" / "docs" / "features" / "demo" / "prd" / "demo-prd.md"
    )
    assert any(f.check == "ids" for f in check_ids(p))


def test_neg_bad_decision_log():
    p = (
        FIX
        / "neg"
        / "bad-decision-log"
        / "docs"
        / "features"
        / "demo"
        / "decision-history"
        / "demo-decision-history.md"
    )
    assert any(f.check == "decision_log" for f in check_decision_log(p))


def test_pos_sdd_parent_design():
    repo = ROOT.parents[2]
    p = repo / "docs/features/spec-driven-development/design/spec-driven-development-design.md"
    assert not check_frontmatter(p)
    assert not check_committed_path(p)


def test_pos_sdd_test_plan_sections():
    repo = ROOT.parents[2]
    p = repo / "docs/features/spec-driven-development/test-plan/spec-driven-development-test-plan.md"
    assert not check_sections(p)


def test_pos_sdd_decision_history():
    repo = ROOT.parents[2]
    p = repo / "docs/features/spec-driven-development/decision-history/spec-driven-development-decision-history.md"
    assert not check_decision_log(p)
    assert not check_sections(p)
