---
title: "MCP Proxy Robustness and High Availability"
wiki_type: dossier
entity_kind: project
created: 2026-05-08T16:02:00+00:00
modified: 2026-05-08T16:02:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-05-08-pieces-mcp-proxy-robustness.md
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

## Timeline

- **2026-05-08 ~11:41** — Hermes disables ast-grep, atlassian, todoist, and sequential-thinking in the mcp-proxy config.
- **2026-05-08 ~14:26** — Leon drafts a prompt for his coding agent to plan robustness improvements, restore disabled servers, and prevent future unauthorised changes.

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
