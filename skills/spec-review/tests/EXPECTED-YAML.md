# spec-review case `expected.yaml` blocks

Mechanical cases under `cases/*/expected.yaml` drive **`run_case_checks.py`** today.

## `mechanical:` (active)

```yaml
mechanical:
  max_findings: 0
  checks:
    - sections
  message_contains: optional substring
```

## `tree:` (active)

```yaml
tree:
  feature_root: input
  min_findings: 1
  checks:
    - parent_complete
```

## `semantic:` (TST-H / TST-I — not executed yet)

Planned fields for LLM judge cases (suggest-only review):

```yaml
semantic:
  severity: must | should
  finding_id: REV-SEM-001
  expected_fix: One sentence fix hint for the agent
  rubric: Optional short criterion quoted from design
```

When implemented, **`run_case_checks.py`** will skip `semantic` until a judge runner exists; mechanical + tree gates stay in CI.
