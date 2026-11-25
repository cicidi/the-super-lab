"""TST-B: mechanical checks vs fixtures."""

import subprocess
import sys
from pathlib import Path

from checks.change_log import check_change_log
from checks.collision import check_collision
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


def test_must_registry_coverage_script():
    repo = ROOT.parents[2]
    r = subprocess.run(
        [sys.executable, str(repo / "tools/must_registry_coverage.py")],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def _doc(tmp_path, rel, doc_type=None):
    p = tmp_path / "docs" / "features" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    front = f"---\nfeature: pay\ntype: {doc_type}\nstate: draft\n---\n" if doc_type else ""
    p.write_text(front + "# Doc\n", encoding="utf-8")
    return p


def test_paths_wrong_feature_prefix_flagged(tmp_path):
    p = _doc(tmp_path, "pay/prd/shop-prd.md", "prd")
    assert any(f.check == "paths" for f in check_committed_path(p))


def test_paths_wrong_type_flagged(tmp_path):
    p = _doc(tmp_path, "pay/prd/pay-design.md", "prd")
    assert any(f.check == "paths" for f in check_committed_path(p))


def test_paths_numbered_noun_part_flagged(tmp_path):
    p = _doc(tmp_path, "pay/design/pay-design-01-auth.md", "design")
    assert any(f.check == "paths" for f in check_committed_path(p))


def test_paths_prd_aspect_part_ok(tmp_path):
    assert not check_committed_path(_doc(tmp_path, "pay/prd/pay-prd-refunds.md", "prd"))


def test_paths_decision_history_sequence_part_ok(tmp_path):
    p = _doc(tmp_path, "pay/decision-history/pay-decision-history-01-launch.md", "decision-history")
    assert not check_committed_path(p)


def _cite(tmp_path, rel, target):
    """Write a design doc in the same feature that links to `target` (DSGN-B)."""
    p = _doc(tmp_path, rel, "design")
    p.write_text(p.read_text(encoding="utf-8") + f"\nSee [notes]({target}).\n", encoding="utf-8")
    return p


def test_paths_supporting_file_ok(tmp_path):
    _cite(tmp_path, "pay/design/pay-design.md", "stripe-api-notes.md")
    assert not check_committed_path(_doc(tmp_path, "pay/design/stripe-api-notes.md"))


def test_paths_supporting_file_with_type_word_ok(tmp_path):
    # Negative control: the name looks like an entry (`...-design-guide.md`), but no
    # committed `type:` in frontmatter and a citing doc make it supporting (DSGN-B).
    _cite(tmp_path, "pay/design/pay-design.md", "./google-api-design-guide.md#intro")
    p = _doc(tmp_path, "pay/design/google-api-design-guide.md")
    assert not check_committed_path(p)


def test_run_file_supporting_file_clean(tmp_path):
    from checks.runners import run_file

    _cite(tmp_path, "pay/design/pay-design.md", "stripe-api-notes.md")
    p = _doc(tmp_path, "pay/design/stripe-api-notes.md")
    assert run_file(p, p.read_text(encoding="utf-8")) == []


def test_run_file_supporting_file_keeps_folder_size_cap(tmp_path):
    from checks.runners import run_file

    _cite(tmp_path, "pay/design/pay-design.md", "stripe-api-notes.md")
    p = tmp_path / "docs" / "features" / "pay" / "design" / "stripe-api-notes.md"
    p.write_text("line\n" * 1001, encoding="utf-8")
    assert [f.check for f in run_file(p, p.read_text(encoding="utf-8"))] == ["size"]


def test_uncited_stale_slug_without_frontmatter_is_document(tmp_path):
    # Regression: a wrongly named doc with no `type:` and no citing doc is not
    # supporting; it is flagged by paths and checked as a document (DSGN-B).
    from checks.paths import is_supporting_file
    from checks.runners import run_file

    _doc(tmp_path, "demo/prd/demo-prd.md", "prd")
    p = _doc(tmp_path, "demo/prd/olddemo-prd.md")
    assert not is_supporting_file(p)
    assert any(f.check == "paths" for f in check_committed_path(p))
    checks = {f.check for f in run_file(p, p.read_text(encoding="utf-8"))}
    assert {"paths", "frontmatter"} <= checks


def test_supporting_file_cited_from_other_feature_not_counted(tmp_path):
    _cite(tmp_path, "shop/design/shop-design.md", "../../pay/design/stripe-api-notes.md")
    p = _doc(tmp_path, "pay/design/stripe-api-notes.md")
    assert any(f.check == "paths" for f in check_committed_path(p))


def test_supporting_file_cited_only_from_raw_notes_flagged(tmp_path):
    # A citer under raw/ is a note, not a committed document (DSGN-B).
    _doc(tmp_path, "pay/design/pay-design.md", "design")
    notes = tmp_path / "docs" / "features" / "pay" / "raw" / "notes.md"
    notes.parent.mkdir(parents=True, exist_ok=True)
    notes.write_text("See [n](../design/stripe-api-notes.md).\n", encoding="utf-8")
    p = _doc(tmp_path, "pay/design/stripe-api-notes.md")
    assert any(f.check == "paths" for f in check_committed_path(p))


def test_supporting_file_cited_from_sub_feature_not_counted(tmp_path):
    _cite(tmp_path, "pay/features/refund/design/refund-design.md", "../../../design/stripe-api-notes.md")
    p = _doc(tmp_path, "pay/design/stripe-api-notes.md")
    assert any(f.check == "paths" for f in check_committed_path(p))


def test_neg_stale_slug_no_frontmatter():
    p = FIX / "neg" / "stale-slug-no-frontmatter" / "docs" / "features" / "demo" / "prd" / "olddemo-prd.md"
    assert any(f.check == "paths" for f in check_committed_path(p))


def test_canonical_name_without_frontmatter_is_document(tmp_path):
    from checks.runners import run_file

    p = _doc(tmp_path, "pay/design/pay-design.md")
    assert any(f.check == "frontmatter" for f in run_file(p, p.read_text(encoding="utf-8")))


def _impl_plan(tmp_path, body):
    p = tmp_path / "docs" / "features" / "pay" / "impl-plan" / "pay-impl-plan.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\nfeature: pay\ntype: impl-plan\nstate: draft\n---\n" + body, encoding="utf-8")
    return p


