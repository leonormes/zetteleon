#!/usr/bin/env python3
"""
calibre_topic_migrate.py

Migrates Calibre ProdOS Topic values from legacy free-text tags to the
canonical vocabulary defined in topics_whitelist.json.

Usage:
  python3 calibre_topic_migrate.py           # dry-run (default, safe)
  python3 calibre_topic_migrate.py --apply   # write changes to Calibre

Phases:
  1. Unambiguous token remapping (automated)
  2. ['Cognition', 'Productivity'] disambiguation via title keyword scoring
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPTS_DIR = Path(__file__).parent
TOPICS_FILE = SCRIPTS_DIR / "topics_whitelist.json"

# Old single-token → new whitelist name (unambiguous)
TOKEN_MAP: dict[str, str] = {
    "Networking":         "Network Engineering",
    "Kubernetes":         "Platform Engineering & Containers",
    "Containers":         "Platform Engineering & Containers",
    "Data Structures":    "Data-Centric Software Engineering",
    "Database Internals": "Data-Centric Software Engineering",
    "Rust":               "Data-Centric Software Engineering",
    "Mathematics":        "Applied Mathematics & Formal Logic",
}

# Keywords for scoring ambiguous ['Cognition', 'Productivity'] books
ADHD_SIGNALS = [
    "brain", "neuro", "attention", "adhd", "habit", "memory", "cognitive",
    "psychology", "emotion", "mind", "behavior", "behaviour", "thinking",
    "learning", "consciousness", "perception", "focus", "stress", "anxiety",
    "motivation", "willpower", "mindfulness", "self-control", "discipline",
    "decision", "bias", "mental",
]

PKM_SIGNALS = [
    "productivity", "system", "gtd", "getting things done", "workflow",
    "organize", "organise", "second brain", "zettelkasten", "obsidian",
    "note", "knowledge", "time management", "planning", "task", "work",
    "bullet", "journal", "process", "deep work", "output", "execution",
    "smart", "ultralearning", "learning system",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_whitelist() -> set[str]:
    with open(TOPICS_FILE) as f:
        data = json.load(f)
    return {t["name"] for t in data["topics"]}


def validate_token_map(valid_topics: set[str]) -> None:
    """Fail fast if TOKEN_MAP or disambiguation targets reference stale names."""
    all_destinations = set(TOKEN_MAP.values()) | {
        "ADHD & Cognitive Scaffolding",
        "PKM & Personal Operating System",
    }
    stale = all_destinations - valid_topics
    if stale:
        print("❌ TOKEN_MAP references names not in topics_whitelist.json:")
        for name in sorted(stale):
            print(f"   • {name!r}")
        print("   Update TOKEN_MAP or topics_whitelist.json to re-align them.")
        sys.exit(1)
    print(f"✅ TOKEN_MAP validated — all destinations exist in whitelist.")


def fetch_books() -> list[dict]:
    result = subprocess.run(
        ["calibredb", "list",
         "--fields", "id,title,*prodos_topic",
         "--for-machine", "--limit", "5000"],
        capture_output=True, text=True,
    )
    raw = result.stdout
    start = raw.index("[")
    end = raw.rindex("]") + 1
    return json.loads(raw[start:end])


def score_title(title: str) -> tuple[int, int]:
    """Return (adhd_score, pkm_score) based on keyword hits in title."""
    t = title.lower()
    adhd = sum(1 for kw in ADHD_SIGNALS if kw in t)
    pkm  = sum(1 for kw in PKM_SIGNALS  if kw in t)
    return adhd, pkm


def classify_ambiguous(title: str) -> list[str]:
    """
    Classify a book from ['Cognition', 'Productivity'] into new topic(s).
    Returns a list with one or both topics when the signal is split.
    """
    adhd, pkm = score_title(title)
    if adhd > pkm:
        return ["ADHD & Cognitive Scaffolding"]
    elif pkm > adhd:
        return ["PKM & Personal Operating System"]
    else:
        # Tied or no signal — assign both; human can prune later
        return ["ADHD & Cognitive Scaffolding", "PKM & Personal Operating System"]


def migrate_topics(old_topics: list[str], title: str) -> list[str]:
    """
    Given a book's current topic list and title, return the migrated list.
    Deduplicates and sorts for stable output.
    """
    old_set = set(old_topics)
    new_topics: set[str] = set()

    is_ambiguous = old_set == {"Cognition", "Productivity"}
    is_lone_productivity = old_set == {"Productivity"}
    is_lone_cognition    = old_set == {"Cognition"}

    if is_ambiguous:
        new_topics.update(classify_ambiguous(title))
    elif is_lone_productivity:
        adhd, pkm = score_title(title)
        new_topics.add("PKM & Personal Operating System" if pkm >= adhd
                       else "ADHD & Cognitive Scaffolding")
    elif is_lone_cognition:
        new_topics.add("ADHD & Cognitive Scaffolding")
    else:
        for token in old_topics:
            mapped = TOKEN_MAP.get(token)
            if mapped:
                new_topics.add(mapped)
            else:
                # Unknown token — keep and flag
                new_topics.add(f"⚠️ UNKNOWN: {token}")

    return sorted(new_topics)


def calibre_set(book_id: int, new_topics: list[str], dry_run: bool) -> None:
    """Write new topic values to Calibre via set_custom."""
    if not new_topics:
        return

    cmds = []
    # First call replaces all existing values
    cmds.append(["calibredb", "set_custom", "prodos_topic",
                 str(book_id), new_topics[0]])
    # Subsequent calls append
    for topic in new_topics[1:]:
        cmds.append(["calibredb", "set_custom", "--append", "prodos_topic",
                     str(book_id), topic])

    for cmd in cmds:
        if dry_run:
            print(f"    [DRY-RUN] {' '.join(cmd)}")
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    ⚠️  ERROR for id={book_id}: {result.stderr.strip()}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrate Calibre ProdOS Topic tags to new whitelist vocabulary."
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Write changes to Calibre (default is dry-run)."
    )
    args = parser.parse_args()
    dry_run = not args.apply

    valid_topics = load_whitelist()
    print(f"{'[DRY-RUN] ' if dry_run else ''}Loaded {len(valid_topics)} whitelist topics.")
    validate_token_map(valid_topics)
    print()

    books = fetch_books()
    tagged = [b for b in books if b.get("*prodos_topic")]
    print(f"Library: {len(books)} books total, {len(tagged)} with ProdOS Topic set.\n")

    # --- Build migration plan ---
    changes:   list[tuple[dict, list[str], list[str]]] = []
    no_change: list[dict] = []
    warnings:  list[tuple[dict, list[str]]] = []

    for book in tagged:
        old = book["*prodos_topic"]
        new = migrate_topics(old, book["title"])

        unknown = [t for t in new if t.startswith("⚠️")]
        if unknown:
            warnings.append((book, new))

        if set(old) == set(new):
            no_change.append(book)
        else:
            changes.append((book, old, new))

    # --- Print dry-run report ---
    print("=" * 70)
    print(f"CHANGES ({len(changes)} books)")
    print("=" * 70)

    ambiguous_flag: list[tuple[dict, list[str]]] = []

    for book, old, new in changes:
        title_short = book["title"][:55] + "…" if len(book["title"]) > 55 else book["title"]
        print(f"\n  [{book['id']:>4}] {title_short}")
        print(f"    BEFORE: {old}")
        print(f"    AFTER:  {new}")

        # Flag books that got two topics from disambiguation (needs human review)
        if (set(old) == {"Cognition", "Productivity"} and len(new) == 2):
            ambiguous_flag.append((book, new))
            print(f"    ⚠️  AMBIGUOUS — both topics assigned; review suggested.")

        calibre_set(book["id"], new, dry_run)

    print("\n" + "=" * 70)
    print(f"NO CHANGE ({len(no_change)} books — already using valid names)")
    print("=" * 70)
    for book in no_change:
        print(f"  [{book['id']:>4}] {book['title'][:60]} → {book['*prodos_topic']}")

    if warnings:
        print("\n" + "=" * 70)
        print(f"⚠️  UNMAPPED TOKENS ({len(warnings)} books — manual action required)")
        print("=" * 70)
        for book, new in warnings:
            print(f"  [{book['id']:>4}] {book['title'][:55]} → {new}")

    # --- Summary ---
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Books to update:      {len(changes)}")
    print(f"  Books unchanged:      {len(no_change)}")
    print(f"  Unmapped tokens:      {len(warnings)}")
    print(f"  Dual-topic (review):  {len(ambiguous_flag)}")
    print(f"  Untagged (Phase 4):   {len(books) - len(tagged)}")

    if dry_run:
        print("\n  ⚡ Dry-run complete. Re-run with --apply to write changes.")
    else:
        print("\n  ✅ Changes written to Calibre.")


if __name__ == "__main__":
    main()
