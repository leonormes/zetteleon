import subprocess
import csv
import io
import sys

# Define mapping for consolidation
mapping = {
    # CLI & Tools
    'cli': 'CLI & Tools',
    'cli-text': 'CLI & Tools',
    'zsh': 'CLI & Tools',
    'vim': 'CLI & Tools',
    'linux': 'CLI & Tools',
    'workstation': 'CLI & Tools',
    
    # Cognition & Focus
    'adhd': 'Cognition & Focus',
    'mindful': 'Cognition & Focus',
    'thinking': 'Cognition & Focus',
    'brain': 'Cognition & Focus',
    'philosophy': 'Cognition & Focus',
    'logic': 'Cognition & Focus',
    'argumentation': 'Cognition & Focus',
    'ontology': 'Cognition & Focus',
    
    # Productivity & PKM
    'gtd': 'Productivity & PKM',
    'PKM': 'Productivity & PKM',
    'reading': 'Productivity & PKM',
    'writing': 'Productivity & PKM',
    'learning': 'Productivity & PKM',
    'team': 'Productivity & PKM',
    
    # Health & Performance
    'diet': 'Health & Performance',
    'fitness': 'Health & Performance',
    'running': 'Health & Performance',
    'health': 'Health & Performance',
    'bio': 'Health & Performance',
    
    # Computer Science
    'algorithms': 'Computer Science',
    'data structures': 'Computer Science',
    'Mathematics': 'Computer Science',
    'Statistics': 'Computer Science',
    'science': 'Computer Science',
    'data': 'Computer Science',
    'systems': 'Computer Science',
    
    # Cloud Native
    'kubernetes': 'Cloud Native',
    'docker': 'Cloud Native',
    'gitops': 'Cloud Native',
    'IaC': 'Cloud Native',
    'DevOps': 'Cloud Native',
    'observability': 'Cloud Native',
    
    # Networking & Security
    'networking': 'Networking & Security',
    'dns': 'Networking & Security',
    'tls': 'Networking & Security',
    'pki': 'Networking & Security',
    'ztn': 'Networking & Security',
    'IAM': 'Networking & Security',
    'security': 'Networking & Security',
    'cryptography': 'Networking & Security',
    
    # Software Engineering
    'TDD': 'Software Engineering',
    'Testing': 'Software Engineering',
    'Refactoring': 'Software Engineering',
    'sdlc': 'Software Engineering',
    'agile': 'Software Engineering',
    'ddd': 'Software Engineering',
    'performance': 'Software Engineering',
    
    # Programming
    'Programming': 'Programming',
    'rust': 'Programming',
    'go': 'Programming',
    'python': 'Programming',
    'javascript': 'Programming',
    
    # Misc Fixes
    'distibuted': 'distributed',
}

def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout

def main():
    print("Fetching books and tags...")
    books_json = run_command('calibredb list --fields id,tags --for-machine')
    
    if not books_json:
        print("Failed to fetch books.")
        return

    import json
    try:
        # Strip trailing non-JSON content
        if ']' in books_json:
            books_json = books_json[:books_json.rfind(']')+1]
        books = json.loads(books_json)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return
    
    count = 0
    for book in books:
        book_id = book['id']
        current_tags = book.get('tags', [])
        
        new_tags = set()
        changed = False
        
        for tag in current_tags:
            # Rule 1: Remove 'calibre' tag
            if tag.lower() == 'calibre':
                changed = True
                continue
                
            # Rule 2: Map tags if they exist in our mapping
            if tag in mapping:
                new_tags.add(mapping[tag])
                changed = True
            else:
                new_tags.add(tag)
        
        if changed:
            tags_to_set = ",".join(sorted(list(new_tags)))
            print(f"[{book_id}] Updating tags: {current_tags} -> {tags_to_set}")
            # Use printf to avoid shell escape issues with special characters in tags
            cmd = f'calibredb set_metadata {book_id} --field "tags:{tags_to_set}"'
            run_command(cmd)
            count += 1

    print(f"\nDone! Updated {count} books.")

if __name__ == "__main__":
    main()
