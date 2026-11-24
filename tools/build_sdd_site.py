#!/usr/bin/env python3
"""Build a paginated, tree-navigated docs site for the SDD spec set."""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_sdd_reader import SDD, inline_figures, md_to_html  # noqa: E402

FEATURES = ROOT / "docs/features"
OUT = ROOT / "docs/book/html"
ASSETS = OUT / "assets"

TYPE_RANK = {"prd": 0, "design": 1, "impl-plan": 2, "test-plan": 3, "decision-history": 4, "how-to": 5}
NAV_ORDER = ("prd", "decision-history", "design", "impl-plan", "test-plan", "how-to")
NAV_NUM = {"prd": "1", "decision-history": "2", "design": "3", "impl-plan": "4", "test-plan": "5", "how-to": "6"}


def _title(path: Path) -> str:
    body = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(?m)^#\s+(.+)$", body)
    return match.group(1).strip() if match else path.stem.replace("-", " ")


def _discover() -> list[dict]:
    found = []
    for path in FEATURES.rglob("*.md"):
        if path.name.startswith("._") or "raw" in path.parts or ".scratch" in path.parts or "pipeline" in path.parts:
            continue
        rel = path.relative_to(FEATURES)
        kind = next((part for part in rel.parts if part in TYPE_RANK), "other")
        found.append(
            {
                "slug": rel.with_suffix("").as_posix(),
                "file": rel.with_suffix(".html").as_posix(),
                "feature": rel.parts[0],
                "kind": kind,
                "title": _title(path),
                "eyebrow": rel.parts[0],
                "crumbs": list(rel.parts[:-1]),
                "desc": rel.as_posix(),
                "related": [],
                "source": (path.relative_to(ROOT).as_posix(), path),
            }
        )
    found.sort(key=lambda d: (d["feature"], TYPE_RANK.get(d["kind"], 9), d["file"]))
    return found


DOCS = _discover()


def rel_href(from_file: str, to_file: str) -> str:
    return Path(os.path.relpath(to_file, start=str(Path(from_file).parent))).as_posix()


ORDER = [d["slug"] for d in DOCS]
BY_SLUG = {d["slug"]: d for d in DOCS}
NUM = {slug: f"{i + 1:02d}" for i, slug in enumerate(ORDER)}
FEATURES_ORDER: list[str] = []
for _doc in DOCS:
    if _doc["feature"] not in FEATURES_ORDER:
        FEATURES_ORDER.append(_doc["feature"])


def feature_docs(feature: str) -> list[dict]:
    return [d for d in DOCS if d["feature"] == feature]


# diagram-design default skin tokens (style-guide.md)
FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Instrument+Serif:ital@0;1"
    "&family=Geist:wght@400;500;600"
    "&family=Geist+Mono:wght@400;500"
    "&family=Noto+Sans+SC:wght@400;500;700"
    "&family=Noto+Serif+SC:wght@400;600"
    '&display=swap">'
)


def _page_for(md_path: Path) -> Path:
    return OUT / md_path.resolve().relative_to(FEATURES.resolve()).with_suffix(".html")


def _retarget_links(body: str, md_path: Path, page: Path | None = None) -> str:
    """Links in the markdown are relative to the source file. Point them at the HTML page."""
    page = page or _page_for(md_path)

    def repl(match: re.Match) -> str:
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        path_part, _, frag = href.partition("#")
        if not path_part:
            return match.group(0)
        target = (md_path.parent / path_part).resolve()
        dest = target
        try:
            rel_feat = target.relative_to(FEATURES.resolve())
        except ValueError:
            rel_feat = None
        if rel_feat is not None and target.suffix == ".md" and (FEATURES / rel_feat).is_file() and not _omitted(rel_feat):
            dest = (OUT / rel_feat).with_suffix(".html")
        new = Path(os.path.relpath(dest, start=page.parent)).as_posix()
        if frag:
            new += "#" + frag
        return f'href="{new}"'

    return re.sub(r'href="([^"]*)"', repl, body)


_ID = r"(?:PRD|DSGN|ARD|IMPL|TST|PIPE|QUES)-[A-Z]+(?:-[A-Z]+)*"
_ID_RE = re.compile(rf"\b({_ID})\b")


def _scope(file: str) -> tuple[str, str]:
    parts = Path(file).parts
    if len(parts) > 2 and parts[1] == "features":
        return parts[0], parts[2]
    return parts[0], ""


