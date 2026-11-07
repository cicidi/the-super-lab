# Spec Scope, Size, and Context

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
| Feature / change spec | 500-1,500 lines |
| Architecture / design spec | 1,000-3,000 lines |
| A single implementation task | 100-500 lines |
| Spec context one agent task needs | roughly 5-10k tokens |

These are guidelines, not hard limits. Split on boundaries, not on line counts:

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
