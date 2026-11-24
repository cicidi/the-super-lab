---
name: research
description: |
  Use when starting any non-trivial task and needing to surface unknowns
  before coding, or when designing a spec from an idea. Use when the user
  says "I'm not sure how to", "what am I missing", wants to brainstorm,
  or needs to go from vague idea to concrete design.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - research
    - discover
    - brainstorm
    - design spec
    - clarify requirements
    - what am I missing
    - I'm not sure how to
    - help me think through this
    - surface unknowns
    - find my unknowns
    - prototype
    - investigate
    - quiz me
    - 考考我
---

# research

Four-branch skill for the front end of development. Discover unknowns surfaces
blind spots before coding. Design spec takes an idea through structured
brainstorming to a written spec ready for implementation. Investigate (AFK)
answers a research question with no user present (wayfinder research briefs).
Quiz checks that the user understands a change or topic.

## When to Use

- Starting any non-trivial feature, refactor, or project
- The user expresses uncertainty about requirements
- Need to go from vague idea to concrete design document
- Working in unfamiliar codebase territory

## When NOT to Use

- Trivial tasks (typo fix, one-line change, obvious bug)
- Requirements are fully specified with no ambiguity
- The user explicitly says they have already planned thoroughly
- Already in implementation — use /bug hunt instead

## Process

### Step 0: Determine Branch

**Unattended first.** If you run as a subagent, were handed a wayfinder
research brief, or the session is non-interactive, do NOT ask anything —
go straight to **Branch C: Investigate (AFK)**.

**Quiz request.** If the user asks to be quizzed ("quiz me", "考考我"), go
straight to **Branch D: Quiz**.

Otherwise ask the user ONE question:

> "What are you trying to do?"
> - **Discover unknowns** — I have a task in mind but I'm not sure what I don't
>   know. Interview me to surface blind spots before coding.
> - **Design spec** — I have an idea. Help me brainstorm, explore approaches,
>   and write a concrete design document.

---

## Branch A: Discover Unknowns

Interview-first approach. Do homework silently first, then ask ONE question
at a time. Based on Thariq Shihipar's "Finding Your Unknowns" framework.

### Phase A1: Scan & Prepare (silent)

Before asking anything:
1. Read relevant code, project governance (CLAUDE.md, CONVENTIONS.md)
2. Map the territory — what exists, what constraints are in play
3. Identify gaps — what decisions are unmade?
4. Use Blind Spot Scan if territory is unfamiliar

### Phase A2: Interview — One Question at a Time

**Question priority:**
1. Architecture-changing decisions (data model, API shape, auth)
2. Scope decisions (what's in vs. out)
3. Convention preferences (follow existing vs. new)
4. Optimization choices (library, config values)
5. Unknowns surfaced during the interview

**Depth heuristic:**
| Go DEEP (2-3 rounds) | Go SHALLOW (1 round) |
|----------------------|---------------------|
| Backend architecture | Library/package choice |
| API design | LLM provider |
| Data model / schema | Config values with defaults |
| Auth / permissions | UI styling |

Litmus: "If I get this wrong, how expensive is the fix?" Expensive → deep.

**Interview rules:**
- ONE question at a time. Wait for the answer.
- 2-3 rounds max per topic, then summarize and pivot.
- "I don't know" is valid → offer to explain options, pick a default, or research.
- **Stop condition:** user says "whatever you think is best" on 2+ consecutive questions.

**Auxiliary tools** (serve the interview, not replace it):
- **Blind Spot Scan:** when the user seems unaware of codebase constraints,
  explore silently then surface as a question
- **Brainstorming & Prototyping:** when the user says "I'll know it when I
  see it," generate 2-3 HTML prototypes for them to react to
- **References:** when the user says "make it like X," read X and extract
  the semantics

### Phase A3: Summarize

After the interview: summarize all decisions, highlight remaining open questions, offer to proceed to design spec or implementation.

---

## Branch B: Design Spec

Structured brainstorming → design → spec → transition to implementation plan.

### Phase B1: Explore Context

Check files, docs, recent commits. Understand the current project state.

### Phase B2: Clarify

Ask questions one at a time. Understand purpose, constraints, success criteria.
Prefer multiple choice when possible, open-ended when needed.

### Phase B3: Propose Approaches

Present 2-3 approaches with trade-offs. Lead with the recommended option.
YAGNI ruthlessly — remove unnecessary features from every approach.

### Phase B4: Present Design

Scale each section to its complexity. Cover: architecture, components,
data flow, error handling, testing. Get user approval section by section.

### Phase B5: Write Spec

If the repo has `docs/features/spec-driven-development/`, write the design
through the `spec-write` skill (it owns the spec format; pass it the approved
design from B4). Otherwise write to `docs/features/<feature>/design/<topic>-design.md`
with: purpose, design decisions, architecture diagram, interface definitions,
error handling, testing strategy.

### Phase B6: Spec Self-Review

Check for: placeholders (TBD/TODO), internal consistency, scope creep, ambiguity.

### Phase B7: Transition

After user approves the written spec, invoke `superpowers:writing-plans`
to create the implementation plan.

---

## Branch C: Investigate (AFK)

No human in the loop. Used when wayfinder fires `/research` as a subagent for
a research brief, or any caller needs facts gathered unattended.

1. **Read the question.** Take it from the brief or the caller's prompt. Never
   ask the user — if the question is unclear, state your reading of it at the
   top of the output and proceed.
2. **Gather.** Read documentation, third-party APIs, and local sources (code,
   docs, git history, knowledge bases). Prefer primary sources.
3. **Write one markdown file.** Sections: Question, Answer (short), Findings,
   Unknowns. Every claim carries a citation: a URL, `path:line`, or a commit
   hash. Anything you could not verify is marked `UNKNOWN` with what you tried.
   Write it where the caller says (wayfinder: on the throwaway
   `research/<name>` branch it names); if the caller names no place, write
   `research/<name>.md` in the working directory.
4. **Return the file path** as your final message, plus a one-line answer.

---

## Branch D: Quiz

Checks that the user understands a change or topic before moving on.
Restored from find-my-unknown's post-implementation quiz.

Generate an HTML report covering:
- **Context:** Why this change, what problem it solves
- **Intuition:** Why this approach over alternatives
- **What changed:** File-by-file walkthrough with rationale (for a topic with
  no code change, walk through its key points instead)
- **Quiz:** 3-5 questions testing understanding (not memorization)

The subject is the change just made, or the topic just discussed if there is
no change. For a code change, the user should pass the quiz before merging.
