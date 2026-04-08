#!/usr/bin/env python3
"""
Extract YAML frontmatter from Markdown notes and validate `prodos` with CUE.

Requires: PyYAML, `cue` on PATH (unless --no-cue).
See: gemini-scribe/cue/README.md
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from shutil import which
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

SCRIPT_DIR = Path(__file__).resolve().parent
GEMINI_SCRIBE = SCRIPT_DIR.parent
VAULT_ROOT = GEMINI_SCRIBE.parent
CUE_SCHEMA = GEMINI_SCRIBE / "cue" / "prodos_frontmatter.cue"

SKIP_DIR_NAMES = frozenset({
    ".git",
    ".obsidian",
    ".history",
    ".trash",
    "node_modules",
    "Excalidraw",
    "Readwise",
    "attachments",
    "assets",
})


@dataclass
class ScanStats:
    files: int = 0
    no_frontmatter: int = 0
    yaml_errors: int = 0
    cue_errors: int = 0
    prodos_cue_ok: int = 0
    prodos_no_cue: int = 0
    legacy_no_prodos: int = 0


def repo_roots(args: argparse.Namespace) -> list[Path]:
    if args.roots:
        return [Path(p).resolve() for p in args.roots]
    return [
        VAULT_ROOT / "30_Library",
        VAULT_ROOT / "10_System" / "prompts",
        VAULT_ROOT / "20_Thinking" / "21_Workbench",
    ]


def path_is_skipped(path: Path) -> bool:
    return bool(SKIP_DIR_NAMES & set(path.parts))


def extract_frontmatter_block(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    # First line is ---; find closing ---
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end]


def strip_nulls(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: strip_nulls(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [strip_nulls(v) for v in obj]
    return obj


def json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    if isinstance(obj, datetime):
        if obj.tzinfo:
            return obj.isoformat()
        return obj.replace(tzinfo=None).isoformat() + "+00:00"
    if isinstance(obj, date):
        return obj.isoformat()
    return obj


def run_cue_vet(json_path: Path, schema: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["cue", "vet", "-d", "#Frontmatter", str(json_path), str(schema)],
        capture_output=True,
        text=True,
        cwd=json_path.parent,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--roots",
        nargs="*",
        help="Directories to scan (default: 30_Library, 10_System/prompts, 21_Workbench)",
    )
    parser.add_argument(
        "--enforce-prodos",
        action="store_true",
        help="Exit with error if a scanned note has parseable frontmatter but no prodos key.",
    )
    parser.add_argument(
        "--require-cue",
        action="store_true",
        help="Exit with error if `cue` is not on PATH.",
    )
    parser.add_argument(
        "--no-cue",
        action="store_true",
        help="Only parse YAML; do not run cue vet (reports legacy / missing prodos).",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=CUE_SCHEMA,
        help="Path to prodos_frontmatter.cue",
    )
    args = parser.parse_args()

    if yaml is None:
        print("Missing PyYAML. Install: pip install -r gemini-scribe/scripts/requirements-validate.txt", file=sys.stderr)
        return 2

    cue_bin = which("cue")
    if not args.no_cue and args.require_cue and not cue_bin:
        print("Required --require-cue but `cue` is not on PATH.", file=sys.stderr)
        return 2

    roots = repo_roots(args)
    missing_roots = [str(r) for r in roots if not r.is_dir()]
    if missing_roots:
        print(f"Warning: missing directories (skipping): {missing_roots}", file=sys.stderr)

    stats = ScanStats()
    schema_path = args.schema.resolve()
    if not schema_path.is_file():
        print(f"CUE schema not found: {schema_path}", file=sys.stderr)
        return 2

    exit_code = 0
    for root in roots:
        if not root.is_dir():
            continue
        for md in root.rglob("*.md"):
            if path_is_skipped(md):
                continue
            stats.files += 1
            try:
                raw = md.read_text(encoding="utf-8", errors="replace")
            except OSError as e:
                print(f"{md}: read error: {e}", file=sys.stderr)
                exit_code = 1
                continue
            block = extract_frontmatter_block(raw)
            if block is None:
                stats.no_frontmatter += 1
                continue
            try:
                data = yaml.safe_load(block) or {}
            except yaml.YAMLError as e:
                stats.yaml_errors += 1
                print(f"{md}: YAML error: {e}", file=sys.stderr)
                exit_code = 1
                continue
            if not isinstance(data, dict):
                print(f"{md}: frontmatter must be a mapping, got {type(data).__name__}", file=sys.stderr)
                stats.yaml_errors += 1
                exit_code = 1
                continue

            if "prodos" not in data:
                stats.legacy_no_prodos += 1
                if args.enforce_prodos:
                    print(f"{md}: missing prodos (enforce mode)", file=sys.stderr)
                    exit_code = 1
                continue

            payload = strip_nulls(json_safe(data))
            if args.no_cue or not cue_bin:
                stats.prodos_no_cue += 1
                continue

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".json",
                encoding="utf-8",
                delete=False,
            ) as tmp:
                json.dump(payload, tmp, ensure_ascii=False)
                tmp_path = Path(tmp.name)
            try:
                proc = run_cue_vet(tmp_path, schema_path)
            finally:
                tmp_path.unlink(missing_ok=True)

            if proc.returncode != 0:
                stats.cue_errors += 1
                print(f"{md}: CUE validation failed\n{proc.stderr}", file=sys.stderr)
                exit_code = 1
            else:
                stats.prodos_cue_ok += 1

    print(
        f"Scanned {stats.files} markdown files. "
        f"prodos+CUE ok: {stats.prodos_cue_ok}, prodos (YAML only, no cue): {stats.prodos_no_cue}, "
        f"legacy (no prodos): {stats.legacy_no_prodos}, no frontmatter block: {stats.no_frontmatter}, "
        f"YAML errors: {stats.yaml_errors}, CUE errors: {stats.cue_errors}."
    )
    if args.no_cue or not cue_bin:
        print(
            "Note: CUE was skipped (`--no-cue` or `cue` not on PATH); "
            "files with prodos were not schema-checked (see prodos_no_cue count).",
            file=sys.stderr,
        )

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
