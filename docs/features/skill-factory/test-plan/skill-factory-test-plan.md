---
feature: skill-factory
type: test-plan
state: final
final_date: 2026-09-25
health: stale
owner: cicidi
last_verified: 2026-09-25
---

# skill-factory Test Plan

## Test Plan

# skill-factory Test Plan

## Testing Decisions

| Level | Scope | Approach |
|-------|-------|----------|
| **Unit** | Skill helper scripts, validation functions, metadata parsers | Isolated tests with mock inputs; run in CI on every push. |
| **Integration** | Cross-skill workflows (skill-create → skill-edit → commit), agent orchestrations (devil-advocate, work-review), import pipeline | Use real or simulated skill files; verify intermediate outputs and final state. |
| **End‑to‑End** | Full user journeys: create a skill from scratch, import a third‑party skill, run an adversarial review, execute a work‑review sign‑off | Execute in a temporary repository; verify all side‑effects (commits, files, marketplace registration). |
| **Static Analysis** | Skill content conformance, frontmatter format, line count, naming rules, metadata completeness | Lint‑style checks (MUST / NICE gates) set up in CI and optionally as pre‑commit hooks. |

### 1.1 Unit Testing

- **Validation helpers**: `is_under_150_lines()`, `description_length_check()`, `prefix_enforcement()`, `anti_patterns_present()`, `metadata_complete()`.
- **Agent sub‑components**: Collector/Reviewer logic for `work-review`, Con/Pro/Judge for `devil-advocate` – test state transitions and vote aggregation.

### 1.2 Integration Testing

- **skill-create** execution (Phase 0–4) with mocked external search results.
- **skill-edit** pipeline: fetch → convert → write → validate.
- **skill-import** workflow: fetch → extract → write metadata → register.
- **Cross‑skill**: skill-edit → redirect to skill-create when ≥80% rewrite.
- **Agent orchestration**: devil-advocate 5‑round debate with vote fallback; work-review with automatic test execution.

### 1.3 End‑to‑End Testing

- Full “Create a coworker skill” journey (including commit and marketplace symlink).
- “Import a skill from GitHub” with metadata validation and CI enforcement.
- “Run work-review against a feature branch” – agent 2 runs Playwright E2E + existing unit tests, produces `acceptance.md` and `report.md`.
- “Trigger devil-advocate on a spec” – outputs `discussion.md` and `report.md` in `docs/devil-advocate/`.

### 1.4 Static Analysis / Content Validation

- **All skills** must pass the MUST gates defined in their own `Quality Gates` section.
- **Import skills** must have a complete `META.yaml` (source, upstream_commit, license, imported_at, imported_by, note).
- **Naming**: `walter-worker-` prefix for own skills; no prefix for imports; folder names unchanged.
- **Line count**: body ≤150 lines (NICE), enforced as soft target.
- **Description**: ≤500 chars.
- **Sections**: must include Anti-Patterns, Quality Gates (MUST/NICE), Philosophy‑driven overview.

---

## Key Test Scenarios

### 2.1 Skill Creation (`skill-create`)

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| SC‑01 | Phase 0 with external search – GitHub (≥10 repos) and Web search – user chooses “import” | Skill is created from fetched content, stored in `import-skills/`. |
| SC‑02 | Phase 0 – user chooses “absorb inspiration” | Skill is created with original content but inspired by found examples. |
| SC‑03 | Phase 0 – user chooses “build from scratch” | No external data used; standard interview Phase 1 begins. |
| SC‑04 | Phase 2 – generated skill includes Anti-Patterns, Quality Gates, Philosophy overview | All three sections present. |
| SC‑05 | Line count of body exceeds 150 | NICE gate triggers warning; skill can still be committed. |
| SC‑06 | Body exceeds 500 lines | (Original loose gate) – tightened to <150; test that gate now warns at 151+. |
| SC‑07 | Description >500 chars | NICE gate warns. |
| SC‑08 | Skill contains `deploy/` concept | MUST gate blocks commit. |

