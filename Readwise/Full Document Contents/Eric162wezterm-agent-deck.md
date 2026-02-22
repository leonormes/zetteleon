# Eric162/wezterm-agent-deck

![rw-book-cover](https://opengraph.githubassets.com/6ac0729a7fce993294a3afe7b2c61514b365c6c3ab281c7b382aff183ef1ccdb/Eric162/wezterm-agent-deck)

## Metadata
- Author: [[https://github.com/Eric162/]]
- Full Title: Eric162/wezterm-agent-deck
- Category: #articles
- Summary: WezTerm Agent Deck is a plugin to monitor AI coding agents inside the WezTerm terminal. It shows colored status dots and sends notifications when agents need attention. Users can customize colors, icons, and display settings for different agent states.
- URL: https://github.com/Eric162/wezterm-agent-deck

## Full Document
#### Create list

[Open in github.dev](https://github.dev/) [Open in a new github.dev tab](https://github.dev/) [Open in codespace](https://github.com/codespaces/new/Eric162/wezterm-agent-deck?resume=1)

### Eric162/wezterm-agent-deck

main

t

Go to file

Code

Open more actions menu

### WezTerm Agent Deck

Monitor AI coding agents (Claude Code, OpenCode, Aider, etc.) in WezTerm. Shows status dots in tabs and notifications when agents need attention.

Inspired by [agent-deck](https://github.com/asheshgoplani/agent-deck).

[![Screenshot 2026-01-12 at 1 01 00 PM](https://private-user-images.githubusercontent.com/3197311/534711022-9285f6d7-cd59-4035-81ce-9d3268948622.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjgyNTI5MzQsIm5iZiI6MTc2ODI1MjYzNCwicGF0aCI6Ii8zMTk3MzExLzUzNDcxMTAyMi05Mjg1ZjZkNy1jZDU5LTQwMzUtODFjZS05ZDMyNjg5NDg2MjIucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDExMiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAxMTJUMjExNzE0WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZjBjMDI1YWQzNTk2ZWFhZjI5ZDRkY2JlY2Y2MjcxN2QyOWYzNWJkMzllMmQ1MGU5YWYzMDI1ZGE0NzQwOTVkZCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.iVtebbvOkHmeUNeoTTgeBNz0qnSNPPa-8FxTAhiCLNk)](https://private-user-images.githubusercontent.com/3197311/534711022-9285f6d7-cd59-4035-81ce-9d3268948622.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjgyNTI5MzQsIm5iZiI6MTc2ODI1MjYzNCwicGF0aCI6Ii8zMTk3MzExLzUzNDcxMTAyMi05Mjg1ZjZkNy1jZDU5LTQwMzUtODFjZS05ZDMyNjg5NDg2MjIucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDExMiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAxMTJUMjExNzE0WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZjBjMDI1YWQzNTk2ZWFhZjI5ZDRkY2JlY2Y2MjcxN2QyOWYzNWJkMzllMmQ1MGU5YWYzMDI1ZGE0NzQwOTVkZCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.iVtebbvOkHmeUNeoTTgeBNz0qnSNPPa-8FxTAhiCLNk)
#### Quick Start

```
local wezterm = require('wezterm')
local agent_deck = wezterm.plugin.require('https://github.com/eshirley/wezterm-agent-deck')
local config = wezterm.config_builder()

agent_deck.apply_to_config(config)

return config
```

#### Configuration

```
agent_deck.apply_to_config(config, {
    update_interval = 500,  -- ms between status checks

    colors = {
        working = '#A6E22E',   -- green: agent processing
        waiting = '#E6DB74',   -- yellow: needs input
        idle = '#66D9EF',      -- blue: ready
        inactive = '#888888',  -- gray: no agent
    },

    icons = {
        style = 'unicode',  -- or 'nerd', 'emoji'
        unicode = { working = '●', waiting = '◔', idle = '○', inactive = '◌' },
    },

    notifications = { enabled = true, on_waiting = true },
})
```

#### Custom Rendering

Disable built-in display and use the plugin's detection in your own handlers:

```
agent_deck.apply_to_config(config, {
    tab_title = { enabled = false },
    right_status = { enabled = false },
    colors = { ... },
})

-- Custom tab title with status dots
wezterm.on('format-tab-title', function(tab)
    local formatted = {}
    for _, pane_info in ipairs(tab.panes or {}) do
        local state = agent_deck.get_agent_state(pane_info.pane_id)
        if state then
            table.insert(formatted, { Foreground = { Color = agent_deck.get_status_color(state.status) } })
            table.insert(formatted, { Text = agent_deck.get_status_icon(state.status) .. ' ' })
        end
    end
    table.insert(formatted, { Text = tab.tab_title or 'Terminal' })
    return wezterm.format(formatted)
end)

-- Custom status bar
wezterm.on('update-status', function(window, pane)
    for _, tab in ipairs(window:mux_window():tabs()) do
        for _, p in ipairs(tab:panes()) do
            agent_deck.update_pane(p)
        end
    end

    local counts = agent_deck.count_agents_by_status()
    local cfg = agent_deck.get_config()
    local items = {}

    if counts.waiting > 0 then
        table.insert(items, { Foreground = { Color = cfg.colors.waiting } })
        table.insert(items, { Text = counts.waiting .. ' waiting ' })
    end

    window:set_right_status(wezterm.format(items))
end)
```

#### API

```
agent_deck.get_agent_state(pane_id)      -- { agent_type, status }
agent_deck.get_all_agent_states()        -- all pane states
agent_deck.count_agents_by_status()      -- { working=N, waiting=N, ... }
agent_deck.get_status_icon(status)       -- configured icon
agent_deck.get_status_color(status)      -- configured color
agent_deck.update_pane(pane)             -- trigger detection
agent_deck.get_config()                  -- current config
```

#### Supported Agents

OpenCode, Claude Code, Gemini, Codex, Aider. Add custom agents:

```
agents = {
    my_agent = {
        patterns = { 'my%-agent' },
        status_patterns = {
            working = { 'thinking' },
            waiting = { 'y/n' },
        },
    },
}
```

#### Development

```
-- Load locally for development
local agent_deck = dofile('/path/to/wezterm-agent-deck/plugin/init.lua')
```

Debug via WezTerm console (Ctrl+Shift+L).

#### License

MIT
