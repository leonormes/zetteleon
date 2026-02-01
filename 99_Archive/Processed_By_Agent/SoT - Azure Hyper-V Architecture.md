---
aliases: ["Azure Boost", "Azure Hypervisor", "Hyper-V Root Partition"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "architecture"
last_reviewed: "2025-12-31"
modified: 2026-01-08T10:49:44+00:00
purpose: "To define the Azure virtualization model and its implications for latency-sensitive workloads."
review_interval: "1 year"
see_also: ["[[MOC - Cloud Hardware Architecture]]", "[[SoT - AWS Nitro System]]"]
source_of_truth: []
status: "stable"
tags: ["azure", "cloud", "hypervisor", "performance"]
title: SoT - Azure Hyper-V Architecture
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> Azure utilizes a customized Hyper-V Type-1 Hypervisor. Unlike AWS Nitro, it relies on a Root Partition (a privileged Windows kernel) to manage scheduling and I/O, though newer generations (D_v6) utilize "Azure Boost" hardware offloading to reduce this overhead.

---

## 2. The vNUMA Complexity

Azure presents a Virtual NUMA (vNUMA) topology to the guest, which attempts to map to the underlying hardware but introduces abstraction risks.

### 2.1 The Misalignment Risk

Hyper-V may construct a large VM (e.g., `Standard_D96s_v6`) from non-contiguous physical cores if the host is fragmented.

- The Problem: The guest sees "1 NUMA Node," but physically, the memory spans two sockets.
- The Cost: A thread accesses "Local RAM" (according to vNUMA) but physically traverses the UPI link (Remote RAM), incurring a 1.5x - 2.5x latency penalty.

### 2.2 Root Partition Jitter

The Root Partition consumes CPU cycles for cluster management. While "Fair Share" scheduling prevents resource monopoly, it can introduce micro-latency spikes ("Jitter") that disrupt isochronous data planes.

---

## 3. Azure Boost (The Nitro Catch-up)

In newer generations (v5/v6), Azure Boost offloads storage and networking to dedicated hardware, significantly reducing the Root Partition's interference footprint and bringing performance closer to the Nitro "metal-like" standard.