### 2.2 Skill Editing (`skill-edit`)

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| SE‑01 | Edit existing skill – change <80% of content | Targeted changes applied via Edit tool; no new file created. |
| SE‑02 | Change ≥80% of content | Tool redirects to `skill-create`. |
| SE‑03 | Non‑existent skill | Redirect to `skill-create`. |
| SE‑04 | Auto‑convert frontmatter (kebab‑case name, `Use when…` description, MIT license, opencode/claude‑code compatibility) | All fields correct. |
| SE‑05 | Auto‑adapt body sections (Philosophy→overview, Anti‑Pattern→Anti‑Patterns, Workflow→Process, Checklist→Quality Gates; remove Changelog/Convention Notes) | Section mapping performed correctly. |
| SE‑06 | Ambiguity triggers – unclear license, unknown body section | Agent asks exactly one clarifying question. |

### 2.3 Skill Import (`skill-import`)

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| SI‑01 | Import valid upstream skill (e.g. `tdd` from mattpocock/skills) | Skill placed in `import-skills/`, name unchanged, prefix not added. |
| SI‑02 | Metadata preservation – `source_author`, `source_url` present | Both fields written and validated in CI. |
| SI‑03 | Missing metadata (no license) | Ambiguity trigger: agent asks one question. |
| SI‑04 | CI validation of import metadata completeness | Pipeline fails if `META.yaml` is missing or incomplete. |

### 2.4 Agent‑Based Skills

#### Devil‑Advocate (`walter-worker-devil-advocate`)

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| DA‑01 | Trigger: “review spec” on a design document | Two output files: `discussion.md` (full debate) and `report.md` (summary). |
| DA‑02 | Debate reaches 5‑round limit | Fallback to 3‑agent majority vote; vote recorded in report. |
| DA‑03 | Trigger: “杠精” / “devil advocate” / “adversarial review” | Skill activates and follows same process. |

#### Work‑Review (`walter-worker-work-review`)

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| WR‑01 | Agent 1 (Collector) creates a test plan (no executable code) | Test plan written to `acceptance.md`. |
| WR‑02 | Agent 2 (Reviewer) executes tests using Playwright, curl, existing UT/FT | Acceptance criteria verified; `report.md` generated. |
| WR‑03 | Output path: `docs/work-review/YYYY-MM-DD-<topic>/` | Files appear in correct directory. |
| WR‑04 | Trigger: “work review” / “acceptance” / “sign off” / “verify work” | Skill activates. |

#### Multi‑Model Team (`multi-model-team`)

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| MT‑01 | GLM 5.2 architect + DeepSeek v4 Pro worker orchestration | Two‑agent collaboration produces coherent output. |

#### Contrarian Review (`walter-worker-contrarian-review`)

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| CR‑01 | 5‑agent adversarial document review | All agents produce independent critiques. |
| CR‑02 | Mode 1 activation | Correct sub‑process invoked. |

### 2.5 Directory & Naming Conventions

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| NC‑01 | All own skills in `walter-worker-skills/` | Folder exists; skills inside have `walter-worker-` prefix in name field. |
| NC‑02 | Imported skills in `import-skills/` | Folder exists; skills have original names (no prefix). |
| NC‑03 | Private skills in `personal-skills/` | Folder exists; symlinked locally, gitignored, not in marketplace. |
| NC‑04 | Flat vs nested structure | Both validated; flat structure allowed. |

### 2.6 Quality Gates Enforcement

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| QG‑01 | MUST gate violation (e.g., no Anti-Patterns section) | Commit blocked. |
| QG‑02 | NICE gate violation (e.g., body >150 lines) | Warning displayed; commit allowed. |
| QG‑03 | Quality gates run before every commit (Step 6 of process) | Script executes; passes/fails reported. |

### 2.7 CI / Automation

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| CI‑01 | Push containing import without complete `META.yaml` | CI job fails. |
| CI‑02 | Push with skill missing required frontmatter fields | CI job fails. |
| CI‑03 | Push with skill that has `deploy/` concept | MUST gate fails in CI. |

---

## Quality Gates / Acceptance Criteria

All skills and tools in the skill‑factory project must meet the following criteria.  
**MUST** gates block commit; **NICE** gates produce warnings.

### 3.1 Skill Content

| Gate | Type | Criteria |
|------|------|----------|
| Anti‑Patterns section present | MUST | Skill includes an `Anti‑Patterns` or `Anti-Patterns` section (or mapped section). |
| Quality Gates section with MUST / NICE | MUST | Skill contains a Quality Gates section with checkbox‑style lists. |
| Philosophy‑driven overview | NICE | Skill starts with a rationale/overview that explains the “why”. |
| No `deploy/` concept | MUST | Skill does not reference a `deploy/` directory or deployment workflow. |
| Description ≤500 chars | NICE | `description` field in frontmatter is ≤500 characters. |
| Body ≤150 lines | NICE | Body of SKILL.md (after frontmatter) is ≤150 lines. (Formerly 500; tightened.) |
| Name kebab‑case | MUST | Skill `name` field is kebab‑case (enforced by skill-edit auto‑conversion). |
| `Use when…` description start | NICE | Description begins with `"Use when..."`. |

