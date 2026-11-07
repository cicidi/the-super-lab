# Spec Scope, Size, and Context

Path, permission, and evidence: `SPEC-STANDARD.md` chapters 1–3. Expression: `skills/spec-html-standard/SPEC-PRESENTATION.md`.

## What a spec is for

A healthy spec is not a complete description of the code. It is a precise
description of the behavior, contracts, constraints, and architecture that
developers and agents must preserve.

Describe:

- What and Why
- Contract
- Invariants
- Constraints
- Expected behavior
- Error semantics
- State transitions
- External interactions

Do not describe:

- class hierarchy
- private methods
- temporary variables
- internal helper functions
- framework-specific implementation
- internal algorithms that are free to be refactored

Prefer:

```
Authorization must reject an expired payment method.
```

over:

```
PaymentAuthorizationService.validateExpiration() calls
ExpirationValidator.validate(), which reads PaymentMethod.expiresAt.
```

The test: if the implementation can change while externally observable behavior
does not, the spec SHOULD NOT change.

## Size guidelines

| Document | Typical range |
|---|---|
| Feature / change spec | at or under the hard cap |
| Architecture / design spec | at or under 1,000 lines |
| A single implementation task | 100-500 lines |
| Spec context one agent task needs | roughly 5-10k tokens |

`design` and `impl-plan` stay at or under the 1,000-line hard cap in `SPEC-STANDARD.md`. `decision-history` is exempt. Split on boundaries, not on line counts:

- bounded context
- domain boundary
- ownership boundary
- independent lifecycle
- independent change frequency
- agent context requirements

A spec describing several independent domains, lifecycles, or behavior models
should be split. Do not split mechanically to satisfy a line count.

## Loading spec context

An agent should not load the whole documentation hierarchy. Load in this order
and stop as soon as the task is answerable:

1. Global rules
2. The relevant domain spec
3. The relevant architecture
4. The relevant contract
5. The relevant examples and tests
6. The code

If an agent routinely needs most of a spec to answer a narrow question, the spec
boundary is wrong. Re-cut it rather than raising the context budget.

## Invariants as data

Write an invariant as a table: the record that exists after a step, or a state that must not occur, with why it is impossible and who guarantees that. A slogan is not an invariant (ARD-AR).

## Diagrams for what prose cannot carry

Use a sequence diagram for an interaction, one flow per diagram. State combinations go in a table. Sample records go in a table. A heading that names steps a–b and contains a sequence diagram has b−a+1 messages. The diagram does not add a fact the prose does not state (ARD-BE).
