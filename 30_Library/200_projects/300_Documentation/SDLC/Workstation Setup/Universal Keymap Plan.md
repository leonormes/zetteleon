---
aliases: []
confidence: 
created: 2025-03-20T12:08:25Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:50Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [keymap, workstation]
title: Universal Keymap Plan
type: plan
uid: 
updated: 
version: 
---

[[keymaps]]

## 1. Core Concepts

- **Leader Key:** Space ( )
- **Modifier Keys:** Ctrl, Shift, Alt (where applicable and consistent)
- **Namespace Structure:** `<Leader> <Namespace> <Action>`
- **Goal:** Consistent and efficient keybindings across WezTerm, Zellij, and Neovim, minimizing conflicts and maximizing muscle memory.
- **Guiding Principles:**
    - **Ergonomics:** Prioritize comfortable key combinations.
    - **Mnemonics:** Use intuitive key mappings (e.g., `s` for search).
    - **Consistency:** Maintain similar patterns across applications.
    - **Extensibility:** Design the system to accommodate future additions.
    - **Discoverability:** (Less of a keymap thing, but important) Consider how you will *learn* and remember these. Maybe a cheat sheet plugin.

## 2. Considerations for Each Application

### 2.1. WezTerm

- Terminal emulator: Focus on window/tab management, launching programs, and general terminal behavior.
- Keybinding limitations: WezTerm has its own keybinding system, so ensure compatibility.
- Modifier keys: Ctrl, Shift, and Alt are commonly used.

### 2.2. Zellij

- Terminal multiplexer: Focus on pane management, sessions, and layouts
- Keybinding challenges: Zellij has a modal system and its own set of default keybindings, which may conflict with Neovim. Careful planning is needed to avoid clashes (see "Zellij Integration" below)
- Modifier keys: Ctrl and Alt are primarily used by Zellij.

### 2.3. Neovim

- Text editor: Focus on editing, navigation, and plugin-specific actions.
- Leader key: Neovim has a built-in leader key concept, making it ideal for namespaced keybindings.
- Modifier keys: Ctrl, Shift, and Alt are used extensively in Neovim.

## 3. Leader Key Namespace Overview

This section provides a high-level overview of the keymap structure. Namespaces are organized by function.

- **Space + c:** Code
- **Space + d:** Debugging
- **Space + e:** Editing
- **Space + f:** File/Find
- **Space + g:** Git
- **Space + h:** Help
- **Space + l:** LSP (Language Server Protocol)
- **Space + m:** Marks/Movement
- **Space + n:** Neovim (Specific commands or plugin access)
- **Space + o:** Options
- **Space + p:** Project/Panes
- **Space + q:** Quit/Close
- **Space + r:** Replace/Refactor
- **Space + s:** Search/Substitute
- **Space + t:** Terminal/Tabs
- **Space + u:** UI (Appearance)
- **Space + v:** Version control (Generic)
- **Space + w:** Window
- **Space + x:** Exit/Close (Alternative to q)
- **Space + z:** Zellij (Specific commands)

## 4. Namespace Details

This section details the specific keybindings within each namespace. It's organized by namespace, then by action. I've added more detail and examples, and tried to make it more consistent.

### 4.1. Code (Space + c)

- **Space + c + f:** Format code (e.g., `:%!clang-format` in Neovim, or a dedicated formatter)
- **Space + c + r:** Run code (e.g., `:!python %` in Neovim, or a build system command)
- **Space + c + b:** Build code (e.g., `:make` in Neovim, or a build tool like `make` or `cargo`)
- **Space + c + t:** Run tests (e.g., `:!pytest` in Neovim, or a test runner)
- **Space + c + d:** Debug code (e.g., launch a debugger in Neovim, or in a separate terminal)
- **Space + c + c:** Code completion (Trigger completion)
- **Space + c + a:** Code action / Quick fix

### 4.2. Debugging (Space + d)

- **Space + d + b:** Set breakpoint
- **Space + d + c:** Continue execution
- **Space + d + s:** Step into
- **Space + d + o:** Step over
- **Space + d + u:** Step out
- **Space + d + r:** Restart debug session
- **Space + d + t:** Toggle breakpoint

### 4.3. Editing (Space + e)