def _index_ids() -> dict[tuple[str, str, str], str]:
    index: dict[tuple[str, str, str], str] = {}
    rank: dict[tuple[str, str, str], int] = {}
    patterns = (
        (0, re.compile(rf"^#{{1,6}}\s+({_ID})\b")),
        (1, re.compile(rf"^(?:[-*] \*\*|\*\*|\| \*\*)({_ID})\b")),
        (2, re.compile(rf"^\| ({_ID})\b")),
    )
    for doc in DOCS:
        parent, sub = _scope(doc["file"])
        for line in doc["source"][1].read_text(encoding="utf-8").splitlines():
            for pri, pattern in patterns:
                match = pattern.match(line)
                if not match:
                    continue
                key = (parent, sub, match.group(1))
                if key not in rank or pri < rank[key]:
                    rank[key] = pri
                    index[key] = doc["file"]
                break
    return index


ID_INDEX = _index_ids()


def _lookup_id(page_file: str, token: str) -> str | None:
    parent, sub = _scope(page_file)
    found = ID_INDEX.get((parent, sub, token))
    if found:
        return found
    if sub:
        return ID_INDEX.get((parent, "", token))
    return None


_NAME_INDEX: dict[str, list[Path]] | None = None


def _files_named(name: str) -> list[Path]:
    global _NAME_INDEX
    if _NAME_INDEX is None:
        index: dict[str, list[Path]] = {}

        def add(path: Path) -> None:
            if not path.name.startswith("._"):
                index.setdefault(path.name, []).append(path)

        for doc in DOCS:
            add(doc["source"][1])
        skills = ROOT / "skills"
        if skills.is_dir():
            for path in skills.rglob("*.md"):
                add(path)
        _NAME_INDEX = index
    return _NAME_INDEX.get(name, [])


_TRACKED: set[str] | None = None
_TRACKED_LOADED = False


def _tracked_files() -> set[str] | None:
    """Repo-relative paths git tracks or would track (not ignored), computed once; None without git."""
    global _TRACKED, _TRACKED_LOADED
    if not _TRACKED_LOADED:
        _TRACKED_LOADED = True
        try:
            out = subprocess.run(
                ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, check=True
            ).stdout.decode("utf-8", "replace")
            _TRACKED = {f for f in out.split("\0") if f}
        except (OSError, subprocess.CalledProcessError):
            _TRACKED = None
    return _TRACKED


def _linkable_file(rel: str) -> bool:
    """A local file earns a link only when tracked or untracked-but-not-ignored (gitignored files never publish)."""
    if not (ROOT / rel).is_file():
        return False
    tracked = _tracked_files()
    return tracked is None or rel in tracked


def _repo_rel(path: Path) -> str | None:
    norm = os.path.normpath(str(path))
    root = str(ROOT)
    if norm == root:
        return ""
    prefix = root + os.sep
    if not norm.startswith(prefix):
        return None
    return Path(norm[len(prefix) :]).as_posix()


_KNOWN_MD = {doc["source"][0]: OUT / doc["file"] for doc in DOCS}


def _dest_for_mention(raw: str, md_path: Path) -> Path | None:
    raw = html.unescape(raw).strip()
    if not raw or any(ch in raw for ch in "<>*| "):
        return None
    if raw.startswith(("http://", "https://", "mailto:")):
        return None
    looks_like_file = "/" in raw or raw.endswith((".md", ".html", ".py", ".yaml", ".yml", ".sh"))
    if not looks_like_file:
        return None
    rels: list[str] = []
    if raw.startswith(("./", "../")) or "/" in raw:
        rel = _repo_rel(md_path.parent / raw)
        if rel:
            rels.append(rel)
    if not raw.startswith(("/", ".", "..")):
        rels.append(raw.lstrip("/"))
    if raw.startswith("docs/features/") and raw.endswith(".html"):
        rels.append("docs/book/html/" + raw[len("docs/features/") :])
    if "/" not in raw and raw.endswith((".md", ".html")):
        hits = _files_named(Path(raw).name)
        if len(hits) == 1:
            rel = _repo_rel(hits[0])
            if rel:
                rels.append(rel)
    for rel in rels:
        if rel in _KNOWN_MD:
            return _KNOWN_MD[rel]
        if rel.startswith("docs/features/") and rel.endswith(".md"):
            continue
        if rel.startswith("docs/book/html/") and rel.endswith(".html"):
            return OUT / rel[len("docs/book/html/") :]
        if _linkable_file(rel):
            return ROOT / rel
    return None


