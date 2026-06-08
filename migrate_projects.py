import os
import shutil
import re

src_dir1 = "/Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_projects"
src_dir2 = "/Volumes/DAL/Zettelkasten/LLMeon/200_projects"
dest_dir = "/Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_Projects"

os.makedirs(dest_dir, exist_ok=True)

def update_frontmatter_and_move(filepath, category, status, project_name):
    if not filepath.endswith(".md"):
        return
        
    with open(filepath, 'r') as f:
        content = f.read()
        
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    
    new_yaml = {"type": "project"}
    if category: new_yaml["project_category"] = category
    if status: new_yaml["project_status"] = status
    if project_name: new_yaml["project_name"] = f'"{project_name}"'
        
    if yaml_match:
        yaml_content = yaml_match.group(1)
        for key, val in new_yaml.items():
            if not re.search(r'^' + key + r':', yaml_content, re.MULTILINE):
                yaml_content += f"\n{key}: {val}"
        new_content = f"---\n{yaml_content}\n---\n" + content[yaml_match.end():]
    else:
        yaml_content = "\n".join([f"{k}: {v}" for k,v in new_yaml.items()])
        new_content = f"---\n{yaml_content}\n---\n{content}"
        
    filename = os.path.basename(filepath)
    dest_path = os.path.join(dest_dir, filename)
    
    # Handle conflicts
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
            counter += 1
            
    with open(dest_path, 'w') as f:
        f.write(new_content)
    # Remove original file to clean up later
    os.remove(filepath)

def process_dir(src_dir):
    if not os.path.exists(src_dir): return
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if not file.endswith(".md"): continue
            filepath = os.path.join(root, file)
            
            rel_path = os.path.relpath(filepath, src_dir)
            parts = rel_path.split(os.sep)
            top_folder = parts[0]
            
            status = "archived"
            category = "general"
            project_name = None
            
            if top_folder == "00_Active_Projects":
                status = "active"
                if len(parts) > 2:
                    category = parts[1].lower().replace(" ", "_")
                    project_name = parts[1]
                else:
                    category = "active_projects"
            elif top_folder == "10_Infrastructure":
                category = "infrastructure"
                if len(parts) > 2: project_name = parts[1]
            elif top_folder == "20_Development":
                category = "development"
                if len(parts) > 2: project_name = parts[1]
            elif top_folder == "40_Personal":
                category = "personal"
            elif top_folder == "ProdOS":
                category = "prodos"
                
            update_frontmatter_and_move(filepath, category, status, project_name)

process_dir(src_dir1)
process_dir(src_dir2)

print("Migration completed.")
