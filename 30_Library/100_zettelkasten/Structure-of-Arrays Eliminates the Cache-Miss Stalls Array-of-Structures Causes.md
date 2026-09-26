---
conformant: true
contradicts: []
created: 2026-09-19T15:25:31+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-25T16:29:32+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/structure-of-arrays-eliminates-the-cache-miss-stalls-array-of-structures-causes
proposition: Because CPUs fetch memory in fixed-size cache lines, storing per-entity properties as an Array of Structures pollutes every cache-line fetch with irrelevant data, whereas a Structure of Arrays, one flat contiguous array per property, lets every fetched cache line contain only the data the current loop actually needs.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [cache-lines, data-oriented-design, mike-acton, performance, structure-of-arrays]
title: Structure-of-Arrays Eliminates the Cache-Miss Stalls Array-of-Structures Causes
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Structure-of-Arrays Eliminates the Cache-Miss Stalls Array-of-Structures Causes

Because CPUs fetch memory in fixed-size cache lines, storing per-entity properties as an Array of Structures (one heap object per entity, each bundling unrelated fields) pollutes every cache-line fetch with irrelevant data, whereas a Structure of Arrays (one flat, contiguous array per property) lets every fetched cache line contain only the data the current loop actually needs.

### Scope & Conditions

A hardware-grounded consequence of CPU cache-line fetching and hardware prefetching; most relevant to hot loops processing many homogeneous entities (e.g. game-engine particle systems).

### Evidence

> "Because the Particle object contains extra, unrelated data (color, lifetime), the 64-byte cache line pulled into the CPU is severely polluted with irrelevant information… a single 64-byte cache line fetch pulls in the specific data for multiple particles simultaneously. The hardware prefetcher recognizes the predictable linear access pattern."

### Implications

- SoA layout also removes virtual-function/vtable dispatch overhead common in AoS+OOP designs, and enables SIMD vectorisation of the resulting tight loops.

### Related

- [[SoT - Data-Oriented Design]]—direct concept match: §4.1 "SoA (Structure of Arrays)" describes the identical AoS-vs-SoA trade-off, including the "Swiss Cheese" cache-pollution framing.
- [[SoT - Mechanical Sympathy]]—direct concept match: the cache-latency table (§4) grounds the same "avoid the supermarket" (main-memory) cost this atom's mechanism avoids.

### See Also

- [[MOC - Data-Oriented Structures & Internals]]

### Further Reading (Personal Library)

- [Introduction to Algorithms, Fourth Edition — Thomas H. Cormen, §11.5 "Practical considerations"](calibre://view-book/GCcalibreBooks/442/PDF)—_corroborates the cache-line mechanism generally: "cache memory is organized in cache blocks of (say) 64 bytes each, which are always fetched together… reusing the same cache block is much more efficient than fetching a different cache block."_
- [Programming Language Pragmatics — Michael L. Scott, §7.4.3 "Memory Layout"](calibre://view-book/GCcalibreBooks/196/PDF)—_corroborates the concrete AoS/SoA-style consequence: rowvs column-major array layout determines whether nested-loop traversal hits or misses the cache on every access._
