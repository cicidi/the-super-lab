# Spec Presentation

How a committed spec is expressed. Paths, what to write, and evidence are in `skills/spec-organize/SPEC-STANDARD.md` chapters 1–3. If this file and a design diverge, fix the design first.

Markdown is the full text. HTML is a reader view of that markdown. A hand-written HTML changelog covers every changed markdown line. Generated HTML is rebuilt from the markdown; it does not add facts.

## Prose

Use prose for a single claim, a reason, or a sequence that is not a procedure. One fact, one place. Do not restate a fact whose home is another document; link to it.

## Format

Required headings stay the English text in SPEC-STANDARD, unnumbered. Number a heading only when the section is an ordered procedure (steps). A step reference names the step id. The count of steps in a citation matches the procedure.

## Style

The markdown source is the authority for wording. The reader HTML may add layout. It may not drop an L1 row or replace a section with a summary. Status words in prose match the tracker row they cite.

## Table

Use a table for a comparison, an ownership row, a decision log, a test case, or a status list. Do not use a table for a single sentence. A tracker citation matches the tracker count.

## Icon

No decorative icons. A mark is allowed only where this standard names a status. Decision Log columns stay `ID | Date | Decision`, with an optional fourth column `Ready` only (ARD-AX). Status and Supersedes are not columns. Readiness may also be written in the decision text.

## Diagram

Add a diagram when the prose cannot show an ordered flow. One flow, one diagram. The diagram does not introduce a fact that the prose does not state.