### 3.2 Imported Skills

| Gate | Type | Criteria |
|------|------|----------|
| META.yaml complete | MUST | Contains `source`, `upstream_commit`, `license`, `imported_at`, `imported_by`, `note`. |
| Original author preserved | MUST | `source_author` and `source_url` present in metadata. |
| No prefix added | MUST | Imported skill name does not get `walter-worker-` prefix. |

### 3.3 Naming & Directory

| Gate | Type | Criteria |
|------|------|----------|
| Own skills in `walter-worker-skills/` | MUST | Skills created by the factory reside in `walter-worker-skills/`. |
| Prefix applied to own skill name | MUST | Skill name field includes `walter-worker-` prefix. |
| Import skills in `import-skills/` | MUST | Third‑party skills go to `import-skills/`. |
| Personal skills in `personal-skills/` | MUST | Private skills go to `personal-skills/` (gitignored). |
| No generic filenames | MUST | File names must include type suffix (e.g., `-decision-YYYY-MM-DD.md`). |

### 3.4 Process Steps

| Gate | Type | Criteria |
|------|------|----------|
| Phase 0 external search | MUST (for skill-create) | At least one external source consulted (GitHub ≥10 repos or web search).

## Skill Consolidation (2026-08-02)

# Skill Consolidation Test Plan

> **Spec:** docs/skill-factory/design/skill-consolidation-design.md
> **Date:** 2026-08-02

## Scope

Verify 38 walter-worker-skills → 10 merged skills correctly implemented.
- 10 new merged SKILL.md files created
- 35 old skill directories deleted
- 3 independent skills untouched (english-grammar-fix, multi-model-team, status)
- 9 personal-skills untouched
- 1 import-skills/tdd deleted (absorbed into auto-tdd)

---

## Layer 1: Conventions Compliance (3 tests per merged skill — 30 tests)

### T1.1 — Frontmatter fields
> For each new SKILL.md:
> - ✅ `name` is lowercase kebab-case, 1-5 words
> - ✅ `description` starts with "Use when...", ≤1024 chars, third person, describes trigger not workflow
> - ✅ `license: MIT` present
> - ✅ `compatibility` includes `claude-code,opencode`
> - ✅ No extra frontmatter fields beyond the 5 recognized

```bash
# Script: for each merged skill, parse frontmatter and validate
for skill in initiative dashboard project skill doc-review doc-organize bug knowledge auto-tdd research; do
  echo "=== $skill ==="
  # check name matches directory
  # check description starts with "Use when"
  # check description length ≤ 1024
  # check license field
  # check compatibility field
done
```

| Skill | Expected name | Expected description trigger |
|-------|--------------|------------------------------|
| initiative | `initiative` | Use when managing cross-project initiatives |
| dashboard | `dashboard` | Use when viewing analytics or managing dashboard |
| project | `project` | Use when managing the project catalog |
| skill | `skill` | Use when creating, editing, or listing skills |
| doc-review | `doc-review` | Use when reviewing a design, spec, proposal, or completed work |
| doc-organize | `doc-organize` | Use when organizing or merging documentation |
| bug | `bug` | Use when debugging, reporting bugs, or recording corrections |
| knowledge | `knowledge` | Use when extracting or querying session knowledge |
| auto-tdd | `auto-tdd` | Use when developing with test-driven methodology |
| research | `research` | Use when exploring unknowns or designing before implementation |

### T1.2 — Body structure
> For each new SKILL.md:
> - ✅ `# <skill-name>` heading + 1-2 sentence overview
> - ✅ `## When to Use` section
> - ✅ `## When NOT to Use` section
> - ✅ `## Process` section
> - ✅ No prohibited content (changelog, emoji, TBD, truncated sentences)

### T1.3 — Naming convention
> - ✅ Each directory name matches `{verb}-{object}` or `{domain}-{action}`
> - ✅ SKILL.md is uppercase
> - ✅ No filler words in names

---

## Layer 2: Structural Tests (10 tests)

### T2.1 — Old skills deleted
> 35 old directories must NOT exist:

