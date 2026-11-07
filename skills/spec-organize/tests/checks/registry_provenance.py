"""MUST provenance: registry items resolve, and contract clauses carry most of them (DSGN-A)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

DESIGN_REL = "docs/features/spec-driven-development/features/document-standard/design/document-standard-design.md"
CONTRACT = {"DSGN-B", "DSGN-C", "DSGN-D", "DSGN-E", "DSGN-F", "DSGN-M"}
HEAD = re.compile(r"#{3,4} (DSGN-[A-Z])")


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def _items(text: str) -> list[dict[str, str]]:
    items, cur = [], {}
    for line in text.splitlines():
        if line.startswith("  - id:"):
            if cur:
                items.append(cur)
            cur = {"id": line.split(":", 1)[1].strip()}
        elif cur and line.strip().startswith(("method:", "check:", "source:")):
            key, value = line.strip().split(":", 1)
            cur[key] = value.strip().strip("'\"")
    if cur:
        items.append(cur)
    return items


def _clause_at(lines: list[str], line_no: int) -> str | None:
    current = None
    for i, line in enumerate(lines, 1):
        m = HEAD.match(line)
        if m and i <= line_no:
            current = m.group(1)
        elif i > line_no:
            break
    return current


def check_registry_provenance(repo_root: Path) -> list[Finding]:
    registry = repo_root / "skills/spec-organize/tests/must_registry.yaml"
    design = repo_root / DESIGN_REL
    checks_dir = repo_root / "skills/spec-organize/tests/checks"
    if not registry.is_file() or not design.is_file():
        return []
    design_lines = design.read_text(encoding="utf-8").splitlines()
    implemented = {p.stem for p in checks_dir.glob("*.py") if not p.name.startswith("._") and p.stem != "__init__"}
    findings: list[Finding] = []
    contract_hits = sourced = 0
    for item in _items(registry.read_text(encoding="utf-8")):
        ident = item["id"]
        source = item.get("source", "")
        if ":" in source:
            rel, _, line_no = source.rpartition(":")
            target = repo_root / rel
            if not target.is_file():
                findings.append(Finding("registry_provenance", rel, f"{ident}: source file missing"))
            elif line_no.isdigit():
                usable = target.read_text(encoding="utf-8").splitlines()
                if int(line_no) > len(usable):
                    findings.append(Finding("registry_provenance", rel, f"{ident}: source line out of range"))
                elif target == design:
                    sourced += 1
                    contract_hits += _clause_at(design_lines, int(line_no)) in CONTRACT
        if item.get("method") == "python":
            check = item.get("check", "")
            if check and check not in implemented:
                findings.append(
                    Finding("registry_provenance", "must_registry.yaml", f"{ident}: no module checks/{check}.py")
                )
    if sourced and contract_hits * 3 < sourced * 2:
        findings.append(
            Finding(
                "registry_provenance",
                DESIGN_REL,
                f"only {contract_hits}/{sourced} design-sourced MUSTs come from contract clauses",
            )
        )
    return findings
