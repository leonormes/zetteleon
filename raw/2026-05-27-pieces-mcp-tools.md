---
title: Mcp Tools — Pieces LTM 2026-05-27
created: 2026-05-27 21:30:22.835947+00:00
source: pieces-ltm
pieces_ids:
- d3905143-5363-442a-a8f5-8fd940404da8
- d9f1b9bd-96d3-4079-9f95-11a54e3fc0d7
- cf9021ea-b7b8-4553-acee-03c91dc45f55
tags:
- raw
- pieces
permalink: llmeon/raw/2026-05-27-pieces-mcp-tools
---

## Asset 1 (Pieces: d3905143-5363-442a-a8f5-8fd940404da8)

**Type:** N/A  
**Captured:** 2026-05-27T07:41:06.566107Z

All four pagination chains are now exhausted (all returning `sufficient`). Here is the fully grounded Hermes `/goal` prompt, built from your real memory evidence.

---

## Your LLM MCP Setup — What Memory Shows

**Hostname / machine:** `implacable-lake` (macOS), with a secondary machine `FF-M07W9K7YN7` (work laptop).

**Central MCP architecture:** You run **`mcpproxy`** (`smart-mcp-proxy` v1.26.0) as a centralised HTTP MCP server on `http://127.0.0.1:8000/mcp/` with `MCPPROXY_ROUTING_TYPE=CALL_TOOL` (clients see only `retrieve_tools` + `call_tool`, not the full federated schema). Config lives at `~/.config/mcpproxy/mcp_proxy.json`.

**LLM clients wired to the proxy:**
- **Gemini CLI** — `~/.gemini/settings.json` with `url: http://127.0.0.1:8000/mcp/`
- **Claude Code** — `~/.claude/settings.json` with `mcpServers: { "mcp-proxy": { "url": "http://127.0.0.1:8000/mcp/" } }` (chezmoi-managed at `dot_claude/settings.json`)
- **LLMeon (Gemini 3 agent)** — same proxy endpoint

**Registered backend MCP servers (from your May 8 2026 config snapshot):**
- `mcp-server-tree-sitter` v0.5.1 (via `uvx`, config at `/Users/leon.ormes/.config/mcp-server-tree-sitter/config.yaml`)
- `pieces` — `http://localhost:39300/model_context_protocol/2025-03-26/mcp`
- `memory` — `/opt/homebrew/bin/npx -y @modelcontextprotocol/server-memory`
- `obsidian-mcp-tools` — `op run --no-masking -- /Volumes/DAL/Zettelkasten/LLMeon/.obsidian/plugins/mcp-tools/bin/mcp-server`
- `atlassian` (Jira/Confluence) — via 1Password op:// credential injection
- `ast-grep`, `codemod`, `lsp-bash`, `sequential-thinking` also configured
- `gitkraken` / `gitkraken-cli` are installed as packages in your `chezmoi` `packages.yaml` (work section)

**Known open pain points from your memory:**
- `mcpproxy` crashes when run from the wrong working directory (needs to be launched from `~/.config/mcpproxy/`)
- Claude Code's MCP tool list finalises at session start — proxy must be running *before* you open a session
- The proxy uses `streamable-http`; Gemini needs `httpUrl` (not `url`) key for that transport
- 1Password (`op run`) wraps secrets at launch so tokens never touch disk

---

## Hermes `/goal` Prompt — Install & Configure GitKraken MCP

Copy this verbatim into your Hermes agent (or Claude Code / Gemini CLI session):

```text
/goal Install and configure the GitKraken MCP server so that mcpproxy exposes it to all LLM clients (Claude Code, Gemini CLI, LLMeon).

## Context
- Machine: implacable-lake (macOS, /Users/leon.ormes)
- Central MCP proxy: smart-mcp-proxy running at http://127.0.0.1:8000/mcp/
- Proxy config: ~/.config/mcpproxy/mcp_proxy.json (source: chezmoi at ~/.local/share/chezmoi/dot_config/mcpproxy/mcp_proxy.json)
- Package registry: cue/packages.yaml in chezmoi repo (managed by mise/brew)
- Secrets: managed via 1Password CLI (op run --no-masking --)
- GitKraken CLI (gk) is already installed as a work package in packages.yaml

## Goal
Add the GitKraken MCP server as a backend in mcpproxy so all LLM agents can use it via the existing proxy endpoint. GitKraken MCP is invoked as: `gk mcp` (stdio transport).

## Steps to perform

### 1. Verify gk CLI is present and authenticated
```bash
which gk && gk --version
gk auth status
```
If not authenticated, run `gk auth login` and follow the GitKraken OAuth flow.

### 2. Test the GitKraken MCP server directly
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}' | gk mcp
```
Confirm you get a valid JSON-RPC response listing MCP capabilities.

