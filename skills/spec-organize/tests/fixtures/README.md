# TST-B fixtures

| Dir | Role |
|---|---|
| `neg/<name>/` | Must trigger checker `{name}` (see `tools/run_neg_fixtures.py`) |
| `pos/<name>/` | Must pass all per-file checkers (`tools/run_pos_fixtures.py`) |

Neg folders (10): `missing-frontmatter`, `bad-filename`, `bad-ids`, `bad-decision-log`, `bad-change-log`, `bad-sections`, `bad-size`, `bad-no-commit`, `collision-pair`, `bad-parent-incomplete`.

Pos folders: `valid-test-plan`, `valid-decision-history`.
