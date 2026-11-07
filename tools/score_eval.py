#!/usr/bin/env python3
"""Score 1 (MUST x/total) and score 2 (gold annotations 0-10) per the SDD test plan.

Usage:
  python3 tools/score_eval.py [feature_dir] [--min-score2 N]

Score 1: python-method items run the mechanical checkers; llm-method items read
verdicts from `skills/spec-organize/tests/judgments/v1.yaml`. An unjudged llm item
counts as fail — the gate is total/total.

Score 2: each annotation in `skills/spec-organize/tests/annotations.yaml` is a
behavioral rule over the feature tree. GOOD hit +1, BAD violated -1;
score = (plus - minus) * 10 / total.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "skills/spec-organize/tests"
sys.path.insert(0, str(TESTS))

from checks.book import check_book  # noqa: E402
from checks.change_log import check_change_log  # noqa: E402
from checks.collision import check_collision  # noqa: E402
from checks.publish_nav import check_publish_nav  # noqa: E402
from checks.registry_provenance import check_registry_provenance  # noqa: E402
from checks.test_trace import check_test_trace  # noqa: E402
from checks.decision_log import check_decision_log  # noqa: E402
from checks.frontmatter import Finding, check_frontmatter  # noqa: E402
from checks.ids import check_ids  # noqa: E402
from checks.index_book import check_index_book  # noqa: E402
from checks.no_commit import check_no_commit_tree  # noqa: E402
from checks.parent_complete import check_parent_complete  # noqa: E402
from checks.paths import check_committed_path  # noqa: E402
from checks.sections import check_sections  # noqa: E402
from checks.size import check_size  # noqa: E402

REGISTRY = TESTS / "must_registry.yaml"
JUDGMENTS = TESTS / "judgments" / "v1.yaml"
JUDGED = TESTS / "judgments" / "v1-deepseek-flash.yaml"
ANNOTATIONS = TESTS / "annotations.yaml"
ANNOT_VERDICTS = TESTS / "judgments" / "annotations-v1-deepseek-flash.yaml"
DEFAULT_FEATURE = ROOT / "docs/features/spec-driven-development"

EXEMPT: set[Path] = set()  # no grandfathered paths (IMPL-M)
FILE_CHECKS = [
    check_frontmatter,
    check_committed_path,
    check_sections,
    check_decision_log,
    check_change_log,
    check_ids,
    check_size,
]


def md_files(base: Path) -> list[Path]:
    return [
        p
        for p in sorted(base.rglob("*.md"))
        if not p.name.startswith("._")
        and "__pycache__" not in p.parts
        and "/raw/" not in p.as_posix()
        and ".scratch" not in p.as_posix()
    ]


def collect(feature: Path) -> dict[str, list[Finding]]:
    """Findings keyed by check id, same runners as tools/run_spec_checks.py."""
    features_root = ROOT / "docs/features"
    findings: list[Finding] = []
    if features_root.is_dir():
        findings += check_collision(features_root)
        findings += check_no_commit_tree(features_root)
        findings += check_index_book(ROOT)
        findings += check_book(ROOT)
        findings += check_publish_nav(ROOT)
        findings += check_test_trace(feature)
        findings += check_registry_provenance(ROOT)
    if feature.is_dir() and feature.parent.name == "features":
        findings += check_parent_complete(feature)
    for path in md_files(feature):
        if path.resolve() in EXEMPT:
            continue
        text = path.read_text(encoding="utf-8")
        for fn in FILE_CHECKS:
            findings += fn(path, text)
    grouped: dict[str, list[Finding]] = {}
    for f in findings:
        grouped.setdefault(f.check, []).append(f)
    return grouped


def parse_registry() -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    cur: dict[str, str] = {}
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        if line.startswith("  - id:"):
            if cur:
                items.append(cur)
            cur = {"id": line.split(":", 1)[1].strip()}
        elif cur and line.strip().startswith(("method:", "check:")):
            key, value = line.strip().split(":", 1)
            cur[key] = value.strip().strip("'\"")
    if cur:
        items.append(cur)
    return items


def score1(feature: Path) -> tuple[int, int, list[str]]:
    grouped = collect(feature)
    judgments: dict[str, dict] = {}
    source = JUDGED if JUDGED.exists() else JUDGMENTS
    if source.exists():
        raw = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
        judgments = {j["id"]: j for j in raw.get("items", [])}
    passed, lines = 0, []
    for item in parse_registry():
        ident, method = item["id"], item.get("method", "")
        if method == "python":
            check = item.get("check", "")
            findings = grouped.get(check, [])
            ok = not findings
            detail = f"{check}: {len(findings)} finding(s)"
        else:
            verdict = judgments.get(ident)
            if not verdict:
                ok, detail = False, "unjudged"
            else:
                ok = verdict.get("verdict") == "pass"
                detail = verdict.get("evidence", "")
        passed += ok
        lines.append(f"{'PASS' if ok else 'FAIL'}\t{ident}\t{detail}")
    return passed, len(parse_registry()), lines


def _texts(feature: Path) -> dict[Path, str]:
    return {p: p.read_text(encoding="utf-8") for p in md_files(feature)}


def _designs(feature: Path) -> list[Path]:
    return [p for p in md_files(feature) if "design" in p.parts]


def _examples() -> list[re.Pattern[str]]:
    return [re.compile(r"\bshed\b"), re.compile("北京旅游"), re.compile("数学题"), re.compile("股票")]


# --- annotation predicates: True means the stated behavior holds -------------

def _strip_code(text: str) -> str:
    """Rules quote counter-examples inside backticks; only real ids count."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`]*`", "", text)


