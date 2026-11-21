#!/usr/bin/env python3
"""TST-V readability (IMPL-Q): can an undergraduate programmer answer questions from one doc alone?

Usage:
  python3 tools/run_readability.py DOC.md [DOC.md ...] [--runs 3] [--max-q 20] [--out FILE.json] [--dry-run]

Per run: one question per numbered item (max 20); drop questions the model answers without the
doc; answer the rest with only the doc and the glossary; grade; list unexplained terms.
A run passes at >= 80% correct and 0 unexplained terms. A doc passes when 2 of 3 runs pass.
--dry-run swaps the API for a deterministic fake model (no network, no key).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "skills/spec-organize/tests/eval.yaml"
GLOSSARY_DOC = ROOT / "docs/features/spec-driven-development/design/spec-driven-development-design.md"
ID_HEAD = re.compile(r"^(#{2,4})\s+((?:PRD|DSGN|PIPE|IMPL|TST|ARD)-[A-Z]+)\b.*$", re.M)
PASS_ACCURACY = 0.8
MAX_ITEM_CHARS = 1500

Ask = Callable[[str], dict]

PERSONA = (
    "You are an undergraduate programmer. You know general programming, but nothing about "
    "this project except what you are given."
)


def glossary_text() -> str:
    text = GLOSSARY_DOC.read_text(encoding="utf-8")
    start = text.find('<a id="glossary">')
    if start < 0:
        return ""
    end = text.find("\n## ", start + 1)
    return text[start : end if end > 0 else len(text)]


def extract_items(text: str, max_q: int) -> list[dict[str, str]]:
    heads = list(ID_HEAD.finditer(text))
    items = []
    for i, m in enumerate(heads):
        level = len(m.group(1))
        stop = len(text)
        for later in re.finditer(r"^(#{1,6})\s", text[m.end() :], re.M):
            if len(later.group(1)) <= level:
                stop = m.end() + later.start()
                break
        items.append({"id": m.group(2), "text": text[m.start() : stop].strip()[:MAX_ITEM_CHARS]})
    seen: set[str] = set()
    unique = [it for it in items if not (it["id"] in seen or seen.add(it["id"]))]
    return unique[:max_q]


def _prompt(task: str, instructions: str, payload: dict) -> str:
    return f"TASK: {task}\n{instructions}\nReply with JSON only.\nPAYLOAD:\n{json.dumps(payload, ensure_ascii=False)}"


def make_questions(items: list[dict[str, str]], ask: Ask) -> list[dict[str, str]]:
    out = ask(
        _prompt(
            "QUESTIONS",
            "For each item write one question a reader can answer only by understanding that item, "
            'and its short reference answer. Return {"questions":[{"id","question","answer"}]}.',
            {"items": items},
        )
    )
    return [q for q in out.get("questions", []) if q.get("id") and q.get("question")]


def answer(questions: list[dict[str, str]], ask: Ask, doc: str | None, glossary: str) -> dict[str, str]:
    qs = [{"id": q["id"], "question": q["question"]} for q in questions]
    if doc is None:
        task, payload = "CONTROL", {"questions": qs}
        how = PERSONA + " Answer from general knowledge only; say 'unknown' if you cannot."
    else:
        task, payload = "ANSWER", {"questions": qs, "document": doc, "glossary": glossary}
        how = PERSONA + " Answer using only the document and the glossary."
    out = ask(_prompt(task, how + ' Return {"answers":[{"id","answer"}]}.', payload))
    return {a["id"]: a.get("answer", "") for a in out.get("answers", []) if a.get("id")}


def grade(questions: list[dict[str, str]], answers: dict[str, str], ask: Ask) -> dict[str, bool]:
    pairs = [
        {"id": q["id"], "question": q["question"], "reference": q["answer"], "answer": answers.get(q["id"], "")}
        for q in questions
    ]
    out = ask(
        _prompt(
            "GRADE",
            "Mark an answer correct when it states the same fact as the reference. "
            'Return {"grades":[{"id","correct"}]}.',
            {"pairs": pairs},
        )
    )
    return {g["id"]: bool(g.get("correct")) for g in out.get("grades", []) if g.get("id")}


def unexplained_terms(doc: str, glossary: str, ask: Ask) -> list[str]:
    out = ask(
        _prompt(
            "TERMS",
            PERSONA + " List terms used in the document that are neither explained where they first "
            'appear nor in the glossary. Return {"terms":[...]}.',
            {"document": doc, "glossary": glossary},
        )
    )
    return [t for t in out.get("terms", []) if isinstance(t, str) and t.strip()]


def run_once(doc: str, glossary: str, ask: Ask, max_q: int) -> dict:
    questions = make_questions(extract_items(doc, max_q), ask)
    control = grade(questions, answer(questions, ask, None, glossary), ask)
    kept = [q for q in questions if not control.get(q["id"], False)]
    grades = grade(kept, answer(kept, ask, doc, glossary), ask) if kept else {}
    correct = sum(1 for q in kept if grades.get(q["id"], False))
    accuracy = correct / len(kept) if kept else 1.0
    terms = unexplained_terms(doc, glossary, ask)
    return {
        "questions": len(questions),
        "dropped_by_control": len(questions) - len(kept),
        "kept": len(kept),
        "correct": correct,
        "accuracy": round(accuracy, 3),
        "unexplained_terms": terms,
        "passed": accuracy >= PASS_ACCURACY and not terms,
    }


def verdict(passes: list[bool]) -> bool:
    """2 of 3 runs must pass (TST-V)."""
    need = max(1, (2 * len(passes) + 2) // 3)
    return sum(passes) >= need


def evaluate(doc_path: Path, ask: Ask, runs: int, max_q: int) -> dict:
    doc = doc_path.read_text(encoding="utf-8")
    glossary = glossary_text()
    results = [run_once(doc, glossary, ask, max_q) for _ in range(runs)]
    return {
        "doc": str(doc_path.relative_to(ROOT)) if doc_path.is_relative_to(ROOT) else str(doc_path),
        "runs": results,
        "passed": verdict([r["passed"] for r in results]),
    }


class FakeModel:
    """Deterministic stand-in: answers with the reference, knows nothing without the doc."""

    def __init__(self, known_without_doc: set[str] | None = None, terms: list[str] | None = None):
        self.known = known_without_doc or set()
        self.terms = terms or []
        self.refs: dict[str, str] = {}

    def __call__(self, prompt: str) -> dict:
        task = prompt.split("\n", 1)[0].removeprefix("TASK: ").strip()
        payload = json.loads(prompt.split("PAYLOAD:\n", 1)[1])
        if task == "QUESTIONS":
            qs = [{"id": it["id"], "question": f"What does {it['id']} require?", "answer": f"ref-{it['id']}"} for it in payload["items"]]
            self.refs.update({q["id"]: q["answer"] for q in qs})
            return {"questions": qs}
        if task == "CONTROL":
            return {"answers": [{"id": q["id"], "answer": self.refs[q["id"]] if q["id"] in self.known else "unknown"} for q in payload["questions"]]}
        if task == "ANSWER":
            return {"answers": [{"id": q["id"], "answer": self.refs.get(q["id"], "")} for q in payload["questions"]]}
        if task == "GRADE":
            return {"grades": [{"id": p["id"], "correct": p["answer"] == p["reference"]} for p in payload["pairs"]]}
        if task == "TERMS":
            return {"terms": list(self.terms)}
        raise ValueError(f"unknown task {task}")


def api_model() -> Ask:
    sys.path.insert(0, str(ROOT / "tools"))
    import judge_deepseek

    cfg = yaml.safe_load(EVAL.read_text(encoding="utf-8"))
    judge_deepseek.MODEL = cfg["judge"]["model"]
    return judge_deepseek.call


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("docs", nargs="+")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--max-q", type=int, default=20)
    ap.add_argument("--out", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.dry_run:
        ask: Ask = FakeModel()
    else:
        import os

        if "DEEPSEEK_API_KEY" not in os.environ:
            sys.exit("DEEPSEEK_API_KEY not set (use --dry-run to test without the API)")
        ask = api_model()
    reports = []
    for d in args.docs:
        path = Path(d) if Path(d).is_absolute() else ROOT / d
        rep = evaluate(path, ask, args.runs, args.max_q)
        reports.append(rep)
        accs = ", ".join(f"{r['accuracy']:.0%}" for r in rep["runs"])
        terms = sorted({t for r in rep["runs"] for t in r["unexplained_terms"]})
        print(f"{'PASS' if rep['passed'] else 'FAIL'}\t{rep['doc']}\taccuracy {accs}\tterms {terms or '-'}")
    if args.out:
        Path(args.out).write_text(json.dumps({"readability": reports}, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.exit(0 if all(r["passed"] for r in reports) else 1)


if __name__ == "__main__":
    main()
