---
name: doc-organize
description: |
  Use when creating, moving, reorganizing, or merging documentation, when a
  document needs checking against the project's doc standard, or when specs and
  code have drifted apart. Use when deciding where a document belongs, how to
  name it, which files to consolidate, or how to reconcile documents that
  disagree.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - organize docs
    - doc organize
    - where should this go
    - move document
    - rename document
    - merge docs
    - doc merge
    - consolidate docs
    - too many files
    - doc lint
    - check docs
    - sync docs
    - docs inconsistent
    - spec is stale
    - INDEX.md
    - feature docs
---

# doc-organize

Defines the project's documentation standard, then enforces it in four modes:
place a document, lint the tree against the standard, consolidate sprawl into one
file per type, and sync documents with each other and with the code.

## When to Use

- Creating a document and unsure where it belongs or what to call it
- A docs tree has grown files that do not match the standard
- Too many files were committed while writing a spec
- Documents disagree with each other on tone or on a decision
- A spec looks stale relative to the code it describes
- Regenerating or repairing INDEX.md

## When NOT to Use

- Writing document content — write it, then use Organize mode for placement
- Reviewing whether a design is sound — use doc-review
- Resolving git merge conflicts in code — use git, not this skill
- Deciding which of two conflicting decisions is correct — this skill reports
  the conflict, a human rules on it

## The Standard

### Document types

Six committed types, one local type. Every document belongs to exactly one.

| Type | Holds | Committed |
|---|---|---|
| `prd` | What to build and why — product-level requirements | yes |
| `spec` | How it is built — technical detail, interfaces, design decisions | yes |
| `impl-plan` | The task breakdown that implements the spec | yes |
| `test-plan` | How the implementation is verified | yes |
| `decision-history` | Every decision ever made for the feature, in order | yes |
| `how-to` | Operational instructions for using the result | yes |
| `state` | Working progress, for compaction recovery | no — gitignored |

Architecture and design content belongs in a `## Design` section of `spec`, not
in a separate `design` type. External material that a document cites belongs
beside that document, not in a separate `reference` type.

### Exempt from the standard

The standard governs documents under `docs/features/`. These are not typed
documents and carry no frontmatter, type, or Change Log:

| Path | Why exempt |
|---|---|
| `docs/INDEX.md` | Generated index, rewritten wholesale each time |
| `docs/book/**` | Assembled output, built from documents that are already `final` |
| `CONTEXT.md` | Domain glossary, owned by domain-modeling |
| `README.md` | Repository orientation, not a feature document |

Lint reports these only if their links break or they list a file that no longer
exists. Do not add frontmatter to them.

### Path and naming

```
docs/features/<feature>/<type>/<feature>-<type>.md
```

One file per type per feature. A feature has at most one `prd`, one `spec`, one
`impl-plan`, one `test-plan`, one `decision-history`, and one `how-to`.

- `<feature>` is kebab-case, lowercase, no spaces or special characters
- The filename repeats the feature and the type, so a file is identifiable
  outside its directory
- A supporting file that a document cites sits in that document's folder:
  `docs/features/<feature>/spec/<source-name>.md`

### Frontmatter

Every document carries these four fields:

```yaml
---
feature: <feature-name>
type: prd | spec | impl-plan | test-plan | decision-history | how-to
state: draft | final
final_date: YYYY-MM-DD
---
```

`final_date` is required when `state` is `final`. A document becomes `final` when
its content is settled; after that, the code becomes the source of truth and the
document is maintained rather than rewritten.

### Required sections

Each type has a fixed section set. Sections may be added, never renamed or
dropped.

| Type | Required sections |
|---|---|
| `prd` | Overview, Goals and Success Metrics, User Stories, Functional Requirements, Non-Functional Requirements, Out of Scope |
| `spec` | Problem Statement, Solution, User Stories, Implementation Decisions, Design, Testing Decisions, Out of Scope, Further Notes |
| `impl-plan` | Global Constraints, then numbered Tasks |
| `test-plan` | Test Cases, Test Execution Order, Expected Pass Threshold |
| `decision-history` | Decision Log, Evidence Appendix |
| `how-to` | Overview, Prerequisites, Steps, Verification |

`prd` carries product intent. `spec` carries technical intent and the `Design`
section replacing the old separate design document.

### Decision history

The `decision-history` file is a tracking history, not a curated summary. It
keeps every decision ever made for the feature, including ones later superseded
and ones that turned out wrong. Nothing is deleted.

The Decision Log is a table:

```markdown
| # | Date | Decision | Status | Supersedes |
|---|------|----------|--------|------------|
| 0001 | 2026-07-14 | Adopt kebab-case for feature directories | accepted | — |
| 0002 | 2026-07-22 | Store state per feature, not per project | superseded by 0007 | — |
```

