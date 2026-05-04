# quick look

Yes, you can enable Markdown file previews in Finder on macOS using a Quick Look plugin. By default, Finder doesn't natively support Markdown previews, but with a simple third-party plugin, you can enable it.

Here’s how you can do it:

Option 1: Use QLMarkdown

1. Download the QLMarkdown Quick Look plugin from GitHub.

2. Follow the installation instructions provided in the repository:

Run the following command in Terminal to install the plugin via Homebrew:

brew install qlmarkdown

Alternatively, you can manually download the plugin and move it to \~/Library/QuickLook.

1. Once installed, refresh Quick Look by running:

qlmanage -r

1. Now, when you select a .md file in Finder and press Space (Quick Look), it should show a preview of the file's content.

Option 2: Use QLstephen

This plugin allows previews for text files without extensions or with uncommon extensions (like README or markdown files):

1. Install QLstephen by running:

brew install qlstephen

1. Follow the same steps to refresh Quick Look.

Both of these plugins should allow you to preview Markdown files directly in Finder.

Yes, there are several Finder plugins, especially for enhancing Quick Look functionality on macOS. These plugins allow Finder to preview different types of files that aren't supported natively. Here are some popular Quick Look plugins:

1. QLImageSize

Purpose: Displays the dimensions of image files in the Quick Look preview.

Installation:

brew install qlimagesize

Usage: Shows image dimensions when previewing images (JPEG, PNG, etc.).

1. QLVideo

Purpose: Extends Quick Look support for video formats not natively supported (like MKV, AVI, and FLV).

Installation:

brew install qlvideo

Usage: Previews these video formats directly in Finder with Quick Look.

1. QuickLookJSON

Purpose: Allows you to preview JSON files with syntax highlighting and formatting.

Installation:

brew install quicklook-json

Usage: Quick Look now shows pretty-printed JSON files.

1. QLColorCode

Purpose: Enables syntax highlighting for source code files (HTML, CSS, JavaScript, Python, Ruby, etc.).

Installation:

brew install qlcolorcode

Usage: See highlighted code in various file formats in Quick Look.

1. Suspicious Package

Purpose: Allows you to inspect the contents of macOS installer .pkg files.

Installation: Download from here.

Usage: Provides details about the files and scripts within .pkg files.

1. QLPrettyPatch

Purpose: Allows previewing patch files with color formatting.

Installation:

brew install qlprettypatch

Usage: Provides a better visual representation for .patch and .diff files.

1. QLStephen

Purpose: Previews plain text files without extensions (such as README files or other extensionless documents).

Installation:

brew install qlstephen

Usage: Shows the content of plain text files without extensions in Quick Look.

1. WebPQuickLook

Purpose: Adds Quick Look support for WebP image files.

Installation:

brew install webpquicklook

Usage: Preview .webp images in Finder.

1. QuickLookCSV

Purpose: Provides a preview for CSV files formatted in a readable table format.

Installation:

brew install quicklook-csv

Usage: Quick Look now shows CSV files as properly formatted tables.

1. EPUBQuickLook

Purpose: Allows previewing EPUB files (eBooks) within Finder.

Installation:

brew install epubquicklook

Usage: See a preview of .epub eBooks in Quick Look.

How to Install These Plugins:

Homebrew: You can install most of these plugins via Homebrew, a package manager for macOS. The installation commands are provided above for each plugin.

Manually: Some plugins are available for manual download. You would typically place them in \~/Library/QuickLook and then run:

qlmanage -r

These plugins can greatly extend the functionality of Finder, making it easier to preview and work with various file types directly from the file explorer.

Yes, there are several tools and plugins that can help improve keyboard control over Finder on macOS. While Finder itself has some built-in keyboard shortcuts, you can use third-party tools to enhance and customize the keyboard navigation experience further.

Here are some options:

1. BetterTouchTool

Purpose: Although primarily known for customizing trackpad and mouse gestures, BetterTouchTool also allows you to create custom keyboard shortcuts for Finder and many other apps.

