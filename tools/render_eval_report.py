#!/usr/bin/env python3
"""IMPL-L / TST-K: render one self-contained HTML report for an eval run.

  python3 tools/render_eval_report.py [--out PATH] [--feature DIR]

Reports are run artifacts: they are not committed (ARD-AD). Default output is
skills/spec-organize/tests/runs/<run_id>/report.html, which is gitignored.
"""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from score_eval import ANNOTATIONS, JUDGED, TESTS, parse_registry, score1, score2  # noqa: E402
from score_run import score_run  # noqa: E402

RUNS = TESTS / "runs"


def git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def eval_config() -> dict:
    return yaml.safe_load((TESTS / "eval.yaml").read_text(encoding="utf-8"))


def judge_meta() -> dict:
    if not JUDGED.exists():
        return {"model": "unjudged", "runs": 0}
    data = yaml.safe_load(JUDGED.read_text(encoding="utf-8")) or {}
    return {"model": data.get("model", "unknown"), "runs": data.get("runs", 0)}


def rows(lines: list[str], columns: list[str]) -> str:
    out = []
    for line in lines:
        cells = line.split("\t")
        padded = (cells + [""] * len(columns))[: len(columns)]
        out.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in padded) + "</tr>")
    return "\n".join(out)


def gold_bundles() -> list[tuple[str, list[dict]]]:
    """Newest bundles with their per-repetition scores."""
    out = []
    for bundle in sorted(RUNS.glob("*/gold"), key=lambda p: p.stat().st_mtime, reverse=True)[:6]:
        rows = []
        for run in sorted(p for p in bundle.iterdir() if p.is_dir() and p.name.startswith("run")):
            passed, total, score, findings, _ = score_run(run)
            rows.append({"run": run.name, "passed": passed, "total": total, "score": score})
        out.append((bundle.parent.name, rows))
    return out


def gold_section() -> str:
    bundles = gold_bundles()
    if not bundles:
        return "<p>No generated gold runs found (runs/ is gitignored).</p>"
    blocks = []
    for name, rows in bundles:
        body = "".join(
            f"<tr><td>{html.escape(r['run'])}</td><td>{r['passed']}/{r['total']}</td>"
            f"<td>{r['score']:.1f}/10</td></tr>"
            for r in rows
        )
        blocks.append(
            f"<h3>{html.escape(name)}</h3><table><thead><tr><th>run</th>"
            f"<th>score 1</th><th>score 2</th></tr></thead><tbody>{body}</tbody></table>"
        )
    return "\n".join(blocks)


def readability_section(path: Path | None) -> str:
    """TST-V: per-doc accuracy and unexplained terms from run_readability.py --out."""
    if path is None or not path.is_file():
        return "<p>No readability results (run <code>tools/run_readability.py --out</code>).</p>"
    import json

    reports = json.loads(path.read_text(encoding="utf-8")).get("readability", [])
    body = "".join(
        f"<tr><td class=\"{'pass' if r['passed'] else 'fail'}\">{'PASS' if r['passed'] else 'FAIL'}</td>"
        f"<td>{html.escape(r['doc'])}</td>"
        f"<td>{', '.join(f'{x['accuracy']:.0%}' for x in r['runs'])}</td>"
        f"<td>{html.escape(', '.join(sorted({t for x in r['runs'] for t in x['unexplained_terms']})) or '-')}</td></tr>"
        for r in reports
    )
    return (
        "<table><thead><tr><th>verdict</th><th>doc</th><th>accuracy per run</th>"
        f"<th>unexplained terms</th></tr></thead><tbody>{body}</tbody></table>"
    )


def score2_max() -> float:
    """Highest reachable score 2: GOOD x 10 / total annotations."""
    entries = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8"))["annotations"]
    return 10 * sum(1 for e in entries if e["kind"] == "good") / len(entries)


def with_method(lines: list[str]) -> list[str]:
    """Insert each MUST item's method (python or llm) after its id."""
    methods = {i["id"]: i.get("method", "") for i in parse_registry()}
    out = []
    for line in lines:
        verdict, ident, detail = (line.split("\t", 2) + ["", ""])[:3]
        method = "python" if methods.get(ident) == "python" else "llm"
        out.append(f"{verdict}\t{ident}\t{method}\t{detail}")
    return out


def review_section() -> str:
    """TST-L: 5-run review per item, with Claude's audit note."""
    files = sorted((TESTS / "judgments").glob("*-deepseek-flash.yaml"))
    if not files:
        return "<p>No review results (run <code>tools/judge_deepseek.py</code>).</p>"
    blocks = []
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        body = "".join(
            f"<tr><td>{html.escape(str(i.get('id', '')))}</td>"
            f"<td>{html.escape(str(i.get('verdict', '')))}</td>"
            f"<td>{html.escape(', '.join(map(str, i.get('votes') or [])))}</td>"
            f"<td>{html.escape(str(i.get('claude_audit') or '-'))}</td></tr>"
            for i in data.get("items", [])
        )
        blocks.append(
            f"<h3>{html.escape(path.name)} — {html.escape(str(data.get('model', '')))} "
            f"x {data.get('runs', 0)} runs</h3><table><thead><tr><th>id</th><th>verdict</th>"
            f"<th>votes</th><th>claude_audit</th></tr></thead><tbody>{body}</tbody></table>"
        )
    return "\n".join(blocks)


TSTF_INPUTS = ("budget-conflict", "family-disagree", "missing-info", "midway-change")


