"""TST-B: mechanical checks vs fixtures."""

import subprocess
import sys
from pathlib import Path

from checks.change_log import check_change_log
from checks.collision import check_collision
from checks.no_commit import check_no_commit_tree
from checks.index_book import check_index_book
from checks.parent_complete import check_parent_complete
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


def test_pos_sdd_parent_five_docs():
    repo = ROOT.parents[2]
    p = repo / "docs/features/spec-driven-development"
    assert not check_parent_complete(p)


def test_pos_sdd_decision_history():
    repo = ROOT.parents[2]
    p = repo / "docs/features/spec-driven-development/decision-history/spec-driven-development-decision-history.md"
    assert not check_decision_log(p)
    assert not check_sections(p)


def test_neg_collision_fixture():
    root = FIX / "neg" / "collision-pair" / "docs" / "features"
    assert any(f.check == "collision" for f in check_collision(root))


def test_neg_bad_change_log():
    p = FIX / "neg" / "bad-change-log" / "docs" / "features" / "demo" / "prd" / "demo-prd.md"
    assert any(f.check == "change_log" for f in check_change_log(p))


def test_neg_bad_sections():
    p = (
        FIX
        / "neg"
        / "bad-sections"
        / "docs"
        / "features"
        / "demo"
        / "test-plan"
        / "demo-test-plan.md"
    )
    assert any(f.check == "sections" for f in check_sections(p))


def test_neg_bad_size():
    p = FIX / "neg" / "bad-size" / "docs" / "features" / "demo" / "prd" / "demo-prd.md"
    assert any(f.check == "size" for f in check_size(p))


def test_neg_bad_no_commit_reference():
    root = FIX / "neg" / "bad-no-commit" / "docs" / "features"
    assert any(f.check == "no_commit" and "reference" in f.message for f in check_no_commit_tree(root))


def test_neg_bad_parent_incomplete():
    root = FIX / "neg" / "bad-parent-incomplete" / "docs" / "features" / "incomplete-parent"
    assert any(f.check == "parent_complete" for f in check_parent_complete(root))


def test_neg_index_dead_link():
    repo = ROOT.parents[2]
    index = repo / "docs/INDEX.md"
    text = index.read_text(encoding="utf-8")
    bad = text.replace(
        "skill-factory-prd.md",
        "skill-factory-prd-missing.md",
        1,
    )
    index.write_text(bad, encoding="utf-8")
    try:
        assert any(
            f.check == "index_book" and "dead link" in f.message
            for f in check_index_book(repo)
        )
    finally:
        index.write_text(text, encoding="utf-8")


def test_pos_sdd_index_book():
    repo = ROOT.parents[2]
    assert not check_index_book(repo)


def test_pos_fixture_valid_test_plan():
    p = (
        FIX
        / "pos"
        / "valid-test-plan"
        / "docs"
        / "features"
        / "pos-demo"
        / "test-plan"
        / "pos-demo-test-plan.md"
    )
    assert not check_frontmatter(p)
    assert not check_sections(p)
    assert not check_change_log(p)
    assert not check_size(p)


def test_pos_pipeline_subfeature_design():
    repo = ROOT.parents[2]
    p = repo / "docs/features/spec-driven-development/features/pipeline/design/pipeline-design.md"
    assert not check_sections(p)


def test_gold_v1_context_variants_present():
    variants = ROOT / "gold/v1/context-variants"
    for name in ("budget-conflict", "missing-info", "midway-change", "family-disagree"):
        assert (variants / f"{name}.md").is_file()


def test_pos_fixture_valid_decision_history():
    p = (
        FIX
        / "pos"
        / "valid-decision-history"
        / "docs"
        / "features"
        / "pos-demo"
        / "decision-history"
        / "pos-demo-decision-history.md"
    )
    assert not check_decision_log(p)
    assert not check_change_log(p)


def test_run_spec_checks_help():
    repo = ROOT.parents[2]
    proc = subprocess.run(
        [sys.executable, str(repo / "tools/run_spec_checks.py"), "--help"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "usage:" in proc.stdout


def test_run_spec_checks_summary_flag():
    repo = ROOT.parents[2]
    proc = subprocess.run(
        [
            sys.executable,
            str(repo / "tools/run_spec_checks.py"),
            "--summary",
            "docs/features/spec-driven-development",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == "0"


def test_gold_v1_annotations_scaffold():
    ann = ROOT / "gold/v1/annotations.yaml"
    text = ann.read_text(encoding="utf-8")
    assert "version: v1" in text
    assert "GOOD-A" in text


def test_validate_sdd_reader_script():
    repo = ROOT.parents[2]
    script = repo / "tools/validate_sdd_reader.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_eval_preflight_script():
    repo = ROOT.parents[2]
    proc = subprocess.run(
        [sys.executable, str(repo / "tools/eval_preflight.py")],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_run_pos_fixtures_script():
    repo = ROOT.parents[2]
    proc = subprocess.run(
        [sys.executable, str(repo / "tools/run_pos_fixtures.py")],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_run_neg_fixtures_script():
    repo = ROOT.parents[2]
    proc = subprocess.run(
        [sys.executable, str(repo / "tools/run_neg_fixtures.py")],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_tst_a_registry_stats_script():
    repo = ROOT.parents[2]
    proc = subprocess.run(
        [sys.executable, str(repo / "tools/tst_a_registry_stats.py")],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "registry items:" in proc.stdout


def test_spec_review_case_checks_script():
    repo = ROOT.parents[2]
    script = repo / "skills/spec-review/tests/run_case_checks.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "all 4 cases ok" in proc.stdout


def test_tst_a_anchor_check_script():
    repo = ROOT.parents[2]
    script = repo / "tools/tst_a_anchor_check.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_must_registry_coverage_script():
    repo = ROOT.parents[2]
    script = repo / "tools/must_registry_coverage.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "python:" in proc.stdout
