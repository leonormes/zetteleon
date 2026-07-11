import os
import yaml
import re
import json
import difflib

vault_path = "/Volumes/DAL/Zettelkasten/LLMeon"
folders_to_scan = [
    "30_Library",
    "20_Thinking",
    "10_System",
    "01_journals",
    "00_Inbox"
]

report_path = os.path.join(vault_path, "output/reports/2026-07-11-frontmatter-migration-dryrun.md")
# Ensure directory exists
os.makedirs(os.path.dirname(report_path), exist_ok=True)

stats = {
    "scanned": 0,
    "migrated": 0,
    "exceptions": 0,
    "by_folder": {}
}

exceptions = []
diffs = []

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
    # Using safe_dump with specific params
    return yaml.safe_dump(d, default_flow_style=False, sort_keys=False, allow_unicode=True)

# Helper for merging
def merge_dicts(d1, d2):
    for k, v in d2.items():
        if isinstance(v, dict) and k in d1 and isinstance(d1[k], dict):
            merge_dicts(d1[k], v)
        elif k not in d1:
            d1[k] = v
    return d1

for root, _, files in os.walk(vault_path):
    rel_root = os.path.relpath(root, vault_path)
    if not any(rel_root.startswith(f) for f in folders_to_scan) and not any(f == rel_root for f in folders_to_scan):
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
        if body is None:
            exceptions.append(f"- `{rel_path}`: Failed to parse YAML frontmatter: {raw_fm}")
            stats["exceptions"] += 1
            continue
            
        if not isinstance(fm, dict):
            # empty frontmatter or not a dict
            if fm is None:
                fm = {}
            else:
                exceptions.append(f"- `{rel_path}`: Frontmatter is not a dictionary.")
                stats["exceptions"] += 1
                continue
                
        # Dry run migration
        original_fm = dict(fm)
        has_changes = False
        exception_raised = False
        
        # We will collect legacy keys to delete, but only if they are successfully mapped
        to_delete = []
        new_prodos = {}
        
        # folder mapping
        implied_kind = None
        if rel_path.startswith("30_Library/100_zettelkasten/"): implied_kind = "atomic"
        elif rel_path.startswith("30_Library/SoT/"):
            implied_kind = "protocol" if file.startswith("Protocol - ") else "sot"
        elif rel_path.startswith("01_journals/"): implied_kind = "journal"
        elif rel_path.startswith("30_Library/MoC/"): implied_kind = "moc"
        elif rel_path.startswith("30_Library/ops/"): implied_kind = "ops"
        elif rel_path.startswith("20_Thinking/21_Workbench/"): implied_kind = "head"
        elif rel_path.startswith("10_System/prompts/"): implied_kind = "prompt"
        elif rel_path.startswith("30_Library/200_projects/"): implied_kind = "project"
        
        # Legacy type mapping
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
            # Maybe add kind based on folder if type is missing? Prompt says "Folder is normative for prodos.kind".
            new_prodos['kind'] = implied_kind

        # Lifecycle
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
                
        # Dates
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
            
        # Apply changes if no exceptions
        if exception_raised:
            stats["exceptions"] += 1
            continue
            
        if new_prodos:
            if 'prodos' not in fm:
                fm['prodos'] = {}
            # Merge logic: never overwrite existing prodos values
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
            
            if len(diffs) < 10:
                old_yaml = "---\n" + raw_fm.strip() + "\n---\n"
                new_yaml = "---\n" + dict_to_yaml_str(fm).strip() + "\n---\n"
                diff = list(difflib.unified_diff(
                    old_yaml.splitlines(keepends=True),
                    new_yaml.splitlines(keepends=True),
                    fromfile=f"a/{rel_path}",
                    tofile=f"b/{rel_path}"
                ))
                diffs.append((rel_path, "".join(diff)))

# Write report
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# Frontmatter Migration Dry Run Report\n\n")
    f.write("## Stats\n")
    f.write(f"- Scanned: {stats['scanned']}\n")
    f.write(f"- Planned Migrations: {stats['migrated']}\n")
    f.write(f"- Exceptions: {stats['exceptions']}\n\n")
    
    f.write("## Per-folder Counts\n")
    for k, v in stats["by_folder"].items():
        f.write(f"- {k}: {v}\n")
        
    f.write("\n## Exceptions\n")
    if exceptions:
        for ex in exceptions:
            f.write(ex + "\n")
    else:
        f.write("None\n")
        
    f.write("\n## 10 Sample Diffs\n")
    for path, diff in diffs:
        f.write(f"### {path}\n```diff\n{diff}\n```\n\n")

print(f"Dry run complete. Found {stats['migrated']} migrations and {stats['exceptions']} exceptions.")
