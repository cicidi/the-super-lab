#!/usr/bin/env python3
"""Check a local spec-ticket run against an expected list (spec-ticket design, ARD-N).

usage: check_spec_ticket_fixture.py <issues_dir> <expected.txt>

expected.txt lines:
  IMPL-B: IMPL-A, IMPL-C   # IMPL-B must exist, blocked by exactly A and C
  IMPL-D: -                # IMPL-D must exist, blocked by nothing
  absent: IMPL-X, IMPL-Y   # these must NOT have a ticket (done IMPLs)
Blank lines and '#' comments are ignored. Exit 0 when everything matches.
"""
import re
import sys
from pathlib import Path

ID = re.compile(r"IMPL-[A-Z]+")
FILE = re.compile(r"^(IMPL-[A-Z]+)(?:-[a-z0-9-]+)?\.md$")


def parse_expected(path):
    want, absent = {}, set()
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        key, _, rest = line.partition(":")
        if key.strip() == "absent":
            absent |= set(ID.findall(rest))
        else:
            want[key.strip()] = set(ID.findall(rest))
    return want, absent


def read_tickets(issues_dir):
    found, problems = {}, []
    for f in sorted(Path(issues_dir).glob("*.md")):
        if f.name == "_feature.md":
            continue
        m = FILE.match(f.name)
        if not m:
            problems.append(f"unexpected file name: {f.name}")
            continue
        impl = m.group(1)
        if impl in found:
            problems.append(f"duplicate ticket for {impl}: {f.name}")
            continue
        text = f.read_text(encoding="utf-8")
        if not re.search(r"^Parent: _feature\s*$", text, re.M):
            problems.append(f"{f.name}: missing 'Parent: _feature' line")
        lines = re.findall(r"^Blocked by:(.*)$", text, re.M)
        if len(lines) > 1:
            problems.append(f"{f.name}: {len(lines)} 'Blocked by:' lines, expected 1")
        bl = re.search(r"^Blocked by:(.*)$", text, re.M)
        if not bl:
            problems.append(f"{f.name}: missing 'Blocked by:' line")
        else:
            for ref in re.findall(r"\((IMPL-[A-Z]+[^)]*\.md)\)", bl.group(1)):
                if not (Path(issues_dir) / ref).is_file():
                    problems.append(f"{f.name}: blocker file {ref} does not exist")
        found[impl] = set(ID.findall(bl.group(1))) if bl else set()
    return found, problems


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[2])
        return 2
    issues_dir, expected = argv[1], argv[2]
    want, absent = parse_expected(expected)
    found, problems = read_tickets(issues_dir)
    if not (Path(issues_dir) / "_feature.md").is_file():
        problems.append("missing parent ticket _feature.md")
    for impl in sorted(set(want) - set(found)):
        problems.append(f"missing ticket for {impl}")
    for impl in sorted(set(found) - set(want)):
        kind = "done IMPL has a ticket" if impl in absent else "unexpected ticket"
        problems.append(f"{kind}: {impl}")
    for impl in sorted(set(want) & set(found)):
        if want[impl] != found[impl]:
            problems.append(f"{impl}: blocked by {sorted(found[impl])}, expected {sorted(want[impl])}")
    for p in problems:
        print(p)
    print(f"# tickets: {len(found)}  problems: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
