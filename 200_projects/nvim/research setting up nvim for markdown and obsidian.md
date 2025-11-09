---
aliases: []
confidence: 
created: 2025-10-26T10:25:05Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: research setting up nvim for markdown and obsidian
type:
uid: 
updated: 
version:
---

Setting up Neovim (nvim) as a powerful Markdown editor with full integration for editing Obsidian vaults is straightforward and provides a fast, distraction-free note-taking experience that syncs directly with your existing vaults. Below are tested steps and plugin recommendations to optimize your workflow for Markdown and seamless Obsidian vault editing using modern nvim best practices as of 2025.[^1_1][^1_2][^1_3]

## Key Plugins for Markdown \& Obsidian Vaults

- `obsidian.nvim` (community fork): Native support for navigating and editing Obsidian vaults inside nvim; bidirectional links, daily notes, templates, and frontmatter.[^1_2][^1_3]
- `markdown-preview.nvim`: Live preview of Markdown files in your browser; KaTeX/Mermaid supported.[^1_4]
- `nvim-treesitter`: Rich syntax highlighting and structure for Markdown (with Treesitter `markdown` parser enabled).[^1_5][^1_6]
- `telescope.nvim`: Fuzzy finder for notes by title/content or tags in vault.[^1_6][^1_7]
- Optional: `render-markdown.nvim` for better in-editor Markdown rendering.[^1_8]

## Step-by-Step Setup

### 1. Install Plugins

With `lazy.nvim` or `packer.nvim` (Lua examples):

```lua
-- obsidian.nvim (community fork)
{ "obsidian-nvim/obsidian.nvim", version = "*", lazy = true, ft = "markdown" },

-- Markdown preview (requires nodejs & yarn)
{
  "iamcco/markdown-preview.nvim",
  build = function() vim.fn["mkdp#util#install"]() end,
  ft = { "markdown" },
},

-- nvim-treesitter
{ "nvim-treesitter/nvim-treesitter" },

-- Telescope (helps search/fuzzy-find notes)
{ "nvim-telescope/telescope.nvim" },

-- Optionally, for pretty Markdown
{ "MeanderingProgrammer/render-markdown.nvim" },
```

Sync plugins and ensure installation completes.

### 2. Configure obsidian.nvim

Basic Lua config for `~/.config/nvim/init.lua` or a dedicated plugin config:

```lua
require("obsidian").setup({
  workspaces = {
    {
      name = "main",
      path = "~/ObsidianVault", -- adjust to your vault location
    },
  },
  daily_notes = {
    folder = "Daily", -- set to your vault's daily notes folder
  },
})
```

Supports multiple vaults and dynamic workspaces (good for Obsidian-style “open folder as vault” flexibility).[^1_2]

### 3. Markdown Preview (Browser)

Enable on-demand preview inside your Markdown files:

- Start preview in open Markdown buffer:
`:MarkdownPreview`
- Toggle/stop as needed:
`:MarkdownPreviewToggle` and `:MarkdownPreviewStop`

### 4. Enhance Editing Experience

- Use Treesitter for highlighting and folding by enabling the `markdown` parser.
- Use Telescope to fuzzy-find/grep notes and tags within your vault.
- Optionally, use code snippets/UltiSnips/Luasnip for live templates (meeting notes, daily notes, etc.).[^1_9][^1_6]

### 5. Sync and Edit Vault

- Use Obsidian on mobile or desktop for quick capture; nvim for fast editing, scripting, Zettelkasten workflows, and bulk editing. Files sync seamlessly as they're plain Markdown.[^1_10][^1_1]
- Set nvim as "default editor" for `.md` files in your OS for one-click opening from Obsidian.[^1_11]

## Tips for ADHD-Friendly Markdown Note-Taking

- Create simple command aliases/scripts for daily note creation and inbox capture.
- Use Obsidian/nvim tags and backlinks to organize contextually, not just by folders.
- Periodically clarify notes using telescope-fuzzy search to surface and organize forgotten fragments.

***

### Example: Minimal Lua Config

```lua
require('obsidian').setup({
  workspaces = {
    { name = "vault", path = "~/vaults/notes" },
  },
  notes_subdir = "Notes", -- Optional
})
```

Enable `markdown` features in Treesitter:

```lua
require'nvim-treesitter.configs'.setup {
  ensure_installed = { "markdown", "markdown_inline" },
  highlight = { enable = true },
}
```

***

## Further Reading

- For a real-world workflow and tips: [Reddit workflow guide], [detailed setup posts], and developer README docs on each plugin.[^1_12][^1_3][^1_7][^1_5][^1_4][^1_6]

***

### Action Items

- Install the core plugins using your Lua plugin manager.
- Set up your vault path in `obsidian.nvim` config.
- Try live preview with `markdown-preview.nvim` and customize as you prefer.
- Consider integrating Telescope and Treesitter for fastest navigation and search within your notes.

If you need a concrete `init.lua` config block tailored for your vault structure or sample scripts for daily note creation, just ask!
