#!/usr/bin/env python3
"""
check_status_drift.py - flags prose and frontmatter that still use a retired `status` value.

The allowed values live in 10_System/schema/status.yaml. This script reports:
  - `status: <retired>` anywhere in a file's frontmatter;
  - a retired value in backticks on a line that talks about `status`, Tier 1/2 or promotion
    (lines about prodos.lifecycle / trust, and dated or "retired" history lines, are skipped).

It also compares the hand-synced copies of the vocabularies with 10_System/schema/*.yaml:
the `type`, `status` and `epistemic_status` options in the Note and claim fileClasses, and the
status / epistemic_status dropdown in Template - Claim. A copy that differs is a hit.

Usage:
    uv run --with pyyaml python3 10_System/scripts/check_status_drift.py
Exit code 1 if any drift is found.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import schema  # noqa: E402
import yaml  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".obsidian", "node_modules", "99_Archive", "BookFusion", "assets", "01_journals", "90_Audits"}
retired = "|".join(sorted(schema.RETIRED))
FM_RE = re.compile(rf"^status:\s*['\"]?({retired})['\"]?\s*$")
TICK_RE = re.compile(rf"`({retired})`|\b(?:status|tier\s*[12])\b[^\n]*?\b({retired})\b", re.I)
CONTEXT_RE = re.compile(r"status|tier\s*[12]|promot", re.I)
SAFE_RE = re.compile(r"lifecycle|prodos\.|trust|retired|migrat|legacy|older|^\s*[-*]?\s*20\d\d-\d\d-\d\d", re.I)


def fileclass_options(path: Path, field: str) -> set[str] | None:
    text = path.read_text(encoding="utf-8")
    fm = yaml.safe_load(text.split("---", 2)[1]) or {}
    for f in fm.get("fields", []):
        if f.get("name") == field:
            return set(f.get("options") or [])
    return None


def synced_copy_hits() -> list[tuple[Path, int, str]]:
    hits = []
    checks = [
        ("10_System/fileClasses/Note.md", "type", schema.TYPE),
        ("10_System/fileClasses/Note.md", "status", schema.VALUES),
        ("10_System/fileClasses/claim.md", "epistemic_status", schema.EPISTEMIC_STATUS),
    ]
    for rel, field, want in checks:
        p = ROOT / rel
        got = fileclass_options(p, field)
        if got is None:
            hits.append((p, 0, f"field '{field}' not found"))
        elif got != want:
            hits.append((p, 0, f"{field} options differ from schema: missing {sorted(want - got)}, extra {sorted(got - want)}"))
    tpl = ROOT / "10_System/templates/Template - Claim.md"
    for field, want in (("status", schema.VALUES), ("epistemic_status", schema.EPISTEMIC_STATUS)):
        m = re.search(rf"inlineSelect\(((?:option\([^)]*\)(?:, )?)+)\):{field}\]", tpl.read_text(encoding="utf-8"))
        got = set(re.findall(r"option\(([^)]*)\)", m.group(1))) if m else None
        if got is None:
            hits.append((tpl, 0, f"{field} dropdown not found"))
        elif got != want:
            hits.append((tpl, 0, f"{field} dropdown differs from schema: missing {sorted(want - got)}, extra {sorted(got - want)}"))
    return hits


def main() -> int:
    hits = synced_copy_hits()
    for p in ROOT.rglob("*.md"):
        if SKIP_DIRS & set(p.relative_to(ROOT).parts):
            continue
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        in_fm = bool(lines) and lines[0] == "---"
        for i, line in enumerate(lines, 1):
            if i > 1 and in_fm and line == "---":
                in_fm = False
                continue
            if in_fm and FM_RE.match(line):
                hits.append((p, i, line.strip()))
            elif not in_fm and CONTEXT_RE.search(line) and re.search(rf"`({retired})`", line) and not SAFE_RE.search(line):
                hits.append((p, i, line.strip()[:140]))
    for p, i, text in hits:
        print(f"{p.relative_to(ROOT)}:{i}: {text}")
    print(f"\nstatus drift: {len(hits)} hit(s); allowed = {sorted(schema.VALUES)}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
