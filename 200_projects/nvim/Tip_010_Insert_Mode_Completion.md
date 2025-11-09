---
aliases: []
confidence: 
created: 2025-09-10T16:48:57Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tip_010_Insert_Mode_Completion
type:
uid: 
updated: 
version:
---

## Tip 010: Master Insert Mode Completion

### Problem

You need to complete text, scroll through buffers, or access various completion sources without leaving Insert mode.

### Solution

Use `CTRL+x` followed by specific keys for different completion types:

```vim
" In Insert mode:
CTRL+x CTRL+l  " Complete whole line
CTRL+x CTRL+f  " Complete filepath
CTRL+x s       " Spelling suggestions
CTRL+x CTRL+v  " Command history
CTRL+x CTRL+i  " Keywords from current/included files
```

### Completion Types

#### Navigation

- `CTRL+x CTRL+y` - Scroll up without leaving Insert mode
- `CTRL+x CTRL+e` - Scroll down without leaving Insert mode

#### Text Completion

- `CTRL+x CTRL+l` - Complete entire line from any buffer
- `CTRL+x CTRL+f` - Complete filepath (expands environment variables)
- `CTRL+x s` - Complete with spelling suggestions
- `CTRL+x CTRL+v` - Complete from command line history
- `CTRL+x CTRL+i` - Complete keywords from current and included files

### Requirements

Vim must be compiled with `+insert_expand` feature for these to work.

### Example Usage

```vim
" Type partial path and complete
/home/user/Doc<CTRL+x CTRL+f>
" Expands to: /home/user/Documents/

" Type beginning of line that exists elsewhere
function my<CTRL+x CTRL+l>
" Completes entire matching line
```

### Advanced Features

- **Thesaurus completion** - Set up with dictionary files
- **Omni-completion** - Language-specific intelligent completion
- **Path completion** - Uses `path` option for included files

### Related Tips

- See [Tip 011](Tip_011_Insert_Mode_Keystrokes.md) for other Insert mode shortcuts
- See [Tip 017](Tip_017_Abbreviations.md) for text expansion

---

*Source: A Vim Guide For Veteran Users*
