---
created: 2026-05-08 16:02:00+00:00
modified: 2026-05-26 11:43:46+00:00
pieces_ids:
- 21928c9c-0594-4a77-b2b2-1a6ce4ea18e4
- 43297b3b-1d50-474f-86c2-0b56dfc1ecb4
- 47f17296-ce00-4a40-849a-7b404b3f9868
- 9c4d5e8d-4f42-4cba-8bdc-f02da4e6665b
- c6e3d6ed-6f93-4d76-8e90-11d385ef16fa
- cde78b55-6a0a-4a70-9715-b0c35f6cfde3
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-05-08-pieces-mcp-proxy-robustness
permalink: llmeon/raw/2026-05-08-pieces-mcp-proxy-robustness
---

## Asset 1 (Pieces: 9c4d5e8d-4f42-4cba-8bdc-f02da4e6665b)

> "I have installed mcp-proxy and am trying to make it robust. I have a coding llm that has access to the config files in my chezmoi repo. Give me a prompt that instructs the agent to plan how to make the mcp-proxy robust and highly available. Hermes just disabled a bunch of servers that I do want to be on. It should research the mcp-proxy docs and then review the config I already have. It should query the pieces ltm to find relevant work and then make a plan to improve the current config."

## Asset 2 (Pieces: 21928c9c-0594-4a77-b2b2-1a6ce4ea18e4)

> "Leon wants a prompt to give to his coding LLM agent (likely Claude Code or similar) that will…"

## Asset 3 (Pieces: c6e3d6ed-6f93-4d76-8e90-11d385ef16fa)

Planned phases identified:

1. Research mcp-proxy docs
2. Review his existing config in chezmoi
3. Query Pieces LTM for relevant prior work
4. Make a plan to make mcp-proxy robust and highly available
5. Restore the servers that Hermes disabled

## Asset 4 (Pieces: 47f17296-ce00-4a40-849a-7b404b3f9868)

> "From the memories, I can see: His chezmoi repo is at `/Users/leon.ormes/.local/share/chezmoi`"

## Asset 5 (Pieces: 43297b3b-1d50-474f-86c2-0b56dfc1ecb4)

Key context points:

- The mcp-proxy config lives in the chezmoi templates, and Hermes has a separate config there too.
- Originally there were 10 servers running, but Hermes stripped out four of them (ast-grep, atlassian, todoist, and sequential-thinking).
- The proxy runs on localhost at port 8000, and there's a template file for standardizing how MCP server entries are defined.
- The proxy is wired up across multiple AI tools—Claude, Cursor, and Gemini all point to it.
- Goal: structure a prompt that accounts for all these moving pieces and helps the coding agent work effectively with this setup.

## Asset 6 (Pieces: cde78b55-6a0a-4a70-9715-b0c35f6cfde3)

Detailed agent prompt drafted with the following structure:

### Phase 1: Research Mcp-proxy Documentation

- Read official mcp-proxy docs (GitHub repo, `--help`, `pip show`)
- Document every resilience-related configuration knob (timeouts, retries, connection pooling, health endpoints)

### Phase 2: Review Existing Configuration (chezmoi Repo ONLY)

Files to read (do NOT modify):

- `~/.local/share/chezmoi/dot_config/mcpproxy/mcp_proxy.json.tmpl`
- `~/.local/share/chezmoi/dot_config/mcpproxy/README.md`
- `~/.local/share/chezmoi/private_dot_hermes/private_config.yaml`
- `~/.local/share/chezmoi/.chezmoitemplates/mcp_server_entry.tmpl`
Rendered/live state to inspect:
- `~/.config/mcpproxy/mcp_proxy.json`
- `ps aux | grep mcp-proxy`
- `lsof -i:8000`
Cross-reference other consumers:
- Claude: `~/.local/share/chezmoi/dot_claude/settings.json`
- Cursor: `~/.local/share/chezmoi/dot_cursor/mcp.json.tmpl`
- Gemini: `~/.local/share/chezmoi/dot_gemini/antigravity/mcp_config.json`

### Critical—Identify All 10 Original Servers

1. pieces—`http://localhost:39300/model_context_protocol/2025-03-26/mcp`
2. memory—`@modelcontextprotocol/server-memory`
3. obsidian-mcp-tools—Zettelkasten plugin MCP server (uses 1Password `op run`)
4. tree-sitter—`mcp-server-tree-sitter==0.5.1`
5. codemod—`codemod@latest mcp`
6. lsp-bash—`lsp-mcp-server`
7. ast-grep—`@notprolands/ast-grep-mcp`
8. atlassian—`mcp-atlassian` (Jira + Confluence, uses 1Password for tokens)
9. sequential-thinking—`@modelcontextprotocol/server-sequential-thinking`
10. todoist—`mcp-remote https://ai.todoist.net/mcp`

If ANY are currently set to `"disabled": true` or have been removed from the template, flag as an issue.

### Phase 3: Query Pieces LTM

Search terms: "mcp-proxy configuration", "mcp-proxy timeout", "hermes mcp servers disabled", "smart-mcp-proxy", "mcp_proxy.json.tmpl", "chezmoi mcp"

### Phase 4: Produce the Robustness Plan

4a. Resilience at the Proxy Layer—health checks, per-server timeouts, retry/backoff, graceful degradation, connection pooling.

4b. Process Management—launchd/systemd, auto-restart, log rotation, startup ordering (Pieces OS before pieces MCP).

4c. Configuration Integrity—chezmoi template as single source of truth; no direct edits to `~/.config/mcpproxy/mcp_proxy.json`; prevent future agents from disabling servers; propose drift detection (`chezmoi verify` or diff check).

4d. Multi-Consumer Consistency—Hermes, Claude Code, Cursor, Gemini all consume proxy at `http://127.0.0.1:8000/mcp/`; ensure consistent generated config; consider per-consumer endpoints vs shared.

4e. Restore Disabled Servers—produce exact diff to restore all 10 servers to `"disabled": false` in the chezmoi template (do NOT apply).

### Output Format

1. Research Findings
2. LTM Context
3. Current State Audit
4. Proposed Plan
5. Proposed Diffs (DO NOT APPLY)

### Constraints

- Do NOT run any Python code—use only terminal commands and file read/write tools.
- Do NOT modify any files until explicitly approved.
- Do NOT disable any servers.
- Only look at files inside `~/.local/share/chezmoi/` for source-of-truth config.
- Look at `~/.config/mcpproxy/` only to check for drift against the chezmoi source.