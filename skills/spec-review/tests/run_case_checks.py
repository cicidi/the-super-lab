#!/usr/bin/env python3
"""Run TST-B checkers on spec-review case input trees; compare to expected.yaml mechanical block."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CASES = Path(__file__).resolve().parent / "cases"
TESTS = ROOT / "skills/spec-organize/tests"
sys.path.insert(0, str(TESTS))

from checks.change_log import check_change_log  # noqa: E402
from checks.frontmatter import check_frontmatter  # noqa: E402
from checks.sections import check_sections  # noqa: E402
from checks.size import check_size  # noqa: E402
from checks.ids import check_ids  # noqa: E402
from checks.paths import check_committed_path  # noqa: E402

RUNNERS = [
    check_frontmatter,
    check_committed_path,
    check_sections,
    check_ids,
    check_size,
    check_change_log,
]


def _load_expected(case_dir: Path) -> dict:
    path = case_dir / "expected.yaml"
    if not path.is_file():
        return {}
    out: dict = {"mechanical": {}}
    block = None
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s == "mechanical:":
            block = "mechanical"
            continue
        if block and s.startswith("min_findings:"):
            out["mechanical"]["min_findings"] = int(s.split(":", 1)[1].strip())
        if block and s.startswith("max_findings:"):
            out["mechanical"]["max_findings"] = int(s.split(":", 1)[1].strip())
        if block and s.startswith("- ") and not s.startswith("- id:"):
            check_name = s[2:].strip()
            if check_name and check_name not in ("case:",):
                out["mechanical"].setdefault("checks", []).append(check_name)
        if block and s.startswith("message_contains:"):
            out["mechanical"]["message_contains"] = s.split(":", 1)[1].strip()
    return out


def _findings_for_input(input_root: Path) -> list:
    findings = []
    for path in sorted(input_root.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for fn in RUNNERS:
            findings.extend(fn(path, text))
    return findings


def main() -> None:
    failures = 0
    ok_count = 0
    for case_dir in sorted(CASES.iterdir()):
        if not case_dir.is_dir():
            continue
        input_root = case_dir / "input"
        if not input_root.is_dir():
            continue
        exp = _load_expected(case_dir)
        mech = exp.get("mechanical") or {}
        if not mech:
            continue
        findings = _findings_for_input(input_root)
        case_fail = False
        if "max_findings" in mech:
            max_n = int(mech["max_findings"])
            if len(findings) > max_n:
                print(
                    f"FAIL {case_dir.name}: expected <={max_n} findings, got {len(findings)}"
                )
                for f in findings[:5]:
                    print(f"  {f.check}\t{f.path}\t{f.message}")
                case_fail = True
        if "min_findings" in mech:
            min_n = int(mech["min_findings"])
            if len(findings) < min_n:
                print(f"FAIL {case_dir.name}: expected >={min_n} findings, got {len(findings)}")
                case_fail = True
        elif "max_findings" not in mech:
            min_n = 1
            if len(findings) < min_n:
                print(f"FAIL {case_dir.name}: expected >={min_n} findings, got {len(findings)}")
                case_fail = True
        for check in mech.get("checks") or []:
            if not any(f.check == check for f in findings):
                print(f"FAIL {case_dir.name}: missing check {check!r}")
                case_fail = True
        substr = mech.get("message_contains")
        if substr and not any(substr in f.message for f in findings):
            print(f"FAIL {case_dir.name}: no message containing {substr!r}")
            case_fail = True
        if case_fail:
            failures += 1
        else:
            ok_count += 1
            print(f"ok {case_dir.name} ({len(findings)} findings)")
    if failures:
        sys.exit(1)
    print(f"all {ok_count} cases ok")


if __name__ == "__main__":
    main()
