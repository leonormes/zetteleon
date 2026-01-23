---
alias: ["Vault KV Data Structure"]
aliases: []
confidence: "5/5"
created: 2025-12-25T00:00:00Z
epistemic: "First Principles Model"
last_reviewed: 
modified: 2026-01-23T18:09:16+00:00
purpose: "To define the first-principles data model of HashiCorp Vault (KV Store)."
review_interval: "1 year"
see_also: ["[[SoT - Data-Centric Software Engineering]]", "[[SoT - The Data Architecture of Source Control (Git)]]"]
source_of_truth: []
status: "stable"
tags: ["data-structures", "infrastructure", "SoftwareEngineering/Security", "vault"]
title: SoT - Vault KV Data Structure
type: "SoT"
uid: 
updated: 
---

## 0. The Lineage

This analysis applies the Data-Centric philosophy to infrastructure.

- **The Axiom:** **[[SoT - Data-Centric Software Engineering]]**—_Structure is truth._
- **The Subject:** **HashiCorp Vault (KV)**—_A persistent, content-addressed Merkle Tree._

---

## 1. The Definitive Statement

> [!definition] Vault from First Principles
> Vault KV is not a database; it is a **Persistent Content-Addressed Merkle Tree** wrapped in a RESTful interface.
>
> Strip away the security terminology ("secrets," "sealing"). From a data perspective, it is a **Versioned Trie of JSON Documents**.

---

## 2. The Core Primitives

### 2.1 The Key-Value Pair (The Atom)

At the lowest level, a "secret" is just a **JSON Object**.

- **Data Structure:** A flat or nested Map (Dictionary).
- **Logic:** Vault acts as a BLOB store that guarantees JSON serialization.

### 2.2 The Namespace (The Address)

The "Path" functions exactly like a **Unix File System**.

- **Structure:** A **Prefix Tree (Trie)**. Each `/` is a node.
- **Logical Separation:** Paths (`secret/app1/db`) act as routing keys to specific storage buckets.

### 2.3 The Versioning Engine (Linked List)

In KV-V2, the data model shifts from a simple Map to a **Linked List of Snapshots** attached to each leaf node.

---

## 3. First Principles Assumptions

To maintain a clean mental model, accept these structural truths:

1. **Atomic Updates:** Every write is a **PUT** (full replacement), not a PATCH. You cannot update a single field in a secret without rewriting the whole JSON object.
2. **Encryption is Transparent:** Encryption is just a **Transformation Function** ($f(x) = y$) applied before disk I/O. It changes _legibility_, not _structure_.
3. **Virtual Filesystem:** Vault mounts "engines" (plugins) at path prefixes (e.g., `secret/`).

---

## 4. The Summary Framework

Think of Vault KV as a three-layer structure:

1. **Trie (Prefix Tree):** Addressing and Routing.
2. **Ordered List:** Version History.
3. **Map (Hash Table):** Data Payload.

---

## 5. Access Control as Path Filters

ACLs are not abstract permissions; they are **Path-Based Bitmasks** applied to the Trie.

- **The Data Structure:** A mapping of **Path Pattern** $	o$ **Capability Set**.
    - `secret/data/app1/*` $	o$ `[create, read, update]`
- **The Algorithm:** **Longest Prefix Match (LPM)**.
    - Vault traverses the Trie using the request path.
    - It intersects the user's "Identity Bitmask" with the node's path.
    - If no match, the node effectively _does not exist_ (404/403).

---

## 6. The Integrity Model (Merkle Tree)

Vault Enterprise uses Merkle Trees for replication, distinct from the Prefix Tree used for routing.

- **Prefix Tree (Trie):** Defined by **Keys** (Paths). Used for **Lookup**.
- **Merkle Tree:** Defined by **Values** (Hashes). Used for **Sync**.

### The Sync Logic (Divide and Conquer)

To sync Cluster A and Cluster B:

1. Compare Root Hashes. If match, done.
2. If mismatch, compare children.
3. Recurse down the "dirty" branch only.
4. This mathematically guarantees **Binary Identity** without sending the full dataset.

---

## 7. Comparison: Vault vs. Kubernetes vs. GitOps

| Feature | Vault | Kubernetes (etcd) | ArgoCD (GitOps) |
|:--- |:--- |:--- |:--- |
| **Model** | **Merkle Tree** | **Raft Log (Stream)** | **Recursive Diff** |
| **Trigger** | Hash Mismatch | New Log Index | Periodic Poll |
| **Goal** | **Cryptographic Identity**<br>(Is it _exactly_ this?) | **Sequential Consistency**<br>(Did I replay all events?) | **Logical Equivalence**<br>(Is the intent met?) |

> **Insight:** Use Merkle Trees (Vault) for **Security** (integrity). Use Reconciliation (K8s) for **Liveness** (state converging).

---

## 8. The Vault Secrets Operator (The Bridge)

The Operator functions as a **Unidirectional State Synchronizer**.

### The Flow

1. **Identity:** K8s ServiceAccount (JWT) $	o$ Vault Role.
2. **Observation:** Operator reads Vault JSON (Source).
3. **Transformation:** Operator converts JSON $	o$ K8s Secret (Base64 Map).
4. **Materialization:** Operator writes to `etcd` (Target).

### Static vs. Dynamic

- **Static (`VaultStaticSecret`):** Mirroring a JSON object. `GET` loop.
- **Dynamic (`VaultDynamicSecret`):** Managing a **Lease**. `POST` loop. The Operator acts as a "Garbage Collector" for credentials, renewing them until TTL expiry.
