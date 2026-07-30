---
conformant: true
created: 2026-07-27T17:50:00+01:00
modified: 2026-07-28T09:12:53+00:00
permalink: llmeon/30-library/100-zettelkasten/evidence-mcp-2026-07-28-removes-protocol-sessions-in-favour-of-explicit-handles
source_quote: "What makes the handle more than a workaround is that it is visible to the model. Session state hidden in transport metadata was something the model could never reason about, whereas a handle in a tool result can be composed across tools and handed between workflow steps."
source_reference: "The New Stack, 'MCP's biggest update removes the machinery many servers were built around', 2026-07-27 — https://thenewstack.io/mcp-release-candidate-rewrite/. Corroborated against the official MCP release post (blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) and the specification changelog; SEP-2567 (session removal) and SEP-2575 (handshake removal) confirmed."
supports_claims: ["[[Protocol Statelessness Relocates Agent State into Model-Visible Handles]]"]
tags: [domain/llm, topic/context-engineering, topic/mcp, type/evidence]
title: Evidence - MCP 2026-07-28 Removes Protocol Sessions in Favour of Explicit Handles
type: evidence
---

## Evidence - MCP 2026-07-28 Removes Protocol Sessions in Favour of Explicit Handles

### The Quote

> "What makes the handle more than a workaround is that it is visible to the model. Session state hidden in transport metadata was something the model could never reason about, whereas a handle in a tool result can be composed across tools and handed between workflow steps."

### What Was Changed, Specifically

The Model Context Protocol revision dated 2026-07-28 removes two things that had been foundational since launch:

- The `initialize`/`initialized` handshake (SEP-2575). Protocol version, client info and client capabilities now travel in `_meta` on every request instead of being exchanged once at connect time.
- The protocol-level session and its `Mcp-Session-Id` header (SEP-2567). That header previously pinned a client to the instance that issued it.

State that genuinely must persist is not abolished—it moves to the explicit handle: a tool mints an identifier, returns it in the result, and the model passes it back as an ordinary argument on the next call. The release post names the governing principle _pay-as-you-go complexity_: the core stays lean, and statefulness appears only where a feature genuinely needs it.

### Why This Counts as Evidence rather than just News

The claim it supports is about _where state lives and who can see it_, not about MCP. What makes this a useful data point is that the maintainers made the visibility argument themselves, and made it as a design justification rather than a side effect. They could have justified session removal purely on scaling grounds—session affinity, shared session stores, MCP-aware gateway routing—and those arguments are in the source too. They went further and argued that a model-visible handle is _better_ than hidden transport state because the model can compose it.

That is an independent party, in protocol design rather than prompt or context engineering, arriving at the same principle the vault already holds about attention and structure.

### The Stated Cost

The source does not present this as free, and the counterweight belongs here:

> "The trade-off is that it also appears in prompts, transcripts, and logs, so bind it to the authenticated principal and verify permissions with each use instead of considering it as proof of authorization."

Making state visible to the model necessarily makes it visible to everything else reading the context window. The security burden moves to the tool author.

### Confidence: 0.85

High, but not 1.0. The factual claims about what the specification removes are independently corroborated and carry SEP numbers. The _interpretive_ claim—that model-visibility is a capability gain rather than an incidental consequence of a scaling fix—is the source's argument, made by a journalist summarising the maintainers, not a measured result. No benchmark demonstrates that agents actually compose handles better than they handled sessions.

### Provenance

Raw capture: [[raw/2026-07-27-thenewstack-mcp-spec-rewrite]]

Originating workbench note: [[HEAD MCP’s biggest update removes the machinery many servers were built around]]

%%[supports:: [[Protocol Statelessness Relocates Agent State into Model-Visible Handles]], strength=4, confidence=high]%%
