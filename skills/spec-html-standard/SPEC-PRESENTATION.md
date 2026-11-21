# Spec Presentation

How a committed spec is expressed. Paths, what to write, and evidence are in `skills/spec-organize/SPEC-STANDARD.md`. If this file and a design diverge, fix the design first. Rules marked NICE are reminders, not failures (ARD-BN).

Markdown is the full text. HTML is a reader view of that markdown. Generated HTML is rebuilt from the markdown; it does not add facts. A hand-maintained HTML changelog has a row for every markdown Change Log date (NICE, ARD-BA).

## Prose

Use prose for a single claim, a reason, or a sequence that is not a procedure. One fact, one place. Do not restate a fact whose home is another document; link to it.

**Readable by an undergraduate (MUST, PRD-M / ARD-BO).** The reader has only this document and the glossary in the parent design's appendix.

- Write complete sentences with a subject and a verb. Not keyword strings, not `A → B → fails` arrow chains, not slash lists like `organize/lint/sync`.
- Explain a term or an abbreviation where it first appears, or link it to the glossary. If the glossary lacks it, add it there.
- One idea per sentence. Split a sentence that needs two semicolons.
- Use bold only for the label at the start of a list item or a paragraph, not inside sentences for emphasis.
- Say what an ID means in words the first time it matters ("PRD-F, the rule for conflicting decisions").
- Body text may mix Chinese and English if it reads smoothly; keep an author's own words in their voice. Required headings and IDs stay English (ARD-BS).

## Format

Required headings stay the English text in SPEC-STANDARD, unnumbered. Number a heading only when the section is an ordered procedure (steps), or when it is the author's own numbered subheading under Problem Statement (ARD-BS). A step reference names the step id; the count of steps in a citation matches the procedure (NICE, ARD-AM, ARD-AZ).

The title, a section, a subsection, and a clause each use a different size, weight, and shape. Body text stays one size. Do not mark those paragraphs with a, b, c or 1, 2, 3.

## Style

The markdown source is the authority for wording. The reader HTML may add layout. It may not drop an L1 row or replace a section with a summary. Status words in prose match the tracker row they cite (MUST, ARD-BC). Strikethrough appears only in decision-history (MUST, ARD-BM).

## Table

Use a table for a comparison, an ownership row, a decision log, a test case, or a status list. Do not use a table for a single sentence. Each cell is a short phrase or one sentence; if a cell needs a paragraph, write the paragraph below the table instead. A tracker citation matches the tracker count (NICE, ARD-BB).

## Icon

No decorative icons. A mark is allowed only where this standard names a status. Decision Log columns stay `ID | Date | Decision`, with an optional fourth column `Ready` only (ARD-AX). Status and Supersedes are not columns. Readiness may also be written in the decision text.

## Diagram

Add a diagram when the prose shape is clearer visually than as a table or list (ARD-CA).

| Content shape | diagram-design type |
|---|---|
| Ordered phases | Steps |
| Components and connections | Architecture |
| Branching rules | Flowchart |
| Time-ordered messages | Sequence |
| States and transitions | State machine |
| Stacked levels | Layer stack |
| Task dependencies | Dependency graph |
| Req → design → test links | Requirement traceability |
| Parent / child structure | Tree |

Rules: no fact in the figure that prose does not state; L1 text must not live only in the figure; ≤9 nodes and ≤12 edges per figure; Simplified Chinese in `'Geist','Noto Sans SC','PingFang SC',sans-serif` at ≥12px; titles `'Instrument Serif','Noto Serif SC',serif`; keep diagram-design default skin unless onboarding says otherwise; static SVG only (no script).

Workflow: draft in `raw/diagrams/` with **diagram-design**; run `self_check.py` and `verify_geometry.py`; export `<doc-stem>-fig-<slug>.svg` beside the citing `.md`; cite with a blank-line-separated `![caption](<file>.svg)` line.
