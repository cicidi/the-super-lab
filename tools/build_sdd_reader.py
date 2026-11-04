#!/usr/bin/env python3
"""Build spec-driven-development-reader.html from committed .md (SPEC-HTML-STANDARD)."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDD = ROOT / "docs/features/spec-driven-development"
OUT = SDD / "spec-driven-development-reader.html"

PANELS: list[tuple[str, str, list[tuple[str, Path]]]] = [
    (
        "p-prd",
        "PRD",
        [("prd/spec-driven-development-prd.md", SDD / "prd/spec-driven-development-prd.md")],
    ),
    (
        "p-design",
        "Design (HLD)",
        [("design/spec-driven-development-design.md", SDD / "design/spec-driven-development-design.md")],
    ),
    (
        "p-impl",
        "Impl plan",
        [("impl-plan/spec-driven-development-impl-plan.md", SDD / "impl-plan/spec-driven-development-impl-plan.md")],
    ),
    (
        "p-test",
        "Test plan",
        [("test-plan/spec-driven-development-test-plan.md", SDD / "test-plan/spec-driven-development-test-plan.md")],
    ),
    (
        "p-dh",
        "Decision history",
        [
            (
                "decision-history/spec-driven-development-decision-history.md",
                SDD / "decision-history/spec-driven-development-decision-history.md",
            )
        ],
    ),
    (
        "c-pipeline",
        "Pipeline",
        [
            (
                "features/pipeline/design/pipeline-design.md",
                SDD / "features/pipeline/design/pipeline-design.md",
            )
        ],
    ),
    (
        "c-standard",
        "Document standard",
        [
            (
                "features/document-standard/design/document-standard-design.md",
                SDD / "features/document-standard/design/document-standard-design.md",
            ),
            (
                "features/document-standard/design/document-standard-design-spec-reader-html.md",
                SDD / "features/document-standard/design/document-standard-design-spec-reader-html.md",
            ),
            (
                "features/document-standard/prd/document-standard-prd-spec-reader-html.md",
                SDD / "features/document-standard/prd/document-standard-prd-spec-reader-html.md",
            ),
        ],
    ),
]


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def inline_md(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", s)
    return s


def md_to_html(md: str) -> str:
    md = strip_frontmatter(md)
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []
    list_type: str | None = None

    def close_list():
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    while i < len(lines):
        line = lines[i]

        if in_code:
            if line.strip().startswith("```"):
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                code_buf = []
                in_code = False
            else:
                code_buf.append(line)
            i += 1
            continue

        if line.strip().startswith("```"):
            close_list()
            in_code = True
            i += 1
            continue

        if re.match(r"^#{1,6}\s", line):
            close_list()
            level = len(line) - len(line.lstrip("#"))
            title = line.lstrip("#").strip()
            tag = f"h{min(level + 1, 6)}" if level > 1 else "h2"
            if level == 1:
                tag = "h2"
            out.append(f"<{tag}>{inline_md(title)}</{tag}>")
            i += 1
            continue

        if line.strip() == "---":
            close_list()
            out.append("<hr>")
            i += 1
            continue

        if line.startswith("|") and "|" in line[1:]:
            close_list()
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            if len(table_lines) < 2:
                out.append(f"<p>{inline_md(line)}</p>")
                continue
            header = [c.strip() for c in table_lines[0].strip("|").split("|")]
            body_rows = table_lines[2:] if len(table_lines) > 1 and re.match(r"^\|[\s\-:|]+\|$", table_lines[1]) else table_lines[1:]
            out.append("<table><thead><tr>")
            for c in header:
                out.append(f"<th>{inline_md(c)}</th>")
            out.append("</tr></thead><tbody>")
            for row in body_rows:
                cells = [c.strip() for c in row.strip("|").split("|")]
                out.append("<tr>")
                for c in cells:
                    out.append(f"<td>{inline_md(c)}</td>")
                out.append("</tr>")
            out.append("</tbody></table>")
            continue

        if re.match(r"^>\s?", line):
            close_list()
            bq = []
            while i < len(lines) and re.match(r"^>\s?", lines[i]):
                bq.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote><p>{inline_md(' '.join(bq))}</p></blockquote>")
            continue

        m_ul = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        m_ol = re.match(r"^(\s*)\d+\.\s+(.*)$", line)
        if m_ul:
            if list_type != "ul":
                close_list()
                out.append("<ul>")
                list_type = "ul"
            out.append(f"<li>{inline_md(m_ul.group(2))}</li>")
            i += 1
            continue
        if m_ol:
            if list_type != "ol":
                close_list()
                out.append("<ol>")
                list_type = "ol"
            out.append(f"<li>{inline_md(m_ol.group(2))}</li>")
            i += 1
            continue

        if not line.strip():
            close_list()
            i += 1
            continue

        close_list()
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith("|") and not lines[i].startswith("```") and not re.match(r"^>\s?", lines[i]) and not re.match(r"^[-*]\s+", lines[i]) and not re.match(r"^\d+\.\s+", lines[i]):
            para_lines.append(lines[i])
            i += 1
        out.append(f"<p>{inline_md(' '.join(para_lines))}</p>")

    close_list()
    if in_code and code_buf:
        out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    return "\n".join(out)


def panel_html(panel_id: str, title: str, sources: list[tuple[str, Path]]) -> str:
    parts = [f'<article id="{panel_id}" class="panel{" active" if panel_id == "p-prd" else ""}">']
    parts.append(f'<p class="panel-label">{html.escape(title)}</p>')
    parts.append('<div class="md-body">')
    for idx, (rel, path) in enumerate(sources):
        text = path.read_text(encoding="utf-8")
        if idx > 0:
            parts.append(f'<hr><p class="src-inline">Source: <code>{html.escape(rel)}</code></p>')
        parts.append(md_to_html(text))
    parts.append("</div>")
    canon = " · ".join(f"<code>{html.escape(r)}</code>" for r, _ in sources)
    parts.append(f'<p class="src">Canonical: {canon}</p>')
    parts.append("</article>")
    return "\n".join(parts)


CSS_EXTRA = """
.panel-label{font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--orange);margin:0 0 8px}
.md-body h2{font-size:21px;margin:24px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
.md-body h3{font-size:16px;margin:18px 0 8px}
.md-body h4{font-size:14.5px;margin:14px 0 6px;color:var(--muted)}
.md-body pre{background:var(--code);border:1px solid var(--line);border-radius:8px;padding:12px 14px;overflow-x:auto;font-size:12px;line-height:1.45;max-width:100%}
.md-body blockquote{margin:12px 0;padding:8px 14px;border-left:3px solid var(--line);color:var(--muted);background:var(--surface-2);border-radius:0 8px 8px 0}
.src-inline{font-family:var(--mono);font-size:10.5px;color:var(--subtle);margin:20px 0 8px}
"""

SHELL_HEAD = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Spec-Driven Development — Human Reader</title>
<style>
:root{
  --bg:#F6F7F4;--surface:#fff;--surface-2:#EEF1F0;--ink:#14202B;--muted:#55636F;--subtle:#7C8A96;
  --line:#DCE2E6;--code:#F1F3F1;--navy:#102D46;--navy-2:#173B5C;
  --yellow:#F2C94C;--green:#5F8D4E;--orange:#D98A3A;--red:#B95547;
  --soft-yellow:#FCF5DA;--soft-green:#EDF4E9;--soft-orange:#FBF0E4;--soft-red:#F8EBE9;--soft-blue:#E8F0F6;
  --serif:Georgia,'Times New Roman','Noto Serif CJK SC',serif;
  --sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang SC','Microsoft YaHei',sans-serif;
  --mono:'SF Mono','JetBrains Mono',Menlo,Consolas,monospace;
}
[data-theme="dark"]{
  --bg:#0B1824;--surface:#102434;--surface-2:#163044;--ink:#EAF0F4;--muted:#A9B8C4;--subtle:#7F93A3;
  --line:#22394C;--code:#0E2130;--navy:#08131C;--navy-2:#0E2130;
  --soft-yellow:#3A3418;--soft-green:#1B3222;--soft-orange:#3A2A1A;--soft-red:#3A2020;--soft-blue:#122A3D;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15.5px;line-height:1.65}
a{color:var(--orange);text-decoration:none}a:hover{text-decoration:underline}
code{font-family:var(--mono);font-size:.88em;background:var(--code);border:1px solid var(--line);padding:1.5px 6px;border-radius:4px}
.top{position:sticky;top:0;z-index:50;background:var(--navy);color:#DCE7EF;display:flex;align-items:center;justify-content:space-between;padding:12px 28px;gap:16px}
.crumbs{font-family:var(--mono);font-size:11px;color:#9CB0C0;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.crumbs a{color:#DCE7EF}.crumbs a:hover{color:var(--yellow)}
.theme-btn{display:inline-flex;align-items:center;gap:6px;padding:5px 10px;border:1px solid rgba(255,255,255,.18);background:transparent;color:#C4D3DE;border-radius:999px;font-family:var(--mono);font-size:10.5px;cursor:pointer}
.wrap{max-width:1040px;margin:0 auto;padding:32px 56px 80px}
.hero{padding-bottom:20px;margin-bottom:16px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--orange)}
h1{font-family:var(--serif);font-size:clamp(28px,3.2vw,40px);line-height:1.12;margin:8px 0 10px}
.deck{font-size:16px;color:var(--muted);max-width:78ch;margin:0 0 12px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.chip{font-family:var(--mono);font-size:10.5px;color:var(--muted);background:var(--surface);border:1px solid var(--line);padding:3px 9px;border-radius:999px}
.chip b{color:var(--ink)}
.tabgroups{margin:16px 0 24px}
.tabgroup-label{font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--subtle);margin:12px 0 6px}
.tabs{display:flex;flex-wrap:wrap;gap:8px}
.tabs button{font-family:var(--mono);font-size:11px;padding:7px 14px;border:1px solid var(--line);background:var(--surface);border-radius:999px;color:var(--muted);cursor:pointer}
.tabs button.active{border-color:var(--orange);color:var(--orange);background:var(--soft-orange)}
.panel{display:none}.panel.active{display:block}
table{width:100%;border-collapse:collapse;margin:14px 0 20px;font-size:13.5px;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--subtle);background:var(--surface-2)}
tr:last-child td{border-bottom:0}
.callout{background:var(--soft-blue);border:1px solid var(--line);border-left:4px solid var(--navy-2);border-radius:0 10px 10px 0;padding:12px 16px;margin:16px 0;font-size:14px;max-width:82ch}
.src{font-family:var(--mono);font-size:10.5px;color:var(--subtle);margin-top:28px;padding-top:12px;border-top:1px dashed var(--line)}
.foot{margin-top:40px;font-family:var(--mono);font-size:10.5px;color:var(--subtle)}
@media(max-width:700px){.wrap{padding:24px 18px 60px}}
"""

SHELL_MID = """
</style>
</head>
<body>
<div class="top">
  <div class="crumbs"><a href="../../index.html">The Super Lab</a><span>/</span><a href="spec-driven-development.html">SDD</a><span>/</span><span>Reader</span></div>
  <button class="theme-btn" type="button" onclick="document.documentElement.dataset.theme=document.documentElement.dataset.theme==='dark'?'light':'dark'">theme</button>
</div>
<div class="wrap">
  <header class="hero">
    <span class="eyebrow">Human-readable spec · SPEC-HTML-STANDARD</span>
    <h1>Spec-Driven Development</h1>
    <p class="deck">本页由 committed <code>.md</code> <strong>高保真汇编</strong>（L1 表格/ID/MUST 保留，富 HTML 排版）。改规范请先改 Markdown，再运行 <code>tools/build_sdd_reader.py</code> 或按同一标准手更。</p>
    <div class="chips">
      <span class="chip">parent <b>5 文稿</b></span>
      <span class="chip">children <b>pipeline · document-standard (+ DSGN-N aspect)</b></span>
      <span class="chip">norm <b>skills/spec-html-standard/SPEC-HTML-STANDARD.md</b></span>
    </div>
    <div class="callout"><p><strong>保真：</strong> 非 Markdown 预览；非 executive summary。Document standard Tab 含主 design + spec reader HTML 的 aspect PRD/design。</p></div>
  </header>

  <div class="tabgroups">
    <div class="tabgroup-label">Parent · spec-driven-development</div>
    <div class="tabs" data-group="parent">
      <button type="button" class="active" data-panel="p-prd">PRD</button>
      <button type="button" data-panel="p-design">Design (HLD)</button>
      <button type="button" data-panel="p-impl">Impl plan</button>
      <button type="button" data-panel="p-test">Test plan</button>
      <button type="button" data-panel="p-dh">Decision history</button>
    </div>
    <div class="tabgroup-label">Child sub-features</div>
    <div class="tabs" data-group="child">
      <button type="button" data-panel="c-pipeline">Pipeline</button>
      <button type="button" data-panel="c-standard">Document standard</button>
    </div>
  </div>
"""

SHELL_TAIL = """
  <p class="foot">SDD Human Reader · assembled from canonical .md · not source of truth</p>
</div>
<script>
document.querySelectorAll('.tabs button').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.panel).classList.add('active');
  });
});
</script>
</body>
</html>
"""


def main() -> None:
    panels = "\n\n".join(panel_html(pid, title, [(r, p) for r, p in srcs]) for pid, title, srcs in PANELS)
    css = SHELL_HEAD + CSS_EXTRA + SHELL_MID + panels + SHELL_TAIL
    OUT.write_text(css, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
