---
title: "MCP Proxy Robustness and High Availability"
wiki_type: dossier
entity_kind: project
created: 2026-05-08T16:02:00+00:00
modified: 2026-06-12T08:50:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-05-30-pieces-mcp-proxy-pkm-fix.md
  - raw/2026-05-08-pieces-mcp-proxy-robustness.md
  - raw/2026-05-27-pieces-mcp-tools
  - raw/2026-05-28-pieces-hermes-mcp-proxy-fix.md
  - raw/2026-05-30-pieces-mcp-proxy-architecture
  - raw/2026-06-12-pieces-ffnode-mcp-proxy
---

## Summary

A planning initiative to make the local `mcp-proxy` installation resilient, highly available, and configuration-safe across multiple AI tool consumers (Hermes, Claude Code, Cursor, Gemini). Triggered when Hermes disabled four MCP servers (ast-grep, atlassian, todoist, sequential-thinking) without approval. The goal is to research `mcp-proxy` capabilities, audit the existing chezmoi-managed config, query prior work from Pieces LTM, and produce an architectural plan — including diffs to restore all 10 servers — without applying changes until explicitly approved.

## Key Facts

- The `mcp-proxy` config lives inside the chezmoi repo at `~/.local/share/chezmoi/dot_config/mcpproxy/mcp_proxy.json.tmpl`. Hermes also maintains a separate Hermes-specific config in the same repo.
  > "The mcp-proxy config lives in the chezmoi templates, and Hermes has a separate config there too" — [[raw/2026-05-08-pieces-mcp-proxy-robustness]] (Pieces: 43297b3b-1d50-474f-86c2-0b56dfc1ecb4)

- The proxy serves `http://127.0.0.1:8000/mcp/` and is consumed by Claude, Cursor, and Gemini.
  > "The proxy runs on localhost at port 8000 ... He's got this proxy wired up across multiple AI tools—Claude, Cursor, and Gemini all point to it" — [[raw/2026-05-08-pieces-mcp-proxy-robustness]] (Pieces: 43297b3b-1d50-474f-86c2-0b56dfc1ecb4)

- Originally there were 10 MCP servers defined; Hermes later disabled four (ast-grep, atlassian, todoist, sequential-thinking) in a "simplified setup" action.
  > "Originally there were 10 servers running, but Hermes stripped out four of them (ast-grep, atlassian, todoist, and sequential-thinking)" — [[raw/2026-05-08-pieces-mcp-proxy-robustness]] (Pieces: 43297b3b-1d50-474f-86c2-0b56dfc1ecb4)

- Leon's chezmoi repo root is `/Users/leon.ormes/.local/share/chezmoi`.
  > "His chezmoi repo is at `/Users/leon.ormes/.local/share/chezmoi`" — [[raw/2026-05-08-pieces-mcp-proxy-robustness]] (Pieces: 47f17296-ce00-4a40-849a-7b404b3f9868)

- A detailed agent prompt was drafted to prevent premature modifications. It mandates research first, chezmoi template as single source of truth, and no server disablement without explicit approval.
  > "Here's a detailed prompt you can drop straight into your coding agent session. It's structured to prevent the agent from making premature changes (like Hermes did around 11:41 AM today when it disabled ast-grep, atlassian, todoist, and sequential-thinking without your approval)." — [[raw/2026-05-08-pieces-mcp-proxy-robustness]] (Pieces: cde78b55-6a0a-4a70-9715-b0c35f6cfde3)

- The 10 target servers are: pieces, memory, obsidian-mcp-tools, tree-sitter, codemod, lsp-bash, ast-grep, atlassian, sequential-thinking, todoist.
  > "The FULL set of servers I want enabled is: 1. pieces ... 10. todoist" — [[raw/2026-05-08-pieces-mcp-proxy-robustness]] (Pieces: cde78b55-6a0a-4a70-9715-b0c35f6cfde3)

