"""TST-B: every negative fixture fails its check; the positive fixture passes all."""

from pathlib import Path

from checks.change_log import check_change_log
from checks.frontmatter import check_frontmatter
from checks.ids import check_ids
from checks.index_book import check_index_book
from checks.no_commit import check_no_commit_tree
from checks.sections import check_sections
from checks.size import check_size

ROOT = Path(__file__).resolve().parent
FIX = ROOT / "fixtures"

NEG = [
    ("bad-sections", "sections", FIX / "neg/bad-sections/docs/features/demo/design/demo-design.md"),
    ("bad-change-log", "change_log", FIX / "neg/bad-change-log/docs/features/demo/prd/demo-prd.md"),
]


def test_neg_sections_and_change_log():
    file_checks = {"sections": check_sections, "change_log": check_change_log}
    for name, check, path in NEG:
        findings = file_checks[check](path)
        assert any(f.check == check for f in findings), f"{name} did not fail {check}"


def test_neg_index_orphan():
    root = FIX / "neg/bad-index"
    findings = check_index_book(root)
    assert any(f.check == "index_book" for f in findings)


def test_neg_index_dead_link():
    root = FIX / "neg/bad-index-dead-link"
    findings = check_index_book(root)
    assert any("dead link" in f.message for f in findings)


def test_neg_frontmatter_missing_state():
    path = FIX / "neg/bad-frontmatter-key/docs/features/demo/prd/demo-prd.md"
    findings = check_frontmatter(path)
    assert any("state" in f.message for f in findings)


def test_neg_reference_dir_is_not_committable():
    root = FIX / "neg/no-commit-reference/docs/features"
    findings = check_no_commit_tree(root)
    assert any(f.check == "no_commit" for f in findings)


def test_neg_size_overflow_by_type():
    text = "---\nfeature: demo\ntype: design\nstate: draft\n---\n\n## Change Log\n\n"
    text += "\n".join(f"line {i}" for i in range(1005))
    findings = check_size(Path("oversize-design.md"), text)
    assert any(f.check == "size" for f in findings)


def test_pos_clean_feature_passes_every_check():
    root = FIX / "pos/clean-feature"
    features = root / "docs/features"
    findings = check_index_book(root) + check_no_commit_tree(features)
    for path in (features / "demo").rglob("*.md"):
        findings += check_frontmatter(path)
        findings += check_sections(path)
        findings += check_change_log(path)
        findings += check_ids(path)
        findings += check_size(path)
    assert not findings, findings
