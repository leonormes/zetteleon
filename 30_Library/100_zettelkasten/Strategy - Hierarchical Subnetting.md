---
aliases: []
confidence: 0.9
created: 2025-11-22T15:05:01Z
epistemic: principle
last_reviewed: 2025-11-22
modified: 2025-11-22T14:50:52Z
purpose: "Advocates for grouping subnets logically rather than flattening them."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [best-practices, networking, terraform]
title: Strategy - Hierarchical Subnetting
type: strategy
uid: 2025-11-22T15:05:01Z
updated: 2025-11-22T15:05:01Z
---

## Hierarchical Subnetting

**Summary:** Hierarchical subnetting involves carving out intermediate "blocks" of IP space for related resources before allocating specific subnets, rather than slicing a large network into a flat list of small subnets.

**Details:**
Instead of calculating a small subnet directly from a large parent prefix (e.g., a `/29` from a `/24` using a large index), this strategy suggests:
1.  Carving a larger intermediate block (e.g., a `/26` "jumpbox area") from the parent.
2.  Carving the final subnet (e.g., the `/29`) from that intermediate block.
This improves readability by making the "location" of subnets within the address space explicit and avoids using large, opaque index numbers (like `netnum 16`) that are hard to verify mentally.
