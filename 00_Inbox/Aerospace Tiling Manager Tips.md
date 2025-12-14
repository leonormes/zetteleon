---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/127b3eb60f1f"
author:
  - "[[Gemini]]"
published:
created: 2025-12-14
description: "Created with Gemini"
tags:
  - "clippings"
---
Based on your request and the analysis of the video "Aerospace Is Probably The Best MacOS Tiling Manager I've Ever Used," here is a structural breakdown and list of essential tips for using the **Aerospace Tiling Window Manager**.

Aerospace functions as a tiling window manager for macOS, operating on a conceptual tree structure to efficiently organise and navigate windows across multiple workspaces (referred to as "spaces").

---

### Core Principles & Navigation

Aerospace's efficiency is rooted in keyboard-centric control, using `Alt` (Option) combined with **Vim keybindings (H, J, K, L)** for intuitive motion.

| Function | Keybinding | Explanation |
| --- | --- | --- |
| **Move Focus Sideways** | `Alt` + `H` (Left) or `L` (Right) | Shifts focus to an adjacent tile. \[[02:34](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=154)\] |
| **Move Focus Vertically** | `Alt` + `J` (Down) or `K` (Up) | Shifts focus up or down within a vertical layout. \[[03:33](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=213)\] |
| **Move Window** | *Use the mouse* with `Command` + `Control` | Drag a window to a new position, and Aerospace will dynamically reorganise the surrounding tiles. \[[03:45](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=225)\] |
| **Increase Tile Size** | `Alt` + `+` (or `Alt` + `Shift` + `=`) | Increases the relative size of the currently focused tile, which smoothly adjusts the proportions of other tiles. \[[04:55](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=295)\] |
| **Reset Layout/Canvas** | `Alt` + `Shift` + `;` followed by `R` | Enters Service Mode, then sends the reset signal to clear and revert the current workspace layout. \[[05:14](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=314)\] |

### Layout Management

Aerospace supports flexible tiling and stacking models, moving beyond simple half-screen splits.

| Layout Feature | Keybinding | Conceptual Framework |
| --- | --- | --- |
| **Toggle Orientation** | `Alt` + `/` | Switches the current layout between a **Vertical** (default) and **Horizontal** tile arrangement. \[[03:21](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=201)\] |
| **Accordion Layout** | `Alt` + `,` | Switches the layout style to *Accordion*, which stacks windows (like a drawer) while keeping a full-size view of the active one. Use `Alt` + `J/K` to cycle through the stack. \[[04:07](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=247)\] |
| **Nested Tiling (Joining)** | `Alt` + `Shift` + `Arrow` (or `Control` + `Vim Key`) | **Structural Tip:** Joins two adjacent tiles into a single, nested container within the Aerospace tree. This allows for complex layouts (e.g., one vertical tile next to a split horizontal container). \[[06:10](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=370)\] |
| **Focus Fullscreen** | `Alt` + `Control` + `Shift` + `F` | A temporary mode to see the focused application clearly without using macOS's native fullscreen, which would break the tiling structure. \[[09:13](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=553)\] |

### Space (Workspace) Management

Aerospace treats macOS Spaces as distinct, configurable workspaces.

| Space Control | Keybinding | Purpose |
| --- | --- | --- |
| **Send Window to Space** | `Alt` + `Shift` + `Number` | Moves the focused window to the specified Space number and immediately follows the window to the new Space. \[[03:09](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=189)\] |
| **Jump to Space** | `Alt` + `Number` | Switches focus to the specified Space number. \[[03:16](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=196)\] |
| **Fuzzy Search/Focus** | *Custom Keybinding* (e.g., `Alt` + `G` in the video) | **Mental Model:** By integrating Aerospace with a tool like `fzf`, you can search across all open windows on *all* spaces by name or content, eliminating the need to memorise space numbers for specific applications. \[[07:07](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=427)\] |

### Advanced Configuration

The system is configured via an `aerospace.toml` file located in `~/.config/aerospace`.