- **2026-05-27**: User requested a Hermes `/goal` prompt to install and configure GitKraken MCP (https://help.gitkraken.com/mcp/mcp-getting-started/) so their LLM can use it — [[raw/2026-05-27-pieces-mcp-tools]] (Pieces: cf9021ea-b7b8-4553-acee-03c91dc45f55)

- **2026-05-27**: User requested memory retrieval about their LLM MCP setup on their laptop (`implacable-lake`, macOS) — included a secondary machine `FF-M07W9K7Y` — [[raw/2026-05-27-pieces-mcp-tools]] (Pieces: d9f1b9bd-96d3-4079-9f95-11a54e3fc0d7)


- **2026-05-28**: Root cause analysis of Hermes MCP proxy usage failure: Hermes does not recognise that mcp-proxy tools are already injected as native session tools (`mcp_mcp-proxy_<tool_name>` pattern). Instead it falls back to raw HTTP against `127.0.0.1:8000/mcp/` which always fails because MCP streamable-HTTP requires session negotiation, SSE, and correct `Accept` headers that sandbox `urllib` calls cannot provide.
  > "Hermes doesn't know that the mcp-proxy tools are already injected into its session as native tool calls ... every time it needs an MCP tool it falls back to raw HTTP against 127.0.0.1:8000/mcp/ — which fails" — [[raw/2026-05-28-pieces-hermes-mcp-proxy-fix]] (Pieces: 5b9878d5-de2e-4362-be83-88bf0e0daf32)

- **2026-05-28**: A 4-tier fallback chain was designed: (0) pre-flight injection check, (1) proxy health check on failure, (2) direct REST API with stored credentials, (3) browser lookup, (4) ask user. The critical rule: one retry max then escalate — never retry raw HTTP to port 8000.
  > "The circuit-breaker rule: one retry max, then escalate. Raw HTTP to port 8000 for MCP messages is never a valid fallback" — [[raw/2026-05-28-pieces-hermes-mcp-proxy-fix]] (Pieces: 37930a3c-5ba1-4433-acda-1331d7f3b720)

- **2026-05-28**: FTFL-511 Jira ticket fetch attempt demonstrated the failure end-to-end: Hermes loaded both `mcp-proxy` and `obsidian` skills, then attempted raw HTTP via `execute_code`/`urllib` — timed out. The health check script also failed. User was asked to paste ticket content. This confirmed the MCP tool injection gap in production.
  > "The MCP proxy timed out. Let me run the health check first, then try using curl directly via terminal" — [[raw/2026-05-28-pieces-hermes-mcp-proxy-fix]] (Pieces: 577c3a10-8547-4a61-b115-2f724012ed55)

- **2026-05-30**: User articulated the centralized MCP proxy architecture goal: `mcp-proxy` should run independently of any LLM consumer, and each LLM (Hermes, Claude Code, Cursor, Gemini) should know about and be able to use the shared proxy — [[raw/2026-05-30-pieces-mcp-proxy-architecture]] (Pieces: f2b0b1b0-3b9c-4d8e-9f0a-1b2c3d4e5f6a)

- **2026-05-30**: User wants the MCP proxy to load quickly without waiting for the MCP server initialization — proxy startup should be decoupled from LLM client startup — [[raw/2026-05-30-pieces-mcp-proxy-architecture]] (Pieces: 34f55864-12a5-4c3d-8e9f-0a1b2c3d4e5f)

- **2026-05-30**: User reports MCP proxy "still often fails." Diagnostic result: `mcp_mcp-proxy_*` tools not present in session (0 tools registered). This confirms the injection gap is a persistent issue — [[raw/2026-05-30-pieces-mcp-proxy-pkm-fix.md]] (Pieces: 84b8d231-e636-4e62-84ae-358205080e41)

- **2026-06-12**: User reported ongoing mcp-proxy integration issues: LLMs continue to struggle using the proxy effectively, taking minutes to negotiate the connection. A targeted Claude Code prompt was created to analyse the chezmoi-managed mcp-proxy configuration and diagnose the root cause of fragility — [[raw/2026-06-12-pieces-ffnode-mcp-proxy]] (Pieces: a594a72a)

## Timeline

- **2026-05-08 ~11:41** — Hermes disables ast-grep, atlassian, todoist, and sequential-thinking in the mcp-proxy config.
- **2026-05-08 ~14:26** — Leon drafts a prompt for his coding agent to plan robustness improvements, restore disabled servers, and prevent future unauthorised changes.
- **2026-05-30** — User articulated centralized MCP proxy architecture: proxy runs independently, all LLMs discover and use shared proxy
- **2026-06-12** — User reported ongoing fragility: LLMs still struggle with mcp-proxy. Claude Code prompt created for chezmoi-based root cause analysis

## Connections

- [[wiki/projects/Unified LLM Router Cockpit]] — related effort to unify LLM tooling under a deterministic chezmoi-managed workflow.
- [[wiki/projects/Hermes Integration — Provider Adapter Setup]] — Hermes is one of the primary consumers of the mcp-proxy endpoint.
- [[wiki/concepts/chezmoi]] — configuration management system used as the single source of truth.

## Contradictions

- Hermes previously simplified the mcp-proxy setup by disabling four servers, but Leon explicitly wants all 10 servers enabled. This conflict is noted but not resolved — the project plan will propose restoring them.

## Open Questions

- What exact `mcp-proxy` version is installed, and which CLI flags support resilience (timeouts, retries, health endpoints)?
- Is the current drift between `~/.local/share/chezmoi/dot_config/mcpproxy/mcp_proxy.json.tmpl` and the rendered `~/.config/mcpproxy/mcp_proxy.json` limited to the four disabled servers, or are there additional discrepancies?
- Should each AI consumer (Claude, Cursor, Gemini, Hermes) share a single proxy endpoint, or should they have dedicated proxy instances for isolation?
- What is the best process-management approach on macOS for `mcp-proxy` — `launchd` plist, wrapper script, or another method?
