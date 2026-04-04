---
aliases: []
created: 2025-07-10T12:36:00Z
last_reviewed:
modified: 2026-02-01T15:08:06+00:00
status:
tags: ["SoftwareEngineering/Networking", data-perspective]
title: MOC - Data-Centric Networking
type: map
updated:
---

## Core Principle

> [!definition] The Data-Centric Lens
> Networking is not about "wires" or "hardware"; it is the computational study of distributed state transport.
>
> We deconstruct complex network systems by identifying the Atomic State (PDUs), the Structural Layout (Tries, Stacks, Tables), and the Invariants (Integrity, Uniqueness) that make logic self-evident.

---

## 1. The Core Pillars (Sources of Truth)

These are the authoritative specifications for the data-centric view of networking.

- [[SoT - The Data-Centric Theory of Networking]]—_The "Why" and "How" of state transport, recursive encapsulation, and routing as prefix-trie traversal._
- [[SoT - The Architecture of Packet Encapsulation (TCP-IP)]]—_The bit-level anatomy of the Segment, Packet, and Frame containers._
- [[SoT - The Data Architecture of DNS]]—_DNS as a distributed hierarchical database and zone-based state partitioning._

---

## 2. State Atoms (Components)

Lower-level details on the specific data units and identification systems.

- [[SoT - Protocol Data Units (PDU)|Protocol Data Unit (PDU)]]—The fundamental container of information (SDU vs PDU).
- [[30_Library/100_zettelkasten/How Computers Identify Each other on a Network|How Computers Identify Each other on a Network]]—Resolution of identifiers (IP to MAC).
- [[30_Library/ops/sot-network-tools-patterns#3. Layer 4: Ports & Sockets (The Doors)|IPs and ports form a socket]]—The 5-tuple as a unique pointer to a process.
- [[30_Library/200_projects/10_Infrastructure/k8s/the k8s service abstraction|DNS for Services and Pods]]—Automated name-to-state binding in dynamic environments.

---

## 3. Implementation Domains

How these data principles manifest in specific technologies and models.

### Models & Layers

- [[SoT - Protocol Data Units (PDU)#2. Layer-by-Layer Encapsulation Logic|The OSI Model]]—The legacy conceptual map of encapsulation.
- [[30_Library/100_zettelkasten/Layer 1 Physical Layer|Physical Layer]]—The serialization of bits into physical signals.

### Cloud & Kubernetes

- [[SoT - Cloud Networking Core Components]]—VPCs, Subnets, and Gateways as virtualized data structures.
- [[SoT - Kubernetes Networking Model|Kubernetes Networking Model]]—The overlay network as a software-defined state layer.
- [[SoT - Secure Cross-Cloud Data Transport]]—The Virtual Private Data Plane pattern for multi-cloud systems.
- [[30_Library/200_projects/10_Infrastructure/Networking/curriculum for learning Kubernetes networking|Kubernetes Networking Curriculum]]—Learning paths for cluster connectivity.
- [[30_Library/200_projects/10_Infrastructure/Containerisation/Container Runtime Configures Pod Networking Through CNI Plugins|CNI Explained]]—The data interface for container networking.

---

## 4. Related Concepts

- [[MOC - Interpretation of References]]—How names (DNS) resolve to state (IP).
- [[SoT - Atomicity and Loose Coupling]]—Why we separate the network core from endpoint intelligence.
- [[SoT - The Extended Mind]]—Networking as the "Synapses" of the distributed extended mind.
