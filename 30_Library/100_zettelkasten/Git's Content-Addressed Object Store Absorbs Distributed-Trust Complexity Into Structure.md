---
confidence: medium
conformant: true
created_utc: 2026-09-19 00:00:00+00:00
prodos:
  atomic:
    form: mechanism
  kind: atomic
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags:
- git
- content-addressing
- data-structures
- distributed-systems
title: "Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure"
type: claim
upstream: '[[Data Structures vs Control Flow]]'
permalink: llmeon/00-inbox/gits-content-addressed-object-store-absorbs-distributed-trust-complexity-into-structure
---

### Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure

Git represents every file, tree, and commit as an object named by the SHA-1 hash of its own content, so identity, tamper-detection, and history verification become direct consequences of the data structure rather than results computed by separate algorithms.

#### Scope & Conditions

Applies to Git's object model specifically (2005 design for Linux kernel-scale distributed version control).

#### Evidence

> "Because the data structure perfectly modeled a tamper-evident, directed acyclic graph, the algorithms required to distribute code, verify integrity, and merge histories became trivial consequences of the structure itself."

#### Implications

- Content-addressing turns "is this the same version?" and "was this tampered with?" into structural comparisons instead of bespoke diff/verification algorithms.

#### Related

- [[SoT - Git]]—direct concept match: "Git uses a content-addressable object database, where objects are identified by their SHA-1 (or SHA-256) hash" — same mechanism, same terminology.
- [[SoT - The Data-Centric Philosophy]]—direct concept match: §5 "Applied Philosophy: Git's Content-Addressable DAG" makes this exact case study its worked example of the data-centric thesis.