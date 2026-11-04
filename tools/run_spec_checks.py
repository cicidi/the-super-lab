#!/usr/bin/env python3
"""Run TST-B mechanical checks on a docs/features tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "skills/spec-organize/tests"
sys.path.insert(0, str(TESTS))

from checks.change_log import check_change_log  # noqa: E402
from checks.decision_log import check_decision_log  # noqa: E402
from checks.frontmatter import Finding, check_frontmatter  # noqa: E402
from checks.ids import check_ids  # noqa: E402
from checks.paths import check_committed_path  # noqa: E402
from checks.sections import check_sections  # noqa: E402
from checks.collision import check_collision  # noqa: E402
from checks.index_book import check_index_book  # noqa: E402
from checks.no_commit import check_no_commit_tree  # noqa: E402
from checks.parent_complete import check_parent_complete  # noqa: E402
from checks.size import check_size  # noqa: E402

# Grandfathered paths (spec frozen — fix when user approves spec edit)
EXEMPT = {
    ROOT / "docs/features/spec-driven-development/prd/spec-driven-development-prd.md",
}

# Slug pairs already tracked for rename (avoid blocking lint until resolved)
COLLISION_ALLOW = {frozenset({"delivery-pipeline", "pipeline"})}


def _filter_collision(findings: list) -> list:
    out = []
    for f in findings:
        if f.check != "collision":
            out.append(f)
            continue
        m = re.match(r"feature `([^`]+)` vs `([^`]+)`", f.message)
        if m and frozenset(m.groups()) in COLLISION_ALLOW:
            continue
        out.append(f)
    return out

RUNNERS = [
    check_frontmatter,
    check_committed_path,
    check_sections,
    check_decision_log,
    check_change_log,
    check_ids,
    check_size,
]


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs/features"
    if not target.exists():
        print(f"missing: {target}", file=sys.stderr)
        sys.exit(1)
    findings = []
    features_root = ROOT / "docs/features"
    if "docs/features" in target.as_posix():
        if features_root.is_dir():
            findings.extend(_filter_collision(check_collision(features_root)))
            findings.extend(check_no_commit_tree(features_root))
        findings.extend(check_index_book(ROOT))
    if target.is_dir() and target.name not in ("features", "docs") and "docs/features" in target.as_posix():
        findings.extend(check_parent_complete(target))
    for path in sorted(target.rglob("*.md")):
        if path.name.startswith("._") or "/raw/" in path.as_posix() or ".scratch" in path.as_posix():
            continue
        if path.resolve() in EXEMPT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding("encoding", str(path), "not utf-8"))
            continue
        for fn in RUNNERS:
            findings.extend(fn(path, text))
    for f in findings:
        print(f"{f.check}\t{f.path}\t{f.message}")
    print(f"\n# findings: {len(findings)}")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