```bash
# Category 3 — CRUD sets (22 removed)
test ! -d walter-worker-skills/initiative-create
test ! -d walter-worker-skills/initiative-edit
test ! -d walter-worker-skills/initiative-activate
test ! -d walter-worker-skills/initiative-deactivate
test ! -d walter-worker-skills/initiative-list
test ! -d walter-worker-skills/initiative-show
test ! -d walter-worker-skills/initiative-remove

test ! -d walter-worker-skills/analytics-create-db
test ! -d walter-worker-skills/analytics-daemon
test ! -d walter-worker-skills/analytics-dashboard
test ! -d walter-worker-skills/analytics-import
test ! -d walter-worker-skills/analytics-once

test ! -d walter-worker-skills/project-add
test ! -d walter-worker-skills/project-edit
test ! -d walter-worker-skills/project-remove
test ! -d walter-worker-skills/project-list
test ! -d walter-worker-skills/project-show
test ! -d walter-worker-skills/project-sync

test ! -d walter-worker-skills/skill-create
test ! -d walter-worker-skills/skill-edit
test ! -d walter-worker-skills/skill-import
test ! -d walter-worker-skills/skill-list

# Category 1/2 — merged skills (12 removed, doc-organize overwritten in-place)
test ! -d walter-worker-skills/devil-advocate
test ! -d walter-worker-skills/contrarian-review
test ! -d walter-worker-skills/work-review
test ! -d walter-worker-skills/bug-hunt
test ! -d walter-worker-skills/bug-report
test ! -d walter-worker-skills/self-analyze
test ! -d walter-worker-skills/self-heal
test ! -d walter-worker-skills/doc-merge
test ! -d walter-worker-skills/session-memory
test ! -d walter-worker-skills/knowledge-skill
test ! -d walter-worker-skills/find-my-unknown

# import-skills absorbed
test ! -d import-skills/tdd
```

### T2.2 — New skills exist
> 10 new directories must exist with SKILL.md:

```bash
for skill in initiative dashboard project skill doc-review doc-organize bug knowledge auto-tdd research; do
  test -f walter-worker-skills/$skill/SKILL.md || echo "MISSING: $skill"
done
```

### T2.3 — Independent skills untouched
> 3 skills must still exist unchanged:

```bash
test -f walter-worker-skills/english-grammar-fix/SKILL.md
test -f walter-worker-skills/multi-model-team/SKILL.md
test -f walter-worker-skills/status/SKILL.md
```

### T2.4 — Personal-skills untouched
> All 9 must still exist:

```bash
ls personal-skills/*/SKILL.md | wc -l  # must be 9
```

---

## Layer 3: Content Merge Quality Tests (20 tests)

### T3.1 — CRUD subcommand routing
> For `/initiative`, `/project`, `/skill`, `/dashboard`:

| Test | Description |
|------|-------------|
| T3.1.1 | No subcommand → lists current state + asks user what to do |
| T3.1.2 | Each subcommand has a clear one-line description |
| T3.1.3 | Invalid subcommand → suggests valid options |
| T3.1.4 | Each subcommand's process section references the CLI command it wraps |

### T3.2 — Conversation-branch routing
> For `/doc-review`, `/bug`, `/knowledge`, `/auto-tdd`, `/research`:

| Test | Description |
|------|-------------|
| T3.2.1 | Skill starts by asking ONE question to determine branch |
| T3.2.2 | Each branch has a self-contained `## Process` sub-section |
| T3.2.3 | Branches are mutually exclusive and collectively exhaustive |
| T3.2.4 | If user gives ambiguous answer, skill asks ONE clarifying follow-up |

### T3.3 — Merged logic: doc-review
| Test | Description |
|------|-------------|
| T3.3.1 | Design review branch includes adversarial questioning from devil-advocate |
| T3.3.2 | Design review branch includes alternative-searching from contrarian-review |
| T3.3.3 | Work completion branch includes acceptance criteria checking from work-review |
| T3.3.4 | Severity gate is explicitly defined (5-point scale, 3+ only discussed) |

### T3.4 — Merged logic: bug
| Test | Description |
|------|-------------|
| T3.4.1 | Hunt branch includes hypothesis→test→fix loop from bug-hunt |
| T3.4.2 | Report branch includes GitHub issue creation from bug-report |
| T3.4.3 | Heal branch includes trace recording from self-heal + pattern analysis from self-analyze |