### 3. Add gitkraken to the mcpproxy config
Edit `~/.local/share/chezmoi/dot_config/mcpproxy/mcp_proxy.json` (or its .tmpl variant) and add the following server entry alongside the existing backends:

```json
"gitkraken": {
  "command": "gk",
  "args": ["mcp"],
  "env": {}
}
```

The full mcpServers block should look like:
```json
{
  "mcpServers": {
    "tree-sitter": { ... },
    "pieces": { ... },
    "memory": { ... },
    "obsidian-mcp-tools": { ... },
    "atlassian": { ... },
    "gitkraken": {
      "command": "gk",
      "args": ["mcp"]
    }
  }
}
```

### 4. Apply the chezmoi change
```bash
chezmoi apply --verbose
```

### 5. Restart mcpproxy from its config directory
```bash
pkill -f mcpproxy || true
sleep 2
cd ~/.config/mcpproxy && nohup /Users/leon.ormes/.local/bin/mcpproxy > /tmp/mcpproxy.log 2>&1 &
sleep 3
curl -s http://127.0.0.1:8000/mcp/ -H "Accept: application/json, text/event-stream" | head -20
```

### 6. Verify gitkraken tools are visible via the proxy
In a new Claude Code or LLMeon session, run:
```
/mcp list
```
You should see `gitkraken` listed under the proxy's available tools via `retrieve_tools`.

Alternatively, test with curl:
```bash
curl -s -X POST http://127.0.0.1:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### 7. Smoke test from an LLM agent
Open LLMeon or Claude Code and ask:
> "Use the gitkraken MCP tool to list my recent repositories."

## Success criteria
- [ ] `gk mcp` responds correctly when invoked directly
- [ ] mcpproxy config includes the gitkraken entry
- [ ] `chezmoi apply` succeeds without errors
- [ ] mcpproxy restarts cleanly and is listening on port 8000
- [ ] `retrieve_tools` via the proxy surfaces gitkraken tools
- [ ] An LLM agent can successfully invoke a gitkraken MCP tool

## Known gotchas (from your setup history)
- mcpproxy MUST be launched from ~/.config/mcpproxy/ or it looks for mcp_config.json in the cwd and crashes
- Claude Code finalises its MCP tool list at session start — restart Claude Code after restarting the proxy
- If gk requires a token at runtime, wrap the launch with `op run --no-masking --` and store the credential in 1Password at op://Private/GitKraken_Token/credential, then add it to the env block in mcp_proxy.json as an op:// reference
- The mcpproxy uses CALL_TOOL routing — clients won't see gitkraken tools directly, they'll call retrieve_tools with a query like "gitkraken repository" and the proxy will route accordingly
```

## Asset 2 (Pieces: d9f1b9bd-96d3-4079-9f95-11a54e3fc0d7)

**Type:** N/A  
**Captured:** 2026-05-27T07:37:15.494651Z

The user wants me to:
1. Retrieve memories about their LLM MCP setup on their laptop
2. Give them a Hermes/goal prompt to install and configure GitKraken MCP so their LLM can use it

Let me start by searching their memory for LLM MCP setup information, and also look up the GitKraken MCP getting started page simultaneously.

## Asset 3 (Pieces: cf9021ea-b7b8-4553-acee-03c91dc45f55)

**Type:** N/A  
**Captured:** 2026-05-27T07:37:09.406826Z

retrive memories about my llm mcp setup on my laptop. give me a hermes /goal prompt to install and configure https://help.gitkraken.com/mcp/mcp-getting-started/ so that my llm can use it