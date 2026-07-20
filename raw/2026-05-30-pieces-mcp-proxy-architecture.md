---
created: 2026-05-30T08:31:27+00:00
modified: 2026-07-20T16:32:49+00:00
permalink: llmeon/raw/2026-05-30-pieces-mcp-proxy-architecture
pieces_ids: [34f55864-12a6-4948-a355-1c70f614ef14, f2b0b1b0-3b96-4697-aa75-150caec71cae]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-30-pieces-mcp-proxy-architecture
---

## Asset 1 (Pieces: 34f55864-12a6-4948-a355-1c70f614ef14)

The user is asking about separating their MCP (Model Context Protocol) proxy server setup from their LLM client (Hermes with --tui flag) so that Hermes loads quickly without waiting for the MCP server to initialize. Let me search their memory for context about their setup - what tools they use, how they've configured things, etc.

Let me search for relevant information about their MCP setup, Hermes configuration, and any related work they've done.

---

## Asset 2 (Pieces: f2b0b1b0-3b96-4697-aa75-150caec71cae)

I have been trying to centralise my mcp servers. I want the mcp-proxy to run independantly of any llm, but each llm should know about it and be able to use it. I use llm all the time so it is ok to have the mcp-proxy running all the time. at the moment it seems that when I start herme --tui it takes over 60secs to load. I think it is waiting on the mcp server. How can we seperate them so that hermes loads quickly but still has access to the mcp
