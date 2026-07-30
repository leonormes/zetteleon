---
created: 2026-04-14T17:46:24+00:00
created_utc: '2026-04-14T12:20:00Z'
kind: claim
modified: 2026-07-28T09:12:49+00:00
permalink: llmeon/30-library/100-zettelkasten/paxos-vs-raft-correctness-vs-intuition
source_title: The Fundamental Challenge of Concurrent and Distributed Systems
source_url: http://www.youtube.com/watch?v=U719vQz-WFs
status: seed
tags: [consensus, correctness, intuition, paxos, raft]
title: Paxos vs Raft (Correctness vs Intuition)
type: atom
upstream: '[[SoT - Rust Concurrency & Async Paradigms]]'
---

## Paxos Vs Raft (Correctness Vs Intuition)

The selection of consensus protocols in industry often prioritises intuitive understandability (e.g., the Raft algorithm) over formal mathematical rigour (e.g., Paxos). While Raft provides "warm fuzzy feelings" of understanding, Paxos remains the primary protocol grounded in formal proofs of correctness, highlighting a tension between developer experience and absolute technical rigour.

### Scope & Conditions

Applies to the architectural selection of consensus protocols for distributed databases and orchestration tools.

### Evidence

> "practitioners prioritise 'warm fuzzy feelings' of intuitive understanding (e.g., the Raft algorithm) over formal proofs of correctness."

### Implications

- Intuitive understanding can be a distraction from, or even a substitute for, formal mathematical verification.
- The industry preference for "understandable" protocols may incur a cost in terms of provable system reliability.

### Related

- [[SoT - Pragmatism vs Rigour in Software]]—shared mechanism: the trade-off between the "fuzzy feelings" of pragmatism and the "certainty" of rigour.
- [[The Illusion of Fluency is a Cognitive Bias Where Ease of Processing is Mistaken for Deep Learning]]—shared mechanism: mistaking the ease of understanding a protocol (Raft) for its fundamental correctness.

### See Also

- [[SoT - State Synchronization Models]]
