---
aliases: []
confidence: 
created: 2025-10-24T10:01:37Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:23Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Hookmark + Obsidian on macOS_ Integration Report
type:
uid: 
updated: 
version:
---

This markdown guide is designed to give your local LLM full context for **setting up and using Hookmark with Obsidian on macOS**, including integration schemes, benefits, restrictions, setup steps, and actionable command-line instructions.

***

## Overview

- **Hookmark**: A macOS tool for linking notes, emails, files, web pages, and more, across your workflows.
- **Obsidian**: A local markdown-based knowledge base. Integrates deeply with Hookmark, offering linked data objects for powerful PKM workflows.

***

## Setup: Enabling Obsidian Integration

1. **Enable URI Callbacks in Obsidian:**
    - Launch Obsidian.
    - Go to **Settings → Files and Links → Advanced**.
    - Enable `Allow URI callbacks`.

***

## Integration Schemes: Comparison Table

| Feature | Default (`obsidian://`) | Advanced URI (`obsidian://advanced-uri`) | Hook File (`hook://file/`) |
| :-- | :-- | :-- | :-- |
| No extra plugins needed | ✅ | ❌ | ✅ |
| No extra Hookmark config needed | ✅ | ❌ | ❌ |
| Supports `Hook to New > Obsidian` | ✅ | ✅ | ✅ |
| Supports `Reveal File in Finder` | ❌ | ❌ | ✅ |
| Opens directly in Obsidian | ✅ | ✅ | ❌ (opens in Finder/default app) |
| Can move file within same vault | ❌ | ✅ | ✅ |
| Can move file across vaults/Mac | ❌ | ❌ | ✅ |
| Links survive switching note app | ❌ | ❌ | ✅ |
| No info added to note body | ✅ | ❌ (adds UID to frontmatter) | ✅ |

***

## Scheme Details \& Setup Actions

### 1. **Default Integration (`obsidian://`)**

- *How*: Out-of-the-box after enabling Obsidian URI callbacks.
- *Usage*: Hookmark’s `Copy Link`, `Copy Markdown Link`, and hooks reference notes.
- *Benefits*: Simple, cross-device compatibility (if files synced).
- *Limitations*:
  - Can't use `Reveal File in Finder` from Hookmark.
  - Renaming/moving notes may break links.
  - Links don't work if switching to a different notes app.

***

### 2. **Advanced URI Integration (`obsidian://advanced-uri`)**

- *Requires*: [Obsidian Advanced URI plugin](https://github.com/Vinzent03/obsidian-advanced-uri)
- *Setup Steps*:

1. **Install plugin inside Obsidian** (Community Plugins).
2. **Enable `Use UID instead of file paths`** in plugin settings.
3. **Optionally**: Set UID field name in frontmatter.
4. **Configure Hookmark** in Terminal:

```bash
defaults write com.cogsciapps.hook integration.obsidian.URL.scheme obsidian-advanced-URI
```

- *Benefits*: Robust links survive moving notes inside the same vault.
- *Limitations*: Extra metadata in notes, plugin dependency.

***

### 3. **Hook File Integration (`hook://file/`)**

- *Setup*: Set via Terminal:

```bash
defaults write com.cogsciapps.hook integration.obsidian.URL.scheme hook-file
```

- *Benefits*:
  - Robust file tracking across vaults and even if switching apps.
  - `Reveal File in Finder` works from Hookmark.
- *Limitations*: Links open in Finder or default app, not directly in Obsidian.

***

## Switching Schemes

Change integration via Terminal:

```bash
# Default
defaults write com.cogsciapps.hook integration.obsidian.URL.scheme obsidian-default

# Advanced URI plugin
defaults write com.cogsciapps.hook integration.obsidian.URL.scheme obsidian-advanced-URI

# Hook File
defaults write com.cogsciapps.hook integration.obsidian.URL.scheme hook-file
```

*Note*: Links created under old schemes remain valid, but Hookmark will show connections only for links created under the current active scheme.

***

## Practical Examples

- **Linking a note to an email or web page**:
  - Open note in Obsidian.
  - Use Hookmark menu bar > "Hook to Copied Link" or "Copy Markdown Link."
  - Paste link elsewhere to create a bi-directional link.
- **Creating new note and linking from anywhere**:
  - Use Hookmark’s “Hook to New > Obsidian” menu command.
- **Reveal a note in Finder** (only with `hook://file/` scheme):
  - Use "Reveal File in Finder" from Hookmark menu.

***

## Recommendations for ADHD/PKM Context

- **Default scheme** is simplest for starting out.
- **Advanced URI** preferred if notes are reorganized often within a vault.
- **Hook File** is most robust for file tracking and app-agnostic workflows.

For LLM context-driven automation, expose the above **setup instructions, scheme options, and actionable commands** so the agent can recommend or execute the proper command chains programmatically.

***

## Additional Resources

- [Hookmark Forum: Obsidian Integration Discussions](https://discourse.hookproductivity.com/)
- [Advanced URI Plugin Docs](https://github.com/Vinzent03/obsidian-advanced-uri)
- [Hookmark Help: Using Hookmark with Obsidian](https://hookproductivity.com/help/integration/using-hook-with-obsidian/)

***

**Ready for direct agent-driven setup and workflow assistance.**

---

## Hookmark Configuration \& Data File Locations (macOS)

**To edit Hookmark’s config directly, use these filesystem paths:**

***

### Core Config and Data Files

- **Bookmarks, links, and internal database:**
  - `~/Library/Application Support/com.cogsciapps.hook`
- **Preferences (plist file):**
  - `~/Library/Preferences/com.cogsciapps.hook.plist`

***

### User Files Folder (Customizable)

- **Hookmark Files (created via Make Hookmark File command):**
  - `~/Documents/Hook/Hook Files`
- **Templates and Notes (created via Hook to New):**
  - `~/Documents/Hook`
  - Includes subfolders like `/Templates` and `/Notes`, location is user-configurable in preferences.[^2_1][^2_2]

***

### Advanced Settings

- **Log Files and Debug:**
  - `~/Library/Logs/com.cogsciapps.hook`
- **Command-line only settings** (such as integration schemes) are set with `defaults write` for the domain `com.cogsciapps.hook`.

***

### Editing Instructions

1. **Close Hookmark before editing config files.**
2. Edit plist files with Xcode, `defaults write`, or any plist editor.
3. Adjust templates, notes, or .hookmark files directly in the user files folder.

***

### Backup/Restore

- Always back up `~/Library/Application Support/com.cogsciapps.hook` and `~/Documents/Hook` to retain links and custom templates.

***

**Use the above paths and procedures for direct config, automation, or agent integration.**

[^2_1]: <https://hookproductivity.com/help/preferences/general/>

[^2_2]: <https://hookproductivity.com/help/more/how-to-backup-and-restore-hook-data/>
