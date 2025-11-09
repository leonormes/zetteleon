---
aliases: []
confidence: 0.8
created: 2025-10-31T10:18:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Explain mtri tree data structure for network filtering."
review_interval: 90
see_also: ["Access Control Lists Filter Traffic Based on Protocol and Address Rules.md", "Routing Tables Use Longest Prefix Match for Forwarding Decisions.md"]
source_of_truth: []
status: seedling
tags: [algorithms, data-structures, networking]
title: Mtri Trees Efficiently Store ACL and Routing Table Entries
type: concept
uid: 
updated: 
---

## Mtri Trees Efficiently Store ACL and Routing Table Entries

**Summary:** Mtri trees are specialized data structures that efficiently store and retrieve Access Control List (ACL) and routing table entries using prefix matching.

**Node structure:**
- Stores "effective prefix" (IP + wildcard/mask)
- Contains:
  - Parent pointer
  - Up to 3 child pointers (0, 1, or don't-care)
  - Next-hop data

**Key operations:**
- **Insertion**: Traverse tree, split nodes at mismatches, create daughter/niece nodes
- **Search**: Walk tree using exact match (including don't-care bits)
- **Deletion**: Remove leaf, merge branches to eliminate half nodes
- **Lookup**: Uses stack for backtracking, returns longest prefix match

**Performance:**
- All operations: O(k) where k=32 for IPv4
- Used in firewalls, routers, and network filtering systems
