---
aliases: []
created: 2025-11-22T15:05:01+00:00
last_reviewed: '2025-11-22'
modified: 2026-08-29T09:36:05+00:00
permalink: llmeon/30-library/100-zettelkasten/strategy-hierarchical-subnetting
status: seedling
tags: [best-practices, SoftwareEngineering/Networking, terraform]
title: Strategy - Hierarchical Subnetting
type: strategy
updated: null
---

## Hierarchical Subnetting

Summary: Hierarchical subnetting involves carving out intermediate "blocks" of IP space for related resources before allocating specific subnets, rather than slicing a large network into a flat list of small subnets.

Details:

Instead of calculating a small subnet directly from a large parent prefix (e.g., a `/29` from a `/24` using a large index), this strategy suggests:

1. Carving a larger intermediate block (e.g., a `/26` "jumpbox area") from the parent.
2. Carving the final subnet (e.g., the `/29`) from that intermediate block.
This improves readability by making the "location" of subnets within the address space explicit and avoids using large, opaque index numbers (like `netnum 16`) that are hard to verify mentally.
