#!/usr/bin/env python3
"""IMPL-E / TST-C: run the skill against gold v1 and capture a feature spec.

  python3 tools/run_gold_eval.py --runs 3 [--run-id ID]

Each run answers as spec-organize + spec-write would, using ONLY
gold/v1/requirement.md and gold/v1/context.md (interview answers). Outputs land
under skills/spec-organize/tests/runs/<run_id>/gold/run<N>/ and are gitignored
(ARD-AD: runs are not committed).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "skills/spec-organize/tests"
GOLD = TESTS / "gold" / "v1"
STANDARD = ROOT / "skills/spec-organize/SPEC-STANDARD.md"
API = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-flash"
DOCS = {
    "prd": "prd/iphone-purchase-prd.md",
    "design": "design/iphone-purchase-design.md",
    "decision_history": "decision-history/iphone-purchase-decision-history.md",
    "impl_plan": "impl-plan/iphone-purchase-impl-plan.md",
    "test_plan": "test-plan/iphone-purchase-test-plan.md",
}

SYSTEM = (
    "You are the spec-organize and spec-write skills. You produce committed feature "
    "spec documents that follow the project standard exactly. Answer with JSON only."
)

INSTRUCTIONS = """\
Produce the five committed documents for feature `iphone-purchase`.

Rules:
1. Follow SPEC-STANDARD below: frontmatter (feature, type, state: draft), required
   sections per type, letter-prefix ids only (PRD-A, DSGN-A, ARD-A, IMPL-A, TST-A),
   Change Log as the last section, decision log newest-first with columns
   `| ID | Date | Decision |`.
2. Interview answers may come ONLY from the context pack. Anything not in it is
   written as 未提供; never invent a fact about the user.
3. Every PRD requirement must be anchored in the design.
4. Keep each document under its hard cap (prd 800, design/impl-plan 1000,
   test-plan 800 lines).
5. Output JSON with exactly these keys: prd, design, decision_history,
   impl_plan, test_plan. Each value is the full markdown of one document.
"""


def call(prompt: str) -> dict:
    body = json.dumps(
        {
            "model": MODEL,
            "temperature": 0.3,
            "max_tokens": 64000,
            "response_format": {"type": "json_object"},
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
    with urllib.request.urlopen(req, timeout=900) as resp:
        data = json.load(resp)
    choice = data["choices"][0]
    if choice.get("finish_reason") not in (None, "stop"):
        print(f"warning: finish_reason={choice.get('finish_reason')}", file=sys.stderr)
    text = choice["message"]["content"].strip()
    start = text.find("{")
    payload, _ = json.JSONDecoder().raw_decode(text[start:])
    return payload


def build_prompt(grill: list[str] | None = None) -> str:
    extra = ""
    for name in grill or []:
        body = ROOT / f"skills/{name}/SKILL.md"
        if body.is_file():
            extra += f"\n\nADDITIONAL SKILL `{name}`:\n{body.read_text(encoding='utf-8')}"
    return (
        f"{INSTRUCTIONS}\n\nSPEC-STANDARD:\n{STANDARD.read_text(encoding='utf-8')}\n\n"
        f"REQUIREMENT:\n{(GOLD / 'requirement.md').read_text(encoding='utf-8')}\n\n"
        f"CONTEXT (interview answers):\n{(GOLD / 'context.md').read_text(encoding='utf-8')}\n"
        f"{extra}"
    )


def write_run(base: Path, payload: dict) -> list[str]:
    missing = [k for k in DOCS if not payload.get(k)]
    base.mkdir(parents=True, exist_ok=True)
    for key, rel in DOCS.items():
        text = payload.get(key, "")
        path = base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return missing


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--run-id", default="")
    ap.add_argument("--grill", default="", help="comma-separated extra skills, TST-F variants")
    args = ap.parse_args()
    grill = [s.strip() for s in args.grill.split(",") if s.strip()]
    if "DEEPSEEK_API_KEY" not in os.environ:
        sys.exit("DEEPSEEK_API_KEY not set")
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    prompt = build_prompt(grill)
    out = TESTS / "runs" / run_id
    for i in range(1, args.runs + 1):
        payload = call(prompt)
        missing = write_run(out / "gold" / f"run{i}", payload)
        status = "ok" if not missing else f"missing {missing}"
        print(f"run {i}/{args.runs}: {status}", flush=True)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
