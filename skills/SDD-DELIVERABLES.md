# Spec-Driven Development — skill deliverables

Initiative spec: `docs/features/spec-driven-development/`. Deliverable skills are spec-write, spec-review and wayfinder (ARD-CH). The other rows are supporting files, not the deliverable.

| Skill | Role |
|---|---|
| [spec-pipeline](spec-pipeline/SKILL.md) | Phase orchestration, reader trigger |
| [spec-organize](spec-organize/SKILL.md) | Standard, placement, lint, INDEX |
| [spec-write](spec-write/SKILL.md) | Committed prose edits |
| [spec-review](spec-review/SKILL.md) | Mechanical + semantic review |
| [wayfinder](wayfinder/SKILL.md) | Progress record = map directory; recap on resume; review gate before commit; Downstream blocked by open blocking QUES |
| [spec-html-standard](spec-html-standard/SPEC-HTML-STANDARD.md) | Human reader HTML rules (**DSGN-N** summary); Mermaid: [MERMAID-PATTERNS.md](spec-html-standard/MERMAID-PATTERNS.md) |

**Harness:** `./tools/run_sdd_mechanical.sh` · **Tools:** `tools/README-SDD.md` · **Spec bundle:** parent PRD `version` → `python3 tools/build_spec_skills.py` · **Pipeline ops:** `spec-pipeline/INDEX.md` · **Eval matrix:** `spec-organize/tests/eval/TST-J-MATRIX.md`.
