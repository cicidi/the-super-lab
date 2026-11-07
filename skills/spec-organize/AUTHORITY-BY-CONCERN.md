# Authority by Concern

No single artifact is the source of truth for everything. Each kind of fact has
one authoritative artifact, and that artifact is what to read — and to change
first — when the fact is in question.

## The authority table

| Concern | Authoritative artifact | Answers |
|---|---|---|
| Intended behavior | the feature's `design` | What the system SHOULD do |
| API contract | OpenAPI, protobuf, GraphQL, JSON Schema, event schema, AsyncAPI — when present | The contract's exact shape |
| Database structure | migrations and schema definitions | What the database actually is |
| Current implementation | the code | What the system CURRENTLY does |
| Executable verification | the tests | Does the implementation satisfy the expected behavior |

**Spec is authoritative for intended behavior:** requirements, business rules,
invariants, architectural constraints, externally observable behavior, security
and authorization rules, reliability guarantees, and performance targets that
were explicitly specified.

**Code is authoritative for current implementation:** class, module and package
structure, internal algorithms and data structures, framework usage,
implementation-specific optimizations, and the code paths actually taken.

Spec is not authoritative for current implementation. Code is not authoritative
for intended behavior. Do not restate a machine-readable contract or a database
schema in a Markdown spec — read the artifact it already lives in, and generate
the prose from it.

## Deciding what to establish

Before reading anything, answer: *what concern am I trying to establish?* Then
read the artifact that owns that concern. Do not read the code to learn intended
behavior, and do not read the spec to learn the current call graph.

## Conflict between authorities

When two authoritative artifacts disagree about the same concern, do not
silently overwrite either one:

```
spec:  retry = 3
code:  retry = 5
tests: expect 5
```

This is Spec/Implementation drift. Neither `spec > code` nor `code > spec`
resolves it. Work through:

1. What is the intended behavior?
2. Is there a recent requirement or change that speaks to it?
3. Is there an explicit product or business decision?
4. Was the code changed deliberately?
5. Are the tests merely recording the current implementation?
6. Is there a production-behavior or compatibility requirement?
7. Which artifact is authoritative for this concern?

If the answer is not determinable, STOP. Explain the conflict, show the evidence
on each side, and ask. Never silently pick a side, and never rewrite the spec or
the code to match the other before the intended behavior is established.

On a production system, existing behavior is never broken automatically because
the spec reads as more authoritative.

## A passing test is not a requirement

Tests are executable verification, not a substitute for requirements. They
answer "does the current implementation satisfy the expected behavior?". A test
that passes today may only be recording what the code already does.
