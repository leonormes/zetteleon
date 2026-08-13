---
conformant: true
contradicts: []
created: 2026-07-27T17:52:00+01:00
epistemic_status: medium
evidence_links: ["[[Evidence - MCP 2026-07-28 Removes Protocol Sessions in Favour of Explicit Handles]]"]
modified: 2026-08-13T10:56:58+00:00
permalink: llmeon/30-library/100-zettelkasten/protocol-statelessness-relocates-agent-state-into-model-visible-handles
proposition: Removing protocol-level sessions does not remove state but relocates it from transport metadata the model cannot see into explicit handles that appear in tool results, and this relocation is a capability gain rather than merely a scaling fix, because a handle can be composed across tools and passed between workflow steps while a session identifier never could.
status: draft
tags: [domain/llm, topic/agent-architecture, topic/context-engineering, topic/mcp]
title: Protocol Statelessness Relocates Agent State into Model-Visible Handles
type: claim
---

## Protocol Statelessness Relocates Agent State into Model-Visible Handles

When a protocol drops sessions, the tempting reading is that it has been simplified—one less thing to run, one less thing to break. That reading misses what actually happened. The state did not go anywhere. It moved from a place the model could not see into a place it can.

A session identifier lives in transport metadata. It does its job invisibly: the client holds it, the server recognises it, and the model orchestrating the work has no idea it exists. It cannot reason about it, cannot pass it to a different tool, cannot decide that the thing it is holding is the same thing another tool wants. The state is real and load-bearing, and the reasoning layer is blind to it.

A handle lives in a tool result. It is an ordinary value in the context window—which means the model can carry it between steps, hand it to a different tool, and treat it as a first-class object in a plan. The capability that appears is not persistence; persistence was always there. What appears is composability.

### Why This is the Same Move as Encoding Relevance as Structure

The vault already holds the principle in a different domain: attention should be targeted by structure the model can traverse, never by volume it must search through ([[Targeting LLM Attention Requires Encoding Relevance as Structure]]). Hidden session state is the degenerate case of that failure—not merely hard to search, but genuinely unreachable. Making it an explicit handle is the same corrective applied at the protocol layer rather than the context layer: put the thing that matters somewhere the model can address it directly.

That two independent design communities—one worrying about codebase context, one about transport semantics—arrive at the same rule is the reason this claim is worth holding separately from the MCP change that prompted it. The claim is about state visibility as an architectural property. MCP is the instance.

### Scope and Conditions

The claim holds for state a reasoning agent needs to _act on_. It does not hold, and should not be stretched, to cover state the model has no business touching: credentials, internal routing, connection pooling, or anything whose exposure in a transcript would be a defect. The protocol's own guidance is that a handle must be bound to the authenticated principal and permission-checked on every use rather than treated as proof of authorization—precisely because visibility to the model means visibility to everything else that reads the context window.

There is also a cost the enthusiasm tends to skip. Handles consume context budget, appear in logs and transcripts, and can be hallucinated or corrupted in a way an opaque session identifier never could. The trade is real; it is just a better trade than it first appears.

### Open Question

Does the composability benefit show up in practice, or only in principle? Nothing measured demonstrates that agents actually chain handles across tools more successfully than they coped with sessions. The argument is a good one and it is currently an argument, which is why `epistemic_status` is `medium` rather than `high`.

### Provenance

Promoted from `raw/proposed-claims/2026-07-27-protocol-statelessness-relocates-state-to-model-visible-handles` (Hermes vault) on 2026-07-27 by explicit human instruction (AGENTS.md §2.4 scope override—see `log.md`).

Raw source: `raw/2026-07-27-thenewstack-mcp-spec-rewrite` (Hermes vault)

### Steelman of the Opposing view

Hidden transport state is a feature, not a defect. A session identifier that never enters the context window costs no tokens, cannot leak into a transcript or log, cannot be hallucinated or corrupted by the model, and cannot be replayed by anyone reading the conversation. Making state model-visible trades a well-understood infrastructure problem—session affinity, which load balancers have solved for decades—for a poorly-understood security surface, and pushes the burden of authorization onto every individual tool author.

%%[supports:: [[Targeting LLM Attention Requires Encoding Relevance as Structure]], strength=4, confidence=medium]%%
