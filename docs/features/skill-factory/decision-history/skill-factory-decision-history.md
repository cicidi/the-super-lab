---
feature: skill-factory
type: decision-history
state: final
final_date: 2026-09-25
health: active
owner: cicidi
last_verified: 2026-09-25
---

# skill-factory — Decision History

Append-only. Superseded and wrong decisions stay in the log; a decision
that is overturned gets a new numbered entry that supersedes it, never an
edit. Entries 0001-0126 were consolidated from fourteen per-day records
that were generated automatically from session analysis; no decision was
dropped in the consolidation.

## Decision Log

| # | Date | Decision | Status | Supersedes |
|---|------|----------|--------|------------|
| 0001 | 2026-06-10 | fix: skill-create quality gate improvements from round-01 review | accepted | — |
| 0002 | 2026-06-10 | docs: round-01 agent-B evaluation — both skills PASS | accepted | — |
| 0003 | 2026-06-10 | skill: add skill-edit and skill-import from round-01 Agent-A | accepted | — |
| 0004 | 2026-06-10 | chore: remove ai-worker-skills, fix skill-create description and references | accepted | — |
| 0005 | 2026-06-10 | docs: implementation plan for skill-factory bootstrap | accepted | — |
| 0006 | 2026-06-10 | docs: add skill-factory bootstrap design spec | accepted | — |
| 0007 | 2026-06-10 | refactor: move skills into walter-worker-skills namespace | accepted | — |
| 0008 | 2026-06-10 | feat: initialize skill-factory project with skill-create | accepted | — |
| 0009 | 2026-06-10 | Public open source repository | accepted | — |
| 0010 | 2026-06-10 | Directory structure: ai-worker-skills/ for own skills, import/ for imported, personal/ for private | accepted | — |
| 0011 | 2026-06-10 | Naming convention: ai-worker-skills get prefix 'ai-worker-', imports keep original name | accepted | — |
| 0012 | 2026-06-10 | Use Claude Code local marketplace via extraKnownMarketplaces | accepted | — |
| 0013 | 2026-06-10 | skill-import skill behavior: fetch, extract, write metadata, register in marketplace | accepted | — |
| 0014 | 2026-06-10 | META.yaml schema with source, upstream_commit, license, imported_at, imported_by, note | accepted | — |
| 0015 | 2026-06-10 | CI workflow to validate import metadata completeness | accepted | — |
| 0016 | 2026-06-10 | Test flat vs nested SKILL.md structure | accepted | — |
| 0017 | 2026-06-10 | OpenCode installation: git plugin + project-level symlink | accepted | — |
| 0018 | 2026-06-10 | Personal skills symlinked directly, gitignored, not in marketplace | accepted | — |
| 0019 | 2026-06-11 | skill: add walter-worker-devil-advocate — multi-agent adversarial review for specs and design docs | accepted | — |
| 0020 | 2026-06-11 | skill: add 5 migrated coworker skills | accepted | — |
| 0021 | 2026-06-11 | feat(skill-create): Phase 0 multi-source search — GitHub (>=10 repos), web search, import-vs-inspire | accepted | — |
| 0022 | 2026-06-11 | refactor: three-directory structure with walter-worker- prefix naming | accepted | — |
| 0023 | 2026-06-11 | fix(skill-import): add author preservation, import/ subdirectory, and anti-pattern for lost authorsh | accepted | — |
| 0024 | 2026-06-11 | docs: final verification logs and bootstrap summary | accepted | — |
| 0025 | 2026-06-11 | fix(tdd): optimize description and overview per skill-factory conventions | accepted | — |
| 0026 | 2026-06-11 | skill: import tdd from mattpocock/skills | accepted | — |
| 0027 | 2026-06-12 | skill: add walter-worker-work-review — 2-agent gatekeeper for work acceptance sign-off | accepted | — |
| 0028 | 2026-06-18 | skill: add walter-worker-contrarian-review — 5-agent adversarial document review | accepted | — |
| 0029 | 2026-06-23 | chore: remove self-heal/self-analyze from personal-skills (in walter-worker-skills) | accepted | — |
| 0030 | 2026-06-23 | chore: remove self-strain | accepted | — |
| 0031 | 2026-06-23 | fix: add english-grammar-fix (was untracked) | accepted | — |
| 0032 | 2026-06-23 | refactor: rename self-patch to english-grammar-fix | accepted | — |
| 0033 | 2026-06-23 | chore: remove skills deleted from walter-worker (flow-*, connect-*, doc-review, bug-sleuth, bug-create | accepted | — |
| 0034 | 2026-06-23 | chore: remove gate-* skills (not in walter-worker scope) | accepted | — |
| 0035 | 2026-06-23 | chore: remove self-init (walter-worker skills/init/ is more current) | accepted | — |
| 0036 | 2026-06-23 | feat: add self-heal and self-analyze skills | accepted | — |
| 0037 | 2026-06-23 | chore: remove session-memory (moved to walter-worker) | accepted | — |
| 0038 | 2026-06-23 | chore: remove initiative-create/edit (moved to walter-worker) | accepted | — |
| 0039 | 2026-06-23 | refactor: rename skills to simplified naming, migrate 21 AI coworker skills | accepted | — |
| 0040 | 2026-06-23 | chore: remove docs/superpowers from tracking, add to gitignore | accepted | — |
| 0041 | 2026-06-23 | feat: add auto-tdd, session-memory, initiative-create/edit skills; add contrarian-review Mode 1 | accepted | — |
| 0042 | 2026-06-24 | fix: re-apply skill fixes lost during rebase (frontmatter + sections) | accepted | — |
| 0043 | 2026-06-24 | chore: contrarian review overhaul — source repo enforcement, naming cleanup, tests, docs | accepted | — |
| 0044 | 2026-07-01 | skill: add tmux-status-bar — tmux bar with project, git, and initiative context | accepted | — |
| 0045 | 2026-07-02 | fix: remove walter-worker- prefix from 4 skill frontmatter names | accepted | — |
| 0046 | 2026-07-14 | skill: add multi-model-team — GLM 5.2 architect + DeepSeek v4 Pro worker orchestration | accepted | — |
| 0047 | 2026-07-17 | fix: knowledge-repo is separate repo at different path, not under project/ | accepted | — |
| 0048 | 2026-07-17 | docs: clarify knowledge-repo is separate repo, add CLAUDE.md reference example | accepted | — |
| 0049 | 2026-07-17 | docs: add INDEX.md generation workflow + content summary column | accepted | — |
| 0050 | 2026-07-17 | refactor: filename must include type suffix | accepted | — |
| 0051 | 2026-07-17 | docs: add naming anti-pattern rule — no generic file names | accepted | — |
| 0052 | 2026-07-17 | feat: add state type (10 types). state files: dated, overwrite not append | accepted | — |
| 0053 | 2026-07-17 | fix: remove dates from suffix section examples | accepted | — |
| 0054 | 2026-07-17 | refactor: no dates on any file with Change Log (all 8 main types) | accepted | — |
| 0055 | 2026-07-17 | fix: split naming — dated vs dateless types | accepted | — |
| 0056 | 2026-07-17 | feat: add 22 skills migrated from walter-worker | accepted | — |
| 0057 | 2026-07-17 | feat: add doc-organize skill (9 doc types, 6 stages, INDEX.md) | accepted | — |
| 0058 | 2026-07-18 | skill: add image review gate + scatterbrain design system to youtube-research-pipeline | accepted | — |
| 0059 | 2026-07-18 | skill: add youtube-research-pipeline — end-to-end YouTube video research pipeline with 3-agent deep | accepted | — |
| 0060 | 2026-07-18 | skill: add pic-to-txt — extract text from image folders using OCR + LLM refinement | accepted | — |
| 0061 | 2026-07-18 | feat: add transcript refinement step using LLM + metadata + comments | accepted | — |
| 0062 | 2026-07-18 | feat: add screenshot+OCR tier for burned-in subtitles | accepted | — |
| 0063 | 2026-07-18 | feat: add full transcription pipeline to youtube-summarize skill | accepted | — |
| 0064 | 2026-07-18 | feat: add youtube-summarize skill for summarizing YouTube video content | accepted | — |
| 0065 | 2026-07-22 | skill: add transcribe-audio — local GPU Whisper audio-to-text | accepted | — |
| 0066 | 2026-07-22 | skill: add create-video-workflow v3 — 7-phase human-in-the-loop content factory | accepted | — |
| 0067 | 2026-07-22 | skill: enhance skill-create — add Phase 3 Precision & Examples with legal-clause bounds and 2-3 exam | accepted | — |
| 0068 | 2026-07-22 | docs: add orphan folder cleanup step to doc-organize reorganize workflow | accepted | — |
| 0069 | 2026-07-23 | skill(luma-event-scout): add Robotics Reading Club to seed calendars | accepted | — |
| 0070 | 2026-07-23 | skill(luma-event-scout): add form filling rules + verification gate | accepted | — |
| 0071 | 2026-07-23 | skill(luma-event-scout): move personal info to ~/.person_info.md | accepted | — |
| 0072 | 2026-07-23 | skill(luma-event-scout): replace scraping with public API, clean up failed approaches | accepted | — |
| 0073 | 2026-07-23 | skill(luma-event-scout): note __NEXT_DATA__ 20-event limit, add Playwright scroll strategy | accepted | — |
| 0074 | 2026-07-23 | skill(luma-event-scout): lower hackathon prize threshold to K+ | accepted | — |
| 0075 | 2026-07-23 | skill(luma-event-scout): add hackathon prize/host quality gates | accepted | — |
| 0076 | 2026-07-23 | skill(luma-event-scout): clarify hackathons are acceptable with speaker gate | accepted | — |
| 0077 | 2026-07-23 | skill(luma-event-scout): add __NEXT_DATA__ JSON extraction method | accepted | — |
| 0078 | 2026-07-23 | skill(luma-event-scout): expand to entire Bay Area — SF + South Bay + Peninsula | accepted | — |
| 0079 | 2026-07-23 | skill(luma-event-scout): add broad AI search, hard speaker gate, dual-list output | accepted | — |
| 0080 | unknown | Add 'variant': 'thinking-high' to the build agent in opencode config | accepted | — |
| 0081 | unknown | 重建三个平级的 skill 目录：walter-worker-skills、import-skills、personal-skills | accepted | — |
| 0082 | unknown | walter-worker-skills 和 personal-skills 下的 skill 在 name 字段加 walter-worker- 前缀，文件夹名不改；import-skills 不加前缀；修 | accepted | — |
| 0083 | unknown | 在 skill-create 的 Phase 0 增加 GitHub 搜索（≥10 repo）和 Web 搜索，并提供 import/吸收灵感/自建三种决策分支 | accepted | — |
| 0084 | unknown | 在 ~/.claude/CLAUDE.md 添加规则：每次请求至少问1-3个 clarify 问题，除非置信度≥90% | accepted | — |
| 0085 | unknown | 为 skill-import 增加 metadata.source_author 和 metadata.source_url 字段，并在 Quality Gates 中验证 | accepted | — |
| 0086 | unknown | 导入的 skill 放入独立的 import-skills/ 目录，而非 walter-worker-skills/import/ | accepted | — |
| 0087 | unknown | 保留并修复 skill-create 作为自举起点，而非从头重建 | accepted | — |
| 0088 | unknown | Follow exact skill-create process phases (0->1->2->3->4) for skill-edit creation | accepted | — |
| 0089 | unknown | Use provided requirements as user answers during interview (Phase 1) | accepted | — |
| 0090 | unknown | Accept default factor weights (Accuracy 0.4, Edge cases 0.3, Readability 0.15, Speed 0.1, Tool integ | accepted | — |
| 0091 | unknown | Build SKILL.md following opencode 5-field frontmatter format and CONVENTIONS.md body structure with | accepted | — |
| 0092 | unknown | Include anti-patterns section in SKILL.md | accepted | — |
| 0093 | unknown | Include quality gates section that blocks if violated (MUST gates) | accepted | — |
| 0094 | unknown | Present diff summary and get user approval before editing (Step 4) | accepted | — |
| 0095 | unknown | Use Edit tool for targeted changes, never Write on entire file, never create new file | accepted | — |
| 0096 | unknown | Run quality gates before commit; MUST gates block publish | accepted | — |
| 0097 | unknown | Use conventional commit message format: skill(<name>): <imperative verb> <description> | accepted | — |
| 0098 | unknown | Output only final SKILL.md content at end, not actually create files or commit | accepted | — |
| 0099 | unknown | Redirect to skill-create if target skill doesn't exist or change is ≥80% rewrite | accepted | — |
| 0100 | unknown | Skip interview phase and go directly to build with pre-specified requirements | accepted | — |
| 0101 | unknown | Use webfetch (preferred) or curl to fetch source SKILL.md | accepted | — |
| 0102 | unknown | Auto-convert frontmatter: map name to kebab-case, rewrite description to start with 'Use when...', d | accepted | — |
| 0103 | unknown | Auto-adapt body sections: map Philosophy→overview, Anti-Pattern→Anti-Patterns, Workflow→Process, Che | accepted | — |
| 0104 | unknown | Implement Ambiguity Triggers: ask user one question at a time only when mapping is ambiguous (no lic | accepted | — |
| 0105 | unknown | Define Quality Gates as MUST (block commit) and NICE (warn only) checklists | accepted | — |
| 0106 | unknown | Include Anti-Patterns section with four specific anti-patterns | accepted | — |
| 0107 | unknown | Target <150 lines but accept 186 lines due to required content (conversion table, gates, anti-patter | accepted | — |
| 0108 | unknown | Tighten NICE gate 'Body < 500 lines' to '< 150 lines' in skill-create | accepted | — |
| 0109 | unknown | Add 'Anti-Patterns section present' as NICE gate in skill-create | accepted | — |
| 0110 | unknown | Add 'Quality Gates section with MUST/NICE checkboxes' as NICE gate in skill-create | accepted | — |
| 0111 | unknown | Add 'Philosophy-driven overview' as NICE requirement in skill-create Phase 2 | accepted | — |
| 0112 | unknown | Add 'No deploy/ concept' prohibition as MUST gate in skill-create | accepted | — |
| 0113 | unknown | Add 'description ≤ 500 chars' as NICE gate in skill-create | accepted | — |
| 0114 | unknown | Accept Agent-B's assessment that skill-edit and skill-import have zero MUST violations | accepted | — |
| 0115 | unknown | Commit changes to skill-create and report with specific commit message | accepted | — |
| 0116 | unknown | Use main agent orchestration with stateless subagents for each round (con, pro, judge) in devil-advo | accepted | — |
| 0117 | unknown | Change output path for devil-advocate from project default to {project-path}/docs/devil-advocate/YYY | accepted | — |
| 0118 | unknown | Create two output files for devil-advocate: discussion.md (full debate) and report.md (summary). | accepted | — |
| 0119 | unknown | Limit debate to max 5 rounds, then fall back to 3-agent majority vote on unresolved points. | accepted | — |
| 0120 | unknown | Use triggers 'review spec', '杠精', 'devil advocate', 'adversarial review' for devil-advocate skill. | accepted | — |
| 0121 | unknown | Use sequential two-agent architecture (Collector then Reviewer) without auto-retry for work-review s | accepted | — |
| 0122 | unknown | Agent 1 (Collector) writes a test plan (scenarios, types, steps) but no executable test code. | accepted | — |
| 0123 | unknown | Agent 2 (Reviewer) executes the test plan by running existing UT/FT, writing Playwright for E2E, and | accepted | — |
| 0124 | unknown | Output for work-review goes to {project-path}/docs/work-review/YYYY-MM-DD-<topic>/ with acceptance.m | accepted | — |
| 0125 | unknown | Use triggers 'work review', 'acceptance', 'sign off', 'verify work' for work-review skill. | accepted | — |
| 0127 | 2026-09-25 | Consolidated fourteen per-day decision records into this single append-only history | accepted | — |
| 0128 | 2026-09-25 | Folded the design/ directory into the spec's Design sections; design is not one of the six types | accepted | — |
| 0129 | 2026-09-25 | Marked the skill-factory documents stale rather than rewriting them to match the code | accepted | — |
| 0130 | 2026-09-25 | Four documents keep their own section shapes instead of the standard template; reported, not forced | accepted | — |
| 0126 | unknown | Compress SKILL.md to under 150 lines to pass quality gate. | accepted | — |

## Evidence Appendix

Each entry preserves the rationale exactly as it was recorded, including the
alternatives that were rejected. Support content is kept verbatim.

### 0001 — fix: skill-create quality gate improvements from round-01 review

Status: accepted

1. fix: skill-create quality gate improvements from round-01 review
- **Source**: git-commit
- **Timestamp**: 2026-06-10T23:59:31-07:00
- **Context**: git commit 33e48d2e
- **Rationale**: committed change
- **Commit**: `33e48d2e`
- **Confidence**: high

### 0002 — docs: round-01 agent-B evaluation — both skills PASS

Status: accepted

2. docs: round-01 agent-B evaluation — both skills PASS
- **Source**: git-commit
- **Timestamp**: 2026-06-10T23:55:57-07:00
- **Context**: git commit d9baa432
- **Rationale**: committed change
- **Commit**: `d9baa432`
- **Confidence**: high

### 0003 — skill: add skill-edit and skill-import from round-01 Agent-A

Status: accepted

3. skill: add skill-edit and skill-import from round-01 Agent-A
- **Source**: git-commit
- **Timestamp**: 2026-06-10T23:53:49-07:00
- **Context**: git commit 1d7bb7ed
- **Rationale**: committed change
- **Commit**: `1d7bb7ed`
- **Confidence**: high

### 0004 — chore: remove ai-worker-skills, fix skill-create description and references

Status: accepted

4. chore: remove ai-worker-skills, fix skill-create description and references
- **Source**: git-commit
- **Timestamp**: 2026-06-10T23:47:31-07:00
- **Context**: git commit 8cb87bec
- **Rationale**: committed change
- **Commit**: `8cb87bec`
- **Confidence**: high

### 0005 — docs: implementation plan for skill-factory bootstrap

Status: accepted

5. docs: implementation plan for skill-factory bootstrap
- **Source**: git-commit
- **Timestamp**: 2026-06-10T23:47:03-07:00
- **Context**: git commit 8ce5ae73
- **Rationale**: committed change
- **Commit**: `8ce5ae73`
- **Confidence**: high

### 0006 — docs: add skill-factory bootstrap design spec

Status: accepted

6. docs: add skill-factory bootstrap design spec
- **Source**: git-commit
- **Timestamp**: 2026-06-10T23:43:57-07:00
- **Context**: git commit 5dcb52c7
- **Rationale**: committed change
- **Commit**: `5dcb52c7`
- **Confidence**: high

### 0007 — refactor: move skills into walter-worker-skills namespace

Status: accepted

7. refactor: move skills into walter-worker-skills namespace
- **Source**: git-commit
- **Timestamp**: 2026-06-10T21:14:15-07:00
- **Context**: git commit 54496dad
- **Rationale**: committed change
- **Commit**: `54496dad`
- **Confidence**: high

### 0008 — feat: initialize skill-factory project with skill-create

Status: accepted

8. feat: initialize skill-factory project with skill-create
- **Source**: git-commit
- **Timestamp**: 2026-06-10T21:10:17-07:00
- **Context**: git commit 5d9747e9
- **Rationale**: committed change
- **Commit**: `5d9747e9`
- **Confidence**: high

### 0009 — Public open source repository

Status: accepted

9. Public open source repository
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: User originally chose private local, but later changed to public open source.
- **Rationale**: To share skills with the community and enable collaboration.
- **Alternatives rejected**: Private local, Public + private hybrid
- **Confidence**: high

### 0010 — Directory structure: ai-worker-skills/ for own skills, import/ for imported, personal/ for private

Status: accepted

10. Directory structure: ai-worker-skills/ for own skills, import/ for imported, personal/ for private
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: Need to organize skills by source and visibility.
- **Rationale**: Clear separation; personal/ is gitignored for privacy; import/ has metadata for attribution.
- **Alternatives rejected**: Flat all in one directory, Nested by author only
- **Confidence**: high

### 0011 — Naming convention: ai-worker-skills get prefix 'ai-worker-', imports keep original name

Status: accepted

11. Naming convention: ai-worker-skills get prefix 'ai-worker-', imports keep original name
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: User wanted brand recognition for own skills and clarity.
- **Rationale**: Easy to identify sources in tool UI; imports preserve upstream identity.
- **Alternatives rejected**: Same prefix for all, No prefix
- **Confidence**: high

### 0012 — Use Claude Code local marketplace via extraKnownMarketplaces

Status: accepted

12. Use Claude Code local marketplace via extraKnownMarketplaces
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: Need a standard way to install skills.
- **Rationale**: Native support; no extra scripts for Claude; OpenCode uses separate symlink approach.
- **Alternatives rejected**: Symlink-only, Custom install script for each tool
- **Confidence**: high

### 0013 — skill-import skill behavior: fetch, extract, write metadata, register in marketplace

Status: accepted

13. skill-import skill behavior: fetch, extract, write metadata, register in marketplace
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: Automate import of third-party skills with proper attribution.
- **Rationale**: Ensure license compliance and traceability; reusable workflow.
- **Alternatives rejected**: Manual copy-paste, Script without interactive prompts
- **Confidence**: high

### 0014 — META.yaml schema with source, upstream_commit, license, imported_at, imported_by, note

Status: accepted

14. META.yaml schema with source, upstream_commit, license, imported_at, imported_by, note
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: Need structured metadata for each import for compliance.
- **Rationale**: Standard format; easy to validate in CI; human-readable.
- **Alternatives rejected**: Only README note, JSON schema
- **Confidence**: high

### 0015 — CI workflow to validate import metadata completeness

Status: accepted

15. CI workflow to validate import metadata completeness
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: Ensure all imports meet attribution requirements.
- **Rationale**: Automated enforcement; prevent incomplete contributions.
- **Alternatives rejected**: Manual review only
- **Confidence**: high

### 0016 — Test flat vs nested SKILL.md structure

Status: accepted

16. Test flat vs nested SKILL.md structure
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: User questioned deep nesting (skills/<name>/SKILL.md).
- **Rationale**: Validate compatibility with Claude Code marketplace; both passed, so may adopt flat structure for simplicity.
- **Alternatives rejected**: Assuming nested required
- **Confidence**: medium

### 0017 — OpenCode installation: git plugin + project-level symlink

Status: accepted

17. OpenCode installation: git plugin + project-level symlink
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: OpenCode does not support marketplace natively.
- **Rationale**: Git plugin offers easy sharing; symlink for per-project control.
- **Alternatives rejected**: Only symlink, Only git plugin
- **Confidence**: high

### 0018 — Personal skills symlinked directly, gitignored, not in marketplace

Status: accepted

18. Personal skills symlinked directly, gitignored, not in marketplace
- **Source**: opencode
- **Timestamp**: 2026-06-10
- **Context**: User wants private skills not exposed in public repo.
- **Rationale**: Privacy; simplifies git management; still usable via symlink.
- **Alternatives rejected**: Encrypted storage in repo, Separate private repo
- **Confidence**: high

### 0019 — skill: add walter-worker-devil-advocate — multi-agent adversarial review for specs and design docs

Status: accepted

1. skill: add walter-worker-devil-advocate — multi-agent adversarial review for specs and design docs
- **Source**: git-commit
- **Timestamp**: 2026-06-11T22:52:46-07:00
- **Context**: git commit 70ccdc4a
- **Rationale**: committed change
- **Commit**: `70ccdc4a`
- **Confidence**: high

### 0020 — skill: add 5 migrated coworker skills

Status: accepted

2. skill: add 5 migrated coworker skills
- **Source**: git-commit
- **Timestamp**: 2026-06-11T01:03:50-07:00
- **Context**: git commit a5dcc4e9
- **Rationale**: committed change
- **Commit**: `a5dcc4e9`
- **Confidence**: high

### 0021 — feat(skill-create): Phase 0 multi-source search — GitHub (>=10 repos), web search, import-vs-inspire

Status: accepted

3. feat(skill-create): Phase 0 multi-source search — GitHub (>=10 repos), web search, import-vs-inspire
- **Source**: git-commit
- **Timestamp**: 2026-06-11T00:19:02-07:00
- **Context**: git commit d30f01c0
- **Rationale**: committed change
- **Commit**: `d30f01c0`
- **Confidence**: high

### 0022 — refactor: three-directory structure with walter-worker- prefix naming

Status: accepted

4. refactor: three-directory structure with walter-worker- prefix naming
- **Source**: git-commit
- **Timestamp**: 2026-06-11T00:14:52-07:00
- **Context**: git commit a2e47245
- **Rationale**: committed change
- **Commit**: `a2e47245`
- **Confidence**: high

### 0023 — fix(skill-import): add author preservation, import/ subdirectory, and anti-pattern for lost authorsh

Status: accepted

5. fix(skill-import): add author preservation, import/ subdirectory, and anti-pattern for lost authorsh
- **Source**: git-commit
- **Timestamp**: 2026-06-11T00:05:11-07:00
- **Context**: git commit 773594b9
- **Rationale**: committed change
- **Commit**: `773594b9`
- **Confidence**: high

### 0024 — docs: final verification logs and bootstrap summary

Status: accepted

6. docs: final verification logs and bootstrap summary
- **Source**: git-commit
- **Timestamp**: 2026-06-11T00:01:52-07:00
- **Context**: git commit 3c058b5e
- **Rationale**: committed change
- **Commit**: `3c058b5e`
- **Confidence**: high

### 0025 — fix(tdd): optimize description and overview per skill-factory conventions

Status: accepted

7. fix(tdd): optimize description and overview per skill-factory conventions
- **Source**: git-commit
- **Timestamp**: 2026-06-11T00:01:21-07:00
- **Context**: git commit d98ed8d3
- **Rationale**: committed change
- **Commit**: `d98ed8d3`
- **Confidence**: high

### 0026 — skill: import tdd from mattpocock/skills

Status: accepted

8. skill: import tdd from mattpocock/skills
- **Source**: git-commit
- **Timestamp**: 2026-06-11T00:00:49-07:00
- **Context**: git commit eed365ce
- **Rationale**: committed change
- **Commit**: `eed365ce`
- **Confidence**: high

### 0027 — skill: add walter-worker-work-review — 2-agent gatekeeper for work acceptance sign-off

Status: accepted

1. skill: add walter-worker-work-review — 2-agent gatekeeper for work acceptance sign-off
- **Source**: git-commit
- **Timestamp**: 2026-06-12T01:31:08-07:00
- **Context**: git commit 01f533c9
- **Rationale**: committed change
- **Commit**: `01f533c9`
- **Confidence**: high

### 0028 — skill: add walter-worker-contrarian-review — 5-agent adversarial document review

Status: accepted

1. skill: add walter-worker-contrarian-review — 5-agent adversarial document review
- **Source**: git-commit
- **Timestamp**: 2026-06-18T21:26:45-07:00
- **Context**: git commit 3a54ffc6
- **Rationale**: committed change
- **Commit**: `3a54ffc6`
- **Confidence**: high

### 0029 — chore: remove self-heal/self-analyze from personal-skills (in walter-worker-skills)

Status: accepted

1. chore: remove self-heal/self-analyze from personal-skills (in walter-worker-skills)
- **Source**: git-commit
- **Timestamp**: 2026-06-23T23:29:10-07:00
- **Context**: git commit bd9bb024
- **Rationale**: committed change
- **Commit**: `bd9bb024`
- **Confidence**: high

### 0030 — chore: remove self-strain

Status: accepted

2. chore: remove self-strain
- **Source**: git-commit
- **Timestamp**: 2026-06-23T23:28:01-07:00
- **Context**: git commit 06a4e020
- **Rationale**: committed change
- **Commit**: `06a4e020`
- **Confidence**: high

### 0031 — fix: add english-grammar-fix (was untracked)

Status: accepted

3. fix: add english-grammar-fix (was untracked)
- **Source**: git-commit
- **Timestamp**: 2026-06-23T23:26:39-07:00
- **Context**: git commit c329159c
- **Rationale**: committed change
- **Commit**: `c329159c`
- **Confidence**: high

### 0032 — refactor: rename self-patch to english-grammar-fix

Status: accepted

4. refactor: rename self-patch to english-grammar-fix
- **Source**: git-commit
- **Timestamp**: 2026-06-23T23:26:27-07:00
- **Context**: git commit 7226d537
- **Rationale**: committed change
- **Commit**: `7226d537`
- **Confidence**: high

### 0033 — chore: remove skills deleted from walter-worker (flow-*, connect-*, doc-review, bug-sleuth, bug-create

Status: accepted

5. chore: remove skills deleted from walter-worker (flow-*, connect-*, doc-review, bug-sleuth, bug-create
- **Source**: git-commit
- **Timestamp**: 2026-06-23T23:25:08-07:00
- **Context**: git commit 1b48039a
- **Rationale**: committed change
- **Commit**: `1b48039a`
- **Confidence**: high

### 0034 — chore: remove gate-* skills (not in walter-worker scope)

Status: accepted

6. chore: remove gate-* skills (not in walter-worker scope)
- **Source**: git-commit
- **Timestamp**: 2026-06-23T23:24:43-07:00
- **Context**: git commit 82c4563a
- **Rationale**: committed change
- **Commit**: `82c4563a`
- **Confidence**: high

### 0035 — chore: remove self-init (walter-worker skills/init/ is more current)

Status: accepted

7. chore: remove self-init (walter-worker skills/init/ is more current)
- **Source**: git-commit
- **Timestamp**: 2026-06-23T23:23:30-07:00
- **Context**: git commit 887a719b
- **Rationale**: committed change
- **Commit**: `887a719b`
- **Confidence**: high

### 0036 — feat: add self-heal and self-analyze skills

Status: accepted

8. feat: add self-heal and self-analyze skills
- **Source**: git-commit
- **Timestamp**: 2026-06-23T23:11:04-07:00
- **Context**: git commit dce0d79c
- **Rationale**: committed change
- **Commit**: `dce0d79c`
- **Confidence**: high

### 0037 — chore: remove session-memory (moved to walter-worker)

Status: accepted

9. chore: remove session-memory (moved to walter-worker)
- **Source**: git-commit
- **Timestamp**: 2026-06-23T22:59:08-07:00
- **Context**: git commit fca74392
- **Rationale**: committed change
- **Commit**: `fca74392`
- **Confidence**: high

### 0038 — chore: remove initiative-create/edit (moved to walter-worker)

Status: accepted

10. chore: remove initiative-create/edit (moved to walter-worker)
- **Source**: git-commit
- **Timestamp**: 2026-06-23T22:58:43-07:00
- **Context**: git commit 4d02f4cd
- **Rationale**: committed change
- **Commit**: `4d02f4cd`
- **Confidence**: high

### 0039 — refactor: rename skills to simplified naming, migrate 21 AI coworker skills

Status: accepted

11. refactor: rename skills to simplified naming, migrate 21 AI coworker skills
- **Source**: git-commit
- **Timestamp**: 2026-06-23T22:18:22-07:00
- **Context**: git commit 3395648c
- **Rationale**: committed change
- **Commit**: `3395648c`
- **Confidence**: high

### 0040 — chore: remove docs/superpowers from tracking, add to gitignore

Status: accepted

12. chore: remove docs/superpowers from tracking, add to gitignore
- **Source**: git-commit
- **Timestamp**: 2026-06-23T21:38:41-07:00
- **Context**: git commit add4f31e
- **Rationale**: committed change
- **Commit**: `add4f31e`
- **Confidence**: high

### 0041 — feat: add auto-tdd, session-memory, initiative-create/edit skills; add contrarian-review Mode 1

Status: accepted

13. feat: add auto-tdd, session-memory, initiative-create/edit skills; add contrarian-review Mode 1
- **Source**: git-commit
- **Timestamp**: 2026-06-23T21:36:13-07:00
- **Context**: git commit 7bfe010f
- **Rationale**: committed change
- **Commit**: `7bfe010f`
- **Confidence**: high

### 0042 — fix: re-apply skill fixes lost during rebase (frontmatter + sections)

Status: accepted

1. fix: re-apply skill fixes lost during rebase (frontmatter + sections)
- **Source**: git-commit
- **Timestamp**: 2026-06-24T00:27:37-07:00
- **Context**: git commit cca25cd5
- **Rationale**: committed change
- **Commit**: `cca25cd5`
- **Confidence**: high

### 0043 — chore: contrarian review overhaul — source repo enforcement, naming cleanup, tests, docs

Status: accepted

2. chore: contrarian review overhaul — source repo enforcement, naming cleanup, tests, docs
- **Source**: git-commit
- **Timestamp**: 2026-06-24T00:26:28-07:00
- **Context**: git commit 559834af
- **Rationale**: committed change
- **Commit**: `559834af`
- **Confidence**: high

### 0044 — skill: add tmux-status-bar — tmux bar with project, git, and initiative context

Status: accepted

1. skill: add tmux-status-bar — tmux bar with project, git, and initiative context
- **Source**: git-commit
- **Timestamp**: 2026-07-01T22:05:37-07:00
- **Context**: git commit 5cc3d4bc
- **Rationale**: committed change
- **Commit**: `5cc3d4bc`
- **Confidence**: high

### 0045 — fix: remove walter-worker- prefix from 4 skill frontmatter names

Status: accepted

1. fix: remove walter-worker- prefix from 4 skill frontmatter names
- **Source**: git-commit
- **Timestamp**: 2026-07-02T12:22:15-07:00
- **Context**: git commit bc4d6cc0
- **Rationale**: committed change
- **Commit**: `bc4d6cc0`
- **Confidence**: high

### 0046 — skill: add multi-model-team — GLM 5.2 architect + DeepSeek v4 Pro worker orchestration

Status: accepted

1. skill: add multi-model-team — GLM 5.2 architect + DeepSeek v4 Pro worker orchestration
- **Source**: git-commit
- **Timestamp**: 2026-07-14T12:36:08-07:00
- **Context**: git commit 56f3e001
- **Rationale**: committed change
- **Commit**: `56f3e001`
- **Confidence**: high

### 0047 — fix: knowledge-repo is separate repo at different path, not under project/

Status: accepted

1. fix: knowledge-repo is separate repo at different path, not under project/
- **Source**: git-commit
- **Timestamp**: 2026-07-17T13:36:12-07:00
- **Context**: git commit 9aa3483d
- **Rationale**: committed change
- **Commit**: `9aa3483d`
- **Confidence**: high

### 0048 — docs: clarify knowledge-repo is separate repo, add CLAUDE.md reference example

Status: accepted

2. docs: clarify knowledge-repo is separate repo, add CLAUDE.md reference example
- **Source**: git-commit
- **Timestamp**: 2026-07-17T13:27:46-07:00
- **Context**: git commit 6f4608e2
- **Rationale**: committed change
- **Commit**: `6f4608e2`
- **Confidence**: high

### 0049 — docs: add INDEX.md generation workflow + content summary column

Status: accepted

3. docs: add INDEX.md generation workflow + content summary column
- **Source**: git-commit
- **Timestamp**: 2026-07-17T13:25:35-07:00
- **Context**: git commit 3ee687d2
- **Rationale**: committed change
- **Commit**: `3ee687d2`
- **Confidence**: high

### 0050 — refactor: filename must include type suffix

Status: accepted

4. refactor: filename must include type suffix
- **Source**: git-commit
- **Timestamp**: 2026-07-17T12:57:24-07:00
- **Context**: git commit 8dc7afa9
- **Rationale**: committed change
- **Commit**: `8dc7afa9`
- **Confidence**: high

### 0051 — docs: add naming anti-pattern rule — no generic file names

Status: accepted

5. docs: add naming anti-pattern rule — no generic file names
- **Source**: git-commit
- **Timestamp**: 2026-07-17T12:56:15-07:00
- **Context**: git commit 004def01
- **Rationale**: committed change
- **Commit**: `004def01`
- **Confidence**: high

### 0052 — feat: add state type (10 types). state files: dated, overwrite not append

Status: accepted

6. feat: add state type (10 types). state files: dated, overwrite not append
- **Source**: git-commit
- **Timestamp**: 2026-07-17T12:09:19-07:00
- **Context**: git commit 46eaae74
- **Rationale**: committed change
- **Commit**: `46eaae74`
- **Confidence**: high

### 0053 — fix: remove dates from suffix section examples

Status: accepted

7. fix: remove dates from suffix section examples
- **Source**: git-commit
- **Timestamp**: 2026-07-17T12:06:14-07:00
- **Context**: git commit af1689db
- **Rationale**: committed change
- **Commit**: `af1689db`
- **Confidence**: high

### 0054 — refactor: no dates on any file with Change Log (all 8 main types)

Status: accepted

8. refactor: no dates on any file with Change Log (all 8 main types)
- **Source**: git-commit
- **Timestamp**: 2026-07-17T12:06:05-07:00
- **Context**: git commit 634494c5
- **Rationale**: committed change
- **Commit**: `634494c5`
- **Confidence**: high

### 0055 — fix: split naming — dated vs dateless types

Status: accepted

9. fix: split naming — dated vs dateless types
- **Source**: git-commit
- **Timestamp**: 2026-07-17T12:01:07-07:00
- **Context**: git commit 951491e8
- **Rationale**: committed change
- **Commit**: `951491e8`
- **Confidence**: high

### 0056 — feat: add 22 skills migrated from walter-worker

Status: accepted

10. feat: add 22 skills migrated from walter-worker
- **Source**: git-commit
- **Timestamp**: 2026-07-17T09:51:05-07:00
- **Context**: git commit aaa06765
- **Rationale**: committed change
- **Commit**: `aaa06765`
- **Confidence**: high

### 0057 — feat: add doc-organize skill (9 doc types, 6 stages, INDEX.md)

Status: accepted

11. feat: add doc-organize skill (9 doc types, 6 stages, INDEX.md)
- **Source**: git-commit
- **Timestamp**: 2026-07-17T09:49:29-07:00
- **Context**: git commit ee7c7087
- **Rationale**: committed change
- **Commit**: `ee7c7087`
- **Confidence**: high

### 0058 — skill: add image review gate + scatterbrain design system to youtube-research-pipeline

Status: accepted

1. skill: add image review gate + scatterbrain design system to youtube-research-pipeline
- **Source**: git-commit
- **Timestamp**: 2026-07-18T23:31:53-07:00
- **Context**: git commit 70959e94
- **Rationale**: committed change
- **Commit**: `70959e94`
- **Confidence**: high

### 0059 — skill: add youtube-research-pipeline — end-to-end YouTube video research pipeline with 3-agent deep

Status: accepted

2. skill: add youtube-research-pipeline — end-to-end YouTube video research pipeline with 3-agent deep 
- **Source**: git-commit
- **Timestamp**: 2026-07-18T22:54:34-07:00
- **Context**: git commit d7723a20
- **Rationale**: committed change
- **Commit**: `d7723a20`
- **Confidence**: high

### 0060 — skill: add pic-to-txt — extract text from image folders using OCR + LLM refinement

Status: accepted

3. skill: add pic-to-txt — extract text from image folders using OCR + LLM refinement
- **Source**: git-commit
- **Timestamp**: 2026-07-18T22:27:50-07:00
- **Context**: git commit 1e029ae5
- **Rationale**: committed change
- **Commit**: `1e029ae5`
- **Confidence**: high

### 0061 — feat: add transcript refinement step using LLM + metadata + comments

Status: accepted

4. feat: add transcript refinement step using LLM + metadata + comments
- **Source**: git-commit
- **Timestamp**: 2026-07-18T22:04:58-07:00
- **Context**: git commit d64e05c0
- **Rationale**: committed change
- **Commit**: `d64e05c0`
- **Confidence**: high

### 0062 — feat: add screenshot+OCR tier for burned-in subtitles

Status: accepted

5. feat: add screenshot+OCR tier for burned-in subtitles
- **Source**: git-commit
- **Timestamp**: 2026-07-18T22:02:48-07:00
- **Context**: git commit b04f00aa
- **Rationale**: committed change
- **Commit**: `b04f00aa`
- **Confidence**: high

### 0063 — feat: add full transcription pipeline to youtube-summarize skill

Status: accepted

6. feat: add full transcription pipeline to youtube-summarize skill
- **Source**: git-commit
- **Timestamp**: 2026-07-18T22:01:38-07:00
- **Context**: git commit cd0e658d
- **Rationale**: committed change
- **Commit**: `cd0e658d`
- **Confidence**: high

### 0064 — feat: add youtube-summarize skill for summarizing YouTube video content

Status: accepted

7. feat: add youtube-summarize skill for summarizing YouTube video content
- **Source**: git-commit
- **Timestamp**: 2026-07-18T21:56:09-07:00
- **Context**: git commit db0261dd
- **Rationale**: committed change
- **Commit**: `db0261dd`
- **Confidence**: high

### 0065 — skill: add transcribe-audio — local GPU Whisper audio-to-text

Status: accepted

1. skill: add transcribe-audio — local GPU Whisper audio-to-text
- **Source**: git-commit
- **Timestamp**: 2026-07-22T23:42:53-07:00
- **Context**: git commit ee5f3d5a
- **Rationale**: committed change
- **Commit**: `ee5f3d5a`
- **Confidence**: high

### 0066 — skill: add create-video-workflow v3 — 7-phase human-in-the-loop content factory

Status: accepted

2. skill: add create-video-workflow v3 — 7-phase human-in-the-loop content factory
- **Source**: git-commit
- **Timestamp**: 2026-07-22T01:20:51-07:00
- **Context**: git commit c4159a94
- **Rationale**: committed change
- **Commit**: `c4159a94`
- **Confidence**: high

### 0067 — skill: enhance skill-create — add Phase 3 Precision & Examples with legal-clause bounds and 2-3 exam

Status: accepted

3. skill: enhance skill-create — add Phase 3 Precision & Examples with legal-clause bounds and 2-3 exam
- **Source**: git-commit
- **Timestamp**: 2026-07-22T00:56:39-07:00
- **Context**: git commit a7f57de6
- **Rationale**: committed change
- **Commit**: `a7f57de6`
- **Confidence**: high

### 0068 — docs: add orphan folder cleanup step to doc-organize reorganize workflow

Status: accepted

4. docs: add orphan folder cleanup step to doc-organize reorganize workflow
- **Source**: git-commit
- **Timestamp**: 2026-07-22T00:56:17-07:00
- **Context**: git commit fe9d34e8
- **Rationale**: committed change
- **Commit**: `fe9d34e8`
- **Confidence**: high

### 0069 — skill(luma-event-scout): add Robotics Reading Club to seed calendars

Status: accepted

1. skill(luma-event-scout): add Robotics Reading Club to seed calendars
- **Source**: git-commit
- **Timestamp**: 2026-07-23T23:18:39-07:00
- **Context**: git commit 5bfdb57e
- **Rationale**: committed change
- **Commit**: `5bfdb57e`
- **Confidence**: high

### 0070 — skill(luma-event-scout): add form filling rules + verification gate

Status: accepted

2. skill(luma-event-scout): add form filling rules + verification gate
- **Source**: git-commit
- **Timestamp**: 2026-07-23T22:41:17-07:00
- **Context**: git commit 04eb9caf
- **Rationale**: committed change
- **Commit**: `04eb9caf`
- **Confidence**: high

### 0071 — skill(luma-event-scout): move personal info to ~/.person_info.md

Status: accepted

3. skill(luma-event-scout): move personal info to ~/.person_info.md
- **Source**: git-commit
- **Timestamp**: 2026-07-23T22:32:38-07:00
- **Context**: git commit e169832b
- **Rationale**: committed change
- **Commit**: `e169832b`
- **Confidence**: high

### 0072 — skill(luma-event-scout): replace scraping with public API, clean up failed approaches

Status: accepted

4. skill(luma-event-scout): replace scraping with public API, clean up failed approaches
- **Source**: git-commit
- **Timestamp**: 2026-07-23T22:12:15-07:00
- **Context**: git commit 24d42641
- **Rationale**: committed change
- **Commit**: `24d42641`
- **Confidence**: high

### 0073 — skill(luma-event-scout): note __NEXT_DATA__ 20-event limit, add Playwright scroll strategy

Status: accepted

5. skill(luma-event-scout): note __NEXT_DATA__ 20-event limit, add Playwright scroll strategy
- **Source**: git-commit
- **Timestamp**: 2026-07-23T22:06:02-07:00
- **Context**: git commit 9e4fb21e
- **Rationale**: committed change
- **Commit**: `9e4fb21e`
- **Confidence**: high

### 0074 — skill(luma-event-scout): lower hackathon prize threshold to K+

Status: accepted

6. skill(luma-event-scout): lower hackathon prize threshold to K+
- **Source**: git-commit
- **Timestamp**: 2026-07-23T21:54:13-07:00
- **Context**: git commit ff935e3f
- **Rationale**: committed change
- **Commit**: `ff935e3f`
- **Confidence**: high

### 0075 — skill(luma-event-scout): add hackathon prize/host quality gates

Status: accepted

7. skill(luma-event-scout): add hackathon prize/host quality gates
- **Source**: git-commit
- **Timestamp**: 2026-07-23T21:52:48-07:00
- **Context**: git commit 0308f521
- **Rationale**: committed change
- **Commit**: `0308f521`
- **Confidence**: high

### 0076 — skill(luma-event-scout): clarify hackathons are acceptable with speaker gate

Status: accepted

8. skill(luma-event-scout): clarify hackathons are acceptable with speaker gate
- **Source**: git-commit
- **Timestamp**: 2026-07-23T21:50:49-07:00
- **Context**: git commit c629b15c
- **Rationale**: committed change
- **Commit**: `c629b15c`
- **Confidence**: high

### 0077 — skill(luma-event-scout): add __NEXT_DATA__ JSON extraction method

Status: accepted

9. skill(luma-event-scout): add __NEXT_DATA__ JSON extraction method
- **Source**: git-commit
- **Timestamp**: 2026-07-23T21:46:50-07:00
- **Context**: git commit c4fe0ad5
- **Rationale**: committed change
- **Commit**: `c4fe0ad5`
- **Confidence**: high

### 0078 — skill(luma-event-scout): expand to entire Bay Area — SF + South Bay + Peninsula

Status: accepted

10. skill(luma-event-scout): expand to entire Bay Area — SF + South Bay + Peninsula
- **Source**: git-commit
- **Timestamp**: 2026-07-23T21:43:01-07:00
- **Context**: git commit 74e78bcb
- **Rationale**: committed change
- **Commit**: `74e78bcb`
- **Confidence**: high

### 0079 — skill(luma-event-scout): add broad AI search, hard speaker gate, dual-list output

Status: accepted

11. skill(luma-event-scout): add broad AI search, hard speaker gate, dual-list output
- **Source**: git-commit
- **Timestamp**: 2026-07-23T21:39:16-07:00
- **Context**: git commit 0a50040c
- **Rationale**: committed change
- **Commit**: `0a50040c`
- **Confidence**: high

### 0080 — Add 'variant': 'thinking-high' to the build agent in opencode config

Status: accepted

1. Add 'variant': 'thinking-high' to the build agent in opencode config
- **Source**: opencode
- **Context**: User requested to change thinking effort
- **Rationale**: Thinking effort is controlled via variant field; existing config had no variant for build agent, so added thinking-high variant
- **Confidence**: high

### 0081 — 重建三个平级的 skill 目录：walter-worker-skills、import-skills、personal-skills

Status: accepted

2. 重建三个平级的 skill 目录：walter-worker-skills、import-skills、personal-skills
- **Source**: opencode
- **Context**: 原仓库结构混乱，用户明确要求三个独立目录存放不同来源的技能
- **Rationale**: 分离原生、导入和个人技能，便于管理和前缀规则实施
- **Alternatives rejected**: 原先的 walter-worker-skills/import/ 子目录
- **Confidence**: high

### 0082 — walter-worker-skills 和 personal-skills 下的 skill 在 name 字段加 walter-worker- 前缀，文件夹名不改；import-skills 不加前缀；修

Status: accepted

3. walter-worker-skills 和 personal-skills 下的 skill 在 name 字段加 walter-worker- 前缀，文件夹名不改；import-skills 不加前缀；修
- **Source**: opencode
- **Context**: 用户要求所有自身技能显示前缀，但文件夹保持原名
- **Rationale**: 满足显示需求同时避免大量文件夹重命名操作
- **Alternatives rejected**: 文件夹也重命名, 仅在安装后修改显示名
- **Confidence**: high

### 0083 — 在 skill-create 的 Phase 0 增加 GitHub 搜索（≥10 repo）和 Web 搜索，并提供 import/吸收灵感/自建三种决策分支

Status: accepted

4. 在 skill-create 的 Phase 0 增加 GitHub 搜索（≥10 repo）和 Web 搜索，并提供 import/吸收灵感/自建三种决策分支
- **Source**: opencode
- **Context**: 用户希望 skill-create 能从外部获取启发，支持复用或借鉴
- **Rationale**: 增强技能创建时的外部参考能力，提升创建质量
- **Alternatives rejected**: 仅限本地扫描
- **Confidence**: high

### 0084 — 在 ~/.claude/CLAUDE.md 添加规则：每次请求至少问1-3个 clarify 问题，除非置信度≥90%

Status: accepted

5. 在 ~/.claude/CLAUDE.md 添加规则：每次请求至少问1-3个 clarify 问题，除非置信度≥90%
- **Source**: opencode
- **Context**: 用户要求在所有任务中强制澄清需求
- **Rationale**: 减少误解，提高需求准确性；90%阈值避免过度打扰
- **Alternatives rejected**: 总是提问不设阈值
- **Confidence**: high

### 0085 — 为 skill-import 增加 metadata.source_author 和 metadata.source_url 字段，并在 Quality Gates 中验证

Status: accepted

6. 为 skill-import 增加 metadata.source_author 和 metadata.source_url 字段，并在 Quality Gates 中验证
- **Source**: opencode
- **Context**: 导入外部 skill 时需要保留原作者信息
- **Rationale**: 保证知识溯源，符合 open-source 规范
- **Alternatives rejected**: 不记录来源
- **Confidence**: high

### 0086 — 导入的 skill 放入独立的 import-skills/ 目录，而非 walter-worker-skills/import/

Status: accepted

7. 导入的 skill 放入独立的 import-skills/ 目录，而非 walter-worker-skills/import/
- **Source**: opencode
- **Context**: 用户明确要求三个平级目录，导入 skill 不应混合在工厂原生目录内
- **Rationale**: 保持目录职责清晰，避免混淆
- **Alternatives rejected**: walter-worker-skills/import/ 子目录
- **Confidence**: high

### 0087 — 保留并修复 skill-create 作为自举起点，而非从头重建

Status: accepted

8. 保留并修复 skill-create 作为自举起点，而非从头重建
- **Source**: opencode
- **Context**: skill-create 是创建其他技能的入口工具，需要先修复问题再使用
- **Rationale**: 确保自举系统正确运行，避免重复工作
- **Alternatives rejected**: 删除 skill-create 从零开始
- **Confidence**: high

### 0088 — Follow exact skill-create process phases (0->1->2->3->4) for skill-edit creation

Status: accepted

9. Follow exact skill-create process phases (0->1->2->3->4) for skill-edit creation
- **Source**: opencode
- **Context**: User instructed to follow skill-create process exactly
- **Rationale**: Ensures consistency and quality enforcement across all skills
- **Confidence**: high

### 0089 — Use provided requirements as user answers during interview (Phase 1)

Status: accepted

10. Use provided requirements as user answers during interview (Phase 1)
- **Source**: opencode
- **Context**: User role simulated answers based on requirements
- **Rationale**: Simulate realistic interview without actual human interaction
- **Alternatives rejected**: Real-time human interview
- **Confidence**: medium

### 0090 — Accept default factor weights (Accuracy 0.4, Edge cases 0.3, Readability 0.15, Speed 0.1, Tool integ

Status: accepted

11. Accept default factor weights (Accuracy 0.4, Edge cases 0.3, Readability 0.15, Speed 0.1, Tool integ
- **Source**: opencode
- **Context**: AI asked if user accepts defaults; user answered yes
- **Rationale**: No need to customize
- **Alternatives rejected**: Custom weights
- **Confidence**: high

### 0091 — Build SKILL.md following opencode 5-field frontmatter format and CONVENTIONS.md body structure with

Status: accepted

12. Build SKILL.md following opencode 5-field frontmatter format and CONVENTIONS.md body structure with 
- **Source**: opencode
- **Context**: Phase 2 requirement
- **Rationale**: Adhere to project conventions
- **Alternatives rejected**: Different format or longer document
- **Confidence**: high

### 0092 — Include anti-patterns section in SKILL.md

Status: accepted

13. Include anti-patterns section in SKILL.md
- **Source**: opencode
- **Context**: Phase 2, instruction to include anti-patterns section, philosophy-driven approach
- **Rationale**: Prevent common mistakes
- **Confidence**: high

### 0093 — Include quality gates section that blocks if violated (MUST gates)

Status: accepted

14. Include quality gates section that blocks if violated (MUST gates)
- **Source**: opencode
- **Context**: Phase 2, required by skill-create process
- **Rationale**: Enforce quality
- **Confidence**: high

### 0094 — Present diff summary and get user approval before editing (Step 4)

Status: accepted

15. Present diff summary and get user approval before editing (Step 4)
- **Source**: opencode
- **Context**: Workflow requirement
- **Rationale**: Ensure user consent and review
- **Alternatives rejected**: Editing without approval
- **Confidence**: high

### 0095 — Use Edit tool for targeted changes, never Write on entire file, never create new file

Status: accepted

16. Use Edit tool for targeted changes, never Write on entire file, never create new file
- **Source**: opencode
- **Context**: Step 5 of process
- **Rationale**: Prevent overwriting or creating new files (skill-create's job)
- **Alternatives rejected**: Using Write tool
- **Confidence**: high

### 0096 — Run quality gates before commit; MUST gates block publish

Status: accepted

17. Run quality gates before commit; MUST gates block publish
- **Source**: opencode
- **Context**: Step 6 and Step 7
- **Rationale**: Ensure quality
- **Alternatives rejected**: Committing without verification
- **Confidence**: high

### 0097 — Use conventional commit message format: skill(<name>): <imperative verb> <description>

Status: accepted

18. Use conventional commit message format: skill(<name>): <imperative verb> <description>
- **Source**: opencode
- **Context**: Publish step
- **Rationale**: Standard for project
- **Confidence**: high

### 0098 — Output only final SKILL.md content at end, not actually create files or commit

Status: accepted

19. Output only final SKILL.md content at end, not actually create files or commit
- **Source**: opencode
- **Context**: Instructions at end
- **Rationale**: Avoid side effects in simulation
- **Alternatives rejected**: Actually writing to files
- **Confidence**: high

### 0099 — Redirect to skill-create if target skill doesn't exist or change is ≥80% rewrite

Status: accepted

20. Redirect to skill-create if target skill doesn't exist or change is ≥80% rewrite
- **Source**: opencode
- **Context**: Process Step 1 and Step 3
- **Rationale**: Scope boundary
- **Alternatives rejected**: Attempting to edit non-existent skill or full rewrite
- **Confidence**: high

### 0100 — Skip interview phase and go directly to build with pre-specified requirements

Status: accepted

21. Skip interview phase and go directly to build with pre-specified requirements
- **Source**: opencode
- **Context**: User instructed to skip Phase 1 interview and proceed to Phase 2 build using provided requirements.
- **Rationale**: Requirements were complete, no need for elicitation.
- **Alternatives rejected**: Conducting the interview phase to gather more details
- **Confidence**: high

### 0101 — Use webfetch (preferred) or curl to fetch source SKILL.md

Status: accepted

22. Use webfetch (preferred) or curl to fetch source SKILL.md
- **Source**: opencode
- **Context**: Workflow step 2: fetch source content.
- **Rationale**: webfetch is more integrated; curl is fallback.
- **Alternatives rejected**: Using only one tool, Manual copy-paste
- **Confidence**: high

### 0102 — Auto-convert frontmatter: map name to kebab-case, rewrite description to start with 'Use when...', d

Status: accepted

23. Auto-convert frontmatter: map name to kebab-case, rewrite description to start with 'Use when...', d
- **Source**: opencode
- **Context**: Frontmatter mapping required by requirements.
- **Rationale**: Standardize all skills to opencode 5-field format with consistent defaults.
- **Alternatives rejected**: Keeping original description verbatim, Asking user for all fields
- **Confidence**: high

### 0103 — Auto-adapt body sections: map Philosophy→overview, Anti-Pattern→Anti-Patterns, Workflow→Process, Che

Status: accepted

24. Auto-adapt body sections: map Philosophy→overview, Anti-Pattern→Anti-Patterns, Workflow→Process, Che
- **Source**: opencode
- **Context**: Body section mapping required to match CONVENTIONS.md structure.
- **Rationale**: All imported skills must follow the same structure for consistency and AI readability.
- **Alternatives rejected**: Keeping source section names, Adding more mappings without user input
- **Confidence**: high

### 0104 — Implement Ambiguity Triggers: ask user one question at a time only when mapping is ambiguous (no lic

Status: accepted

25. Implement Ambiguity Triggers: ask user one question at a time only when mapping is ambiguous (no lic
- **Source**: opencode
- **Context**: User requirement: ask ONE QUESTION AT A TIME only when ambiguous.
- **Rationale**: Minimize interruptions while ensuring correctness for edge cases.
- **Alternatives rejected**: Ask user to fill all gaps upfront, Silently guess all values
- **Confidence**: high

### 0105 — Define Quality Gates as MUST (block commit) and NICE (warn only) checklists

Status: accepted

26. Define Quality Gates as MUST (block commit) and NICE (warn only) checklists
- **Source**: opencode
- **Context**: Quality section required by build instructions.
- **Rationale**: Ensure accuracy and compliance; separate blocking from non-blocking checks.
- **Alternatives rejected**: Single list of all checks, No quality gates
- **Confidence**: high

### 0106 — Include Anti-Patterns section with four specific anti-patterns

Status: accepted

27. Include Anti-Patterns section with four specific anti-patterns
- **Source**: opencode
- **Context**: Required by build instructions to have anti-patterns section.
- **Rationale**: Prevent common mistakes during import (silent conversion, verbatim copy, skipped audit, write to existing dir).
- **Alternatives rejected**: Generic anti-patterns, Omit section
- **Confidence**: high

### 0107 — Target <150 lines but accept 186 lines due to required content (conversion table, gates, anti-patter

Status: accepted

28. Target <150 lines but accept 186 lines due to required content (conversion table, gates, anti-patter
- **Source**: opencode
- **Context**: User requirement 'Target < 150 lines'; output ended at 186.
- **Rationale**: Content completeness prioritized over strict line count; line count is soft target.
- **Alternatives rejected**: Cutting required sections to meet line target
- **Confidence**: medium

### 0108 — Tighten NICE gate 'Body < 500 lines' to '< 150 lines' in skill-create

Status: accepted

29. Tighten NICE gate 'Body < 500 lines' to '< 150 lines' in skill-create
- **Source**: opencode
- **Context**: Diagnosis of skill-create revealed the body line limit was too loose per CONVENTIONS.md requirement.
- **Rationale**: CONVENTIONS.md specifies body should be under 150 lines; the existing 500-line limit would allow overly long skills.
- **Alternatives rejected**: Keeping the limit at 500 lines
- **Confidence**: high

### 0109 — Add 'Anti-Patterns section present' as NICE gate in skill-create

Status: accepted

30. Add 'Anti-Patterns section present' as NICE gate in skill-create
- **Source**: opencode
- **Context**: skill-create lacked a requirement for an Anti-Patterns section, though downstream skills need it.
- **Rationale**: Ensures generated skills include anti-patterns, aligning with CONVENTIONS.md.
- **Confidence**: high

### 0110 — Add 'Quality Gates section with MUST/NICE checkboxes' as NICE gate in skill-create

Status: accepted

31. Add 'Quality Gates section with MUST/NICE checkboxes' as NICE gate in skill-create
- **Source**: opencode
- **Context**: skill-create did not require a Quality Gates section in generated skills.
- **Rationale**: Makes quality criteria explicit and traceable, improving skill consistency.
- **Confidence**: high

### 0111 — Add 'Philosophy-driven overview' as NICE requirement in skill-create Phase 2

Status: accepted

32. Add 'Philosophy-driven overview' as NICE requirement in skill-create Phase 2
- **Source**: opencode
- **Context**: Phase 2 instructions in skill-create were missing guidance to include a philosophy-driven overview.
- **Rationale**: Philosophical framing improves skill cohesion and user understanding.
- **Confidence**: medium

### 0112 — Add 'No deploy/ concept' prohibition as MUST gate in skill-create

Status: accepted

33. Add 'No deploy/ concept' prohibition as MUST gate in skill-create
- **Source**: opencode
- **Context**: CONVENTIONS.md prohibits deploy/ concept, but skill-create didn't check for it.
- **Rationale**: Prevents invalid skill structures from being created.
- **Confidence**: high

### 0113 — Add 'description ≤ 500 chars' as NICE gate in skill-create

Status: accepted

34. Add 'description ≤ 500 chars' as NICE gate in skill-create
- **Source**: opencode
- **Context**: CONVENTIONS.md recommends description length ≤500 characters, but skill-create didn't enforce it.
- **Rationale**: Keeps descriptions succinct and readable.
- **Confidence**: high

### 0114 — Accept Agent-B's assessment that skill-edit and skill-import have zero MUST violations

Status: accepted

35. Accept Agent-B's assessment that skill-edit and skill-import have zero MUST violations
- **Source**: opencode
- **Context**: Double-checked both skills against CONVENTIONS.md and found no issues.
- **Rationale**: Both skills pass all quality gates; no additional issues found.
- **Confidence**: high

### 0115 — Commit changes to skill-create and report with specific commit message

Status: accepted

36. Commit changes to skill-create and report with specific commit message
- **Source**: opencode
- **Context**: Changes required version control tracking.
- **Rationale**: Follow standard development workflow for traceability.
- **Confidence**: high

### 0116 — Use main agent orchestration with stateless subagents for each round (con, pro, judge) in devil-advo

Status: accepted

37. Use main agent orchestration with stateless subagents for each round (con, pro, judge) in devil-advo
- **Source**: opencode
- **Context**: During brainstorming for devil-advocate skill.
- **Rationale**: Clear state management, debuggable, follows project's existing pattern (Agent-A/B/C bootstrap).
- **Alternatives rejected**: Persistent sessions with task_id for cross-round memory (Scheme B) - risk of state drift and debugging difficulty.
- **Confidence**: high

### 0117 — Change output path for devil-advocate from project default to {project-path}/docs/devil-advocate/YYY

Status: accepted

38. Change output path for devil-advocate from project default to {project-path}/docs/devil-advocate/YYY
- **Source**: opencode
- **Context**: User requested a specific location (docs/devil-advocate) instead of docs/superpowers/devil-advocate.
- **Rationale**: Direct user request.
- **Alternatives rejected**: Staying at docs/superpowers/
- **Confidence**: high

### 0118 — Create two output files for devil-advocate: discussion.md (full debate) and report.md (summary).

Status: accepted

39. Create two output files for devil-advocate: discussion.md (full debate) and report.md (summary).
- **Source**: opencode
- **Context**: User asked '有没有discussion.md' (is there a discussion.md?).
- **Rationale**: Separate raw debate from human-readable summary.
- **Alternatives rejected**: Single report.md containing everything.
- **Confidence**: high

### 0119 — Limit debate to max 5 rounds, then fall back to 3-agent majority vote on unresolved points.

Status: accepted

40. Limit debate to max 5 rounds, then fall back to 3-agent majority vote on unresolved points.
- **Source**: opencode
- **Context**: Part of devil-advocate process design.
- **Rationale**: Prevent infinite loops; voting provides tie-breaker.
- **Alternatives rejected**: No limit or different round count.
- **Confidence**: high

### 0120 — Use triggers 'review spec', '杠精', 'devil advocate', 'adversarial review' for devil-advocate skill.

Status: accepted

41. Use triggers 'review spec', '杠精', 'devil advocate', 'adversarial review' for devil-advocate skill.
- **Source**: opencode
- **Context**: Defining skill activation.
- **Rationale**: Match user's intended use cases.
- **Alternatives rejected**: Single trigger only.
- **Confidence**: medium

### 0121 — Use sequential two-agent architecture (Collector then Reviewer) without auto-retry for work-review s

Status: accepted

42. Use sequential two-agent architecture (Collector then Reviewer) without auto-retry for work-review s
- **Source**: opencode
- **Context**: During work-review brainstorming.
- **Rationale**: Simple, clear separation of concerns; user manually re-triggers after fixes.
- **Alternatives rejected**: Cyclic review with automatic re-check (Scheme B) - risk of infinite loop and skill responsibility creep.
- **Confidence**: high

### 0122 — Agent 1 (Collector) writes a test plan (scenarios, types, steps) but no executable test code.

Status: accepted

43. Agent 1 (Collector) writes a test plan (scenarios, types, steps) but no executable test code.
- **Source**: opencode
- **Context**: User corrected that Agent 1 should not write test code, only test plan.
- **Rationale**: Keep Agent 1's role limited to analysis and specification; Agent 2 executes.
- **Alternatives rejected**: Agent 1 writing actual test scripts.
- **Confidence**: high

### 0123 — Agent 2 (Reviewer) executes the test plan by running existing UT/FT, writing Playwright for E2E, and

Status: accepted

44. Agent 2 (Reviewer) executes the test plan by running existing UT/FT, writing Playwright for E2E, and
- **Source**: opencode
- **Context**: User specified that Agent 2 should actually run tests, possibly write code, and use Playwright/dev's tests.
- **Rationale**: Agent 2 validates each acceptance criterion through real execution.
- **Alternatives rejected**: Agent 2 only analyzing code without running tests.
- **Confidence**: high

### 0124 — Output for work-review goes to {project-path}/docs/work-review/YYYY-MM-DD-<topic>/ with acceptance.m

Status: accepted

45. Output for work-review goes to {project-path}/docs/work-review/YYYY-MM-DD-<topic>/ with acceptance.m
- **Source**: opencode
- **Context**: During work-review output structure design.
- **Rationale**: Consistent with devil-advocate pattern, easy to find.
- **Alternatives rejected**: Output to default skill directory.
- **Confidence**: high

### 0125 — Use triggers 'work review', 'acceptance', 'sign off', 'verify work' for work-review skill.

Status: accepted

46. Use triggers 'work review', 'acceptance', 'sign off', 'verify work' for work-review skill.
- **Source**: opencode
- **Context**: Defining skill activation.
- **Rationale**: Aligns with typical developer terminology.
- **Alternatives rejected**: Single or different triggers.
- **Confidence**: medium

### 0126 — Compress SKILL.md to under 150 lines to pass quality gate.

Status: accepted

47. Compress SKILL.md to under 150 lines to pass quality gate.
- **Source**: opencode
- **Context**: After writing devil-advocate SKILL.md, it was 271 lines, then reduced to 175, then 155.
- **Rationale**: Line count limit (NICE: 150) enforced by project guidelines.
- **Alternatives rejected**: Leaving as is and ignoring quality gate.
- **Confidence**: high

### 0127 — Consolidated fourteen per-day decision records into this single append-only history

Status: accepted

Date: 2026-09-25


### 0128 — Folded the design/ directory into the spec's Design sections; design is not one of the six types

Status: accepted

Date: 2026-09-25


### 0129 — Marked the skill-factory documents stale rather than rewriting them to match the code

Status: accepted

Date: 2026-09-25


### 0130 — Four documents keep their own section shapes instead of the standard template; reported, not forced

Status: accepted

Date: 2026-09-25


## Change Log

| Date | Change |
|------|--------|
| 2026-07-26 | Auto-generated from session analysis into fourteen per-day records |
| 2026-09-25 | Consolidated into this single append-only history; 126 decisions preserved in full |
| 2026-09-25 | Added 0127-0130 recording the docs/features consolidation |

Consolidated from: `2026-06-10-fix-skill-create-quality-gate-improvements-from-r-decision.md`, `2026-06-11-skill-add-ai-coworker-devil-advocate--multi-agen-decision.md`, `2026-06-12-skill-add-ai-coworker-work-review--2-agent-gatek-decision.md`, `2026-06-18-skill-add-ai-coworker-contrarian-review--5-agent-decision.md`, `2026-06-23-chore-remove-self-healself-analyze-from-personal-decision.md`, `2026-06-24-fix-re-apply-skill-fixes-lost-during-rebase-fron-decision.md`, `2026-07-01-skill-add-tmux-status-bar--tmux-bar-with-project-decision.md`, `2026-07-02-fix-remove-ai-coworker--prefix-from-4-skill-front-decision.md`, `2026-07-14-skill-add-multi-model-team--glm-52-architect---decision.md`, `2026-07-17-fix-knowledge-repo-is-separate-repo-at-different--decision.md`, `2026-07-18-skill-add-image-review-gate--scatterbrain-design-decision.md`, `2026-07-22-skill-add-transcribe-audio--local-gpu-whisper-au-decision.md`, `2026-07-23-skillluma-event-scout-add-robotics-reading-club-decision.md`, `unknown-add-variant-thinking-high-to-the-build-agent--decision.md`
