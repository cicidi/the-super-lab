"""TST-AA: wayfinder carries the SDD progress rules (parent ARD-CH)."""

from pathlib import Path

SKILL = Path(__file__).resolve().parents[3] / "skills/wayfinder/SKILL.md"

REQUIRED = {
    "map file before the name is confirmed": "docs/state/wayfinder-<working-name>.md",
    "map file after the name is confirmed": "docs/features/<f>/raw/state/wayfinder-map.md",
    "review gate asks for spec-review (PIPE-A-D)": "ask whether to run **spec-review** first",
    "a declined review is recorded": "spec-review skipped by user",
    "blocking briefs stop Downstream (PIPE-E-A)": "do not\n  start Downstream",
    "recap on resume (PIPE-A-E)": "Recap on resume",
}


def test_wayfinder_states_each_progress_rule():
    text = SKILL.read_text(encoding="utf-8")
    missing = [what for what, needle in REQUIRED.items() if needle not in text]
    assert not missing, f"wayfinder SKILL.md lacks: {missing}"


def test_wayfinder_no_longer_points_at_doc_review_or_mkdocs():
    text = SKILL.read_text(encoding="utf-8").lower()
    assert "doc-review" not in text and "mkdocs" not in text
