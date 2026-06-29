---
title: Hermes MCP Config — Self-Fix Goal Prompt for Legacy MCP Settings
created: 2026-05-30 08:31:27+00:00
source: pieces-ltm
pieces_ids:
- 19808e94-4125-495b-b2cb-85c5bad2a6f3
- 19aa7a0e-e2ac-480e-bf87-17ef44da8a9a
- 97f2e103-f3f2-421d-b4df-47146aed1b83
tags:
- raw
- pieces
permalink: llmeon/raw/2026-05-30-pieces-hermes-mcp-config
---

## Asset 1 (Pieces: 19808e94-4125-495b-b2cb-85c5bad2a6f3)

Here's the ready-to-paste `/goal` prompt:

---

```
/goal

## MISSION: Audit and fix Hermes MCP server configuration

### CONTEXT

You are running on a macOS machine managed via chezmoi. Your MCP configuration is managed in TWO places that must stay in sync:

- **Chezmoi source (authoritative):** `~/.local/share/chezmoi/private_dot_hermes/private_config.yaml`
- **Live config (generated):** `~/.hermes/config.yaml`

All changes MUST be made to the chezmoi source first, then applied with `chezmoi apply --force ~/.hermes/config.yaml`. Never edit the live config directly — it will be overwritten.

### ARCHITECTURE

A `smart-mcp-proxy` daemon runs permanently at `http://127.0.0.1:8000/mcp/` via a macOS LaunchAgent (`com.user.mcpproxy`). It federates ALL external MCP servers (Jira, Obsidian, memory, GitKraken, tree-sitter, etc.). Hermes should connect to it as a single HTTP endpoint — NOT spawn any of those individual servers itself.

The only valid MCP entries in Hermes config are:
1. `mcp-proxy` → HTTP to `http://127.0.0.1:8000/mcp/` with `transport: streamable-http`
2. `pieces` → SSE to `http://localhost:39300/model_context_protocol/2025-03-26/mcp` (used for LTM)

Any other `mcp_servers` entries — especially command/stdio-based ones — cause hermes `--tui` to hang on startup waiting for `connect_timeout` seconds before giving up. This is the root cause of 30–60+ second startup times.

### YOUR TASKS — execute in order, do not skip steps

#### PHASE 1: Investigate current state

1. Read the chezmoi source config:
   `cat ~/.local/share/chezmoi/private_dot_hermes/private_config.yaml`

2. Read the live config:
   `cat ~/.hermes/config.yaml`

3. Check if there is drift between them:
   `chezmoi diff ~/.hermes/config.yaml 2>&1`

4. List all currently configured MCP servers in Hermes:
   `hermes mcp list 2>&1`

5. Check proxy health:
   `~/scripts/mcpproxy-healthcheck.sh 2>&1`

6. Run hermes diagnostics:
   `hermes doctor 2>&1`

7. Time the current startup baseline (without user config to isolate Python overhead):
   `{ sleep 3; printf '/quit\n'; } | time hermes --tui --ignore-user-config 2>&1 | tail -5`

8. Time the real startup:
   `{ sleep 10; printf '/quit\n'; } | time hermes --tui 2>&1 | tail -5`

Document your findings before proceeding.

#### PHASE 2: Identify legacy and broken entries

Audit the chezmoi source `mcp_servers` block. Flag any entry that:

- Uses `command:` or `args:` to spawn a local process (stdio transport) — these servers are federated through `mcp-proxy` and should NOT be duplicated here
- Has a `connect_timeout` above 10 (anything > 10 causes visible startup lag)
- Has a `transport:` mismatch with the running service (e.g. no `transport: streamable-http` for the proxy)
- Points to a binary or command that doesn't exist or isn't valid as an MCP server (e.g. any `graphify --mcp` style entry — graphify is a skill, not an MCP server)
- Is a legacy entry from before the centralised proxy was set up

List every problematic entry with a reason before making any changes.

#### PHASE 3: Apply fixes to chezmoi source

Edit `~/.local/share/chezmoi/private_dot_hermes/private_config.yaml` using `chezmoi edit ~/.hermes/config.yaml` or patch the source file directly.

The `mcp_servers` block should end up looking exactly like this (preserve any other sections of the config untouched):

```yaml
mcp_servers:
  mcp-proxy:
    url: http://127.0.0.1:8000/mcp/
    transport: streamable-http
    connect_timeout: 8
  pieces:
    url: http://localhost:39300/model_context_protocol/2025-03-26/mcp
    transport: sse
    connect_timeout: 8
```

Remove ALL other `mcp_servers` entries. Do not modify any other top-level config keys (model, memory, approval, delegation, skills, profiles, etc.).

#### PHASE 4: Apply and verify

1. Apply the chezmoi source to the live config:
   `chezmoi apply --force ~/.hermes/config.yaml 2>&1`

2. Confirm live config matches intent:
   `grep -A 20 "^mcp_servers:" ~/.hermes/config.yaml`

3. Confirm no chezmoi drift remains:
   `chezmoi diff ~/.hermes/config.yaml 2>&1`

4. Verify Hermes sees the right MCP servers:
   `hermes mcp list 2>&1`

5. Run doctor again to confirm no new issues:
   `hermes doctor 2>&1 | grep -E "(v|A|×|MCP|issue|error)"`

6. Time the startup — target is under 12 seconds:
   `{ sleep 15; printf '/quit\n'; } | time hermes --tui 2>&1 | tail -5`

#### PHASE 5: Report

Produce a summary with:
- What entries were found and why they were problematic
- What was changed in the chezmoi source
- Before/after startup time
- Whether `hermes mcp list` confirms both `mcp-proxy` and `pieces` are connected and ready
- Any remaining issues or caveats

### CONSTRAINTS

- DO NOT touch `auth.json`, `auth/` directory, or any credential files
- DO NOT change the primary model or provider
- DO NOT modify any profiles (ops.yaml, jira.yaml, etc.)
- DO NOT modify `SOUL.md`
- DO NOT remove the `pieces` MCP entry
- ALL file edits must go through chezmoi source — never edit `~/.hermes/config.yaml` directly
- If in doubt about an entry, document it and ask before removing it
```

---

**How to use:** paste the whole block into `hermes --tui` after the `/goal` command (or use it as the goal directly). Hermes will work through the phases sequentially, show you what it found before removing anything, and produce a timing comparison at the end.

---

## Asset 2 (Pieces: 19aa7a0e-e2ac-480e-bf87-17ef44da8a9a)

The user wants a Hermes `/goal` prompt that they can paste into `hermes --tui` to fix its own configuration. Based on everything I know from their memory:

1. The prompt should tell Hermes to:
   - Review the chezmoi repo for legacy MCP server settings
   - Remove stale/broken MCP entries from both `~/.hermes/config.yaml` and the chezmoi source (`~/.local/share/chezmoi/private_dot_hermes/private_config.yaml`)
   - Ensure the proxy is properly configured with `transport: streamable-http` and low `connect_timeout`
   - Strip out any command-based MCP entries that should route through the proxy instead
   - Validate that the configuration is working correctly

Now I'm pulling together the specific details from their setup to craft the actual prompt text.

---

## Asset 3 (Pieces: 97f2e103-f3f2-421d-b4df-47146aed1b83)

give me the hermes prompt to fix its own config. It should review the chezmoi repo for legacy mcp server settings and remove them from the home dir and the chezmoi repo so that they do not confuse llm. it should investigate the current setup and do as you have advised.