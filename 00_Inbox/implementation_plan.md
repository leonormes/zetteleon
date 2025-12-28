# Aerospace and Sketchybar Integration Plan

## Goal Description
Enhance the integration between Aerospace and Sketchybar to make the workspace indicator dynamic and informative. 
Currently, the user has a static list of workspaces (1-9). We will transition to a dynamic generation based on Aerospace's state, split by monitor, and add descriptive names to workspaces (e.g., "1: Web", "2: Term").

## User Review Required
> [!IMPORTANT]
> **Workspace Names**: I have inferred potential workspace names based on your `aerospace.toml` routing rules. Please review and edit the `workspace_names` array in the new `items/aerospace.sh` file if you prefer different names.
>
> **Proposed Mapping:**
> - 1: Web
> - 2: Term
> - 3: Code
> - 4: Notes
> - 5: Media
> - 6: Misc
> - 7: Services
> - 8: Music
> - 9: Other

## Proposed Changes

### Sketchybar Configuration
We will refactor the `sketchybarrc` to be cleaner and more modular, following the reference implementation pattern.

#### [MODIFY] [sketchybarrc](file:///Users/leon.ormes/.local/share/chezmoi/dot_config/sketchybar/sketchybarrc)
- Remove the hardcoded `for idx in {1..9}` loop.
- Source the new `items/aerospace.sh` file.

#### [NEW] [items/aerospace.sh](file:///Users/leon.ormes/.local/share/chezmoi/dot_config/sketchybar/items/aerospace.sh)
- Create a script that:
    1. Defines a `workspace_names` associative array for mapping IDs to names.
    2. Queries `aerospace list-monitors` to get monitor IDs.
    3. Queries `aerospace list-workspaces --monitor <id>` to get workspaces for each monitor.
    4. Dynamically adds sketchybar items for each workspace with the correct name and monitor association.
    5. Subscribes to `aerospace_workspace_change`.

#### [MODIFY] [plugins/aerospace.sh](file:///Users/leon.ormes/.local/share/chezmoi/dot_config/sketchybar/plugins/aerospace.sh)
- Update the highlighting logic to match the new item names/variables.
- Ensure it handles the `$FOCUSED_WORKSPACE` variable correctly passed from Aerospace.

## Verification Plan

### Manual Verification
1.  **Reload Sketchybar**: Run `sketchybar --reload` (or the internal reload command).
2.  **Verify Visuals**:
    - Check if workspaces are grouped by monitor.
    - Check if names are displayed (e.g., "1 Web").
    - Check if the active workspace is highlighted.
3.  **Dynamic Updates**:
    - Switch workspaces using Aerospace commands (`alt-shift-1`, etc.).
    - Verify the highlight changes instantly.
    - Move a workspace to another monitor (if applicable) and check if the bar updates (might require a reload or advanced event handling, but basic switching should work).
