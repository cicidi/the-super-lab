---
name: wayfinder
description: |
  Use when planning work too large for one agent session. Charts a shared map
  of decision briefs on the issue tracker, resolves them one at a time until
  the route to the destination is clear.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - wayfinder
    - chart map
    - decision mapping
    - plan large work
    - resume spec work
    - spec progress
    - spec recap
    - where are we on the spec
  when_to_use: |
    When work is too big for one session and the path from here to the
    destination isn't visible. When decisions need shared, persistent tracking
    across multiple sessions. In an SDD repo, also when the user resumes a
    conversation, asks for progress or a recap, or is about to commit docs.
  when_not_to_use: |
    When the work fits in one session. When requirements are already fully
    specified with tickets ready to implement. When you just need a quick
    spec — use spec-ingest instead. (Exception: in an SDD repo the map is always
    created — it is the progress record for every feature.)
  audience:
    - developers
    - architects
    - tech leads
  source_author: mattpocock
  source_url: https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md
  spec_bundle_version: "1.0.11"
  spec_built_at: "2026-11-24"
  spec_git_sha: "071aee7"
---
<!-- SPEC-BUNDLE-START -->
> **SDD spec bundle** `1.0.11` · built 2026-11-24 · git `071aee7`
<!-- SPEC-BUNDLE-END -->

A loose idea has arrived — too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision briefs** — questions whose resolution is a decision, not slices of a build to execute — one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting — it shapes every brief. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic — engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each brief resolves a decision, and the map is done when the way is clear — nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its **Notes** — carrying execution into the map itself — but absent that, produce decisions, not deliverables.

## Refer by name

Every map and brief is an issue, so it has a **name** — its title. In everything the human reads — narration, the map's Decisions-so-far — refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish — a name wraps its link — but they ride *inside* the name, never stand in for it.

## The Map

The map is a single issue on this repo's issue tracker, labelled `wayfinder:map` — the canonical artifact. Its briefs are child issues of the map.

The map is an **index**, not a store. It lists the decisions made and points at the briefs that hold their detail; a decision lives in exactly one place — its brief — so the map never restates it, only gists it and links.

**SDD override.** In an SDD repo the committed docs (decision-history, PRD, design) are authoritative; a brief holds working notes only. Before the feature directory exists, the map may also hold the rough PRD and background.

**Where the map, its child briefs, blocking, and frontier queries physically live is tracker-specific.** The issue tracker configuration should have been provided via the project's init flow. If no tracker has been configured, default to the local-markdown tracker (issues as files under `.scratch/`). In an SDD repo (one with `docs/features/spec-driven-development/`) the tracker is always the local layout in [SDD progress record](#sdd-progress-record-ard-ch). Otherwise consult the tracker doc's "Wayfinding operations" section, if the repo has one, for how _this_ repo expresses them; in an SDD repo the operations are defined inline in that section.

### The map body

The whole map at low resolution, loaded once per session. Open briefs are **not** listed — they are open child issues, found by query.

```markdown
<!-- SDD repos only: header block -->
phase: <Create | Map | Converge | Downstream>
feature: <feature name, or working name before it is confirmed>
last_action: <date — what was last done>

## Rough PRD and background

<!-- SDD repos only, before docs/features/<f>/ exists: working name, rough PRD, research background. Removed once the feature directory exists. -->

## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a brief.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index — one line per closed brief: enough to judge relevance, then zoom the link for the detail the brief holds -->

- [<closed brief title>](link) — <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't brief yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Briefs

Each brief is a **child issue** of the map; the tracker's issue id is its identity. Its body is the question, sized to one 100K token agent session:

```markdown
## Question

