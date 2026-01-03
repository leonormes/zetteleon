---
aliases: []
confidence: "5/5"
created: 2025-02-07T00:00:00Z
epistemic: "architecture"
last_reviewed: "2025-12-22"
modified: 2026-01-03T10:18:50+00:00
purpose: ">-"
review_interval: "6 months"
see_also: []
source_of_truth: []
status: "stable"
tags: []
title: SoT - The Data Architecture of Source Control (Git)
type: "SoT"
uid: 
updated: 
---

## 1. The Core Model: Snapshots, Not Diffs

The fundamental misconception of Git is that it stores a series of "diffs" or "deltas." While `git log -p` presents changes this way for human consumption, the underlying storage is **Snapshot-based**.

- **The Logic:** Every commit is a complete snapshot of the entire project tree at a specific point in time.
- **The Mechanic:** Git uses a Content-Addressable storage model. If a file does not change between commits, the new commit simply points to the existing **Blob** (binary large object) from the previous snapshot.
- **Presentation vs. Storage:** Diffs are calculated on-the-fly during commands like `git diff`. Storage optimizations (deltas) happen internally via "Packfiles," but this is an implementation detail that does not change the logic of the object graph.

## 2. The Trinity of Objects (The DAG)

Git's reality is constructed from three primary object types, identified by SHA-1 hashes:

1. **Blobs (Content):** Pure data. No filenames, no permissions. Just the bytes of a file.
2. **Trees (Structure):** The equivalent of a directory. Maps names and permissions to Blobs or other Trees.
3. **Commits (Metadata):** A pointer to a root Tree, a list of parent commits, and author/message metadata.

---

## 3. Data-Centric Implications

## 4. Invariants & Constraints

1. **Immutability Invariant:** Once an object is written to the store, its hash cannot change. Any mutation creates a new node in the DAG.
2. **Referential Integrity:** A Commit cannot exist without its referenced Tree, and a Tree cannot exist without its referenced Blobs.
3. **Append-Only History:** The DAG is structurally append-only. "Deleting" history (rebase/reset) merely orphans nodes; the underlying data remains until garbage collection.
4. **DAG Invariant:** A Commit cannot be its own ancestor. This prevents circular temporal dependencies.

---

## 5. Logic Derivation (The Algorithms)

Because history is a DAG and state is content-addressed, the complex operations of SCM become trivial graph traversals:

- **Branching:** A constant-time `O(1)` operation. It is merely the creation of a new **Reference pointer** to an existing node. No data is copied.
- **Merging (3-way):**
    1. Find the **Lowest Common Ancestor (LCA)** of two nodes in the DAG.
    2. Perform a `diff` between LCA and each leaf.
    3. Create a new **Commit** node with two parent pointers.
- **Diffing:** A recursive tree comparison. Since Trees are hashed, if `Hash(Tree_A) == Hash(Tree_B)`, the entire subtree can be skipped in `O(1)`, making comparison of massive codebases extremely fast.

### Performance Optimization: Object Packing

To mitigate the storage overhead of many small files, Git periodically performs **Delta Compression**, storing objects as a base blob plus a series of XOR-like deltas in a **Packfile**, optimized for disk locality and retrieval speed.

---

## 6. Theoretical Foundation: The Directed Acyclic Graph (DAG)

Git's architecture is a specialized implementation of a **Directed Acyclic Graph (DAG)**. Understanding the abstract properties of a DAG illuminates why it is the chosen structure for version control.

### 6.1 Core Properties from a Data Perspective

1. **Directed Edges:**
    - Each edge has a direction, indicating a one-way relationship (Dependency / Flow).
    - *In Git:* Child Commits point to Parent Commits.
2. **Acyclicity:**
    - No cycles are permitted. You cannot start at a node and follow edges back to itself.
    - *In Git:* Prevents infinite loops in history traversal and ensures strict temporal ordering.
3. **Nodes and Edges:**
    - **Nodes:** Data entities (Tasks, States, Commits).
    - **Edges:** Relationships (Dependencies, Lineage).
4. **Topological Ordering:**
    - Nodes can be arranged linearly where `A -> B` implies `A` comes before `B`.
    - *In Git:* Essential for build systems and linearizing history (e.g., `git log`).
5. **Reachability:**
    - Determines which nodes are accessible from a given starting point.
    - *In Git:* Used for garbage collection (unreachable nodes are pruned) and sync (finding common ancestors).
6. **Multi-Root / Multi-Leaf:**
    - Unlike trees, DAGs can have multiple entry and exit points (Orphan branches, multiple branch tips).

### 6.2 Why DAGs? (The Utility)

DAGs are the primary abstraction for managing **dependencies** and **causality**.

- **Task Scheduling:** CI/CD pipelines, Build Systems (Make/Bazel).
- **Data Pipelines:** ETL processes (Airflow) where data flows through transformation steps.
- **Compiler Optimization:** Representing code dependencies.
- **Causal History:** Distributed Systems and Version Control (Git, Blockchain).

### 6.3 Comparative Implementation: Mental Model vs. Git Reality

A standard, mutable DAG (like one you might write in TypeScript) differs fundamentally from Git's immutable **Merkle DAG**.

**A. Simple Mutable DAG (In-Memory)**

```typescript
class DAGNode<T> {
  data: T;
  neighbors: DAGNode<T>[] = [];
  constructor(data: T) { this.data = data; }
  addNeighbor(node: DAGNode<T>): void { this.neighbors.push(node); }
}
// Edges are mutable pointers.
// Data is not hashed.
// Cycles must be checked at runtime.
```

**B. Git's Merkle DAG (Persistent)**

1. **Content-Addressable:** Nodes are not pointers to memory addresses; they are pointers to **Hashes**.
2. **Immutable:** You cannot "add a neighbor" to an existing node. You must create a *new* node that points to the old one.
3. **Self-Verifying:** The ID of the node (`Hash`) inherently proves the integrity of its entire history (Sub-graph).
