"""Feature and filename collision signals (NAMING.md / DSGN-J)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from checks.paths import COMMITTED_TYPES, ENTRY_RE


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    message: str


def _normalize(name: str) -> str:
    return name.lower().replace("_", "-").strip()


def _tokens(name: str) -> list[str]:
    return [t for t in _normalize(name).split("-") if t]


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            ins = cur[j - 1] + 1
            delete = prev[j] + 1
            sub = prev[j - 1] + (0 if ca == cb else 1)
            cur.append(min(ins, delete, sub))
        prev = cur
    return prev[-1]


def _aspect_extension(a: str, b: str) -> bool:
    na, nb = _normalize(a), _normalize(b)
    return nb.startswith(na + "-") or na.startswith(nb + "-")


def _collision_reason(a: str, b: str) -> str | None:
    if _aspect_extension(a, b):
        return None
    na, nb = _normalize(a), _normalize(b)
    if na == nb:
        return "identical after normalization"
    ta, tb = set(_tokens(a)), set(_tokens(b))
    if ta and tb and (ta <= tb or tb <= ta) and ta != tb:
        return "one name's tokens are a subset of the other's"
    if _levenshtein(na, nb) <= 2 and na != nb:
        return "edit distance at most 2 on hyphenated name"
    return None


def _feature_slugs(features_root: Path) -> list[tuple[str, str]]:
    """Return (slug, relative feature root path) for each feature tree."""
    out: list[tuple[str, str]] = []
    if not features_root.is_dir():
        return out
    for child in sorted(features_root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        out.append((child.name, child.as_posix()))
        nested = child / "features"
        if nested.is_dir():
            for sub in sorted(nested.iterdir()):
                if sub.is_dir() and not sub.name.startswith("."):
                    out.append((sub.name, sub.as_posix()))
    return out


def _entry_stems(feature_root: Path) -> list[tuple[str, str]]:
    stems: list[tuple[str, str]] = []
    for path in feature_root.rglob("*.md"):
        try:
            rel = path.relative_to(feature_root).as_posix()
        except ValueError:
            continue
        if rel.startswith("features/"):
            continue
        if path.name.startswith("._") or "/raw/" in path.as_posix():
            continue
        if path.parent.name not in COMMITTED_TYPES:
            continue
        if not ENTRY_RE.match(path.name):
            continue
        stem = path.name[: -len(".md")]
        stems.append((stem, path.as_posix()))
    return stems


def check_collision(features_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    slugs = _feature_slugs(features_root)
    for i, (a, pa) in enumerate(slugs):
        for b, pb in slugs[i + 1 :]:
            reason = _collision_reason(a, b)
            if reason:
                findings.append(
                    Finding(
                        "collision",
                        pa,
                        f"feature `{a}` vs `{b}` ({pb}): {reason}",
                    )
                )
    for _slug, froot in slugs:
        root = Path(froot)
        stems = _entry_stems(root)
        for i, (a, pa) in enumerate(stems):
            for b, pb in stems[i + 1 :]:
                if a == b:
                    continue
                reason = _collision_reason(a, b)
                if reason:
                    findings.append(
                        Finding(
                            "collision",
                            pa,
                            f"entry `{a}` vs `{b}` ({pb}): {reason}",
                        )
                    )
    return findings
