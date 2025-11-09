---
aliases: []
confidence: 
created: 2025-09-10T16:47:46Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tip_001_Verbose_Commands
type:
uid: 
updated: 
version:
---

## Tip 001: Use Verbose Commands to Debug Configuration

### Problem

You have a complex Vim configuration with many plugins and custom settings, but you can't remember where specific options, mappings, or commands were defined.

### Solution

Use the `:verbose` command to trace the source of any configuration:

```vim
:verbose set undodir?
:verbose map <leader>f
:verbose command MyCommand
```

### How It Works

The `:verbose` command shows exactly where configuration was last set:

- **File path** where the setting was defined
- **Line number** in that file
- Works for abbreviations, options, mappings, and user commands

### Example

```vim
:verbose set undodir?
" Output: Last set from ~/.config/nvim/init.vim line 354
```

### Why This Matters

- Debugging becomes much easier with complex configurations
- Helps identify conflicting settings from different plugins
- Essential when your configuration grows beyond a simple vimrc

### Related Tips

- See [Tip 024](Tip_024_Saving_Options.md) for saving current configuration
- See [Tip 008](Tip_008_User_Commands.md) for creating custom commands

### Keystrokes

- `:verbose set <option>?` - Show where option was set
- `:verbose map <mapping>` - Show where mapping was defined
- `:verbose command <cmd>` - Show where command was created

---

*Source: A Vim Guide For Experts*
