#!/usr/bin/env python3
"""Assert every fixtures/neg/<name>/ tree triggers at least one TST-B finding."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "skills/spec-organize/tests/fixtures/neg"
TESTS = ROOT / "skills/spec-organize/tests"
sys.path.insert(0, str(TESTS))

from checks.change_log import check_change_log  # noqa: E402
from checks.collision import check_collision  # noqa: E402
from checks.decision_log import check_decision_log  # noqa: E402
from checks.frontmatter import check_frontmatter  # noqa: E402
from checks.ids import check_ids  # noqa: E402
from checks.no_commit import check_no_commit_tree  # noqa: E402
from checks.paths import check_committed_path  # noqa: E402
from checks.sections import check_sections  # noqa: E402
from checks.parent_complete import check_parent_complete  # noqa: E402
from checks.size import check_size  # noqa: E402

# neg folder name → (expected check id, runner)
CASES: list[tuple[str, str, object]] = [
    ("missing-frontmatter", "frontmatter", check_frontmatter),
    ("bad-filename", "paths", check_committed_path),
    ("bad-ids", "ids", check_ids),
    ("bad-decision-log", "decision_log", check_decision_log),
    ("bad-change-log", "change_log", check_change_log),
    ("bad-sections", "sections", check_sections),
    ("bad-size", "size", check_size),
    ("bad-no-commit", "no_commit", check_no_commit_tree),
    ("collision-pair", "collision", check_collision),
    ("bad-parent-incomplete", "parent_complete", check_parent_complete),
]


def _run_case(name: str, check: str, fn) -> list:
    base = FIX / name
    if not base.is_dir():
        return [f"missing fixture dir {name}"]
    if fn is check_parent_complete:
        for feat in (base / "docs" / "features").iterdir():
            if feat.is_dir():
                findings = fn(feat)
                if any(f.check == check for f in findings):
                    return []
        return [f"{name}: no {check} finding"]
    if fn is check_no_commit_tree or fn is check_collision:
        root = base / "docs" / "features"
        if not root.is_dir():
            return [f"{name}: missing docs/features"]
        findings = fn(root)
        return [] if any(f.check == check for f in findings) else [f"{name}: no {check} finding"]
    findings = []
    for path in base.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        findings.extend(fn(path, text) if fn is not check_committed_path else fn(path))
    if any(f.check == check for f in findings):
        return []
    return [f"{name}: no {check} finding"]


def main() -> None:
    errors: list[str] = []
    for name, check, fn in CASES:
        errors.extend(_run_case(name, check, fn))
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)
    print(f"ok: {len(CASES)} neg fixtures")


if __name__ == "__main__":
    main()
