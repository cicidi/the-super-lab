#!/usr/bin/env python3
"""Stamp SDD skill SKILL.md files with the parent PRD spec bundle version.

Each build (without --check) first adds 1 to the last part of the version (ARD-CK).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRD = ROOT / "docs/features/spec-driven-development/prd/spec-driven-development-prd.md"
SKILLS = [
    ROOT / "skills/spec-write/SKILL.md",
    ROOT / "skills/spec-review/SKILL.md",
    ROOT / "skills/spec-organize/SKILL.md",
    ROOT / "skills/spec-pipeline/SKILL.md",
    ROOT / "skills/wayfinder/SKILL.md",
]

BUNDLE_START = "<!-- SPEC-BUNDLE-START -->"
BUNDLE_END = "<!-- SPEC-BUNDLE-END -->"


def git_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def read_prd_version() -> str:
    if not PRD.is_file():
        print(f"missing PRD: {PRD}", file=sys.stderr)
        sys.exit(1)
    text = PRD.read_text(encoding="utf-8")
    m = re.search(r"(?m)^version:\s*['\"]?([^'\"\n#]+)", text)
    if not m:
        print("missing frontmatter version: in parent SDD PRD", file=sys.stderr)
        sys.exit(1)
    return m.group(1).strip()


def bump_prd_version() -> str:
    """Add 1 to the last part of the parent PRD `version` and write it back (ARD-CK)."""
    text = PRD.read_text(encoding="utf-8")
    old = read_prd_version()
    parts = old.split(".")
    if not parts[-1].isdigit():
        print(f"cannot bump non-numeric version {old!r}", file=sys.stderr)
        sys.exit(1)
    parts[-1] = str(int(parts[-1]) + 1)
    new = ".".join(parts)
    text = re.sub(r'(?m)^version:.*$', f'version: "{new}"', text, count=1)
    PRD.write_text(text, encoding="utf-8")
    return new


def bundle_block(version: str, built: str, sha: str) -> str:
    return (
        f"{BUNDLE_START}\n"
        f"> **SDD spec bundle** `{version}` · built {built} · git `{sha}`\n"
        f"{BUNDLE_END}"
    )


def parse_bundle(text: str) -> str | None:
    m = re.search(
        rf"{re.escape(BUNDLE_START)}.*?{re.escape(BUNDLE_END)}",
        text,
        flags=re.S,
    )
    return m.group(0) if m else None


def bundle_version(block: str) -> str | None:
    m = re.search(r"SDD spec bundle\*\* `([^`]+)`", block)
    return m.group(1) if m else None


def upsert_metadata(front: str, version: str, built: str, sha: str) -> str:
    front = front.rstrip("\n") + "\n"
    front = re.sub(r"(?m)^  spec_bundle_version:.*\n", "", front)
    front = re.sub(r"(?m)^  spec_built_at:.*\n", "", front)
    front = re.sub(r"(?m)^  spec_git_sha:.*\n", "", front)
    insert = (
        f"  spec_bundle_version: \"{version}\"\n"
        f"  spec_built_at: \"{built}\"\n"
        f"  spec_git_sha: \"{sha}\"\n"
    )
    if not re.search(r"(?m)^metadata:\s*$", front):
        return front.rstrip() + f"\nmetadata:\n{insert}"
    return front.rstrip() + "\n" + insert


def stamp_skill(path: Path, version: str, built: str, sha: str) -> bool:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.S)
    if not m:
        print(f"no YAML frontmatter: {path}", file=sys.stderr)
        sys.exit(1)
    front, body = m.group(1), m.group(2)
    new_front = upsert_metadata(front, version, built, sha)
    block = bundle_block(version, built, sha)
    old = parse_bundle(body)
    if old:
        body = body.replace(old, block, 1)
    else:
        body = block + "\n\n" + body.lstrip()
    new_text = f"---\n{new_front.rstrip()}\n---\n{body}"
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def check_skill(path: Path, version: str) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        print(f"no frontmatter: {path}", file=sys.stderr)
        sys.exit(1)
    front = m.group(1)
    keys = re.findall(r"(?m)^\s*([A-Za-z_][\w-]*):", front)
    dupes = sorted({k for k in keys if keys.count(k) > 1 and k.startswith("spec_")})
    if dupes:
        print(f"{path.name}: duplicate frontmatter key(s) {dupes}", file=sys.stderr)
        sys.exit(1)
    for key, want in (
        ("spec_bundle_version", version),
    ):
        fm = re.search(rf"(?m)^  {key}:\s*\"?([^\"\n]+)\"?", front)
        if not fm or fm.group(1).strip() != want:
            print(f"{path.name}: metadata {key} != PRD version {want}", file=sys.stderr)
            sys.exit(1)
    block = parse_bundle(text)
    if not block:
        print(f"{path.name}: missing SPEC-BUNDLE block (run build_spec_skills.py)", file=sys.stderr)
        sys.exit(1)
    bv = bundle_version(block)
    if bv != version:
        print(f"{path.name}: bundle shows {bv!r}, want {version!r}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if SKILL stamps do not match parent PRD version",
    )
    args = parser.parse_args()
    version = read_prd_version() if args.check else bump_prd_version()
    built = date.today().isoformat()
    sha = git_sha()
    if args.check:
        for path in SKILLS:
            if not path.is_file():
                print(f"missing: {path}", file=sys.stderr)
                sys.exit(1)
            check_skill(path, version)
        print(f"ok: spec bundle {version} on {len(SKILLS)} skill(s)")
        return
    changed = 0
    for path in SKILLS:
        if not path.is_file():
            print(f"missing: {path}", file=sys.stderr)
            sys.exit(1)
        if stamp_skill(path, version, built, sha):
            changed += 1
    print(f"spec bundle {version} · sha {sha} · updated {changed}/{len(SKILLS)} skill(s)")


if __name__ == "__main__":
    main()