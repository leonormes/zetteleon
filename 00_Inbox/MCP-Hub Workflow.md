---
created: 2026-01-11T17:05:53+00:00
modified: 2026-01-11T17:06:24+00:00
title: MCP-Hub Workflow
---

# MCP-Hub Workflow

The development environment has been transitioned to a unified MCP (Model Context Protocol) Hub architecture. This centralises the management of all MCP servers, providing a single endpoint for AI assistants (like Gemini CLI, Claude Code, or Cursor).

## Architecture Overview

- Orchestrator: `mcp-hub` (installed via `mise` as a global npm package).
- Configuration: Managed via `~/.config/mcphub/config.json` (Source: `chezmoi` template).
- Unified Endpoint: `http://localhost:37373/mcp`
- Clients: Gemini CLI is configured to use only the Hub URL.

## Configured Servers

The following servers are currently managed by the Hub:

1. memory: The standard `@modelcontextprotocol/server-memory` for long-term fact retention.
2. obsidian-mcp-tools: Integration for vault management and note creation.

## Key Benefits

- Deterministic Resolution: No more conflicting command paths across macOS and Linux.
- Hot Reloading: The Hub can watch config changes and restart servers without restarting the main AI session.
- Lower Overhead: Clients only maintain one connection instead of spawning multiple processes.

## Management Commands

- Start Hub: `systemctl --user start mcp-hub`
- Check Logs: `journalctl --user -u mcp-hub -f`
- Configuration Path: `~/.local/share/chezmoi/dot_config/mcphub/config.json.tmpl`

---

_Created by Gemini CLI - 2026-01-11_
