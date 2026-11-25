#!/usr/bin/env python3
"""
check_all.py - one command for the vault's mandatory write gates (AGENTS.md 7.2).

Runs, over the notes you changed:
  1. frontmatter contract   (validate_note_frontmatter.py)  - new notes fail; edited legacy notes only report
  2. atomic note shape      (validate_note_shape.py)         - in-scope notes only (the script decides)
  3. typed edges            (edge_lint.py)                   - fails only on ERRORs in changed notes
  4. status drift           (check_status_drift.py)          - vault-wide, fails on any hit
  5. protected notes        (AGENTS.md 6.1)                  - no body edit, delete, move or own_words
     change to an own_words: true note or an existing note in 01_journals/ or 20_Thinking/.
     Enforced on --staged only when CLAUDECODE is set (agent sessions) or PROTECTED_GUARD=1, so your
     own commits stay frictionless; elsewhere it is a warning. Override: ALLOW_PROTECTED_EDIT=1.
     Moving a note out of 20_Thinking/21_Workbench/ passes when the change also adds a
     type: tombstone note with the same filename (the Workbench sweep).

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


PROTECTED_DIRS = ("01_journals/", "20_Thinking/")
WORKBENCH = "20_Thinking/21_Workbench/"
OWN_WORDS_RE = re.compile(r"^own_words:\s*true\s*$", re.M)


def show(spec: str) -> str | None:
    p = subprocess.run(["git", "-C", str(ROOT), "show", spec], capture_output=True)
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None


def split_note(text: str) -> tuple[str, str]:
    """Return (frontmatter, body). A note without frontmatter has an empty frontmatter."""
    m = re.match(r"---\n(.*?)\n---\n?(.*)\Z", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)


def norm_body(body: str) -> str:
    return "\n".join(l.rstrip() for l in body.replace("\r\n", "\n").split("\n")).strip()


def name_status(staged_only: bool) -> list[tuple[str, str, str]]:
    """(status letter, old path, new path) for every changed or untracked-added file."""
    args = ["diff", "--cached"] if staged_only else ["diff", "HEAD"]
    toks = git(*args, "--name-status", "-M", "-z")
    out, i = [], 0
    while i < len(toks):
        s = toks[i][0]
        if s in "RC":
            out.append((s, toks[i + 1], toks[i + 2])); i += 3
        else:
            out.append((s, toks[i + 1], toks[i + 1])); i += 2
    if not staged_only:
        out += [("A", u, u) for u in git("ls-files", "--others", "--exclude-standard", "-z")]
    return out


def protected_violations(staged_only: bool) -> list[str]:
    """Messages describing edits to protected notes (AGENTS.md 6.1). Empty if none."""
    entries = name_status(staged_only)

    def new_text(path: str) -> str | None:
        if staged_only:
            return show(f":{path}")
        f = ROOT / path
        return f.read_text(encoding="utf-8", errors="replace") if f.exists() else None

    tombstones = set()
    added = []  # (frontmatter, normalised body) of every added note, to recognise a moved copy
    for s, _, new in entries:
        if s == "A" and new.endswith(".md"):
            fm_a, body_a = split_note(new_text(new) or "")
            added.append((bool(OWN_WORDS_RE.search(fm_a)), norm_body(body_a)))
            if re.search(r"^type:\s*tombstone\s*$", fm_a, re.M):
                tombstones.add(Path(new).stem)

    out = []
    for s, old, new in entries:
        if s == "A" or not old.endswith(".md"):
            continue
        old_txt = show(f"HEAD:{old}")
        if old_txt is None:
            continue
        old_fm, old_body = split_note(old_txt)
        was_own = bool(OWN_WORDS_RE.search(old_fm))
        protected = old.startswith(PROTECTED_DIRS) or was_own
        new_txt = None if s == "D" else new_text(new)
        # Workbench sweep: the note was moved elsewhere (added copy, same body and own_words flag)
        # and a type: tombstone note now sits at the old path. Git stages that as a modification.
        if (
            s == "M" and old.startswith(WORKBENCH) and new_txt is not None
            and re.search(r"^type:\s*tombstone\s*$", split_note(new_txt)[0], re.M)
            and (was_own, norm_body(old_body)) in added
        ):
            continue
        if new_txt is not None and bool(OWN_WORDS_RE.search(split_note(new_txt)[0])) != was_own:
            out.append(f"{new}: own_words was added, removed or changed")
        if not protected:
            continue
        if s == "D" or new_txt is None:
            out.append(f"{old}: protected note deleted")
            continue
        if old != new and not (old.startswith(WORKBENCH) and Path(old).stem in tombstones):
            out.append(f"{old}: protected note moved or renamed to {new}")
        if norm_body(old_body) != norm_body(split_note(new_txt)[1]):
            out.append(f"{new}: protected note body changed")
    return out


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

    if not a.path:
        import os

        prot = protected_violations(a.staged)
        enforce = a.staged and (os.environ.get("CLAUDECODE") or os.environ.get("PROTECTED_GUARD") == "1")
        for v in prot:
            if os.environ.get("ALLOW_PROTECTED_EDIT") == "1":
                print(f"  note protected edit allowed by ALLOW_PROTECTED_EDIT=1: {v}")
            elif enforce:
                print(f"  FAIL protected {v}")
                failures.append(f"protected: {v}")
            else:
                print(f"  WARN protected {v}")
        if prot and enforce and os.environ.get("ALLOW_PROTECTED_EDIT") != "1":
            print("  (set ALLOW_PROTECTED_EDIT=1 to override; see AGENTS.md 6.1)")

    rc, out = run("check_status_drift.py")
    if rc != 0:
        failures.append("status drift")
        print(f"  FAIL status drift\n{out}\n")

    print("check_all: FAILED (" + "; ".join(failures[:6]) + ")" if failures else "check_all: all gates passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
