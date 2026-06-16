---
created: 2026-04-23T15:27:21+00:00
modified: 2026-06-08T11:49:22+00:00
project_category: prodos
project_name: ProdOS
project_status: active
title: PKM should probably be proposition-centred, not topic-centred
type:
---

## PKM Should Probably Be Proposition-centred, not Topic-centred

A personal wiki is mostly about "What is X?" and "What facts do I have about X?". A thinking-oriented PKM is more like "What do I think is true about X?" and "How confident am I?".

### The Key Shift

Instead of organising around subjects, organise around beliefs, questions, models, and evidence. Organize around _propositions_.

#### The Five Core Note Types

To eliminate taxonomy bloat and infrastructure toil, ProdOS enforces exactly five note types:

| Note Type | Purpose | Example |
|:--- |:--- |:--- |
| Claim | A verifiable proposition or belief. The primary unit. | "Packet traces usually outperform dashboards for root-cause analysis." |
| Concept | A definition or distinction needed for thought. | "Congestion control", "epistemic status", "service mesh". |
| Evidence | Why you believe a claim (quotes, data, benchmarks). | A quote from a book, a benchmark result, or an incident log. |
| Question | An unresolved tension or uncertainty. | "When does eBPF actually reduce debugging clarity?" |
| Procedure | Repeatable, binary "know-how" (Protocols). | "How to debug DNS-01 cert-manager failures." |

Note on Maps: Index notes or Maps of Content (MOCs) may exist sparingly to serve as entry points, but they are not "knowledge nodes"—they are just maps.

### Operating Rules

1. No Topic Buckets: Do not create a note called "Networking" to dump information into. Create claims _about_ networking.
2. Sharpen the Signal: When reading, only capture claims that surprise you, challenge your thinking, or explain real-world failures.
3. Computed Truth: A note should only exist if it sharpens a concept, records a claim, preserves evidence, captures a question, or encodes a useful procedure.

### Summary

> A PKM is a belief revision system, not an information warehouse.

By sticking to these five types, you ensure that your system remains a "Runtime Environment for Thought" rather than a stagnant database of facts.
