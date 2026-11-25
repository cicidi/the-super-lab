# the-super-lab

![the-super-lab](pic/the-super-lab.png)

A curated collection of AI agent skills (SKILL.md format), framework-agnostic, opencode-native.

## What's a skill?

A **skill** is a self-contained directory with a `SKILL.md` file. It packages "how to do X" in a way any SKILL.md-aware agent can execute. Copy it, fork it, move it between projects — it just works.

## Available Skills

> **walter-worker skills have moved to [walter-worker](https://github.com/cicidi/walter-worker)** — they now live alongside the project they serve.

### General Skills (`skills/`)

| Skill | Description |
|-------|-------------|
| [auto-tdd](skills/auto-tdd/) | Test-driven development with multi-agent TDD loop — red-green-refactor or full continuous loop |
| [bug](skills/bug/) | Debugging, bug reporting, and self-healing loop management |
| [doc-organize](skills/doc-organize/) | Document placement, naming, INDEX.md maintenance, and merge conflict resolution |
| [doc-review](skills/doc-review/) | Adversarial design/spec review or work completion verification |
| [domain-modeling](skills/domain-modeling/) | Build or sharpen a project's domain model with glossary and ADRs | 🔗 |
| [english-grammar-fix](skills/english-grammar-fix/) | Auto-correct minor English grammar errors in AI responses |
| [grill-with-docs](skills/grill-with-docs/) | Relentless interview to sharpen a plan or design with inline documentation | 🔗 |
| [implement](skills/implement/) | Implement work from a spec or tickets with TDD, typechecking, and code review | 🔗 |
| [multi-model-team](skills/multi-model-team/) | Decompose large tasks into subtasks executed by specialized workers |
| [prototype](skills/prototype/) | Build throwaway prototypes to answer design questions | 🔗 |
| [research](skills/research/) | Surface unknowns before coding; go from vague idea to concrete design |
| [skill](skills/skill/) | Skill lifecycle — create, edit, import, list skills |
| [spec-ingest](skills/spec-ingest/) | Sort chat or local files into prd / design / decision-history / impl-plan / test-plan items, then hand off to spec-write |
| [spec-ticket](skills/spec-ticket/) | Open one parent ticket per feature and one ticket per IMPL-* in local / GitHub / Jira |
| [wayfinder](skills/wayfinder/) | Plan work too large for one agent session via decision briefs on the issue tracker | 🔗 |

🔗 = imported from [mattpocock/skills](https://github.com/mattpocock/skills)

### Personal Skills (`personal-skills/`)

| Skill | Description |
|-------|-------------|
| [create-video-workflow](personal-skills/create-video-workflow/) | Convert research documents into audience-tailored content — presentations, videos, websites |
| [doc-protect](personal-skills/doc-protect/) | Protect sections of documents from AI edits |
| [luma-event-scout](personal-skills/luma-event-scout/) | Scout AI/tech events on Luma in the Bay Area with advanced filtering |
| [pic-to-txt](personal-skills/pic-to-txt/) | Convert a folder of screenshot images into a clean text document via OCR |
| [tmux-status-bar](personal-skills/tmux-status-bar/) | Set up tmux status bar with session, git, and feature info |
| [transcribe-audio](personal-skills/transcribe-audio/) | Convert audio files to text transcripts using local Whisper on GPU |
| [video-production-pip-style](personal-skills/video-production-pip-style/) | Replicate the Andrei Jikh video production style with PiP citations |
| [youtube-research-pipeline](personal-skills/youtube-research-pipeline/) | Turn any topic into a complete YouTube video package with research and interactive HTML |
| [youtube-summarize](personal-skills/youtube-summarize/) | Download, transcribe, and summarize YouTube videos |

## Workflow

Skills are created and edited in this source code repo, then deployed to IDE configs:

```
Source Repo (~/project/the-super-lab/) → git push → Deployed Copy → IDE Configs
```

**Never create or edit skills directly in the deployed copy** (`~/.config/opencode/skills/the-super-lab/`) or IDE config directories (`~/.claude/commands/`, `~/.opencode/instructions/`). Changes in deployed copies are lost on next install.

## Install

```bash
git clone https://github.com/cicidi/the-super-lab.git ~/project/the-super-lab
```

To deploy skills to your IDEs, use the walter-worker install script or `coworker sync`.

## Testing

```bash
python3 tools/check_skills.py            # all skills
python3 tools/check_skills.py skills/bug  # one skill
```

Checks every SKILL.md: frontmatter (name matches the directory, description set), references to skills that do not exist or were retired, relative links, and repo paths.
CI runs it on every push and pull request (`.github/workflows/skills-check.yml`). To run it before each commit that touches a SKILL.md:

```bash
git config core.hooksPath tools/git-hooks
```

## Conventions

See [CONVENTIONS.md](CONVENTIONS.md) for the project's conventions.

## License

MIT — see LICENSE file.
