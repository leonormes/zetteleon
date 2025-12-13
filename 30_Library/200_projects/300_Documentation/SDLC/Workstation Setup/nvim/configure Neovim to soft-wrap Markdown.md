---
aliases: []
confidence: 
created: 2025-03-19T06:43:34Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [markdown, nvim, pkm]
title: configure Neovim to soft-wrap Markdown
type: 
uid: 
updated: 
version: 
---

To configure Neovim to soft-wrap Markdown text similarly to Obsidian, you can adjust several settings and utilize plugins to enhance the editing experience without inserting hard line breaks.

**1. Enable Soft Wrapping:**

To wrap long lines visually without inserting actual line breaks, add the following to your Neovim configuration (`init.vim` or `init.lua`):

```vim
" Enable line wrapping
set wrap

" Break lines at word boundaries
set linebreak

" Indicate wrapped lines with a character (e.g., '↪')
set showbreak=↪
```



These settings ensure that lines wrap at word boundaries, enhancing readability.

**2. Set Text Width for Optimal Readability:**

To limit the width of text, making it easier to read, you can set the `textwidth` option. For example, to set it to 80 characters:

```vim
" Set text width to 80 characters
set textwidth=80
```



This setting controls the maximum width of text before it wraps to the next line.

**3. Center Text in the Window:**

To center the text within the window, you can use the `colorcolumn` option to create visual margins:

```vim
" Set color column at 80 characters
set colorcolumn=80
```

This creates a vertical line at the 80-character mark, helping to center your text visually.

**4. Utilize Plugins for Enhanced Markdown Editing:**

Several plugins can further improve the Markdown editing experience in Neovim:

- **`vim-pencil`:** Enhances soft-wrapping and formatting for prose writing.
- **`render-markdown.nvim`:** Improves the rendering of Markdown files within Neovim, providing a more readable and visually appealing display.
- **`marksman`:** A language server for Markdown that offers features like document symbols, completion for links, and navigation.

**5. Example Configuration:**

Here's how you might incorporate these settings and plugins into your Neovim configuration:

```lua
-- init.lua

-- Enable line wrapping and set text width
vim.o.wrap = true
vim.o.linebreak = true
vim.o.showbreak = '↪'
vim.o.textwidth = 80
vim.o.colorcolumn = '80'

-- Plugin manager setup (e.g., using 'packer.nvim')
require('packer').startup(function()
  use 'preservim/vim-pencil'  -- Enhanced soft-wrapping
  use {
    'MeanderingProgrammer/render-markdown.nvim',
    requires = { 'nvim-treesitter/nvim-treesitter', 'nvim-tree/nvim-web-devicons' },
    config = function()
      require('render-markdown').setup({})
    end
  }
  use 'artempyanykh/marksman'  -- Markdown language server
end)

-- Enable vim-pencil for Markdown files
vim.cmd [[
  autocmd FileType markdown call pencil#init()
]]
```

This configuration sets up soft-wrapping, centers the text, and integrates plugins to enhance the Markdown editing experience in Neovim.

**Additional Resources:**

For a comprehensive guide on setting up Neovim for Markdown editing, consider reviewing the following resource:

- **"My Neovim markdown setup in 2025"** By Christian Arzu: This blog post details various plugins, tips, and tricks for taking Markdown notes in Neovim as of January 2025.

By implementing these configurations and utilizing the recommended plugins, you can achieve a Markdown editing environment in Neovim that closely resembles the readability and formatting features of Obsidian, without the need for hard-coded line breaks.

## Achieving Consistent Markdown Readability in Neovim and Obsidian

**1. Introduction: Bridging the Readability Gap Between Obsidian and Neovim**

Users who work with Markdown files across different platforms often seek a consistent and comfortable reading experience. Obsidian, a popular note-taking application, provides a "readability setting" that intelligently wraps long lines of text to a manageable width and centres them on the screen. This feature enhances focus and reduces eye strain, particularly when dealing with lengthy documents. Neovim, a powerful and highly customizable text editor, in its default configuration, displays Markdown files with lines extending to the full width of the editor window. This can lead to horizontal scrolling and a less optimal reading experience for users accustomed to Obsidian's presentation. The core issue arises from the difference in how these two applications handle the visual presentation of long lines in Markdown files.

Obsidian's approach to readability involves dynamically adjusting the display of text without altering the underlying Markdown content. It achieves this by implementing a form of soft wrapping, where lines that exceed a certain width are visually broken into multiple lines within the editor window. Furthermore, the centring of the text block contributes to a focused reading environment. In contrast, Neovim, by default, does not impose such visual constraints online length. Long lines simply continue horizontally, requiring the user to scroll to view the entire content. While this behavior is suitable for many coding and text editing tasks, it can detract from the reading experience of prose-heavy Markdown documents.

