#!/usr/bin/env python3
"""
validate_note_frontmatter.py — ProdOS Frontmatter Validator

Validates every markdown note in the vault against SoT - ProdOS Frontmatter
Contract (Note Type Schemas). Reports errors for missing required fields,
invalid types, and conformance violations.

Usage:
    uv run --with pyyaml python3 10_System/scripts/validate_note_frontmatter.py
    uv run --with pyyaml python3 10_System/scripts/validate_note_frontmatter.py --path "30_Library/100_zettelkasten/SoT - Flow Engineering.md"
    uv run --with pyyaml python3 10_System/scripts/validate_note_frontmatter.py --folder 30_Library/100_zettelkasten
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# Vault root — resolve from env or assume cwd
VAULT_ROOT = Path(os.environ.get("OBSIDIAN_VAULT_PATH", os.getcwd()))

# Canonical type enum per §2
VALID_TYPES = {
    "claim", "concept", "evidence", "question",
    "procedure", "protocol", "map", "journal",
    "project", "sot", "link_report", "equipment", "source", "prompt", "tombstone",
    "problem",
}

# Prodos.kind enum per §4.1
VALID_PRODOS_KINDS = {
    "head", "sot", "protocol", "moc", "atomic",
    "project", "ops", "prompt", "journal",
}

# Prodos.lifecycle enum per §4.1
VALID_PRODOS_LIFECYCLES = {
    "seedling", "active", "stable", "evergreen", "archived",
}

# status enum per the base `Note` fileClass (10_System/fileClasses/Note.md) — inherited by
# every canonical note type, including claim. Empty-string/literal-"null" legacy values are
# common migration artifacts and are just as invalid to the Bases plugin as any other
# out-of-enum string.
VALID_STATUS = {"draft", "seed", "stable", "evergreen", "stale", "superseded", "archived"}
QUESTION_STATUS = VALID_STATUS | {"open", "thinking", "resolved"}
PROBLEM_STATUS = VALID_STATUS | {"captured", "clarifying", "active-project", "mitigated", "accepted-constraint"}

# Fields whose fileClass type is MultiFile at the base `Note` level (not type-specific) —
# same "must be a list, not a bare scalar" rule as TYPE_SCHEMA_LIST_FIELDS below, just
# universal instead of per-type.
UNIVERSAL_LIST_FIELDS = {"supersedes", "superseded_by"}

# Scopes per §8
SCOPED_FOLDERS = {
    "30_Library", "20_Thinking", "10_System",
    "01_journals", "00_Inbox",
}

# Required frontmatter fields per §2
REQUIRED_FIELDS = ["title", "type", "tags", "conformant"]

# Conditional field per §2
CONDITIONAL_FIELDS = {"non_conformance_reason": "conformant"}

# Schema-specific required fields per §3
TYPE_SCHEMAS = {
    "claim": {"proposition", "epistemic_status", "evidence_links", "contradicts"},
    "concept": {"definition", "distinguishes_from", "used_in_claims"},
    "evidence": {"source_quote", "source_reference", "supports_claims", "confidence"},
    "question": {"tension", "candidate_answers", "related_claims"},
    "procedure": {"trigger", "steps", "verification"},
    "problem": {"role", "status"},
}

# Schema-specific enum fields per the fileClass Select definitions (10_System/fileClasses/*.md).
# A field merely being *present* is not enough — the Fileclass/Bases plugin enforces these
# values live in Obsidian, so the script must too or it silently passes what the UI flags.
TYPE_SCHEMA_ENUMS = {
    "claim": {"epistemic_status": {"high", "medium", "low", "unknown"}},
    "problem": {"role": {"symptom", "root-cause", "constraint"}},
}

# Fields whose fileClass type is MultiFile — must be a list (of wikilinks), never a bare
# string/scalar, or the Bases plugin will reject the row even though the field is "present".
TYPE_SCHEMA_LIST_FIELDS = {
    "claim": {"evidence_links", "contradicts"},
}

# Soft synonym warnings for flat/drift tags that have a canonical counterpart in
# [[SoT - Canonical Interest Tags]]. Matched case-insensitively (stripped of leading '#').
# These emit warnings only — never errors — so existing notes are not blocked.
ADHD_TAG_QUALIFIERS = {
    "adhd-tools",
    "adhd-friendly",
    "adhd-optimization",
    "adhd-self-compassion",
}

CANONICAL_TAG_SYNONYMS = {
    "adhd": "TheHuman/Health/ADHD",
    "topic/adhd": "TheHuman/Health/ADHD",
    "pkm": "domain/pkm",
    "topic/pkm": "domain/pkm",
    "productivity": "topic/productivity",
    "epistemology": "topic/epistemology",
    "philosophy": "TheHuman/Philosophy",
    "cognition": "TheHuman/Cognition",
    "psychology": "TheHuman/Psychology",
    "maths": "topic/maths",
    "math": "topic/maths",
    "mathematics": "topic/maths",
    "architecture": "SoftwareEngineering/Architecture",
    "software-architecture": "SoftwareEngineering/Architecture",
    "llm": "domain/llm",
    "ai": "domain/llm",
    "infrastructure": "domain/infrastructure",
    "kubernetes": "domain/infrastructure",
    "devops": "domain/infrastructure",
    "family": "TheHuman/Family",
    "health": "TheHuman/Health",
    "culture": "topic/culture",
    "storytelling": "topic/culture",
}


def collect_tag_warnings(fm):
    """Return soft warnings for flat/drift tags with canonical interest-tag counterparts."""
    tags = fm.get("tags")
    if not isinstance(tags, (list, tuple)):
        return []
    tag_set = {str(t).lstrip("#").strip() for t in tags if t is not None}
    warnings = []
    for raw_tag in tags:
        if raw_tag is None:
            continue
        tag = str(raw_tag).lstrip("#").strip()
        lower = tag.lower()
        if lower in ADHD_TAG_QUALIFIERS:
            continue
        canonical = CANONICAL_TAG_SYNONYMS.get(lower)
        if canonical and tag != canonical and canonical not in tag_set:
            warnings.append(
                f"tag '{tag}' has canonical interest tag '{canonical}' (see SoT - Canonical Interest Tags)"
            )
    return warnings


def parse_frontmatter(content):
    """Extract YAML frontmatter as a dict. Returns (fm_dict, error)."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, "no frontmatter block found"
    try:
        import yaml
        fm = yaml.safe_load(match.group(1))
        if not isinstance(fm, dict):
            return None, "frontmatter is not a mapping"
        return fm, None
    except Exception as e:
        return None, f"YAML parse error: {e}"


