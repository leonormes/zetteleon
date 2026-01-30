---
aliases: [Cloud Hardware MOC, Compute Substrates, The Metal]
confidence: 5/5
created: 2025-12-31T00:00:00Z
epistemic: index
last_reviewed: 2025-12-31
modified: 2026-01-28T20:55:45+00:00
purpose: To map the physical reality of Cloud Compute substrates (AWS/Azure) for high-performance Data-Oriented Programming.
review_interval: 6 months
see_also: ["[[SoT - Data-Centric Software Engineering]]", "[[SoT - Data-Oriented Programming (DOP)]]"]
source_of_truth: []
status: active
tags: ["SoftwareEngineering/Architecture", cloud, hardware, performance, type/moc]
title: MOC - Cloud Hardware Architecture
type: map
uid:
updated:
---

## 1. The Core Thesis

> "The Abstraction is a Lie."

In high-performance Cloud Engineering, treating instances (e.g., `m7i.xlarge`, `Standard_D16s_v6`) as generic compute units is a failure mode. To achieve Data-Oriented Performance, you must program against the specific Silicon Reality beneath the Hypervisor.

This MOC organizes the physical and virtual constraints that define the execution environment.

---

## 2. The Hypervisor Substrate

The software layer that sits between your code and the metal.

- AWS: [[SoT - AWS Nitro System]] (The "Near-Metal" decoupled architecture).
- Azure: [[SoT - Azure Hyper-V Architecture]] (The Root Partition and vNUMA models).

## 3. The Silicon (Microarchitecture)

The instruction execution engines. Understanding cache hierarchies is critical for DOP.

- The Genealogy: [[SoT - Intel Server Microarchitectures]]
    - Ice Lake (m6i / D_v5): Monolithic, uniform, older.
    - Sapphire Rapids (m7i): Chiplet (4-tile), mesh interconnects, AMX.
    - Emerald Rapids (D_v6): Chiplet (2-tile), Massive L3 Cache (5MB/core).
- ARM Alternative: [[SoT - AWS Graviton Architecture]] (Monolithic consistency).

## 4. The Topology (Memory & Interconnects)

The map of latency.

- The Latency Map: [[SoT - NUMA and Cloud Memory Topology]] (SNC, UPI links, and the cost of crossing the socket).

## 5. The Configuration (Kubernetes Tuning)

How to align the software control plane with the hardware reality.

- The Golden Config: [[SoT - High-Performance Kubernetes Node Tuning]] (Topology Manager, Hugepages, Pinning).
