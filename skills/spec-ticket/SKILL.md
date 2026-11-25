---
name: spec-ticket
description: |
  Use when an impl-plan is ready and its IMPL-* steps should become tickets.
  Opens one parent ticket per feature and one child ticket per IMPL in the
  configured tracker (local markdown, GitHub, or Jira), wires blocking edges
  from each IMPL's dependencies, and on rerun adds only new IMPLs.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - spec ticket
    - tickets from impl-plan
    - open tickets
    - impl to issues
    - track impl-plan
  when_to_use: |
    When a feature's impl-plan has passed spec-review and you want each IMPL
    tracked as a GitHub issue, Jira issue, or local ticket file. When the
    impl-plan gained new IMPLs and the tracker should catch up.
  when_not_to_use: |
    When there is no impl-plan yet — write it with spec-write first. When a
    blocking QUES is still open. When you want work re-sliced — the impl-plan
    owns the slicing. Never to write or update spec docs.
  audience:
    - developers
    - tech leads
  source_author: cicidi
  inspired_by: "mattpocock to-tickets — https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md"
---

# spec-ticket

Turn an impl-plan into tickets: one **parent** per feature, one **child** per `IMPL-*`.
One-way only: the tracker never writes back into spec docs.
Spec and rationale: `docs/features/skill-factory/features/spec-ticket/design/spec-ticket-design.md` (DSGN-A…N).
If this file and the design disagree, the design wins.

## Inputs

A feature name (`docs/features/<f>/`) or an impl-plan path. The **feature dir** is the parent of the
`impl-plan/` directory; `<f>` is its name. The design is `<feature dir>/design/<f>-design.md`.

## Process

### 1. Locate (DSGN-A)

Find `<feature dir>/impl-plan/*.md`. No file, or no `## IMPL-X — <title>` (or `### IMPL-X — <title>`) heading → stop:
"write the impl-plan with spec-write first".

### 2. Blocking-question gate (DSGN-B)

Read the design's `## Open Questions` table. The blocking column is headed `Blocking` or `阻塞`.
If any `QUES-*` row has `yes` or `是` there
(case-insensitive), stop and list those rows. Do not judge the answer cell. Create nothing.
No design file or no Open Questions table → nothing blocks; say so in the report.

### 3. Tracker (DSGN-C)

Look for a line `tracker: github | jira | local` in the project's `CLAUDE.local.md` (shared with
wayfinder). Missing line or file → `local`. Any other value → stop with an error.

### 4. Parse every IMPL (DSGN-D)

For each `## IMPL-X — <title>` or `### IMPL-X — <title>` section (until the next heading of the same or higher level):

- **deps**: every `IMPL-*` id after a `依赖` / `Depends on` label, anywhere in the section, up to the
  next label or line end. Conditional deps ("报告部分还依赖 IMPL-L") count.
- **blocks**: every `IMPL-*` id after a `挡住` / `Blocks` label.
- **non-IMPL text**: any dependency/blocks fragment that is not an IMPL id and not `无`/`none`
  (e.g. "本批 spec 修改完成") → keep for the report, never drop silently. A qualifier that only
  leads into another label ("报告部分还" before "依赖 IMPL-L") is not an item, and neither is a
  qualifier after an id ("IMPL-E 的报告部分" = an edge to IMPL-E).
- **done**: a sentence about this item itself says it is finished — `这一项已完成`, `这一项已经完成`,
  `这一项已于 … 完成`, `本项已完成` — or a line `Status: done` → no ticket; list it in the report.
  "IMPL-X 已完成后…" (a condition about another item) is not done.

### 5. Edges and order (DSGN-F)

A blocks B if B's deps name A **or** A's blocks name B (union). Report every edge stated on only
one side. Skip and report edges to unknown ids and edges where either end is done.
Topologically sort the remaining IMPLs (blockers first; ties in IMPL-id order). A cycle → stop and
report the IMPLs on it; create nothing.

### 6. Confirm (github / jira only)