def _stamp_ids(body: str, page_file: str) -> str:
    present = set(re.findall(r'id="([^"]+)"', body))

    def stamp(pattern: str, wrap) -> None:
        nonlocal body

        def repl(match: re.Match) -> str:
            token = match.group(1)
            if _lookup_id(page_file, token) != page_file or token in present:
                return match.group(0)
            present.add(token)
            return wrap(token)

        body = re.sub(pattern, repl, body)

    stamp(
        rf"<strong>({_ID})</strong>",
        lambda token: f'<strong id="{token}">{token}</strong>',
    )
    stamp(
        rf"<td>({_ID})</td>",
        lambda token: f'<td id="{token}">{token}</td>',
    )
    return body


def _linkify(body: str, md_path: Path, page_file: str) -> str:
    parts = re.split(r"(<[^>]+>)", body)
    skip = 0
    out: list[str] = []
    page_dir = (OUT / page_file).parent
    for part in parts:
        if part.startswith("<"):
            name = re.match(r"</?([a-zA-Z0-9]+)", part)
            if name:
                tag = name.group(1).lower()
                if part.startswith("</"):
                    if tag in {"a", "code", "pre"} and skip:
                        skip -= 1
                elif tag in {"a", "code", "pre"} and not part.endswith("/>"):
                    skip += 1
            out.append(part)
            continue
        if skip:
            out.append(part)
            continue

        def repl(match: re.Match) -> str:
            token = match.group(1)
            dest = _lookup_id(page_file, token)
            if not dest:
                return token
            href = f"#{token}" if dest == page_file else rel_href(page_file, dest) + f"#{token}"
            return f'<a class="id-ref" href="{href}">{token}</a>'

        out.append(_ID_RE.sub(repl, part))
    body = "".join(out)

    def code_repl(match: re.Match) -> str:
        dest = _dest_for_mention(match.group(1), md_path)
        if dest is None:
            return match.group(0)
        href = Path(os.path.relpath(dest, start=page_dir)).as_posix()
        return f'<a href="{html.escape(href, quote=True)}">{match.group(0)}</a>'

    return re.sub(r"<code>([^<]+)</code>", code_repl, body)


def render_source(rel: str, path: Path) -> str:
    body = _retarget_links(md_to_html(path.read_text(encoding="utf-8")), path)
    return re.sub(r"(<table>.*?</table>)", r'<div class="table-wrap">\1</div>', body, flags=re.S)


def feature_home(feature: str) -> dict:
    pages = feature_docs(feature)
    wanted = f"{feature}/prd/{feature}-prd.html"
    for doc in pages:
        if doc["file"] == wanted:
            return doc
    for doc in pages:
        if "/features/" not in doc["file"]:
            return doc
    return pages[0]


def head(title: str, from_file: str) -> str:
    css = rel_href(from_file, "assets/styles.css")
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{FONT_LINK}
<link rel="stylesheet" href="{css}">
</head>'''


def topbar(from_file: str) -> str:
    home = rel_href(from_file, "index.html")
    return f'''<header class="topbar">
  <div class="topbar-inner">
    <div class="brand"><a href="{home}"><span class="brand-mark">SDD</span><span class="brand-name">Spec Atlas</span></a></div>
    <button class="strike-btn" type="button" onclick="var r=document.documentElement;var off=r.dataset.strike!=='off';r.dataset.strike=off?'off':'on';this.textContent=off?'显示删除线':'隐藏删除线'">隐藏删除线</button>
  </div>
