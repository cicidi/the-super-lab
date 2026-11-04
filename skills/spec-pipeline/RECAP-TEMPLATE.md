# spec-pipeline — recap template (copy to chat or state notes)

```markdown
## SDD recap — <feature-slug>

**Phase:** Create | Map | Converge | Downstream  
**State file:** CLAUDE.local.md | `docs/features/<f>/raw/state/state-YYYY-MM-DD.md`

### Last actions
- 

### Open items
- 

### Mechanical check (optional)
`python3 tools/run_spec_checks.py docs/features/<f>/` → paste finding count  
Full harness (this repo): `skills/spec-organize/tests/run_mechanical.sh`

### Next skill (see INTEGRATIONS.md)
| Step | Skill |
|------|-------|
| … | … |
```

Keep recap **out of git** unless user asks to append to `raw/state/`.
