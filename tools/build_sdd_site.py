#!/usr/bin/env python3
"""Build a paginated, tree-navigated docs site for the SDD spec set."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_sdd_reader import SDD, md_to_html  # noqa: E402

OUT = SDD / "site"
ASSETS = OUT / "assets"

DOCS = [
    {
        "slug": "sdd-prd",
        "file": "sdd-prd.html",
        "title": "PRD",
        "eyebrow": "Parent · spec-driven-development",
        "crumbs": ["Spec-driven development"],
        "desc": "Problem, scope, functional requirements, and out-of-scope.",
        "related": ["sdd-design", "sdd-skill-contracts", "sdd-impl-plan", "sdd-test-plan", "sdd-decision-history"],
        "source": ("prd/spec-driven-development-prd.md", SDD / "prd/spec-driven-development-prd.md"),
    },
    {
        "slug": "sdd-design",
        "file": "sdd-design.html",
        "title": "Design (HLD)",
        "eyebrow": "Parent · spec-driven-development",
        "crumbs": ["Spec-driven development"],
        "desc": "System context, artifact loop, peer/sub tree, and review completeness.",
        "related": ["sdd-prd", "sdd-skill-contracts", "pipeline-design", "ds-design", "sdd-impl-plan", "sdd-test-plan"],
        "source": ("design/spec-driven-development-design.md", SDD / "design/spec-driven-development-design.md"),
    },
    {
        "slug": "sdd-skill-contracts",
        "file": "sdd-skill-contracts.html",
        "title": "Design (Skill contracts)",
        "eyebrow": "Parent · spec-driven-development",
        "crumbs": ["Spec-driven development"],
        "desc": "Inputs, outputs, and boundaries for the four skills.",
        "related": ["sdd-design", "pipeline-design", "ds-design"],
        "source": (
            "design/spec-driven-development-design-skill-contracts.md",
            SDD / "design/spec-driven-development-design-skill-contracts.md",
        ),
    },
    {
        "slug": "sdd-impl-plan",
        "file": "sdd-impl-plan.html",
        "title": "Implementation plan",
        "eyebrow": "Parent · spec-driven-development",
        "crumbs": ["Spec-driven development"],
        "desc": "IMPL-A–O: migration, skills, eval, checkers, reader.",
        "related": ["sdd-prd", "sdd-design", "sdd-test-plan"],
        "source": ("impl-plan/spec-driven-development-impl-plan.md", SDD / "impl-plan/spec-driven-development-impl-plan.md"),
    },
    {
        "slug": "sdd-test-plan",
        "file": "sdd-test-plan.html",
        "title": "Test plan",
        "eyebrow": "Parent · spec-driven-development",
        "crumbs": ["Spec-driven development"],
        "desc": "TST-A–S, scoring, gates, and the Unverified list.",
        "related": ["sdd-design", "sdd-impl-plan", "sdd-decision-history"],
        "source": ("test-plan/spec-driven-development-test-plan.md", SDD / "test-plan/spec-driven-development-test-plan.md"),
    },
    {
        "slug": "sdd-decision-history",
        "file": "sdd-decision-history.html",
        "title": "Decision history",
        "eyebrow": "Parent · spec-driven-development",
        "crumbs": ["Spec-driven development"],
        "desc": "ARD-A–AI: what was decided, why, and what changed.",
        "related": ["sdd-prd", "sdd-design", "sdd-test-plan"],
        "source": (
            "decision-history/spec-driven-development-decision-history.md",
            SDD / "decision-history/spec-driven-development-decision-history.md",
        ),
    },
    {
        "slug": "pipeline-design",
        "file": "pipeline-design.html",
        "title": "Design",
        "related_label": "Pipeline design",
        "eyebrow": "Child · pipeline",
        "crumbs": ["Spec-driven development", "Children", "Pipeline"],
        "desc": "Create, Map, Converge, Downstream; PIPE-A–L.",
        "related": ["sdd-design", "ds-design"],
        "source": (
            "features/pipeline/design/pipeline-design.md",
            SDD / "features/pipeline/design/pipeline-design.md",
        ),
    },
    {
        "slug": "ds-prd",
        "file": "ds-prd.html",
        "title": "PRD — spec reader HTML",
        "related_label": "Document standard PRD",
        "eyebrow": "Child · document-standard",
        "crumbs": ["Spec-driven development", "Children", "Document standard"],
        "desc": "Spec reader HTML: fidelity, coverage, canonical links.",
        "related": ["ds-design", "ds-design-aspect"],
        "source": (
            "features/document-standard/prd/document-standard-prd-spec-reader-html.md",
            SDD / "features/document-standard/prd/document-standard-prd-spec-reader-html.md",
        ),
    },
    {
        "slug": "ds-design",
        "file": "ds-design.html",
        "title": "Design",
        "related_label": "Document standard design",
        "eyebrow": "Child · document-standard",
        "crumbs": ["Spec-driven development", "Children", "Document standard"],
        "desc": "Types, paths, IDs, quality gates, and enforcement.",
        "related": ["ds-prd", "ds-design-aspect", "pipeline-design"],
        "source": (
            "features/document-standard/design/document-standard-design.md",
            SDD / "features/document-standard/design/document-standard-design.md",
        ),
    },
    {
        "slug": "ds-design-aspect",
        "file": "ds-design-aspect.html",
        "title": "Design — spec reader HTML",
        "related_label": "Document standard design — spec reader HTML",
        "eyebrow": "Child · document-standard",
        "crumbs": ["Spec-driven development", "Children", "Document standard"],
        "desc": "Spec reader HTML fidelity and assembly rules.",
        "related": ["ds-prd", "ds-design"],
        "source": (
            "features/document-standard/design/document-standard-design-spec-reader-html.md",
            SDD / "features/document-standard/design/document-standard-design-spec-reader-html.md",
        ),
    },
    {
        "slug": "sf-prd",
        "file": "sf-prd.html",
        "title": "PRD",
        "eyebrow": "Peer · skill-factory",
        "crumbs": ["Skill factory"],
        "desc": "Skill factory problem, goals, and requirements.",
        "related": ["sf-design", "sf-impl-plan", "sf-test-plan", "sf-decision-history"],
        "source": (".", Path("docs/features/skill-factory/prd/skill-factory-prd.md")),
    },
    {
        "slug": "sf-design",
        "file": "sf-design.html",
        "title": "Design",
        "eyebrow": "Peer · skill-factory",
        "crumbs": ["Skill factory"],
        "desc": "Skill factory architecture and contracts.",
        "related": ["sf-prd", "sf-impl-plan", "sf-test-plan"],
        "source": (".", Path("docs/features/skill-factory/design/skill-factory-design.md")),
    },
    {
        "slug": "sf-impl-plan",
        "file": "sf-impl-plan.html",
        "title": "Implementation plan",
        "eyebrow": "Peer · skill-factory",
        "crumbs": ["Skill factory"],
        "desc": "Skill factory implementation order.",
        "related": ["sf-prd", "sf-design", "sf-test-plan"],
        "source": (".", Path("docs/features/skill-factory/impl-plan/skill-factory-impl-plan.md")),
    },
    {
        "slug": "sf-test-plan",
        "file": "sf-test-plan.html",
        "title": "Test plan",
        "eyebrow": "Peer · skill-factory",
        "crumbs": ["Skill factory"],
        "desc": "Skill factory verification.",
        "related": ["sf-design", "sf-impl-plan", "sf-decision-history"],
        "source": (".", Path("docs/features/skill-factory/test-plan/skill-factory-test-plan.md")),
    },
    {
        "slug": "sf-decision-history",
        "file": "sf-decision-history.html",
        "title": "Decision history",
        "eyebrow": "Peer · skill-factory",
        "crumbs": ["Skill factory"],
        "desc": "Skill factory decisions and evidence.",
        "related": ["sf-prd", "sf-design", "sf-test-plan"],
        "source": (".", Path("docs/features/skill-factory/decision-history/skill-factory-decision-history.md")),
    },
]

# Resolve peer paths against the repo root; keep parent/child paths absolute.
for doc in DOCS:
    rel, path = doc["source"]
    if not path.is_absolute():
        doc["source"] = (rel, ROOT / path)

ORDER = [d["slug"] for d in DOCS]
BY_SLUG = {d["slug"]: d for d in DOCS}
NUM = {slug: f"{i + 1:02d}" for i, slug in enumerate(ORDER)}

PARENT_SLUGS = ["sdd-prd", "sdd-design", "sdd-skill-contracts", "sdd-impl-plan", "sdd-test-plan", "sdd-decision-history"]
CHILD_SLUGS = ["pipeline-design", "ds-prd", "ds-design", "ds-design-aspect"]
PEER_SLUGS = ["sf-prd", "sf-design", "sf-impl-plan", "sf-test-plan", "sf-decision-history"]

TREE = [
    {
        "label": "Spec-driven development",
        "children": [
            {"slug": "sdd-prd"},
            {"slug": "sdd-design"},
            {"slug": "sdd-skill-contracts"},
            {"slug": "sdd-impl-plan"},
            {"slug": "sdd-test-plan"},
            {"slug": "sdd-decision-history"},
            {
                "label": "Children",
                "children": [
                    {"label": "Pipeline", "children": [{"slug": "pipeline-design"}]},
                    {
                        "label": "Document standard",
                        "children": [
                            {"slug": "ds-prd"},
                            {"slug": "ds-design"},
                            {"slug": "ds-design-aspect"},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "label": "Skill factory",
        "children": [
            {"slug": "sf-prd"},
            {"slug": "sf-design"},
            {"slug": "sf-impl-plan"},
            {"slug": "sf-test-plan"},
            {"slug": "sf-decision-history"},
        ],
    },
]

# Single theme: Google Cloud docs (devsite) design language.
# Tokens extracted from https://cloud.google.com clouddocs app.css (2026-11).
FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css?'
    "family=Google+Sans:400,500"
    "|Roboto:400,400italic,500,500italic,700"
    "|Roboto+Mono:400,500,700"
    "|Noto+Sans+SC:400,500,700"
    '&display=swap">'
)


def render_source(rel: str, path: Path) -> str:
    body = md_to_html(path.read_text(encoding="utf-8"))
    return re.sub(r"(<table>.*?</table>)", r'<div class="table-wrap">\1</div>', body, flags=re.S)


def head(title: str) -> str:
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{FONT_LINK}
<link rel="stylesheet" href="assets/styles.css">
</head>'''


def topbar() -> str:
    return '''<header class="topbar">
  <div class="topbar-inner">
    <div class="brand"><a href="index.html"><span class="brand-mark">SDD</span><span class="brand-name">Spec Atlas</span></a></div>
  </div>
</header>'''


def render_tree(nodes: list[dict], current: str) -> str:
    parts = ['<ul class="tree">']
    for node in nodes:
        if "slug" in node:
            doc = BY_SLUG[node["slug"]]
            current_attr = ' aria-current="page"' if node["slug"] == current else ""
            parts.append(
                f'<li class="tree-leaf"><a class="tree-link" href="{doc["file"]}"{current_attr}>'
                f'<span class="tree-link__num">{NUM[node["slug"]]}</span>{html.escape(doc["title"])}</a></li>'
            )
        else:
            parts.append(
                f'<li class="tree-branch"><details open><summary>{html.escape(node["label"])}</summary>'
                f'{render_tree(node["children"], current)}</details></li>'
            )
    parts.append("</ul>")
    return "".join(parts)


def sidebar(current: str) -> str:
    overview_attr = ' aria-current="page"' if current == "overview" else ""
    return f'''<aside class="sidebar">
  <details class="tree-drawer" open>
    <summary>Browse the spec tree</summary>
    <nav aria-label="Spec tree">
      <div class="tree-overview"><a class="tree-link" href="index.html"{overview_attr}><span class="tree-link__num">00</span>Overview</a></div>
      {render_tree(TREE, current)}
    </nav>
  </details>
</aside>'''


def breadcrumbs(doc: dict) -> str:
    parts = ['<a href="index.html">Docs</a>']
    parts.extend(f"<span>{html.escape(label)}</span>" for label in doc["crumbs"])
    parts.append(f"<span>{html.escape(doc['title'])}</span>")
    return '<nav class="breadcrumbs">' + " / ".join(parts) + "</nav>"


def related(doc: dict) -> str:
    if not doc["related"]:
        return ""
    links = "".join(
        f'<a href="{BY_SLUG[slug]["file"]}">{html.escape(BY_SLUG[slug].get("related_label", BY_SLUG[slug]["title"]))}</a>'
        for slug in doc["related"]
    )
    return f'<nav class="related" aria-label="Related pages"><span class="related__label">Related</span>{links}</nav>'


def pager(slug: str) -> str:
    idx = ORDER.index(slug)
    prev_slug = ORDER[idx - 1] if idx > 0 else None
    next_slug = ORDER[idx + 1] if idx + 1 < len(ORDER) else None
    parts = ['<nav class="pager" aria-label="Previous and next">']
    if prev_slug:
        d = BY_SLUG[prev_slug]
        parts.append(f'<a class="prev" href="{d["file"]}"><span class="label">Previous</span>{html.escape(d["title"])}</a>')
    else:
        parts.append("<span></span>")
    if next_slug:
        d = BY_SLUG[next_slug]
        parts.append(f'<a class="next" href="{d["file"]}"><span class="label">Next</span>{html.escape(d["title"])}</a>')
    parts.append("</nav>")
    return "".join(parts)


def apply_doc_transforms(slug: str, body: str) -> str:
    def callout(match: re.Match) -> str:
        inner = match.group(1)
        label = "UNVERIFIED" if "Unverified" in inner or "UNKNOWN" in inner else "NOTE"
        return f'<blockquote class="callout" data-label="{label}">{inner}</blockquote>'

    body = re.sub(r"<blockquote>(.*?)</blockquote>", callout, body, flags=re.S)

    if slug == "sdd-prd":
        body = re.sub(
            r"<p><strong>(PRD-[A-Z]+)</strong>\s*—\s*(.*?)</p>",
            r'<div class="req"><span class="req-id">\1</span><span class="req-text">\2</span></div>',
            body,
            flags=re.S,
        )
    if slug == "ds-design":
        body = re.sub(
            r"<(h[45])>(DSGN-[A-Z]+)\s*—\s*(.*?)</\1>",
            lambda m: (
                f'<{m.group(1)} class="clause"><span class="clause-id">{m.group(2)}</span>'
                f'<span class="clause-title">{m.group(3)}</span></{m.group(1)}>'
            ),
            body,
        )
    if slug == "sdd-impl-plan":
        body = re.sub(
            r"<h3>(IMPL-[A-Z]+)\s*—\s*(.*?)</h3>",
            r'<h3 class="impl-step"><span class="impl-id">\1</span><span class="impl-title">\2</span></h3>',
            body,
        )
        body = body.replace("<p><strong>Goal:</strong>", '<p class="impl-goal"><strong>Goal:</strong>')
        body = body.replace("<p><strong>Steps:</strong>", '<p class="impl-steps"><strong>Steps:</strong>')
        body = body.replace("<p><strong>Verify:</strong>", '<p class="impl-verify"><strong>Verify:</strong>')
    if slug == "sdd-test-plan":
        parts = re.split(r"(?=<h[34]>)", body)
        body = "".join(
            f'<section class="test-card">{part}</section>' if re.match(r"<h4>TST-", part) else part
            for part in parts
        )
    return body


def site_title(doc: dict) -> str:
    context = doc["crumbs"][-1] if doc["crumbs"] else ""
    if context == "Spec-driven development":
        return f"{doc['title']} · Spec Atlas"
    return f"{doc['title']} · {context} · Spec Atlas"


def doc_page(doc: dict) -> str:
    rel, path = doc["source"]
    body = apply_doc_transforms(doc["slug"], render_source(rel, path))
    return f'''{head(site_title(doc))}
<body>
{topbar()}
<div class="site">
  {sidebar(doc["slug"])}
  <main class="content">
    {breadcrumbs(doc)}
    <article class="doc" data-doc="{doc['slug']}">
      <header class="doc-head">
        <p class="eyebrow">{html.escape(doc["eyebrow"])}</p>
        <h1>{html.escape(doc["title"])}</h1>
        <p class="source">Canonical: {html.escape(rel)}</p>
      </header>
      {related(doc)}
      <div class="doc-body">
        {body}
      </div>
    </article>
    {pager(doc["slug"])}
  </main>
</div>
<footer class="foot"><div class="foot-inner">Assembled from committed <code>.md</code>. The Markdown is authoritative; this page is a reading view.</div></footer>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>if(window.mermaid){{mermaid.initialize({{startOnLoad:false}});}}</script>
<script src="assets/app.js"></script>
</body>
</html>'''


def doc_card(doc: dict) -> str:
    return f'''<a class="doc-card" href="{doc["file"]}">
  <span class="doc-card__meta">{NUM[doc["slug"]]} · {html.escape(doc["eyebrow"])}</span>
  <span class="doc-card__title">{html.escape(doc["title"])}</span>
  <span class="doc-card__desc">{html.escape(doc["desc"])}</span>
  <span class="doc-card__arrow">Read</span>
</a>'''


def doc_group(title: str, slugs: list[str]) -> str:
    cards = "".join(doc_card(BY_SLUG[slug]) for slug in slugs)
    return f'''<section class="doc-group">
  <div class="doc-group__head"><h3 class="doc-group__title">{html.escape(title)}</h3><span class="doc-group__count">{len(slugs)} pages</span></div>
  <div class="doc-grid">{cards}</div>
</section>'''


def index_page() -> str:
    return f'''{head("Spec Atlas")}
<body>
{topbar()}
<div class="site">
  {sidebar("overview")}
  <main class="content">
    <section class="hero">
      <p class="eyebrow">Spec-driven development · complete spec</p>
      <h1>The spec, page by page.</h1>
      <p class="deck">One page per document, a tree that mirrors the feature hierarchy, and links between related docs. The Markdown under docs/features/ stays the source of truth; this site is a reading view.</p>
      <div class="hero-chips">
        <span class="chip">15 documents</span>
        <span class="chip">Parent · children · peer</span>
        <span class="chip">source: docs/features</span>
      </div>
    </section>

    <section class="doc-index" aria-labelledby="docs-title">
      <div class="section-head">
        <p class="eyebrow">Browse the tree</p>
        <h2 id="docs-title">Parent, children, peer</h2>
        <p>The sidebar carries the full tree. These cards are the same map, grouped by level.</p>
      </div>
      {doc_group("Parent · spec-driven-development", PARENT_SLUGS)}
      {doc_group("Children · pipeline + document-standard", CHILD_SLUGS)}
      {doc_group("Peer · skill-factory", PEER_SLUGS)}
    </section>

    <section class="reading-note">
      <h2>How this site works</h2>
      <p>Each page is one committed document. Breadcrumbs show the tree path; the “Related” row links siblings and neighbours; the pager follows the reading order. The Markdown remains the source of truth.</p>
    </section>
  </main>
</div>
<footer class="foot"><div class="foot-inner">Assembled from committed <code>.md</code> under <code>docs/features/</code>. The Markdown is authoritative; this page is a reading view.</div></footer>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>if(window.mermaid){{mermaid.initialize({{startOnLoad:false}});}}</script>
<script src="assets/app.js"></script>
</body>
</html>'''


SITE_CSS = r"""
/* Google Cloud docs (devsite) theme — tokens from cloud.google.com clouddocs app.css */
:root {
  --bg: #ffffff;
  --bg-2: #f8f9fa;
  --bg-3: #f1f3f4;
  --fg: #202124;
  --muted: #5f6368;
  --subtle: #9aa0a6;
  --border: #dadce0;
  --border-2: #e8eaed;
  --link: #1a73e8;
  --link-hover: #1967d2;
  --blue-soft: #e8f0fe;
  --red: #d93025;
  --red-soft: #fce8e6;
  --code-bg: #f1f3f4;
  --code-fg: #37474f;
  --pre-bg: #283142;
  --pre-fg: #f1f3f4;
  --pre-link: #669df6;
  --font-display: "Google Sans", "Noto Sans SC", Roboto, Arial, sans-serif;
  --font-body: Roboto, "Noto Sans SC", Arial, sans-serif;
  --font-mono: "Roboto Mono", "Sarasa Mono SC", ui-monospace, monospace;
  --measure: 820px;
  --topbar-h: 52px;
  color-scheme: light;
}