Features:

Customize Finder navigation and commands with custom shortcuts.

Assign keyboard shortcuts to specific actions like opening a new Finder window, creating new folders, moving between panes, etc.

Installation: Download from the official website.

Usage: Set up specific shortcuts in Finder to streamline file management tasks.

1. Keyboard Maestro

Purpose: A powerful automation tool that allows you to create custom keyboard shortcuts and automate tasks in Finder and other macOS applications.

Features:

Automate repetitive tasks in Finder.

Create keyboard shortcuts for file management, navigation, and even multi-step workflows.

Create macros to manipulate Finder windows, open folders, search, or move/copy files.

Installation: Available from the official website.

Usage: Build custom macros to control Finder with specific key combinations.

1. Path Finder

Purpose: A Finder replacement with many advanced features, including extensive keyboard control.

Features:

Offers better keyboard navigation and shortcuts than the default Finder.

Keyboard shortcuts for all major actions (file management, navigation, viewing, etc.).

Dual-pane browsing and other power features that can be controlled via the keyboard.

Installation: Available from the official website.

Usage: Install Path Finder as a replacement or supplement to Finder for more control with keyboard shortcuts.

1. XtraFinder

Purpose: An enhancement to Finder that adds extra features and more keyboard shortcuts.

Features:

Adds dual-pane browsing to Finder.

Provides more file manipulation options with keyboard shortcuts (like cut/paste, show/hide hidden files, etc.).

Allows customizable keyboard shortcuts for various actions.

Installation: Download from here.

Usage: Use it to improve your Finder experience with keyboard-focused controls.

1. Alfred

Purpose: A powerful productivity app that extends macOS's built-in Spotlight. You can use Alfred to navigate Finder with custom workflows and keyboard shortcuts.

Features:

Create workflows to control Finder and automate file management.

Use keyboard shortcuts to open specific folders or files.

Quickly search for files and directories using just the keyboard.

Installation: Available from the official website.

Usage: Set up Finder workflows and custom shortcuts to navigate and manage files efficiently.

1. Hammerspoon

Purpose: A powerful macOS automation tool that uses Lua scripting to automate Finder (and other app) controls via the keyboard.

Features:

Create custom keyboard shortcuts to control Finder, such as moving or renaming files.

Use Lua scripting to extend Finder’s functionality and add features like advanced navigation or file management tasks.

Installation: Download from the official website.

Usage: Requires some Lua scripting knowledge to customize Finder controls, but it offers unparalleled flexibility.

1. Default macOS Keyboard Shortcuts

macOS Finder already has several built-in keyboard shortcuts. Here are some common ones:

Cmd + N: Open a new Finder window.

Cmd + Shift + N: Create a new folder.

Cmd + I: Get information about the selected item.

Cmd + C, Cmd + V: Copy and paste files.

Cmd + Option + V: Move (cut and paste) files.

Cmd + Delete: Move items to Trash.

Cmd + Shift + G: Open “Go to Folder” dialog.

Tab: Move between Finder elements (sidebar, file list, etc.).

Enhancing Finder Keyboard Usage with System Preferences

1. Mission Control

Assign a hotkey to open Finder windows using Mission Control, like setting up a shortcut to quickly navigate to Finder.

1. System Preferences > Keyboard > Shortcuts

You can customize the built-in macOS keyboard shortcuts here, including Finder-specific actions.

By using these tools, plugins, and shortcuts, you can significantly enhance your control over Finder via the keyboard and streamline your file management workflows.

Centralizing keybindings across multiple terminal apps and system tools can significantly streamline your workflow and make your keyboard-focused productivity more efficient. Here are a few strategies and approaches clever users employ to centralize and manage keybindings across different tools:

1. Use a Universal Tool for Keybinding Management

Keyboard Maestro or Karabiner-Elements can act as a central hub for all keybindings:

Karabiner-Elements: A powerful keyboard remapping tool for macOS. You can create profiles and remap keys globally or for specific apps. It's useful for unifying keybinding behavior across all apps, including terminal apps.

