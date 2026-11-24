---
name: spec-ingest
description: |
  Use when turning the current chat or local md/pdf/txt files into spec
  content. Reads the input, splits it into single-fact items with sources,
  sorts each item into a doc type (PRD, design, impl-plan, test-plan,
  decision-history, open question) and a target feature, gets one user
  confirmation, then hands the sort table to spec-write. Never writes
  committed spec docs itself.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - spec ingest
    - ingest into spec
    - sort into spec
    - chat to spec
    - file to spec
  when_to_use: |
    When a discussion has reached conclusions, or an existing md/pdf/txt
    document holds content, and it should land in a feature's spec docs
    under docs/features/.
  when_not_to_use: |
    When the content is still fuzzy and needs an interview (use
    grill-with-docs). When you already know exactly what to write and where
    (use spec-write directly). When the input is a URL, a meeting recording,
    or source code (not supported in v1). When you want tracker tickets
    (use spec-ticket after spec-write).
  audience:
    - developers
    - architects
  source_author: cicidi
  inspired_by: mattpocock to-spec — https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md
---

# spec-ingest

Read existing information and sort it into spec doc types. **spec-ingest only reads and sorts.**
The **spec-write** skill is the only writer of committed spec docs; spec-ingest hands its sort
table to spec-write and never edits a file under `docs/features/` outside `raw/`.
Do not interview the user for new content — sort only what the input already says.

Rationale and decisions: `docs/features/skill-factory/features/spec-ingest/design/spec-ingest-design.md`.

## 1. Check the input (DSGN-A)

Accept only:
- **Current chat** — from the start point the user names, else the whole conversation.
- **Local files** — paths ending in `.md`, `.pdf`, `.txt` (several allowed).

Anything else (URL, audio/video, code directory, transcript service) → stop that input, say v1
does not support it, and list it under "Rejected inputs". Future directions: URL, meeting
transcripts, reverse-spec from code. A pdf with no text layer (scanned) → stop and report; do
not guess its content.

## 2. Split into items, each with a source (DSGN-B)

- One item = one fact. A sentence holding a requirement and its reason becomes two items:
  the requirement (prd) and the reason as the decision behind it (decision-history).
- Give each item a temporary number `I-1`, `I-2`, … (not a permanent ID).
- **Source** = the evidence for the fact:
  - chat message → `用户 <date>（会话 <id prefix>）`
  - file line that names who said/decided it, or cites a reference → that attribution or
    reference, plus `path Lnn` (pdf: `path p.nn`)
  - file line that states a fact with no attribution and no reference → `UNKNOWN（path Lnn）`
  - an open question needs no evidence → `path Lnn`
- Keep unsourced items in the table; their source is `UNKNOWN`. Never invent a source.
- Do not add anything the input does not say. Your own inferences are not items.

## 3. Classify (DSGN-C)

Types and ID prefixes follow `skills/spec-organize/SPEC-STANDARD.md`.

| The item is… | Doc type |
|---|---|
| a requirement: what the system must or must not do (incl. constraints) | prd |
| a decision with a reason: what was chosen, why, what was rejected | decision-history |
| a decision with no reason given | decision-history, reason `UNKNOWN` |
| behavior or a contract: how the system behaves, what an interface looks like | design |
| an implementation step: order of work, what depends on what | impl-plan |
| a test case: given an input, expect a result | test-plan |
| an unanswered question | design (Open Questions, QUES) |
| fits no row, or two rows | `待定` — the user picks at step 6 |

Seams or testing remarks already in the input go to design (Testing Decisions) or test-plan.
Do not design test seams yourself (ARD-G).

## 4. Pick the target feature (DSGN-D)

Find the existing `docs/features/<f>/` each item belongs to. If none fits, do not create a
directory: propose a working name and wait for the human to confirm it (SDD ARD-CH).
A repo with no `docs/features/` at all takes the same path: after the human confirms the name,
spec-write creates the first feature directory. If the human does not want spec docs in this
repo, stop. Do not publish the spec as a tracker issue instead (ARD-M).

Do **not** decide new doc vs edit, which doc is the authority, or how to resolve a conflict —
spec-write does that in its own steps (DSGN-E, ARD-I).

## 5. Write the sort table (DSGN-F, ARD-J)

Path: `docs/features/<f>/raw/state/spec-ingest/<YYYY-MM-DD>-sort.md` (gitignored). Before the
feature is confirmed: `docs/state/wayfinder-<working-name>/spec-ingest/<YYYY-MM-DD>-sort.md`.

```markdown
# spec-ingest sort — <date>

Target feature: <f> | <working-name> (proposed, not confirmed)
Inputs: <chat range / file paths>
Rejected inputs: <input — reason> | none

| Item | Text | Source | Doc type | Target feature |
|---|---|---|---|---|
| I-1 | … | 用户 2026-11-20（会话 abcd1234） | prd | <f> |

UNKNOWN: I-n, …
```

No target-file or action column. Permanent IDs (PRD-A …) are assigned by spec-write.

## 6. Confirm once (DSGN-H)

Show the table and ask one question: is the sorting right? The user may change a row's type
or feature, delete rows, and settle `待定` rows. Do not ask for new facts. No confirmation →
stop; nothing is written.

## 7. Hand off to spec-write (DSGN-F)

Invoke the **spec-write** skill with: the sort table path, the target feature (or confirmed
name), the input list, and the UNKNOWN list. spec-write decides files, new vs edit, authority,
IDs, and keeps its ≤10 lines / ≤200 characters per edit rule.

## 8. Report (DSGN-I)

Items per doc type; docs spec-write created or changed; the UNKNOWN list; new QUES; rejected
inputs with reasons. spec-ingest opens no tracker issue (ARD-H) — for tickets run
**spec-ticket**.

## Hard rules

- Never write or edit a committed spec doc; only the sort table under `raw/` or `docs/state/`.
- Every item has a source or `UNKNOWN`.
- No interview, no invented content, no test-seam design.

## Testing

Fixture and expected routing: `tests/fixture-notes.md`, `tests/expected-routing.md`.
Pass = ≥90% agreement on doc type and target feature (`待定` not counted wrong) plus the hard
rules exactly (ARD-L).