</header>'''


def render_tree(nodes: list[dict], current: str, from_file: str) -> str:
    parts = ['<ul class="tree">']
    for node in nodes:
        if "slug" in node:
            doc = BY_SLUG[node["slug"]]
            current_attr = ' aria-current="page"' if node["slug"] == current else ""
            parts.append(
                f'<li class="tree-leaf"><a class="tree-link" href="{rel_href(from_file, doc["file"])}"{current_attr}>'
                f'<span class="tree-link__num">{NUM[node["slug"]]}</span>{html.escape(doc["title"])}</a></li>'
            )
        else:
            parts.append(
                f'<li class="tree-branch"><details open><summary>{html.escape(node["label"])}</summary>'
                f'{render_tree(node["children"], current, from_file)}</details></li>'
            )
    parts.append("</ul>")
    return "".join(parts)


def _omitted(path: Path) -> bool:
    return "pipeline" in path.parts


def _is_entry(doc: dict) -> bool:
    kind = doc["kind"]
    return kind in TYPE_RANK and doc["file"] == f"{doc['feature']}/{kind}/{doc['feature']}-{kind}.html"


def _reader_doc(feature: str) -> dict | None:
    rel = f"{feature}/{feature}-reader.html"
    if not (OUT / rel).is_file():
        return None
    return {
        "slug": f"{feature}/reader",
        "file": rel,
        "feature": feature,
        "kind": "design",
        "title": f"{feature} — Reader",
    }


def _sub_name(file: str) -> str | None:
    parts = Path(file).parts
    if len(parts) > 2 and parts[1] == "features":
        return parts[2]
    return None


def _sub_home(pages: list[dict], name: str) -> dict:
    suffix = f"{name}/design/{name}-design.html"
    for doc in pages:
        if doc["file"].endswith(suffix):
            return doc
    return pages[0]


def _grouped(feature: str) -> tuple[dict[str, dict], dict[str, list[dict]], dict[str, list[dict]]]:
    entries: dict[str, dict] = {}
    children: dict[str, list[dict]] = {kind: [] for kind in TYPE_RANK}
    subs: dict[str, list[dict]] = {}
    for doc in feature_docs(feature):
        if _omitted(Path(doc["file"])):
            continue
        if _is_entry(doc):
            entries[doc["kind"]] = doc
            continue
        name = _sub_name(doc["file"])
        if name:
            subs.setdefault(name, []).append(doc)
            continue
        parent = doc["kind"] if doc["kind"] in children else "design"
        children[parent].append(doc)
    reader = _reader_doc(feature)
    if reader:
        children["design"].append(reader)
    return entries, children, subs


def _leaf(doc: dict, current: str, from_file: str, num: str = "") -> str:
    attr = ' aria-current="page"' if doc["slug"] == current else ""
    num_html = f'<span class="tree-ord">{html.escape(num)}</span>' if num else ""
    return (
        f'<li class="tree-leaf"><a class="tree-link" href="{rel_href(from_file, doc["file"])}"{attr}>'
        f'{num_html}{html.escape(doc["title"])}</a></li>'
    )


def _numbered_docs(pages: list[dict], current: str, from_file: str) -> str:
    by_kind: dict[str, list[dict]] = {}
    for doc in pages:
        kind = doc["kind"] if doc["kind"] in NAV_NUM else "design"
        by_kind.setdefault(kind, []).append(doc)
    chunks: list[str] = []
    for kind in NAV_ORDER:
        docs = by_kind.get(kind, [])
        if not docs:
            continue
        first, rest = docs[0], docs[1:]
        if rest:
            link = _leaf(first, current, from_file, NAV_NUM[kind]).removeprefix('<li class="tree-leaf">').removesuffix("</li>")
            inner = "".join(_leaf(doc, current, from_file) for doc in rest)
            chunks.append(
                f'<li class="tree-branch"><details open><summary>{link}</summary><ul class="tree">{inner}</ul></details></li>'
            )
        else:
            chunks.append(_leaf(first, current, from_file, NAV_NUM[kind]))
    return "".join(chunks)


def _sub_branch(name: str, pages: list[dict], current: str, from_file: str) -> str:
    home = _sub_home(pages, name)
    return (
        '<li class="tree-branch"><details open><summary>'
        f'<a class="tree-link" href="{rel_href(from_file, home["file"])}">{html.escape(name)}</a>'
        '</summary><ul class="tree">'
        + _numbered_docs(pages, current, from_file)
        + "</ul></details></li>"
    )


def _layer(kind: str, kids: list[dict], subs: dict[str, list[dict]], current: str, from_file: str) -> str:
    if kind != "design":
        return "".join(_leaf(doc, current, from_file) for doc in kids)
    readers = [doc for doc in kids if doc["slug"].endswith("/reader")]
    parts = [doc for doc in kids if doc not in readers]
    chunks = [_leaf(doc, current, from_file) for doc in parts]
    chunks.extend(_sub_branch(name, pages, current, from_file) for name, pages in subs.items())
    chunks.extend(_leaf(doc, current, from_file) for doc in readers)
    return "".join(chunks)


def _feature_tree(feature: str, current: str, from_file: str) -> str:
    entries, children, subs = _grouped(feature)
    parts = ['<ul class="tree">']
    for kind in NAV_ORDER:
        entry = entries.get(kind)
        kids = children[kind]
        if entry is None and not kids:
            continue
        inner = _layer(kind, kids, {}, current, from_file)
        num = NAV_NUM[kind]
        if entry is not None and inner:
            link = _leaf(entry, current, from_file, num).removeprefix('<li class="tree-leaf">').removesuffix("</li>")
            parts.append(
                f'<li class="tree-branch"><details open><summary>{link}</summary>'
                f'<ul class="tree">{inner}</ul></details></li>'
            )
        elif entry is not None:
            parts.append(_leaf(entry, current, from_file, num))
        else:
            parts.append(inner)
    if subs:
        inner = "".join(_sub_branch(name, pages, current, from_file) for name, pages in subs.items())
        parts.append(
            '<li class="tree-branch"><details open><summary>'
            '<span class="tree-link"><span class="tree-ord">10</span>sub-feature</span>'
            f'</summary><ul class="tree">{inner}</ul></details></li>'
        )
    parts.append("</ul>")
    return "".join(parts)


def _reading_order(feature: str) -> list[dict]:
    entries, children, subs = _grouped(feature)
    order = []
    for kind in NAV_ORDER:
        if kind in entries:
            order.append(entries[kind])
        order.extend(doc for doc in children[kind] if doc["slug"] in BY_SLUG)
    for pages in subs.values():
        order.extend(doc for doc in pages if doc["slug"] in BY_SLUG)
    return order


def _index_feature(feature: str) -> str:
    entries, children, subs = _grouped(feature)

    def link(doc: dict) -> str:
        return f'<li><a href="{rel_href("index.html", doc["file"])}">{html.escape(doc["title"])}</a></li>'

    items: list[str] = []
    for kind in NAV_ORDER:
        entry = entries.get(kind)
        kids = children[kind]
        if entry is None and not kids:
            continue
        nested_bits: list[str] = []
        if kind == "design":
            readers = [doc for doc in kids if doc["slug"].endswith("/reader")]
            nested_bits.extend(link(doc) for doc in kids if doc not in readers)
            nested_bits.extend(link(doc) for doc in readers)
        else:
            nested_bits.extend(link(doc) for doc in kids)
        nested = "<ul>" + "".join(nested_bits) + "</ul>" if nested_bits else ""
        num = NAV_NUM[kind]
        if entry is not None:
            items.append(
                f'<li><a href="{rel_href("index.html", entry["file"])}">{num} {html.escape(entry["title"])}</a>{nested}</li>'
            )
        else:
            items.extend(nested_bits)
    if subs:
        bits: list[str] = []
        for name, pages in subs.items():
            home = _sub_home(pages, name)
            bits.append(
                f'<li><a href="{rel_href("index.html", home["file"])}">{html.escape(name)}</a><ul>'
                + "".join(link(doc) for doc in pages)
                + "</ul></li>"
            )
        items.append("<li>10 sub-feature<ul>" + "".join(bits) + "</ul></li>")
    home = feature_home(feature)
    return (
        '<section class="doc-group"><h3><a href="'
        + rel_href("index.html", home["file"])
        + '">'
        + html.escape(feature)
        + "</a></h3><ul>"
        + "".join(items)
        + "</ul></section>"
    )


def sidebar(current: str, from_file: str) -> str:
    overview_attr = ' aria-current="page"' if current == "overview" else ""
    home = rel_href(from_file, "index.html")
    if current == "overview":
        rows = []
        for feature in FEATURES_ORDER:
            first = feature_home(feature)
            rows.append(
                f'<li class="tree-leaf"><a class="tree-link" href="{rel_href(from_file, first["file"])}">'
                f'<span class="tree-link__num">{len(feature_docs(feature)):02d}</span>{html.escape(feature)}</a></li>'
            )
        nav = '<ul class="tree">' + "".join(rows) + "</ul>"
        summary = "Features"
    else:
        feature = BY_SLUG[current]["feature"]
        nav = _feature_tree(feature, current, from_file)
        summary = feature
    return f'''<aside class="sidebar">
  <nav aria-label="Directory">
    <div class="tree-overview"><a class="tree-link" href="{home}"{overview_attr}><span class="tree-link__num">00</span>All features</a></div>
    {nav}
  </nav>
