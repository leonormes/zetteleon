#!/usr/bin/env python3
"""
check_status_drift.py - flags prose and frontmatter that still use a retired `status` value.

The allowed values live in 10_System/schema/status.yaml. This script reports:
  - `status: <retired>` anywhere in a file's frontmatter;
  - a retired value in backticks on a line that talks about `status`, Tier 1/2 or promotion
    (lines about prodos.lifecycle / trust, and dated or "retired" history lines, are skipped).

Usage:
    uv run --with pyyaml python3 10_System/scripts/check_status_drift.py
Exit code 1 if any drift is found.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import status_schema  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".obsidian", "node_modules", "99_Archive", "BookFusion", "assets", "01_journals", "90_Audits"}
retired = "|".join(sorted(status_schema.RETIRED))
FM_RE = re.compile(rf"^status:\s*['\"]?({retired})['\"]?\s*$")
TICK_RE = re.compile(rf"`({retired})`|\b(?:status|tier\s*[12])\b[^\n]*?\b({retired})\b", re.I)
CONTEXT_RE = re.compile(r"status|tier\s*[12]|promot", re.I)
SAFE_RE = re.compile(r"lifecycle|prodos\.|trust|retired|migrat|legacy|older|^\s*[-*]?\s*20\d\d-\d\d-\d\d", re.I)


def main() -> int:
    hits = []
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
    print(f"\nstatus drift: {len(hits)} hit(s); allowed = {sorted(status_schema.VALUES)}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
