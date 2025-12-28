---
aliases: []
tags: []
title: "GitHub - Allaman/tf.nvim: A Neovim plugin for a better Terraform experience"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-28T08:49:52+00:00
modified: 2025-12-28T18:49:36+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# GitHub - Allaman/tf.nvim: A Neovim plugin for a better Terraform experience

![rw-book-cover](https://opengraph.githubassets.com/fb62eaa481967888b3bcf4dca58b1812a9a19ff496e387ad3a6ef595d4e39538/Allaman/tf.nvim)

## Metadata

- Author: [[https://github.com/Allaman/]]
- Full Title: GitHub - Allaman/tf.nvim: A Neovim plugin for a better Terraform experience
- Category: #articles
- Summary: tf.nvim is a Neovim plugin that makes working with Terraform easier.
It opens provider docs, shows and edits Terraform state, and runs validate without leaving the editor.
It is configurable (providers, browser, filetypes) and supports major providers.
- URL: https://github.com/Allaman/tf.nvim

## Full Document

### Allaman/tf.nvim

main

Go to file

Code

Open more actions menu

### tf.nvim

[![Neovim](https://camo.githubusercontent.com/28b5ffd8f49341656d05ea42230b36f741bf5b55617b8b723888486557cdab1a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4e656f56696d2d2532333537413134332e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d6e656f76696d266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/28b5ffd8f49341656d05ea42230b36f741bf5b55617b8b723888486557cdab1a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4e656f56696d2d2532333537413134332e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d6e656f76696d266c6f676f436f6c6f723d7768697465)

[![Lua](https://camo.githubusercontent.com/e36213a395c2482ef182bcbce90143b8213e49aefa0761e9681cc96d38e05ffc/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c75612d2532333243324437322e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d6c7561266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/e36213a395c2482ef182bcbce90143b8213e49aefa0761e9681cc96d38e05ffc/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c75612d2532333243324437322e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d6c7561266c6f676f436f6c6f723d7768697465)

[![CI](https://github.com/Allaman/tf.nvim/actions/workflows/ci.yml/badge.svg)](https://github.com/Allaman/tf.nvim/actions/workflows/ci.yml/badge.svg)

[![size](https://camo.githubusercontent.com/1bd8c8bd3483e7fcb281a4dbc267d1892f9648c2fe90c41e5a96330e8543a733/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f7265706f2d73697a652f416c6c616d616e2f74662e6e76696d)](https://camo.githubusercontent.com/1bd8c8bd3483e7fcb281a4dbc267d1892f9648c2fe90c41e5a96330e8543a733/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f7265706f2d73697a652f416c6c616d616e2f74662e6e76696d)

[![issues](https://camo.githubusercontent.com/d8752464fc6fd092d0f8d336c2fc43d6fc3a0ed52131166d39f6282b3ddd4708/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6973737565732f416c6c616d616e2f74662e6e76696d2e737667)](https://camo.githubusercontent.com/d8752464fc6fd092d0f8d336c2fc43d6fc3a0ed52131166d39f6282b3ddd4708/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6973737565732f416c6c616d616e2f74662e6e76696d2e737667)

[![last commit](https://camo.githubusercontent.com/24b10188f246ff482490b0e47af61c4d9c68dab2859d36004f65bb5a7c1d00a5/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6173742d636f6d6d69742f416c6c616d616e2f74662e6e76696d)](https://camo.githubusercontent.com/24b10188f246ff482490b0e47af61c4d9c68dab2859d36004f65bb5a7c1d00a5/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6173742d636f6d6d69742f416c6c616d616e2f74662e6e76696d)

[![license](https://camo.githubusercontent.com/4181ab611afd4d4a5a7fd5bc7a9afd97268630f370f4968aaca9090e8c7db6c7/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f416c6c616d616e2f74662e6e76696d)](https://camo.githubusercontent.com/4181ab611afd4d4a5a7fd5bc7a9afd97268630f370f4968aaca9090e8c7db6c7/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f416c6c616d616e2f74662e6e76696d)

[![release](https://camo.githubusercontent.com/df00d1750312b74ce47bf8d2ff24ace2d01209d3cca84a99bbf03593cf4bbc64/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f762f72656c656173652f416c6c616d616e2f74662e6e76696d3f736f72743d73656d766572)](https://camo.githubusercontent.com/df00d1750312b74ce47bf8d2ff24ace2d01209d3cca84a99bbf03593cf4bbc64/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f762f72656c656173652f416c6c616d616e2f74662e6e76696d3f736f72743d73656d766572)

A Neovim plugin for

* quickly accessing Terraform provider documentation
* Reading and deleting Terraform state
* Run validation

#### Features

* Parse Terraform `resource` and `data` blocks under cursor
	+ Support for major providers (AWS, Azure, Google Cloud, and more)
	+ Automatically constructs Terraform Registry documentation URLs
	+ Configurable provider registry for custom/community providers
	+ Copy URL to clipboard OR open directly in browser
	+ Configurable browser command
* View and manage Terraform state - interactive state browser
	+ Filter, search, and copy Terraform state addresses in-place
	+ Delete resources from state with confirmation dialog
* Run `terraform validate` without leaving Neovim

#### Installation

```
{
  "allaman/tf.nvim",
  opts = {},
  ft = "terraform"
}
```

#### Usage

##### Commands

**Terraform Documentation:**

* `:TerraformDoc` - Uses the configured default action (copy)
* `:TerraformDocCopy` - Always copy URL to clipboard
* `:TerraformDocOpen` - Always open URL in browser

[![tf-doc.png](https://camo.githubusercontent.com/18d86a2cf4cd9989c50f9c33efb050b3a2d70c3cca086ac1b8e267407aa9e7cd/68747470733a2f2f7331322e67696679752e636f6d2f696d616765732f62684d4c452e706e67)](https://camo.githubusercontent.com/18d86a2cf4cd9989c50f9c33efb050b3a2d70c3cca086ac1b8e267407aa9e7cd/68747470733a2f2f7331322e67696679752e636f6d2f696d616765732f62684d4c452e706e67)

**State Management:**

* `:TerraformState` - Open interactive state viewer

**State Management:**

* `:TerraformValidate` - Run `terraform validate` in the detected project root

[![ts-state.png](https://camo.githubusercontent.com/f3feb79dc84e2f722b12a917fc1a5558ddc449204d19344378d3a91cb094d1ba/68747470733a2f2f7331322e67696679752e636f6d2f696d616765732f62684d4c682e706e67)](https://camo.githubusercontent.com/f3feb79dc84e2f722b12a917fc1a5558ddc449204d19344378d3a91cb094d1ba/68747470733a2f2f7331322e67696679752e636f6d2f696d616765732f62684d4c682e706e67)

##### Terraform Documentation

1. Open a Terraform file (`.tf`)
2. Place your cursor anywhere on or inside a `resource` or `data` block
3. Run `:TerraformDoc` (or one of the other commands)
4. The documentation URL will be copied to clipboard or opened in browser

##### Terraform State Viewer

The interactive state viewer allows you to browse, inspect, and manage your Terraform state.

###### Opening the State Viewer

Run `:TerraformState` from any directory containing Terraform files. This opens a split window with your state resources. The plugin automatically walks up from the active buffer to find the nearest Terraform root before executing CLI commands, and every operation is launched asynchronously to keep Neovim responsive.

###### Keybindings in State Viewer

| Key | Action |
| --- | --- |
| `<Enter>` | Show detailed state for resource under cursor |
| `y` | Copy resource address to clipboard |
| `d` | Delete resource from state (with confirmation) |
| `r` | Refresh resource list |
| `f` | Prompt for a substring filter |
| `F` | Clear the active filter |
| `q` | Close state viewer |
| `g?` | Show help |

###### Example Workflow

1. Run `:TerraformState`
2. Navigate to a resource using `j/k`
3. `f` to filter resources (if needed)
4. Press `<Enter>` to view details in a split
5. Press d to delete (if needed) with confirmation
6. Press q to close

#### Configuration

##### Custom Providers

Add or override provider configurations:

```
require("tf").setup({
  doc = {
    providers = {
      -- Add a custom provider
      custom = { namespace = "myorg" },

      -- Override a default provider
      aws = { namespace = "custom-aws-fork" },
    }
  }
})
```

##### Browser Configuration

**Default browser commands by OS:**

* macOS: `open`
* Linux: `xdg-open`
* Windows: `start`

Configure the default action and browser command:

```
require("tf").setup({
  doc = {
    -- Set default action to open in browser instead of copying
    default_action = "open", -- "copy" or "open"

    -- Specify custom browser command (optional, auto-detected if not set)
    -- Accepts either a string or an array of args.
    browser_command = "firefox", -- or { "open", "-a", "Safari" }, "brave", etc.
  }
})
```

##### Terraform CLI Configuration

Override Terraform binary (e.g. when not in PATH)

```
require("tf").setup({
  terraform = {
    bin = "/opt/homebrew/bin/terraform",
  },
})
```

##### Filetype Configuration

Control which filetypes can trigger documentation lookups (defaults include `terraform`, `tf`, `terraform-vars`, `tfvars`, and `hcl`):

```
require("tf").setup({
  filetypes = { "terraform", "tf", "terraform-vars", "tfvars", "hcl" },
})
```

##### State Viewer Options

Tune filtering and detail view behavior:

```
require("tf").setup({
  state = {
    filter = { case_sensitive = true },
    detail = { folds = true, foldmethod = "syntax" },
    window = {
      mode = "float", -- "vsplit" (default), "split", or "float"
      split = { position = "botright", size = 80 },
      float = { width = 0.7, height = 0.8 },
      focus = false,
    },
  },
})
```

##### Key Mappings

You can create keymaps for quick access:

```
vim.keymap.set("n", "<leader>td", ":TerraformDoc<cr>", { desc = "Terraform Documentation" })
vim.keymap.set("n", "<leader>tc", ":TerraformDocCopy<cr>", { desc = "Terraform Doc (Copy)" })
vim.keymap.set("n", "<leader>to", ":TerraformDocOpen<cr>", { desc = "Terraform Doc (Open)" })
vim.keymap.set("n", "<leader>ts", ":TerraformState<cr>", { desc = "Terraform State" })
vim.keymap.set("n", "<leader>tv", ":TerraformValidate<cr>", { desc = "Terraform Validate" })
```

#### Supported Providers

The plugin includes built-in support for:

##### HashiCorp Official

* aws, azurerm, azuread, google, kubernetes, helm
* random, null, template, local, tls
* vault, consul, nomad

##### Community Providers

* datadog, cloudflare, digitalocean
* mongodbatlas, github, gitlab
* auth0, okta, snowflake, databricks

For providers not in the list, the plugin will default to the `hashicorp` namespace. You can add custom providers via configuration.

#### Requirements

* Neovim 0.11+
* Clipboard support (`:checkhealth` and look for "Clipboard") - for documentation copy feature
* `terraform` CLI - for state viewer and validation feature

#### License

MIT

#### Related Projects

* [mvaldes14/terraform.nvim](https://github.com/mvaldes14/terraform.nvim) - Similar to tf.nvim but lacks the doc feature
* [dakota-m/terraform.nvim](https://github.com/dakota-m/terraform.nvim) - Similar to tf.nvim but lacks the doc feature
* [vim-terraform](https://github.com/hashivim/vim-terraform) - Terraform filetype plugin