</aside>'''


def breadcrumbs(doc: dict) -> str:
    parts = [f'<a href="{rel_href(doc["file"], "index.html")}">Docs</a>']
    parts.extend(f"<span>{html.escape(label)}</span>" for label in doc["crumbs"])
    parts.append(f"<span>{html.escape(doc['title'])}</span>")
    return '<nav class="breadcrumbs">' + " / ".join(parts) + "</nav>"


def related(doc: dict) -> str:
    if not doc["related"]:
        return ""
    links = "".join(
        f'<a href="{rel_href(doc["file"], BY_SLUG[slug]["file"])}">{html.escape(BY_SLUG[slug].get("related_label", BY_SLUG[slug]["title"]))}</a>'
        for slug in doc["related"]
    )
    return f'<nav class="related" aria-label="Related pages"><span class="related__label">Related</span>{links}</nav>'


def pager(slug: str) -> str:
    order = [d["slug"] for d in _reading_order(BY_SLUG[slug]["feature"])]
    idx = order.index(slug)
    prev_slug = order[idx - 1] if idx > 0 else None
    next_slug = order[idx + 1] if idx + 1 < len(order) else None
    parts = ['<nav class="pager" aria-label="Previous and next">']
    if prev_slug:
        d = BY_SLUG[prev_slug]
        parts.append(f'<a class="prev" href="{rel_href(BY_SLUG[slug]["file"], d["file"])}"><span class="label">Previous</span>{html.escape(d["title"])}</a>')
    else:
        parts.append("<span></span>")
    if next_slug:
        d = BY_SLUG[next_slug]
        parts.append(f'<a class="next" href="{rel_href(BY_SLUG[slug]["file"], d["file"])}"><span class="label">Next</span>{html.escape(d["title"])}</a>')
    parts.append("</nav>")
    return "".join(parts)


def _callout_label(inner: str) -> str:
    if "UNKNOWN" in inner or "Unverified" in inner:
        return "UNVERIFIED"
    lead = re.match(r"\s*(?:<p>)?\s*<strong>(.*?)</strong>", inner, re.S)
    label = re.sub(r"<[^>]+>", "", lead.group(1)) if lead else ""
    if re.search(r"警告|风险|Warning", label, re.I):
        return "WARN"
    if re.search(r"例子|例如|Example", label, re.I):
        return "EXAMPLE"
    return "NOTE"


def _badge_levels(body: str) -> str:
    parts = re.split(r"(<[^>]+>)", body)
    skip = 0
    out: list[str] = []
    for part in parts:
        if part.startswith("<"):
            tag = re.match(r"</?([a-zA-Z0-9]+)", part)
            if tag:
                name = tag.group(1).lower()
                if part.startswith("</"):
                    if name in {"a", "code", "pre"} and skip:
                        skip -= 1
                elif name in {"a", "code", "pre"} and not part.endswith("/>"):
                    skip += 1
            out.append(part)
            continue
        if skip:
            out.append(part)
            continue
        part = re.sub(
            r"\bMUST NOT\b",
            r'<span class="lvl lvl--must">MUST NOT</span>',
            part,
        )
        part = re.sub(
            r"\bMUST\b(?!\s+NOT)",
            r'<span class="lvl lvl--must">MUST</span>',
            part,
        )
        part = re.sub(
            r"\bNICE\b",
            r'<span class="lvl lvl--nice">NICE</span>',
            part,
        )
        out.append(part)
    return "".join(out)


def apply_doc_transforms(doc: dict, body: str) -> str:
    rel = doc["source"][0]

    def callout(match: re.Match) -> str:
        inner = match.group(1)
        label = _callout_label(inner)
        return f'<blockquote class="callout" data-label="{label}">{inner}</blockquote>'

    body = re.sub(r"<blockquote>(.*?)</blockquote>", callout, body, flags=re.S)

    if rel.endswith("-prd.md"):
        body = re.sub(
            r"<p><strong>(PRD-[A-Z]+)</strong>\s*—\s*(.*?)</p>",
            r'<div class="req" id="\1"><span class="req-id">\1</span><span class="req-text">\2</span></div>',
            body,
            flags=re.S,
        )
    if rel.endswith("document-standard-design.md"):
        body = re.sub(
            r"<(h[45])>(DSGN-[A-Z]+)\s*—\s*(.*?)</\1>",
            lambda m: (
                f'<{m.group(1)} class="clause"><span class="clause-id">{m.group(2)}</span>'
                f'<span class="clause-title">{m.group(3)}</span></{m.group(1)}>'
            ),
            body,
        )
    if "/impl-plan/" in rel:
        body = re.sub(
            r"<h3>(IMPL-[A-Z]+)\s*—\s*(.*?)</h3>",
            r'<h3 class="impl-step"><span class="impl-id">\1</span><span class="impl-title">\2</span></h3>',
            body,
        )
        body = body.replace("<p><strong>Goal:</strong>", '<p class="impl-goal"><strong>Goal:</strong>')
        body = body.replace("<p><strong>Steps:</strong>", '<p class="impl-steps"><strong>Steps:</strong>')
        body = body.replace("<p><strong>Verify:</strong>", '<p class="impl-verify"><strong>Verify:</strong>')
    if "/test-plan/" in rel:
        parts = re.split(r"(?=<h[34]>)", body)
        body = "".join(
            f'<section class="test-card">{part}</section>' if re.match(r"<h4>TST-", part) else part
            for part in parts
        )
    body = _badge_levels(body)
    body = _stamp_ids(body, doc["file"])
    return _linkify(body, doc["source"][1], doc["file"])


def site_title(doc: dict) -> str:
    context = doc["crumbs"][-1] if doc["crumbs"] else ""
    if context == "Spec-driven development":
        return f"{doc['title']} · Spec Atlas"
    return f"{doc['title']} · {context} · Spec Atlas"


def doc_page(doc: dict) -> str:
    rel, path = doc["source"]
    body = inline_figures(apply_doc_transforms(doc, render_source(rel, path)), path)
    page = doc["file"]
    asset = rel_href(page, "assets/app.js")
    return f'''{head(site_title(doc), page)}
