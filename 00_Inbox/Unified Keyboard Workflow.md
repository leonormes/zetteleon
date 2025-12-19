---
aliases: []
confidence: 
created: 2025-12-19T13:41:38Z
epistemic: 
last_reviewed: 
modified: 2025-12-19T13:44:18Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Unified Keyboard Workflow
type: 
uid: 
updated: 
---

## Unified Keyboard Workflow

> [!INFO] Philosophy: **Scope by Modifier**
> The system is designed so you never have to guess "What key does what?". The **modifier** determines the **scope** of your action.

| Scope | Modifier | Function | Trigger |
| :--- | :--- | :--- | :--- |
| **OS / Window** | **Fn + Ctrl** | **Hammerspoon** (Window/System Menu) | `Raise`+`Ctrl` -> **F18** |
| **Launcher** | **Hyper + Space** | **Raycast** (App Launching) | `Esc`+`Space` |
| **App / Pane** | **Ctrl** | **Navigate** (Between Splits) | `Ctrl` + `h` (Left Split) |
| **Editor** | **Space** | **Leader** (Code/Git/File) | `Space` -> Menu |

---

### 📅 1. OS Layer (Hammerspoon)
**Trigger**: Hold `Fn` (Raise) + Tap `Ctrl` (Bottom row).
**Action**: Opens your custom recursive binder menu.

- **Window Management**:
  - `w` -> `h` (Left Half)
  - `w` -> `l` (Right Half)
  - `w` -> `m` (Maximized)
- **System Tools**:
  - `s` -> System menu

### 🚀 2. Launcher Layer (Raycast)
**Trigger**: Hold `Esc` (Hyper) + Tap `Space`.
**Action**: Opens **Raycast**.

*Why*: Your Atreus sends `Cmd+Ctrl+Opt+Shift` (Hyper) when holding Escape.

- **Use for**:
  - Launching Apps (`Chrome`, `Spotify`)
  - Clipboard History
  - Calculations

### 🧭 3. App Layer (Navigation)
**Trigger**: `Ctrl` + `h / j / k / l`.
**Action**: Moves focus between splits/panes.

- **Works in**:
  - **Neovim** (Native splits)
  - **VSCode/Antigravity** (Editor groups)
  - **Terminals** (WezTerm panes - *if configured*)

### 📝 4. Editor Layer (Antigravity/Neovim)
**Trigger**: Tap `Space`.
**Action**: Opens the **WhichKey** leader menu.

- **File Operations**: `f` -> Save (`s`), New (`n`), Find (`f`)
- **Git**: `g` -> Commit (`c`), Push (`p`), Log (`l`)
- **Code**: `c` -> Rename (`r`), Actions (`a`), Format (`f`)

> [!TIP] Memory Hook
>
> - **Pinky (Fn) + Thumb (Ctrl)** -> Move Windows (OS)
> - **Pinky (Esc) + Thumb (Space)** -> Launch Apps (Raycast)
> - **Pinky (Ctrl) + Fingers (HJKL)** -> Move Focus (App)
> - **Thumb (Space)** -> Edit Code (Editor)