* { box-sizing: border-box; }
html { scroll-behavior: auto; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.67;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
a { color: var(--link); text-decoration: none; text-underline-offset: .16em; }
a:hover { color: var(--link-hover); text-decoration: underline; }
:focus-visible { outline: 2px solid var(--link); outline-offset: 2px; }
button { font: inherit; }

/* top bar */
.topbar { position: sticky; top: 0; z-index: 50; background: var(--bg); border-bottom: 1px solid var(--border); }
.topbar-inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.brand a { display: inline-flex; align-items: center; gap: 8px; color: var(--fg); text-decoration: none; }
.brand a:hover { text-decoration: none; }
.brand-mark { color: var(--link); font-family: var(--font-display); font-weight: 500; font-size: 18px; letter-spacing: .2px; }
.brand-name { font-family: var(--font-display); font-size: 18px; font-weight: 500; color: var(--fg); }

/* layout: full-height left nav rail + content */
.site {
  max-width: 1440px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 272px minmax(0, 1fr);
  align-items: start;
  padding-bottom: 48px;
}
.sidebar {
  position: sticky;
  top: var(--topbar-h);
  height: calc(100vh - var(--topbar-h));
  overflow-y: auto;
  border-right: 1px solid var(--border);
  padding: 12px 8px 24px;
  scrollbar-width: thin;
}
.tree-drawer > summary { display: none; }
.tree-overview { margin-bottom: 6px; }
.tree, .tree ul { list-style: none; margin: 0; padding: 0; }
.tree ul { padding-left: 12px; }
.tree-leaf { margin: 0; }
.tree-link {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 7px 16px 7px 12px;
  border-radius: 0 20px 20px 0;
  color: var(--fg);
  text-decoration: none;
  font-size: 13.5px;
  line-height: 1.35;
}
.tree-link:hover { background: var(--bg-3); color: var(--fg); text-decoration: none; }
.tree-link[aria-current="page"] { background: var(--blue-soft); color: var(--link-hover); font-weight: 500; }
.tree-link__num { display: none; }
.tree-branch > details > summary {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px 6px 12px;
  cursor: pointer;
  list-style: none;
  color: var(--fg);
  font-family: var(--font-display);
  font-size: 13.5px;
  font-weight: 500;
}
.tree-branch > details > summary::-webkit-details-marker { display: none; }
.tree-branch > details > summary::before { content: "▾"; color: var(--muted); font-size: 11px; }
.tree-branch > details:not([open]) > summary::before { content: "▸"; }
.tree-branch > details > summary:hover { color: var(--link-hover); }

/* content column */
.content { min-width: 0; padding: 20px 40px 0; }
.breadcrumbs { margin: 0 0 12px; font-size: 12px; color: var(--muted); }
.breadcrumbs a { color: var(--muted); text-decoration: none; }
.breadcrumbs a:hover { color: var(--link-hover); }

/* index hero */
.hero { padding: 36px 0 24px; max-width: 860px; }
.hero h1 {
  margin: 0 0 12px;
  font-family: var(--font-display);
  font-size: clamp(30px, 4vw, 40px);
  font-weight: 400;
  line-height: 1.2;
  color: var(--fg);
}
.hero .deck { margin: 0; max-width: 64ch; color: var(--muted); font-size: 16px; line-height: 1.6; }
.eyebrow { margin: 0 0 6px; font-size: 12px; font-weight: 500; color: var(--muted); }
.hero-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
.chip { border: 1px solid var(--border); border-radius: 4px; padding: 4px 10px; background: var(--bg-2); color: var(--muted); font-size: 12px; }

.section-head { max-width: 720px; margin-bottom: 14px; }
.section-head h2 { margin: 0 0 8px; font-family: var(--font-display); font-size: 22px; font-weight: 400; line-height: 1.3; }
.section-head p:last-child { margin: 0; color: var(--muted); font-size: 14px; }

/* doc index cards */
.doc-index { padding: 8px 0 0; }
.doc-group { margin-top: 24px; }
.doc-group__head { display: flex; align-items: baseline; gap: 10px; margin-bottom: 12px; }
.doc-group__title { margin: 0; font-family: var(--font-display); font-size: 18px; font-weight: 500; }
.doc-group__count { font-size: 12px; color: var(--muted); }
.doc-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px; }
.doc-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
  padding: 16px;
  background: var(--bg);
  color: var(--fg);
  border: 1px solid var(--border);
  border-radius: 8px;
  text-decoration: none;
  transition: box-shadow .15s ease, border-color .15s ease;
}
.doc-card:hover {
  color: var(--fg);
  text-decoration: none;
  border-color: transparent;
  box-shadow: 0 1px 2px rgba(60, 64, 67, .3), 0 1px 3px 1px rgba(60, 64, 67, .15);
}
.doc-card__meta { font-size: 12px; color: var(--muted); }
.doc-card__title { font-family: var(--font-display); font-size: 16px; font-weight: 500; line-height: 1.35; }
.doc-card__desc { color: var(--muted); font-size: 13.5px; line-height: 1.5; }
.doc-card__arrow { margin-top: auto; padding-top: 8px; color: var(--link); font-size: 13px; font-weight: 500; }
.doc-card:hover .doc-card__arrow { text-decoration: underline; }

