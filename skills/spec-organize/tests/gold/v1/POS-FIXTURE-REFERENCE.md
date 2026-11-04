# Pos-fixture reference (mechanical minimum)

TST-D **exemplar/** should eventually mirror a full feature tree. Until TST-C runs exist, use these **TST-B pos fixtures** as the smallest valid committed-spec shapes:

| Fixture | Path | Use |
|---|---|---|
| Test plan | `skills/spec-organize/tests/fixtures/pos/valid-test-plan/` | Downstream test-plan section IDs + frontmatter |
| Decision history | `skills/spec-organize/tests/fixtures/pos/valid-decision-history/` | Decision log + ARD-style IDs |

Verify fixtures anytime:

```bash
python3 tools/run_pos_fixtures.py
```

Do not copy fixture text into **exemplar/** for scoring without updating **`annotations.yaml`**.
