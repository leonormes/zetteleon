---
aliases: []
confidence: 
created: 2025-10-26T10:29:48Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Migrating Obsidian Workflows to Neovim + Marksman
type:
uid: 
updated: 
version:
---

Here's a focused, ADHD-optimized overview of building a powerful, distraction-free Markdown notes system by leveraging Neovim and the Marksman LSP—maximizing keyboard workflow, atomic operations, and automation.

## 🔑 Marksman LSP: Headline Features in Neovim

- **Symbol navigation:** Jump quickly to headings, links, and sections.
- **Cross-file wiki-link support:** Use `[[note]]` and `[[note#heading]]` for atomic, Zettelkasten-style linking.
- **Completion for links \& headings:** Type `[` or `[[` for context-aware link completion.
- **Rename refactoring:** Rename headings or notes with all references updated workspace-wide.
- **Diagnostics:** Get inline diagnostics for broken/dangling links \& duplicate headings.
- **Find references:** See all usages of a heading or note from any context.
- **Workspace-aware:** All features work across your entire vault when `.marksman.toml` is present.
- **Fast preview (hover):** Hover over links/headings for previews \& details.

***

## 🔗 Navigation \& Linking: Code Actions \& Keymaps

### 1. **Jump To Headings/Sections**

- **Obsidian:** Quick switch (`Cmd+O`), heading menu.
- **Neovim/Marksman:**

```lua
-- LazyVim example: go to symbol (heading) with telescope
vim.keymap.set('n', '<leader; h>', function()
  require('telescope.builtin').lsp_document_symbols({ symbols = { 'String', 'Heading' } })
end)
```

    - Alternative: Use `:lua vim.lsp.buf.document_symbol()` for built-in.

### 2. **Refactor Note Titles / Headings**

- **Obsidian:** Rename triggers updates to links.
- **Neovim/Marksman:**
  - With cursor on a heading:

```lua
vim.keymap.set('n', '<leader; r>', vim.lsp.buf.rename)
-- Triggers Marksman to update all links to this heading across the workspace
```

    - For file renames, use file explorer plugins (e.g., `nvim-tree`, `oil.nvim`) and check that Marksman diagnostics revalidate links workspace-wide.

### 3. **Update Links With Completion**

- Start a link (`[`, or `[[`), trigger completion:

```lua
-- Ensure completion plugin is enabled for markdown (e.g., nvim-cmp with LSP source)
-- Completion will propose notes/headings and auto-format wiki/anchor links
```

    - Use `Tab` to cycle suggestions—very ADHD-friendly, keeps flow fast.

### 4. **Diagnostics For Broken Links \& Ambiguities**

- View with `:lua vim.diagnostic.open_float()`, or in-line via signs.
- Aggregate workspace errors:

```lua
vim.keymap.set('n', '<leader; D>', function()
  require('telescope.builtin').diagnostics({ bufnr = 0 }) -- all broken links/duplicates
end)
```

### 5. **Preview Links/Headings (Hover)**

- Hover with `K` (shift-K) on link/heading.

***

## ⚡️ Atomic Workspace Operations

- **Renaming headings automatically updates all inbound links** via Marksman's refactor API—no broken references or manual edits.
- **Moving/Renaming files:** File explorer plugins use native file ops; with `.marksman.toml`, Marksman re-parses workspace, updating diagnostics for any broken links immediately.
- **Creating new notes:** Just link to a non-existent note—Marksman highlights missing file, then create with new file (e.g., `:e notes/NewNote.md`), and errors clear.

***

## 🧰 Advanced Note-Taking — Templates \& Tasks

- **Daily note creation:**

```lua
-- Example LazyVim keymap for auto-generating today's note
vim.keymap.set('n', '<leader; dn>', function()
  local date = os.date('%Y-%m-%d')
  vim.cmd('e notes/'..date..'.md')
end)
```

- **Template/snippet expansion:**
  - Use [LuaSnip](https://github.com/L3MON4D3/LuaSnip) or [UltiSnips](https://github.com/SirVer/ultisnips) for markdown templates.
  - Example config: trigger a snippet for meeting notes, daily log, etc.
- **In-note task management:**
  - Use checkboxes (`- [ ] task`) natively; parse/search via Telescope grep or custom Lua functions.

***

## 🛠️ Setup \& Automation Tips

- **Mason** for automatic Marksman LSP install:

```lua
require('mason').setup()
require('mason-lspconfig').setup { ensure_installed = { 'marksman' } }
require('lspconfig').marksman.setup { filetypes = { 'markdown' } }
```

- **Workspace config:** Place an empty `.marksman.toml` at your vault root for full cross-file features.
- **Dotfile Example:**
  - See [LazyVim LSP config example](https://www.lazyvim.org/extras/lang/markdown) for plug-and-play integration.
- **ADHD Optimizations:**
  - Keep mappings single-stroke, avoid modal complexity.
  - Use Telescope for search and jump (fuzzy is faster than menus).
  - Use workspace diagnostics view as "inbox"—only fix what breaks your navigation.
  - Autofocus new notes with auto-tmpl snippet.

***

## ⏩ Quick Comparison: Obsidian Vs Neovim/Marksman Workflows

| Workflow | Obsidian | Neovim + Marksman LSP |
| :-- | :-- | :-- |
| Jump to heading/note | Cmd+O, heading nav | `Telescope symbols`, `<leader; h>` |
| Link completion | Wiki style, auto-linking | `[`, `[[`, completion in markdown |
| Rename heading/note | Auto-refactor, link update | `vim.lsp.buf.rename` keymap |
| Broken/dangling link diag | Visual indicators | Native LSP diagnostics, `<leader; D>` |
| Atomic workspace changes | Built-in, proprietary | LSP refactor, workspace detection |
| Markdown templates | Templates, snippets | LuaSnip/UltiSnips triggers |
| Task management | Checkboxes, plugins | Markdown tasks + grep/search |

***

## Next Step

Give me a workflow you'd like to migrate or automate—from Obsidian to Neovim—and we can build it step by step, with keyboard shortcuts and Lua/config examples at each stage.

<span style="display:none">[^1_1]</span>

<div align="center">⁂</div>

[^1_1]: <https://github.com/artempyanykh/marksman>