.reading-note { max-width: var(--measure); padding: 20px 0 0; border-top: 1px solid var(--border); }
.reading-note h2 { margin: 0 0 8px; font-family: var(--font-display); font-size: 18px; font-weight: 500; }
.reading-note p { margin: 0; color: var(--muted); font-size: 14px; }

/* article */
.doc { min-width: 0; background: var(--bg); }
.doc-head { margin-bottom: 18px; padding-bottom: 18px; border-bottom: 1px solid var(--border); }
.doc-head h1 {
  margin: 2px 0 10px;
  font-family: var(--font-display);
  font-size: clamp(28px, 3.2vw, 36px);
  font-weight: 400;
  line-height: 1.25;
  color: var(--fg);
}
.doc-head .source { margin: 0; font-family: var(--font-mono); font-size: 12px; color: var(--muted); overflow-wrap: anywhere; }
.related { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 0 0 24px; }
.related__label { margin-right: 4px; color: var(--muted); font-size: 12px; font-weight: 500; }
.related a {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 4px 10px;
  background: var(--bg);
  color: var(--fg);
  text-decoration: none;
  font-size: 12.5px;
}
.related a:hover { background: var(--bg-3); color: var(--fg); text-decoration: none; }

/* article body — devsite type scale */
.doc-body { max-width: var(--measure); min-width: 0; }
.doc-body > h2:first-child { margin-top: 0; }
.doc-body h2 {
  margin: 32px 0 12px;
  font-family: var(--font-display);
  font-weight: 400;
  font-size: 24px;
  line-height: 32px;
  color: var(--fg);
}
.doc-body h3 {
  margin: 26px 0 10px;
  font-family: var(--font-display);
  font-weight: 400;
  font-size: 20px;
  line-height: 28px;
  color: var(--fg);
}
.doc-body h4 { margin: 20px 0 8px; font-family: var(--font-display); font-weight: 500; font-size: 16px; color: var(--fg); }
.doc-body p { margin: 0 0 12px; }
.doc-body ul, .doc-body ol { padding-left: 26px; margin: 0 0 12px; }
.doc-body li { margin: 4px 0; }
.doc-body li::marker { color: var(--fg); }
.doc-body strong { font-weight: 500; }
.doc-body hr { margin: 28px 0; border: 0; border-top: 1px solid var(--border-2); }

