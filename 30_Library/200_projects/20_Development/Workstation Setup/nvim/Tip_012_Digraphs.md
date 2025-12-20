---
aliases: []
confidence: 
created: 2025-09-10T16:49:13Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tip_012_Digraphs
type:
uid: 
updated: 
version:
---

## Tip 012: Insert Special Characters with Digraphs

### Problem

You need to insert special characters like arrows, copyright symbols, or mathematical notation but don't know how to type them efficiently.

### Solution

Use digraphs - two-character combinations that produce special characters:

```vim
" In Insert mode:
CTRL+K ->  " →
CTRL+K TM  " ™
CTRL+K Co  " ©
CTRL+K Eu  " €
```

### How It Works

Every digraph is represented by exactly two "normal" characters that combine to create one special character.

### Essential Digraphs

- `CTRL+K ->` → (arrow right)
- `CTRL+K TM` ™ (trademark)
- `CTRL+K Co` © (copyright)
- `CTRL+K Rg` ® (registered)
- `CTRL+K Eu` € (euro)
- `CTRL+K +-` ± (plus-minus)
- `CTRL+K OK` ✓ (checkmark)
- `CTRL+K XX` ✗ (cross mark)

### Mathematical Symbols

- `CTRL+K AN` ∧ (logical and)
- `CTRL+K OR` ∨ (logical or)
- `CTRL+K (-` ∈ (element of)

### Commands

```vim
:digraphs              " Show all available digraphs
:dig                   " Short form
:digraphs AB 8731      " Create custom digraph (AB = ∫)
```

### Alternative Method

If `digraph` option is set:

```vim
:set digraph
" Then type: <char1><BS><char2>
" Example: -<BS>> produces →
```

### Discovering Digraphs

Use `ga` in Normal mode on any character to see its digraph representation (if it has one).

### Real-World Example

When writing logic proofs or mathematical content:

```sh
p ∧ q → r ∨ s
" Typed as: p CTRL+K AN q CTRL+K -> r CTRL+K OR s
```

### Related Tips

- See [Tip 011](Tip_011_Insert_Mode_Keystrokes.md) for other Insert mode features
- See [Tip 021](Tip_021_Character_Classes.md) for character classes in regex

---

*Source: A Vim Guide for Adept Users*
