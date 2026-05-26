---
created: 2026-05-23T20:15:00+01:00
modified: 2026-05-26T11:43:32+00:00
pieces_ids: ["17a5978e-4cc2-4a6e-93d8-8dca33bb5109", "991b3b21-9faf-4743-a76f-129642603351", "f79dcc22-400c-4969-bec9-268e7bce00e0"]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-23-pieces-hermes-tui-slow
---

## Hermes TUI Slow Startup Diagnosis

### Asset 1 (Pieces: 17a5978e-4cc2-4a6e-93d8-8dca33bb5109)

Here is the `/goal` prompt, grounded in your specific config (chezmoi-managed, qwen/qwen3.5:cloud, honcho memory, MCP servers including `mcp-proxy`/graphify/pieces SSE, multiple profiles, 81 skills, and a recent migration to v0.13.0).

---

### `/goal` prompt—paste Into `hermes --tui`

```
/goal

## GOAL
Diagnose and fix the slow startup time when running `hermes --tui`. Currently taking 30–40+ seconds to reach a usable state. The fix must be persisted via chezmoi (source: ~/.local/share/chezmoi/).
```

### Asset 2 (Pieces: 991b3b21-9faf-4743-a76f-129642603351)

The user wants me to search their memory for context about "hermes" - specifically what it is, how it's configured, and any relevant details that would help craft a `/goal` prompt for debugging and fixing slow loading times.

### Asset 3 (Pieces: f79dcc22-400c-4969-bec9-268e7bce00e0)

User request: my hermes takes a long time to load. I am using `hermes --tui` but it is taking 30-40 seconds or more to get to a usable state. give me a /goal prompt to get hermes to debug and fix the config