def a_letter_ids(feature: Path) -> bool:
    bad = re.compile(r"\b(PRD|DSGN|ARD|IMPL|TST|PIPE)-\d+\b|\b0\d{3}\b")
    return not any(bad.search(_strip_code(t)) for t in _texts(feature).values())


def a_prd_anchor(feature: Path) -> bool:
    texts = _texts(feature)
    prd = "\n".join(t for p, t in texts.items() if p.parts[-2] == "prd")
    prd_ids = set(re.findall(r"PRD-[A-Z]+", prd))
    design = "\n".join(texts[p] for p in _designs(feature))
    return bool(prd_ids) and prd_ids <= set(re.findall(r"PRD-[A-Z]+", design))


def a_five_types(feature: Path) -> bool:
    have = {p.parts[-2] for p in md_files(feature)}
    return {"prd", "design", "decision-history", "impl-plan", "test-plan"} <= have


def a_change_log_last(feature: Path) -> bool:
    for p, text in _texts(feature).items():
        heads = re.findall(r"^## .+$", text, flags=re.M)
        if not heads or not heads[-1].startswith("## Change Log"):
            return False
    return True


def a_ownership(feature: Path) -> bool:
    text = "\n".join(_texts(feature)[p] for p in _designs(feature))
    return "子问题归属" in text and bool(re.search(r"ARD-[A-Z]+|raw/|https?://", text))


def a_skill_examples(feature: Path) -> bool:
    skills = ROOT / "skills"
    for name in ("spec-pipeline", "spec-organize", "spec-review", "spec-write"):
        text = (skills / name / "SKILL.md").read_text(encoding="utf-8")
        if not all(pat.search(text) for pat in _examples()):
            return False
    return True


def a_index_complete(feature: Path) -> bool:
    return not check_index_book(ROOT)


def a_no_size_overflow(feature: Path) -> bool:
    return not any(check_size(p, t) for p, t in _texts(feature).items())


def a_contract_cited(feature: Path) -> bool:
    text = (ROOT / "skills/spec-review/SKILL.md").read_text(encoding="utf-8")
    return "spec-driven-development-design-skill-contracts.md" in text


def a_dh_newest_first(feature: Path) -> bool:
    for p, text in _texts(feature).items():
        if "decision-history" in p.parts:
            dates = re.findall(r"^\| ARD-[A-Z]+ \| (\d{4}-\d{2}-\d{2})", text, flags=re.M)
            return dates == sorted(dates, reverse=True)
    return False


PREDICATES = {
    "letter_ids": a_letter_ids,
    "prd_anchor": a_prd_anchor,
    "five_types": a_five_types,
    "change_log_last": a_change_log_last,
    "ownership": a_ownership,
    "skill_examples": a_skill_examples,
    "index_complete": a_index_complete,
    "no_size_overflow": a_no_size_overflow,
    "contract_cited": a_contract_cited,
    "dh_newest_first": a_dh_newest_first,
}


def score2(feature: Path) -> tuple[float, list[str]]:
    data = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8"))
    entries = data["annotations"]
    verdicts: dict[str, str] = {}
    if ANNOT_VERDICTS.exists():
        raw = yaml.safe_load(ANNOT_VERDICTS.read_text(encoding="utf-8")) or {}
        verdicts = {i["id"]: i["verdict"] for i in raw.get("items", [])}
    plus = minus = 0
    lines = []
    for entry in entries:
        check = entry["check"]
        assert check in PREDICATES, f"unknown annotation check {check}"
        if verdicts:
            holds = verdicts.get(entry["id"]) == "pass"
            source = "judge"
        else:
            holds = PREDICATES[check](feature)
            source = "mechanical"
        kind = entry["kind"]
        delta = 0
        if kind == "good":
            delta = 1 if holds else 0
        else:  # bad: holding means the bad behavior is NOT committed
            delta = 0 if holds else -1
        plus += max(delta, 0)
        minus += max(-delta, 0)
        lines.append(
            f"{'+' if delta > 0 else '-' if delta < 0 else ' '}\t{entry['id']}\t[{source}]\t{entry['text']}"
        )
    return (plus - minus) * 10 / len(entries), lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("feature", nargs="?", default=str(DEFAULT_FEATURE))
    ap.add_argument("--min-score2", type=float, default=6.0)
    args = ap.parse_args()
    feature = Path(args.feature)
    if not feature.is_absolute():
        feature = ROOT / feature

    passed, total, s1_lines = score1(feature)
    s2, s2_lines = score2(feature)

    print("# score 1 — MUST compliance")
    for line in s1_lines:
        print(line)
    print(f"\nscore1 = {passed}/{total}  gate={'PASS' if passed == total else 'FAIL'}")
    print("\n# score 2 — annotations")
    for line in s2_lines:
        print(line)
    print(f"\nscore2 = {s2:.1f}/10  gate={'PASS' if s2 >= args.min_score2 else 'FAIL'} (min {args.min_score2})")

    ok = passed == total and s2 >= args.min_score2
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
