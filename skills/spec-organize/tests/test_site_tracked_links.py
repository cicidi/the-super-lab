"""A code span links to a local file only when git tracks it (gitignored files never publish)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

import build_sdd_site as site  # noqa: E402


def _repo(tmp_path, monkeypatch, tracked):
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools/run.py").write_text("", encoding="utf-8")
    (tmp_path / "tools/local.py").write_text("", encoding="utf-8")
    monkeypatch.setattr(site, "ROOT", tmp_path)
    monkeypatch.setattr(site, "_TRACKED", tracked)
    monkeypatch.setattr(site, "_TRACKED_LOADED", True)


def test_gitignored_file_is_not_linked(tmp_path, monkeypatch):
    _repo(tmp_path, monkeypatch, {"tools/run.py"})
    md = tmp_path / "README.md"
    assert site._dest_for_mention("tools/run.py", md) == tmp_path / "tools/run.py"
    assert site._dest_for_mention("tools/local.py", md) is None


def test_falls_back_to_existence_without_git(tmp_path, monkeypatch):
    _repo(tmp_path, monkeypatch, None)
    assert site._linkable_file("tools/local.py")
    assert not site._linkable_file("tools/missing.py")


def test_real_repo_does_not_link_claude_local_md():
    tracked = site._tracked_files()
    assert tracked is None or "CLAUDE.local.md" not in tracked


def test_untracked_but_not_ignored_file_is_linkable(tmp_path, monkeypatch):
    """A new file not yet `git add`-ed still links, so a rebuild before commit matches CI (TST-R)."""
    import subprocess

    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / ".gitignore").write_text("secret.md\n", encoding="utf-8")
    (tmp_path / "new.md").write_text("x", encoding="utf-8")
    (tmp_path / "secret.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(site, "ROOT", tmp_path)
    monkeypatch.setattr(site, "_TRACKED_LOADED", False)
    assert site._linkable_file("new.md")
    assert not site._linkable_file("secret.md")