<body>
{topbar(page)}
<div class="site">
  {sidebar(doc["slug"], page)}
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
<script src="{asset}"></script>
</body>
</html>'''


def doc_card(doc: dict) -> str:
    return f'''<a class="doc-card" href="{rel_href("index.html", doc["file"])}">
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
    return f'''{head("Spec Atlas", "index.html")}
<body>
{topbar("index.html")}
<div class="site">
  {sidebar("overview", "index.html")}
  <main class="content">
    <section class="hero">
      <p class="eyebrow">One site</p>
      <h1>Features, then the page.</h1>
      <p class="deck">Each page is one line in the directory. Open a feature and its directory stays on the left. The page stays on the right. Markdown under docs/features/ is the source of truth.</p>
      <div class="hero-chips">
        <span class="chip">{len(DOCS)} pages</span>
        <span class="chip">{len(FEATURES_ORDER)} features</span>
        <span class="chip">source: docs/features</span>
      </div>
    </section>

    <section class="doc-index" aria-labelledby="docs-title">
      <div class="section-head">
        <p class="eyebrow">Directory</p>
        <h2 id="docs-title">Open a feature</h2>
      </div>
      {"".join(_index_feature(feature) for feature in FEATURES_ORDER)}
    </section>
  </main>
</div>
<footer class="foot"><div class="foot-inner">Assembled from committed <code>.md</code> under <code>docs/features/</code>. The Markdown is authoritative; this page is a reading view.</div></footer>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>if(window.mermaid){{mermaid.initialize({{startOnLoad:false}});}}</script>
<script src="{rel_href("index.html", "assets/app.js")}"></script>
</body>
</html>'''