- **Space + e + c:** Comment/Uncomment
- **Space + e + d:** Duplicate line
- **Space + e + m:** Move line up/down
- **Space + e + j:** Join lines
- **Space + e + s:** Split line
- **Space + e + t:** Trim trailing whitespace

### 4.4. File/Find (Space + f)

- **Space + f + f:** Find file (e.g., `:Telescope find_files` in Neovim, or a file manager)
- **Space + f + s:** Save file (e.g., `:w` in Neovim, Ctrl+S in many applications)
- **Space + f + a:** Save all files
- **Space + f + d:** Delete file (Careful with this one! May need confirmation)
- **Space + f + r:** Rename file (e.g., `:!mv % <new_name>` in Neovim, or a file manager)
- **Space + f + n:** New file
- **Space + f + o:** Open file

### 4.5. Git (Space + g)

- **Space + g + s:** Git status (e.g., `:!git status` in Neovim, or a Git client)
- **Space + g + c:** Git commit (e.g., `:!git commit` in Neovim, or a Git client)
- **Space + g + p:** Git push (e.g., `:!git push` in Neovim, or a Git client)
- **Space + g + l:** Git log (e.g., `:!git log` in Neovim, or a Git client)
- **Space + g + b:** Git branch (e.g., `:!git branch` in Neovim, or a Git client)
- **Space + g + d:** Git diff
- **Space + g + a:** Git add

### 4.6. Help (Space + h)

- **Space + h + h:** Help (General help)
- **Space + h + k:** Show keybindings (custom keybindings)
- **Space + h + s:** Search help
- **Space + h + t:** Toggle table of contents

### 4.7. LSP (Space + l)

- **Space + l + d:** Go to definition
- **Space + l + r:** Rename symbol
- **Space + l + f:** Format code (LSP)
- **Space + l + a:** Code action
- **Space + l + h:** Show hover information

### 4.8. Marks/Movement (Space + m)

- **Space + m + s:** Set mark
- **Space + m + g:** Go to mark
- **Space + m + c:** Clear mark
- **Space + m + n:** Next mark
- **Space + m + p:** Previous mark

### 4.9. Neovim (Space + n)

- **Space + n + t:** Toggle terminal inside Neovim (e.g., `:ToggleTerm` if you use a plugin)
- **Space + n + l:** Toggle location list (e.g., `:lopen` / `:lclose`)
- **Space + n + q:** Quit Neovim (:qa!)
- **Space + n + v:** Edit Neovim config
- **Space + n + r:** Reload Neovim config

### 4.10. Options (Space + o)

- **Space + o + l:** Line numbers (Toggle)
- **Space + o + r:** Relative line numbers (Toggle)
- **Space + o + w:** Wrap lines (Toggle)
- **Space + o + t:** Theme (Change theme)
- **Space + o + s:** Show/Hide status line

### 4.11. Project/Panes (Space + p)

- **Space + p + n:** New pane
- **Space + p + s:** Split pane horizontally
- **Space + p + v:** Split pane vertically
- **Space + p + h:** Focus left pane
- **Space + p + l:** Focus right pane
- **Space + p + j:** Focus down pane
- **Space + p + k:** Focus up pane
- **Space + p + c:** Close pane
- **Space + p + t:** Project search (e.g., Telescope)

### 4.12. Quit/Close (Space + q)

- **Space + q + q:** Quit current application (e.g., `:qa!` in Neovim, `exit` in terminal)
- **Space + q + w:** Close current window
- **Space + q + s:** Save and quit

### 4.13. Replace/Refactor (Space + r)

- **Space + r + r:** Rename (Refactor)
- **Space + r + i:** Inline
- **Space + r + e:** Extract
- **Space + r + v:** Move file

### 4.14. Search/Substitute (Space + s)

- **Space + s + f:** Find in files (e.g., `:Grep` in Neovim, or a global search tool)
- **Space + s + w:** Find word under cursor (e.g., `*` or `#` in Neovim)
- **Space + s + g:** Grep (e.g., `:!grep -r ...` in Neovim)
- **Space + s + h:** Search history (terminal, command)
- **Space + s + s:** Substitute (e.g., `:%s/foo/bar/g` in Neovim)