How to Use: Set up layers or keybinding profiles for different contexts (e.g., terminal, Raycast, nvim). Use condition-based rules to switch mappings dynamically.

Example: Map Ctrl + J for switching panes in both Zellij and Wezterm, while having Ctrl + K for switching windows in Raycast.

Keyboard Maestro: You can use it to create macros and map complex key sequences globally. These macros can work across different apps or specific apps.

1. Centralize with an Application-Specific Keybinding File

Some users create a single configuration file for their keybindings. For example, they might store all their shortcuts in a dotfile (e.g., .keybindings) and then source this file in different applications.

Neovim: Use Lua or Vimscript to define keybindings and mappings, which can then be dynamically applied based on the active application or context.

Wezterm: The .wezterm.lua file can pull from your centralized keybinding dotfile.

Raycast: Raycast has its own keyboard shortcuts editor, but you can try to align these with your terminal shortcuts.

Example: Store common bindings in a centralized file, and source this file across Wezterm, Zellij, and nvim to unify keybindings.

1. Adopt a Layered Approach to Keybindings

Space or Leader Key Approach: This is popular with Vim and Neovim users. You define a "leader key" that acts as a prefix for other mappings. You can then use the same leader-based shortcuts across different tools (e.g., Space + f for finding files).

Example: Use Space as your leader key in Neovim for navigation, Alt + Space for the same function in Zellij, and Ctrl + Space in Raycast.

This consistency helps you move between different tools without having to remember different mappings.

1. Consistent Modifier Keys Across Tools

Use the same modifiers across all tools for similar tasks. For instance:

Use Ctrl for navigation (e.g., moving between panes, windows).

Use Alt for system-level shortcuts (e.g., launching apps or switching between contexts).

Use Cmd (if on macOS) for actions specific to the current tool (e.g., search in Neovim, Zellij tab creation).

1. Use a Keybinding Mapper/Daemon

sxhkd (Simple X Hotkey Daemon): This tool is popular in tiling window manager setups on Linux (like bspwm). You can use sxhkd to define global keybindings that work across multiple applications.

You could implement a similar idea using tools like Hammerspoon on macOS, which allows custom Lua-based automation.

Example: Create keybinding actions that trigger scripts or commands across multiple apps (like navigating between tmux panes, Zellij panes, and Neovim splits) from one consistent keymap.

1. Automate Keybinding Synchronization

Use a git repository to manage your dotfiles and keybindings. This ensures that changes made to your keybindings are synchronized across different machines or environments.

Dotfiles Example: Store all terminal and editor config files (Wezterm, Zellij, Neovim, etc.) in a GitHub repo. This way, you can clone and push changes from one place.

Example Repo: Your .dotfiles could include a .keybindings file that can be sourced by Neovim, Wezterm, and even Zellij config files. This ensures consistency when switching machines.

1. Use Context-Aware Tools

Raycast: With Raycast, you can use custom scripts to centralize actions and keybindings. You could use it to trigger tasks across your terminal apps, like opening new tabs in Wezterm or sending specific commands to Zellij.

Hammerspoon: On macOS, you can create conditional keybindings that change based on the active application or window context. You could set different keybindings depending on whether you're in a terminal, Neovim, or another app.

1. Standardize Keybindings Across Tools

Create a standard mnemonic system for your mappings. For example:

Ctrl + H/J/K/L: Always for pane navigation in terminal apps (Wezterm, Zellij) and Neovim splits.

Space + f: Always for opening files in all tools (Neovim, Raycast, Zellij, etc.).

Alt + n: Always for creating a new file or tab in any application.

1. Use Terminal Multiplexers (tmux or Zellij)

Many people use tmux to centralize pane and window management within the terminal. Since you use Zellij, you can follow a similar strategy:

Zellij can serve as the primary pane management tool, allowing you to navigate between terminal sessions using keyboard shortcuts, while your applications (like Neovim) inside it use consistent keybindings.

