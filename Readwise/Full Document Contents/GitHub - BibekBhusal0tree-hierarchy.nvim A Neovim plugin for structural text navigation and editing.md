# GitHub - BibekBhusal0/tree-hierarchy.nvim: A Neovim plugin for structural text navigation and editing

![rw-book-cover](https://opengraph.githubassets.com/5f96f06d34fdbcc5d7f3f62b4bdbe3b883d23fc0a6ee76f32555a12c8f6a279e/BibekBhusal0/tree-hierarchy.nvim)

## Metadata
- Author: [[https://github.com/BibekBhusal0/]]
- Full Title: GitHub - BibekBhusal0/tree-hierarchy.nvim: A Neovim plugin for structural text navigation and editing
- Category: #articles
- Summary: tree-hierarchy.nvim is a Neovim plugin for easy code navigation and editing using Treesitter. It lets you select and swap code parts like parent, child, and sibling nodes. You need to install Treesitter parsers and can customize keymaps if you want.
- URL: https://github.com/BibekBhusal0/tree-hierarchy.nvim

## Full Document
### BibekBhusal0/tree-hierarchy.nvim

master

Go to file

Code

Open more actions menu

### tree-hierarchy.nvim

A Neovim plugin for structural text navigation and editing using Treesitter.  

 Compatible with the latest Neovim Treesitter API (main/master branch).

  tree-hierarchy.mp4    
#### Features

* **Select Parent/Child/Sibling**: Navigate the syntax tree structurally.
* **Swap Nodes**: Swap the current node with its next or previous sibling.
* **Dot Repeatable**: Swapping operations in Normal mode are dot-repeatable.
* **Smart Context**: Works intuitively in both Normal and Visual modes.

#### Prerequisites

This plugin relies on **Tree-sitter** parsers to understand the structure of your code. You must have treesitter plugin and the parser installed for the language you are editing.

Ensure you have installed the necessary parsers using [nvim-treesitter](https://github.com/nvim-treesitter/nvim-treesitter):

```
:TSInstall <language>
" Example:
:TSInstall lua
:TSInstall python
```

#### Installation

##### Using [lazy.nvim](https://github.com/folke/lazy.nvim)

```
{
  "BibekBhusal0/tree-hierarchy.nvim",
  dependencies = { "nvim-treesitter/nvim-treesitter" },
  config = function()
    require("tree-hierarchy").setup({})
  end,
}
```

#### Default Keymaps

| Mode | Keymap | Action |
| --- | --- | --- |
| **Visual** | `m` | Select Parent |
| **Visual** | `v` | Select Child |
| **Both** | `<leader>mk` | Swap with Previous Sibling |
| **Both** | `<leader>mj` | Swap with Next Sibling |
| **Both** | `<leader>sk` | Select Previous Sibling |
| **Both** | `<leader>sj` | Select Next Sibling |

#### Configuration

Pass these options to the `setup` function:

```
require("tree-hierarchy").setup({
  debug = false,           -- Enable debug notifications (recommended to keep false)
  disable_keymaps = false, -- Disable default key mappings
})
```

##### Custom Keymaps

To use your own keymaps, set `disable_keymaps = true` in the setup function and define your own mappings using the provided user commands or Lua functions.

```
require("tree-hierarchy").setup({
  disable_keymaps = true,
})

local th = require("tree-hierarchy")

-- Example Custom Mappings
vim.keymap.set("x", "<CR>", th.select_parent, { desc = "Select Parent" })
vim.keymap.set("x", "<BS>", th.select_child, { desc = "Select Child" })

-- You can also use User Commands:
-- :THSelectParent
-- :THSelectChild
-- :THSelectNext
-- :THSelectPrev
-- :THSwapNext
-- :THSwapPrev
```

#### Contributing

This is a new plugin, if you want new features or find any bugs feel free to open Issues and Pull Requests.

#### Credits

* [nvim-treesitter](https://github.com/nvim-treesitter/nvim-treesitter)
* [syntax-tree-surfer](https://github.com/ziontee113/syntax-tree-surfer)

#### Similar Plugins

* [syntax-tree-surfer](https://github.com/ziontee113/syntax-tree-surfer)
* [nvim-treesitter-textsubjects](https://github.com/RRethy/nvim-treesitter-textsubjects)

Note

Some similar plugins may not support the latest Treesitter API in latest main branch.

#### License

[MIT](https://github.com/BibekBhusal0/tree-hierarchy.nvim/blob/master/LICENSE)
