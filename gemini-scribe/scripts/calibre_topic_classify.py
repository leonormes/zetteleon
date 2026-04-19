#!/usr/bin/env python3
"""
calibre_topic_classify.py

Classifies untagged Calibre books into ProdOS Topics using:
  Phase A — Fiction detection via Calibre genre tags
  Phase B — Non-fiction scoring via whitelist keyword matching
             against: Calibre tags + title + description

Usage:
  python3 calibre_topic_classify.py           # dry-run (default, safe)
  python3 calibre_topic_classify.py --apply   # write changes to Calibre
  python3 calibre_topic_classify.py --min-score 2  # raise confidence threshold
"""

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPTS_DIR = Path(__file__).parent
TOPICS_FILE = SCRIPTS_DIR / "topics_whitelist.json"

FICTION_TAGS = {
    "sci-fi", "science fiction", "fiction", "fantasy", "horror",
    "thriller", "mystery", "romance", "literary fiction", "novel",
    "short stories", "graphic novel", "dystopian", "cyberpunk",
    "historical fiction", "adventure", "young adult", "ya",
}

# Calibre genre tags → whitelist topic name (supplements keyword matching)
CALIBRE_TAG_MAP: dict[str, str] = {
    "software engineering":  "Data-Centric Software Engineering",
    "programming":           "Data-Centric Software Engineering",
    "computer science":      "Data-Centric Software Engineering",
    "data structures":       "Data-Centric Software Engineering",
    "sdlc":                  "Data-Centric Software Engineering",
    "rust":                  "Data-Centric Software Engineering",
    "cloud native":          "Platform Engineering & Containers",
    "kubernetes":            "Platform Engineering & Containers",
    "gitops":                "Platform Engineering & Containers",
    "containers":            "Platform Engineering & Containers",
    "docker":                "Platform Engineering & Containers",
    "observability":         "Platform Engineering & Containers",
    "networking & security": "Network Engineering",
    "networking":            "Network Engineering",
    "linux":                 "Network Engineering",
    "shell":                 "Network Engineering",
    "cli & tools":           "Network Engineering",
    "llm":                   "AI Engineering & LLM Systems",
    "ai":                    "AI Engineering & LLM Systems",
    "machine learning":      "AI Engineering & LLM Systems",
    "mindfulness":           "ADHD & Cognitive Scaffolding",
    "psychology":            "ADHD & Cognitive Scaffolding",
    "self help":             "ADHD & Cognitive Scaffolding",
    "self-help":             "ADHD & Cognitive Scaffolding",
    "neuroscience":          "ADHD & Cognitive Scaffolding",
    "philosophy":            "Philosophy, Meaning & Resilience",
    "spirituality":          "Philosophy, Meaning & Resilience",
    "religion":              "Philosophy, Meaning & Resilience",
    "finance":               "Philosophy, Meaning & Resilience",
    "mathematics":           "Applied Mathematics & Formal Logic",
    "logic":                 "Applied Mathematics & Formal Logic",
    "science":               "Applied Mathematics & Formal Logic",
    "physics":               "Applied Mathematics & Formal Logic",
    "health":                "Health & Endurance",
    "fitness":               "Health & Endurance",
    "music":                 "Philosophy, Meaning & Resilience",
    "creativity":            "Philosophy, Meaning & Resilience",
    "distributed":           "Data-Centric Software Engineering",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_whitelist() -> list[dict]:
    with open(TOPICS_FILE) as f:
        return json.load(f)["topics"]


def validate_tag_map(valid_topics: set[str]) -> None:
    stale = set(CALIBRE_TAG_MAP.values()) - valid_topics
    if stale:
        print("❌ CALIBRE_TAG_MAP references names not in topics_whitelist.json:")
        for name in sorted(stale):
            print(f"   • {name!r}")
        raise SystemExit(1)


def fetch_books() -> list[dict]:
    result = subprocess.run(
        ["calibredb", "list",
         "--fields", "id,title,authors,tags,comments,*prodos_topic",
         "--for-machine", "--limit", "5000"],
        capture_output=True, text=True,
    )
    raw = result.stdout
    return json.loads(raw[raw.index("["):raw.rindex("]") + 1])


def is_fiction(book: dict) -> bool:
    tags = {t.lower() for t in book.get("tags", [])}
    return bool(tags & FICTION_TAGS)


def score_book(book: dict, whitelist: list[dict]) -> tuple[str | None, int, str]:
    """
    Returns (topic_name, score, method) for the best matching whitelist topic.
    method is 'tag' (Calibre genre tag hit) or 'keyword' (title/description).
    Score 0 means unclassifiable.
    """
    calibre_tags = {t.lower() for t in book.get("tags", [])}
    title = book.get("title", "").lower()
    description = re.sub(r"<[^>]+>", " ", book.get("comments", "") or "").lower()
    text = f"{title} {description}"

    # Phase 1: Calibre genre tag → topic (authoritative, weight 3 each)
    tag_scores: dict[str, int] = defaultdict(int)
    for tag in calibre_tags:
        mapped = CALIBRE_TAG_MAP.get(tag)
        if mapped:
            tag_scores[mapped] += 3

    if tag_scores:
        best = max(tag_scores, key=lambda t: tag_scores[t])
        return best, tag_scores[best], "tag"

    # Phase 2: Whitelist keyword matching on title + description
    kw_scores: dict[str, int] = defaultdict(int)
    for topic in whitelist:
        for kw in topic["keywords"]:
            if re.search(rf"\b{re.escape(kw.lower())}\b", text):
                kw_scores[topic["name"]] += 1

    if kw_scores:
        best = max(kw_scores, key=lambda t: kw_scores[t])
        return best, kw_scores[best], "keyword"

    return None, 0, "none"


def calibre_set(book_id: int, topic: str, dry_run: bool) -> None:
    cmd = ["calibredb", "set_custom", "prodos_topic", str(book_id), topic]
    if dry_run:
        print(f"    [DRY-RUN] {' '.join(cmd)}")
    else:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    ⚠️  ERROR id={book_id}: {result.stderr.strip()}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Classify untagged Calibre books into ProdOS Topics."
    )
    parser.add_argument("--apply", action="store_true",
                        help="Write changes to Calibre (default is dry-run).")
    parser.add_argument("--min-score", type=int, default=1,
                        help="Minimum keyword score to accept a classification (default: 1).")
    args = parser.parse_args()
    dry_run = not args.apply

    whitelist = load_whitelist()
    valid_topics = {t["name"] for t in whitelist}
    validate_tag_map(valid_topics)
    print(f"{'[DRY-RUN] ' if dry_run else ''}Loaded {len(valid_topics)} whitelist topics.\n")

    books = fetch_books()
    untagged = [b for b in books if not b.get("*prodos_topic")]
    print(f"Library: {len(books)} books total, {len(untagged)} untagged.\n")

    fiction:        list[tuple[dict, str]]         = []
    classified:     list[tuple[dict, str, int, str]] = []
    unclassifiable: list[dict]                     = []

    for book in untagged:
        if is_fiction(book):
            fiction.append((book, "Fiction"))
        else:
            topic, score, method = score_book(book, whitelist)
            if topic and score >= args.min_score:
                classified.append((book, topic, score, method))
            else:
                unclassifiable.append(book)

    # --- Fiction ---
    print("=" * 70)
    print(f"FICTION ({len(fiction)} books) → will be tagged 'Fiction'")
    print("=" * 70)
    for book, _ in fiction:
        tags = [t for t in book.get("tags", []) if t.lower() in FICTION_TAGS]
        title_short = book["title"][:55] + "…" if len(book["title"]) > 55 else book["title"]
        print(f"  [{book['id']:>4}] {title_short}  (tags: {tags})")
        calibre_set(book["id"], "Fiction", dry_run)

    # --- Classified non-fiction ---
    print(f"\n{'=' * 70}")
    print(f"NON-FICTION CLASSIFIED ({len(classified)} books)")
    print("=" * 70)

    # Group by topic for readability
    by_topic: dict[str, list] = defaultdict(list)
    for book, topic, score, method in classified:
        by_topic[topic].append((book, score, method))

    for topic in sorted(by_topic):
        entries = by_topic[topic]
        print(f"\n  [{topic}]  ({len(entries)} books)")
        for book, score, method in sorted(entries, key=lambda x: -x[1]):
            title_short = book["title"][:52] + "…" if len(book["title"]) > 52 else book["title"]
            print(f"    [{book['id']:>4}] {title_short}  score={score} via={method}")
            calibre_set(book["id"], topic, dry_run)

    # --- Unclassifiable ---
    print(f"\n{'=' * 70}")
    print(f"UNCLASSIFIABLE ({len(unclassifiable)} books — no signal found, manual tagging needed)")
    print("=" * 70)
    for book in unclassifiable:
        tags = book.get("tags", [])
        title_short = book["title"][:55] + "…" if len(book["title"]) > 55 else book["title"]
        print(f"  [{book['id']:>4}] {title_short}  tags={tags}")

    # --- Summary ---
    total_actioned = len(fiction) + len(classified)
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print("=" * 70)
    print(f"  Fiction tagged:       {len(fiction)}")
    print(f"  Non-fiction tagged:   {len(classified)}")
    print(f"  Unclassifiable:       {len(unclassifiable)}")
    print(f"  Total to write:       {total_actioned}")

    if dry_run:
        print(f"\n  ⚡ Dry-run complete. Re-run with --apply to write changes.")
    else:
        print(f"\n  ✅ Changes written to Calibre.")


if __name__ == "__main__":
    main()