`Status` uses the vocabulary `proposed`, `accepted`, `deprecated`, or
`superseded by <NNNN>`. A superseded decision stays in the log and keeps its
evidence entry. When a decision is overwritten, add a new numbered entry that
supersedes the old one rather than editing the old one.

The Evidence Appendix holds one numbered entry per decision, preserving the
original rationale and supporting content:

```markdown
### 0001 — Adopt kebab-case for feature directories

Status: accepted

Rationale as originally recorded, including any alternatives that were
considered and why they were rejected. Support content belongs here: benchmark
output, links to the discussion that produced the decision, quoted constraints.
```

### Change Log

Every document ends with a Change Log, as its final section. It is appended to,
never prepended, and existing entries are never removed.

```markdown
## Change Log

| Date | Change |
|------|--------|
| 2026-08-02 | Initial creation |
| 2026-08-14 | Moved from docs/initiatives/ to docs/features/ |
```

### Scratch — not committed

Research, discussion, and adversarial-review artifacts are working material, not
documents. They live under the feature but are gitignored and never committed:

```
docs/features/<feature>/research/<topic>.md
docs/features/<feature>/discussion/<topic>.md
docs/features/<feature>/state/state-<YYYY-MM-DD>.md
```

Add these to `.gitignore`:

```gitignore
docs/features/*/research/
docs/features/*/discussion/
docs/features/*/state/
```

**Not to be confused with `.scratch/`.** Two gitignored trees exist by design,
and they hold different things:

| Tree | Holds | Written by |
|---|---|---|
| `docs/features/<feature>/` | Reasoning material — research, discussion, adversarial review, progress state | This skill, and the skills that produce reasoning |
| `.scratch/<feature-slug>/` | Ephemeral build artifacts — tickets and issues | wayfinder and to-tickets |

Reasoning is worth keeping on disk next to the feature it belongs to. Tickets are
throwaway work items and stay outside the docs tree. This skill does not manage
`.scratch/`, and Lint does not report it.

### INDEX.md

Regenerate after every create, move, rename, or delete. Walk the docs tree and
read each file's frontmatter, first heading, and first paragraph. A file that is
not listed is an orphan; a listed file that does not exist is a dead link.

### PROTECTED blocks

Content between `<!-- PROTECTED -->` and `<!-- END PROTECTED -->` is never
modified by any mode. The `<!-- PROTECTED START -->` / `<!-- PROTECTED END -->`
spelling is also recognised, but prefer the shorter form, which is what the rest
of the tooling uses.

## Process

### Step 0: Determine the mode

Infer from what the user asked. Ask one question only when genuinely ambiguous.

| Signal | Mode |
|---|---|
| "where should this go", a new document | A — Organize |
| "check the docs", "is this valid", reviewing a file | B — Lint |
| "too many files", "merge these", "consolidate" | C — Consolidate |
| "docs disagree", "spec is stale", "out of sync" | D — Sync |

If the user asks to "review the file and fix the format", that is B — Lint.
If they ask to "review the file" meaning whether its content is any good, that
is doc-review, not this skill.

---

### Mode A: Organize

1. Identify the feature. If it is not obvious from context, ask.
2. Identify the type from the six committed types. If the content spans types —
   product intent and technical detail together — split it: intent goes to `prd`,
   technical detail to `spec`.
3. Compute the path: `docs/features/<feature>/<type>/<feature>-<type>.md`.
4. If that file already exists, do not create a second one. Merge the new content
   into the existing file in the right section, and append a Change Log entry.
5. Write the frontmatter and required sections for the type.
6. Append the Change Log entry.
7. Regenerate INDEX.md.

### Mode B: Lint

Audit the docs tree against the standard. Applies mechanical fixes; reports the
rest.

1. Walk `docs/features/` and collect every markdown file.
2. Check each file against the standard:
   - **Wrong root** — a doc tree under `docs/initiatives/` or `docs/<feature>/`,
     outside `docs/features/`
   - **Wrong type directory** — a directory not in the six types: `design/`,
     `plan/`, `raw/`, `reference/`, `mockups/`, `work-review/`, `issues-found/`,
     `devil-advocate/`, `wrong-history/`
   - **Wrong filename** — not `<feature>-<type>.md`
   - **Missing or invalid frontmatter** — any of the four fields absent, or
     `state` outside `draft|final`, or `final` without `final_date`
   - **Missing required sections** for the type
   - **Change Log** missing, misplaced (not last), or containing a non-table
     section after it
   - **Heading skips** — an `##` under no `#`, an `####` under an `##`
   - **Dead links** — a relative link whose target does not exist
   - **Orphan or dangling INDEX.md entries**
   - **`docs/adr/`** — legacy layout; fold into the feature's `decision-history`
