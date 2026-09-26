#!/usr/bin/env python3
"""
validate_note_shape.py - checks that an atomic note has the shape defined in
SoT - Atomic Note Standard (The Proposition Card).

The frontmatter contract is checked by validate_note_frontmatter.py. This script
checks what that one does not: the body (the card), the title, the links and a few
frontmatter rules that the Obsidian Linter makes fatal (no ": ", apostrophes or double
quotes in string values; no prodos or uid keys; confidence on evidence notes only).

Scope (the ratchet): notes in 30_Library/100_zettelkasten/ of type claim, concept,
evidence or procedure, created on or after EFFECTIVE, not superseded. Older notes are
frozen. A note with conformant: false and a non_conformance_reason has its errors
reported as warnings.

Usage (run from anywhere; the vault root is found from this file's location):
    uv run --with pyyaml python3 10_System/scripts/validate_note_shape.py            # all in-scope notes
    uv run --with pyyaml python3 10_System/scripts/validate_note_shape.py --path "30_Library/100_zettelkasten/Some Note.md"
    uv run --with pyyaml python3 10_System/scripts/validate_note_shape.py --staged   # what the pre-commit hook runs
    uv run --with pyyaml python3 10_System/scripts/validate_note_shape.py --report   # legacy shape statistics, never fails
    uv run --with pyyaml python3 10_System/scripts/validate_note_shape.py --self-test

Exit code 1 if any in-scope note has an error. SKIP_NOTE_SHAPE=1 makes the script exit 0.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: run with `uv run --with pyyaml python3 ...`")

ROOT = Path(__file__).resolve().parents[2]
FOLDER = "30_Library/100_zettelkasten"
EFFECTIVE = "2026-09-26"  # the standard applies to notes created on or after this date
SHAPE_TYPES = {"claim", "concept", "evidence", "procedure"}
VALID_TYPES = {
    "claim", "concept", "evidence", "question", "procedure", "protocol",
    "map", "journal", "project", "sot", "link_report", "equipment",
}
VALID_STATUS = {"draft", "seed", "stable", "evergreen", "stale", "superseded"}
VALID_EPISTEMIC = {"high", "medium", "low", "unknown"}

# Keys the Obsidian Linter deletes on save, or that the standard drops.
FORBIDDEN_KEYS = {"uid", "purpose", "epistemic", "updated", "creation_date", "last_reviewed"}

REQUIRED_COMMON = ["title", "type", "tags", "conformant", "created", "modified"]
TYPE_REQUIRED = {
    "claim": ["proposition", "epistemic_status", "evidence_links", "contradicts"],
    "concept": ["definition", "distinguishes_from", "used_in_claims"],
    "evidence": ["source_quote", "source_reference", "supports_claims", "confidence"],
    "procedure": ["trigger", "steps", "verification"],
}
LIST_FIELDS = {"evidence_links", "contradicts", "distinguishes_from", "used_in_claims",
               "supports_claims", "steps", "tags", "aliases"}

CARD_SECTIONS = ["scope & conditions", "evidence", "implications", "steelman",
                 "related", "tensions", "see also", "further reading"]
CARD_REQUIRED = ["scope & conditions", "evidence", "implications"]
EVIDENCE_SECTIONS = ["what it supports", "what it does not show"]
ANNOTATED_SECTIONS = {"related", "tensions"}
LINK_SECTIONS = {"related", "tensions", "see also"}

WIKILINK = re.compile(r"\[\[([^\]]+?)\]\]")
ABBREV = ("e.g.", "i.e.", "vs.", "etc.", "cf.", "dr.", "mr.", "mrs.", "no.", "fig.", "approx.")


# ---------------------------------------------------------------- parsing helpers

def split_note(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return {"_yaml_error": str(e).splitlines()[0]}, m.group(2)
    return (fm if isinstance(fm, dict) else {}), m.group(2)


def strip_code(body):
    """Blank out fenced code blocks and inline code so they are not parsed as content."""
    body = re.sub(r"^```.*?^```", lambda m: "\n" * m.group(0).count("\n"), body, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "``", body)


def created_date(fm):
    v = fm.get("created")
    return str(v)[:10] if v else ""


def sentence_count(text):
    text = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return 0
    parts, buf = [], ""
    tokens = re.split(r"(?<=[.!?])\s+", text)
    for tok in tokens:
        buf = (buf + " " + tok).strip() if buf else tok
        low = buf.lower()
        if low.endswith(ABBREV):
            continue
        parts.append(buf)
        buf = ""
    if buf:
        parts.append(buf)
    return len(parts)


def sections(body):
    """Return (title_line_index, [(level, name, start, end)]) for headings in stripped body."""
    lines = body.split("\n")
    heads = [(i, len(m.group(1)), m.group(2).strip())
             for i, l in enumerate(lines) if (m := re.match(r"^(#{1,6}) (.+?)\s*$", l))]
    return lines, heads


# ---------------------------------------------------------------- vault index (for dangling links)

_INDEX = None


def vault_index():
    global _INDEX
    if _INDEX is not None:
        return _INDEX
    names, aliases = set(), set()
    for dirpath, dirnames, files in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".obsidian", "node_modules")]
        for f in files:
            if not f.endswith(".md"):
                continue
            names.add(f[:-3])
            if dirpath.startswith(str(ROOT / "30_Library")):
                try:
                    head = (Path(dirpath) / f).read_text(errors="ignore")[:1500]
                except OSError:
                    continue
                if "aliases" in head:
                    fm, _ = split_note(head + ("\n---\n" if "\n---\n" not in head[4:] else ""))
                    a = (fm or {}).get("aliases")
                    if isinstance(a, list):
                        aliases.update(str(x) for x in a)
                    elif isinstance(a, str):
                        aliases.add(a)
    _INDEX = (names, aliases)
    return _INDEX


def link_target(raw):
    t = raw.split("|")[0].split("#")[0].split("^")[0].strip()
    return t[:-3] if t.endswith(".md") else t


# ---------------------------------------------------------------- the checks

def check_note(path, text, check_links=True):
    """Return a list of (severity, code, message)."""
    f = []
    err = lambda code, msg: f.append(("error", code, msg))
    warn = lambda code, msg: f.append(("warn", code, msg))
    fm, body = split_note(text)
    stem = Path(path).stem
    if fm is None:
        err("FM0", "no frontmatter")
        return f
    if "_yaml_error" in fm:
        err("FM0", "frontmatter is not valid YAML: " + fm["_yaml_error"])
        return f
    ntype = fm.get("type")

    # ---- frontmatter
    for k in REQUIRED_COMMON:
        if k not in fm or fm[k] in (None, "", []):
            err("FM1", f"missing required field '{k}'")
    if ntype not in VALID_TYPES:
        err("FM2", f"type '{ntype}' is not one of the Contract types")
    if fm.get("title") not in (None, stem) and str(fm.get("title")) != stem:
        err("FM3", f"title '{fm.get('title')}' does not match the filename '{stem}'")
    if fm.get("conformant") is not None and not isinstance(fm.get("conformant"), bool):
        err("FM4", "conformant must be true or false")
    if fm.get("conformant") is False and not fm.get("non_conformance_reason"):
        err("FM4", "conformant: false needs a non_conformance_reason")
    for k in fm:
        if str(k).startswith("prodos"):
            err("FM5", f"'{k}' is dropped for atomic notes (the Linter deletes it): remove it")
        elif k in FORBIDDEN_KEYS:
            err("FM5", f"legacy key '{k}' must not be written")
    if "confidence" in fm and ntype != "evidence":
        err("FM6", "'confidence' belongs to evidence notes only")
    for k in TYPE_REQUIRED.get(ntype, []):
        if k not in fm:
            err("FM7", f"{ntype} note is missing '{k}'")
            continue
        v = fm[k]
        if k in LIST_FIELDS and not isinstance(v, list):
            err("FM7", f"'{k}' must be a list")
        elif k not in LIST_FIELDS and k != "confidence" and (not isinstance(v, str) or not v.strip()):
            err("FM7", f"'{k}' must be a non-empty text value")
    if ntype == "evidence":
        c = fm.get("confidence")
        if not isinstance(c, (int, float)) or isinstance(c, bool) or not 0 <= c <= 1:
            err("FM6", "evidence 'confidence' must be a number from 0 to 1")
        if not fm.get("supports_claims"):
            err("FM7", "evidence note needs at least one entry in 'supports_claims'")
    if ntype == "procedure" and not fm.get("steps"):
        err("FM7", "procedure note needs at least one step")
    if ntype == "claim" and fm.get("epistemic_status") not in (None, *VALID_EPISTEMIC):
        err("FM7", f"epistemic_status must be one of {sorted(VALID_EPISTEMIC)}")
    if fm.get("status") not in (None, *VALID_STATUS):
        err("FM8", f"status '{fm.get('status')}' is not one of {sorted(VALID_STATUS)}")
    tags = fm.get("tags")
    if tags is not None and not isinstance(tags, list):
        err("FM1", "tags must be a list")

    # YAML-safe string values (the Linter's escaping breaks on these)
    def plain(key, val):
        if not isinstance(val, str) or val.startswith("[["):
            return
        bad = [n for n, ch in ((": ", ": "), ("apostrophe", "'"), ("double quote", '"')) if ch in val]
        if bad:
            (warn if key == "source_quote" else err)(
                "FM9", f"'{key}' contains {', '.join(bad)}: reword it (the Linter breaks on these)")
    for k, v in fm.items():
        if isinstance(v, str):
            plain(k, v)
        elif isinstance(v, list):
            for item in v:
                plain(k, item)

    # ---- title
    words = len(stem.split())
    if ntype == "claim":
        if stem.endswith("?"):
            err("T1", "a claim's title is a statement, not a question")
        if words < 4:
            err("T1", f"claim title has {words} words: a claim is titled by a full declarative sentence")
    if ntype == "evidence" and not stem.startswith("Evidence - "):
        warn("T2", "evidence titles start with 'Evidence - '")
    if ntype == "procedure" and not stem.lower().startswith("how to"):
        warn("T2", "procedure titles start with 'How to'")

    # ---- body
    clean = strip_code(body)
    lines, heads = sections(clean)
    if not clean.strip():
        err("B0", "empty body")
        return f
    if any(level == 1 for _, level, _ in heads):
        err("B1", "the body contains an H1 heading: the title is the H2")
    first = next((l for l in lines if l.strip()), "")
    if not first.startswith("## ") or first[3:].strip().lower() != stem.lower():
        err("B2", f"the first line of the body must be '## {stem}' (case aside)")

    h3 = [(i, n) for i, level, n in heads if level == 3]
    h4 = [(i, n) for i, level, n in heads if level == 4]
    if not h3 and h4 and any(n.lower() in CARD_SECTIONS + EVIDENCE_SECTIONS for _, n in h4):
        warn("B3", "section headings are H4: use H3 (the Linter renumbers them)")
    names = [n.lower() for _, n in h3]
    expected = EVIDENCE_SECTIONS if ntype == "evidence" else CARD_SECTIONS
    required = EVIDENCE_SECTIONS if ntype == "evidence" else CARD_REQUIRED
    for r in required:
        if r not in names:
            err("B3", f"missing required section '### {r.title()}'")
    for n in set(names):
        if names.count(n) > 1:
            err("B3", f"section '{n}' appears more than once")
        if n not in expected:
            warn("B3", f"unrecognised section '### {n}'")
    idx = [expected.index(n) for n in names if n in expected]
    if idx != sorted(idx):
        err("B4", "sections are out of order; the order is: " + ", ".join(expected))

    # opening statement
    first_h3 = h3[0][0] if h3 else len(lines)
    title_idx = next((i for i, l in enumerate(lines) if l.strip().startswith("## ")), 0)
    opening = "\n".join(lines[title_idx + 1:first_h3])
    opening_text = "\n".join(l for l in opening.split("\n") if not l.lstrip().startswith(">")).strip()
    if ntype != "evidence":
        if not opening_text:
            err("B5", "no opening statement between the title and the first section")
        else:
            n = sentence_count(opening_text)
            if n > 5:
                err("B5", f"opening statement has {n} sentences: it should be at most 3 (is this two notes?)")
            elif n > 3:
                warn("B5", f"opening statement has {n} sentences: it should be at most 3")
    else:
        if not any(l.lstrip().startswith(">") for l in opening.split("\n")):
            err("B5", "evidence note needs the source quote as a blockquote under the title")

    # empty sections, placeholder sections
    for pos, (i, n) in enumerate(h3):
        end = h3[pos + 1][0] if pos + 1 < len(h3) else len(lines)
        content = "\n".join(lines[i + 1:end]).strip()
        if not content:
            err("B6", f"section '### {n}' is empty: omit it instead")
        elif re.fullmatch(r"(none|n/a|none found\.?|tbd)", content.lower().strip("-* ")):
            err("B6", f"section '### {n}' is a placeholder: omit it instead")
        if n.lower() == "evidence" and ntype != "evidence" and not any(
                l.lstrip().startswith(">") for l in lines[i + 1:end]):
            warn("B7", "the Evidence section has no quotation; if the claim is your own reasoning, say so plainly")

    # links
    if re.search(r"\brel::", clean):
        err("L1", "'rel::' is not parsed by the compiler: use a typed edge [relationship:: [[Target]]]")
    targets = set()
    for pos, (i, n) in enumerate(h3):
        if n.lower() not in LINK_SECTIONS:
            continue
        end = h3[pos + 1][0] if pos + 1 < len(h3) else len(lines)
        for line in lines[i + 1:end]:
            if re.match(r"^\s*[-*] ", line) and WIKILINK.search(line):
                targets.update(link_target(m) for m in WIKILINK.findall(line))
                if n.lower() in ANNOTATED_SECTIONS and not re.search(r"\]\]\s*[—–:-]\s*\S", line):
                    err("L2", f"bare link under '### {n}': add the reason for the connection after the link")
    if len(targets) > 7:
        warn("L3", f"{len(targets)} links across Related, Tensions and See Also: at most 7 is the rule")
    if check_links:
        names_set, aliases = vault_index()
        raw_targets = {link_target(m) for m in WIKILINK.findall(clean)}
        for k in ("upstream", "evidence_links", "supports_claims", "used_in_claims", "distinguishes_from"):
            v = fm.get(k)
            for item in ([v] if isinstance(v, str) else v if isinstance(v, list) else []):
                if isinstance(item, str):
                    raw_targets.update(link_target(m) for m in WIKILINK.findall(item))
        missing = sorted(t for t in raw_targets if t and t not in names_set and t not in aliases
                         and not t.startswith("tmp_atoms"))
        for t in missing:
            err("L4", f"link to a note that does not exist: [[{t}]]")

    # atomicity heuristic
    wc = len(re.findall(r"\w+", clean))
    if wc > 450:
        warn("A1", f"{wc} words: a card should be short; check that this is one idea")
    return f


def in_scope(path, fm):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if not rel.startswith(FOLDER + "/") or fm is None:
        return False
    t = fm.get("type")
    if (t in VALID_TYPES and t not in SHAPE_TYPES) or fm.get("status") == "superseded":
        return False  # maps, SoTs, journals etc. keep their own shapes
    # a missing or non-canonical type (atom, permanent, blank) stays in scope so it is flagged as FM2
    d = created_date(fm)
    return (not d) or d >= EFFECTIVE  # a missing date means brand new: it is checked (and flagged FM1)


def downgrade(findings, fm):
    if fm and fm.get("conformant") is False and fm.get("non_conformance_reason"):
        return [("warn" if s == "error" else s, c, m + (" [downgraded: conformant false]" if s == "error" else ""))
                for s, c, m in findings]
    return findings


# ---------------------------------------------------------------- modes

def note_files(mode_paths=None, staged=False):
    if mode_paths:
        return [Path(p) if Path(p).is_absolute() else ROOT / p for p in mode_paths]
    if staged:
        out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                             cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
        return [ROOT / p for p in out if p.startswith(FOLDER + "/") and p.endswith(".md")]
    return sorted((ROOT / FOLDER).glob("*.md"))


def run(paths, explicit):
    errors = warnings = checked = 0
    for p in paths:
        if not p.exists():
            continue
        text = p.read_text(errors="ignore")
        fm, _ = split_note(text)
        if not explicit and not in_scope(p, fm):
            continue
        checked += 1
        findings = downgrade(check_note(p, text), fm)
        errs = [x for x in findings if x[0] == "error"]
        warns = [x for x in findings if x[0] == "warn"]
        errors += len(errs)
        warnings += len(warns)
        if findings:
            print(f"\n{os.path.relpath(p, ROOT)}")
            for s, c, m in findings:
                print(f"  {s.upper():5s} {c:3s} {m}")
    print(f"\nnote shape: {checked} note(s) checked, {errors} error(s), {warnings} warning(s)")
    return errors


def report():
    shapes, types, total = Counter(), Counter(), 0
    in_scope_n = 0
    for p in sorted((ROOT / FOLDER).glob("*.md")):
        text = p.read_text(errors="ignore")
        fm, body = split_note(text)
        total += 1
        types[str((fm or {}).get("type"))] += 1
        b = body.strip()
        heads = [h.lower() for h in re.findall(r"^#{2,4} (.+)$", b, re.M)]
        if b.startswith("## ") and all(x in heads for x in CARD_REQUIRED):
            shapes["card (the standard)"] += 1
        elif re.search(r"^(Summary|Details):", b, re.M):
            shapes["legacy Summary/Details"] += 1
        elif not heads:
            shapes["no headings"] += 1
        else:
            shapes["other"] += 1
        if in_scope(p, fm):
            in_scope_n += 1
    print(f"{total} notes in {FOLDER}")
    for k, n in shapes.most_common():
        print(f"  {n:5d}  {k}")
    canon = sum(n for t, n in types.items() if t in VALID_TYPES)
    print(f"  {total - canon:5d}  with a missing or non-canonical type")
    print(f"in scope for enforcement (created on or after {EFFECTIVE}): {in_scope_n}")


# ---------------------------------------------------------------- self-test

GOOD = """---
title: Pro-Social Punishment Restores Cooperation
type: claim
tags: [cooperation]
conformant: true
created: 2026-09-26T00:00:00+00:00
modified: 2026-09-26T00:00:00+00:00
proposition: Paying to punish free riders raises contributions.
epistemic_status: medium
evidence_links: []
contradicts: []
---