SITE_CSS = r"""
/* diagram-design editorial skin */
:root {
  --bg: #f5f5f5;
  --bg-2: #ececec;
  --bg-3: #e4e4e4;
  --fg: #2d3142;
  --muted: #4f5d75;
  --subtle: #5a6580;
  --border: #bfc0c0;
  --border-2: rgba(45, 49, 66, 0.12);
  --link: #2e5aa8;
  --link-hover: #24488a;
  --blue-soft: rgba(46, 90, 168, 0.08);
  --red: #bf4520;
  --red-soft: rgba(191, 69, 32, 0.08);
  --code-bg: #ececec;
  --code-fg: #2d3142;
  --pre-bg: #ececec;
  --pre-fg: #2d3142;
  --pre-link: #2e5aa8;
  --font-display: "Instrument Serif", "Noto Serif SC", serif;
  --font-body: Geist, "Noto Sans SC", "PingFang SC", sans-serif;
  --font-mono: "Geist Mono", ui-monospace, monospace;
  --measure: 760px;
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
  justify-content: space-between;
  gap: 12px;
}
.brand a { display: inline-flex; align-items: center; gap: 8px; color: var(--fg); text-decoration: none; }
.brand a:hover { text-decoration: none; }
.brand-mark { color: var(--link); font-family: var(--font-display); font-weight: 500; font-size: 18px; letter-spacing: .2px; }
.brand-name { font-family: var(--font-display); font-size: 18px; font-weight: 500; color: var(--fg); }
.strike-btn { font-family: ui-monospace, monospace; font-size: 12px; padding: 4px 10px; border: 1px solid var(--border); background: transparent; color: var(--fg); border-radius: 999px; cursor: pointer; }
html[data-strike="off"] del { display: none; }

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
.tree-ord { flex: 0 0 auto; min-width: 1.4rem; font-variant-numeric: tabular-nums; color: var(--muted); font-size: 12px; }
.tree-branch > details > summary > .tree-link { display: flex; align-items: baseline; gap: 8px; }
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
.tree-branch > details > summary .tree-link { flex: 1; padding-top: 0; padding-bottom: 0; }

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
  transition: border-color .15s ease;
}
.doc-card:hover {
  color: var(--fg);
  text-decoration: none;
  border-color: var(--fg);
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
.doc-body h2 {
  margin: 40px 0 14px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
  font-family: var(--font-display);
  font-weight: 500;
  font-size: 30px;
  line-height: 1.2;
  color: var(--fg);
}
.doc-body > h2:first-child { margin-top: 0; padding-top: 0; border-top: 0; }
.doc-body h3 {
  margin: 28px 0 10px;
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 20px;
  line-height: 1.3;
  color: var(--fg);
}
.doc-body h4 {
  margin: 22px 0 8px;
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 16px;
  line-height: 1.4;
  color: var(--fg);
  padding-left: 10px;
  border-left: 3px solid var(--red);
}
.doc-body h5 {
  margin: 18px 0 6px;
  font-family: var(--font-body);
  font-weight: 500;
  font-style: italic;
  font-size: 15px;
  line-height: 1.45;
  color: var(--muted);
}
.doc-body p { margin: 0 0 1em; font-size: 16px; line-height: 1.75; }
.doc-body .lvl {
  font-family: var(--font-mono);
  font-size: 11px;
  border-radius: 3px;
  padding: 1px 6px;
  white-space: nowrap;
}
.doc-body .lvl--must { background: var(--red); color: #fff; }
.doc-body .lvl--nice { border: 1px solid var(--border); color: var(--muted); background: var(--bg); }
.doc-body a.id-ref {
  font-family: var(--font-mono);
  font-size: 12px;
  background: var(--bg-2);
  border-radius: 3px;
  padding: 0 4px;
  text-decoration: none;
}
.doc-body a.id-ref:hover { background: var(--bg-3); color: var(--link-hover); }
.doc-body ul, .doc-body ol { padding-left: 26px; margin: 0 0 12px; }
.doc-body li { margin: 4px 0; }
.doc-body li::marker { color: var(--fg); }
.doc-body strong { font-weight: 500; }
.doc-body hr { margin: 28px 0; border: 0; border-top: 1px solid var(--border-2); }

/* callouts */
.doc-body blockquote {
  margin: 16px 0;
  padding: 12px 16px;
  border: 1px solid var(--border-2);
  border-radius: 6px;
  background: #fff;
  color: var(--fg);
}
.doc-body blockquote.callout { border-left-width: 3px; border-left-style: solid; }
.doc-body blockquote.callout[data-label]::before {
  content: attr(data-label);
  display: block;
  margin-bottom: 4px;
  color: var(--muted);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.doc-body blockquote.callout[data-label="NOTE"] { border-left-color: var(--link); }
.doc-body blockquote.callout[data-label="WARN"],
.doc-body blockquote.callout[data-label="UNVERIFIED"] {
  border-left-color: var(--red);
  background: var(--red-soft);
}
.doc-body blockquote.callout[data-label="WARN"]::before,
.doc-body blockquote.callout[data-label="UNVERIFIED"]::before { color: var(--red); }
.doc-body blockquote.callout[data-label="EXAMPLE"] { border-left-color: var(--muted); }

figure.fig {
  margin: 24px 0;
  border: 1px solid var(--border-2);
  border-radius: 6px;
  background: var(--bg);
  padding: 12px;
}
figure.fig .fig-scroll { overflow-x: auto; max-width: 100%; }
figure.fig svg { display: block; max-width: 100%; height: auto; }
figure.fig figcaption {
  margin-top: 10px;
  font-family: var(--font-display);
  font-style: italic;
  font-size: 14px;
  color: var(--muted);
}
.doc-body blockquote p { margin: 0 0 4px; }
.doc-body blockquote p:last-child { margin-bottom: 0; }

/* code — devsite: light inline, dark block */
.doc-body a code { color: var(--link); background: var(--blue-soft); }
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
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  color: var(--fg);
  text-align: left;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.doc-body td { padding: 10px 14px; border-bottom: 1px solid var(--border-2); vertical-align: top; text-align: left; }
.doc-body tbody tr:last-child td { border-bottom: 0; }
.doc-body tbody tr:nth-child(even) td { background: var(--bg-2); }
.doc-body tbody tr:has(del) { opacity: .6; }

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
        dest = OUT / doc["file"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(doc_page(doc), encoding="utf-8")
    for stale in OUT.rglob("*.html"):
        if "pipeline" in stale.relative_to(OUT).parts:
            stale.unlink()
    print(f"Wrote {OUT} ({len(DOCS) + 1} pages)")


if __name__ == "__main__":
    main()
