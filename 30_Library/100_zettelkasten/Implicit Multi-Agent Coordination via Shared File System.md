---
conformant: false
created: 2026-04-10T12:00:00+00:00
modified: 2026-07-21T09:15:06+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/implicit-multi-agent-coordination-via-shared-file-system
tags: [coordination, determinism, file-system, multi-agent-systems]
title: Implicit Multi-Agent Coordination via Shared File System
type: claim
---

## Implicit Multi-Agent Coordination via Shared File System

In the CORAL framework, global coordination between parallel autonomous agents is achieved implicitly: agents read and write a shared, hierarchical directory rather than sending messages to one another. No agent ever calls another agent directly; consensus and awareness emerge through the file system as a shared ledger.

### Scope & Conditions

Demonstrated with 4–8 homogeneous agents running in parallel Git workspaces. The approach is deterministic rather than probabilistic—the file system provides an immutable audit trail of every agent action and hypothesis. Does not address conflict resolution when two agents write the same file simultaneously.

### Evidence

> "Global coordination between agents is achieved implicitly through a shared public directory, rather than direct communication" [04:10]

### Implications

- Eliminates communication overhead and state-synchronisation complexity common in message-passing multi-agent designs.
- Produces a deterministic, human-readable audit trail as a side-effect of normal operation, simplifying debugging and post-hoc analysis.

### Related

- [[Virtual File System for Agent Concurrency]]—direct concept match: the CORAL shared directory and the virtual file system pattern both use a filesystem abstraction as the coordination primitive for concurrent agents; CORAL uses a real hierarchical directory on disk rather than an in-memory dict, but the architectural role is identical.
- [[SoT - Agentic AI Design Patterns]]—extends: implements the "Multi-Agent Collaboration" and "Inter-Agent Communication" patterns from the taxonomy but replaces structured message-passing protocols with passive shared-state reads and writes.
