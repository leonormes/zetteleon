---
created: 2026-04-10T13:00:00+00:00
modified: 2026-04-19T18:30:40+00:00
tags: [architecture, comparison, pgvector, qdrant, scalability]
title: Qdrant Outperforms PGVector for Search-Primary Architectures at Scale
---

## Qdrant Outperforms PGVector for Search-Primary Architectures at Scale

When performance, scalability, and heavy retrieval or filtering are the primary architectural requirements, use Qdrant over PGVector. PGVector is the pragmatic choice when you are already running Postgres and search volume is low. Qdrant is the deliberate choice when semantic search is the bottleneck or core feature.

### Scope & Conditions

Applies to architectural decisions at the point of selecting a vector store. The trade-off is convenience (PGVector—no new service, existing DB expertise) vs. capability ceiling (Qdrant—purpose-built for high-throughput retrieval). The guideline assumes search demand will exceed what PGVector can serve without significant query-time tuning.

### Evidence

> "Qdrant is recommended for applications where performance, scalability, and heavy retrieval/filtering are the primary focus [29:51]"

### Implications

- Prefer PGVector for early-stage products where operational simplicity matters more than retrieval performance.
- Adopt Qdrant when the semantic search path becomes the system's critical path, and latency or throughput under filtering load is observable.

### Related

- [[SoT - Agentic AI Design Patterns]]—extends: instantiates the "Resource-Aware Optimisation" pattern at the infrastructure layer—right tool matched to right load profile rather than a single general-purpose choice.
