import os
import shutil

source_dir = "/Volumes/DAL/Zettelkasten/LLMeon/Heptabase/Card Library"
dest_dir = "/Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_Projects"

files_to_move = [
    "A Personalised Educational Pathway for Bessie Ormes! A Comprehensive GCSE Support Plan.md",
    "Bessie Feedback Table.md",
    "Bessie Sees it Different.md",
    "Bessie’s Year 9 Subjects.md",
    "Meeting Transcript – Teachers – Wednesday at 09!16.md",
    "Summary of Discussion with Bessie ('Lessons' Transcript).md",
    "To assess how consistently Bessie's teachers are implementing her support, drawing on her Individ.md",
    "1.3 Eduqas GCSE Film Studies.md",
    "1.4 Edexcel GCSE History.md",
    "1.5 AQA GCSE Philosophy and Ethics (Religious Studies).md",
    "2.1 AQA GCSE English Language.md",
    "2.2 Edexcel GCSE English Literature.md",
    "2.3 Edexcel GCSE Mathematics.md",
    "2.4 AQA GCSE Combined Science.md",
    "Art.md",
    "Combined Science.md",
    "English Language.md",
    "English Literature.md",
    "Film Studies.md",
    "History.md",
    "Language of Maths.md",
    "Linking the Language of Maths.md",
    "Mathematics.md",
    "Maths and English Language.md",
    "Optional Subjects.md",
    "Other Compulsory Areas of Study!.md",
    "Philosophy and Ethics (within Religious Studies GCSE).md",
    "Photography.md",
    "Subjects.md",
    "Based on the Ofsted report, the UK government's implied expectations for SEN support, and the com.md"
]

metadata = """---
project_name: "Bessie"
type: note
---
"""

for fname in set(files_to_move):
    src = os.path.join(source_dir, fname)
    if not os.path.exists(src):
        print(f"Skipping {fname}, not found.")
        continue
    
    with open(src, "r") as f:
        content = f.read()
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            # Replace existing frontmatter if we want to enforce it, but let's just append
            if "project_name:" not in frontmatter:
                new_frontmatter = frontmatter.rstrip() + "\nproject_name: \"Bessie\"\ntype: note\n"
                new_content = "---" + new_frontmatter + "---" + parts[2]
            else:
                new_content = content
        else:
            new_content = metadata + content
    else:
        new_content = metadata + content
        
    dest = os.path.join(dest_dir, fname)
    with open(dest, "w") as f:
        f.write(new_content)
        
    os.remove(src)
    print(f"Moved and updated: {fname}")
