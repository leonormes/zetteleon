---
type: wiki
title: 'Fix: Claude Code Jira MCP Connectivity'
tags:
- hermes
- solution
- infra
- mcp
- jira
- claude-code
actor: agent/hermes/mechanical-lead
generated: 2026-09-01 10:55:00+01:00
verified: 2026-09-01 10:55:00+01:00
stale_after: 2026-12-01
permalink: llmeon/wiki/2026-09-01-fix-claude-code-jira-mcp
---

# Fix: Claude Code Jira MCP Connectivity

## Problem

Claude Code (`claude --print`) couldn't access live Jira data. `claude mcp list` showed:

```
1mcp: http://127.0.0.1:3050/mcp?app=claude-code (HTTP) - ! Connected · tools fetch failed — Request timed out
```

The `1mcp` proxy connected but the initial `tools/list` request timed out because 1MCP aggregates 15 upstream MCP servers (obsidian ×2, serena, pieces, ast-grep, lsp-bash, etc.) and their combined initialization exceeds Claude Code's HTTP MCP client timeout.

## Root cause

1. Claude Code's `CLAUDE.md` pointed to `http://127.0.0.1:3050/mcp?app=claude-code` (1MCP proxy)
2. 1MCP's `tools/list` timed out because 15 servers need to respond before the list is returned
3. This is a latent issue: Hermes sessions have a longer timeout and tolerate the delay, but Claude Code's MCP HTTP client is stricter

## What was verified working

- 1MCP is live and healthy (`curl -sf http://127.0.0.1:3050/health/live`)
- Atlassian server is healthy within 1MCP (15/15 servers healthy)
- `JIRA_API_TOKEN` is properly resolved via `op run --env-file=secrets.env` → `envsubst` → `mcp.resolved.json`
- `gk provider list` shows Jira as connected (`✓`)
- Jira REST API works directly (tested: `GET /rest/api/2/issue/FTFL-1000`)

## Fix

Added the Atlassian Jira MCP server **directly** to Claude Code's config, bypassing the 1MCP proxy:

```bash
claude mcp add atlassian-jira \
  --scope user \
  -e JIRA_URL="https://fitfile.atlassian.net" \
  -e JIRA_USERNAME="leon.ormes@fitfile.com" \
  -e JIRA_API_TOKEN="$JIRA_API_TOKEN" \
  -e CONFLUENCE_URL="https://fitfile.atlassian.net/wiki" \
  -e CONFLUENCE_USERNAME="leon.ormes@fitfile.com" \
  -e CONFLUENCE_API_TOKEN="$CONFLUENCE_API_TOKEN" \
  -- uvx mcp-atlassian
```

Stored in `~/.claude.json` (user scope). The `JIRA_API_TOKEN` value came from `~/.local/state/1mcp/mcp.resolved.json` which is populated by the `op run` service account mechanism in `run-1mcp.sh`.

## Verification

```
claude mcp list
...
atlassian-jira: uvx mcp-atlassian - ✔ Connected
```

## FTFL-1000 data (fetched via REST API during fix)

| Field | Value |
|-------|-------|
| Key | FTFL-1000 |
| Summary | Pipeline Performance & Reliability |
| Status | Backlog |
| Type | Epic |
| Priority | Medium |
| Assignee | Unassigned |
| Created | 2026-08-26T13:56:10+01:00 |
| Updated | 2026-08-26T14:03:14+01:00 |

## Related

- `~/.config/1mcp/mcp.json` — 1MCP config with the Atlassian server referencing `${JIRA_API_TOKEN}`
- `~/.config/1mcp/secrets.env` — `op://` references resolved by `op run`
- `~/.config/1mcp/run-1mcp.sh` — LaunchAgent script that resolves secrets via 1Password service account