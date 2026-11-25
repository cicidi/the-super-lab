---
name: bug
description: |
  Use when debugging, reporting bugs, or managing the self-healing loop.
  Use when the user encounters an error, wants to file a bug, needs
  systematic root cause investigation, or wants to record a correction
  pattern for future prevention.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - bug
    - debug
    - report bug
    - file issue
    - self heal
    - self analyze
    - fix this error
    - what's wrong
    - why is this failing
    - record correction
    - learn from mistakes
---

# bug

Three-branch skill covering the full bug lifecycle: hunt (find + fix root
cause), report (file a GitHub issue), and heal (record corrections and
analyze patterns for prevention).

## When to Use

- Encountering an error or unexpected behavior that needs investigation
- Unknown cause, multi-service failure, production outage, on-call (deep investigation)
- Wanting to file a GitHub issue — on the current repo or another repo the user picks
- The AI keeps making the same mistake and needs pattern-based prevention
- User corrected the AI and wants that correction remembered

## When NOT to Use

- Feature requests or enhancement proposals → use /feature
- Code review of working code → use /spec-review (design review branch)
- General questions about how something works → just ask

## Process

### Step 0: Determine Branch

Ask the user ONE question:

> "What do you need?"
> - **Hunt** — find and fix a bug (systematic root cause investigation)
> - **Report** — file a GitHub issue (default: the current repo)
> - **Heal** — record a correction and analyze patterns to prevent future mistakes

---

## Branch A: Hunt — Scientific Debugging

Hypothesis-driven root cause investigation. No guessing, no workarounds.
Collect first, then reason with evidence. Two modes depending on scope.

### Choose Mode

- **Mode 1: Quick Debug** — known code bug, single service, stack trace available.
  Follow Phases 1-5 below.
- **Mode 2: Deep Investigation** — unknown cause, multi-service, production
  outage, on-call. Follow "Mode 2: Deep Investigation" below.

### Phase 1: Collect

Gather ALL potentially relevant info before analyzing:
- Error message + full stack trace
- Failing test or reproduction steps
- Code around the failure point (trace all callers and callees)
- Recent git log (what changed? when did this start failing?)
- Related logs, config values, env differences
- Any user reports or messages about the issue
- Does it pass on the main branch?
- Do NOT filter or judge relevance yet — grab everything

### Phase 2: Reason

List evidence and form hypotheses:
- List each piece of evidence found
- 3-5 possible root causes, ranked by likelihood
- Link each hypothesis to specific evidence
  - H1 (most likely): ... — evidence: ...
  - H2: ... — evidence: ...
  - H3: ... — evidence: ...

### Phase 3: Test Hypotheses

For each hypothesis (test in order, stop at first confirmed):
1. Define a minimal test that isolates this hypothesis
2. Run the test
3. Record expected vs actual → CONFIRMED or REJECTED

### Phase 4: Fix

Once a hypothesis is CONFIRMED:
1. Identify the exact root cause (file:line)
2. Apply a **minimal** fix — address only the root cause
3. Add a regression test that would have caught this
4. Run the full test suite — verify no regressions

### Phase 5: Document

- Commit with `fix:` conventional commit format: "fix: {desc} — root cause: {cause}"
- If the pattern is generalizable, offer to run the heal branch

### Mode 2: Deep Investigation

Unknown cause, multi-service, production outage, on-call.

1. **Collect** — exhaust all data sources before forming theories:
   - Logs (all services, around the incident window)
   - Git log / recent PRs / deployments
   - Metrics, dashboards, alerts
   - Messages: Slack, on-call pings, user reports
   - Config changes, env diffs, infra changes
   - Everything. Don't filter yet.
2. **Reason** — build evidence list and timeline:
   - List every finding from step 1
   - Highlight anomalies: "this log line doesn't belong", "this metric spiked"
   - Build timeline of events
   - Form hypotheses linked to evidence
3. **Investigate** — follow leads, verify root cause
4. **Report** — structured report: problem, evidence, root cause, fix, prevention
   (format below)
5. **Issue** — file the report as a GitHub issue via Branch B: Report

#### Investigation Report Format (Mode 2)

```markdown
## Investigation Report

**Problem:** {description}
**Duration:** {start} → {end or ongoing}
**Impact:** {affected users/systems}

## Root Cause
{precise description}

## Evidence
1. {evidence}
2. {evidence}

## Timeline
| Time | Event |
|------|-------|
| T1   | {event} |
| T2   | {event} ← root cause here |

## Fix
{what to do}

## Prevention
{how to prevent recurrence}
```

