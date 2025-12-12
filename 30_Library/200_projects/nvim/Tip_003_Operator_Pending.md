---
aliases: []
confidence: 
created: 2025-09-10T16:48:19Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tip_003_Operator_Pending
type:
uid: 
updated: 
version:
---

## Tip 003: Create Custom Motions with Operator Pending Mode

### Problem

You want to create custom text objects or motions that work with all operators (d, c, y, etc.) but don't know how to make them universally compatible.

### Solution

Use `:onoremap` to create operator pending mappings that define new motions:

```vim
" Simple text object - inside curly brackets
:onoremap ic i{

" Advanced motion - next curly brackets on line
:onoremap nc :normal! f{vi{<cr>
```

### How It Works

When you type an operator (`d`, `c`, `y`), Vim enters **OPERATOR-PENDING** mode and waits for a motion. Your custom mappings become available as motions for any operator.

### Examples

#### Basic Text Object

```vim
:onoremap ic i{
" Usage: dic (delete inside curly brackets)
" Usage: cic (change inside curly brackets)
```

#### Advanced Motion

```vim
:onoremap nc :normal! f{vi{<cr>
" Usage: dnc (delete next curly brackets content)
" Works from anywhere on the line
```

#### Practical Example

```vim
" Motion for next parentheses
:onoremap np :normal! f(vi(<cr>

" Motion for current function (assuming function keyword)
:onoremap if :normal! ?^function<cr>f{vi{<cr>
```

### Key Concepts

- Custom motions always start from cursor position
- Use `:normal!` to execute normal mode commands
- End with visual selection to define the text object
- Works with **all** operators automatically

### Before and After

```javascript
// Cursor anywhere on this line
My super┃line {with curly brackets}

// After 'dnc' (delete next curly)
My super line {}
```

### Related Tips

- See [Tip 004](Tip_004_Execute_Command.md) for using `:execute` with `:normal`
- See [Tip 002](Tip_002_Mapping_Special_Arguments.md) for mapping arguments

---

*Source: A Vim Guide For Experts*
