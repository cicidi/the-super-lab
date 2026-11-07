"""Unit tests for the repo-level gates added for MUST-B/J/K/AA."""

from pathlib import Path

from checks.book import check_book
from checks.publish_nav import check_publish_nav
from checks.registry_provenance import check_registry_provenance
from checks.test_trace import check_test_trace

ROOT = Path(__file__).resolve().parents[3]


def test_book_flags_dead_canonical_link(tmp_path):
    page = tmp_path / "docs/book"
    page.mkdir(parents=True)
    (page / "index.md").write_text("[x](../features/demo/prd/demo-prd.md)", encoding="utf-8")
    assert any(f.check == "book" for f in check_book(tmp_path))


def test_book_accepts_resolving_link(tmp_path):
    page = tmp_path / "docs/book"
    page.mkdir(parents=True)
    target = tmp_path / "docs/features/demo/prd"
    target.mkdir(parents=True)
    (target / "demo-prd.md").write_text("# Demo", encoding="utf-8")
    (page / "index.md").write_text("[x](../features/demo/prd/demo-prd.md)", encoding="utf-8")
    assert not check_book(tmp_path)


def test_publish_nav_is_vacuous_without_config(tmp_path):
    assert not check_publish_nav(tmp_path)


def test_publish_nav_flags_missing_doc(tmp_path):
    (tmp_path / "mkdocs.yml").write_text("nav:\n  - Home: missing.md\n", encoding="utf-8")
    assert any(f.check == "publish_nav" for f in check_publish_nav(tmp_path))


def test_test_trace_flags_uncovered_prd(tmp_path):
    feature = tmp_path / "docs/features/demo"
    (feature / "prd").mkdir(parents=True)
    (feature / "test-plan").mkdir(parents=True)
    (feature / "prd/demo-prd.md").write_text("**PRD-A** x\n**PRD-B** y", encoding="utf-8")
    (feature / "test-plan/demo-test-plan.md").write_text("PRD-A only", encoding="utf-8")
    findings = check_test_trace(feature)
    assert any("PRD-B" in f.message for f in findings)


def test_registry_provenance_is_clean_on_repo():
    assert not check_registry_provenance(ROOT)


def test_test_trace_is_clean_on_repo():
    assert not check_test_trace(ROOT / "docs/features/spec-driven-development")
