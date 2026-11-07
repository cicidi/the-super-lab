---
state: final
final_date: 2026-08-02
---

# Imported Skills — from Matt Pocock's Skills

> **Original Author:** [Matt Pocock](https://github.com/mattpocock)
> **Source Repository:** [mattpocock/skills](https://github.com/mattpocock/skills)
> **License:** MIT
> **Imported by:** [cicidi](https://github.com/cicidi) into [the-super-lab](https://github.com/cicidi/the-super-lab)

## Overview

Seven skills were imported from Matt Pocock's skill collection and adapted for the ai-coworker / the-super-lab ecosystem. They form a decision-to-delivery pipeline: **wayfinder** charts the map, **to-spec** synthesizes decisions into a spec, **to-tickets** decomposes into build tickets, and **implement** executes them. Supporting skills (**domain-modeling**, **grill-with-docs**, **prototype**) provide the interview and exploration capabilities wayfinder depends on.

```
wayfinder ──→ to-spec ──→ doc-review ──→ to-tickets ──→ implement
  (decide)      (write)      (verify)       (ticket)       (build)
     │
     ├── grill-with-docs  (interview)
     ├── domain-modeling  (glossary + ADRs)
     └── prototype        (throwaway artifact)
```

## Attribution

Every imported skill carries explicit attribution in its frontmatter:

```yaml
metadata:
  source_author: mattpocock
  source_url: https://github.com/mattpocock/skills/blob/main/skills/engineering/<skill>/SKILL.md
```

This ensures provenance is never lost — any downstream fork, redeployment, or IDE installation preserves the attribution chain. The MIT license from the original repository is retained.

## Adaptation Principles

When adapting these skills, three principles were followed:

1. **Preserve the body.** Non-wayfinder skills (`domain-modeling`, `grill-with-docs`, `prototype`, `to-spec`, `to-tickets`, `implement`) keep their original body text intact. Only frontmatter was converted to skill-factory conventions.

2. **Adapt where needed.** `wayfinder` received the most changes — terminology, pluggable interfaces, review gates — because it serves as the entry point and orchestrator of the pipeline.

3. **Never erase authorship.** `source_author` and `source_url` are permanent metadata. The `import-skills/` directory preserves original skill names as-is (no prefix, no rename).

---

## Skill-by-Skill Breakdown

### 1. wayfinder — Decision Mapping

| | |
|---|---|
| **Imported** | `2026-07-25` (commit `7c11a7b`) |
| **Role** | Entry point — charts a shared map of decision briefs on the issue tracker |
| **Original** | Charts a map, works through decision briefs one at a time until the route to the destination is clear |

**cicidi's Adaptations:**

| Adaptation | What Changed | Why |
|---|---|---|
| **Terminology** | "ticket" → "brief" for decision tickets | Disambiguate from to-tickets' build tickets; avoids confusion between "deciding what to build" and "building it" |
| **Pluggable Skill Interfaces** | Hardcoded skill references replaced with 4 configurable interfaces (interview, investigate, prototype, tracker) | Matt's version referenced specific skills by name. This version lets projects swap in their own — e.g., ai-coworker's `research` for `investigate` |
| **Delivery Review Gate** | New checkpoint on task brief resolution: `.md` deliverables → `doc-review`, code deliverables → `matt-code-review` | Quality gate — no deliverable leaves a brief without review |
| **Doc-Organize: MkDocs-Ready** | Standing requirement that all documents produced are MkDocs-deployable (INDEX.md maintained, kebab-case naming, `mkdocs.yml` nav updated) | Ensures the entire decision trail is a publishable GitHub Pages site, not a pile of scratch files |
| **Spec Creation + Doc-Review Checkpoint** | New pipeline segment after map completion: `wayfinder` → `to-spec` → `doc-review` → `to-tickets` | Closes the loop — decisions become a spec, spec gets reviewed, reviewed spec becomes build tickets |
| **Frontmatter** | Converted to 5-field ai-coworker format with triggers, when_to_use, when_not_to_use, audience | Convention compliance |

### 2. domain-modeling — Glossary & ADRs

| | |
|---|---|
| **Imported** | `2026-07-25` (commit `f6255af`) |
| **Role** | Builds and sharpens a project's domain model — challenges fuzzy terminology, writes CONTEXT.md glossary and ADRs |
| **Original** | Active discipline: challenge terms, invent edge cases, write glossary/decisions as they crystallize |

**cicidi's Adaptations:**

| Adaptation | What Changed | Why |
|---|---|---|
| **Frontmatter only** | Converted to ai-coworker format | Body preserved as-is; companion files (`CONTEXT-FORMAT.md`, `ADR-FORMAT.md`) imported unchanged |
| **Companion files** | `CONTEXT-FORMAT.md` and `ADR-FORMAT.md` shipped alongside SKILL.md | These are templates the skill references — they travel with the skill |

### 3. grill-with-docs — Relentless Interview

| | |
|---|---|
| **Imported** | `2026-07-25` (commit `6835420`) |
| **Role** | Composes `/grilling` and `/domain-modeling` into one session — interviews the user relentlessly to sharpen a plan |
| **Original** | Run a grilling session using domain-modeling skill |

**cicidi's Adaptations:**

| Adaptation | What Changed | Why |
|---|---|---|
| **Frontmatter only** | Converted to ai-coworker format | Body is a one-liner composition — no substantive changes needed |

### 4. prototype — Throwaway Artifacts

| | |
|---|---|
| **Imported** | `2026-07-25` (commit `78242fa`) |
| **Role** | Builds throwaway code to answer design questions — logic/state-model terminal apps or UI variations |
| **Original** | Two branches: logic terminal app or UI variations on a single route |

**cicidi's Adaptations:**

| Adaptation | What Changed | Why |
|---|---|---|
| **Frontmatter only** | Converted to ai-coworker format | Body preserved as-is; the two-branch design (LOGIC.md / UI.md) was already clean |

### 5. to-spec — Conversation to PRD

| | |
|---|---|
| **Imported** | `2026-07-25` (commit `212aab5`) |
| **Role** | Synthesizes current conversation into a spec (PRD), publishes to the issue tracker |
| **Original** | No interview — just synthesis of what was already discussed |

**cicidi's Adaptations:**

| Adaptation | What Changed | Why |
|---|---|---|
| **Tracker abstraction** | "Jira" references replaced with "project issue tracker" (configured via project init flow) | Tracker-agnostic — works with GitHub Issues, Linear, Jira, or local markdown files |
| **Triage label** | Added `ready-for-agent` label on published specs | Enables agentic workers to discover and claim specs automatically |
| **Frontmatter** | Converted to ai-coworker format | Convention compliance |

### 6. to-tickets — Spec to Tracer Bullets

| | |
|---|---|
| **Imported** | `2026-07-25` (commit `8730941`) |
| **Role** | Breaks a plan/design/conversation into tracer-bullet tickets with declared blocking edges |
| **Original** | Vertical slices through every layer, each demoable on its own, sized for one context window |

**cicidi's Adaptations:**

| Adaptation | What Changed | Why |
|---|---|---|
| **Tracker abstraction** | "Jira" references replaced with "project issue tracker" | Same tracker-agnostic approach as to-spec |
| **Triage label** | Added `ready-for-agent` label | Consistent with to-spec — tickets are agent-grabbable by construction |
| **Frontmatter** | Converted to ai-coworker format | Convention compliance |

### 7. implement — TDD Execution

| | |
|---|---|
| **Imported** | `2026-07-25` (commit `12c7dce`) |
| **Role** | Implements work from spec/tickets — TDD at pre-agreed seams, typechecking, code review, commit |
| **Original** | Use `/tdd` where possible, run typechecking, full test suite, code review, commit |

**cicidi's Adaptations:**

| Adaptation | What Changed | Why |
|---|---|---|
| **Frontmatter only** | Converted to ai-coworker format | Body preserved as-is; skill references (`/tdd`, `/code-review`) resolve to ai-coworker equivalents |

---

## Import History

```
2026-07-25 · grill-with-docs   (6835420) — first import
2026-07-25 · domain-modeling   (f6255af)
2026-07-25 · prototype         (78242fa)
2026-07-25 · wayfinder         (7c11a7b) — imported AND adapted
2026-07-25 · to-spec           (212aab5)
2026-07-25 · to-tickets        (8730941)
2026-07-25 · implement         (12c7dce)
2026-08-01 · phase 1 finalize  (43cb1ef) — doc-review, test plan, deploy
2026-08-02 · merge into root   (8d451059) — import-skills/ merged into skills/
2026-08-02 · consolidate       (93d4a4a) — all skills in single skills/ directory
```

## What Was NOT Imported

Matt Pocock's skill collection includes several other skills. The following were intentionally excluded:

| Skill | Why Excluded |
|---|---|
| `research` | ai-coworker has its own `research` skill — wayfinder's investigate interface points to it instead |
| `setup-matt-pocock-skills` | Replaced by ai-coworker's `init` / `project` flow |
| `triage` | Not needed by the wayfinder → to-tickets pipeline |
| `tdd` | ai-coworker's `auto-tdd` is a multi-agent superset |

---

## Verification

All 7 imported skills pass the skill-factory test suite (`bash tests/test_skills.sh`):

- Frontmatter: all 5 required fields present
- Attribution: `source_author` and `source_url` on every skill
- Body: non-wayfinder skills have original body text intact
- Conventions: no prohibited sections, no TBD/TODO, no emoji, no context leaks
- Terminology: "brief" consistently used for decision tickets; "ticket" only in to-tickets/build contexts