def _task(ident, deps, blocks):
    return f"\n## {ident} — t\n\n**依赖：** {deps}。**挡住：** {blocks}。\n\n完成标准：ok。\n"


def test_impl_edges_two_way_ok(tmp_path):
    from checks.impl_tasks import check_impl_tasks

    body = _task("IMPL-A", "无", "IMPL-B 的语义部分、IMPL-C") + _task("IMPL-B", "IMPL-A", "无")
    body += _task("IMPL-C", "无；报告部分还依赖 IMPL-A", "无")
    assert check_impl_tasks(_impl_plan(tmp_path, body)) == []


def test_impl_blocks_without_depends_flagged(tmp_path):
    from checks.impl_tasks import check_impl_tasks

    body = _task("IMPL-A", "无", "IMPL-B") + _task("IMPL-B", "无", "无")
    msgs = [f.message for f in check_impl_tasks(_impl_plan(tmp_path, body))]
    assert msgs == ["IMPL-A blocks IMPL-B, but IMPL-B 依赖 does not name IMPL-A"]


def test_impl_depends_without_blocks_flagged(tmp_path):
    from checks.impl_tasks import check_impl_tasks

    body = _task("IMPL-A", "无", "无") + _task("IMPL-B", "IMPL-A", "无")
    msgs = [f.message for f in check_impl_tasks(_impl_plan(tmp_path, body))]
    assert msgs == ["IMPL-B depends on IMPL-A, but IMPL-A 挡住 does not name IMPL-B"]


def _task_en(ident, deps, blocks):
    return f"\n## {ident} — t\n\nDepends on: {deps}. **Blocks:** {blocks}.\n\nDone when: ok.\n"


def test_impl_edges_english_labels(tmp_path):
    from checks.impl_tasks import check_impl_tasks

    ok = _task_en("IMPL-A", "none", "IMPL-B") + _task_en("IMPL-B", "IMPL-A", "none")
    assert check_impl_tasks(_impl_plan(tmp_path, ok)) == []
    bad = _task_en("IMPL-A", "none", "IMPL-B") + _task_en("IMPL-B", "none", "none")
    msgs = [f.message for f in check_impl_tasks(_impl_plan(tmp_path, bad))]
    assert msgs == ["IMPL-A blocks IMPL-B, but IMPL-B 依赖 does not name IMPL-A"]


def test_impl_id_followed_by_cjk_matches(tmp_path):
    from checks.impl_tasks import check_impl_tasks

    body = _task("IMPL-A", "无", "IMPL-B的语义部分") + _task("IMPL-B", "无", "无")
    msgs = [f.message for f in check_impl_tasks(_impl_plan(tmp_path, body))]
    assert msgs == ["IMPL-A blocks IMPL-B, but IMPL-B 依赖 does not name IMPL-A"]


def test_neg_impl_blocks_one_way():
    from checks.impl_tasks import check_impl_tasks

    p = FIX / "neg/impl-blocks-one-way/docs/features/demo/impl-plan/demo-impl-plan.md"
    assert any("blocks IMPL-B" in f.message for f in check_impl_tasks(p))


def test_impl_missing_depends_or_blocks_line_flagged(tmp_path):
    """MUST-K: every IMPL names its dependency and what it blocks (write 无 when none)."""
    from checks.impl_tasks import check_impl_tasks

    body = "## IMPL-A — x\n\n**Verify:** ok.\n\n## IMPL-B — y\n\n**依赖：** 无。\n\n**Verify:** ok.\n"
    msgs = [f.message for f in check_impl_tasks(_impl_plan(tmp_path, body))]
    assert "IMPL-A needs a 依赖/Depends on line (write 无 if none)" in msgs
    assert "IMPL-A needs a 挡住/Blocks line (write 无 if none)" in msgs
    assert "IMPL-B needs a 挡住/Blocks line (write 无 if none)" in msgs
