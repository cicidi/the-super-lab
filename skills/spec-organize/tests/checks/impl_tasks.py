"""Each IMPL task has a done line (ARD-AT), a 依赖 and a 挡住 line, and depends/blocks
edges agree both ways (DSGN-E). Execution order and read-before-write stay with the
LLM judge (MUST-K is llm-scored)."""

from __future__ import annotations

import re
from pathlib import Path

from checks.frontmatter import Finding, _parse_frontmatter

_DONE = re.compile(r"Done when|Verify:|完成标准")
# No `\b`: `IMPL-K的…` (CJK right after the id) must still match.
_IMPL_ID = re.compile(r"IMPL-[A-Z]+(?![A-Z])")
_DEPS_LABEL = r"(?:依赖|Depends on)\s*[：:]"
_BLOCKS_LABEL = r"(?:挡住|Blocks)\s*[：:]"
_DEPS = re.compile(rf"{_DEPS_LABEL}(.*?)(?={_BLOCKS_LABEL}|$)", re.MULTILINE)
_BLOCKS = re.compile(rf"{_BLOCKS_LABEL}(.*)$", re.MULTILINE)


def _ids(pattern: re.Pattern[str], body: str) -> set[str]:
    return {i for m in pattern.finditer(body) for i in _IMPL_ID.findall(m.group(1))}


def _edge_findings(path: Path, tasks: dict[str, str]) -> list[Finding]:
    """If A blocks B, B depends on A, and vice versa. Qualifiers like
    `IMPL-K 的语义部分` still match on the IMPL id token."""
    if not any(_DEPS.search(b) or _BLOCKS.search(b) for b in tasks.values()):
        return []
    deps = {t: _ids(_DEPS, b) for t, b in tasks.items()}
    blocks = {t: _ids(_BLOCKS, b) for t, b in tasks.items()}
    out: list[Finding] = []
    for a in tasks:
        for b in sorted(blocks[a]):
            if b in tasks and a not in deps[b]:
                out.append(Finding("impl_tasks", str(path), f"{a} blocks {b}, but {b} 依赖 does not name {a}"))
        for b in sorted(deps[a]):
            if b in tasks and a not in blocks[b]:
                out.append(Finding("impl_tasks", str(path), f"{a} depends on {b}, but {b} 挡住 does not name {a}"))
    return out


def check_impl_tasks(path: Path, text: str | None = None) -> list[Finding]:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)
    if not fm or fm.get("type") != "impl-plan":
        return []
    parts = re.split(r"(?m)^## (IMPL-[A-Z]+)\b", raw)
    findings: list[Finding] = []
    tasks: dict[str, str] = {}
    for i in range(1, len(parts), 2):
        ident, body = parts[i], parts[i + 1] if i + 1 < len(parts) else ""
        tasks[ident] = re.split(r"(?m)^## ", body, maxsplit=1)[0]
        if not _DONE.search(body):
            findings.append(
                Finding("impl_tasks", str(path), f"{ident} needs Done when, Verify, or 完成标准")
            )
        if not _DEPS.search(tasks[ident]):
            findings.append(Finding("impl_tasks", str(path), f"{ident} needs a 依赖/Depends on line (write 无 if none)"))
        if not _BLOCKS.search(tasks[ident]):
            findings.append(Finding("impl_tasks", str(path), f"{ident} needs a 挡住/Blocks line (write 无 if none)"))
    return findings + _edge_findings(path, tasks)
