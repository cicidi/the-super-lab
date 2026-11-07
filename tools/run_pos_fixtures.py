#!/usr/bin/env python3
"""Assert fixtures/pos/* trees pass per-file TST-B checkers (no false positives)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POS = ROOT / "skills/spec-organize/tests/fixtures/pos"
TESTS = ROOT / "skills/spec-organize/tests"
sys.path.insert(0, str(TESTS))

from checks.change_log import check_change_log  # noqa: E402
from checks.decision_log import check_decision_log  # noqa: E402
from checks.frontmatter import check_frontmatter  # noqa: E402
from checks.ids import check_ids  # noqa: E402
from checks.paths import check_committed_path  # noqa: E402
from checks.sections import check_sections  # noqa: E402
from checks.size import check_size  # noqa: E402

RUNNERS = [
    check_frontmatter,
    check_committed_path,
    check_sections,
    check_ids,
    check_size,
    check_change_log,
    check_decision_log,
]


def main() -> None:
    if not POS.is_dir():
        print(f"missing: {POS}", file=sys.stderr)
        sys.exit(1)
    errors: list[str] = []
    count = 0
    for fixture in sorted(POS.iterdir()):
        if not fixture.is_dir():
            continue
        for path in sorted(fixture.rglob("*.md")):
            if path.name.startswith("._"):
                continue
            count += 1
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"{path}: not utf-8")
                continue
            for fn in RUNNERS:
                for f in fn(path, text):
                    errors.append(f"{fixture.name}: {f.check} {f.path} — {f.message}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)
    print(f"ok: {count} pos markdown file(s)")


if __name__ == "__main__":
    main()