/* callouts — devsite aside note style */
.doc-body blockquote {
  margin: 16px 0;
  padding: 12px 16px;
  border: 0;
  border-radius: 8px;
  background: var(--blue-soft);
  color: var(--fg);
}
.doc-body blockquote.callout[data-label]::before {
  content: attr(data-label);
  display: block;
  margin-bottom: 4px;
  color: var(--link-hover);
  font-family: var(--font-display);
  font-size: 13.5px;
  font-weight: 500;
  letter-spacing: .3px;
}
.doc-body blockquote.callout[data-label="UNVERIFIED"] { background: var(--red-soft); }
.doc-body blockquote.callout[data-label="UNVERIFIED"]::before { color: var(--red); }
.doc-body blockquote p { margin: 0 0 4px; }
.doc-body blockquote p:last-child { margin-bottom: 0; }

/* code — devsite: light inline, dark block */
.doc-body code {
  padding: 1px 5px;
  border-radius: 4px;
  background: var(--code-bg);
  color: var(--code-fg);
  font-family: var(--font-mono);
  font-size: .9em;
  overflow-wrap: anywhere;
}
.doc-body pre {
  overflow-x: auto;
  margin: 16px 0;
  padding: 14px 16px;
  border: 0;
  border-radius: 8px;
  background: var(--pre-bg);
  color: var(--pre-fg);
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.6;
}
.doc-body pre a { color: var(--pre-link); }
.doc-body pre code { padding: 0; background: none; color: inherit; font-size: inherit; }
.doc-body pre.mermaid { text-align: center; background: var(--bg-2); color: var(--fg); border: 1px solid var(--border-2); }