You can map the same keybindings (Ctrl + arrow keys for pane navigation, for instance) in Zellij and Neovim to create a unified experience across panes and splits.

1. Multi-layered Workflow

Some advanced users opt for workspaces (like in Zellij or Tmux) where each context has a specific set of shortcuts. For example, your "coding workspace" in Zellij would have keybindings for navigating Neovim, while your "system workspace" would map similar shortcuts for navigating system tools like htop or Wezterm tabs.

Key Takeaways:

1. Unify across tools: Centralize as much as possible using tools like Karabiner-Elements, Keyboard Maestro, or even a custom .keybindings file sourced across your dotfiles.

2. Standardize keybinding themes: Use consistent mappings across apps. This reduces cognitive load.

3. Utilize leader/space key: Create a central keybinding hub with the leader/space key for different apps.

4. Automation with Raycast and Hammerspoon: Use these tools for smart workflows that trigger actions across apps.

5. Git sync: Version-control your keybindings and sync them across devices.

Would you like more specific examples or configurations for any of the tools?

Combining Raycast and Hammerspoon can be a powerful way to centralize keybindings and automate workflows on macOS. Here’s an example of how you can use these two tools together to streamline tasks.

Example: Centralized Keybinding for Terminal and App Automation

Goal

Use a single keybinding in Raycast that triggers an action in Hammerspoon to:

Open a terminal (Wezterm, iTerm, etc.) and run a command.

Focus a specific window or application.

Execute custom Lua code to perform window management.

Step 1: Create a Raycast Script Command

1. Install the Raycast Script Command Template:

Raycast allows you to run custom shell scripts via a script command. You can trigger this with a specific keybinding in Raycast.

Open Raycast → Go to Preferences → Extensions → Create New Script Command.

1. Create a Shell Script that calls a Hammerspoon function using its hs CLI tool:

\#!/bin/bash

# Call Hammerspoon function through the command line

hs -c "focusAndRunTerminal()"

