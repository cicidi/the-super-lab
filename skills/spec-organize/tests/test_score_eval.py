"""TST-E/L gate: the eval itself must stay green (score 1 full).

Score 2 has no fixed floor (ARD-R): a human compares it with the previous run of
the same gold version; run results are not committed, except `judgments/` (ARD-CJ).

Verdicts come from `judgments/*-deepseek-flash.yaml`, written by
tools/judge_deepseek.py: 5 independent runs, at least 4 agreeing (ARD-CJ).
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TESTS_DIR = Path(__file__).resolve().parent


def test_eval_gates_pass():
    run = subprocess.run(
        [sys.executable, str(ROOT / "tools/score_eval.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    match = re.search(r"score1 = (\d+)/(\d+)", run.stdout)
    assert match, run.stdout
    passed, total = int(match.group(1)), int(match.group(2))
    assert passed == total, f"score 1 not full: {passed}/{total}"


# --- multi-check registry items: `check: a,b` merges findings from a and b ---

sys.path.insert(0, str(ROOT / "tools"))
import must_registry_coverage  # noqa: E402
import score_eval  # noqa: E402
import tag_must_registry_checks  # noqa: E402
from checks.frontmatter import Finding  # noqa: E402


def test_check_names_splits_comma_list():
    assert score_eval.check_names("index_book, anchors,,") == ["index_book", "anchors"]
    assert score_eval.check_names("") == []


def _score_one(monkeypatch, tmp_path, grouped):
    item = {"id": "MUST-X", "method": "python", "check": "index_book,anchors"}
    monkeypatch.setattr(score_eval, "collect", lambda feature: grouped)
    monkeypatch.setattr(score_eval, "parse_registry", lambda: [item])
    monkeypatch.setattr(score_eval, "JUDGED", tmp_path / "none.yaml")
    return score_eval.score1(tmp_path)


def test_score1_merges_listed_checks(monkeypatch, tmp_path):
    bad = {"anchors": [Finding("anchors", "a.md", "dead anchor: x")]}
    passed, total, lines = _score_one(monkeypatch, tmp_path, bad)
    assert (passed, total) == (0, 1)
    assert lines[0].startswith("FAIL\tMUST-X\tindex_book,anchors: 1 finding")


def test_score1_ignores_unlisted_checks(monkeypatch, tmp_path):
    other = {"book": [Finding("book", "b.md", "stale")]}
    passed, total, _ = _score_one(monkeypatch, tmp_path, other)
    assert (passed, total) == (1, 1)


def test_collect_runs_same_tree_checks_as_lint():
    lint = (ROOT / "tools/run_spec_checks.py").read_text(encoding="utf-8")
    score = (ROOT / "tools/score_eval.py").read_text(encoding="utf-8")
    calls = set(re.findall(r"\b(check_[a-z_]+)\(", lint))
    assert calls <= set(re.findall(r"\b(check_[a-z_]+)\(", score)), calls


def test_tagger_maps_index_rules_to_check_lists():
    tag = tag_must_registry_checks._tag
    reg = (TESTS_DIR / "must_registry.yaml").read_text(encoding="utf-8")
    texts = re.findall(r"^    text: (.+)$", reg, flags=re.M)
    orphan = next(t for t in texts if "INDEX 没有孤立文档" in t)
    synced = next(t for t in texts if "INDEX 和 book 已经同步" in t)
    assert tag("", f"text: {orphan}") == ("python", "index_book,anchors")
    assert tag("", f"text: {synced}") == ("python", "index_book,book,publish_nav")


def test_coverage_every_module_mapped_or_helper():
    implemented = must_registry_coverage.IMPLEMENTED
    assert {"figure_tree", "struck_links"} <= implemented
    assert not {"__init__", "runners"} & implemented
    items = must_registry_coverage._parse_items(
        (TESTS_DIR / "must_registry.yaml").read_text(encoding="utf-8")
    )
    mapped = {
        n for i in items if i.get("method") == "python"
        for n in must_registry_coverage.check_names(i.get("check", ""))
    }
    helper = set(must_registry_coverage.HELPER)
    assert not mapped & helper, mapped & helper
    assert implemented <= mapped | helper, implemented - mapped - helper
