# Spec Health, Staleness, and Drift

## Metadata

Beyond the four required fields (`feature`, `type`, `state`, `final_date`), an
important spec may carry:

```yaml
spec_id: payment.authorization
version: 3
health: active
owner: payments-team
last_verified: 2026-09-25
```

| Field | Meaning |
|---|---|
| `state` | Authoring state: `draft` or `final` |
| `health` | `active`, `stale`, or `deprecated` |
| `owner` | Who answers for the document's accuracy |
| `last_verified` | When someone last confirmed the spec still matches intended and current behavior |

`last_updated` is when the file was edited. `last_verified` is when someone
confirmed it is still true. Health tracks `last_verified`, not `last_updated`.

The field is `health`, not `status`: `state` already tracks the authoring state,
and a second field named for "state" would be read as the same thing.

Never edit a file only to move a timestamp.

All five optional fields may be omitted. A document without them is still valid;
it simply carries no health signal, and Lint reports that as NICE, not MUST.

## Stale

`stale` means the spec has not been recently verified. It does NOT mean the spec
is wrong. Roughly 90 days is a reasonable review signal and never a hard rule: a
stable spec that rarely changes should not be edited to satisfy a clock.

## Drift detection

Check for, by CI, lint, agent review, or periodic audit:

- spec and code contradict each other
- the spec references an API or component that no longer exists
- the code implements important behavior the spec does not mention
- important behavior changed without the spec being reviewed
- the spec carries excessive implementation detail
- the spec has grown past a useful context boundary
- the same fact is maintained in two places
- `last_verified` is stale

Not every drift is mechanically resolvable. For semantic ambiguity the order is:

```
Detect -> Report -> Ask
```

Never `Detect -> Guess -> Rewrite`.

## Change checklist

Run this when an implementation change is complete:

- [ ] Relevant spec identified
- [ ] Authoritative source identified for each affected concern
- [ ] Determined whether intended behavior changed
- [ ] If behavior changed, the spec is updated
- [ ] If the change is implementation-only, no spec edit was made
- [ ] Code does not contradict intended behavior
- [ ] Tests verify the important spec requirements
- [ ] Machine-readable contracts remain consistent
- [ ] No duplicate source of truth introduced
- [ ] `last_verified` updated only where a real verification happened
- [ ] Unresolved spec/code conflicts reported, not silently resolved

## Duplication

Do not maintain the same fact by hand in a spec, a README, a wiki, an issue
tracker, API documentation, and code comments. Pick one authoritative source,
generate the others, delete the duplicate, or give each document a distinct
purpose. The goal is not that every document agrees; it is that no fact is
maintained twice.
