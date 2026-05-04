# nvim setup

# Nvim Setup

To effectively configure Neovim with Lazy.nvim as your plugin manager, while integrating LSP features, Tree-sitter, Mason, and completion support, we need to define a hierarchy and explain how these components work together.

## Hierarchy Breakdown

1. Neovim (Core)

   - The base editor that will be extended with plugins for LSP, completion, syntax highlighting, and more.

2. Lazy.nvim (Plugin Manager)

   - Handles the installation and loading of Neovim plugins like `nvim-lspconfig`, `mason.nvim`, `nvim-treesitter`, etc.

3. LSP Client (Built-in in Neovim)

   - Neovim's built-in LSP client communicates with LSP servers. Plugins like `nvim-lspconfig` and `mason.nvim` help with configuring and managing these LSP servers.

4. nvim-lspconfig

   - Provides easy configuration for LSP servers in Neovim's built-in LSP client.

5. Mason.nvim

   - Manages installation of LSP servers, debuggers, linters, and formatters.

6. mason-lspconfig.nvim

   - Bridges Mason and `nvim-lspconfig` for smoother integration of LSP servers managed by Mason.

7. nvim-treesitter

   - Provides better syntax highlighting, code folding, and more using Tree-sitter's parsing technology.

8. Completions (nvim-cmp)

   - Handles autocompletion features for LSP, buffer, path, etc.

## Configuration Strategy

To integrate these components, we will:

- Use Lazy.nvim to load and manage the plugins.

- Configure LSP servers via Mason and `nvim-lspconfig`.

- Integrate syntax highlighting via Tree-sitter.

- Set up completion using `nvim-cmp`.

## Example Configuration

```lua
-- File: ~/.config/nvim/init.lua

-- Ensure lazy.nvim is installed first
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  -- Mason: LSP, formatters, linters manager
  {
    "williamboman/mason.nvim",
    build = ":MasonUpdate",
    config = function()
      require("mason").setup()
    end,
  },

  -- Mason LSPconfig: Integrates Mason with nvim-lspconfig
  {
    "williamboman/mason-lspconfig.nvim",
    after = "mason.nvim",
    config = function()
      require("mason-lspconfig").setup({
        ensure_installed = { "lua_ls", "pyright", "tsserver" }, -- add desired LSP servers
      })
    end,
  },

  -- nvim-lspconfig: Easy configuration for LSP
  {
    "neovim/nvim-lspconfig",
    after = "mason-lspconfig.nvim",
    config = function()
      local lspconfig = require("lspconfig")

      -- Example LSP server configurations
      lspconfig.lua_ls.setup({})
      lspconfig.pyright.setup({})
      lspconfig.tsserver.setup({})
    end,
  },

  -- nvim-cmp: Autocompletion plugin
  {
    "hrsh7th/nvim-cmp",
    config = function()
      local cmp = require("cmp")
      cmp.setup({
        snippet = {
          expand = function(args)
            vim.fn["vsnip#anonymous"](args.body)
          end,
        },
        mapping = cmp.mapping.preset.insert({
          ['<C-d>'] = cmp.mapping.scroll_docs(-4),
          ['<C-f>'] = cmp.mapping.scroll_docs(4),
          ['<C-Space>'] = cmp.mapping.complete(),
          ['<C-e>'] = cmp.mapping.close(),
          ['<CR>'] = cmp.mapping.confirm({ select = true }),
        }),
        sources = {
          { name = 'nvim_lsp' },
          { name = 'vsnip' },
          { name = 'buffer' },
          { name = 'path' },
        }
      })
    end,
  },

  -- nvim-cmp LSP source
  { "hrsh7th/cmp-nvim-lsp", after = "nvim-cmp" },

  -- Snippet engine for nvim-cmp
  { "hrsh7th/vim-vsnip", after = "nvim-cmp" },

  -- nvim-treesitter: Better syntax highlighting and parsing
  {
    "nvim-treesitter/nvim-treesitter",
    run = ":TSUpdate",
    config = function()
      require("nvim-treesitter.configs").setup({
        ensure_installed = { "lua", "python", "javascript", "html", "css" }, -- languages to be installed
        highlight = {
          enable = true, -- enable treesitter-based syntax highlighting
        },
        indent = { enable = true }, -- enable tree-sitter based indentation
      })
    end,
  },
})

-- Optional: Configure diagnostics to look clean
vim.diagnostic.config({
  virtual_text = {
    prefix = "●", -- Could be '●', '▎', 'x'
  },
  update_in_insert = true,
})
```

## Detailed Flow

1. Neovim:

   - Neovim acts as the editor with built-in support for LSP. The `nvim-lspconfig` plugin makes it easier to configure language servers.

2. Lazy.nvim:

   - Handles the lazy-loading of all plugins, ensuring Neovim remains fast and only loads what's needed.

3. Mason.nvim:

   - A utility for managing LSP servers, formatters, linters, and other language tools. It installs these binaries locally without the need for manual installation.

4. mason-lspconfig.nvim:

   - Integrates Mason and `nvim-lspconfig`, automatically ensuring that installed servers are registered with the LSP client and Neovim.

5. nvim-lspconfig:

   - Provides quick and easy configuration for LSP servers, allowing you to set up LSP for various languages by just specifying the server names.

6. nvim-cmp (Completion Engine):

   - This handles code completions from LSP and other sources like the buffer, path, and snippets.

7. nvim-treesitter:

   - Provides enhanced syntax highlighting, indentation, and code folding using the Tree-sitter library. It ensures a more modern and precise syntax highlighting experience compared to traditional regex-based methods.

## Workflow Summary

- Mason.nvim installs and manages LSP servers.

- mason-lspconfig ensures that these LSP servers are automatically configured with Neovim's LSP client using `nvim-lspconfig`.

- nvim-lspconfig makes LSP server configuration more straightforward.

- nvim-treesitter improves the syntax highlighting experience by using a more accurate and efficient parsing engine.

- nvim-cmp provides autocompletion support, pulling suggestions from the LSP server, buffer content, paths, and snippets.

## Final Notes

- Ensure you have the required dependencies installed for LSP servers to run (e.g., Node.js for `tsserver`).

- Adjust the `ensure_installed` options in both `mason-lspconfig` and `nvim-treesitter` for your desired languages.

- Customize the key bindings and sources for `nvim-cmp` as per your preferences.

This setup provides a modern and fully-featured Neovim development environment, leveraging the power of LSP and completion, with Lazy.nvim ensuring optimal performance and plugin management.