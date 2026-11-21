"""TST-X (IMPL-T): L1 headings and MUST sentences must not shrink without an ARD."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

import check_l1_delta as l1  # noqa: E402

DESIGN = "docs/features/demo/design/demo-design.md"
DH = "docs/features/demo/decision-history/demo-decision-history.md"
BASE_DESIGN = "# Demo\n\n#### DSGN-A — a\n\nThis MUST hold.\n\n#### DSGN-B — b\n\nThis MUST also hold.\n"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _write(repo: Path, rel: str, text: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "t")
    _write(tmp_path, DESIGN, BASE_DESIGN)
    _write(tmp_path, DH, "# Decisions\n\n### ARD-A — start\n")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


def _run(repo: Path) -> list[str]:
    return l1.check(repo, "HEAD", None, "docs/features")


def test_removed_heading_fails(repo: Path):
    _write(repo, DESIGN, BASE_DESIGN.replace("#### DSGN-B — b\n", "b\n"))
    assert any("DSGN-B" in f for f in _run(repo))


def test_removed_must_sentence_fails(repo: Path):
    _write(repo, DESIGN, BASE_DESIGN.replace("This MUST also hold.", "Also holds."))
    assert any("MUST sentences 2 -> 1" in f for f in _run(repo))


def test_removal_with_ard_passes(repo: Path):
    _write(repo, DESIGN, BASE_DESIGN.replace("#### DSGN-B — b\n\nThis MUST also hold.\n", ""))
    _write(repo, DH, "# Decisions\n\n### ARD-B — drop DSGN-B\n\nDSGN-B merged into demo-design DSGN-A.\n\n### ARD-A — start\n")
    assert _run(repo) == []


def test_additions_only_pass(repo: Path):
    _write(repo, DESIGN, BASE_DESIGN + "\n#### DSGN-C — c\n\nThis MUST be new.\n")
    assert _run(repo) == []


def test_raw_changes_ignored(repo: Path):
    _write(repo, "docs/features/demo/raw/notes.md", "#### DSGN-Z — draft\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "raw")
    (repo / "docs/features/demo/raw/notes.md").unlink()
    assert _run(repo) == []
