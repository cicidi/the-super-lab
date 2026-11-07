"""Judgments must match the corpus they judge, or the scores are stale.

Freshness is content-based: verdict records carry the corpus hash they were
produced from. Any edit to spec, skills, checkers, registry, or annotations
changes that hash and fails this test until tools/judge_deepseek.py is re-run
for both targets.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from judge_deepseek import OUT_GOLD, OUT_MUST, corpus, corpus_sha  # noqa: E402


def test_judgments_match_current_corpus():
    current = corpus_sha(corpus())
    for out in (OUT_MUST, OUT_GOLD):
        assert out.exists(), f"missing verdicts: {out}"
        data = yaml.safe_load(out.read_text(encoding="utf-8")) or {}
        assert data.get("corpus_sha") == current, (
            f"{out.name} was produced from a different corpus; "
            "re-run tools/judge_deepseek.py"
        )