/* tables — devsite reference tables */
.table-wrap { overflow-x: auto; margin: 16px 0; border: 1px solid var(--border); border-radius: 8px; }
.doc-body table { width: 100%; min-width: 560px; border-collapse: collapse; font-size: 13.5px; }
.doc-body th {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-2);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  color: var(--fg);
  text-align: left;
}
.doc-body td { padding: 10px 14px; border-bottom: 1px solid var(--border-2); vertical-align: top; text-align: left; }
.doc-body tbody tr:last-child td { border-bottom: 0; }

/* requirement / clause / impl rows — reference-style rows */
.req { display: grid; grid-template-columns: 76px 1fr; gap: 12px; padding: 8px 0; border-bottom: 1px solid var(--border-2); }
.req-id { font-family: var(--font-mono); font-size: 12.5px; color: var(--link-hover); padding-top: 2px; }
.doc-body h4.clause, .doc-body h5.clause { display: grid; grid-template-columns: 88px 1fr; gap: 10px; align-items: baseline; }
.clause-id { font-family: var(--font-mono); font-size: 12px; font-weight: 400; color: var(--link-hover); }
.doc-body h3.impl-step { display: grid; grid-template-columns: 76px 1fr; gap: 10px; align-items: baseline; }
.impl-id { font-family: var(--font-mono); font-size: 12px; font-weight: 400; color: var(--link-hover); }
.doc-body p.impl-goal,
.doc-body p.impl-steps,
.doc-body p.impl-verify { padding-left: 12px; border-left: 2px solid var(--border-2); }
.doc-body .test-card { border: 1px solid var(--border-2); border-radius: 8px; padding: 4px 16px; margin: 0 0 12px; }
.doc-body .test-card h4 { margin: 14px 0 6px; }

