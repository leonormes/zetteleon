---
aliases: []
confidence: 
created: 2025-09-10T16:48:02Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tip_002_Mapping_Special_Arguments
type:
uid: 
updated: 
version:
---

## Tip 002: Master Special Arguments for Mappings

### Problem

Your mappings clutter the command line, conflict with existing ones, or don't work as expected in different contexts.

### Solution

Use special arguments to control mapping behavior:

```vim
" Silent mapping - no command line output
:nnoremap <silent> <leader><f6> :source $MYVIMRC<CR>

" Buffer-local mapping
:nnoremap <buffer> <leader>t :echo "Buffer specific"<CR>

" Expression mapping
:iab <expr> cdate strftime('%Y-%m-%d')

" Unique mapping - fails if already exists
:nnoremap <unique> <leader>x :echo "Safe mapping"<CR>

" Command mapping - stay in current mode
:inoremap <c-d> <Cmd>delete<cr>
```

### Special Arguments

- `<silent>` - No command line output when mapping is used
- `<buffer>` - Mapping only applies to current buffer (overrides global)
- `<expr>` - Execute Vimscript expression instead of literal command
- `<unique>` - Fail if mapping already exists (prevents conflicts)
- `<Cmd>` - Execute command without leaving current mode

### Key Points

- Special arguments must come **first** in the mapping command
- `<Cmd>` is the exception - it goes just before the command
- Use `:silent` command to also suppress command output: `:nnoremap <leader><f6> :silent :source $MYVIMRC<CR>`

### Example Use Cases

```vim
" Silent reload without command line noise
:nnoremap <silent> <leader>r :source $MYVIMRC<CR>

" Buffer-specific mappings for different file types
:autocmd FileType python nnoremap <buffer> <leader>r :!python %<CR>

" Dynamic content with expressions
:iab <expr> timestamp strftime('%Y-%m-%d %H:%M:%S')
```

### Related Tips

- See [Tip 003](Tip_003_Operator_Pending.md) for operator pending mappings
- See [Tip 005](Tip_005_Autocommands.md) for file-type specific mappings

---

*Source: A Vim Guide For Experts*