## Pro-Social Punishment Restores Cooperation

Paying to punish free riders raises contributions. It does so even when the punisher gains nothing.

### Scope & Conditions

Laboratory games only.

### Evidence

> "Contributions typically go up."
> (A source)

### Implications

- Punishment helps keep shared resources intact.

### Related

- [[Other Note]]—shared mechanism: the same pattern.
"""


def self_test():
    global _INDEX
    _INDEX = ({"Other Note"}, set())
    cases = [
        ("passes as written", GOOD, "Pro-Social Punishment Restores Cooperation", None),
        ("prodos key", GOOD.replace("contradicts: []", "contradicts: []\nprodos:\n  kind: atomic"), "Pro-Social Punishment Restores Cooperation", "FM5"),
        ("colon in a value", GOOD.replace("proposition: Paying to punish free riders raises contributions.", 'proposition: "Result: paying raises contributions."'), "Pro-Social Punishment Restores Cooperation", "FM9"),
        ("unquoted colon is invalid YAML", GOOD.replace("proposition: Paying to punish free riders raises contributions.", "proposition: Result: paying raises contributions."), "Pro-Social Punishment Restores Cooperation", "FM0"),
        ("label title on a claim", GOOD, "Punishment Effects", "T1"),
        ("H3 title", GOOD.replace("\n## Pro-Social", "\n### Pro-Social"), "Pro-Social Punishment Restores Cooperation", "B2"),
        ("missing Implications", GOOD.replace("### Implications\n\n- Punishment helps keep shared resources intact.\n\n", ""), "Pro-Social Punishment Restores Cooperation", "B3"),
        ("bare Related link", GOOD.replace("—shared mechanism: the same pattern.", ""), "Pro-Social Punishment Restores Cooperation", "L2"),
        ("dangling link", GOOD.replace("[[Other Note]]", "[[Missing Note]]"), "Pro-Social Punishment Restores Cooperation", "L4"),
        ("rel:: edge", GOOD + "\n[rel:: [[Other Note]]]\n", "Pro-Social Punishment Restores Cooperation", "L1"),
        ("empty section", GOOD.replace("Laboratory games only.", ""), "Pro-Social Punishment Restores Cooperation", "B6"),
        ("confidence on a claim", GOOD.replace("contradicts: []", "contradicts: []\nconfidence: high"), "Pro-Social Punishment Restores Cooperation", "FM6"),
    ]
    failed = 0
    for name, text, stem, want in cases:
        text2 = text.replace("title: Pro-Social Punishment Restores Cooperation", f"title: {stem}")
        codes = {c for s, c, m in check_note(f"{stem}.md", text2, check_links=True) if s == "error"}
        ok = (not codes) if want is None else (want in codes)
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  (wanted {want}, got {sorted(codes)})"))
        failed += 0 if ok else 1
    print("self-test:", "all passed" if not failed else f"{failed} failed")
    return failed


def main():
    ap = argparse.ArgumentParser(description="Check atomic notes against the Atomic Note Standard.")
    ap.add_argument("--path", nargs="+", help="check these files regardless of date or scope")
    ap.add_argument("--staged", action="store_true", help="check staged in-scope notes (pre-commit)")
    ap.add_argument("--report", action="store_true", help="print legacy shape statistics and exit 0")
    ap.add_argument("--self-test", action="store_true", help="run the built-in fixtures")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(1 if self_test() else 0)
    if a.report:
        report()
        return
    if os.environ.get("SKIP_NOTE_SHAPE") == "1":
        print("note shape: skipped (SKIP_NOTE_SHAPE=1)")
        return
    errors = run(note_files(a.path, a.staged), explicit=bool(a.path))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