3. Apply the mechanical fixes directly: rename to the standard filename, move to
   the standard directory, add missing frontmatter, move Change Log to the end.
4. Report what was applied and what needs a human decision — content that must be
   split across types, or a section that has no counterpart in the standard.
5. Regenerate INDEX.md.
6. Append a Change Log entry to every file touched.

### Mode C: Consolidate

Reduce many files to one per type per feature. This mode deletes and merges, so
it proposes and waits — it never applies without approval.

1. For each feature, list the files by type.
2. Identify what consolidates:
   - Multiple `prd`, `spec`, `impl-plan`, `test-plan`, or `how-to` files for the
     same feature become one file per type.
   - Multiple decision records become one `decision-history`, with the Decision
     Log in chronological order and every original preserved in the Evidence
     Appendix. Nothing is dropped, including superseded and incorrect decisions.
   - `research/`, `discussion/`, `devil-advocate/`, and `raw/` content moves to
     gitignored scratch, or is deleted if it has no continuing value. Cite what
     it supported before removing it.
   - A `reference/` file is a supporting file, not scratch. Move it into the
     folder of the document it supports — a source cited by the spec goes to
     `spec/` — and keep it committed so the citation stays verifiable.
3. Present the plan: every move, merge, and deletion, with the target of each.
4. On approval, apply it, regenerate INDEX.md, and append Change Log entries.
5. If a decision is being overwritten by consolidation, add a superseding entry
   rather than editing the original.

### Mode D: Sync

Reconcile documents with each other and with the code.

1. Read each feature's documents.
2. Check for drift within and across documents:
   - **Tone and terminology** — the same concept named differently in two places,
     or a glossary term from CONTEXT.md not used
   - **Decision conflict** — two documents asserting different decisions
   - **Code drift** — a document describing behavior the code no longer has
3. Resolve in this order:
   - **Change Log first.** If one document records a later change than another,
     the later one wins.
   - **Code is the source of truth.** Where a document and the code disagree
     about what the system does, update the document to match the code.
   - **Report what cannot be resolved.** A disagreement about which decision is
     correct is a human decision. Report it; never silently pick one.
4. Auto-fix formatting, tone, terminology, links, and heading hierarchy directly.
5. Report every semantic conflict with the two positions and the evidence from
   each side. Do not rewrite a decision.
6. Append a Change Log entry to every file changed.

## Quality Gates

MUST:

- [ ] Every document is under `docs/features/` with a type from the six
- [ ] Filename is `<feature>-<type>.md` and matches its directory
- [ ] Frontmatter carries all four fields; `final` has `final_date`
- [ ] Required sections for the type are present and correctly named
- [ ] Change Log present, last in the file, appended to only
- [ ] PROTECTED blocks intact
- [ ] INDEX.md regenerated after any create, move, rename, or delete
- [ ] Consolidation preserved every decision, including superseded ones
- [ ] Scratch content is gitignored and not committed
- [ ] No content lost — every unique section from a merged file has a home

NICE:

- [ ] Heading hierarchy has no skipped levels
- [ ] All relative links resolve
- [ ] Terminology matches CONTEXT.md

## Anti-Patterns

- **Creating a second file for a type that already exists.** One feature has one
  `spec`. Add to it rather than creating `spec-v2.md`.
- **Deleting a superseded decision.** Superseded and wrong decisions stay in the
  log. That history is the point.
- **Committing scratch.** Research and discussion are working material. If it
  matters enough to commit, it belongs in the document it supports.
- **Silently resolving a decision conflict.** Report it and let a human rule.
- **Rewriting a `final` document.** After `final`, maintain it; the code is the
  source of truth.
- **Consolidating without approval.** Mode C deletes files. Always propose first.
- **Treating a content review as a lint.** Judging whether a design is sound is
  doc-review, not this skill.

## Sources

- Existing doc-organize skill: two-branch structure (organize, merge) and
  PROTECTED block handling, carried forward
- to-spec (mattpocock): the `spec` required-section template, reused verbatim
- domain-modeling (mattpocock): ADR status vocabulary and evidence format
- write-doc (walter-worker): Change Log format and append-only rule
- Observed in skill-factory and wayfinder-import documents: the `prd`, `spec`,
  `impl-plan`, and `test-plan` section sets
- User requirement: one file per type per feature, feature vocabulary, scratch
  gitignored, decision history kept whole, Lint applies while Consolidate
  proposes