List what will be created (parent if new, then each new IMPL with its blockers) and every blocking
edge to be added to an existing ticket (step 7.4); ask the user once. No new ticket and no edge
to add → do not ask.
Local mode does not ask.

### 7. Publish (DSGN-H, DSGN-N)

1. **Parent first.** Find the parent (map file, else title `[<f>] feature`); create it only if absent.
   Found by title but not in the map → add its map row now (`found <date>`).
2. **Children in order.** For each IMPL: find it (map file, else exact title); if found, record it and
   move on — never edit an existing ticket (the one exception is step 4). Found by title only →
   add its map row. Otherwise create it with its parent and blockers.
3. After each creation, record it immediately (map row, or the file itself in local mode).
4. If a new IMPL blocks an IMPL that already has a ticket, add that one blocking edge to the old
   ticket right after creating the new one; change nothing else on it. A new edge between two IMPLs
   that both already had tickets is not added in v1: report it.
5. IMPLs that disappeared from the plan: report only. Never close or edit. Changed IMPL text is not
   detected in v1.

### 8. Report (DSGN-L) — in chat, never into spec docs

Tracker; created (IMPL → ticket); already existed; skipped done IMPLs; one-sided edges; unknown ids;
edges to done IMPLs; non-IMPL dependency text; vanished IMPLs; label not applied; edges between
two existing tickets that were not added (step 7.4).

## Ticket content (DSGN-E, DSGN-N)

Titles: parent `[<f>] feature`; child `[<f>] IMPL-X — <IMPL title>`. Label `ready-for-agent` on children only
(GitHub: only if the repo has it — `gh label list --json name`; otherwise skip and report).

Parent body — links only, no copied content. List only the docs that exist; on github/jira the
paths become full URLs (see Links below):

```
Feature <f>.
- PRD: docs/features/<f>/prd/<f>-prd.md
- Design: docs/features/<f>/design/<f>-design.md
- Impl-plan: docs/features/<f>/impl-plan/<file>.md
Generated by spec-ticket. The spec docs are the source of truth.
```

Child body:

```
<IMPL section text verbatim except for the link rewrites below, without its heading (the title carries it), including its Verify / 完成标准 line>

Source: docs/features/<f>/impl-plan/<file>.md#<anchor>
Generated by spec-ticket from the impl-plan, which is the source of truth; edits here are not written back.
```

Blockers are not part of this body: each adapter records them its own way (local header line,
GitHub `--blocked-by`, Jira issue links).

Links in the child body (ARD-Q):
- `<anchor>` is GitHub's slug of the IMPL heading text: lowercase; drop every character that
  is not a letter, digit, space, `-` or `_` (CJK letters stay); each space becomes `-`.
  `### IMPL-B — 读侧 store` → `#impl-b--读侧-store`.
- Every relative markdown link copied from the IMPL text is resolved against the impl-plan file
  and rewritten as a repo-root path (`docs/features/<f>/design/x.md#sec`). An anchor-only link
  `(#x)` becomes `docs/features/<f>/impl-plan/<file>.md#x`.
- github: the Source path and those links become full URLs
  `https://github.com/<owner>/<repo>/blob/<default branch>/<path>` (`gh repo view --json
  nameWithOwner,defaultBranchRef`). jira: same full URLs when the repo has a GitHub remote.

## Adapters

All three implement: **find** (by exact title), **create** (with parent and blockers), **add edge**.

### local (DSGN-J)

Dir: `<feature dir>/raw/state/spec-ticket/issues/` (gitignored with `docs/features/**/raw/`).
Parent file `_feature.md`; child file `IMPL-X-<slug>.md`, or `IMPL-X.md` when the slug is empty.
Slug: lowercase the IMPL title (the part after `IMPL-X — `), replace each run of non-`a-z0-9`
chars with `-`, trim `-`.
The filename **is** the mapping — find = "does a file starting `IMPL-X` (followed by `-` or `.md`) exist". No map file.
`_feature.md` = `# [<f>] feature`, a blank line, the parent body (no label: the parent is not work for an agent).
Each child file starts with:

```
# [<f>] IMPL-X — <title>

Parent: _feature
Blocked by: IMPL-A (IMPL-A-<slug>.md), IMPL-C (IMPL-C.md)   ← or "none"
Labels: ready-for-agent
```

then the child body above. Adding an edge to an old ticket = append `, IMPL-X (<file>.md)` to its
`Blocked by:` line, or replace `none` with `IMPL-X (<file>.md)`.

### github (DSGN-I)

Needs gh ≥ 2.94 and `gh auth status` OK; otherwise stop (no fallback to local).

- find: `gh issue list --state all --json number,title --limit 1000`, exact title match.
- parent: `gh issue create --title "[<f>] feature" --body-file <tmp>` (no `ready-for-agent`)
- child: `gh issue create --title "<title>" --body-file <tmp> --parent <P> [--blocked-by n1,n2] [--label ready-for-agent]`
- add edge: `gh issue edit <old> --add-blocked-by <new>`
- Old self-hosted GitHub rejects `--blocked-by` / `--parent`: create without them and write
  `Blocked by: #n1, #n2` / `Parent: #P` lines into the body instead.

### jira (DSGN-K) — tested against a mock of the Cloud v3 API only, not a real Jira

Needs env `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`; check them at step 3,
before any request; any missing → stop, create nothing. Jira Cloud only, REST API v3; Data Center
is not supported (ARD-P). Auth `-u "$JIRA_EMAIL:$JIRA_API_TOKEN"`.

- labels: every issue gets `spec-ticket-<f>` (each char of `<f>` outside `a-z0-9-` becomes `-`);
  child Tasks also get `ready-for-agent`, the Epic does not.
- search once, before the first create, whenever any IMPL or the parent is missing from the map.
- find: `POST $JIRA_BASE_URL/rest/api/3/search/jql` with
  `{"jql":"project = $JIRA_PROJECT_KEY AND labels = \"spec-ticket-<f>\"","fields":["summary"],"maxResults":100}`
  (follow `nextPageToken` until `isLast`), then exact summary match. Search by label, not
  `summary ~`, because summary search is tokenized and can miss a title. Search results can lag a
  few seconds behind creation, so the map file stays the first place to look.
- parent: `POST /rest/api/3/issue`, `issuetype: {"name":"Epic"}`.
- child: `POST /rest/api/3/issue`, `issuetype: {"name":"Task"}`, `parent: {"key":"<epic>"}`,
  description in ADF with one `paragraph` node per blank-line-separated block of the body and a
  `hardBreak` node between lines inside a block:
  `{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"..."},{"type":"hardBreak"},...]}]}`.
- edge (right after creating the blocked issue; a step 7.4 edge right after creating the new
  blocker): `POST /rest/api/3/issueLink` with
  `{"type":{"name":"Blocks"},"outwardIssue":{"key":"<blocker>"},"inwardIssue":{"key":"<blocked>"}}`.
- direction check (first edge of each run): `GET /rest/api/3/issue/<blocker>?fields=issuelinks`.
  The new link must appear with `outwardIssue.key = <blocked>` (the blocker "blocks" it). If it
  appears with `inwardIssue.key = <blocked>` instead, the direction is reversed on this Jira:
  `DELETE /rest/api/3/issueLink/<link id>`, swap `outwardIssue` and `inwardIssue` for this edge and
  every later one, and say so in the report. GET again to confirm the re-posted link; if it
  appears in neither form, stop and report.

### Map file (github / jira only, DSGN-G)

`<feature dir>/raw/state/spec-ticket-map.md`, one row written right after each creation:

```
| IMPL | tracker | ticket | title | created |
|---|---|---|---|---|
| _feature | github | #41 | [<f>] feature | 2026-11-24 |
| IMPL-B | github | #42 | [<f>] IMPL-B — ... | 2026-11-24 |
```

A ticket found by search (not created in this run) gets `found <date>` in the `created` column.

## Checking a local run

`python3 tools/check_spec_ticket_fixture.py <issues dir> <expected.txt>` compares the IMPL files and
their `Parent:` / `Blocked by:` lines against an expected list. Fixtures: `skills/spec-ticket/tests/`.
