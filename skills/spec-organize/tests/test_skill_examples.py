"""TST-S: each skill body names the four PRD-Q examples; spec-review reads contracts."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "skills"

# PRD-Q: 盖 shed、北京旅游、数学题、股票. Word boundaries keep "bikeshedding"/"finished" out.
EXAMPLES = [
    ("shed", re.compile(r"\bshed\b")),
    ("北京旅游", re.compile("北京旅游")),
    ("数学题", re.compile("数学题")),
    ("股票", re.compile("股票")),
]
SKILL_NAMES = ["spec-pipeline", "spec-organize", "spec-review", "spec-write"]

CONTRACT = "docs/features/spec-driven-development/design/spec-driven-development-design-skill-contracts.md"


def body(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_skill_names_four_examples(name):
    text = body(name)
    missing = [label for label, pattern in EXAMPLES if not pattern.search(text)]
    assert not missing, f"{name}/SKILL.md missing PRD-Q examples: {missing}"


def test_spec_review_cites_contract():
    assert CONTRACT in body("spec-review"), (
        "spec-review/SKILL.md must cite the skill contracts authority (IMPL-N)"
    )
