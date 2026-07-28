---
title: MCP 2026-07-28 specification rewrite — sessions and initialization handshake removed
type: source
created: 2026-07-27T17:03:36+01:00
source_url: https://thenewstack.io/mcp-release-candidate-rewrite/
source_title: "MCP's biggest update removes the machinery many servers were built around"
source_outlet: The New Stack
captured_from: "[[HEAD MCP’s biggest update removes the machinery many servers were built around]]"
corroboration: high
tags: [raw, source, domain/llm, topic/mcp, agent-ingested]
permalink: llmeon/raw/2026-07-27-thenewstack-mcp-spec-rewrite
---

## Provenance & trust

**Corroboration: HIGH.** Independently confirmed against the official MCP blog (`blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/`), the MCP spec changelog, and multiple third-party write-ups (Microsoft Community Hub, WorkOS, HackerNoon, Stacktree). SEP numbers cited below appear in the official release post. Release candidate frozen 21 May 2026; final specification 28 July 2026.

## Extracted claims

### On what is removed

- The `initialize`/`initialized` handshake is removed entirely (SEP-2575). Protocol version, client info and client capabilities now travel in `_meta` on **every** request.
- The protocol-level session and the `Mcp-Session-Id` header are removed (SEP-2567). That header previously pinned a client to the issuing server instance.
- Three core features deprecated. Sampling and Logging are the sharpest cases.
- Resumability is gone: an interrupted in-flight request is reissued by the client under a new request ID.

### On why (the operator cost)

> "A team shipping an MCP server was paying to solve a distributed-systems problem the protocol had created for them."

- MCP's original shape was a desktop app talking to a local process over stdio, where a startup handshake over a long-lived connection was cheap.
- Remote, horizontally-scaled deployment turned sessions into a liability: scaling out required session affinity, an externally shared session store, **or MCP-aware gateway logic that parses JSON bodies to determine routing**.
- Capability negotiation added a second cost: capabilities exchanged once at connect time meant list results could vary by connection, making caching across sessions or in a shared intermediary hard to reason about.

### On the replacement mechanism

- Six Specification Enhancement Proposals converge on making every request stand on its own. `server/discover` makes server capabilities independently queryable.
- Stated design principle: **"pay-as-you-go complexity"** — the core stays lean; statefulness appears only where a feature genuinely needs it.
- State that genuinely must persist moves to the **explicit handle** — the pattern every HTTP shopping cart has used for twenty years. A tool mints a `basket_id`, returns it in the result, the model passes it back as an ordinary argument.

> "What makes the handle more than a workaround is that it is visible to the model. Session state hidden in transport metadata was something the model could never reason about, whereas a handle in a tool result can be composed across tools and handed between workflow steps."

- Trade-off: the handle also appears in prompts, transcripts and logs. Bind it to the authenticated principal and verify permissions on each use; do not treat it as proof of authorization.

### On gateways and platform teams

- A required `Mcp-Method` header, plus `Mcp-Name` for named tool/resource/prompt operations, lets a gateway rate-limit or authorize **by operation without inspecting the request body**.
- This only holds under the transport validation rules: the backend must reject any header disagreeing with the body, and a policy-enforcing intermediary must refuse protocol versions that don't guarantee the check. *"Skip that and a benign header can front a different call underneath."*

### On caching

- Affected list and read results must now carry `ttlMs` and `cacheScope`, modelled on HTTP `Cache-Control`. `ttlMs` is a freshness hint, not a promise the data still holds.
- Servers are asked to return tools in **deterministic order**, which the draft ties to better prompt-cache hit rates — potentially lower latency and token cost where the provider prices prompt caching.

### The stated caveat

> "Statelessness at the protocol layer buys routability, not determinism. Two replicas will accept the same request without consulting protocol state, and they will still return different answers if they run different versions or read different downstream data."

### On extensions and governance

- Extensions get namespaced identifiers (official under `io.modelcontextprotocol`, third-party under a reversed domain the author owns), their own `ext-` repositories and independent release cadences. Compared to Kubernetes CRDs.
- **Tasks** shipped as an experimental core feature in 2025-11-25, hit design problems in production, and has been redesigned as an extension. Moving it out of core is itself a breaking change; subsequent iterations are not, because extensions evolve via capability flags or settings-level versioning.
- Feature lifecycle policy: every feature has Active / Deprecated / Removed states with a **minimum twelve-month** window from the revision in which it first becomes Deprecated. Shortened only for an active security risk with a published advisory or documented exploitation, and ninety days is then the hard floor.
- A Standards Track proposal cannot reach Final until a matching scenario lands in the conformance suite.

> "For anyone who has to justify an MCP integration to a platform review board, a written deprecation guarantee is worth more than any capability in the release."

### On migration cost

- Servers that issued their own requests to the client move to the Multi Round-Trip Requests (MRTR) pattern: the server returns what it still needs, the client retries with the answers. The server must authenticate any echoed `requestState` that can influence authorization or business logic.
- **Sampling deprecation is a role change, not a swap.** A server using client-mediated Sampling needed no provider credentials and generally did not carry the model bill. Calling a provider API directly makes it a credential holder, a billing party, and a separate processor of user data.
- Logging: `stderr` and OpenTelemetry answer operator observability but give a remote client no equivalent of the structured log stream it used to receive.

> "The protocol stopped managing state, which is not the same as the state going away."

- Migration path: clients probe with `server/discover` first and fall back to `initialize` only on encountering a legacy-only server. A wire-level break with a negotiated path across it, not a flag day.
- Beta SDKs for Python, TypeScript, Go and C#; ten-week validation window.
