---
name: skill
description: |
  Use when creating, editing, importing, or listing skills in the-super-lab.
  Use when the user wants to capture a workflow as a skill, modify an existing
  skill, import from GitHub, or see what skills are available.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - skill
    - create skill
    - edit skill
    - import skill
    - list skills
    - new skill
    - make a skill
---

# skill

Manage skills in the-super-lab. Create self-contained SKILL.md files from
workflows, edit existing skills, import from external sources, and list what's
available.

## When to Use

- Capturing a reusable workflow as a new skill
- Modifying or fixing an existing skill's instructions
- Importing a skill from a GitHub URL or external repo
- Listing configured or available skills

## When NOT to Use

- Running an existing skill — just invoke it directly
- Creating a feature → use /feature
- Managing the project catalog → use /project

## Process

### No subcommand given

List current skills and ask what the user wants to do.

### Subcommands

| Subcommand | Description |
|------------|-------------|
| `create <name>` | Create a new SKILL.md with guided setup + quality gates |
| `edit <name>` | Modify an existing skill's content or frontmatter |
| `import <url>` | Import a skill from a GitHub URL into skills/ |
| `list` | List all configured skills |

### create workflow

1. Ask for the skill name (kebab-case, `{verb}-{object}` format)
2. Search for existing similar skills (locally, GitHub, web) — avoid duplicates
3. Read CONVENTIONS.md for frontmatter and body structure rules
4. Draft the SKILL.md with:
   - Frontmatter: name, description ("Use when...", third person), license, compatibility
   - Body: # heading + overview, When to Use, When NOT to Use, Process, Quality Gates
5. Present the draft for review
6. On approval: save to `skills/<name>/SKILL.md`
7. Run `python3 tools/check_skills.py skills/<name>`; fix every finding
   before reporting done

### edit workflow

1. Read the current SKILL.md
2. Ask what to change (frontmatter fields, process steps, quality gates, triggers)
3. Apply changes while preserving: no TBD/TODO, no emoji in body, description
   must stay ≤1024 chars and start with "Use when"
4. Show diff and confirm before saving
5. After saving, run `python3 tools/check_skills.py <skill dir>`; fix every
   finding before reporting done

### import workflow

1. Fetch the SKILL.md from the GitHub URL
2. Convert to the-super-lab conventions:
   - Add `license: MIT` if missing
   - Add `compatibility: claude-code,opencode` if missing
   - Verify description starts with "Use when..."
   - Add When to Use / When NOT to Use sections if missing
3. Record provenance in frontmatter `metadata` (never drop it):
   - `source_author`: original author or organization
   - `source_url`: URL of the source SKILL.md; pin it to the commit sha
     when available (`.../blob/<sha>/...`)
   - `imported`: import date (YYYY-MM-DD)
4. Check dependencies: list every skill (`/grilling`) and file (`LOGIC.md`,
   `agents/`) the imported SKILL.md references. Import each missing one from
   the same source, or flag it in the report. Do not finish with a dangling
   reference.
5. Save to `skills/<original-name>/SKILL.md`, keeping the original name
6. Run `python3 tools/check_skills.py skills/<original-name>`; a finding is
   a dangling reference from step 4
7. Report what was converted vs kept as-is, the provenance recorded, and
   each dependency imported or still missing

### list workflow

Run `coworker skill list` to show all configured skills with name, path,
and enabled status.
