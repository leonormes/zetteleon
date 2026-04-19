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
        cmd = ["calibredb", "list", "--fields", "id,title,authors,tags", "--for-machine"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        match = re.search(r"\[.*\]", result.stdout, re.DOTALL)
        if not match:
            print("❌ No JSON found in Calibre output.")
            return []
            
        return json.loads(match.group(0))
    except Exception as e:
        print(f"❌ Failed to run calibredb: {e}")
        return []

def synthesize(whitelist, books):
    print("🧪 Cross-referencing Library with Topics...")
    synthesis = defaultdict(list)
    
    for topic_obj in whitelist:
        topic_name = topic_obj["name"]
        keywords = [k.lower() for k in topic_obj["keywords"]]
        
        for book in books:
            book_tags = [t.lower() for t in book.get('tags', [])]
            title = book.get('title', '').lower()
            
            # Match if ANY keyword for this topic is in the book's tags or title
            match_found = False
            for kw in keywords:
                if kw in book_tags or re.search(rf"\b{re.escape(kw)}\b", title):
                    match_found = True
                    break
            
            if match_found:
                synthesis[topic_name].append(book)

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
