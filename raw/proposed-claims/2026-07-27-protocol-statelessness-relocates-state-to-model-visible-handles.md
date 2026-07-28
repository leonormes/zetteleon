---
title: Protocol-level statelessness relocates agent state into explicit handles the model can reason about
type: claim-stub
status: proposed
created: 2026-07-27 17:30:00+01:00
source_raw: '[[raw/2026-07-27-thenewstack-mcp-spec-rewrite]]'
claim_statement: Removing protocol-level sessions does not remove state; it relocates state from transport metadata the model cannot see into explicit handles that appear in tool results, and this relocation is a capability gain rather than merely a scaling fix, because a handle can be composed across tools and passed between workflow steps while a session ID never could.
steel_man: Hidden transport state is a feature, not a defect. A session ID that never enters the context window costs no tokens, cannot be leaked into a transcript or log, cannot be hallucinated or corrupted by the model, and cannot be replayed by anyone reading the conversation. Making state model-visible trades a well-understood infrastructure problem (session affinity, which load balancers have solved for decades) for a poorly-understood security surface, and pushes the burden of authorization onto every individual tool author.
tags:
- claim-stub
- agent-proposed
- domain/llm
- topic/mcp
- topic/context-engineering
permalink: llmeon/raw/proposed-claims/2026-07-27-protocol-statelessness-relocates-state-to-model-visible-handles
---

## Supporting Context

The MCP 2026-07-28 revision removes the `initialize`/`initialized` handshake (SEP-2575) and the `Mcp-Session-Id` header (SEP-2567), moving protocol version, client info and client capabilities into `_meta` on every request [source: raw/2026-07-27-thenewstack-mcp-spec-rewrite]. State that genuinely must persist moves to the explicit handle — "the pattern every shopping cart built over HTTP has used for twenty years" — where a tool mints an id, returns it in the result, and the model passes it back as an ordinary argument [source: raw/2026-07-27-thenewstack-mcp-spec-rewrite]. The source is explicit that the significance is not only operational: "What makes the handle more than a workaround is that it is visible to the model. Session state hidden in transport metadata was something the model could never reason about, whereas a handle in a tool result can be composed across tools and handed between workflow steps" [source: raw/2026-07-27-thenewstack-mcp-spec-rewrite]. The stated cost is that the handle also appears in prompts, transcripts and logs, so it must be bound to the authenticated principal and permission-checked on each use rather than treated as proof of authorization [source: raw/2026-07-27-thenewstack-mcp-spec-rewrite]. This is the same move the vault already records in a different domain: encoding relevance as structure the model can traverse rather than state it must search for (see [[Targeting LLM Attention Requires Encoding Relevance as Structure]]) [inference].

<!-- Intentionally left blank for human completion per AGENTS.md §2.4 -->
## Falsifiers

## Crux

## Confidence

## Counter Positions
