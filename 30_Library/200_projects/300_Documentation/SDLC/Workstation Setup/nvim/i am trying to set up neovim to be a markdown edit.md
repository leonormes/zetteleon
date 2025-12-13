---
aliases: []
confidence: 
created: 2025-03-19T18:43:57Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [nvim, pkm, workstation]
title: i am trying to set up neovim to be a markdown edit
type: 
uid: 
updated: 
version: 
---

i am trying to set up neovim to be a markdown editor. I want to read markdown files in both obsidian or nvim. But the line lengths are a problem. In obsidian there is a readability setting that wraps the long lines to a sensible length and centres the text. nvim doesn't do this and the lines are just full screen length. I have looked it up but people seem to use newlines when the line reaches a certain number of chars. This is bad then in obsidian. I don't want to hard code line breaks. How can I get nvim to softwrap any text to the same as obsidian does

To achieve Obsidian-like soft wrapping in Neovim for Markdown without hard line breaks, use a combination of native settings and specialized plugins:

## Core Configuration

**Basic soft wrapping** (works with any Neovim install):

```lua
-- Enable visual wrap without line breaks
vim.wo.wrap = true
vim.wo.linebreak = true  -- Break at word boundaries
vim.wo.breakindent = true  -- Maintain indentation in wrapped lines
vim.wo.showbreak = '↪ '  -- Optional wrap indicator
```

**Window-centric wrapping** (mimics Obsidian's centered layout):

```lua
vim.opt_local.colorcolumn = "80"  -- Visual guide without affecting splits
vim.cmd[[autocmd BufWinEnter *.md setlocal winwidth=80]]  -- Soft-limit window width
```

## Recommended Plugins

### 1. wrapping.nvim ([GitHub][^2][^4])

- Auto-detects wrapping style (soft/hard)
- Provides commands to toggle modes
- Works with Treesitter for Markdown files

```lua
-- lazy.nvim config example
{
  "andrewferrier/wrapping.nvim",
  config = function()
    require("wrapping").setup({
      auto_set_mode = true,
      default_to_soft = true  -- Force soft-wrap if detection fails
    })
  end
}
```

### 2. render-markdown.nvim ([GitHub][^6])

Adds Obsidian-like rendering features:

```lua
{
  "MeanderingProgrammer/render-markdown.nvim",
  ft = "markdown",
  opts = {
    view = {
      centered = true,  -- Mimic Obsidian's centered layout
      width = 80        -- Match your preferred line length
    }
  }
}
```

## Key Workflow Notes

1. **Avoid `textwidth`/`formatoptions`** - These insert hard line breaks[^5]
2. **Use `gwap` command** - Reflows paragraphs without changing line endings
3. **Vertical splits** - Use `vim.opt.winwidth` instead of `columns`[^1] to prevent split issues

This setup maintains compatibility with Obsidian while providing:

- Word-aware soft wrapping
- Visual column guides
- Centered content display
- Automatic wrapping style detection

For focused writing sessions, combine with:

```lua
:set nonumber norelativenumber  -- Minimal UI
:Goyo 80  -- If using goyo.vim for centered writing
```

<div style="text-align: center">⁂</div>

[^1]: <https://neovim.discourse.group/t/how-to-have-a-soft-word-wrap-without-messing-with-vertical-splits/4246>

[^2]: <https://github.com/andrewferrier/wrapping.nvim>

[^3]: <https://github.com/benlubas/wrapping-paper.nvim>

[^4]: <https://www.reddit.com/r/neovim/comments/105ut94/new_plugin_for_handling_softhard_line_wrapping/>

[^5]: <https://sbulav.github.io/til/til-neovim-autoformatting-markdown/>

[^6]: <https://github.com/MeanderingProgrammer/render-markdown.nvim>

[^7]: <https://stackoverflow.com/questions/39945392/soft-wrap-by-markdown-only>

[^8]: <https://github.com/neovim/neovim/issues/3784>

[^9]: <https://stackoverflow.com/questions/25290840/vim-automatic-line-wrapping-in-markdown>

[^10]: <https://martin-ueding.de/posts/hard-vs-soft-line-wrap/>
