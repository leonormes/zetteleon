---
title: Deprecating client-mediated sampling converts tool servers from stateless intermediaries into credential holders, billing parties and data processors
type: claim-stub
status: proposed
created: 2026-07-27 17:34:00+01:00
source_raw: '[[raw/2026-07-27-thenewstack-mcp-spec-rewrite]]'
claim_statement: Removing a protocol's client-mediated inference path is not a like-for-like deprecation but a transfer of legal and commercial liability, because a server that previously borrowed the client's model access without holding credentials or paying the bill must, on migrating, become a credential holder, a billing party, and a separate processor of user data — three roles with compliance consequences that no migration guide frames as such.
steel_man: Client-mediated sampling was an architectural inversion that should never have shipped. A server reaching back into the client's model access inverts the trust relationship, gives the server an unbounded call on someone else's budget, and makes it impossible for the client to reason about what it is paying for. Making the server hold its own credentials and its own bill is the honest arrangement; the compliance burden is not new, it is finally landing on the party that was already making the decision.
tags:
- claim-stub
- agent-proposed
- domain/llm
- topic/mcp
- topic/agent-governance
- topic/data-protection
permalink: llmeon/raw/proposed-claims/2026-07-27-deprecating-client-mediated-sampling-transfers-liability-to-servers
---

## Supporting Context

Among the three core features deprecated in the MCP 2026-07-28 revision, the source identifies Sampling as "the sharpest case", noting that the deprecations "are migration directions rather than drop-in replacements" [source: raw/2026-07-27-thenewstack-mcp-spec-rewrite]. Specifically: "A server using client-mediated Sampling needed no provider credentials and generally did not carry the model bill, whereas calling a provider API directly turns it into a credential holder, a billing party, and a separate processor of user data" [source: raw/2026-07-27-thenewstack-mcp-spec-rewrite]. Logging follows a similar pattern — `stderr` and OpenTelemetry answer operator observability but give a remote client no equivalent of the structured log stream it previously received, so the capability is not replaced but redistributed [source: raw/2026-07-27-thenewstack-mcp-spec-rewrite]. The general form the source states is: "The protocol stopped managing state, which is not the same as the state going away" [source: raw/2026-07-27-thenewstack-mcp-spec-rewrite]. The third role — separate processor of user data — is the one with the sharpest consequences in a regulated or NHS-adjacent deployment, where adding a processor is a documentation and contractual event rather than a configuration change, and the twelve-month deprecation window is therefore a compliance timeline, not just an engineering one [inference].

<!-- Intentionally left blank for human completion per AGENTS.md §2.4 -->
## Falsifiers

## Crux

## Confidence

## Counter Positions
