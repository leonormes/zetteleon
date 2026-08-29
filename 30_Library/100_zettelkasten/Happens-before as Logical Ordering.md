---
created: 2026-04-14T17:44:07+00:00
created_utc: '2026-04-14T12:20:00Z'
kind: definition
modified: 2026-08-29T09:36:01+00:00
permalink: llmeon/30-library/100-zettelkasten/happens-before-as-logical-ordering
source_title: The Fundamental Challenge of Concurrent and Distributed Systems
source_url: http://www.youtube.com/watch?v=U719vQz-WFs
status: seed
tags: [distributed-systems, happens-before, logical-time, relativity]
title: Happens-before as Logical Ordering
type: atom
upstream: '[[SoT - Rust Concurrency & Async Paradigms)]]'
---

## Happens-before as Logical Ordering

The "Happens-before" relation is a logical framework for ordering events in a distributed system without relying on a global clock. Derived from the special relativity view of spacetime, it dictates that event A occurs before event B only if a signal could have travelled from A to B, providing a partial ordering necessary for state machine synchronisation.

### Scope & Conditions

Foundational principle for reasoning about event order and consistency in distributed environments.

### Evidence

> "The 'Happens-before' relation… dictates that event A occurs before event B only if a signal could have travelled from A to B."

### Implications

- Replaces physical time with causal dependencies as the primary ordering mechanism.
- Enables the consistent synchronisation of state across multiple, independent nodes.

### Related

- [[Special Relativity (Everyday Consequences)]]—shared mechanism: both rely on the speed of light/signal as the universal limit for causality.
- [[The Universal Speed of Causality]]—direct concept match: both define causality through signal propagation.

### See Also

- [[SoT - Process Execution (Kernel Logic)]]
