---
conformant: false
created: 2026-09-18T00:00:00+00:00
created_utc: 2026-09-18T00:00:00Z
modified: 2026-09-25T16:29:32+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/symmetric-multiprocessing-gives-every-core-equal-access-to-shared-system-resources
prodos.atomic.form: definition
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags: [computer-architecture, computer-science, concurrency]
title: Symmetric Multiprocessing Gives Every Core Equal Access to Shared System Resources
type: concept
---

## Symmetric Multiprocessing Gives Every Core Equal Access to Shared System Resources

Symmetric Multiprocessing (SMP) is the arrangement in which every processor or core in a system is identical and has equal, uniform-latency access to shared system resources—chiefly main memory and I/O—rather than some cores having privileged or faster access than others.

### Scope & Conditions

Describes the SMP arrangement itself, as contrasted with asymmetric arrangements (e.g. NUMA, where memory access latency depends on which bank a core is nearest to) and with distributed-memory systems, which have no shared resource pool at all.

### Evidence

> "Both architectures often employ Symmetric Multiprocessing (SMP), where all processors (or cores) are identical and have equal access to system resources."

### Implications

- SMP is the specific technical claim underneath the "equal access" half of [[SoT - The Logical Definition of a Computer]]'s Multicore Paradox—"128 cores are one computer" relies on those cores actually having symmetric, not just shared, access to memory.
- Because SMP assumes uniform access latency, it doesn't scale indefinitely: large machines move to NUMA (non-uniform memory access), trading the "symmetric" property for the ability to add more cores.

### Related

- [[SoT - The Logical Definition of a Computer]]—extends: names the precise architectural term for the "equal access to system resources" claim embedded in the Multicore Paradox. [extends:: [[SoT - The Logical Definition of a Computer]], strength=3, confidence=high]
- [[Shared-Memory Multi-Core Systems Require Kernel-Enforced Synchronization to Prevent Race Conditions]]—shared mechanism: SMP's shared-resource access is exactly what creates the synchronization problem that note describes.

#### Further Reading

- [Programming Language Pragmatics — Michael L. Scott, §12.1.2 "Multiprocessor Architecture"](calibre://view-book/GCcalibreBooks/196/PDF)—_notes that small shared-memory multiprocessors (2–8 processors) were "often symmetric, in the sense that all memory was equally distant from all processors," directly corroborating the definition._
