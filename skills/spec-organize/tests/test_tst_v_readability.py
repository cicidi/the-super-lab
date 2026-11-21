"""TST-V harness (IMPL-Q): question cap, control drop, 2-of-3 verdict — with a fake model."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

import run_readability as rr  # noqa: E402


def _doc(n: int) -> str:
    return "\n\n".join(f"#### DSGN-{chr(65 + i // 26)}{chr(65 + i % 26)} — rule {i}\n\nBody {i}." for i in range(n))


def test_question_cap_is_twenty():
    assert len(rr.extract_items(_doc(25), 20)) == 20


def test_item_text_stops_at_next_heading_of_same_level():
    items = rr.extract_items("#### PRD-A — a\n\nalpha\n\n#### PRD-B — b\n\nbeta\n", 20)
    assert [i["id"] for i in items] == ["PRD-A", "PRD-B"]
    assert "beta" not in items[0]["text"]


def test_control_correct_questions_are_dropped():
    doc = _doc(5)
    fake = rr.FakeModel(known_without_doc={"DSGN-AA", "DSGN-AB"})
    result = rr.run_once(doc, "", fake, 20)
    assert result["questions"] == 5
    assert result["dropped_by_control"] == 2
    assert result["kept"] == 3
    assert result["accuracy"] == 1.0
    assert result["passed"] is True


def test_unexplained_term_fails_the_run():
    result = rr.run_once(_doc(3), "", rr.FakeModel(terms=["HLD"]), 20)
    assert result["accuracy"] == 1.0
    assert result["passed"] is False


def test_two_of_three_verdict():
    assert rr.verdict([True, True, False]) is True
    assert rr.verdict([True, False, False]) is False
    assert rr.verdict([True, True, True]) is True
