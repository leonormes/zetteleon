---
aliases: []
confidence: 
created: 2025-12-14T01:01:42Z
epistemic: 
last_reviewed: 
modified: 2025-12-14T13:01:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Untitled
type: 
uid: 
updated: 
---

## AeroSpace Guide for macOS

### 1. Core Concepts

- **Workspaces**: These are virtual desktops (like macOS Spaces) but more powerful. You have workspaces 1-9 available by default.
- **Monitors**: Your physical screens (Laptop, External 1, External 2).
- **Tiling**: AeroSpace automatically arranges your windows so they don't overlap.
- **Focus**: Which window is currently active.
- **Service Mode**: A special "layer" of commands for actions you don't do constantly (like resizing or moving a window to a far-away workspace), keeping your main shortcuts simple.

### 2. Your Current Keybindings (Hyper Key)

Your configuration uses the **Hyper Key** (`cmd` + `alt` + `ctrl` + `shift`) for almost everything.

#### **Navigation (Moving Focus)**

- **Focus Left/Down/Up/Right**: `Hyper` + `h` / `j` / `k` / `l`
- **Switch Workspace**: `Hyper` + `1` through `9`
- **Focus Next Monitor**: `Hyper` + `m`
- **Back-and-Forth (Last Workspace)**: `Hyper` + `tab`

#### **Moving Windows (Quick Moves)**

- **Move Window Left/Down/Up/Right**: `Hyper` + `Arrow Keys`

#### **Service Mode (`Hyper` + `q`)**

Press `Hyper` + `q` to enter Service Mode. You are now in a "command waiting" state.

- **Move Window to Workspace**: Press `1`-`9` to send the active window there.
- **Resize Window**: Press `h` / `j` / `k` / `l`.
- **Move Workspace to Next Monitor**: Press `m`.
- **Reset Sizes**: Press `r`.
- **Exit Service Mode**: Press `Esc` or `q`.

---

### 3. Configuring Monitors (The "How-To")

Right now, your config tries to force workspaces 7, 8, and 9 to a monitor named 'secondary'. Since you have 3 monitors, we need to be more specific.

#### Step 1: Find Your Monitor Names

Open a terminal and run:

```bash

aerospace list-monitors

```

You will see output usually identifiable by ID or name (e.g., `1`, `2`, `3` or names if they are distinct).

#### Step 2: Assign Workspaces

Open your config file: `~/.config/aerospace/aerospace.toml`.

Look for the `[workspace-to-monitor-force-assignment]` section.

You can map specific workspaces to specific monitors. For a 3-monitor setup (Left, Center, Right), you might want a setup like this:

```toml

[workspace-to-monitor-force-assignment]

1 = 1 # Main laptop display (example ID)

2 = 1

3 = 2 # External Monitor 1

4 = 2

5 = 3 # External Monitor 2

6 = 3

```

*Note: You can use regex patterns for monitor names, or simple IDs if they are stable.*

#### Step 3: Reload Config

After saving the file, AeroSpace usually reloads automatically. If not, you can run:

```bash

aerospace reload-config

```

---

### 4. Workflows to Try

#### **Experiment 1: The "Tosser" (Moving Windows)**

1. Open three windows on Workspace 1.
2. Focus one window using `Hyper` + `h`/`l`.
3. Move it to the right using `Hyper` + `Right Arrow`. Watch it swap places.
4. **Send it away**: Press `Hyper` + `q` (enter Service Mode), then pres `2`. The window is now on Workspace 2.
5. Go to Workspace 2 (`Hyper` + `2`) to say hello to it.

#### **Experiment 2: The "Multi-Monitor Master"**

1. Focus a window on your main screen.
2. Press `Hyper` + `m`. Focus should jump to the next monitor.
3. Press `Hyper` + `m` again to cycle through all 3 screens.
4. **Bring a workspace to you**: If you are on Monitor 1, and you press `Hyper` + `3` (and Workspace 3 is currently on Monitor 2), AeroSpace will often swap the workspaces so you can see it *right here*. (This behavior depends on settings, but is the default "switch to workspace" behavior).

#### **Experiment 3: The "Resizer"**

1. Have two windows side-by-side.
2. Press `Hyper` + `q` (Service Mode).
3. Press `l` (lowercase L) explicitly to widen the focused window.
4. Press `r` to reset them to equal size.
5. Press `Esc` to leave Service Mode.

---

### 5. Troubleshooting

- **"I lost a window!"**: Toggle `Hyper` + `tab` to check your last workspace, or cycle through `1`-`9`.
- **"My layout is messsed up"**: Press `Hyper` + `q` then `f` (flatten) to reset the tiling tree if you accidentally made a weird nest of windows.