def tstf_section(path: Path | None) -> str:
    """TST-F: the four abnormal inputs, from runs/<id>/tstf.json ({input: {verdict, note}})."""
    import json

    ran = path is not None and path.is_file()
    results = json.loads(path.read_text(encoding="utf-8")) if ran else {}
    body = ""
    for name in TSTF_INPUTS:
        r = results.get(name) or {}
        verdict = str(r.get("verdict", "not run"))
        cls = {"pass": "pass", "fail": "fail"}.get(verdict, "")
        body += (
            f"<tr><td>{html.escape(name)}</td><td class=\"{cls}\">{html.escape(verdict)}</td>"
            f"<td>{html.escape(str(r.get('note', '-')))}</td></tr>"
        )
    return ("" if ran else "<p>TST-F: not run.</p>") + (
        "<table><thead><tr><th>input</th><th>verdict</th><th>note</th></tr></thead>"
        f"<tbody>{body}</tbody></table>"
    )


def render(run_id: str, readability: Path | None = None, tstf: Path | None = None) -> str:
    passed, total, s1_lines = score1(ROOT / "docs/features/spec-driven-development")
    s2, s2_lines = score2(ROOT / "docs/features/spec-driven-development")
    cfg = eval_config()
    judge = judge_meta()
    meta = [
        ("run_id", run_id),
        ("branch", git("rev-parse", "--abbrev-ref", "HEAD")),
        ("commit", git("rev-parse", "--short", "HEAD")),
        ("gold version", cfg["gold"]["version"]),
        ("judge", f"{judge['model']} x {judge['runs']} runs"),
        ("grill.skills", ", ".join(cfg["grill"]["skills"]) or "(baseline: none)"),
        (
            "eval config",
            f"gold {', '.join(cfg['gold']['models'])} x {cfg['gold']['repeats']}; "
            f"review {', '.join(cfg['checkers']['models'])} x {cfg['checkers']['repeats']}; "
            f"target {cfg['target']['feature']}",
        ),
        ("generated", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
    ]
    meta_html = "\n".join(f"<tr><th>{html.escape(k)}</th><td>{html.escape(str(v))}</td></tr>" for k, v in meta)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SDD eval report — {html.escape(run_id)}</title>
<style>
 body{{font-family:Roboto,Arial,sans-serif;margin:0;background:#fff;color:#202124;font-size:15px;line-height:1.6}}
 main{{max-width:980px;margin:0 auto;padding:32px 24px 64px}}
 h1{{font-family:"Google Sans",Arial,sans-serif;font-weight:400;font-size:30px;margin:0 0 8px}}
 h2{{font-family:"Google Sans",Arial,sans-serif;font-weight:400;font-size:21px;margin:32px 0 10px}}
 table{{border-collapse:collapse;width:100%;font-size:13.5px}}
 th,td{{border-bottom:1px solid #e8eaed;padding:8px 10px;text-align:left;vertical-align:top}}
 th{{background:#f8f9fa;font-weight:500}}
 .score{{display:flex;gap:24px;margin:20px 0}}
 .score div{{border:1px solid #dadce0;border-radius:8px;padding:14px 20px}}
 .score b{{font-family:"Google Sans",Arial,sans-serif;font-size:26px;font-weight:400}}
 .pass{{color:#1e8e3e}} .fail{{color:#d93025}}
 code{{font-family:"Roboto Mono",monospace;background:#f1f3f4;padding:1px 5px;border-radius:4px}}
</style>
</head>
<body><main>
<h1>SDD eval report</h1>
<p><code>{html.escape(run_id)}</code></p>
<table>{meta_html}</table>

<div class="score">
  <div>score 1 — MUST<br><b class="{'pass' if passed == total else 'fail'}">{passed}/{total}</b></div>
  <div>score 2 — gold<br><b>{s2:.1f}/10</b><br><small>max {score2_max():.1f}; no fixed floor (ARD-R)</small></div>
</div>

<h2>Score 1 — per MUST item</h2>
<table><thead><tr><th>verdict</th><th>id</th><th>method</th><th>detail</th></tr></thead>
<tbody>{rows(with_method(s1_lines), ["verdict", "id", "method", "detail"])}</tbody></table>

<h2>Score 2 — annotations</h2>
<table><thead><tr><th>±</th><th>id</th><th>source</th><th>behavior</th></tr></thead>
<tbody>{rows(s2_lines, ["±", "id", "source", "behavior"])}</tbody></table>

<h2>Generated gold runs (TST-C / TST-E)</h2>
{gold_section()}

<h2>Readability (TST-V)</h2>
{readability_section(readability)}

<h2>TST-F inputs</h2>
{tstf_section(tstf)}

<h2>Review (TST-L)</h2>
{review_section()}

<h2>Configs (TST-J)</h2>
<p>Each <code>grill.skills</code> config ([], [research], [grill-with-docs], both) is recorded
as its own bundle; wayfinder is always on. Scores are reported, not gated.</p>
</main></body></html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    ap.add_argument("--run-id", default="")
    ap.add_argument("--readability", default="", help="run_readability.py --out JSON (default runs/<id>/readability.json)")
    ap.add_argument("--tstf", default="", help="TST-F results JSON (default runs/<id>/tstf.json)")
    args = ap.parse_args()
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = Path(args.out) if args.out else TESTS / "runs" / run_id / "report.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    readability = Path(args.readability) if args.readability else TESTS / "runs" / run_id / "readability.json"
    tstf = Path(args.tstf) if args.tstf else TESTS / "runs" / run_id / "tstf.json"
    out.write_text(render(run_id, readability, tstf), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
