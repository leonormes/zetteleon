#!/usr/bin/env python3
"""
check_all.py - one command for the vault's mandatory write gates (AGENTS.md 7.2).

Runs, over the notes you changed:
  1. frontmatter contract   (validate_note_frontmatter.py)  - new notes fail; edited legacy notes only report
  2. atomic note shape      (validate_note_shape.py)         - in-scope notes only (the script decides)
  3. typed edges            (edge_lint.py)                   - fails only on ERRORs in changed notes
  4. status drift           (check_status_drift.py)          - vault-wide, fails on any hit

Legacy debt elsewhere in the vault never blocks a change. The quote gate (verify_quote.py) is
not run here: it needs a Calibre id, so run it by hand when a quotation changes.

Usage (from anywhere):
    uv run --with pyyaml python3 10_System/scripts/check_all.py --staged     # what the pre-commit hook runs
    uv run --with pyyaml python3 10_System/scripts/check_all.py              # staged + unstaged + untracked
    uv run --with pyyaml python3 10_System/scripts/check_all.py --path "30_Library/100_zettelkasten/X.md" ...
Exit code 1 if any gate fails. SKIP_NOTE_SHAPE=1 skips the shape gate (same switch as the script).
"""
import argparse
import sys as _sys

_sys.dont_write_bytecode = True  # importing validate_note_shape must not litter __pycache__
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent


def git(*args: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout
    return [l for l in out.split("\0" if "-z" in args else "\n") if l]


def changed_notes(staged_only: bool) -> tuple[list[str], set[str]]:
    """Return (changed .md paths, subset that are new: added or renamed)."""
    if staged_only:
        changed = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z", "--", "*.md")
        new = set(git("diff", "--cached", "--name-only", "--diff-filter=AR", "-z", "--", "*.md"))
    else:
        tracked = git("diff", "HEAD", "--name-only", "--diff-filter=ACMR", "-z", "--", "*.md")
        untracked = git("ls-files", "--others", "--exclude-standard", "-z", "--", "*.md")
        changed = sorted(set(tracked) | set(untracked))
        new = set(untracked) | set(git("diff", "HEAD", "--name-only", "--diff-filter=AR", "-z", "--", "*.md"))
    return changed, new


def run(script: str, *args: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True, cwd=ROOT)
    return p.returncode, (p.stdout + p.stderr).strip()


def edge_errors(changed: set[str]) -> list[str]:
    """Run edge_lint over the vault; keep only ERROR lines that belong to changed notes."""
    _, text = run("edge_lint.py", "--quiet")
    hits, current = [], None
    for line in text.splitlines():
        if line and not line.startswith(" ") and line.endswith(".md"):
            current = line.strip()
        elif current in changed and re.match(r"\s+ERROR\b", line):
            hits.append(f"{current}: {line.strip()}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--staged", action="store_true", help="only staged notes (pre-commit mode)")
    ap.add_argument("--path", nargs="+", help="check these notes instead of using git")
    a = ap.parse_args()

    if a.path:
        rels = [str(Path(p).resolve().relative_to(ROOT)) for p in a.path]
        changed, new = rels, set(rels)
    else:
        changed, new = changed_notes(a.staged)
    notes = [n for n in changed if (ROOT / n).exists()]
    failures: list[str] = []
    print(f"check_all: {len(notes)} changed note(s), {len(new & set(notes))} new")

    for n in notes:
        rc, out = run("validate_note_frontmatter.py", "--path", n)
        if rc != 0 and n in new:
            failures.append(f"frontmatter: {n}")
            print(f"  FAIL frontmatter {n}\n{out}\n")
        elif rc != 0:
            print(f"  (legacy note, frontmatter not enforced) {n}")

    # validate_note_shape.py --path checks files unconditionally, so apply its own scope rule
    # (ratchet date, claim/concept/evidence/procedure types, not superseded) here first.
    sys.path.insert(0, str(SCRIPTS))
    import validate_note_shape as shape

    in_library = []
    for n in notes:
        fm, _ = shape.split_note((ROOT / n).read_text(errors="ignore"))
        if shape.in_scope(ROOT / n, fm):
            in_library.append(n)
    if in_library:
        rc, out = run("validate_note_shape.py", "--path", *in_library)
        if rc != 0:
            failures.append("shape")
            print(f"  FAIL shape\n{out}\n")

    errs = edge_errors(set(notes))
    for e in errs:
        print(f"  FAIL edges {e}")
    failures += [f"edges: {e}" for e in errs]

    rc, out = run("check_status_drift.py")
    if rc != 0:
        failures.append("status drift")
        print(f"  FAIL status drift\n{out}\n")

    print("check_all: FAILED (" + "; ".join(failures[:6]) + ")" if failures else "check_all: all gates passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
