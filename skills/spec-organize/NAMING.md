# Paths, Names, and Splitting

## The path

```
docs/features/<feature>/<type>/<feature>-<type>.md
```

One file per type per feature by default. `prd`, `test-plan`, `decision-history`,
and `how-to` stay single-file — none of them grows without bound. `spec` and
`impl-plan` may be split, because they do.

- `<feature>` is kebab-case, lowercase, no spaces or special characters
- The filename repeats the feature and the type, so a file is identifiable
  outside its directory
- A supporting file that a document cites sits in that document's folder:
  `docs/features/<feature>/design/<source-name>.md`
- A feature has at most one `decision-history`, and it is exempt from the
  1,000-line cap: it is append-only history, and history is never trimmed

## Splitting a spec or a plan

Split when one file would cross 1,000 lines. Split on a boundary — a bounded
context, domain, ownership edge, or lifecycle — never to reach a line count.

```
docs/features/payment/design/payment-design-authorization.md
docs/features/payment/design/payment-design-settlement.md
docs/features/payment/impl-plan/payment-impl-plan-01-schema.md
docs/features/payment/impl-plan/payment-impl-plan-02-api.md
```

- A `spec` part takes a bounded-context noun. Never a number: a number says
  nothing about the contents, and inserting a part forces a renumber across the
  set. A spec is cut by bounded context, so a noun carries the meaning
- An `impl-plan` part takes a zero-padded sequence plus a phase name. A plan is
  ordered, so the number carries meaning there
- A `<feature>-design.md` may stay as an entry file holding global L1 constraints
  and links to the parts. Do not keep one as an empty shell

## Name collisions

Check a new feature or file name against what already exists, every time a
document is placed — in Organize before creating, and in Lint across the tree.
Any one of these is a collision:

| Signal | Example |
|---|---|
| Identical after normalization | `Payment` vs `payment` |
| One name's tokens are a subset of the other's | `auth` within `auth-service` |
| Singular, plural, or a common abbreviation of the same word | `doc`/`docs`, `auth`/`authentication` |
| Edit distance at most 2 on the hyphenated name | `payment-api` vs `payments-api` |

Resolve by intent, not by picking a winner:

- **Same bounded context** — merge into one feature folder, then split its `design`
  by aspect
- **Different contexts, confusable names** — rename both so each is
  distinguishable (a bare `auth` becomes `payment-auth` and `user-auth`), and
  record the rename in the affected feature's `decision-history`
- **A file collision inside one feature** — make the aspect names distinct; if
  they cannot be, the feature name is too generic

A rename is a decision. Log it rather than performing it silently, because every
inbound link and every reader's memory of the old name has to be updated.