The user in this scenario specifically desires to replicate Obsidian's soft wrapping behavior within Neovim when editing Markdown files. A critical constraint is that this solution must not involve inserting hard line breaks (newline characters) into the Markdown files themselves. Introducing hard line breaks would negatively impact how these files are rendered in Obsidian, defeating the purpose of achieving consistency. Therefore, the goal is to find a method to make Neovim visually wrap long lines of Markdown text to a sensible length, mirroring Obsidian's functionality, without making any permanent changes to the file content. This report will explore various Neovim features, configuration options, and plugins that can be employed to achieve this desired visual consistency.

**2. Leveraging Neovim's Core Functionality for Soft Wrapping**

Neovim possesses built-in features that can be configured to address the user's need for soft wrapping in Markdown files. The primary options to consider are `wrap` and `textwidth`.

**2.1 The `wrap` Option: Enabling Basic Soft Wrapping**

The fundamental setting for enabling soft wrapping in Neovim is the `wrap` option. When this option is enabled (`:set wrap` or `vim.opt.wrap = true`), Neovim will visually break lines that are longer than the editor window's width onto the next line 1. This means that while the underlying line in the file remains unbroken, it will be displayed as multiple lines within the Neovim buffer. This behavior directly addresses the user's requirement for lines to not extend beyond the screen's edge. The `wrap` option can be set globally in the Neovim configuration file (`init.lua` or `init.vim`) to apply to all file types. However, for the specific use case of Markdown editing, it is more appropriate to enable it only for Markdown files. This can be achieved using an autocommand that triggers when a Markdown file is opened 1. For instance, the following Lua code snippet in the Neovim configuration would enable the `wrap` option specifically for Markdown files:

Lua

```lua
vim.api.nvim_create_autocmd("FileType", {
    pattern = {"markdown"},
    callback = function()
        vim.opt_local.wrap = true
    end,
})
```

Alternatively, this setting can be placed in a file named `markdown.lua` (or `markdown.vim` for Vimscript) within the `~/.config/nvim/after/ftplugin/` directory. This `ftplugin` mechanism allows for filetype-specific configurations that are loaded after the main configuration and any plugins, ensuring that these settings are applied only when editing files of the specified type 4. While the `wrap` option provides the basic visual line breaking, it does not, by itself, control the width at which the lines are wrapped. This is where the `textwidth` option comes into play.

**2.2 The `textwidth` Option: Defining the Visual Line Length**

The `textwidth` option in Neovim allows users to define a maximum character width for lines 2. When `textwidth` is set to a specific number (e.g., 80), Neovim will attempt to keep lines within that length. Importantly, when typing new text, Neovim will automatically insert line breaks at word boundaries to adhere to this specified width 2. This is crucial for mimicking Obsidian's behavior of wrapping lines to a "sensible length," which is often considered to be around 80 characters for readability 9. Similar to the `wrap` option, `textwidth` can be set globally, but it is more effective to configure it specifically for Markdown files. This ensures that other file types, where a different line length might be preferred (like in code files), are not affected. The same autocommand or `ftplugin` mechanism used for the `wrap` option can also be used to set the `textwidth` for Markdown files 3. For example, adding the following line to the previous Lua autocommand would set the `textwidth` to 80 characters for Markdown files:

```lua
vim.opt_local.textwidth = 80
```

It is important to note that the `textwidth` option primarily affects new text being entered. Existing lines in a Markdown file that exceed the set `textwidth` will not be automatically wrapped 10. To apply the `textwidth` to existing content, a reformatting command like `gq` needs to be used, which will be discussed in a later section 9.

**2.3 Combining `wrap` and `textwidth` for the Desired Effect**

To achieve the desired Obsidian-like soft wrapping in Neovim, both the `wrap` and `textwidth` options need to be enabled and configured for Markdown files. The `wrap` option ensures that lines exceeding the window width are visually wrapped, while the `textwidth` option dictates the preferred maximum length of these visual lines. By setting `textwidth` to a value like 80, users can ensure that long paragraphs are broken down into readable chunks, similar to how Obsidian handles them 9. The combined configuration, using an autocommand in `init.lua`, would look like this:

```lua
vim.api.nvim_create_autocmd("FileType", {
    pattern = {"markdown"},
    callback = function()
        vim.opt_local.wrap = true
        vim.opt_local.textwidth = 80
    end,
})
```

Alternatively, the same configuration within a `~/.config/nvim/after/ftplugin/markdown.lua` file would be:

Lua

```lua
vim.opt_local.wrap = true
vim.opt_local.textwidth = 80
```

This basic configuration using Neovim's core options provides a solid foundation for achieving soft wrapping in Markdown files. However, for users seeking more advanced control or encountering specific scenarios, exploring dedicated plugins might be beneficial.

