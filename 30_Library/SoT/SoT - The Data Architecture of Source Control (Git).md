---
aliases: []
confidence: "5/5"
created: 2025-02-07T00:00:00Z
epistemic: "architecture"
last_reviewed: "2025-12-22"
modified: 2025-12-30T14:11:33+00:00
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

## 2. State Definition (The Atoms)

The state of a repository is represented by four primary atomic objects, each indexed by a SHA-1 (or SHA-256) hash of its content.

### The Git Object Tuple: `(Hash, Type, Size, Payload)`

| Object Type | Conceptual Role | Data Content |
|:--- |:--- |:--- |
| **Blob** | **File State** | Raw byte stream of a file's content. No metadata (names/perms). |
| **Tree** | **Directory State** | A list of tuples: `(Mode, Type, Hash, Name)`. Maps names to Blobs or other Trees. |
| **Commit** | **Point-in-Time State** | A tuple: `(Tree_Hash, Parent_Hashes, Author, Message)`. Defines a snapshot and its lineage. |
| **Tag** | **Named State** | A persistent alias for a specific Object Hash. |

---

## 3. Structural Mapping (The Layout)

The complexity of SCM resides in the **Merkle DAG** structure, which provides cryptographically verifiable integrity and efficient state comparison.

### The Merkle DAG (The Object Store)

State is organized as a graph of hashes:

- **Content-Addressability:** The `Hash(Content)` is the primary key. If two files have identical content, they share the same **Blob** atom, providing "free" deduplication.
- **Recursive Hashing:** A **Tree** hash depends on the hashes of its children. A change in a single leaf (Blob) cascades up, changing the Root Tree hash and the subsequent Commit hash.

### References (The Mutable Pointers)

While the Object Store is immutable, the user interacts with it via **Refs**.

- **Branch:** A mutable pointer to a **Commit** node.
- **HEAD:** A symbolic link pointing to the "active" Branch ref.

---

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
