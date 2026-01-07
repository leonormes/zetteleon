import os
import re

root_dir = "."

tag_map = {
    "topic/linux": "SoftwareEngineering/Linux",
    "architecture": "SoftwareEngineering/Architecture",
    "security": "SoftwareEngineering/Security",
    "topic/technology/containers": "SoftwareEngineering/Containers",
    "topic/technology/networking": "SoftwareEngineering/Networking",
    "topic/technology/kubernetes": "SoftwareEngineering/Kubernetes",
}

def transform_tag(tag):
    t = tag.strip().strip('"\'')
    if t in tag_map:
        return tag_map[t]
    if t.startswith("topic/technology/"):
        return t.replace("topic/technology/", "SoftwareEngineering/")
    return t

def update_tags_in_content(content):
    match_fm = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match_fm:
        return content, False

    frontmatter = match_fm.group(1)
    lines = frontmatter.split('\n')
    new_lines = []
    in_tags_block = False
    changes_made = False

    for line in lines:
        # Case 1: tags: [a, b, c]
        inline_match = re.match(r'^(tags:\s*)\[(.*?)\]', line)
        if inline_match:
            prefix = inline_match.group(1)
            tags_content = inline_match.group(2)
            if not tags_content.strip():
                new_lines.append(line)
                continue
                
            current_tags = [t.strip() for t in tags_content.split(',')]
            new_tags = []
            line_changed = False
            
            for t in current_tags:
                clean_t = t.strip('"\'')
                trans_t = transform_tag(clean_t)
                if trans_t != clean_t:
                    new_tags.append(f'"{trans_t}"') # Always quote new tags for safety
                    line_changed = True
                else:
                    new_tags.append(t) # Keep original formatting if no change
            
            if line_changed:
                new_lines.append(f"{prefix}[{', '.join(new_tags)}]")
                changes_made = True
            else:
                new_lines.append(line)
            in_tags_block = False
            continue

        # Case 2: tags: start of block
        if re.match(r'^tags:\s*$', line):
            in_tags_block = True
            new_lines.append(line)
            continue
        
        # Case 3: List item "- tag"
        if in_tags_block:
            list_match = re.match(r'^(\s*-\s+)(.*)', line)
            if list_match:
                prefix = list_match.group(1)
                tag_val = list_match.group(2)
                clean_t = tag_val.strip().strip('"\'')
                trans_t = transform_tag(clean_t)
                
                if trans_t != clean_t:
                    new_lines.append(f'{prefix}"{trans_t}"')
                    changes_made = True
                else:
                    new_lines.append(line)
                continue
            
            # Check if block ended (unindented line or new key)
            if re.match(r'^\S', line):
                in_tags_block = False
                new_lines.append(line)
                continue
            
            new_lines.append(line)
        else:
            new_lines.append(line)

    if changes_made:
        new_fm_str = '\n'.join(new_lines)
        new_content = content.replace(frontmatter, new_fm_str, 1)
        return new_content, True
    
    return content, False

def process_files():
    count = 0
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs: dirs.remove('.git')
        if '.obsidian' in dirs: dirs.remove('.obsidian')
        
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content, changed = update_tags_in_content(content)
                    
                    if changed:
                        print(f"Updating {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    process_files()