**3. Exploring Advanced Wrapping with `wrapping.nvim`**

For users who desire more sophisticated control over wrapping behavior, the `wrapping.nvim` plugin offers an alternative approach 3. This plugin is designed to simplify the management of both soft and hard wrapping modes in Neovim, particularly for text-like files such as Markdown.

**3.1 Introduction to `wrapping.nvim`**

`wrapping.nvim` attempts to automatically detect the natural wrapping style of text files when they are opened 3. Some Markdown files might consist of long lines without hard carriage returns, representing entire paragraphs as a single line. This plugin aims to intelligently apply appropriate Neovim settings (like `textwidth` and `wrap`/`nowrap`) to make editing these files feel more natural. While Neovim's core functionality provides the basic building blocks for soft wrapping, `wrapping.nvim` offers a layer of automation and potentially more nuanced handling of different wrapping styles 1. However, it's worth noting that some users have found that the base soft wrapping functionality in Neovim itself might be sufficient and that plugins like `wrapping.nvim` could potentially overwrite user-defined settings 1.

**3.2 Installation and Setup**

To use `wrapping.nvim`, it needs to be installed using a Neovim plugin manager such as Lazy or Packer. Assuming the use of Lazy, the plugin can be added to the `pluginspec` in the `init.lua` file:

Lua

```lua
{
    "andrewferrier/wrapping.nvim",
    config = function()
        require("wrapping").setup()
    end,
}
```

The `require("wrapping").setup()` line initializes the plugin with its default settings.

**3.3 Key Configuration Options for Markdown**

`wrapping.nvim` provides several configuration options that can be customized through the `setup()` function. One particularly relevant option for Markdown files is `softener` 3. This option influences how the plugin detects whether a file uses soft or hard line wrapping. By default, the `softener` value is set to `1.0` for all file types. Increasing this value for Markdown files makes it more likely that the plugin will detect them as having soft line wrapping. For example, to set the `softener` value to `1.3` specifically for Markdown files, the configuration would be:

Lua

```lua
require("wrapping").setup({
    softener = { markdown = 1.3 },
})
```

Alternatively, the `softener` value can be set to `true` to always treat Markdown files as having soft line endings or `false` to always treat them as having hard line endings 3. For users who prefer to have explicit control over the wrapping mode and disable the plugin's automatic detection, the `auto_set_mode_heuristically` option can be set to `false` 3.

**3.4 Using Commands and Key Mappings**

`wrapping.nvim` provides default commands and key mappings to manually switch between hard and soft wrapping modes 3. The default commands are `HardWrapMode`, `SoftWrapMode`, and `ToggleWrapMode`. The corresponding normal-mode key mappings are `[ow` for soft wrap mode, `]ow` for hard wrap mode, and `yow` to toggle between the two. These commands and key mappings can be used if the plugin's automatic detection does not behave as expected or if the user wants to manually control the wrapping mode for specific Markdown files.

**4. Formatting Existing Markdown Files**

As mentioned earlier, simply setting the `textwidth` option might not affect existing long lines in Markdown files. To apply the desired line length to such content, Neovim provides the `gq` command.

**4.1 The `gq` Command: Reformatting Text**

The `gq` command in Neovim is an operator that formats the text within a specified motion or text object according to the currently set formatting options, including `textwidth` 2. To reformat the entire Markdown file, the command `ggVGgq` can be used 9. `gg` moves the cursor to the beginning of the file, `VG` selects the entire file in visual line mode, and `gq` then formats the selected text. Alternatively, to format a paragraph, the cursor can be placed anywhere within the paragraph, and the command `}` followed by `gq` will format the current paragraph and the ones below until the next blank line 2. Similarly, `{` followed by `gq` will format the current paragraph and the ones above. For a more targeted approach, the command `V}gq` can be used to visually select a paragraph (using `}`) and then format it 13. It is crucial to understand that the `gq` command inserts hard line breaks into the text to enforce the `textwidth` 9. While this effectively makes the text visually wrap at the desired length, it alters the underlying Markdown content, which the user specifically wants to avoid for compatibility with Obsidian. Therefore, while `gq` is useful for initially formatting existing files, it might not be the ideal solution for ongoing editing if the goal is to maintain Markdown files without hard-coded line breaks.

**4.2 Considering Prettier with `prose-wrap`**

Prettier is a popular code formatter that also supports Markdown formatting 9. When integrated with Neovim (e.g., using the `prettier/vim-prettier` plugin), it can automatically format Markdown files upon saving or through a specific command 9. Prettier offers a `prose-wrap` option that specifically controls how prose within Markdown documents is wrapped 9. This option can be configured to wrap prose to a defined print width, which can be set to a value like 80 characters. To use Prettier with `prose-wrap`, the `prettier/vim-prettier` plugin would need to be installed and configured in the Neovim setup. For example, in a Lazy configuration:

Lua

```lua
{
    "prettier/vim-prettier",
    ft = { "markdown" },
    init = function()
        vim.g["prettier#autoformat"] = 1
        vim.g["prettier#autoformat_require_pragma"] = 0
    end,
}
```

And a `.prettierrc.yaml` file in the project root (or a parent directory) with the following content:

YAML

```lua
proseWrap: always
printWidth: 80
```

Similar to the `gq` command, Prettier will insert hard line breaks to enforce its formatting rules, which might not align with the user's preference for soft wrapping to maintain Obsidian compatibility 9. However, for users who prioritize consistent formatting and are less concerned about the hard line breaks, Prettier can be a powerful tool.

**5. Addressing Potential Issues and Considerations**

While implementing soft wrapping in Neovim for Markdown files, several potential issues and considerations should be kept in mind.

**5.1 Conflicts with Other Markdown Plugins**

Some Neovim plugins designed for Markdown editing might rely on specific line lengths or character positions. For example, a plugin that renders images within the Neovim buffer might have issues if long lines are wrapped, potentially causing overlaps or incorrect display 14. If such conflicts arise, it might be necessary to adjust the configuration of either the wrapping settings or the conflicting plugin. Testing the interaction between different Markdown-related plugins after enabling soft wrapping is recommended.

**5.2 Consistency Between Editing and Rendering**

Maintaining a consistent visual line length, ideally around 80 characters, is beneficial for both the editing experience in Neovim and the rendered output in Obsidian or other Markdown processors 9. While soft wrapping in Neovim addresses the editing view, Obsidian's rendering will also respect any hard line breaks present in the file. If the goal is to have a visually similar experience in both editors without introducing hard breaks, relying solely on Neovim's `wrap` and `textwidth` options is the most direct approach. Markdown renderers typically treat single line breaks as spaces, so paragraphs written with soft wrapping in Neovim will generally render as expected in Obsidian 15.

**5.3 Centring Text (Secondary Consideration)**

The user mentioned that Obsidian's readability setting also centers the text. Neovim's core `wrap` and `textwidth` options primarily focus on line wrapping and do not directly provide a feature for centering the entire text block within the editor window 2. While Neovim offers commands like `:center` to centre a range of lines 2, this is typically used for specific formatting purposes rather than the overall display of a document. There might be more advanced configurations or plugins that could potentially influence the positioning of the text within the window, but these would likely be more involved than simply enabling soft wrapping. For instance, some users might explore custom statusline configurations or window management techniques to achieve a visually centered effect, but these are outside the scope of standard soft wrapping configurations. The `zz` command in Neovim can center the current line on the screen 19, which might offer some improvement in focus, but it does not center the entire text block like Obsidian's readability setting.

**6. Practical Configuration Examples**

Here are practical examples of how to configure Neovim for Obsidian-like soft wrapping in Markdown files.

**6.1 Basic Configuration using Neovim Options**

Using an autocommand in the `init.lua` file:

Lua

```lua
vim.api.nvim_create_autocmd("FileType", {
    pattern = {"markdown"},
    callback = function()
        vim.opt_local.wrap = true
        vim.opt_local.textwidth = 80
    end,
})
```

Alternatively, creating a file `~/.config/nvim/after/ftplugin/markdown.lua` with the following content:

Lua

```lua
vim.opt_local.wrap = true
vim.opt_local.textwidth = 80
```

**7. Conclusion: Achieving Seamless Markdown Editing**

Achieving Obsidian-like soft wrapping in Neovim for Markdown files is readily possible by leveraging Neovim's built-in `wrap` and `textwidth` options. By enabling the `wrap` option, long lines will be visually broken to fit within the editor window, and by setting the `textwidth` option to a reasonable value, such as 80 characters, the width of these visual lines can be controlled for improved readability. Configuring these options specifically for the Markdown filetype ensures that other file types in Neovim are not affected.

While plugins like `wrapping.nvim` offer more advanced features for managing wrapping modes, the core functionality provided by Neovim's options is often sufficient for replicating the desired soft wrapping behavior. It is important to note the distinction between soft wrapping, which affects only the visual display, and hard line breaks, which alter the file content. For maintaining compatibility with Obsidian and ensuring that Markdown files are rendered as intended in both applications, relying on soft wrapping through the `wrap` and `textwidth` options is the recommended approach. Users who need to format existing Markdown files with long lines should be aware that commands like `gq` and formatters like Prettier introduce hard line breaks. Therefore, for ongoing editing with the goal of Obsidian compatibility, the focus should be on configuring Neovim to soft wrap new and existing content without altering the underlying line structure. By implementing the configurations outlined in this report, users can significantly enhance the readability of Markdown files in Neovim and achieve a more consistent editing experience with Obsidian.