/* pager — devsite next/prev */
.pager { display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; margin-top: 40px; }
.pager a {
  flex: 1 1 240px;
  padding: 12px 18px;
  border-radius: 4px;
  color: var(--fg);
  text-decoration: none;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 500;
}
.pager a:hover { text-decoration: none; }
.pager .label { display: block; margin-bottom: 3px; font-family: var(--font-body); font-size: 11px; font-weight: 400; color: inherit; opacity: .8; }
.pager .prev { border: 1px solid var(--border); background: var(--bg); }
.pager .prev:hover { background: var(--bg-3); }
.pager .next { border: 1px solid var(--link); background: var(--link); color: #fff; text-align: right; }
.pager .next:hover { background: var(--link-hover); border-color: var(--link-hover); color: #fff; }

/* footer */
.foot { background: var(--bg-2); border-top: 1px solid var(--border); color: var(--muted); font-size: 12px; }
.foot-inner { max-width: 1440px; margin: 0 auto; padding: 18px 24px 32px; }
.foot code { color: var(--fg); font-family: var(--font-mono); background: none; padding: 0; }

@media (max-width: 900px) {
  .site { grid-template-columns: 1fr; }
  .sidebar { position: static; height: auto; border-right: 0; padding: 0 16px; }
  .tree-drawer { padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg); }
  .tree-drawer > summary { display: flex; align-items: center; gap: 8px; cursor: pointer; list-style: none; color: var(--fg); font-family: var(--font-display); font-size: 14px; font-weight: 500; }
  .tree-drawer > summary::-webkit-details-marker { display: none; }
  .tree-drawer > summary::before { content: "▸"; color: var(--muted); }
  .tree-drawer[open] > summary::before { content: "▾"; }
  .tree-drawer nav { margin-top: 10px; }
  .content { padding: 16px 16px 0; }
  .tree-link { border-radius: 4px; }
}
@media (max-width: 640px) {
  .topbar-inner { padding: 10px 16px; }
  .brand-name { display: none; }
  .hero { padding-top: 20px; }
  .pager a { flex: 1 1 100%; }
  .pager .next { text-align: left; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { transition-duration: .01ms !important; animation-duration: .01ms !important; }
}
"""

APP_JS = r"""
(function () {
  function renderMermaid() {
    if (!window.mermaid) return;
    document.querySelectorAll("pre.mermaid").forEach(function (el) {
      if (!el.dataset.src) el.dataset.src = el.textContent;
      el.removeAttribute("data-processed");
      el.textContent = el.dataset.src;
    });
    try {
      mermaid.initialize({ startOnLoad: false, theme: "neutral", securityLevel: "loose" });
      mermaid.run({ querySelector: "pre.mermaid" }).catch(function () {});
    } catch (e) {}
  }

  window.addEventListener("load", renderMermaid);
})();
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "styles.css").write_text(SITE_CSS, encoding="utf-8")
    (ASSETS / "app.js").write_text(APP_JS, encoding="utf-8")
    (OUT / "index.html").write_text(index_page(), encoding="utf-8")
    for doc in DOCS:
        (OUT / doc["file"]).write_text(doc_page(doc), encoding="utf-8")
    print(f"Wrote {OUT} ({len(DOCS) + 1} pages)")


if __name__ == "__main__":
    main()
