import json
import subprocess
import os
import re
from pathlib import Path
from collections import defaultdict

# --- CONFIGURATION ---
VAULT_PATH = "/Volumes/DAL/Zettelkasten/LLMeon"
SCRIPTS_DIR = os.path.join(VAULT_PATH, "gemini-scribe/scripts")
TOPICS_FILE = os.path.join(SCRIPTS_DIR, "topics_whitelist.json")
CALIBRE_LIBRARY_NAME = "DAL"
OUTPUT_FILENAME = "30_Library/400_indexes/Main Topics of Interest.md"

def load_whitelist():
    print(f"🔍 Loading High-Signal Topics from: {TOPICS_FILE}...")
    try:
        with open(TOPICS_FILE, "r") as f:
            return json.load(f)["topics"]
    except Exception as e:
        print(f"❌ Error loading whitelist: {e}")
        return []

def get_calibre_books():
    print("📚 Fetching Calibre Library Data...")
    try:
        cmd = ["calibredb", "list",
               "--fields", "id,title,authors,tags,*prodos_topic",
               "--for-machine", "--limit", "5000"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        raw = result.stdout
        start = raw.index("[")
        end = raw.rindex("]") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError) as e:
        print(f"❌ Failed to parse Calibre JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ Failed to run calibredb: {e}")
        return []

def synthesize(whitelist, books):
    print("🧪 Cross-referencing Library with Topics...")
    synthesis = defaultdict(list)
    valid_names = {t["name"] for t in whitelist}
    keyword_map = {t["name"]: [k.lower() for k in t["keywords"]] for t in whitelist}

    curated = 0
    fallback = 0

    for book in books:
        prodos_topics = book.get("*prodos_topic") or []

        if prodos_topics:
            # Primary path: trust the curated ProdOS Topic field directly
            # Skip fiction — not a knowledge domain
            if prodos_topics == ["Fiction"]:
                continue
            for topic_name in prodos_topics:
                if topic_name in valid_names:
                    synthesis[topic_name].append(book)
            curated += 1
        else:
            # Fallback: keyword match on title + tags for untagged books
            book_tags = [t.lower() for t in book.get("tags", [])]
            title = book.get("title", "").lower()
            for topic_name, keywords in keyword_map.items():
                for kw in keywords:
                    if kw in book_tags or re.search(rf"\b{re.escape(kw)}\b", title):
                        synthesis[topic_name].append(book)
                        break
            fallback += 1

    print(f"   ✅ Curated match: {curated} books  |  🔍 Keyword fallback: {fallback} books")
    return synthesis

def write_note(whitelist, synthesis):
    output_path = Path(VAULT_PATH) / OUTPUT_FILENAME
    print(f"📝 Writing Master Index to: {output_path}")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🗺️ Main Topics of Interest\n")
        f.write(f"*Last synthesized: {subprocess.check_output(['date']).decode().strip()}*\n\n")
        f.write("This is a curated index of your primary knowledge domains, automatically cross-referenced with your Calibre library.\n\n---\n\n")

        for topic_obj in whitelist:
            name = topic_obj["name"]
            desc = topic_obj["description"]
            related_books = synthesis[name]

            if not related_books:
                continue

            f.write(f"## {name.upper()}\n")
            f.write(f"> {desc}\n\n")
            f.write("### Related Library Resources\n")
            
            # Deduplicate books
            seen_ids = set()
            for book in related_books:
                if book['id'] in seen_ids: continue
                seen_ids.add(book['id'])
                
                authors_raw = book.get('authors', 'Unknown')
                authors = ", ".join(authors_raw) if isinstance(authors_raw, list) else str(authors_raw)
                url = f"calibre://show-book/{CALIBRE_LIBRARY_NAME}/{book['id']}"
                f.write(f"- [{book['title']}]({url}) — *{authors}*\n")
            f.write("\n")

def main():
    whitelist = load_whitelist()
    if not whitelist:
        return
        
    books = get_calibre_books()
    if not books:
        return
        
    graph = synthesize(whitelist, books)
    write_note(whitelist, graph)
    print("✨ Sync Complete!")

if __name__ == "__main__":
    main()
