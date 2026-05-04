# Mason

Portable package manager for Neovim that runs everywhere Neovim runs. 

Easily install and manage:

- LSP servers

- DAP servers

- Linters

- Formatters

![image 7.png](image%207.png)

is a [nvim.md](nvim.md) plugin that allows you to easily manage external editor tooling such as [LSP.md](LSP.md) servers, DAP servers, [Linting.md](Linting.md), and [Formatting.md](Formatting.md) through a single interface. 

Packages are installed in Neovim's data directory (`:h standard-path`) by default. Executables are linked to a single `bin/` directory, which `mason.nvim` will add to Neovim's PATH during setup, allowing seamless access from Neovim builtins (shell, terminal, etc.) as well as other 3rd party plugins.

[mason-lspconfig.md](mason-lspconfig.md) bridges Mason with the [lsp-config.md](lsp-config.md) plugin - making it easier to use both plugins together.