### T3.5 — Merged logic: research
| Test | Description |
|------|-------------|
| T3.5.1 | Discover unknowns branch includes interview rules (one question, depth heuristic, stop condition) |
| T3.5.2 | Design spec branch includes explore→clarify→approaches→design→spec→write→review flow |
| T3.5.3 | After design spec completes, transitions to writing-plans |

---

## Layer 4: Deployment Tests (5 tests)

### T4.1 — coworker sync
```bash
coworker sync
```
> - ✅ No errors
> - ✅ All 10 new skills appear in `~/.claude/skills/` as SKILL.md files
> - ✅ Old skill directories removed from `~/.claude/skills/`

### T4.2 — Slash command availability
```bash
ls ~/.claude/skills/ | grep -E "^(initiative|dashboard|project|skill|doc-review|doc-organize|bug|knowledge|auto-tdd|research)$" | wc -l
# must be 10
```

### T4.3 — Old commands removed
```bash
ls ~/.claude/skills/ | grep -E "^(initiative-create|devil-advocate|bug-hunt|self-heal|find-my-unknown)$" | wc -l
# must be 0
```

### T4.4 — Config consistency
```bash
# skills in coworker.yaml match actual skill directories
coworker skill list
```
> - ✅ Count matches number of deployed skills (10 merged + 3 independent + ~20 other global skills)
> - ✅ No orphaned paths pointing to deleted skill directories

### T4.5 — coworker status still works
```bash
coworker status
```
> - ✅ Shows config table
> - ✅ Shows initiative progress if one is active

---

## Layer 5: Functional Regression (manual, via Claude Code)

### T5.1 — Each merged skill can be invoked
```
/initiative list
/dashboard start
/project list
/skill list
/doc-review          ← should ask "design or work review?"
/doc-organize
/bug                 ← should ask "hunt, report, or heal?"
/knowledge           ← should ask "obsidian vault or sqlite analytics?"
/auto-tdd            ← should ask "basic or auto?"
/research            ← should ask "discover unknowns or design spec?"
```

### T5.2 — Independent skills still work
```
/english-grammar-fix  ← should not break
/multi-model-team     ← should not break
/status               ← should run coworker status
```

---

## Summary

| Layer | Tests | Type |
|-------|-------|------|
| L1 — Conventions | 30 | Automated |
| L2 — Structural | 10 | Automated |
| L3 — Content | 20 | Manual review |
| L4 — Deployment | 5 | Shell |
| L5 — Functional | 12 | Manual (Claude Code) |
| **Total** | **77** | |

### Automation Priority

1. **L2 (10 tests)** — run first, pure shell, catches missing/extra directories immediately
2. **L4 (5 tests)** — run after `coworker sync`, verifies deployment
3. **L1 (30 tests)** — a script that parses SKILL.md frontmatter + validates sections
4. **L3 (20 tests)** — manual review of each merged SKILL.md body content
5. **L5 (12 tests)** — final smoke test in real Claude Code session

## Known Drift

The document below was accurate when written and is kept as the record. These
parts no longer match the repository, detected by reading the code against it on
2026-09-25. Nothing here has been rewritten — decide each one before changing it.

| Stated in this document | Current state | Evidence |
|---|---|---|
| Three skill directories: `walter-worker-skills/`, `import-skills/`, `personal-skills/` | Two: `skills/` and `personal-skills/` | commit `93d4a4a`, `8d451059` |
| `walter-worker-` prefix on native skill names | Prefix removed | commit `bc4d6cc0` |
| Five-field frontmatter with a `trigger` string | `name`, `description`, `license`, `compatibility`, `metadata` map | `CONVENTIONS.md` |
| `skill-create`, `skill-edit`, `skill-import` as separate skills | Merged into one `skill` skill | commit `6086424` |
| `devil-advocate`, `work-review`, `contrarian-review` skills | Removed or merged into `doc-review` | commit `6086424` |
| Outputs under `docs/devil-advocate/`, `docs/work-review/` | Documents live under `docs/features/` | `doc-organize` standard |
| `self-heal`, `self-analyze`, `tmux-setup` skills | No longer present | `coworker skill list` |

## Change Log

| Date | Change |
|------|--------|
| Date | Version | Description |
| 2026-07-23 | 1.0 | Initial test plan, derived from development history (commits 5d9747e9…5bfdb57e) |
| 2026-09-25 | Merged the companion document of the same type into this file; added frontmatter and the drift table |
