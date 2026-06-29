---
aliases: []
created: 2025-10-31 10:18:00+00:00
last_reviewed: ''
modified: 2026-02-01 15:08:30+00:00
status: seedling
tags:
- algorithms
- data-structures
- SoftwareEngineering/Networking
title: Mtri Trees Efficiently Store ACL and Routing Table Entries
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/mtri-trees-efficiently-store-acl-and-routing-table-entries
---

## Mtri Trees Efficiently Store ACL and Routing Table Entries

Summary: Mtri trees are specialized data structures that efficiently store and retrieve Access Control List (ACL) and routing table entries using prefix matching.

Node structure:

- Stores "effective prefix" (IP + wildcard/mask)
- Contains:
  - Parent pointer
  - Up to 3 child pointers (0, 1, or don't-care)
  - Next-hop data

Key operations:

- Insertion: Traverse tree, split nodes at mismatches, create daughter/niece nodes
- Search: Walk tree using exact match (including don't-care bits)
- Deletion: Remove leaf, merge branches to eliminate half nodes
- Lookup: Uses stack for backtracking, returns longest prefix match

Performance:

- All operations: O(k) where k=32 for IPv4
- Used in firewalls, routers, and network filtering systems