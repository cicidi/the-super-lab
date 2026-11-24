"""TST-AA: wayfinder carries the SDD progress rules (parent ARD-CH)."""

from pathlib import Path

SKILL = Path(__file__).resolve().parents[3] / "skills/wayfinder/SKILL.md"

REQUIRED = {
    "map before the name is confirmed": "docs/state/wayfinder-<working-name>/map.md",
    "map directory after the name is confirmed": "docs/features/<f>/raw/state/wayfinder/",
    "SDD mode always creates the map": "always create the map",
    "review gate asks for spec-review (PIPE-A-D)": "ask whether to run **spec-review** first",
    "a declined review is recorded": "spec-review skipped by user",
    "blocking briefs stop Downstream (PIPE-E-A)": "do not\n  start Downstream",
    "recap on resume (PIPE-A-E)": "Recap on resume",
    "blocking questions come from the design's QUES tracker": "design's Open Questions tracker: `QUES-*`",
    "SDD claim is an Assignee line": "an `Assignee:` line",
    "SDD resolve adds an Answer section": "add a `## Answer` section",
    "SDD committed docs are authoritative": "the committed docs (decision-history, PRD, design) are authoritative",
    "SDD Downstream needs no open blocking QUES": "marked blocking = yes (PIPE-E-A)",
}


def test_wayfinder_states_each_progress_rule():
    text = SKILL.read_text(encoding="utf-8")
    missing = [what for what, needle in REQUIRED.items() if needle not in text]
    assert not missing, f"wayfinder SKILL.md lacks: {missing}"


def test_wayfinder_no_longer_points_at_doc_review_or_mkdocs():
    text = SKILL.read_text(encoding="utf-8").lower()
    assert "doc-review" not in text and "mkdocs" not in text


def test_wayfinder_is_tracker_neutral():
    assert "jira" not in SKILL.read_text(encoding="utf-8").lower()


def test_wayfinder_has_no_bare_commit_trigger():
    import yaml

    text = SKILL.read_text(encoding="utf-8")
    front = yaml.safe_load(text.split("---", 2)[1])
    triggers = [t.strip().lower() for t in front["metadata"]["triggers"]]
    assert "commit" not in triggers, "bare `commit` trigger collides with the commit skill"
