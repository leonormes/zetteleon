---
aliases:
  - DAG
  - directed acyclic graph
conformant: true
created: 2026-11-18T15:56:00+00:00
definition: A finite directed graph with no directed cycles, ensuring a strict partial ordering where no node can reach itself by following directed edges.
distinguishes_from:
  - "[[Directed Acyclic Graphs for Action Sequences Are Directed Acyclic and Graph-Structured]]"
modified: 2026-11-18T15:56:00+00:00
permalink: llmeon/30-library/100-zettelkasten/directed-acyclic-graph-dag
status: stable
tags:
  - domain/infrastructure
  - git
  - graph-theory
  - version-control
title: Directed Acyclic Graph (DAG)
type: concept
used_in_claims:
  - "[[SoT - Git]]"
---

## Directed Acyclic Graph (DAG)

A Directed Acyclic Graph (DAG) is a finite graph with directed edges and no cycles, guaranteeing a topological order in which no node can be an ancestor of itself. In Git, commits form a DAG where edges point from child commits to parent commits, preserving an unambiguous, loop-free history across branches and merges. ^def

### Scope & Conditions

- **Acyclicity:** A branch pointer can move and a merge commit can have two or more parents, but no commit hash can reference itself because hashes depend on parent hashes.
- **Partial order:** Concurrent branches are incomparable until joined by a merge commit, which establishes a common descendant.

### Evidence

- Standard graph-theoretic definition applied to Git's commit object model (see `[[SoT - Git]]`). *(No Calibre book quotation attached yet.)*

### Implications

- **Deterministic ancestry:** Enables `git merge-base` to compute the lowest common ancestor for three-way merges and makes tampered history detectable by hash invalidation.

### Related

- [[SoT - Git]]—synthesises: applies DAG structure to commit history.
- [[Directed Acyclic Graphs for Action Sequences Are Directed Acyclic and Graph-Structured]]—parallel: uses DAGs for task/action dependency ordering.