### 4.15. Terminal/Tabs (Space + t)

- **Space + t + n:** New terminal/tab
- **Space + t + r:** Rename terminal/tab
- **Space + t + s:** Switch terminal/tab
- **Space + t + k:** Kill terminal/tab
- **Space + t + h:** Previous tab
- **Space + t + l:** Next tab

### 4.16. UI (Space + u)

- **Space + u + t:** Toggle theme
- **Space + u + f:** Toggle full-screen
- **Space + u + s:** Toggle status bar
- **Space + u + m:** Toggle menu bar

### 4.17. Version Control (Space + v)

- **Space + v + d:** Diff
- **Space + v + h:** History
- **Space + v + u:** Update
- **Space + v + c:** Commit

### 4.18. Window (Space + w)

- **Space + w + s:** Split window horizontally
- **Space + w + v:** Split window vertically
- **Space + w + h:** Move to left window
- **Space + w + l:** Move to right window
- **Space + w + j:** Move to down window
- **Space + w + k:** Move to up window
- **Space + w + c:** Close window
- **Space + w + f:** Toggle fullscreen

### 4.19. Exit/Close (Space + x)

- **Space + x + q:** Quit
- **Space + x + c:** Close

### 4.20. Zellij (Space + z)

- **Space + z + n:** New Zellij pane
- **Space + z + s:** Switch Zellij panes
- **Space + z + f:** Fullscreen Zellij pane
- **Space + z + q:** Quit Zellij session
- **Space + z + t:** New tab in zellij
- **Space + z + a:** Attach/Detach

## 5. Zellij Integration

Zellij's default keybindings can conflict with Neovim's. Here are a few strategies:

- **Zellij's Tmux Mode:** Zellij has a "tmux mode" which can help avoid conflicts. You can switch to tmux mode, which changes how Zellij interprets key presses.
- **Remap Zellij's Leader:** Change Zellij's modifier key (the equivalent of tmux's `Ctrl+b`) to something else (e.g., `Alt+z` or `Ctrl+Space`). This frees up Ctrl for Neovim.
- **Clear Zellij Keybindings:** You can clear Zellij's default keybindings in certain modes and define your own, ensuring no overlap with Neovim. This gives you the most control but requires more configuration.
- **WezTerm SendKey:** In some cases, you might be able to use WezTerm's `send_key` action to send specific key combinations to Zellij or Neovim, bypassing conflicts. This is more advanced.

**Example: Remapping Zellij's Leader Key**

In your Zellij configuration file, you might remap the leader key like this (check Zellij's documentation for the exact syntax):

```sh
keybinds {
    normal {
        unbind "Ctrl b"
        bind "Alt z" { SwitchToMode "Tmux"; }
    }
}
```

Then, in Tmux mode, you define your Zellij bindings.

## 6. WezTerm Configuration

WezTerm's configuration is done in Lua. You'll need to translate the keybindings from this plan into WezTerm's configuration syntax. Here's a basic example:

```sh
-- ~/.config/wezterm/wezterm.lua
local wezterm = require 'wezterm'

return {
    -- Example:  Space + t + n for new tab
    keys = {
        {
            key = 'n',
            mods = 'SUPER',  --  Use Super key as an example
            action = wezterm.action.SpawnTab {
                spawn = { 'bash' }  -- Or your shell
            },
        },
        -- More keybindings here...
    },
}
```

- `key`: The key to bind.
- `mods`: The modifier keys (e.g., 'CTRL', 'SHIFT', 'ALT', 'SUPER'). WezTerm uses strings for these.
- `action`: The action to perform (see WezTerm's documentation for available actions).

**Important Notes:**

- **Consistency is Key:** The goal is to make these keybindings as consistent as possible across all three applications. This will take time and refinement.
- **Testing:** Test your keybindings thoroughly in each application after you configure them.
- **Documentation:** Keep this document updated as you change your keybindings. This will help you remember them and keep things organized.
- **Start Simple:** Begin with a small set of essential keybindings and gradually add more as you become comfortable with them.
- **Version Control:** Store your configuration files (WezTerm, Zellij, Neovim) in version control (e.g., Git). This will allow you to track changes, revert to previous versions, and easily sync your configuration across multiple machines.
