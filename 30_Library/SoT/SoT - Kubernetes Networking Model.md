---
aliases:
- K8s Network Model
- Pod Networking Rules
created: 2026-02-05 00:00:00+00:00
modified: 2026-07-04 10:50:55+00:00
permalink: llmeon/30-library/so-t/so-t-kubernetes-networking-model
tags:
- kubernetes
- networking
- sot
title: SoT - Kubernetes Networking Model
prodos:
  kind: sot
  lifecycle: stable
---


## Minimum Viable Understanding (MVU)

The Kubernetes networking model is a flat, NAT-less address space where every Pod has a unique, cluster-wide IP address. It decouples the application from the underlying infrastructure by mandating a set of connectivity invariants that all CNI (Container Network Interface) plugins must enforce.

---

## 1. The Four Invariants

Every CNI implementation must satisfy these four requirements:

1. Unique Pod IPs: Every Pod gets its own IP address.
2. Pod-to-Pod Communication: Any Pod can communicate with any other Pod in the cluster without NAT.
3. Node-to-Pod Communication: Nodes can reach all Pods (and vice-versa) without NAT.
4. Internal Container Comms: Containers within a Pod share the same network namespace (`localhost`) and can communicate using distinct ports.

---

## 2. Implementation: The Node Bridge (`cbr0`)

In a standard (non-accelerated) setup, the node uses a Linux Software Bridge to manage local traffic.

- `cbr0`: The software bridge interface on the Node.
- `vethN`: Virtual Ethernet pairs that connect Pod namespaces to `cbr0`.
- IPAM (IP Address Management): Assigns disjoint CIDR ranges to each Node to ensure cluster-wide IP uniqueness.

### Traffic Flow (Intra-Node)

1. Pod A emits packet -> `vethA` -> `cbr0`.
2. `cbr0` checks ARP/IP tables.
3. Packet -> `vethB` -> Pod B.

### Traffic Flow (Inter-Node)

1. Pod A emits packet -> `cbr0` -> `eth0` (Node NIC).
2. Packet enters the Physical/Cloud Routing Table.
3. Target Node receives packet via `eth0` -> `cbr0` -> Pod IP.

---

## 3. Interaction with Cloud Providers

- Azure (Kubenet): The cloud provider manages the "Routing Tables" (User Defined Routes) to handle inter-node jumps.
- Overlay Networks: Technologies like VXLAN or IP-in-IP "hide" Pod traffic inside standard Node-to-Node packets, bypassing the need for cloud-native route table entries.

_Related:_ [[SoT - Calico CNI Architecture]]
