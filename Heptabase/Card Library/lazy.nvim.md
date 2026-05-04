# lazy.nvim

[LazyVim](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/ad966919-c4e9-4548-9a79-884a980b6a84) is a Neovim setup powered by [lazy.nvim](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/ad966919-c4e9-4548-9a79-884a980b6a84) to make it easy to customize and extend your config.

Plugins are managed by the lazy.nvim plugin manager. It is configured to automatically load any `.lua` file in your config folder’s `lua/plugins` directory. 

Lua files in this directory should always return a [Lua table](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/b083429f-291c-4d74-a19f-68475dcb9edc). Therefore, they will be structured like this:

```lua
return {

}
```

This Lua table can contain either a plugin specification or a table containing multiple plugin specifications in their own Lua table. For example, the structure will either be:

```lua
return {
  "username/plugin",
  opts = {...},
  keys = {...}
  ...
}
```

for a single plugin specification, or:

```lua
return {
  {
    "username/plugin",
    opts = {...},
    keys = {...}
  },
  {
    "username2/plugin2",
    ...
  }

}
```

Personally, I usually place each plugin in its own file so they are easy to search for when I use the `<Space>fc` shortcut. However, I do use the multiple plugin format when the existence of one plugin requires me to modify the configuration of another.

### Plugin Specifications Cascade

Any one plugin can be specified multiple times in your configuration and LazyVim will merge everything together. There are a few cases where this is useful:

- Some people like to configure keybindings in a separate area from the plugin options and configuration.

- Sometimes you want your primary plugin configuration to be in one file, and then have a second, related plugin configure some overrides for that plugin.

- (Most Common) LazyVim pre-configures many plugins with sensible defaults, but you will occasionally want to override those defaults with your preferred keybindings or options.

### Plugin Specification

The simplest plugin specification is just a table containing a single string with the GitHub username and repo separated by a `/`. Occasionally, this is all you need, especially for VimScript plugins. If the plugin in question isn’t hosted on GitHub, you can omit this first argument and pass either `dir=/path/to/a/folder` or `url=https://domain.com/path/to/plugin`.

If you need to pin your plugin to a specific version or git branch, you can pass the `branch`, `tag`, `commit`, or `version`. For GitHub-hosted plugins, you can find the values for these version specifiers on GitHub. You will likely use this only rarely, as it is normal to install the `main` branch of the plugin. But if you know that a recent change in a plugin is causing issues for you, or if you want to try out some bleeding edge feature that hasn’t been merged yet, you’ll want to set one of these.

There are almost two dozen options you can pass to a Lazy.nvim plugin specification, all documented at <https://lazy.folke.io/spec>. We discussed some of them in Chapter 5, namely `enabled`, `opts`, and `keys`. Now we’ll touch on several of the others.

### Plugin Lifecycle Methods

There are several options that are invoked at various times during the lifecycle of a plugin. You only need to specify these rarely, but they can be very useful to control when code executes, especially if you are trying to port “raw config” installation instructions to Lazy.nvim config.

#### Build

The `build` option is called once when the plugin is installed or updated, and is not called during the normal startup or execution of Neovim. We saw an example of it in the `smart-splits` configuration in chapter 9. In that example, we passed a string path to a shell script that ships with the plugin. Every time the plugin is installed or upgraded, that build command is run, ensuring that the relevant Kitty scripts are installed. In addition to a string pathname, `build` can also be a:

- Lua function that accepts the plugin spec as its only argument.

- path to an arbitrary Lua file.

- the string “rockspec”, which will build a `luarocks` package. Luarocks is a package manager and index for Lua modules not unlike pypi, npm, or crates in the Python, Javascript, and Rust ecosystems respectively.

- string starting with `:`, which will execute an arbitrary Vim command.

- list of one or more of the above.

As a plugin consumer, you will likely only specify the `build` function if the plugin’s documentation instructs you to do so.

#### Init

