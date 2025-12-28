---
aliases: []
confidence: "5/5"
created: 2025-02-07T00:00:00Z
epistemic: "architecture"
last_reviewed: "2025-12-22"
modified: 2025-12-28T18:49:16+00:00
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
