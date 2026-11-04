# Mechanical checks (TST-B)

Implement Python modules per parent test plan: paths, size, frontmatter, sections, ids, decision_log, change_log, index_book, collision, no_commit.

Run on a tree: `python3 tools/run_spec_checks.py docs/features/<f>/`

Modules: `frontmatter`, `paths`, `sections`, `decision_log`, `change_log`, `ids`, `size`, `parent_complete`, `collision`, `index_book`, `no_commit`. Tree-level: `collision`, `index_book`, `no_commit` (via `run_spec_checks` on any `docs/features/` path). Unit tests: `tests/test_checks.py` with `PYTHONPATH=checks`.