The `init` option is executed during program startup, so to keep the startup time short, it’s best to avoid it unless absolutely necessary. It accepts a Lua function with a single argument holding any specs for that plugin. (Specifically, it is an instance of [LazyPlugin](https://github.com/folke/lazy.nvim/blob/main/lua/lazy/types.lua)).

I’ve never actually had to specify `init` in any of my plugin configurations. Typically, if I need the plugin to execute at startup, I use `lazy=false` so it configures the whole thing on startup. I can see `init` being helpful if there are legitimate two-step setups, but in my experience, all of those are in plugins that LazyVim is managing on my behalf, so I’ve never needed it.

#### Config

The `config` option is the one you are most likely to specify, but try to only reach for it if you’ve run out of other options. It is called whenever the plugin is loaded, which may be on startup, or only when it is first used, depending on how it is configured.

The first thing you need to understand about `config` is its default behaviour if you don’t specify it.

There is a de facto standard in Lua-based plugins of providing a `setup` function that accepts a single argument which is a table of options for that plugin. The vast majority of plugins you encounter will have instructions in their README to write code something like this:

Listing 77. Non-LazyVim Setup Call

```lua
require('pluginName').setup({key = value, key2 = value2...})
```

They’ll tell you to put this in your `init.lua`. These are good instructions if you’re not using Lazy.nvim, but it’s not for us.

The default `config` function that Lazy.nvim provides invokes this code automatically if your spec contains any `opts`. So the above code should always be ported to something like this:

Listing 78. LazyVim Options

```lua
return {
  'username/plugin',
  opts = {key = value, key2 = value2}
}
```

Under the hood, if you supply `opts` in the plugin spec, the `config` function will call the `.setup` code for you.

This is a wonderful thing because LazyVim does automatic merging of `opts` tables if you provided multiple specs for the same plugin in different places. If you override `config`, you won’t so easily be able to take advantage of this merging behaviour.

However, if the plugin you are configuring is non-standard or requires you to run additional code when it is starting up, you’ll need to specify `config` yourself.

The `config` function is always a Lua function that accepts two arguments. The first is the same `LazyPlugin` spec that `init` receives. The second is the table of `opts` that Lazy.nvim has created for you, possibly by merging opts from multiple definitions.

The main place where this becomes a problem is when you want to customize the default LazyVim configuration for a plugin and that default configuration overrides config.

Unlike with `opts` and `keys`, only one `config` function is called (the last one loaded). So if you specify `config` for a plugin, the LazyVim one will not execute.

Typically, these overridden configs can be modified with judicious use of `opts` or `keys`, but if you need to do imperative tasks that differ from whatever LazyVim provides, there’s a good chance you’ll be copying the entire configuration for that plugin from the [https://lazyvim.org](https://lazyvim.org/) website into your personal config.

While that’s not a great outcome, it’s still better than if you didn’t use LazyVim at all, because then you’d have to write the entire configuration from scratch instead of copying and modifying a trusted source.

### Modifying Options In-place

The “merging” that LazyVim does on `opts` if you supply a table may not always do the right thing, especially with nested tables or if you want to remove, instead of add, a key. Sometimes it is better to specify opts as a Lua function that takes the existing `opts` as input and modifies it in place. A great example of this is the LazyVim [recipe](https://www.lazyvim.org/configuration/recipes) for adding a `nvim-cmp` source:

Listing 79. Modifying Options With Function

```lua
{
  "hrsh7th/nvim-cmp",
  dependencies = { "hrsh7th/cmp-emoji" },
  opts = function(_, opts)
    table.insert(opts.sources, { name = "emoji" })
  end,
}
```

Here, `opts` is specified as a function that takes two arguments, and we modify the second one, which is the Lua table LazyVim is building to pass into `config`. In the case of `nvim-cmp` the LazyVim spec does not override config, so those opts will be passed to the default `config` which calls `require('nvim-cmp).setup(opts)`.

### Complex Plugin Example: Telescope-live-grep-args

LazyVim’s plugin abstractions are usually very elegant, but occasionally can get in the way. I wanted to include a complicated example in the hopes it will help you navigate the hairier situations.

The [Telescope.md](Telescope.md) `live_grep` integration that ships with LazyVim doesn’t allow us to pass arguments to ripgrep by default. However, there is a `telescope-live-grep-args` extension that does permit customizing the ripgrep arguments.

Start by visiting the [telescope-live-grep-args.nvim](https://github.com/nvim-telescope/telescope-live-grep-args.nvim) repository. You’ll find installation instructions for Lazy.nvim (that’s the plugin manager, NOT the LazyVim distro itself) that, at time of writing look like this:

Listing 80. Incorrect Configuration for Telescope Plugin

```lua
-- This is not helpful with LazyVim
use {
  "nvim-telescope/telescope.nvim",
  dependencies = {
    {
        "nvim-telescope/telescope-live-grep-args.nvim" ,
    },
  },
  config = function()
    require("telescope").load_extension("live_grep_args")
  end
}
```

The reason I added the “not helpful” comment there is the call to `config`. LazyVim already configures Telescope with a fairly complex function that you can find under the `editor` section of the plugins menu on the LazyVim website (click the `Full spec`) tab.

For the most part, LazyVim does a good job of merging its own defaults with any customizations you do with the various plugins it sets up. It’s easy to change or remove keybindings or override the options that get passed into a `setup` function, for example.

But it’s not easy to override `config`.

You *could* do something like this:

Listing 81. Another Incorrect Configuration for Telescope Plugin

```lua
config = function(_, opts)
  require("telescope").setup(opts)
  require("telescope").load_extension("live_grep_args")

end
```

This works because the default behaviour of `config` in Lazy.nvim is to call `require(<the_plugin>).setup(opts)`. So we’re basically copying the contents of that function into our custom function. But if LazyVim happened to have a very complicated `config` for Telescope, you would have to copy the whole thing in, and it would eventually get out of date with any changes that LazyVim makes in the future. That wouldn’t be fun for you to maintain. More importantly, it runs a very real risk of clobbering any Telescope-related changes that LazyVim makes with other plugins or extras.

In general, I try very hard to avoid implementing `config` when overriding LazyVim’s defaults. It’s fine to have a custom implementation of `config` if I am adding a new plugin that LazyVim isn’t aware of, since I’m already responsible for maintaining it. But when I’m *customizing* plugins, I try not to override `config`.

The secret (in this case) is to use the “dependencies” feature of Lazy.nvim. The “Full Spec” on the LazyVim website has an example of how to set up the telescope-fzf-native.nvim extension, which looks something like this

Listing 82. How LazyVim Configures Telescope-fzf-native

```lua
  dependencies = {
    {
      "nvim-telescope/telescope-fzf-native.nvim",
      -- snipped some build instructions
      config = function()
        LazyVim.on_load("telescope.nvim", function()
          -- snipped loading the extension
        end)
      end,
    },
  },
```

This is showing us how to have a mini-config for a dependent plugin, which is *exactly* what we want. Further, if we customize our spec, `dependencies` is one of the tables that Lazy.nvim will *merge* with the parent spec (the one created by LazyVim). So we **don’t** need to copy the above code into our Telescope extension file so it doesn’t get clobbered. Instead we only need to create a single new table.

Here’s the configuration (I put it in `extend-telescope.lua`):

Listing 83. Correct Configuuration for Telescope Plugin

```lua
return {
  { "nvim-telescope/telescope-live-grep-args.nvim" },
  {
    "nvim-telescope/telescope.nvim",
    dependencies = {
      {
        "nvim-telescope/telescope-live-grep-args.nvim",
        config = function()
          LazyVim.on_load("telescope.nvim", function()
            require(
              "telescope"
            ).load_extension("live_grep_args")
          end)
        end,
      },
    },
  }
}
```

It’s kind of verbose, but this should be all you need to enable the plugin.

Next, you need to set up a keybinding to invoke the plugin. You can choose to override the existing `<Space>/` keybinding, or perhaps you would use `<Space>?` if you want to have separate “default live_grep” and “live_grep_args” mode.

Your first attempt, if you are following the live-grep-args README might look like this:

Listing 84. Incorrect configuration for Live Grep Args

```lua
-- This won't work
keys = {
  {
    "<leader>/",
    require(
      "telescope"
    ).extensions.live_grep_args.live_grep_args,
    desc = "Grep with Args",
  },
},
```

Unfortunately, this is too easy for LazyVim. Because the `live_grep_args` plugin has been set up to run in a `LazyVim.on_load`, it is not defined at the time this keys array is created.

The solution is to wrap the call in another function, so the import only happens after you press the keybinding. That works because the `onLoad` handler will have been called by that point:

Listing 85. Correct Configuration for Live Grep Args

```lua
keys = {
  -- Other telescope-related keybindings
  {
    "<leader>/",
    function()
      require(
        "telescope"
      ).extensions.live_grep_args.live_grep_args()
    end,
    desc = "Grep with Args (root dir)",
  },
},
```

Before we move on to actually **using** the live-grep-args plugin, there is one more place you need to apply this weird nested function calls trick. Telescope-live-grep-args suggests hooking up `ctrl-k` to the `quote_prompt()` action, like so:

Listing 86. Incorrect Configuration for Live Grep Args Keymaps

```lua
-- Don't do this
local lga_actions = require("telescope-live-grep-args.actions")
telescope.setup {
  extensions = {
    live_grep_args = {
      mappings = { -- extend mappings
        i = {
          ["<C-k>"] = lga_actions.quote_prompt(),
        },
      },
    }
  }
}
```

The table passed into `setup` there just comes from our `opts` array, but we again need to avoid importing `telescope-live-grep-args` at the top-level like that. Instead, we need a new function. But there are a couple gotchas:

- `quote_prompt()` is a function that returns a different function. So we need to invoke that function with a odd-looking `()()` syntax.

- Telescope mappings accept an integer argument (the internal id of the picker), so we need to forward that to the called function.

The resulting `opts` array looks like this:

Listing 87. Correct Configuration For Live Grep Args Keymaps

```lua
opts = {
    extensions = {
      live_grep_args = {
        mappings = {
          i = {
            ["<C-k>"] = function(picker)
              require(
                "telescope-live-grep-args.actions"
              ).quote_prompt()(picker)
            end,
          },
        },
      },
    },
  }
```

For completeness (and because all the above snippets on their own may not make indentational sense), here is my entire Telescope configuration:

Listing 88. Complete Configuration for Live Grep Args

```lua
return {
  { "nvim-telescope/telescope-live-grep-args.nvim" },
  {
    "nvim-telescope/telescope.nvim",
    dependencies = {
      {
        "nvim-telescope/telescope-live-grep-args.nvim",
        config = function()
          LazyVim.on_load("telescope.nvim", function()
            require(
              "telescope"
            ).load_extension("live_grep_args")
          end)
        end,
      },
    },
    keys = {
      {
        "<leader>/",
        function()
          require(
            "telescope"
          ).extensions.live_grep_args.live_grep_args()
        end,
        desc = "Grep with Args (root dir)",
      },
    },
    opts = {
      extensions = {
        live_grep_args = {
          mappings = {
            i = {
              ["<C-k>"] = function(picker)
                require(
                  "telescope-live-grep-args.actions"
                ).quote_prompt()(picker)
              end,
            },
          },
        },
      },
    },
  }
}
```

It’s a mess, I know. Part of the mess is because Telescope is pretty generic, and that mess would still exist if you were managing your own config. But part of the mess is because we need to cooperate with LazyVim when we enter our customizations, and the config is necessarily more complicated than it would be. As usual, I’m ok with this because I have to do it rarely enough and I appreciate not having to manage *most* of my configuration by myself.

### Configuring Non-plugin Options

Vim is a highly configurable editor and Neovim is even more so. There are over three hundred options in the `:help option-list` output. The default Vim configuration for most of these is fine, though there are a few that have silly defaults for historical reasons. Neovim has fixed a few of these and LazyVim sets almost a third of them so the out-of-the-box experience approximates what most modern developers would want.

However, you’ll probably still want to change a few options to suit your taste. This is typically done in the `lua/config/options.lua` file. LazyVim loads this file by default.

For any given option, you *probably* want to set the `vim.opt.<optionname>` field. `vim.opt` is a special Lua table that allows you to interact with Vim settings as…​ well, a special Lua table. If you are searching for a Vim setting and see something saying you should call `:set option=value`, that will work, if you want to do it temporarily. But if you want to store the setting for the next time you start Neovim, you need to translate it to `vim.opt.option = value`.

*Sometimes*, and after 25 years using Vim I’m *still* not sure exactly when, you’ll need to set `vim.g.<optionname> = value` instead. The `g` in this case means global. If you see an instruction to set a variable such as `let g:varname = value`, you may need to use `vim.g.varname = value`. Some options are inherently global while others only apply to the current buffer *unless* you specify `g`. Some plugins, especially older non-Lua plugins, are configured with global variables, and this is the syntax you would use for them as well.

In general, use `vim.opt` unless you see `vim.g` or `g:` in the documentation or code you are copying from.

### Setting the Colour Scheme (Theme)

Vim has two options for setting the colour scheme and they can interact in unexpected ways.

First, you can set your window background to be either `dark` or `light`. You can toggle this setting at runtime with the `<Space>ub` keybinding under the “Ui” menu. **Usually** when you toggle the background, the colour scheme will change the foreground colours to suit the chosen background, but this isn’t always reliable. Sometimes it even changes the colour scheme to a related one that is more suitable when the background is light. For example, if you have `catpuccin-mocha` enabled, and change your background to light, `catpuccin-latte` will become the selected colour scheme.

If you want to change the background permanently, set `vim.opt.background = "light"` or `vim.opt.background = "dark"` in your `options.lua` file.

To change to a different colour scheme altogether, use `<Space>uC` where the C is capitalized. This will pop up a Telescope picker with all currently installed colour schemes. Neovim ships with a few default colour schemes, and LazyVim adds several variations of `Catpuccin` and `Tokyo Night` (the default). The advantage of these colour schemes over the Neovim-provided ones is that they have a ton of extra highlight groups for the various plugins LazyVim installs.

If you want to change the colour scheme permanently, it should be set as an `opt` on the `LazyVim/LazyVim` plugin. I prefer the `catpuccin` colour scheme, so I have a `plugins/core.lua` file that looks like this:

Listing 89. Colour Scheme Configuration

```lua
return {
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "catppuccin",
    },
  },
}
```

However if you want to set the colour scheme to something that isn’t shipped with LazyVim by default, you *also* need to install the plugin that ships that colour scheme. For example, the popular standby gruvbox can be installed like this:

Listing 90. Third Party Colour Scheme

```lua
return {
  { "ellisonleao/gruvbox.nvim" },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "gruvbox",
    },
  },
}
```

|  | When looking for new colour schemes, try to find well-maintained repositories that feature "treesitter support" and provide highlight groups for all the plugins you use regularly (including those that ship with LazyVim). You can find colour schemes on the [Awesome Neovim list](https://github.com/rockerBOO/awesome-neovim/). |

### Lazy Loading

LazyVim automatically lazy-load plugins on demand instead of during program startup. This can shave milliseconds off your startup time (that oh-so-precious resource).

LazyVim knows to load the plugin whenever its code is `require`d, or when any of the keybindings specified in the `keys` array are pressed. This is usually exactly when you want it to load. However, if you encounter plugins that are not working as expected, you may need to tweak the lazy loading configuration.

First, try adding `lazy = false` to the plugin spec. This will ensure the plugin loads on startup. If the plugin works after you add that, you have two options:

- Just leave `lazy = false` and get on with your day.

- Micro-optimize to try to force the plugin to load lazily at the right time.

For the most part, I recommend the first option. Micro-optimization makes sense in the context of optimizing plugins for public consumption. Plugin maintainers might use it in their packages, and certainly distro maintainers such as Folke himself spend a lot of time on it. But it’s not likely worth it for you.

Run the plugin with lazy enabled and disabled and check the startup time in the dashboard. If it makes a difference that you want to solve for, read on.

If a plugin should only be specified for certain filetypes, then add a `ft` key to the spec. This key accepts a string or list of strings representing the filetype. (To get the filetype for the current buffer, type `:set ft<Enter>`).

If instead the plugin should only be loaded if certain commands are called, specify a list of strings with the command names under the `cmd` key.

You can also specify a Neovim `event` that should trigger the plugin to load. There are way too many of these to list in this book, so I’ll refer you to `:help events`. The most common ones to trigger plugin loading would be `BufEnter`, `BufRead`, and `BufWrite`.

### Filetype-specific Configuration

If you need to configure something to run for a specific filetype, you’ll need the `nvim_create_autocmd` function. Technically you can place this call anywhere, including `init.lua` or the `config` or `init` for a specific plugin, but the LazyVim convention is to put them in the `lua/config/autocmds.lua` file.

I actually only have one autocmd because LazyVim does such a good job of configuring filetype-specific behaviours for me (usually using the appropriate `lang.*` LazyVim Extra). That command looks like so:

Listing 91. Filetype-specific Autocommands

```lua
vim.api.nvim_create_autocmd({ "BufRead", "BufNewFile" }, {
pattern = "\*.svx",
command = "setlocal filetype=markdown",
})
```

The first argument is a keyless Lua table of string event names; in this case any time I create or read a file, the autocommand is run. There are other events you can use, but for the most part you’ll only need these two unless you are writing your own plugin (see `:help autocmd-events` for a whole list).

The second argument contains the options for the autocommand. In this case I am including a `pattern`, which is a Vim regex for the type of file I want to match. I specifically said “Vim regex” to excuse the goofy `\*`, as discussed in Chapter 12.

In this case I’m using the `command` key to execute a command whenever I read a `*.svx` file. You can instead specify a `callback` key where the value is a Lua function that will be called whenever the event occurs.

### Per-project Configuration

Sometimes, you’ll want to have a custom LazyVim configuration for a specific project. For example, most of my Typescript projects are in Svelte, which means I can’t (yet) use the exceptional `biome` linter/formatter for them. That means I’m using `prettier` for formatting in these repos. My `extend-conform.lua` plugin specification looks like this:

Listing 92. Prettier in Default Configuration

```lua
return {
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        ["typescript"] = { "prettier" },
        ["markdown"] = { "prettier" },
        ["yaml"] = { "prettier" },
        ["svelte"] = { "prettier" },
      },
    },
  },
}
```

However, for my Typescript API servers, I **can** use Biome, and I want to override my configuration for those projects only.

LazyVim makes this dead simple: just create a `.lazy.lua` file in your project. It can return any valid plugin spec, and it will be called after any other plugins are loaded, overwriting them. So my Hono api server has a `.lazy.lua` file that looks like this:

Listing 93. Project-specific `.lazy.lua`

```lua
return {
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        ["typescript"] = { "biome" },
      },
    },
  },
}
```

You can choose to commit this with your project or `.gitignore` it depending on the standards of the project.

### LazyVim Recipes

LazyVim helpfully collects some of the most commonly requested features as recipes on their [home page](https://www.lazyvim.org/configuration/recipes). Most of these can simply be copied directly into any file in your `lua/plugins` folder. Remember to add `return` in front of them so that whatever table they give you is exported.

Most of the recipes are just providing a set of suggested `opts` to trigger the behaviour in question. These `opts` are always plugin-specific and you’ll need to visit the help file or README for the plugin to understand what they are doing.

### Summary

This chapter was all about configuring LazyVim. Much of it may have been review of examples I’ve used throughout the book when adding plugins to support specific features. However, I wanted to make sure there was coverage in one place for when you want to look things up.