def validate_fileclass_schema(fm, path):
    """Validate a fileClass schema definition in 10_System/fileClasses/."""
    errors = []
    if "type" in fm:
        errors.append("fileClass schema must not set top-level 'type' (would self-bind via fileClassAlias)")
    if path.name != "Note.md" and fm.get("extends") != "Note":
        errors.append("fileClass schema must declare 'extends: Note'")
    fields = fm.get("fields")
    if not isinstance(fields, list) or not fields:
        errors.append("fileClass schema must declare a non-empty 'fields' list")
    else:
        for idx, f in enumerate(fields):
            if not isinstance(f, dict):
                errors.append(f"fields[{idx}] must be a mapping")
                continue
            for key in ("name", "id", "type"):
                if not f.get(key):
                    errors.append(f"fields[{idx}] missing required key '{key}'")
    return errors


def validate_note(path, relative_path, warnings_out=None):
    """Validate a single note's frontmatter. Returns list of error strings."""
    errors = []
    
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"read error: {e}"]

    fm, parse_err = parse_frontmatter(content)
    if parse_err:
        return [parse_err]
    if fm is None:
        return ["no parsable frontmatter"]

    if path.parent.name == "fileClasses":
        return validate_fileclass_schema(fm, path)

    if warnings_out is not None:
        warnings_out.extend(collect_tag_warnings(fm))

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] is None or fm[field] == "":
            errors.append(f"missing required field: '{field}'")
        elif field == "tags" and not isinstance(fm[field], (list, tuple)):
            errors.append(f"'tags' must be a list, got {type(fm[field]).__name__}")
        elif field == "conformant" and not isinstance(fm[field], bool):
            errors.append(f"'conformant' must be boolean, got {type(fm[field]).__name__}")

    # Check conditional field
    conformant = fm.get("conformant")
    if conformant is False:
        if "non_conformance_reason" not in fm or not fm["non_conformance_reason"]:
            errors.append("missing 'non_conformance_reason' (required when conformant: false)")

    # Validate type enum
    note_type = fm.get("type")
    if note_type and note_type not in VALID_TYPES:
        errors.append(f"invalid type '{note_type}' — must be one of {sorted(VALID_TYPES)}")

    # Validate status enum (base Note fileClass field — optional, but must be a real
    # enum value if present at all; a stray '' or literal-string 'null' is still invalid).
    status = fm.get("status")
    if note_type == "question":
        allowed_status = QUESTION_STATUS
    elif note_type == "problem":
        allowed_status = PROBLEM_STATUS
    else:
        allowed_status = VALID_STATUS
    if status is not None and status != "" and status not in allowed_status:
        errors.append(f"invalid 'status' value '{status}' — must be one of {sorted(allowed_status)}")
    elif status == "":
        errors.append("'status' is an empty string — remove the field entirely or set a valid value")

    # 'superseded' is conditional on having something to point at, same pattern as
    # conformant/non_conformance_reason above.
    if status == "superseded":
        if not fm.get("superseded_by"):
            errors.append("missing 'superseded_by' (required when status: superseded)")

    # Universal MultiFile-typed fields (base Note schema, not type-specific): a bare scalar
    # is a common hand-written mistake — the fileClass field type is MultiFile, so the
    # Bases plugin expects a list even when there's only one target.
    for field in UNIVERSAL_LIST_FIELDS:
        value = fm.get(field)
        if value is not None and value != "" and not isinstance(value, (list, tuple)):
            errors.append(f"'{field}' must be a list, got {type(value).__name__}")

    # Validate prodos object if present
    prodos = fm.get("prodos")
    if prodos and isinstance(prodos, dict):
        kind = prodos.get("kind")
        if kind and kind not in VALID_PRODOS_KINDS:
            errors.append(f"invalid prodos.kind '{kind}' — must be one of {sorted(VALID_PRODOS_KINDS)}")
        lifecycle = prodos.get("lifecycle")
        if lifecycle and lifecycle not in VALID_PRODOS_LIFECYCLES:
            errors.append(f"invalid prodos.lifecycle '{lifecycle}' — must be one of {sorted(VALID_PRODOS_LIFECYCLES)}")

    # Validate type-specific schema if conformant
    if conformant is True and note_type in TYPE_SCHEMAS:
        for field in TYPE_SCHEMAS[note_type]:
            if field not in fm or fm[field] is None:
                errors.append(f"missing schema field '{field}' for type '{note_type}' (required when conformant: true)")

        # Enum-valued schema fields: presence isn't enough, the value must be a valid option.
        for field, allowed in TYPE_SCHEMA_ENUMS.get(note_type, {}).items():
            value = fm.get(field)
            if value is not None and value not in allowed:
                errors.append(
                    f"invalid '{field}' value '{value}' for type '{note_type}' — must be one of {sorted(allowed)}"
                )

        # MultiFile-typed schema fields must be lists, not bare scalars.
        for field in TYPE_SCHEMA_LIST_FIELDS.get(note_type, set()):
            value = fm.get(field)
            if value is not None and not isinstance(value, (list, tuple)):
                errors.append(
                    f"'{field}' must be a list for type '{note_type}', got {type(value).__name__}"
                )

        if note_type == "problem" and "impact" in fm and fm["impact"] is not None:
            impact = fm["impact"]
            if isinstance(impact, bool) or not isinstance(impact, (int, float)) or not (1 <= impact <= 5):
                errors.append(
                    f"invalid 'impact' value '{impact}' for type 'problem' — must be a number between 1 and 5"
                )

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate note frontmatter against ProdOS schema")
    parser.add_argument("--path", type=str, help="Validate a single file")
    parser.add_argument("--folder", type=str, help="Validate all notes in a folder (relative to vault root)")
    parser.add_argument("--audit", action="store_true", help="Full vault audit across all scoped folders")
    args = parser.parse_args()

    if not any([args.path, args.folder, args.audit]):
        parser.print_help()
        sys.exit(1)

    files_to_check = []

    if args.path:
        p = Path(args.path)
        if not p.is_absolute():
            p = VAULT_ROOT / p
        if p.exists():
            files_to_check.append(p)
        else:
            print(f"File not found: {p}")
            sys.exit(1)

    elif args.folder:
        folder = VAULT_ROOT / args.folder
        if folder.exists():
            files_to_check.extend(folder.rglob("*.md"))
        else:
            print(f"Folder not found: {folder}")
            sys.exit(1)

    elif args.audit:
        for folder_name in SCOPED_FOLDERS:
            folder = VAULT_ROOT / folder_name
            if folder.exists():
                files_to_check.extend(folder.rglob("*.md"))

    # Sort for deterministic output
    files_to_check.sort()

    total_errors = 0
    total_warnings = 0
    files_with_errors = 0
    error_details = defaultdict(list)
    warning_details = defaultdict(list)

    for fpath in files_to_check:
        try:
            rel = fpath.relative_to(VAULT_ROOT)
        except ValueError:
            rel = fpath
        file_warnings = []
        errs = validate_note(fpath, rel, warnings_out=file_warnings)
        if errs:
            files_with_errors += 1
            total_errors += len(errs)
            for e in errs:
                error_details[str(rel)].append(e)
        if file_warnings:
            total_warnings += len(file_warnings)
            warning_details[str(rel)].extend(file_warnings)

    # Report
    if warning_details:
        print(f"\n=== TAG SYNONYM WARNINGS ({total_warnings}) ===\n")
        for fname in sorted(warning_details):
            print(f"  ! {fname}")
            for w in warning_details[fname]:
                print(f"      {w}")

    if error_details:
        print(f"\n=== PRODOS FRONTMATTER VALIDATION ===\n")
        for fname in sorted(error_details):
            print(f"  ✗ {fname}")
            for e in error_details[fname]:
                print(f"      {e}")
        print(f"\n{files_with_errors} file(s) with errors, {total_errors} total error(s), {total_warnings} warning(s)")
        sys.exit(1)
    else:
        print(f"No frontmatter violations found.\n")
        print(f"scanned {len(files_to_check)} notes · 0 error(s), {total_warnings} warning(s)")
        sys.exit(0)


if __name__ == "__main__":
    main()