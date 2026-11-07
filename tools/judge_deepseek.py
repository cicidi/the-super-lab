#!/usr/bin/env python3
"""Real judge: deepseek-flash, 3 independent runs, writes cross-model verdicts.

  python3 tools/judge_deepseek.py --target must   # 15 llm MUST items
  python3 tools/judge_deepseek.py --target gold   # 10 gold annotations

Corpus: committed SDD markdown + the four SKILL.md + SPEC-STANDARD.md, sent whole
(~33k tokens/run). Verdicts aggregate 3/3: unanimous pass, unanimous fail, else
"disputed" (counts as fail). See test-plan TST-D/E/L.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "skills/spec-organize/tests"
SDD = ROOT / "docs/features/spec-driven-development"
REGISTRY = TESTS / "must_registry.yaml"
ANNOTATIONS = TESTS / "annotations.yaml"
OUT_MUST = TESTS / "judgments" / "v1-deepseek-flash.yaml"
OUT_GOLD = TESTS / "judgments" / "annotations-v1-deepseek-flash.yaml"
API = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-flash"
RUNS = 3

SYSTEM = (
    "You are a strict repository auditor. You check whether a repository actually "
    "enforces each normative rule or exhibits each behavior. Never guess: if the "
    "provided corpus does not support a rule, answer fail. Reply with JSON only."
)


def corpus() -> str:
    return "".join(
        f"\n===== FILE: {p.relative_to(ROOT)} =====\n{p.read_text(encoding='utf-8')}"
        for p in corpus_files()
    )


def corpus_sha(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def corpus_files() -> list[Path]:
    """Evidence set fed to the judge; excludes the judge itself to avoid self-staleness."""
    docs = [
        p
        for p in (ROOT / "docs/features").rglob("*.md")
        if not p.name.startswith("._") and "raw" not in p.parts and "site" not in p.parts
    ]
    docs += [ROOT / "docs/INDEX.md"]
    docs += [ROOT / "skills/spec-organize/SPEC-STANDARD.md"]
    docs += [ROOT / f"skills/{n}/SKILL.md" for n in ("spec-pipeline", "spec-organize", "spec-review", "spec-write")]
    # Enforcement evidence: checkers, tools, registry, eval config.
    # Plumbing that is not evidence for any MUST: builders, the harness itself.
    skip = {
        "build_sdd_reader.py",
        "build_sdd_site.py",
        "judge_deepseek.py",
        "score_eval.py",
        "render_eval_report.py",
        "verify_gates.py",
        "run_gold_eval.py",
        "score_run.py",
    }
    code = [p for p in (ROOT / "tools").glob("*.py") if p.name not in skip]
    code += sorted((TESTS / "checks").glob("*.py"))
    harness_tests = {"test_judge_freshness.py", "test_tst_e_gold.py"}
    code += [p for p in sorted(TESTS.glob("test_*.py")) if p.name not in harness_tests]
    code += [
        TESTS / "must_registry.yaml",
        TESTS / "eval.yaml",
        TESTS / "annotations.yaml",
        TESTS / "judgments" / "v1.yaml",
    ]
    files = []
    for p in docs + code:
        if p.is_file() and not p.name.startswith("._"):
            try:
                p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            files.append(p)
    return files


def load_registry() -> list[dict[str, str]]:
    items, cur = [], {}
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        if line.startswith("  - id:"):
            if cur:
                items.append(cur)
            cur = {"id": line.split(":", 1)[1].strip()}
        elif cur and line.strip().startswith("method:"):
            cur["method"] = line.strip().split(":", 1)[1].strip()
        elif cur and line.strip().startswith("text:"):
            cur["text"] = line.strip().split(":", 1)[1].strip().strip("'\"")
    if cur:
        items.append(cur)
    return [i for i in items if i.get("method") == "llm"]


def build_prompt(corpus_text: str, target: str) -> str:
    if target == "must":
        items = [{"id": i["id"], "rule": i.get("text", ""), "source": i.get("source", "")} for i in load_registry()]
        task = (
            "For each MUST rule decide pass only if the corpus shows the repository enforces it. "
            "These are semantic (llm-method) rules: pass when the rule is stated in the standard "
            "and reflected in the relevant skill body or design; a mechanical checker is NOT required "
            "for an llm-method rule. Fail only when the rule is absent or contradicted. "
            'Return {"items":[{"id":"MUST-A","verdict":"pass|fail","evidence":"<=160 chars, cite a file","confidence":0.0}]}'
        )
    else:
        ann = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8"))["annotations"]
        items = [
            {
                "id": a["id"],
                "kind": a["kind"],
                "behavior": a["text"],
                "operational_definition": a.get("detail", ""),
                "rule": "pass means this good behavior holds" if a["kind"] == "good" else "pass means this bad behavior is absent",
            }
            for a in ann
        ]
        task = (
            "For each annotation decide pass if the stated behavior holds in the corpus. "
            'Return {"items":[{"id":"GOOD-A","verdict":"pass|fail","evidence":"<=160 chars, cite a file","confidence":0.0}]}'
        )
    scope = (
        "SCOPE: judge the target feature docs/features/spec-driven-development only. "
        "Other features in the corpus are context; legacy violations in them are out of "
        "scope (ARD-AF: no legacy migration).\n\n"
    )
    return f"{scope}{task}\n\nITEMS:\n{json.dumps(items, ensure_ascii=False, indent=1)}\n\nCORPUS:{corpus_text}"


def call(prompt: str) -> dict:
    body = json.dumps(
        {
            "model": MODEL,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt},
            ],
        }
    ).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
        },
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.load(resp)
    text = data["choices"][0]["message"]["content"]
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    start = text.find("{")
    return json.loads(text[start:])


def aggregate(runs: list[dict]) -> list[dict]:
    by_id: dict[str, list[dict]] = {}
    for run in runs:
        for item in run.get("items", []):
            by_id.setdefault(item["id"], []).append(item)
    out = []
    for ident, votes in by_id.items():
        verdicts = [v.get("verdict", "fail") for v in votes]
        if len(votes) < RUNS:
            final = "fail"
        elif all(v == "pass" for v in verdicts):
            final = "pass"
        elif all(v == "fail" for v in verdicts):
            final = "fail"
        else:
            final = "disputed"
        out.append(
            {
                "id": ident,
                "verdict": final,
                "votes": verdicts,
                "evidence": votes[0].get("evidence", ""),
                "confidence": votes[0].get("confidence"),
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["must", "gold"], default="must")
    ap.add_argument("--runs", type=int, default=RUNS)
    args = ap.parse_args()
    if "DEEPSEEK_API_KEY" not in os.environ:
        sys.exit("DEEPSEEK_API_KEY not set")

    corpus_text = corpus()
    prompt = build_prompt(corpus_text, args.target)
    runs = []
    for i in range(args.runs):
        runs.append(call(prompt))
        print(f"run {i + 1}/{args.runs} done", file=sys.stderr)
    items = aggregate(runs)
    out = OUT_MUST if args.target == "must" else OUT_GOLD
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        yaml.safe_dump(
            {
                "model": MODEL,
                "runs": args.runs,
                "target": args.target,
                "corpus_sha": corpus_sha(corpus_text),
                "items": items,
            },
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    bad = [i for i in items if i["verdict"] != "pass"]
    for i in items:
        print(f"{i['verdict'].upper():9} {i['id']:8} votes={','.join(i['votes'])} {i['evidence'][:90]}")
    print(f"\nwrote {out.relative_to(ROOT)}  ({len(items) - len(bad)} pass / {len(bad)} not pass)")
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
