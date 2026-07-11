import sys
import os
import yaml

vault_path = "/Volumes/DAL/Zettelkasten/LLMeon"

# Folders for this batch are passed as arguments
folders_to_scan = sys.argv[1:]

stats = {
    "scanned": 0,
    "migrated": 0,
    "exceptions": 0,
    "by_folder": {}
}

exceptions = []

def parse_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                return fm, parts[1], parts[2]
            except Exception as e:
                return None, str(e), None
    return None, "No YAML frontmatter", None

def dict_to_yaml_str(d):
    return yaml.safe_dump(d, default_flow_style=False, sort_keys=False, allow_unicode=True)

for root, _, files in os.walk(vault_path):
    rel_root = os.path.relpath(root, vault_path)
    
    # Check if the current dir is under any of the target folders
    match = False
    for f in folders_to_scan:
        f = f.strip('/')
        if rel_root.startswith(f) or f == rel_root:
            match = True
            break
            
    if not match:
        continue
    
    for file in files:
        if not file.endswith(".md"):
            continue
            
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, vault_path)
        folder_prefix = rel_path.split('/')[0] if '/' in rel_path else "root"
        
        stats["scanned"] += 1
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        fm, raw_fm, body = parse_frontmatter(content)
        if body is None or not isinstance(fm, dict):
            exceptions.append(f"- `{rel_path}`: Failed to parse YAML frontmatter or not dict.")
            stats["exceptions"] += 1
            continue
            
        original_fm = dict(fm)
        has_changes = False
        exception_raised = False
        to_delete = []
        new_prodos = {}
        
        implied_kind = None
        if rel_path.startswith("30_Library/100_zettelkasten/"): implied_kind = "atomic"
        elif rel_path.startswith("30_Library/SoT/"):
            implied_kind = "protocol" if file.startswith("Protocol - ") else "sot"
        elif rel_path.startswith("01_journals/"): implied_kind = "journal"
        elif rel_path.startswith("30_Library/MoC/"): implied_kind = "moc"
        elif rel_path.startswith("30_Library/ops/"): implied_kind = "ops"
        elif rel_path.startswith("20_Thinking/21_Workbench/"): implied_kind = "head"
        elif rel_path.startswith("10_System/prompts/"): implied_kind = "prompt"
        elif rel_path.startswith("30_Library/200_Projects/"): implied_kind = "project"
        
        if 'type' in fm:
            l_type = str(fm['type']).strip() if fm['type'] is not None else 'null'
            if l_type == '': l_type = 'null'
            
            if l_type in ['concept', 'atom', 'permanent', 'note', 'null', 'None']:
                if rel_path.startswith("30_Library/100_zettelkasten/"):
                    new_prodos['kind'] = 'atomic'
                    tags = fm.get('tags', [])
                    if isinstance(tags, str): tags = [tags]
                    form = 'concept'
                    if tags:
                        for tag in tags:
                            tag_str = str(tag).lower()
                            if 'hypothesis' in tag_str: form = 'hypothesis'
                            elif 'claim' in tag_str: form = 'claim'
                            elif 'definition' in tag_str: form = 'definition'
                    new_prodos.setdefault('atomic', {})['form'] = form
                    to_delete.append('type')
                else:
                    exceptions.append(f"- `{rel_path}`: Legacy type '{l_type}' found but not in 100_zettelkasten.")
                    exception_raised = True
            elif l_type == 'SoT':
                new_prodos['kind'] = 'protocol' if file.startswith('Protocol - ') else 'sot'
                to_delete.append('type')
            elif l_type == 'daily':
                new_prodos['kind'] = 'journal'
                to_delete.append('type')
            elif l_type == 'map':
                new_prodos['kind'] = 'moc'
                to_delete.append('type')
            elif l_type in ['command', 'atomic_command', 'playbook']:
                new_prodos['kind'] = 'ops'
                to_delete.append('type')
            else:
                exceptions.append(f"- `{rel_path}`: Unhandled legacy type '{l_type}'.")
                exception_raised = True
        elif implied_kind:
            new_prodos['kind'] = implied_kind

        if 'status' in fm:
            l_status = str(fm['status']).strip()
            if l_status in ['seedling', 'active', 'stable', 'evergreen', 'archived']:
                new_prodos['lifecycle'] = l_status
                to_delete.append('status')
            elif l_status == 'draft':
                new_prodos['lifecycle'] = 'seedling'
                to_delete.append('status')
            else:
                exceptions.append(f"- `{rel_path}`: Unhandled legacy status '{l_status}'.")
                exception_raised = True
                
        if 'trust-level' in fm:
            new_prodos['trust'] = str(fm['trust-level']).strip()
            to_delete.append('trust-level')
            
        if 'last_reviewed' in fm:
            new_prodos.setdefault('review', {})['last_reviewed'] = fm['last_reviewed']
            to_delete.append('last_reviewed')
            
        if 'review_interval' in fm:
            new_prodos.setdefault('review', {})['interval'] = fm['review_interval']
            to_delete.append('review_interval')
            
        if 'last_synthesis' in fm:
            new_prodos.setdefault('chronos', {})['last_synthesis'] = fm['last_synthesis']
            to_delete.append('last_synthesis')
            
        if 'synthesis-count' in fm:
            new_prodos.setdefault('chronos', {})['synthesis_count'] = fm['synthesis-count']
            to_delete.append('synthesis-count')
            
        for id_key in ['id', 'ID', 'uid']:
            if id_key in fm:
                new_prodos['id'] = fm[id_key]
                to_delete.append(id_key)
                
        created_missing = 'created' not in fm
        modified_missing = 'modified' not in fm
        
        if 'creation_date' in fm:
            if created_missing:
                fm['created'] = fm['creation_date']
                has_changes = True
            to_delete.append('creation_date')
            
        if 'updated' in fm:
            if modified_missing:
                fm['modified'] = fm['updated']
                has_changes = True
            to_delete.append('updated')
            
        if exception_raised:
            stats["exceptions"] += 1
            continue
            
        if new_prodos:
            if 'prodos' not in fm:
                fm['prodos'] = {}
            for k, v in new_prodos.items():
                if k not in fm['prodos']:
                    fm['prodos'][k] = v
                elif isinstance(v, dict) and isinstance(fm['prodos'][k], dict):
                    for subk, subv in v.items():
                        if subk not in fm['prodos'][k]:
                            fm['prodos'][k][subk] = subv
            has_changes = True
            
        for k in to_delete:
            if k in fm:
                del fm[k]
                has_changes = True
                
        if has_changes:
            stats["migrated"] += 1
            stats["by_folder"][folder_prefix] = stats["by_folder"].get(folder_prefix, 0) + 1
            new_yaml = "---\n" + dict_to_yaml_str(fm).strip() + "\n---\n"
            new_content = new_yaml + body
            with open(file_path, 'w', encoding='utf-8') as fw:
                fw.write(new_content)

print(f"Migrated: {stats['migrated']} | Exceptions: {stats['exceptions']}")
for ex in exceptions:
    print(ex)