| Configuration Tip | Method/Keybinding | Function and **Why it Works** |
| --- | --- | --- |
| **Floating Windows** | Regex in `aerospace.toml` | Define specific applications (e.g., Finder, Telegram) to always launch as **floating windows**. This preserves the integrity of the tiling layout for core work while allowing quick, temporary use of messenger/utility apps. \[[08:35](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=515)\] |
| **Use Modes** | Custom mapping (e.g., `Alt` + `Shift` + `Enter`) | **Conceptual Framework:** Modes allow you to define layers of keybindings, similar to keyboard layers. This lets you switch context (e.g., to an `apps` mode) and use a simple key combo (`Alt` + `W`) to launch an application, preventing key conflicts in the main working mode. \[[11:31](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=691)\] |
| **Application Launching** | `exec and forget` command | Aerospace can be configured to act as an application launcher by assigning key combinations to execute and forget a command, simplifying the setup by replacing a separate app launcher (like `skhd`). \[[09:37](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=577)\] |
| **Reload Configuration** | `Alt` + `Shift` + `;` followed by `Escape` | After modifying the `aerospace.toml` file, entering Service Mode and hitting `Escape` instantly reloads the configuration without requiring a full restart of the application. \[[11:02](http://www.youtube.com/watch?v=5nwnJjr5eOo&t=662)\] |

---

**Video Details:**

- **Title:** Aerospace Is Probably The Best MacOS Tiling Manager I've Ever Used
- **Channel:** DevOps Toolbox
- **URL:**[http://www.youtube.com/watch?v=5nwnJjr5eOo](http://www.youtube.com/watch?v=5nwnJjr5eOo)

This is another video about aerospace do the same thing again

https://youtu.be/gjR2eiomRwo?si=C7vtpdiayI9jsUZa

This analysis provides a top-down, structural overview of using Aerospace, focusing on the underlying concepts and configuration mechanisms, which aligns with your Abstract-Conceptual cognitive style.

---

## Aerospace: Structural and Conceptual Analysis

The video frames Aerospace as a tiling window manager that replaces the mouse-heavy window management of macOS with an efficient, **keyboard-centric, tree-based workflow**. The core differentiator from competitors like Yabai is its use of **Virtual Workspaces** instead of relying on macOS's native Spaces feature, which simplifies setup (no SIP disabling required) and enhances stability.

### I. System Architecture & Configuration

Aerospace’s design prioritises a unified, clean configuration layer.

| Conceptual Layer | Mechanism | Key Tip/Value Proposition |
| --- | --- | --- |
| **Workspace Abstraction** | **Virtual Workspaces** (Custom to Aerospace) | **Conceptual Tip:** Unlike native macOS Spaces, Aerospace’s workspaces are defined within the application, providing control that is decoupled from macOS updates. This makes the system more stable. \[[02:21](http://www.youtube.com/watch?v=gjR2eiomRwo&t=141)\] |
| **System Rules** | **Rule-Based Allocation** | **Structural Tip:** Use the configuration file to enforce that specific applications (e.g., Brave, VS Code) **always open on a designated workspace number**. This builds a persistent mental model of your setup. \[[09:06](http://www.youtube.com/watch?v=gjR2eiomRwo&t=546)\] |
| **Multi-Monitor Logic** | **Display-to-Workspace Mapping** | **Efficiency Tip:** In a multi-screen setup, **force a range of workspaces to a specific display**. For example, Workspaces 1-5 on the main monitor, 6-7 on the laptop screen. Moving a window between screens becomes a conceptual move between two predefined workspaces. \[[09:38](http://www.youtube.com/watch?v=gjR2eiomRwo&t=578)\] |
| **Customisation** | **`~/.config/aerospace/aerospace.toml`** | The entire system is customised through a single, well-commented TOML file, promoting a centralised configuration model. \[[03:12](http://www.youtube.com/watch?v=gjR2eiomRwo&t=192)\] |
| **Process Automation** | **Callback Events** (e.g., `exec-on-workspace-change`) | Allows you to trigger shell scripts (e.g., to update a custom status bar like SketchyBar) when an event occurs, enabling real-time visual synchronisation. \[[05:22](http://www.youtube.com/watch?v=gjR2eiomRwo&t=322)\] |

### II. Core Layout and Manipulation Tips

Aerospace manages windows as nodes in a tree structure. Manipulation commands move the focus or the window itself within this structure.

| Function | Keybinding (Example) | Conceptual Purpose |
| --- | --- | --- |
| **Window Focus** | `Alt` + `H/J/K/L` (Vim Motion) | The fundamental action for navigation; shifts focus to adjacent windows based on the layout, eliminating mouse use. \[[07:31](http://www.youtube.com/watch?v=gjR2eiomRwo&t=451)\] |
| **Full-Screen Zoom** | `Alt` + `F` (Custom) | **Visualisation Tip:** Temporarily zooms the focused window to fill the entire screen, allowing intense focus without breaking the underlying tiling structure. \[[07:11](http://www.youtube.com/watch?v=gjR2eiomRwo&t=431)\] |
| **Layout Orientation** | `Alt` + `E` (Custom) | Toggles the layout of the current window grouping between a **Vertical** split and a **Horizontal** split. \[[07:03](http://www.youtube.com/watch?v=gjR2eiomRwo&t=423)\] |
| **Move Window** | `Alt` + `Shift` + `Arrow` (or Vim key) | Moves the window to a different position within the current workspace structure. \[[07:46](http://www.youtube.com/watch?v=gjR2eiomRwo&t=466)\] |
| **Move to Workspace** | `Alt` + `Shift` + `Number` | Transfers the focused window to a specified workspace. Essential for organising tasks across your defined workspaces. \[[08:16](http://www.youtube.com/watch?v=gjR2eiomRwo&t=496)\] |

### III. Productivity and Workflow Integration

The most significant performance gains come from integrating Aerospace with other tools for instant access and system monitoring.

| Integration Concept | Tool/Feature | Value |
| --- | --- | --- |
| **Application Launching** | **Application Shortcuts** (via Modes/Main Bindings) | **Efficiency Tip:** Configure keybindings (e.g., `Alt` + `C` for Chrome) to instantly launch or jump to a specific application, regardless of which workspace it is on. \[[06:37](http://www.youtube.com/watch?v=gjR2eiomRwo&t=397)\] |
| **System Visualisation** | **SketchyBar Integration** | **Monitoring Tip:** Use a custom status bar like SketchyBar to display the **current focus application** and **status of all workspaces** (e.g., which apps are open on which number). This prevents cognitive load from remembering where everything is. \[[01:43](http://www.youtube.com/watch?v=gjR2eiomRwo&t=103)\], \[[10:41](http://www.youtube.com/watch?v=gjR2eiomRwo&t=641)\] |
| **Contextual Keybindings** | **Modes** (e.g., `service`, `main`) | Allows for creating different layers of keybindings. Commands that are used infrequently (e.g., configuration reload) are relegated to a separate *service* mode, keeping the main mode clean and fast for daily use. \[[05:54](http://www.youtube.com/watch?v=gjR2eiomRwo&t=354)\] |

---

**Video Details:**

- **Title:** Aerospace Changes Your macOS Window Management FOREVER!
- **Channel:** mehdio DataTV
- **URL:**[https://youtu.be/gjR2eiomRwo](https://www.google.com/search?q=https://youtu.be/gjR2eiomRwo)

Https://youtu.be/W7FMMTifS6c?si=c3q2DjQjGexRp9hF

Based on your request and the analysis of the video "Aerospace and Leader Key go PERFECT together – tiling window manager on macOS," here is a top-down, conceptual breakdown of the Aerospace setup, focusing on the synergy between the window manager and the Leader Key system.

This approach prioritises structural efficiency and the underlying logic of the workflow.

---

## Aerospace Workflow: The Leader Key Model

The core concept presented is that the key space for global shortcuts on macOS is crowded. To overcome this, the workflow separates commands into two logical groups: **Core Navigation** (retained as global shortcuts) and **All Other Commands** (namespaced under a **Leader Key**).

### I. Conceptual Architecture

| Layer | Component/Tool | Purpose & Mental Model |
| --- | --- | --- |
| **Window Management** | **Aerospace** | The structural engine. Manages windows as **nested tiles** or **stacks** within a workspace tree, enabling a highly efficient, keyboard-driven layout. \[[01:14](http://www.youtube.com/watch?v=W7FMMTifS6c&t=74)\] |
| **Command Namespacing** | **Leader Key** (Application) | The efficiency layer. It maps all secondary and tertiary Aerospace commands into a single nested key sequence (e.g., `Leader` + `W` for Window). This prevents hotkey conflicts and provides a visual **cheat sheet** (legend) for quick recall. \[[02:27](http://www.youtube.com/watch?v=W7FMMTifS6c&t=147)\], \[[06:09](http://www.youtube.com/watch?v=W7FMMTifS6c&t=369)\] |
| **Visual Feedback** | **Janky Borders** | Provides a highly visible, configurable border (e.g., bright red) around the **currently focused window**, compensating for the minimal visual cues in tiling managers. \[[06:46](http://www.youtube.com/watch?v=W7FMMTifS6c&t=406)\] |
| **System Overview** | **Sketchy Bar** | Replaces the native macOS menu bar with a custom bar to display real-time information, such as the workspace overview, current focused app, and integration status (e.g., to-do list items). \[[07:11](http://www.youtube.com/watch?v=W7FMMTifS6c&t=431)\] |

### II. Core Global Bindings (High-Frequency Actions)

These are the only commands retained as global shortcuts for maximum speed and muscle memory. The default bindings use the `Option` (Alt) modifier.

| Function | Keybinding (Default) | Conceptual Role |
| --- | --- | --- |
| **Move Focus** | `Option` + Vim movement keys (`H`, `J`, `K`, `L`) | Shifts the bright border (focus) to an adjacent tile. This is the most frequent command. \[[03:01](http://www.youtube.com/watch?v=W7FMMTifS6c&t=181)\] |
| **Switch Workspace** | `Shift` + `Option` + Vim movement keys | Switches the entire view to a different logical workspace. \[[03:08](http://www.youtube.com/watch?v=W7FMMTifS6c&t=188)\] |

### III. Namespaced Commands (Via Leader Key)

All remaining, less frequent, or more complex commands are placed into a named group, typically prefixed with a 'W' (for Window) in the Leader Key configuration.

### IV. Configuration and Organisational Tips

1. **Use a Dedicated Sizing Mode:** Instead of cluttering the main mode with resizing commands, create a single-purpose `resizing mode` in `aerospace.toml`. Enter this mode with a simple hotkey, perform your size adjustments (increase/decrease tile size), and then exit to return focus to navigation. \[[03:16](http://www.youtube.com/watch?v=W7FMMTifS6c&t=196)\], \[[03:24](http://www.youtube.com/watch?v=W7FMMTifS6c&t=204)\]
2. **External Monitor Mapping:** Dedicate a specific, higher-numbered workspace (e.g., the fifth workspace 'T') exclusively to your external monitor. This simplifies the mental model: switching to the 'T' workspace means switching to the external screen. \[[04:20](http://www.youtube.com/watch?v=W7FMMTifS6c&t=260)\], \[[04:27](http://www.youtube.com/watch?v=W7FMMTifS6c&t=267)\]
3. **Aesthetic Padding:** Configure a small amount of padding around your windows. This is not purely aesthetic; it ensures the focus border (from Janky Borders) is fully visible, providing clearer feedback on the active window. \[[02:49](http://www.youtube.com/watch?v=W7FMMTifS6c&t=169)\]

Https://youtube.com/watch?v=Nozqf0ZCiPw&si=kr6b\_9zTplnktDFp

The following analysis extracts the structural tips and core operational concepts from the video, presenting them in a framework that aligns with a top-down, efficiency-focused cognitive style.

---

## Aerospace: Operational and Configuration Tips

The central philosophy of this setup is to achieve a **keyboard-driven workflow**, moving control away from the mouse to increase productivity and maintain focus. Aerospace is complemented by external tools to provide essential visual and systemic feedback.

### I. Core Window Tiling and Navigation

Aerospace manages applications as a grid of tiles, where focus and manipulation are controlled by the keyboard, primarily using the `Option` (Alt) key with Vim movement bindings (`H`, `J`, `K`, `L`).

| Function | Keybinding (Concept) | Conceptual Role |
| --- | --- | --- |
| **Move Focus Left/Right** | `Option` + `H` / `L` | Shifts the active focus (indicated by the border) between horizontal tiles. \[[02:50](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=170)\] |
| **Move Focus Up/Down** | `Option` + `J` / `K` | Shifts the active focus between vertical tiles (commonly used on vertical monitors). \[[03:03](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=183)\], \[[11:59](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=719)\] |
| **Move Application Tile** | `Option` + `Shift` + `Movement Key` | Repositions the entire focused application within the current tiled layout. \[[03:24](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=204)\], \[[12:12](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=732)\] |
| **Full Screen Mode** | `Option` + `F` | Toggles the focused application to fill the screen, temporarily overriding the tile split. \[[13:03](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=783)\] |
| **Toggle Floating Mode** | `Option` + `Shift` + `Space` | **Crucial Tip:** Toggles the application between a fixed tile and a **floating window**. A floating window will not snap to the grid, allowing it to be resized freely and placed above the grid. \[[13:47](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=827)\], \[[14:12](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=852)\] |

### II. Workspace (Space) Management

Aerospace uses its own set of numbered workspaces, which are more easily controlled and switched than native macOS Spaces.

| Function | Keybinding (Concept) | Structural Tip/Goal |
| --- | --- | --- |
| **Switch Workspace (General)** | `Option` + `Number` (1-9) | Instantly jumps to the numbered workspace, with no delay. Workspaces with no open applications are not typically displayed by Sketchy Bar. \[[14:52](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=892)\], \[[15:05](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=905)\] |
| **Switch to Monitor-Specific Workspaces** | `Option` + `A`, `B`, `C` (Custom) | **Structural Mapping:** Dedicate specific keybindings to workspaces intended for an external monitor (e.g., Workspaces A, B, and C are for VS Code/coding). \[[10:10](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=610)\], \[[11:34](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=694)\] |
| **Move Window to Workspace** | `Option` + `Shift` + `Number` | Moves the focused application to a different workspace. This is the mechanism for organising your work by context. \[[15:44](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=944)\] |
| **Named Workspaces** | *Configuration via Sketchy Bar* | **Focus Tip:** Define descriptive names for primary workspaces (e.g., `1-web`, `2-code`, `3-media`) in your Sketchy Bar configuration to assign a clear purpose to each space, reducing context switching overhead. \[[22:34](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=1354)\] |

### III. System Integration and Feedback

Effective use of Aerospace relies on integrating external tools for visual feedback and system status.

| Tool | Tip / Configuration Logic | Purpose and Value |
| --- | --- | --- |
| **Janky Borders** | Set a prominent colour (e.g., red) and width (e.g., 5px) in the configuration. | **Visual Feedback:** Provides an immediate, clear border around the focused application, replacing the ambiguous native macOS focus state. \[[02:03](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=123)\], \[[06:49](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=409)\] |
| **Sketchy Bar** | 1\. Configure Aerospace to auto-start Sketchy Bar (`after-startup-command`). \[[06:40](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=400)\] 2. Set Aerospace to trigger a Sketchy Bar update on every workspace change (`exec-on-workspace-change`). \[[07:20](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=440)\] | **System Overview:** Displays real-time workspace status, showing the icons of open applications within each workspace, as well as general system information. \[[07:45](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=465)\], \[[23:54](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=1434)\] |
| **Raycast** | Use as a replacement for Spotlight, which is faster and provides advanced options to manage (quit, force quit, disable) running applications from a single command interface. \[[26:11](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=1571)\] | **Application Management:** Quickly launch and manage applications without affecting the tiling structure. \[[26:46](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=1606)\] |

### IV. Configuration and Maintenance

Tips for configuring the core `aerospace.toml` file for reliability and aesthetics.

| Configuration Tip | Location / Mechanism | Why it is Necessary |
| --- | --- | --- |
| **Set Floating Rules** | `on-window-detected` command in `aerospace.toml` | **Efficiency Tip:** Specify utility applications (e.g., Finder, SF Symbols) to automatically open in `layout floating` mode to prevent them from snapping and disrupting your primary tiled layouts. \[[17:31](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=1051)\], \[[17:58](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=1078)\] |
| **Configure Monitor-Specific Gaps** | `gaps` setting, using `monitor-id` | Adjust the outer-top gap specifically for your Mac's screen (often needing a lower value like 40) to ensure the Sketchy Bar does not overlap or obscure the top of application windows. \[[08:05](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=485)\], \[[09:13](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=553)\], \[[09:34](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=574)\] |
| **Reload Configuration** | `mode service` with the key sequence: `Option` + `Shift` + `;` then `Escape` | Enables rapid application of configuration changes without needing to restart the entire application. \[[16:35](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=995)\], \[[16:45](http://www.youtube.com/watch?v=Nozqf0ZCiPw&t=1005)\] |
|  |  |  |

Https://www.youtube.com/live/t73K2LTST8E?si=kOsHWOhJRWtFrr16

This analysis synthesises the collective knowledge and best practices for Aerospace from the videos provided, adhering to your preference for a structured, abstract-conceptual, and efficiency-focused guide.

---

## Aerospace: A Conceptual Framework for macOS Tiling

Aerospace functions as a keyboard-centric tiling window manager for macOS. Its core architectural advantage is the use of **Virtual Workspaces**, which are decoupled from macOS's native Spaces feature. This provides a stable, efficient environment that does not require disabling System Integrity Protection (SIP), a key benefit over older tiling managers like Yabai.

### I. Core Principles and Essential Commands (Tier 1)

The most essential interaction is rapid, keyboard-driven navigation, primarily using the `Option` (Alt) key combined with the muscle memory of **Vim keys (H, J, K, L)**.

### II. Advanced Layout and Structural Manipulation (Tier 2)

Aerospace treats windows as nodes in a logical **tree structure**. These commands manipulate the layout of the nodes.

| Functional Concept | Command/Mechanism | Why & How It Works |
| --- | --- | --- |
| **Layout Orientation** | Toggle the root container's orientation. | `Option` + `/` (Toggles between **Vertical** and **Horizontal** splits). |
| **Accordion Layout** | Stack windows on top of each other, displaying one fully while allowing rapid cycling. | `Option` + `,` (Toggles layout style to Accordion; use `J/K` to cycle). |
| **Nesting/Joining Tiles** | Groups multiple tiles into a single container node within the tree. | `Option` + `Shift` + `Arrow Key` (or `Control` + `Vim Key` custom). Necessary for creating complex, multi-dimensional layouts (e.g., a horizontal split next to a vertical split). |
| **Toggle Floating Mode** | Removes a window from the tiling structure. | `Option` + `Shift` + `Space`. Essential for applications that should not be tiled (e.g., Messenger apps, utilities, floating tool windows). |
| **Full-Screen Zoom** | Temporarily fills the screen with the focused application. | `Option` + `F` (or similar custom binding). Allows focused work without engaging the native macOS full-screen feature, which typically breaks the tiling environment. |
| **Flatten Tree/Reset** | Reset the layout of the current workspace. | Enter Service Mode (`Option` + `Shift` + `;`) followed by `R` (Reload/Reset command). |

### III. Configuration and Workflow Architecture (Tier 3)

All logic is managed in the centralised configuration file: `~/.config/aerospace/aerospace.toml`.

| Configuration Tip | Implementation Logic | Conceptual Value (The 'Why') |
| --- | --- | --- |
| **Auto-Reload Config** | Use a Neovim/editor hook (`autocmd BufWritePost`) to execute the `aerospace reload-config` command on save. | **Efficiency:** Instantly applies changes to the setup upon saving the TOML file, eliminating manual reloading. |
| **Maximising Screen Space** | Set external padding/gaps (`gap outer left`, `right`, `bottom`) to `0`. | **Density:** Reclaims every pixel of screen real estate, allowing windows to abut the screen edges, ideal for a minimalist setup. |
| **Anchor Applications** | Use the `on-window-detected` command to auto-assign key applications to specific workspaces. | **Workflow:** Enforces a persistent cognitive map (e.g., Terminal always on Workspace A, Browser always on Workspace W), reducing mental load for app location. |
| **Floating Rules** | Use `on-window-detected` rules to force utility apps (e.g., Finder, Raycast) into `layout floating`. | **Stability:** Prevents temporary windows from entering the tiling tree, which would disrupt complex layouts. |
| **Using Modes** | Define secondary keybinding layers (e.g., `[mode.resize]`). | **Clarity:** Namespaces less-used or multi-step commands (like detailed resizing or maintenance) under a single entry key, preserving a clean global hotkey space. |

### IV. Essential External Tool Integration

Aerospace works best when integrated with complementary utilities to provide missing visual feedback and functionality.

| Companion Tool | Integration Purpose | Role in the Workflow |
| --- | --- | --- |
| **Sketchy Bar** | Status bar replacement, configured to read Aerospace's virtual workspace status. | **Monitoring:** Provides visual feedback on the currently active workspace number/name and displays icons of all running applications across all workspaces. |
| **Janky Borders** | Dedicated application for custom window borders. | **Focus:** Provides a highly visible, customisable border (e.g., bright red/7px) around the *focused* window, which is crucial feedback in a minimal tiling environment. |
| **Raycast** | Application launcher and command tool (replacing Spotlight). | **Access:** Enables instant launch, focus, or hiding of applications via keyboard, often providing better application management (e.g., force quit, hidden state control). |
| **Home Row App** (or similar) | System-wide keyboard navigation/clicking tool. | **Omnipresence:** Extends the keyboard-driven philosophy by allowing in-app navigation (clicking buttons, following links) using Vim-like keystrokes in applications that are not natively Vim-friendly. |
|  |  |  |

Https://youtu.be/3DpLQwSzT-M?si=egC6CRl01Zw-Ytc1

This comprehensive analysis consolidates all structural tips and usage concepts from the five videos you provided, presented in a top-down, conceptual framework.

Aerospace is presented as an efficient, keyboard-driven **tiling window manager** for macOS. Its central design mechanism is the use of **Virtual Workspaces**, which are decoupled from native macOS Spaces. This architectural choice simplifies configuration and stability by eliminating the need to disable System Integrity Protection (SIP).

---

## I. Core Navigation & Primitives (Tier 1)

The most essential commands rely on muscle memory, typically combining the **Option** (Alt) key with Vim movement keys (`H`, `J`, `K`, `L`).

| Functional Concept | Keybinding (Default) | Role in the Workflow |
| --- | --- | --- |
| **Move Focus** | `Option` + `H/J/K/L` | Shifts the active focus (indicated by the border) between adjacent tiles without moving the windows. |
| **Move Window** | `Option` + `Shift` + `H/J/K/L` | Physically repositions the entire focused window within the current layout structure. (Note: Many users customise this to include `Control` instead of `Shift`). |
| **Tiling Orientation** | `Option` + `/` (Forward Slash) | Toggles the layout of the current container between **Vertical** (default) and **Horizontal** splits. |
| **Full-Screen Zoom** | Custom binding, e.g., `Option` + `F` | Temporarily maximises the focused application to the screen size, overriding the tiling structure for intense focus without using native macOS fullscreen. |
| **Toggle Floating Mode** | `Option` + `Shift` + `Space` | Removes the window from the tiling grid, allowing it to be freely resized and placed over other windows. |

---

## II. Structural Logic & Advanced Layout (Tier 2)

Aerospace manages windows as nodes in a flexible **tree structure**. These concepts define the underlying mental model of your desktop organisation.

| Conceptual Mechanism | Keybindings/Process | Value Proposition |
| --- | --- | --- |
| **Virtual Workspaces** | `Option` + `Number` or `Letter` | **Decoupled Organisation:** Allows for simple, fast switching between dedicated contexts (e.g., '1-Web', 'A-Terminal') that are separate from native macOS Spaces. |
| **Mnemonic Naming** | Configured via `aerospace.toml` | **Efficiency:** Name workspaces using relevant mnemonics (e.g., `T` for Terminal, `B` for Browser, `P` for Productivity) for instant recall and navigation. |
| **Accordion Layout** | `Option` + `,` (Comma) | **Density:** Stacks multiple windows into a single, full-screen tile, allowing you to cycle through them quickly using the focus keys. Ideal for reference materials or blog posts. |
| **Nesting/Joining Windows** | Use **Service Mode** (`Option` + `Shift` + `;`) followed by a move/join command (`Alt` + `Shift` + `H/L`). | **Flexibility:** Merges two adjacent windows into a single, nested container, enabling complex splits (e.g., a vertical split where one side is further split horizontally). |
| **Dedicated Sizing Mode** | Custom Modes (e.g., `[mode.resize]`) | **Clarity:** Creates a separate key layer for sizing commands (e.g., `Option` + `Plus` / `Minus` to increase/decrease tile size), preventing conflicts with main navigation bindings. |
| **Move to Monitor** | `Option` + `Shift` + `Tab` (or similar custom binding) | **Multi-Monitor Logic:** Moves the focused virtual workspace to the adjacent physical monitor. Many users dedicate specific workspace ranges (e.g., 6 and 7) to a secondary screen. |

---

## III. Configuration & System Blueprint (Tier 3)

The system's control centre is the `aerospace.toml` file, located at `~/.config/aerospace/aerospace.toml`.

| Configuration Tip | Mechanism / Code Logic | Why it is Essential |
| --- | --- | --- |
| **Automate Startup** | Set `start-at-login = true` in the TOML file. | Ensures Aerospace begins managing your windows immediately upon system boot. |
| **Automate Reloading** | Use an editor hook (e.g., Neovim `autocmd`) to run `aerospace reload-config` every time the `aerospace.toml` file is saved. | **Efficiency:** Instantly applies configuration changes without manual restarts or reloads. |
| **Enforce Floating Rules** | Use `on-window-detected` to set `layout floating` for specific app IDs (e.g., Finder, Settings). | **Stability:** Stops utility windows from breaking your main tiled layouts when they open. |
| **Configure Gaps** | Adjust `gap outer` and `gap inner` settings in the TOML file. | **Aesthetics/Density:** Setting outer gaps to `0` maximises screen space, while adjusting inner gaps controls the visual separation between active windows. |
| **Enter Service Mode** | `Option` + `Shift` + `;` | **Maintenance:** Used to access commands for maintenance, such as configuration reloading (`Escape`) or layout resetting (`R`), without cluttering the main keybindings. |
| **Mission Control Setting** | Set macOS System Settings > Mission Control to **Group windows by application**. | **Clarity:** Improves the visual layout of your workspaces when viewing Mission Control, making it easier to see which windows belong where. |

---

## IV. Essential Ecosystem Tools (Tier 4)

Aerospace is typically installed alongside these utilities to complete the highly efficient workflow.

| Tool Name | Purpose and Role | Value in the Aerospace System |
| --- | --- | --- |
| **Janky Borders** | A small utility to draw a highly visible, custom-coloured border around the **focused window**. | **Critical Feedback:** Compensates for the minimal visual cues in tiling managers by clearly indicating which window is currently active. |
| **Sketchy Bar** | A highly customisable replacement for the native macOS menu bar. | **Monitoring:** Reads Aerospace's status to display the names/icons of applications running on each virtual workspace, providing a constant overview. |
| **Raycast** | A powerful launcher and command-line utility (often replacing Spotlight). | **Application Management:** Used for quickly launching, focusing, and managing (quitting, forcing quit) applications with keyboard shortcuts without disrupting the tiling environment. |
| **Homebrew** | The primary package manager for installing Aerospace and its companion utilities. | **Installation:** Provides the simplest, most stable method for installing and maintaining all tools in the ecosystem. |
|  |  |  |

Https://youtu.be/Th6P52IAyKI?si=pf1\_D9ahkLxVcThx

This comprehensive analysis consolidates all tips and conceptual mechanisms from the five videos you provided, offering a structural and efficiency-focused guide on how to use the **Aerospace Tiling Window Manager**.

The core premise of Aerospace is to achieve a stable, keyboard-driven environment on macOS by using its own **Virtual Workspaces**, which are decoupled from the native macOS Spaces feature, thus avoiding the need to disable System Integrity Protection (SIP).

---

## I. System Architecture & Setup (The Blueprint)

This defines the foundational layer of control and system integration.

| Structural Component | Tip / Mechanism | Conceptual Value (The 'Why') |
| --- | --- | --- |
| **Installation** | Use Homebrew (`brew install`). | Provides the simplest, most stable package management for installation and updates. |
| **Configuration File** | Modify `~/.config/aerospace/aerospace.toml`. | Centralises all configuration logic, from keybindings to window rules, in one place. |
| **Startup** | Set `start-at-login = true` in the TOML file. | Ensures immediate window management upon system boot, maintaining a persistent workflow. |
| **Reloading Config** | Execute `aerospace reload-config` in the terminal or configure an editor hook. | **Efficiency:** Instantly applies changes made to the TOML file without requiring a full restart of the application. |
| **Gaps Configuration** | Adjust `gap inner` (between windows) and `gap outer` (edges of the screen). | **Aesthetics & Density:** Allows control over screen real estate. Setting `outer` gaps to 0 maximises space; setting `outer right` higher reserves space for desktop files. |
| **Visual Feedback** | Integrate **Janky Borders** (for a focus indicator) and **Sketchy Bar** (for a workspace overview). | **Clarity:** Compensates for the minimal UI by providing clear, visual confirmation of the active window and the status of all workspaces. |

---

## II. Core Primitives & Navigation (Tier 1)

These are the fundamental, high-frequency actions, typically bound to **Option** (Alt) and **Vim keys** (`H`, `J`, `K`, `L`).

| Functional Concept | Keybinding (Default/Common) | How It Works |
| --- | --- | --- |
| **Move Focus** | `Option` + `H/J/K/L` | Shifts the active focus (red border) between adjacent tiles without moving the windows themselves. |
| **Move Window** | `Option` + `Shift` + `H/J/K/L` | Moves the focused window to a new position within the tree structure, dynamically rearranging neighbouring tiles. |
| **Toggle Orientation** | `Option` + `/` (Forward Slash) | Switches the current layout between **Vertical** and **Horizontal** tiling. |
| **Resize Tile** | `Option` + `Plus` (`=`) / `Minus` (`-`) | Increases or decreases the size of the focused window, with the surrounding tiles automatically resizing to fill the space (`resize smart`). |
| **Quick Workspace Switch** | `Option` + `Tab` | Switches focus between the last two active workspaces, similar to the Command-Tab function for applications. |

---

## III. Structural Logic & Advanced Concepts (Tier 2)

These commands manipulate the underlying tree structure and control the context of your workflow.

| Concept | Keybinding/Mechanism | The Why (Architectural Role) |
| --- | --- | --- |
| **Workspace Switching** | `Option` + `Number/Letter` | **Context Management:** Used to instantly jump to a workspace dedicated to a specific task (e.g., `T` for Terminal, `B` for Browser). |
| **Move to Workspace** | `Option` + `Shift` + `Number/Letter` | **Organisation:** Moves the active window and follows it to the destination workspace. |
| **Toggle Floating Mode** | `Option` + `Shift` + `Space` | **Isolation:** Removes a window from the tiling grid, allowing it to be freely resized and layered above the grid. Used for non-tiling apps like Settings or pop-ups. |
| **Accordion Layout** | `Option` + `,` (Comma) | **Density:** Stacks multiple windows into one full-screen tile, allowing quick cycling (using `J/K` for up/down) without wasting space on multiple small tiles. |
| **Service Mode** | Enter with `Option` + `Shift` + `;` | **Maintenance Layer:** Provides a separate key map for low-frequency operations, such as configuration reloading (`Escape`) or layout resetting (`R`), keeping the main keybindings clean. |
| **Nesting/Joining** | Accessed via Service Mode, e.g., `Alt` + `Shift` + `H/L` | **Flexibility:** Merges two adjacent windows into a single container node. This is the key to creating complex, multi-dimensional layouts. |
| **Rule-Based Allocation** | `on-window-detected` rules in `.toml` | **Automation:** Automatically forces specific utility apps (e.g., Finder, Messages) into `layout floating` or to a dedicated workspace upon launch. |
| **Custom Modes** | Defining `[mode.resize]` in `.toml` | **Keybinding Strategy:** Creates a unique key map for a specific task (e.g., resizing), which is activated by an entry key, preventing hotkey conflicts in the main working mode. |
|  |  |  |

Google Account

Leon Ormes

leonormes@gmail.com