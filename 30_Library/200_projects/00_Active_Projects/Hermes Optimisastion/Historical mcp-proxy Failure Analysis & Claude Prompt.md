---
created: 2026-05-28T14:45:16+00:00
modified: 2026-05-28T14:46:38+00:00
tags: [1]
title: Historical mcp-proxy Failure Analysis & Claude Prompt
---
You are a systems reliability engineer fixing the mcp-proxy integration in my chezmoi dotfiles repo at ~/.local/share/chezmoi. You have full filesystem access. Do NOT deviate from the steps below without surfacing the issue first.

## CONTEXT

I use `smart-mcp-proxy` (installed via uv as `mcpproxy`) as a single HTTP MCP gateway for all LLM clients (Claude Code, Gemini CLI, Cursor, Hermes). It runs at http://127.0.0.1:8000/mcp/ in CALL_TOOL mode, exposing only `retrieve_tools` and `call_tool`. Upstream servers are defined in `.chezmoidata.toml` and templated into `~/.config/mcpproxy/mcp_proxy.json` via chezmoi.

## KNOWN HISTORICAL FAILURES (do NOT repeat these)

1. mcp-remote OAuth loop — The stdio bridge `npx -y mcp-remote http://127.0.0.1:8000/mcp/ --allow-http` causes mcp-remote v0.1.38 to loop on /.well-known/oauth-protected-resource and never connect. It also crashes with `TypeError: Invalid URL` on some invocations. The fix is direct HTTP registration, NOT the mcp-remote bridge.

2. Gemini SSE vs Streamable HTTP mismatch — Gemini CLI uses `"url"` key for SSE and `"httpUrl"` key for Streamable HTTP. The proxy runs streamable-http. Using `"url"` causes silent hang (200 OK, session ID returned, no data). dot_gemini/settings.json.tmpl MUST use `"httpUrl"`.

3. No hot-reload — mcpproxy reads config ONCE at startup. After any `chezmoi apply` that changes `mcp_proxy.json`, the proxy MUST be restarted via `launchctl kickstart -k gui/$(id -u)/com.user.mcpproxy`.

4. Discovery-wedging — Servers that fail to start (Obsidian not running, op credentials unavailable, mcp-remote OAuth) block discovery for ALL servers. High-risk servers (obsidian-mcp-tools, atlassian, todoist with mcp-remote) must have startup dependencies satisfied before the proxy starts, OR be kept `disabled = true` until explicitly needed.

5. LLM doesn't know the retrieve_tools → call_tool two-step — Every CLAUDE.md or context doc MUST contain the mandatory workflow: (1) call retrieve_tools with plain-English query, (2) pick tool name, (3) call call_tool. If this is absent, agents waste 5–15 rounds re-deriving it.

6. Hermes disabling wanted servers — Never set `disabled = true` on user-specified servers without explicit confirmation. Only disable servers that are confirmed broken/unnecessary.

7. `__NPX__` placeholder must be used — Never write bare `"npx"`, `"uvx"`, or `"node"` in `.chezmoidata.toml`. Always use `__NPX__`, `__UVX__`, or `__NODE__` placeholders so the CUE pipeline resolves absolute paths.

## TASKS — execute in order, do not skip

### Task 1: Fix Claude Code MCP registration
The current `dot_claude/settings.json` uses the broken mcp-remote bridge. Replace it with direct HTTP:

```json
{
  "mcpServers": {
    "mcp-proxy": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp/"
    }
  }
}
```

Verify: `cat ~/.local/share/chezmoi/dot_claude/settings.json`—confirm it no longer contains `mcp-remote`.

Also check `dot_claude/CLAUDE.md` (or create it if absent) and ensure it contains the mandatory workflow block (see Task 5).

### Task 2: Fix Gemini CLI Transport Key

Read `dot_gemini/settings.json.tmpl`. If it contains `"url": "http://127.0.0.1:8000/mcp/"`, change to `"httpUrl": "http://127.0.0.1:8000/mcp/"`. Leave all other fields unchanged.

Also check `dot_gemini/antigravity/mcp_config.json` and `dot_gemini/antigravity-cli/` configs—apply the same `url` → `httpUrl` fix if present.

### Task 3: Add Auto-restart Hook on Config Change

Check if `run_onchange_restart-mcpproxy.sh.tmpl` exists in the scripts/ directory. If not, create it:

