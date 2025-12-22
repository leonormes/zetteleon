---
aliases: [DNS Data Architecture, Domain Name System Structure, SoT - DNS]
confidence: 5/5
created: 2025-02-12T19:42:08Z
epistemic: architecture
last_reviewed: 2025-12-22
modified: 2025-12-22T11:08:38Z
purpose: To define DNS strictly as a distributed hierarchical database, focusing on its data structures and state representation rather than just resolution logic.
review_interval: 6 months
see_also: ["[[SoT - Cloud Networking Core Components]]", "[[SoT - Kubernetes Networking & DNS]]"]
source_of_truth: true
status: stable
tags: [architecture, data-centric, dns, networking, sot]
title: SoT - The Data Architecture of DNS
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] Definition
> The **Domain Name System (DNS)** is a distributed, hierarchical, eventually consistent database designed to provide a unified namespace for network resources.
>
> From a data-centric perspective, it is a **forest of inverted trees**, where state is partitioned into administrative units called **Zones**. The logic of resolution is merely a tree-traversal algorithm over this distributed data structure.

---

## 2. State Definition: The Resource Record

The fundamental atomic unit of state in DNS is the **Resource Record (RR)**. It is a tuple that defines a specific assertion about a name.

**RR Tuple Structure:** `(Name, Type, Class, TTL, RData)`

| Field | Definition | Conceptual Role |
| :--- | :--- | :--- |
| **Name** | The Fully Qualified Domain Name (FQDN). | The Primary Key (Index). |
| **Type** | The schema of the payload (e.g., `A`, `MX`). | The Data Type definition. |
| **Class** | The protocol family (almost always `IN` for Internet). | The Namespace Scope. |
| **TTL** | Time-to-Live (Seconds). | The Cache Coherency Contract. |
| **RData** | The type-specific payload. | The Value. |

### Core Data Types

-   **A / AAAA:** `Address Record`. Maps `Hostname -> IP`. The fundamental binding of Name to Location.
-   **NS:** `Name Server`. Maps `Zone -> Authority`. A pointer that delegates a subtree to a different database shard (nameserver).
-   **SOA:** `Start of Authority`. Maps `Zone -> Metadata`. Defines the parameters of the zone's state (Serial, Refresh, Retry).
-   **CNAME:** `Canonical Name`. Maps `Alias -> Name`. A symbolic link within the namespace.
-   **PTR:** `Pointer`. Maps `IP -> Name`. Used for reverse lookups (indexing by Value).
-   **MX:** `Mail Exchange`. Maps `Domain -> Mail Server`. Includes a `Priority` field for failover logic.
-   **TXT:** `Text`. Maps `Name -> String`. Used for arbitrary metadata verification (e.g., SPF, DKIM) to prove domain ownership.

### The DNS Message PDU

Data transfer occurs via a standardized Protocol Data Unit (PDU) containing five sections:

| Section | Role | Content |
| :--- | :--- | :--- |
| **Header** | Control Metadata | Flags (`QR`, `AA`, `TC`), Transaction ID, Record Counts. |
| **Question** | Query Definition | The Name and Type being requested. |
| **Answer** | Result Set | The RRs that directly match the query. |
| **Authority** | Delegation Pointers | `NS` records pointing to the next shard (if answer not found). |
| **Additional** | Optimization (Glue) | `A` records for the nameservers in the Authority section to prevent extra lookups. |

---

## 3. Structural Mapping: The Distributed Hierarchy

The complexity of DNS resides in its data layout, which partitions the global namespace into manageable, autonomous shards.

### The Inverted Tree (The Namespace)

The data structure is a tree with a null-label root (`.`).

-   **Depth:** Maximum of 127 levels.
-   **Label:** Each node is a string (max 63 chars).
-   **FQDN:** The concatenation of labels from node to root (e.g., `www.example.com.`).

### The Zone (The Shard)

The tree is partitioned into **Zones**.

-   **Definition:** A Zone is a contiguous subtree delegated to a specific administrative authority.
-   **Storage:** Physically stored as a **Zone File** (or database equivalent) on an **Authoritative Name Server**.
-   **Delegation:** A Zone contains `NS` records that point to the servers responsible for sub-zones. This creates a linked list of database shards.

**Structural Invariant:** Every node in the tree belongs to exactly one Zone at any point in time.

---

## 4. Invariants & Constraints

For the system to function as a global truth, specific data invariants must be maintained.

1.  **Uniqueness:** Within a single Zone, a `(Name, Type)` tuple must be unique (except for RRsets like load-balanced `A` records).
2.  **The Authoritative Chain:** Every domain name must have an unbroken chain of trust (via `NS` records) from the Root Zone (`.`) down to the Authoritative Zone.
3.  **SOA Singleton:** A Zone must contain exactly one `SOA` record at its apex.
4.  **Glue Logic:** If a sub-zone's nameserver lies *within* the sub-zone itself (e.g., `ns1.example.com` is inside `example.com`), the parent zone MUST store a "Glue Record" (`A` record) for that nameserver to prevent circular dependency resolution failures.

---

## 5. Logic Derivation: Resolution as Tree Traversal

Because the data is structured as a hierarchical tree of delegated zones, the resolution logic is a "degenerate" algorithm: simple iterative traversal.

**The Algorithm:**
1.  **Query:** Client requests `www.example.com.`
2.  **Root:** Resolver queries Root Server (`.`).
    -   *Data:* Root does not hold `www.example.com`.
    -   *Pointer:* Root returns `NS` records for `.com` TLD servers.
3.  **TLD:** Resolver queries `.com` Server.
    -   *Data:* TLD does not hold `www.example.com`.
    -   *Pointer:* TLD returns `NS` records for `example.com` Authoritative Servers.
4.  **Auth:** Resolver queries `example.com` Server.
    -   *Data:* Server holds the Zone File.
    -   *Result:* Returns the `A` record for `www`.

**Caching (Performance Optimization):**
Resolvers cache the results of traversals based on the `TTL` invariant. This turns the O(N) traversal into O(1) lookup for frequently accessed nodes, at the cost of eventual consistency.

---

## 6. Security Implication: Data Integrity

Since DNS is a decoupled distributed system, the primary threat is **Data Spoofing** (injecting false records).

-   **DNSSEC:** Adds a layer of cryptographic data integrity.
    -   **RRSIG:** A digital signature of the Resource Record set.
    -   **DS (Delegation Signer):** A hash of the child's key stored in the parent zone.
    -   **Chain of Trust:** Validates the data structure from Root to Leaf, ensuring the record retrieved is bit-for-bit identical to the Authoritative state.
