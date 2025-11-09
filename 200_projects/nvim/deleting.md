---
aliases: []
confidence: 
created: 2025-07-03T10:35:34Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: deleting
type:
uid: 
updated: 
version:
---

The behaviour you are encountering is a core aspect of Vim's modal editing philosophy, particularly how it manages 'registers'. When you delete or change text using commands like `d` (delete) or `c` (change), Vim, by default, 'cuts' this text into an internal clipboard-like storage area called the 'unnamed register'. This is usually convenient, as it means deletion inherently makes the text available for pasting. However, as you've observed, if you first yank (copy) something, then delete text to make space for your paste, the act of deletion will overwrite the unnamed register with the newly deleted text, causing your subsequent paste command to insert the deleted content instead of your originally yanked content.

Vim offers several mechanisms to manage this, from explicit register usage to a 'black hole' register for deletions you don't wish to save, and even plugins for more advanced clipboard history management.

## Understanding Vim's Registers: The Core of Copy-Pasting

Vim's copy and paste experience is built around 'registers', which are essentially containers that hold text. Unlike a single system-wide clipboard, Vim provides multiple registers, allowing for various pieces of text to be stored simultaneously.

### 1. The Unnamed Register (`""`)

This is the default register, addressed by `""`, which Vim uses if you don't specify another one. Commands like `x` (delete character), `s` (substitute character), `d{motion}` (delete motion), `c{motion}` (change motion), and `y{motion}` (yank motion) all set the contents of this register by default. When you paste using `p` or `P` in Normal mode, it typically pulls from this unnamed register. The problem you describe occurs precisely because `d{motion}` overwrites this default register.

### 2. The Yank Register (`"0`)

When you use the `y{motion}` command (for yanking/copying text), the specified text is copied not only into the unnamed register but also into the yank register, which is addressed by the `0` (zero) symbol. This is crucial for your workflow.

#### 3. Numbered Registers (`"1` through `"9`)

These registers automatically store the text you most recently changed or deleted. When a new deletion or change occurs, the content of `"1` moves to `"2`, `"2` to `"3`, and so on, with `"9` being dropped. This means your deleted lines are indeed kept, even if they aren't in the unnamed register.

#### 4. Named Registers (`"a` through `"z`)

You can explicitly copy or delete text into any of these 26 named registers. This provides dedicated storage that won't be overwritten by subsequent default `d` or `c` operations.

#### 5. System Clipboard Registers (`"` and `"+`)

These registers are used to interact with your operating system's clipboard. LazyVim's default configuration syncs the ``and`+` registers with the unnamed register, meaning any text you cut, copy, or paste in Vim will also be available to other applications, and vice-versa. While convenient, this also means that deleting text in Vim can overwrite your system clipboard.

### Solutions to Prevent Accidental Overwriting

Here are the primary ways to address your workflow, ensuring your yanked text is preserved:

#### Solution 1: Use the "Black Hole" Register for Deletions (`"_`)

When you delete text and explicitly *do not* want it to be stored in any register (including the unnamed or system clipboards), you can direct it to the "black hole" register, addressed by `_` (underscore).

How to use it:

Prefix your delete or change command with `"_`.

- To delete a word without it going into any register: `"_dw`.
- To delete a line without it going into any register: `"_dd`.
- To change (delete and enter insert mode) a word without the deleted text being saved: `"_cw` (Note: `cw` implies change, so `_c` would send to black hole).

Example of your workflow with the black hole register:

1. Yank the desired text: `yiw` (yank inner word) or `yy` (yank line). This text goes to the unnamed register and the yank register (`"0`).
2. Move to the target location.
3. Delete the existing text, sending it to the black hole: `"_diw` (delete inner word to black hole) or `"_dd` (delete line to black hole).
4. Paste the originally yanked text: `p` (Normal mode paste from unnamed register). Since the black hole deletion didn't overwrite the unnamed register, your originally yanked text is still there.

This method directly solves your problem by preventing unwanted deletions from entering and clobbering your primary paste buffer.

#### Solution 2: Explicitly Paste from the Yank Register (`"0`)

Even if you forget to use the black hole register and your deletion *does* overwrite the unnamed register, you can still access your previously yanked text because the `y{motion}` command also copies to the yank register (`"0`).

How to use it:

Prefix your paste command with `"0`.

- To paste from the yank register: `"0p` or `"0P`.

Example of your workflow with the yank register:

1. Yank the desired text: `yy` (yank line). This text goes to `""` and `"0`.
2. Move to the target location.
3. Delete the existing text: `dd` (delete line). This text now overwrites the `""` register.
4. Paste the originally yanked text: `"0p`. This explicitly tells Vim to paste from register `0`, bypassing the clobbered unnamed register.

This approach ensures that even if you don't explicitly avoid saving deletions, your most recent *yank* is always accessible.

#### Solution 3: Use Named Registers for Multi-Item Clipboards (`"a` to `"z`)

For more complex scenarios where you need to manage several distinct pieces of text, you can explicitly yank into and paste from named registers.

How to use it:

- Yank to a specific register: `"ayy` (yank current line to register `a`).
- Delete to a specific register: `"bdd` (delete current line to register `b`).
- Paste from a specific register: `"ap` (paste from register `a`).

This is particularly useful when you're refactoring code and need to paste different pieces of text at multiple locations, as it prevents registers from being accidentally overwritten.

### Retaining Deleted Lines for Later Use

Your requirement is to "still have the things I delete in vim available." The numbered registers (`"1` through `"9`) fulfil this automatically. Even if you use the black hole register for a current deletion, previous deletions will still be available in these numbered registers.

To access them:

- You can view the contents of all registers by typing `:registers` or `:reg` in Command-Line mode. This will display the contents of `""`, `"0`, `"1` through `"9`, named registers, and special registers.
- Once you know which numbered register contains the deleted text you want, you can paste it using, for example, `"1p`.

### Enhancing Clipboard Management with Plugins

For a more streamlined and intuitive experience, especially with clipboard history, consider using a plugin like `yanky.nvim`. LazyVim includes `yanky.nvim` and configures it with useful keybindings.

Key features of `yanky.nvim` related to your problem:

- Better clipboard history management: It provides an improved way to navigate and paste from your clipboard history beyond just the numbered registers.
- Dedicated paste keybinding: LazyVim typically maps `<Space>p` to bring up a picker dialog for your paste history. This allows you to visually select and paste any past yanked or deleted item without needing to remember its specific register number.
- Cycle through history: After a `put` (paste) operation, you can use `[y` to replace the just-pasted text with the previous item in your history, and `]y` to cycle forward. This is incredibly useful for finding the exact item you want to paste without having to re-yank or manually inspect registers.

Using such a plugin can significantly reduce the cognitive load of managing Vim's extensive register system, making your "copy, delete, then paste original copy" workflow much smoother and more reliable.
