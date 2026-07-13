---
aliases: []
created: 2025-12-21T00:00:00+00:00
modified: 2026-07-13T08:52:56+00:00
permalink: llmeon/30-library/so-t/so-t-unified-keyboard-workflow
tags: []
title: SoT - Unified Keyboard Workflow
---

## 1. Core Philosophy: "Scope by Modifier"

---

## 2. The Layered Architecture

The workflow is organized into five distinct layers, moving from the physical hardware to the application-specific context.

| Layer | Scope | Modifier | Tool / Function | Trigger |
|:--- |:--- |:--- |:--- |:--- |
| 0 | Physical Hardware | `Esc` (as Hyper) | Keyboardio Atreus (Firmware) | `Hold Esc` |
| 1 | OS / Window Mgmt | `Fn` + `Ctrl` | Hammerspoon (Window/System Menu) | `Raise`+`Ctrl` -> `F18` |
| 2 | App Launcher | `Hyper` + `Space` | Raycast (App Launching, Clipboard) | `Esc`+`Space` |
| 3 | Pane Navigation | `Ctrl` | Global Navigation (Across Splits/Panes) | `Ctrl` + `h/j/k/l` |
| 4 | Editor Actions | `Space` (as Leader) | WhichKey (Code/Git/File Operations) | `Tap Space` -> Menu |

---

### Layer 0: Physical Hardware (Keyboardio Atreus)

The foundation of the entire system is the Keyboardio Atreus. Its firmware is configured to emit specific keycodes that the operating system can interpret.

- The Hyper Key: The `Esc` key is configured to function as a "Hyper" key (`Cmd+Ctrl+Opt+Shift`) when held down. This provides a dedicated, system-wide modifier for the application launcher layer, preventing conflicts with standard application hotkeys.
- The Fn (Raise) Key: This key provides access to a separate layer of keys, used here to trigger the OS/Window Management layer.

### Layer 1: OS & Window Management (Hammerspoon)

- Trigger: Hold `Fn` (Raise) + Tap `Ctrl`. This chord is mapped to the `F18` key, which triggers a custom, recursive menu in Hammerspoon.
- Action: Provides system-level control over window positioning and other OS functions.
- Example Chains:
    - Window Management: `Fn+Ctrl` -> `w` -> `h` (move window to Left Half)
    - System Tools: `Fn+Ctrl` -> `s` -> (custom system menu)

### Layer 2: Application Launcher (Raycast)

- Trigger: Hold `Esc` (as Hyper) + Tap `Space`.
- Action: Opens the Raycast launcher.
- Purpose: Provides a single entry point for launching applications, searching files, accessing clipboard history, and performing calculations.

### Layer 3: Pane Navigation (Global `Ctrl` + HJKL)

- Trigger: `Ctrl` + `h` / `j` / `k` / `l`.
- Action: Moves focus between adjacent panes or splits.
- Consistency: This is a globally consistent navigation scheme that works across multiple applications, including:
    - Neovim (native window splits)
    - VSCode (editor groups)
    - WezTerm (terminal panes)

### Layer 4: Editor-Specific Actions (Leader Key)

- Trigger: Tap `Space` (configured as the Leader key).
- Action: Opens the WhichKey menu within the active editor (Neovim/VSCode), displaying available contextual actions.
- Purpose: Provides a structured, discoverable menu for application-specific commands, organized mnemonically.
- Example Chains:
    - File Ops: `Space` -> `f` -> `s` (File Save)
    - Git Ops: `Space` -> `g` -> `c` (Git Commit)
    - Code Actions: `Space` -> `c` -> `a` (Code Actions)

---

## 3. Ergonomics & Memory Hooks

> [!tip]
> The workflow is designed to be ergonomic and easy to remember by assigning modifiers to specific fingers/hand positions.
>
> -   Pinky (Fn) + Thumb (Ctrl) -> Move Windows (OS)
> -   Pinky (Esc) + Thumb (Space) -> Launch Apps (Launcher)
> -   Pinky (Ctrl) + Fingers (HJKL) -> Move Focus (App Panes)
> -   Thumb (Space) -> Edit Code (Editor)
