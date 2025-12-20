---
aliases: []
confidence: 
created: 2025-09-10T16:48:35Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tip_004_Execute_Command
type:
uid: 
updated: 
version:
---

## Tip 004: Use Execute to Handle Special Characters in Commands

### Problem

You need to use special key notations like `<CR>` in `:normal` commands, but they don't work because `:normal` doesn't recognize them as special characters.

### Solution

Use `:execute` to build commands from strings, allowing proper handling of special characters:

```vim
" This won't work
:normal /emacs<cr>ciwvim

" This works
:execute "normal! /emacs\<cr>ciwvim"
```

### How It Works

`:execute` treats the argument as a string and converts escape sequences:

- `\<cr>` becomes actual carriage return
- `\<esc>` becomes actual escape key
- All key notations work with backslash prefix

### Key Differences

| Context    | Special Characters            |
| ---------- | ----------------------------- |
| Mappings   | `<CR>`, `<ESC>` work directly |
| `:normal`  | Special chars are literal     |
| `:execute` | `\<CR>`, `\<ESC>` work        |

### Practical Examples

#### Search and Replace

```vim
" Search for 'emacs' and replace with 'vim'
:execute "normal! /emacs\<cr>ciwvim"
```

#### Complex Operator Pending Mapping

```vim
:onoremap nc :execute "normal! f{vi{"
```

#### String Concatenation

```vim
" Multiple arguments are concatenated with spaces
:execute 'echo "this" "is" "a" "str"."ing"'
" Output: "this is a string"

" Use dots to avoid spaces
:execute 'echo "no"."spaces"'
" Output: "nospaces"
```

### Alternative: CTRL+V Method

You can also use `CTRL+V` followed by the actual key:

```vim
:normal! /emacs^Mciwvim
```

But `:execute` is more readable and maintainable.

### Related Tips

- See [Tip 003](Tip_003_Operator_Pending.md) for operator pending mappings
- See [Tip 007](Tip_007_Custom_Functions.md) for using execute in functions

---

*Source: A Vim Guide For Experts*
