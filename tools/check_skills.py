#!/usr/bin/env python3
"""Static check for SKILL.md files (skill design, ARD-K).

usage: check_skills.py [SKILL_DIR ...]     (default: every skill in skills/ and personal-skills/)

Checks each SKILL.md for:
  frontmatter  YAML parses; `name` equals the directory name; `description` is set
  skill-ref    every `/name` in backticks names a skill that exists
  link         every relative markdown link resolves to a file
  repo-path    every `skills/...`, `personal-skills/...`, `tools/...` path in backticks exists
Exit 0 when nothing is found.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOTS = ("skills", "personal-skills")
# Skills that live outside this repo: walter-worker skills and Claude Code built-ins.
EXTERNAL = {
    "commit", "dashboard", "feature", "init", "knowledge", "matt-code-review", "memory",
    "project", "status", "add-mcp-skill", "walter-worker-fix", "walter-worker-upgrade",
    "walter-worker-setup-in-project", "walter-worker-setup-graphify", "write-doc", "graphify",
    "code-review", "simplify", "loop", "schedule", "review", "security-review",
}
SKILL_REF = re.compile(r"(?<![\w.~/:<-])/([a-z][a-z0-9-]*[a-z0-9])(?![\w/.-])")
LINK = re.compile(r"\]\(([^)\s]+)\)")
REPO_PATH = re.compile(r"`((?:skills|personal-skills|tools)/[^`\s*<>{}]+)`")
FENCE = re.compile(r"^(```|~~~)")
# Sections that may name old skills on purpose (where a skill came from).
HISTORY_SECTIONS = {"sources", "provenance", "change log", "changelog", "history"}
# A line that says where something came from may name an old skill.
PROVENANCE = re.compile(r"absorbed|restored from|upstream|inspired|renamed|merged|replac|formerly|source_", re.I)
# Old skill names that are also ordinary words in this repo.
GENERIC = {"initiative"}


def skill_names():
    return {p.parent.name for r in SKILL_ROOTS for p in (ROOT / r).glob("*/SKILL.md")}


def retired_names(known):
    """Skill directories that existed in git history and are gone now."""
    import subprocess
    log = subprocess.run(["git", "-C", str(ROOT), "log", "--all", "--name-only", "--format="],
                         capture_output=True, text=True).stdout
    seen = set(re.findall(r"^[a-z-]+/([a-z0-9-]+)/SKILL\.md$", log, re.M))
    return seen - known - EXTERNAL - GENERIC


def body_lines(text):
    """Yield (line_no, line) outside fenced code blocks."""
    fenced = False
    for no, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line.strip()):
            fenced = not fenced
            continue
        if not fenced:
            yield no, line


def check_frontmatter(path, text):
    if not text.startswith("---\n"):
        return [f"{path}:1 frontmatter: missing"]
    head = text[4:].split("\n---", 1)[0]
    try:
        meta = yaml.safe_load(head) or {}
    except yaml.YAMLError as e:
        return [f"{path}:1 frontmatter: YAML error: {e}".splitlines()[0]]
    out = []
    if meta.get("name") != path.parent.name:
        out.append(f"{path}:1 frontmatter: name {meta.get('name')!r} != directory {path.parent.name!r}")
    if not meta.get("description"):
        out.append(f"{path}:1 frontmatter: description missing")
    return out


def check_body(path, text, known, retired_re):
    out = []
    section = ""
    in_front = text.startswith("---\n")
    for no, line in body_lines(text):
        if in_front and no > 1 and line.strip() == "---":
            in_front = False
        if PROVENANCE.search(line):
            continue
        if line.startswith("## "):
            section = line[3:].strip().lower()
        for name in SKILL_REF.findall(line):
            if name not in known and name not in EXTERNAL:
                out.append(f"{path}:{no} skill-ref: /{name} is not a known skill")
        trigger_item = in_front and line.lstrip().startswith("- ")
        if retired_re and not trigger_item and section not in HISTORY_SECTIONS:
            for name in sorted(set(retired_re.findall(line))):
                out.append(f"{path}:{no} retired: {name} was a skill and no longer exists")
        for target in LINK.findall(line):
            if re.match(r"^(https?:|mailto:|#|~|/)", target):
                continue
            file = target.split("#", 1)[0]
            if file and not (path.parent / file).exists():
                out.append(f"{path}:{no} link: {target} does not resolve")
        for rel in REPO_PATH.findall(line):
            rel = rel.split("#", 1)[0].split(":", 1)[0].rstrip(".,)")
            if not (ROOT / rel).exists():
                out.append(f"{path}:{no} repo-path: {rel} does not exist")
    return out


def main(argv):
    known = skill_names()
    retired = retired_names(known)
    retired_re = re.compile(r"(?<![\w/.-])(" + "|".join(sorted(retired, key=len, reverse=True))
                            + r")(?![\w-]|/(?![A-Z]))") if retired else None
    if argv:
        files = [Path(a).resolve() / "SKILL.md" for a in argv]
    else:
        files = sorted(p for r in SKILL_ROOTS for p in (ROOT / r).glob("*/SKILL.md"))
    findings = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(ROOT) if f.is_relative_to(ROOT) else f
        findings += check_frontmatter(rel, text) + check_body(rel, text, known, retired_re)
    print("\n".join(findings))
    print(f"# skills: {len(files)}  findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
