# Cracking Neovim code folding 1

# Cracking Neovim Code Folding 1

## Foldmethod and Foldexpr

I chose to use [treesitter](https://github.com/nvim-treesitter/nvim-treesitter?tab=readme-ov-file#folding) as my source of truth for folding. I chose this over the LSP option as I don't always work in codebases that have an LSP configured - especially if I am quickly hacking on a script. By using the treesitter grammar, I ensure every file I load will have it.

```lua
vim.opt.foldmethod = "expr"vim.opt.foldexpr = "v:lua.vim.treesitter.foldexpr()"
```

## Foldcolumn

I don't like taking up room with an extra column to display information on folds, so I turn this off.

```lua
vim.opt.foldcolumn = "0"
```

## Foldtext

By setting this to an empty string, it means that the first line of the fold will be syntax highlighted, rather than all be one colour. I prefer this visually to a formatted line representing the fold with no syntax highlighting.

```lua
vim.opt.foldtext = ""
```

> At the time of writing this feature is only in Neovim nightly and not in the stable 0.9.X releases.

## Foldlevel and Foldlevelstart

Setting `foldlevel` sets the minimum level of a fold that will be closed by default. Therefore I set this to `99` as I don't want this behaviour at all.

However, I discovered that I can use `foldlevelstart` to dicate upon editing a buffer what level of folds should be open by default vs closed.

After some experimenting, I settled on `1` for this value, meaning top level folds are open, but anything nested beyond that is closed. I've found this helps with navigating a large file as not all the contents will be expanded initially.

```lua
vim.opt.foldlevel = 99
vim.opt.foldlevelstart = 1
```

## Foldnestmax

This limits how deeply code gets folded, and I've found that I don't really care for nesting some object 20 levels deep into a function (however rare that is!). So I set this value to `4`, meaning that once code gets beyond 4 levels it won't be broken down into more granular folds. I've found this means I can easily toggle larger chunks of nested code as they are treated as one fold. I think this a very subjective setting though!

```lua
vim.opt.foldnestmax = 4
```

```lua
vim.opt.foldcolumn = "0"
vim.opt.foldmethod = "expr"
vim.opt.foldexpr = "v:lua.vim.treesitter.foldexpr()"
vim.opt.foldtext = ""

vim.opt.foldnestmax = 3
vim.opt.foldlevel = 99
vim.opt.foldlevelstart = 99

local function close_all_folds()
  vim.api.nvim_exec2("%foldc!", { output = false })
end
local function open_all_folds()
  vim.api.nvim_exec2("%foldo!", { output = false })
end

vim.keymap.set("n", "<leader>zs", close_all_folds, { desc = "[s]hut all folds" })
vim.keymap.set("n", "<leader>zo", open_all_folds, { desc = "[o]pen all folds" })
```