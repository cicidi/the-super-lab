"""IMPL-J: eval configuration must stay runnable (judge, gold, checkers, target)."""

from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parent / "eval.yaml"


def config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def test_judge_and_checkers_use_deepseek_flash():
    data = config()
    assert data["judge"]["model"] == "deepseek-flash"
    assert data["checkers"]["models"] == ["deepseek-flash"]
    assert data["checkers"]["repeats"] == 3
    assert data["single_provider"] is True


def test_gold_case_and_repeats():
    data = config()
    assert data["gold"]["version"] == "v1"
    assert data["gold"]["repeats"] == 3
    case = data["gold"]["cases"]["iphone"]
    assert case["version"] == "v1"
    assert (CONFIG.parent / case["path"]).is_dir(), "gold case path missing"
    assert (CONFIG.parent / case["path"] / "requirement.md").is_file()
    assert (CONFIG.parent / case["path"] / "context.md").is_file()


def test_baseline_grill_and_target():
    data = config()
    assert data["grill"]["skills"] == []
    assert data["target"]["repo"], "target.repo required (SDD_EVAL_REPO overrides)"
    assert data["target"]["feature"]