### Hunt Rules

- Never guess — every fix backed by evidence
- Never fix symptoms instead of root cause
- Never add workarounds for code you don't understand
- Always add a regression test
- If pattern is generalizable → log a heal trace (Branch C)
- Use strongest model for complex investigations

---

## Branch B: Report — File a GitHub Issue

File a structured GitHub issue: project bugs, walter-worker system issues,
or feature requests that need discussion.

### Steps

1. **Detect the target repo:** default to the current repo:
   ```bash
   gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null \
     || git remote get-url origin
   ```
   Also offer repos from the project catalog (`~/.coworker/project.yaml`)
   and "Other (enter owner/repo)".
2. **Confirm the target with the user** before filing:
   "File this issue on `{owner}/{repo}`?" Never file until the user confirms.
3. **Describe:** what happened vs what was expected, reproduction steps,
   relevant files and error messages. For an AI mistake: what the AI did
   wrong and which skill/rule was involved.
4. **Draft the issue:** sections for what happened, expected behavior,
   affected component, reproduction steps, suggested fix.
   Title: `fix: {desc}` for bugs, `feat: {desc}` for features;
   prefix `[coworker]` when the issue is about the walter-worker system itself.
5. **Labels:** `bug` or `enhancement`; for walter-worker system issues
   `coworker-bug` or `coworker-improvement`.
6. **Create:**
   ```bash
   gh issue create --repo {owner}/{repo} --title "{title}" \
     --body "{body}" --label "{labels}"
   ```
7. **Link:** if this was an AI mistake, also run the heal branch to log a trace

---

## Branch C: Heal — Self-Healing Loop

Record corrections and generate prevention rules.

### Phase C0: Check the Hook

Automatic logging depends on a global `UserPromptSubmit` hook. Check it,
do not assume it is active:

```bash
ls ~/.claude/hooks/on-self-heal.sh 2>/dev/null                # Claude Code: script exists?
grep -q on-self-heal.sh ~/.claude/settings.json && echo registered
ls ~/.config/opencode/hooks/on-self-heal.sh 2>/dev/null       # OpenCode: script exists?
grep -qs on-self-heal.sh ~/.config/opencode/config.json ~/.config/opencode/opencode.json && echo registered
```

If a script is missing or not registered, tell the user:
"Self-heal hook is not active for {ide} — corrections are only logged when
you run Heal yourself." Do NOT install or register the hook unless the user
explicitly asks.

### Phase C1: Record Correction

When the user corrects the AI:
1. Detect the correction (trigger keywords: no, don't, stop, wrong, never, "not like that", "I told you")
2. Write a trace to `.self-healing/traces/YYYY-MM-DD.yaml`:
   ```yaml
   - id: <uuid>
     timestamp: <ISO8601>
     context: <what the AI did wrong>
     correction: <what the user said>
     category: code-conventions | workflow | security | architecture | tool-use
   ```
3. Confirm: "Logged. Run /bug → Heal → Analyze Patterns later to generate prevention rules."

### Phase C2: Analyze Patterns

When the user wants to generate prevention rules from accumulated traces:
1. Read all `traces/*.yaml` files, group by category, count frequency
2. Find patterns: same correction occurring 2+ times
3. Generate a markdown block with the rules
4. Inject into the project's CLAUDE.md (replace existing SELF-ANALYZE block or append)
5. Report: traces analyzed, patterns found, rules injected

A single correction does NOT trigger a rule — only repeated patterns (2+ occurrences).

## Quality Gates

### MUST (block)

- Hunt: evidence collected and listed before hypotheses
- Hunt: every hypothesis linked to specific evidence
- Hunt: hypotheses formed before any fix attempted
- Hunt: regression test added
- Hunt: fix is minimal (only root cause, no refactoring)
- Hunt Mode 2: investigation report includes evidence and timeline
- Report: target repo detected and confirmed by the user before filing
- Report: reproduction steps included in issue
- Report: affected skill/component identified
- Heal: hook status checked and reported, never assumed
- Heal: trace written with valid category
- Heal: only 2+ occurrence patterns generate rules

### NICE (warn)

- Hunt: git log checked for when the failure started
- Report: suggested fix included
- Heal: suggestion to run analyze after accumulating traces