Save this script with an appropriate name (e.g., [focus-terminal.sh](http://focus-terminal.sh)) in your Raycast Script Commands directory (\~/.config/raycast/scripts/).

1. Assign a Raycast Hotkey:

In Raycast → Preferences → Extensions → Select your script.

Assign a global hotkey, e.g., Ctrl + Alt + T, that will trigger this script command.

Step 2: Define a Hammerspoon Function

1. Enable the Hammerspoon CLI:

Open Hammerspoon → Go to the menubar → Preferences → Check the Enable CLI option. This will allow you to use the hs command from the terminal.

1. Add a Lua function in Hammerspoon’s configuration file (\~/.hammerspoon/init.lua):

\-- Function to focus the terminal (Wezterm or iTerm) and run a command
function focusAndRunTerminal()
\-- Focus or launch the terminal (Wezterm in this case)
local weztermApp = hs.application.find("Wezterm") or hs.application.launchOrFocus("Wezterm")

    -- Wait until the app is fully focused before sending the command
hs.timer.doAfter(0.2, function()
\-- Bring the terminal to the front and send a custom command
hs.eventtap.keyStrokes("ls -la\\n")  -- Example command: list directory
end)
end

This Lua script checks if Wezterm is running; if not, it launches it. Once Wezterm is in focus, it sends a terminal command (in this case, ls -la) via keystrokes.

1. Reload Hammerspoon:

After saving your changes, reload Hammerspoon by clicking the Reload Config button in the menu bar or using the default hotkey Ctrl + Alt + Cmd + R.

Step 3: Test the Setup

Press the global hotkey you assigned in Raycast (Ctrl + Alt + T).

Raycast will execute the shell script, which invokes Hammerspoon.

Hammerspoon will focus or launch Wezterm and automatically run the command ls -la.

Customization and Extensions

1. Window Management with Hammerspoon

You can extend this by adding more complex window management logic within Hammerspoon. For instance, you can move Wezterm to a specific part of the screen:

function focusAndRunTerminal()
local weztermApp = hs.application.find("Wezterm") or hs.application.launchOrFocus("Wezterm")

    hs.timer.doAfter(0.2, function()
\-- Move Wezterm to the left half of the screen
local win = weztermApp:mainWindow()
win:moveToUnit(hs.layout.left50)

        -- Send a command to Wezterm
hs.eventtap.keyStrokes("top\\n")  -- Run the `top` command
end)
end

1. Chain Other Applications in Raycast

You can also extend this to launch multiple apps at once via Hammerspoon, such as opening Wezterm and your code editor (e.g., Neovim in a terminal or VSCode):

function launchDevEnvironment()
\-- Launch or focus Wezterm
local weztermApp = hs.application.find("Wezterm") or hs.application.launchOrFocus("Wezterm")

    -- Wait until Wezterm is active
hs.timer.doAfter(0.2, function()
hs.eventtap.keyStrokes("nvim\\n")  -- Start Neovim in terminal
end)

    -- Launch or focus VSCode
hs.application.launchOrFocus("Visual Studio Code")
end

Then modify your Raycast script to call this function:

\#!/bin/bash
hs -c "launchDevEnvironment()"

Benefits of Using Raycast and Hammerspoon Together:

1. Centralized control: Raycast becomes the frontend with global hotkeys, while Hammerspoon handles the logic for controlling applications.

2. Extensibility: You can extend the Hammerspoon Lua script to do things like window tiling, automating repetitive workflows, or even moving files between apps.

3. Custom workflows: Raycast workflows, combined with Hammerspoon's automation, allow you to create unique setups suited to your specific productivity needs.

Would you like help with further customization or adding more complex logic?

It's a great goal to centralize your keybindings for a more consistent and efficient workflow! Here's a breakdown of how people achieve this, along with some advanced techniques:

1. Configuration Files:

- Identify Central Locations: Most terminal apps use configuration files (often in your home directory).  For example:

   - WezTerm: \~/.config/wezterm/wezterm.lua

   - Zellij: \~/.config/zellij/config.kdl

   - Neovim: \~/.config/nvim/init.vim (or init.lua)

   - Raycast:  Raycast uses extensions with their own config, but you can often script actions.

- Create a Shared File:  Consider creating a separate file (e.g., \~/.config/my_keybindings.lua or .conf) where you define your preferred mappings. Then, source this file within your WezTerm, Zellij, and Neovim configurations.

1. Scripting and Automation:

- Shell Scripts: Use shell scripts to define complex keybindings that involve multiple commands or actions. You can then map these scripts to keys within your terminal applications.

- Dedicated Keybinding Daemons:  Tools like sxhkd (Simple X Hotkey Daemon) or xbindkeys allow you to define system-wide keybindings that work across different X11 applications. You can use these to trigger scripts or send key sequences to your terminal.

1. Advanced Techniques:

- Lua for Cross-Application Consistency:  If you're comfortable with Lua, you can leverage its power for more advanced keybinding management. Define your mappings in Lua and use it to configure WezTerm and Neovim (both have excellent Lua support).

- Symbolic Links:  For simpler scenarios, use symbolic links to share configuration snippets between your different configuration files.

- Git for Version Control: Store your keybinding configuration files in a Git repository. This allows you to track changes, experiment with different setups, and easily revert to previous versions.
   Example (Lua with WezTerm and Neovim):

- \~/.config/my_keybindings.lua:
   local keybindings = {
   \-- Navigation
   { key = "Ctrl+h", action = "move_left" },
   { key = "Ctrl+l", action = "move_right" },
   { key = "Ctrl+j", action = "move_down" },
   { key = "Ctrl+k", action = "move_up" },

  -- Window management
{ key = "Ctrl+Shift+c", action = "close_window" },
{ key = "Ctrl+Shift+n", action = "new_window" },
}

return keybindings

- \~/.config/wezterm/wezterm.lua:
   local my_keybindings = require("my_keybindings")

return {
keys = my_keybindings,
\-- ... other WezTerm config ...
}

- \~/.config/nvim/init.lua:
   local my_keybindings = require("my_keybindings")

for \_, mapping in ipairs(my_keybindings) do
vim.api.nvim_set_keymap("n", mapping.key, mapping.action, { noremap = true })
end

\-- ... other Neovim config ...

Important Considerations:

- Context is Key: Be mindful of how keybindings might conflict between applications or within different modes (e.g., normal mode vs. insert mode in Neovim).

- Ergonomics: Choose keybindings that are comfortable and easy to reach to avoid strain.

- Personalization:  Ultimately, the best approach is the one that best suits your workflow and preferences. Experiment and refine your setup over time.
   By centralizing your keybindings, you'll create a more unified and efficient experience across your terminal environment. Good luck!

I use keybindings in the terminal and terminal apps. Wezterm, zellij and nvim as well as raycast. I want to centralise all my keybindings/ mappings to make it easier to do my work using just the keyboard. What are some ways clever people have gone about this

Centralizing keybindings across multiple terminal applications and tools is a great way to improve productivity and efficiency. Here are some clever approaches that people have used to achieve this:

## Unified Configuration

One approach is to create a unified configuration system that defines keybindings for all your applications in one place:

- Use a configuration management tool like Ansible, Puppet, or Chef to manage and deploy your keybindings across different applications\[1\].

- Create a central YAML or JSON file that defines all your keybindings, then use scripts to generate application-specific config files from this master file.

## Consistent Keybinding Schemes

Develop a consistent keybinding scheme across all your applications:

- Use the same modifier keys (e.g., Ctrl, Alt, Cmd) consistently for similar actions across different apps\[5\].

- Group similar actions under the same key prefix. For example, use "Space" as a leader key in both Neovim and Zellij for window management commands\[1\]\[3\].

## Integration and Interoperability

Look for ways to make your applications work together seamlessly:

- Use plugins like wezterm.nvim to allow seamless navigation between Neovim panes and Wezterm panes using the same keybindings\[2\].

- Configure your terminal multiplexer (Zellij) to pass through certain keybindings to Neovim, avoiding conflicts\[1\].

## Smart Context Switching

Implement context-aware keybindings that change based on the active application:

- Use tools like Hammerspoon (for macOS) or AutoHotkey (for Windows) to create global keybindings that behave differently depending on the active window\[7\].

- Configure your terminal emulator (Wezterm) to detect when you're in a full-screen application like Neovim and adjust keybindings accordingly\[4\].

## Documentation and Cheat Sheets

Create a centralized documentation system for your keybindings:

- Maintain a personal wiki or markdown files in a Git repository with all your keybindings documented.

- Use tools like Raycast to create custom commands that display your keybinding cheat sheets on demand\[6\].

## Gradual Implementation

Implement your centralized keybinding system gradually:

- Start with the most common actions across applications and slowly expand.

- Regularly review and refine your keybindings based on usage patterns\[6\].

## Modular Configuration

Structure your configuration files in a modular way:

- Break down your keybindings into logical groups (e.g., navigation, text manipulation, window management).

- Use separate files for different applications or contexts, but source them from a main configuration file.

By combining these approaches, you can create a powerful, centralized keybinding system that works across Wezterm, Zellij, Neovim, Raycast, and other terminal applications. Remember to regularly review and adjust your keybindings as your workflow evolves, and don't be afraid to experiment with different setups to find what works best for you.

Citations:
\[1\] Zellij ❤️ Neovim | Shoukoo Think Space <https://shoukoo.github.io/blog/zellij-love-neovim/>
\[2\] How I use Wezterm - [mwop.net](http://mwop.net) matthew weier o'phinney <https://mwop.net/blog/2024-07-04-how-i-use-wezterm.html>
\[3\] Of the wezterm and neovim users: what are your keybinds? - Reddit <https://www.reddit.com/r/neovim/comments/1ekzr5x/of_the_wezterm_and_neovim_users_what_are_your/>
\[4\] Mapping CTRL+C in both Wezterm and NVIM #2426 - GitHub <https://github.com/wez/wezterm/discussions/2426>
\[5\] Key Binding - Wez's Terminal Emulator <https://wezfurlong.org/wezterm/config/keys.html>
\[6\] 10 Best Practices for Centralized Encryption Key Management | Thales <https://cpl.thalesgroup.com/blog/encryption/10-best-practices-for-centralized-encryption-key-management>
\[7\] Neovim smart-splits on macOS - Brian Schiller <https://brianschiller.com/blog/2024/07/17/neovim-smart-splits-on-macos/>
\[8\] Mastering key bindings - [stitcher.io](http://stitcher.io) <https://stitcher.io/blog/mastering-key-bindings>

Are there any tools to manage and centralize keybindings for multiple applications

There are indeed several tools and approaches that can help centralize and manage keybindings across multiple applications like Wezterm, Zellij, Neovim, and Raycast. Here are some clever ways people have tackled this challenge:

## Configuration Management Tools

Using configuration management tools can help centralize your keybindings:

- Ansible, Puppet, or Chef can be used to manage and deploy keybinding configurations across different applications.

- Create a central YAML or JSON file defining all keybindings, then use scripts to generate application-specific config files from this master file.

## Unified Keybinding Schemes

Developing a consistent keybinding scheme across applications can improve usability:

- Use the same modifier keys consistently for similar actions across different apps.

- Group similar actions under the same key prefix. For example, use "Space" as a leader key in both Neovim and Zellij for window management commands.

## Integration Tools

Some tools allow for seamless integration between applications:

- The wezterm.nvim plugin enables navigation between Neovim panes and Wezterm panes using the same keybindings\[4\].

- Configure Zellij to pass through certain keybindings to Neovim, avoiding conflicts\[5\].

## Context-Aware Keybindings

Implement keybindings that change based on the active application:

- Tools like Hammerspoon (macOS) or AutoHotkey (Windows) can create global keybindings that behave differently depending on the active window.

- Configure Wezterm to detect when you're in a full-screen application like Neovim and adjust keybindings accordingly\[4\].

## Centralized Documentation

Maintain a central repository for your keybinding documentation:

- Use a personal wiki or markdown files in a Git repository to document all your keybindings.

- Create custom commands in Raycast to display your keybinding cheat sheets on demand.

## Modular Configuration

Structure your configuration files in a modular way:

- Break down your keybindings into logical groups (e.g., navigation, text manipulation, window management).

- Use separate files for different applications or contexts, but source them from a main configuration file.

## Windows-Specific Tools

For Windows users, there are specific tools that can help manage keybindings:

- Microsoft PowerToys includes a Keyboard Manager utility that allows you to remap keys and create custom shortcuts system-wide\[1\]\[2\]\[3\].

- AutoHotkey is a powerful scripting language for Windows that can be used to create complex keybinding systems.

By combining these approaches, you can create a centralized keybinding system that works across Wezterm, Zellij, Neovim, Raycast, and other terminal applications. Remember to regularly review and adjust your keybindings as your workflow evolves, and don't be afraid to experiment with different setups to find what works best for you.

Citations:
\[1\] How to remap keys in Windows 11 with PowerToys Keyboard ... <https://www.techradar.com/computing/windows/how-to-remap-keys-in-windows-11-with-powertoys-keyboard-manager>
\[2\] PowerToys Keyboard Manager utility for Windows - Microsoft Learn <https://learn.microsoft.com/nl-nl/windows/powertoys/keyboard-manager>
\[3\] How to remap keys using Keyboard Manager in Microsoft's PowerToys <https://www.zdnet.com/home-and-office/work-life/how-to-remap-keys-using-keyboard-manager-in-microsofts-powertoys/>
\[4\] How I use Wezterm <https://mwop.net/blog/2024-07-04-how-i-use-wezterm.html>
\[5\] Zellij ❤️ Neovim <https://shoukoo.github.io/blog/zellij-love-neovim/>