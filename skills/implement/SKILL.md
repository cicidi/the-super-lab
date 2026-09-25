---
name: implement
description: |
  Use when implementing work described in a spec or set of tickets. Drives TDD
  at pre-agreed seams, runs typechecking and tests, and closes out with code
  review before committing.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - implement
    - build
    - implement tickets
  when_to_use: |
    When a spec and tickets are ready for implementation. When the work has
    clear acceptance criteria and pre-agreed testing seams.
  when_not_to_use: |
    When the spec is still fuzzy or decisions are unmade — use wayfinder or
    grill-with-docs first. When there are no tickets to work from.
  audience:
    - developers
  source_author: mattpocock
  source_url: https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md
---

# implement

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.

## Skill Dependencies

Classify the change before touching the spec. `doc-organize/CONTENT-PRIORITY.md`
and `doc-organize/AUTHORITY-BY-CONCERN.md` define the difference between a
behavior change and an implementation-only change. Refactoring, renaming, internal
optimization, and framework migration do not require a spec edit; a change to
externally observable behavior does.

When code and spec disagree, do not silently rewrite either one. Report the
conflict, show the evidence on both sides, and ask.
