# Content Priority

A spec is trimmed from the bottom up. Every piece of content sits at one of four
levels, and the level decides what happens when the document needs to shrink.

## The four levels

| Level | Holds | Test | On trim |
|---|---|---|---|
| **L1 Decisive** | What the system must do and must not do | Remove it and a reader implements something different | **Never deleted** |
| **L2 Rationale** | Why this design, with evidence | Remove it and the rule still holds, but nobody knows why | Moved out or compressed |
| **L3 Alternatives** | Why not the other approach | Remove it and the rule still holds, but the road not taken is lost | Deleted first |
| **L4 Support** | References, research, examples, raw output | Remove it and nothing about the behavior is lost | Deleted first |

## What sits at L1

- intended behavior, requirements, business rules
- contracts and the shape of inputs and outputs
- invariants and constraints
- error semantics
- state transitions and external interactions
- security, authorization, and permission rules
- architecture boundaries — module edges and dependency direction
- performance guarantees that were explicitly specified
- **out of scope and non-goals** — these prevent drift as much as goals do
- **assumptions** — a premise that, if wrong, invalidates the design
- **compatibility and migration constraints** — what must keep working
- **open questions** — marked as unresolved, never silently dropped

The last four are easy to misfile as L2. They are L1: an implementation built on
a dropped assumption, or one that breaks a dropped compatibility constraint, is
wrong in the same way as one that ignores a stated requirement.

## What sits at L2

- the rationale for a decision
- benchmark or profile output that justifies a stated guarantee
- the incident or regression number that motivated a rule
- a link to the discussion that produced the decision

## What sits at L3

- rejected alternatives, with the reason each was rejected
- trade-off comparisons between the options that were live
- "X was considered and dropped because Y"

## What sits at L4

- raw research notes and product comparisons
- mockups and screenshots
- illustrative example payloads and sample data
- long logs and unprocessed benchmark output
- meeting notes
- a copy of a glossary that already exists in `CONTEXT.md`
- tutorial-style explanation of background material

## A duplicated fact is L4

A fact has exactly one authoritative home. If the same fact already appears in
another document — a contract, a glossary, a `decision-history`, a README — then
the second appearance is not a restatement. It is a link, and a link is L4.

Restating a fact is not a level, it is a defect: it creates a second place to
update and a second place to be wrong. When lint or a reader finds one, replace
the copy with a link to the document that owns it.

The link survives trimming as long as something depends on following it. What
never survives is the copy. This is the same rule as the duplication section of
`SPEC-HEALTH.md`, seen from the trimming side.

## What belongs at no level

These do not belong in a spec at any level. They are not L4 — they are absent:

- class hierarchy
- private methods
- temporary variables
- internal helper functions
- pseudocode
- framework-specific implementation detail
- internal algorithms that are free to be refactored

If the implementation can change while externally observable behavior does not,
the content belongs in the code, not the spec.

## Trimming procedure

1. Replace every restated fact with a link to the document that owns it. This
   comes first: a duplicate is a defect, and it is not worth trimming around.
2. Delete the remaining L4 content. Move research and long logs to the feature's
   gitignored scratch rather than deleting them outright, and keep a link if the
   spec cites them.
3. Delete L3 content, unless a rejected alternative is the only thing preventing
   the decision from being relitigated.
4. Compress L2 — keep the reason, drop the narration.
5. Never delete L1.
6. If the document is still over 1,000 lines, the boundary is wrong. Split it on
   a bounded context, domain, ownership, or lifecycle edge and name the parts by
   the rules in `SKILL.md`.

Deleting L1 to fit a size cap is a defect, not an optimization.