<the decision or investigation this brief resolves>
```

Each brief carries a `wayfinder:<type>` label — one of `research`, `prototype`, `grilling`, `task` (see [Brief Types](#brief-types)).

A session **claims** a brief by assigning it to the dev driving the map (SDD: set `Status: claimed` in the brief file; see [SDD progress record](#sdd-progress-record-ard-ch)), **first**, before any work, so concurrent sessions skip it. That assignee _is_ the claim: an open, unassigned brief is unclaimed.

Blocking uses the tracker's **native** dependency relationship — essential because it renders the frontier _visually_ in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker that lacks native blocking falls back to a body convention (SDD: a `Blocked by: NN, NN` line of brief numbers; see [SDD progress record](#sdd-progress-record-ard-ch)). A brief is **unblocked** when every brief blocking it is closed (SDD: `Status: resolved`); the **frontier** is the open, unblocked, unclaimed children — the edge of the known.

The answer isn't part of the body — it's recorded on resolution (see [Work through the map](#work-through-the-map)). Assets created while resolving a brief are linked from the issue, not pasted in.

## Brief Types

Every brief is either **HITL** — human in the loop, worked *with* a human who speaks for themselves — or **AFK**, driven by the agent alone. A HITL brief only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved by a `/research` **subagent**. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to — an outline, a rough take, a stub, or UI/logic code via the /prototype skill. Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation via the /grilling and /domain-modeling skills, one question at a time. The default case.
- **Task** (HITL or AFK): Manual work that must happen before a *decision* can be made — nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that *does* rather than decides — and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later briefs depend on.

## Pluggable Skill Interfaces

Wayfinder depends on four capabilities. Each is an interface with a default
implementation; you can replace any of them with your own skill at install time.

| Interface | Purpose | Default | Your Replacement |
|---|---|---|---|
| **interview** | Grill user, one question at a time, write CONTEXT.md + ADRs | `grill-with-docs` + `domain-modeling` | (ask on install) |
| **investigate** | Read docs/APIs/source, produce cited markdown file | `research` (ai-coworker) | (ask on install) |
| **prototype** | Build throwaway artifact to answer a design question | `prototype` | (ask on install) |
| **tracker** | Issue CRUD — create, list, label, assign, close | `gh` CLI (GitHub Issues); in an SDD repo, the local markdown layout under [SDD progress record](#sdd-progress-record-ard-ch) | (ask on install) |

### Configuration

On first install, the user is asked one question per interface:

> For `<interface>` (`<purpose>`), default is `<default>`. Replace or keep?

Answers can be:
- **"keep" / "default"** — use the default implementation
- **"use <name>"** — use a named skill (must exist in the project)
- **"skip"** — that brief type is unavailable

Choices are recorded so the skill reads them on every invocation.

## SDD progress record (ARD-CH)

In the-super-lab's spec-driven development (SDD), wayfinder owns the progress
rules of the pipeline design (PIPE-A-D, PIPE-A-E, PIPE-A-F, PIPE-H, PIPE-E-A).
An SDD repo is one with `docs/features/spec-driven-development/`. There the
tracker is upstream's local-markdown layout (mattpocock/skills
`setup-matt-pocock-skills/issue-tracker-local.md`): a directory holding
`map.md` plus one file per brief, `issues/NN-<slug>.md`. The operations follow
upstream, plus two SDD statuses — `claimed` and `out-of-scope`:

- **Brief header:** `Status:` (one of `open`, `claimed`, `resolved`, `out-of-scope`), `Type:` (`research`, `prototype`, `grilling` or `task` — the local stand-in for the `wayfinder:<type>` label) and `Blocked by:` (brief numbers `NN, NN`, or empty).
- **Claim:** set `Status: claimed`. **Frontier:** open briefs whose blockers are all resolved; take the lowest number first.
- **Resolve:** add a `## Answer` section, set `Status: resolved`, and append the one-line gist to map.md **Decisions so far**.
- **Out of scope:** set `Status: out-of-scope`. It does **not** count as resolved for blocking: any brief listing it in `Blocked by:` must be re-scoped (drop the blocker) or ruled out of scope too.
- **Work through the map:** invoke it with the map path, not a URL or number.

The **map is the progress record**:

| When | Map directory | Committed? |
|---|---|---|
| Before the feature name is confirmed | `docs/state/wayfinder-<working-name>/map.md` and `docs/state/wayfinder-<working-name>/issues/NN-<slug>.md` | No (`docs/state/` is gitignored) |
| After the name is confirmed and `docs/features/<f>/` exists | move the whole directory to `docs/features/<f>/raw/state/wayfinder/` (map at `docs/features/<f>/raw/state/wayfinder/map.md`) | No (`raw/` is gitignored) |

Never commit the map directory. One directory per feature, so efforts in
progress at the same time never overwrite each other. In SDD mode,
**always create the map**, even when it has no briefs: the map is the progress record
for every feature (this overrides "you don't need a map" in
[Chart the map](#chart-the-map) step 2). The map body starts with the SDD
header block (`phase`, `feature`, `last_action`); before the name is
confirmed, the working name, the rough PRD and the research background live in
its **Rough PRD and background** section. The project's CLAUDE layer stores
only the path of the active map: write it to `CLAUDE.local.md` if the repo has
one, else `CLAUDE.md`; if neither exists, ask the user whether to create one
(ARD-CG).

- **Recap on resume (PIPE-A-E).** When the user asks, or a conversation resumes,
  read the map and the committed docs, then report: what was done, where things
  stand, what remains, and the suggested next step. The recap is not committed.
- **Blocking questions stop Downstream (PIPE-E-A).** The authoritative list of
  blocking questions is the feature design's Open Questions tracker: `QUES-*`
  rows with a blocking yes/no column, one tracker per feature. While any QUES
  row marked blocking = yes is open, do not
  start Downstream (impl-plan, test-plan, spec-ticket). A brief that works on such
  a question names its QUES id in its body. This is different from wayfinder's
  own `Blocked by:` between briefs, which only orders briefs.
- **Review gate before commit (PIPE-A-D).** Before committing or pushing a change
  to committed docs, ask whether to run **spec-review** first. If the user says
  no, record the skip in the map (date and "spec-review skipped by user"); never
  skip silently.
- **Decisions leave the map.** A decision with direction goes into
  decision-history, the PRD or the design via **spec-write**; the map only links it.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live briefs lies the **fog of war** — the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a brief clears the fog ahead of it, graduating whatever's now specifiable into fresh briefs — one at a time, until the way to the destination is clear and no briefs remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination — everything here is in scope, just not sharp enough to brief. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or brief?** The test is whether you can state the question precisely now — _not_ whether you can answer it now.

- **Brief when** the question is already sharp — even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into brief-sized pieces: it's coarser than a brief, and one patch may graduate into several briefs, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live brief, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope** — it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates — the frontier stops at the destination — so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a brief that already exists turns out to sit past the destination — mis-scoped in while charting, or exposed by a resolution — **close it** (a closed brief is unambiguously off the frontier; SDD: closing it as out of scope does **not** unblock the briefs it blocks) and leave one line in the **Out of scope** section: the gist plus why it's out of scope, linking the closed brief (SDD: set `Status: out-of-scope`, then re-scope or rule out every brief that lists it in `Blocked by:`; see [SDD progress record](#sdd-progress-record-ard-ch)). It stays out of **Decisions so far**, which records the route actually walked — a scope boundary isn't a step on it.

## Spec site

Every committed document created or moved during a Wayfinder session follows
`skills/spec-organize/SPEC-STANDARD.md` (paths, kebab-case names, INDEX.md).
The one site is rebuilt with `python3 tools/build_sdd_site.py` before commit and
deployed by GitHub Pages from master (ARD-CF, ARD-CD).

## Spec Creation & Spec-Review Checkpoint

After all briefs are resolved (SDD: or `Status: out-of-scope`, with every brief it blocked re-scoped or ruled out too) and the map is done, before handing off to
`spec-ticket`:

```
Wayfinder map done
       |
       v
    spec-ingest
       |
       +-- Sorts all brief conclusions into prd / design / decision-history /
       |   impl-plan / test-plan items
       +-- Hands them to spec-write, which writes docs/features/<f>/
       |
       v
    spec-review checkpoint
       |
       +-- Reviews: spec + all closed briefs + CONTEXT.md + ADRs
       +-- Checks: consistency, completeness, no contradictions
       +-- Verifies: SPEC-STANDARD paths, INDEX.md, naming
       |
       v
    Review passed?
       |
   YES +-- spec-ticket -> one parent ticket per feature + one ticket per IMPL-*
   NO  +-- fix documents, re-review
```

The spec-review checkpoint is a gate — it must pass before `spec-ticket` can run.
In an SDD repo, Downstream / `spec-ticket` also requires that no open QUES row is
marked blocking = yes (PIPE-E-A). A map with no briefs is not "done" by that
fact alone: in SDD every feature has a map.
This ensures all documents are consistent, complete, and deployable before any
implementation begins.

### Entity Relationships

```
N briefs (decisions) -> 1 spec (docs/features/<f>/) -> 1 parent + M tickets (build)

  Map:      1 issue, label wayfinder:map
  Brief:    N child issues, label wayfinder:<type>
            (research | grilling | prototype | task)
  Spec:     docs, not an issue (spec-ingest sorts, spec-write writes)
  Parent:   1 ticket per feature, links only (created by spec-ticket)
  Tickets:  1 per IMPL-*, children of the parent (created by spec-ticket)
```

The spec is not an issue: it is written with **spec-write** into
`docs/features/<f>/`. The parent ticket only links to it.

## Pipeline

```
wayfinder -> spec-ingest -> spec-write -> spec-review -> spec-ticket -> auto-tdd
 (decide)    (sort)         (write)       (verify)      (ticket)       (build)
```

## Invocation

Two modes. Either way, **never resolve more than one brief per session** — with the exception of research briefs.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run a `/grilling` and `/domain-modeling` session to pin down what this map is finding its way to — the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** — the way to the destination is already clear, the whole journey small enough for one session — you don't need a map. Stop and ask the user how they'd like to proceed. (SDD repo: still create the map — see [SDD progress record](#sdd-progress-record-ard-ch).)
3. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Create the briefs you can specify now** as child issues of the map — then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Wiring sorts them into the frontier and the blocked; everything you can't yet specify stays in the fog — the **Not yet specified** section.
5. **Fire the research subagents.** For each `research` brief you just created, spin up a `/research` subagent to resolve it in parallel, capturing its findings on a throwaway `research/<name>` branch with a context pointer from the brief.
6. Stop — charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with a map (URL or number; in an SDD repo, the map path). A brief is **optional** — without one, you pick the next decision, not the user.

1. Load the **map** — the low-res view, not every brief body.
2. Choose the brief. If the user named one, use it. Otherwise take the first frontier brief in order. **Claim it**: assign it to yourself before any work (SDD: set `Status: claimed`; see [SDD progress record](#sdd-progress-record-ard-ch)).
3. Resolve it — **zoom as needed**: fetch the full body of any related or closed brief on demand; invoke the skills the `## Notes` block names. If in doubt, use `/grilling` and `/domain-modeling`.
4. Record the resolution:
   4a. **Delivery Review Gate.** IF the brief type is `task` AND the task produced
       deliverables (files, code, documents):
       - Determine deliverable type:
         - spec docs under `docs/features/` → invoke `spec-review`
         - other `.md` files → Claude's default review
         - code files → invoke `matt-code-review` (ai-coworker)
         - fallback (spec-review or matt-code-review unavailable) → Claude's default review
       - Review must pass before the brief can be closed.
       - If review fails → fix issues, re-review.
       
       Research, grilling, and prototype briefs skip this gate — their output
       is knowledge/decisions, not deliverables.
   
   Post the answer as a **resolution comment**, **close** the issue, and **append a context pointer** to the map's Decisions-so-far. (SDD: use the resolve operation in [SDD progress record](#sdd-progress-record-ard-ch).)
5. Add newly-surfaced briefs (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new brief. If the answer reveals a brief — this one or another — sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those briefs.

The user may run unblocked briefs in parallel, so expect other sessions to be editing the tracker concurrently.
