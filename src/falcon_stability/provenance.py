"""Code-version stamp written next to every result row."""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]


def git_state() -> dict:
    def run(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    sha = run("rev-parse", "--short", "HEAD") or "unknown"
    dirty = bool(run("status", "--porcelain", "--", "src", "scripts", "configs"))
    return {"git_sha": sha, "code_dirty": dirty}
