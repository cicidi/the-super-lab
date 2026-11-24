# Spec HTML Standard (enforceable summary)

**Authoritative spec:** `docs/features/spec-driven-development/features/document-standard/design/document-standard-design-spec-reader-html.md` (**DSGN-N**). PRD: `docs/features/spec-driven-development/features/document-standard/prd/document-standard-prd-spec-reader-html.md` (**PRD-A–P**). If this file and **DSGN-N** diverge, **fix the design first**, then update this summary.

**Not a skill.** Expression rules: `SPEC-PRESENTATION.md`. Agents assemble reader HTML from this standard. spec-write edits markdown; spec-review checks fidelity. No separate `spec-reader` skill.

Hand-maintained HTML (ARD-AK) sets `spec-paired` to `hand-maintained`, `spec-source` to the repo path of the markdown, and `spec-source-sha256` to that file's hash. A mismatch fails `paired_html_stale`. Generated readers omit this meta and are rebuilt. Its changelog has one row for every date in the markdown Change Log (NICE, ARD-BA / ARD-BN). `<!-- html-skip -->` may wrap L4, not L1 or a struck sentence. Struck sentences stay in the HTML. One button switches between showing the strikethrough and hiding it.

## Output (MUST)

- Path: `docs/book/html/<parent>/<parent>-reader.html`. Other spec HTML mirrors `docs/features/` under `docs/book/html/` (ARD-BF)
- Source of truth: committed `.md` only; HTML is **derived**
- Scope: parent types present (`prd`, `design`, `impl-plan`, `test-plan`, `decision-history`; `how-to` optional); each `features/<sub>/` at least **design** (+ other types if committed)

## Fidelity (MUST — no over-trimming)

Align with document-standard **DSGN-I**:

| Level | In HTML |
|---|---|
| **L1** | Full: MUST/forbidden rows, req/test/impl/decision **table rows**, contract table rows, Out of Scope, IDs — **not** one-paragraph substitutes for whole sections |
| **L2** | Keep facts; may shorten wording, not drop conclusions |
| **L3** | May compress + link to canonical md |
| **L4** | Omit body; **MUST** link to md |

**IDs (**DSGN-F**):** Visible in HTML (`PRD-`, `DSGN-`, `ARD-`, `IMPL-`, `TST-` as in md).

**MUST NOT:** executive-summary-only tabs; fetch + raw md in `<pre>` as main UI; drop **DSGN-***/**PIPE-*** section bodies while keeping headers only.

**MAY:** HTML tables with same row set; callouts; flows; part files as sections/sub-tabs inside one tab.

## Structure (MUST)

- Page header: reading assembly; edit `.md` first; parent slug
- Tabs: parent (one per type); children (per sub-feature)
- Per tab footer: `Canonical:` path(s); all parts listed if split

## Site (MUST, ARD-BG)

One website for the whole project. Entry: `docs/book/html/index.html`.

- Each spec HTML page is one line in the directory.
- The directory opens a feature. It does not dump every feature's pages into one flat list with no feature.
- Inside a feature, the left column is that feature's directory. The right column is the page.
- Every page is reachable from the entry. GitHub Pages publishes the site from `master` (ARD-CD).
- The left directory shows hierarchy and numbers: 1 prd, 2 decision-history, 3 design, 4 impl plan, 5 test plan, 6 how to, 10 sub-feature (ARD-BI). Design parts and the reader expand under 3. Sub-features expand under 10. Pipeline has no HTML page.
- After a spec edit, spec-write prompts the user to rebuild this site; it does not rebuild it itself, and it does not invent a second layout (DSGN-N-E, reader PRD-M).

Rebuild: `python3 tools/build_sdd_site.py`

## Links (MUST, DSGN-N-K)

- An ID (`PRD-`, `DSGN-`, `ARD-`, `IMPL-`, `TST-`, `PIPE-`, `QUES-`) links to its definition. If the text names the owning feature ("parent design 的 DSGN-A", or `<feature>/<id>`), link there. Only an unqualified ID resolves in the same feature first, then the parent.
- A path written in the body is a link. A `.md` under `docs/features/` links to the same path under `docs/book/html/` with `.html`. A source with no page of its own (pipeline design) links to its section in the reader page. Any other file that exists links to that file.

## Visual and technical (DSGN-N-D)

- MUST: body text and committed SVG figures open offline in the browser (reader PRD-O, ARD-CB). Fonts and Mermaid may load from the network.
- NICE: site skin uses diagram-design default tokens and typography (ARD-CA).
- MUST: no runtime `.md` fetch for main content; no secrets and no raw eval text in the page.
- NICE: one site-wide style for layout, ID tags, cards, and callouts (ARD-BY).

## Workflow

- **spec-write:** after the markdown edit, prompt the user to rebuild the one site (`python3 tools/build_sdd_site.py`); rebuild when the user asks
- Conflict or spec bug found while assembling → **Ask human** → fix md → regenerate HTML
- SDD parent: `python3 tools/build_sdd_reader.py` then `python3 tools/validate_sdd_reader.py`

## Diagrams

- Committed `![alt](<doc-stem>-fig-<slug>.svg)` beside the citing `.md`; build inlines SVG (ARD-CA).
- Mermaid fenced blocks remain allowed; reader build renders them (`MERMAID-PATTERNS.md` samples). ASCII flows remain allowed; do not drop L1 labels when converting.

## Reference (structure OK, content must meet fidelity)

`docs/book/html/spec-driven-development/spec-driven-development-reader.html`