```bash
#!/usr/bin/env bash
# chezmoi:onchange: ~/.config/mcpproxy/mcp_proxy.json
# Restart mcpproxy when its config changes.
set -euo pipefail
launchctl kickstart -k "gui/$(id -u)/com.user.mcpproxy" 2>/dev/null || \
  pkill -f mcpproxy && sleep 2 && ~/scripts/start-mcpproxy.sh &
echo "[mcpproxy] Restarted after config change at $(date)"
```

This ensures chezmoi apply automatically restarts the proxy whenever `mcp_proxy.json` changes.

### Task 4: Audit `.chezmoidata.toml` for Placeholder Correctness

Read `.chezmoidata.toml`. For EVERY `[mcp_servers.*]` block:

- If `command = "npx"` (bare), change to `command = "__NPX__"`
- If `command = "uvx"` (bare), change to `command = "__UVX__"`
- If `command = "node"` (bare, absolute path to a specific install), document it clearly with a comment explaining why an absolute path is necessary (as `brain-mcp` currently does)
- If `command = "mcp-remote"` (bare), it must use the absolute path: `command = "/opt/homebrew/bin/mcp-remote"`—PATH is not reliable in launchd context

Check specifically: `pieces` currently uses `command = "mcp-remote"`—change to `/opt/homebrew/bin/mcp-remote`.

### Task 5: Add/update CLAUDE.md with Mandatory Mcp-proxy Workflow

Check for `dot_claude/CLAUDE.md` (rendered to `~/.claude/CLAUDE.md`). Add or update this section:

```markdown
## MCP Tools (smart-mcp-proxy)

ALL external tools (Jira, Confluence, Obsidian, Todoist, GitKraken, memory, code analysis)
are exposed through a single proxy: mcp-proxy at http://127.0.0.1:8000/mcp/.

The proxy surfaces exactly TWO tools:
- `mcp-proxy:retrieve_tools(query)` — semantic search across all upstream tools
- `mcp-proxy:call_tool(name, args)` — executes a named tool from retrieve_tools results

### Mandatory workflow (no exceptions):
1. `retrieve_tools(query="plain English description of what you need")`
2. Pick the best-matching tool name from results
3. `call_tool(name="<tool_name>", arguments_json="{...}")`

NEVER call Jira, Obsidian, GitKraken, or Todoist tools directly — they are not registered.
NEVER spend more than 1 round searching for a tool — retrieve_tools finds it immediately.
NEVER try to run `which mcp-proxy` or `curl /mcp/list` to discover the tool surface.

If retrieve_tools returns no results, try a shorter/simpler query. If the proxy appears
down, run: ~/scripts/mcpproxy-healthcheck.sh
```

### Task 6: Smoke-test the Fixes

After applying:

```bash
chezmoi apply --verbose
sleep 3
~/scripts/mcpproxy-healthcheck.sh
```

Expected: `[mcpproxy-healthcheck] OK: proxy is healthy and tool surface is ready`

Then verify Claude Code sees the proxy:

```bash
claude mcp list
```

Expected: `mcp-proxy` listed with type `http`, URL `http://127.0.0.1:8000/mcp/`.

### Task 7: Commit

```bash
cd ~/.local/share/chezmoi
git add dot_claude/settings.json dot_claude/CLAUDE.md dot_gemini/ scripts/ .chezmoidata.toml
git commit -m "fix(mcp): replace mcp-remote bridge with direct HTTP, fix Gemini transport key, add auto-restart hook, enforce __NPX__ placeholders"
git push origin development
```

## SUCCESS CRITERIA

- [ ] `dot_claude/settings.json` uses `"type": "http"`, not `mcp-remote`
- [ ] `dot_gemini/settings.json.tmpl` uses `"httpUrl"`, not `"url"`
- [ ] `run_onchange_restart-mcpproxy.sh.tmpl` exists and is executable
- [ ] All bare `"npx"`/`"uvx"` commands replaced with `__NPX__`/`__UVX__` in `.chezmoidata.toml`
- [ ] `dot_claude/CLAUDE.md` contains the retrieve_tools → call_tool workflow
- [ ] `mcpproxy-healthcheck.sh` passes after `chezmoi apply`
- [ ] Change committed to `development` branch

## CONSTRAINTS

- Do NOT disable any currently-enabled mcp_servers without explicit confirmation
- Do NOT modify `dot_config/mcpproxy/mcp_proxy.json.tmpl` directly (it is generated)
- Do NOT change the routing mode from CALL_TOOL
- Use British English in all commit messages and comments
- If any step reveals an unexpected state (e.g. a file doesn't exist, config key differs), surface it rather than silently working around it
