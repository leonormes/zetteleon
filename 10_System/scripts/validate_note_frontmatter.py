#!/usr/bin/env python3
"""
validate_note_frontmatter.py — ProdOS Frontmatter Validator

Validates every markdown note in the vault against SoT - ProdOS Frontmatter
Contract (Note Type Schemas). Reports errors for missing required fields,
invalid types, and conformance violations.

Usage:
    uv run --with pyyaml python3 10_System/scripts/validate_note_frontmatter.py
    uv run --with pyyaml python3 10_System/scripts/validate_note_frontmatter.py --path "30_Library/SoT/SoT - Flow Engineering.md"
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
    "project", "sot",
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
}


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


def validate_note(path, relative_path):
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
    files_with_errors = 0
    error_details = defaultdict(list)

    for fpath in files_to_check:
        try:
            rel = fpath.relative_to(VAULT_ROOT)
        except ValueError:
            rel = fpath
        errs = validate_note(fpath, rel)
        if errs:
            files_with_errors += 1
            total_errors += len(errs)
            for e in errs:
                error_details[str(rel)].append(e)

    # Report
    if error_details:
        print(f"\n=== PRODOS FRONTMATTER VALIDATION ===\n")
        for fname in sorted(error_details):
            print(f"  ✗ {fname}")
            for e in error_details[fname]:
                print(f"      {e}")
        print(f"\n{files_with_errors} file(s) with errors, {total_errors} total error(s)")
        sys.exit(1)
    else:
        print(f"No frontmatter violations found.\n")
        print(f"scanned {len(files_to_check)} notes · 0 error(s), 0 warning(s)")
        sys.exit(0)


if __name__ == "__main__":
    main()