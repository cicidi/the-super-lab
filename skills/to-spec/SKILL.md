---
name: to-spec
description: |
  Use when turning the current conversation into a spec (PRD) and publishing it
  to the project issue tracker. Synthesizes what was discussed — no interview,
  just synthesis.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - to spec
    - write spec
    - create PRD
    - publish spec
    - spec from conversation
  when_to_use: |
    When a conversation has produced enough clarity to capture as a formal spec.
    When decisions have been made and need to be recorded as a PRD on the issue
    tracker.
  when_not_to_use: |
    When the conversation is still fuzzy and needs more grilling first. When you
    need to interview the user to fill gaps — use grill-with-docs instead.
  audience:
    - developers
    - architects
    - product managers
  source_author: mattpocock
  source_url: https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md
---

# to-spec

This skill takes the current conversation context and codebase understanding and produces a spec (you may know this document as a PRD). Do NOT interview the user — just synthesize what you already know.

The issue tracker configuration should have been provided via the project's init flow. If no tracker has been configured, default to the local-markdown tracker.

## Skill Dependencies

What this skill produces is a `spec` under the project's doc standard. Placement,
frontmatter, and required sections come from `doc-organize`. What belongs inside
it comes from `doc-organize/AUTHORITY-BY-CONCERN.md` and
`doc-organize/CONTENT-PRIORITY.md`.

Write the spec at L1: behavior, contracts, invariants, constraints, error
semantics, security rules, architecture boundaries, out of scope, assumptions,
and compatibility constraints. Rationale is L2 and rejected alternatives are L3.
Do not put class structure, private methods, or internal algorithms in a spec —
those belong to the code.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Check with the user that these seams match their expectations.

3. Write the spec using the template below, then publish it to the project issue tracker. Apply the `ready-for-agent` triage label - no need for additional triage.

<spec-template>

<!-- Every section is tagged with its content level (doc-organize/CONTENT-PRIORITY.md).
     L1 decisive - never trimmed. L2 rationale. L3 alternatives. L4 support.
     Trim order when the spec runs long: L4 first, then L3, then compress L2.
     Never delete L1. The whole spec stays under 1,000 lines; if it cannot, split
     it by bounded context and name the parts by doc-organize/NAMING.md. -->

## Problem Statement — L1

The problem that the user is facing, from the user's perspective.

Without it the feature's direction cannot be checked, so it is not trimmable even
when the Solution reads as self-explanatory.

## Solution — L1

The solution to the problem, from the user's perspective.

## User Stories — L1

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

Each story states externally observable behavior, which is why it is L1. A story
that only restates the Solution in different words is a duplicate, and a
duplicate is L4 — write it once.

## Implementation Decisions — L1 for the decision, L2 for the rationale

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

A decision is L1: an implementation built without it is wrong. The paragraph
explaining WHY that decision was taken is L2 — keep the reason, drop the
narration. Class structure, private methods, and internal algorithms are not a
level at all; they belong to the code.

## Alternatives Considered — L3, optional

The approaches that were live and were rejected, each with the reason it lost.
Omit this section when no alternative was seriously considered — an empty
section implies a diligence that did not happen.

This is the first section to delete when the spec runs long, unless a rejected
alternative is the only thing preventing the decision from being relitigated.

## Testing Decisions — L1 for the constraint, L2 for the specifics

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

"Test external behavior, not implementation details" is L1: it is a constraint on
the whole test suite. The module list and the prior-art pointers are L2.

## Out of Scope — L1

A description of the things that are out of scope for this spec.

Non-goals prevent drift as much as goals do. Never trim this section.

## Further Notes — L4

Any further notes about the feature.

Support material: background, references, examples, open threads. This is the
first section to delete, and a fact that already lives in another document
belongs here as a link, never as a restatement.

</spec-template>
