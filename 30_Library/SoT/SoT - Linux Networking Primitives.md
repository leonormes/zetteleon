---
aliases: ["Veth Pairs", "Linux Bridges", "IPTables Masquerade", "Container Networking Primitives"]
confidence: "5/5"
created: 2025-12-30T15:00:00Z
epistemic: "technical"
last_reviewed: "2025-12-30"
modified: 2025-12-30T14:04:31+00:00
purpose: "To define the low-level Linux kernel networking constructs that underpin all container networking abstractions."
review_interval: "1 year"
see_also: ["[[SoT - Linux Container Primitives]]", "[[SoT - Kubernetes Networking & DNS]]"]
source_of_truth: []
status: "stable"
tags: ["linux", "networking", "kernel", "containers"]
title: SoT - Linux Networking Primitives
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

Container networking is not magic; it is the automation of standard Linux kernel primitives. Understanding these three components—**Veth Pairs**, **Bridges**, and **IPTables**—demystifies how a container communicates with the world.

---

## 2. The Core Primitives

### A. Veth Pairs (The Virtual Cable)

A **Virtual Ethernet (veth)** pair is a linked pair of network interfaces. Packets transmitted on one interface immediately appear on the other.

* **Function:** To tunnel traffic between the **Host Namespace** and a **Container Namespace**.
* **Analogy:** A patch cable connecting a computer (Container) to a wall socket (Host Switch/Bridge).
* **Architecture:**
    * `veth0` (Host side): Attached to a Bridge.
    * `veth1` (Container side): Renamed to `eth0` inside the container namespace.

### B. Linux Bridge (The Virtual Switch)

A **Linux Bridge** is a software implementation of a Layer 2 Ethernet switch. It forwards packets based on MAC addresses.

* **Function:** To connect multiple veth pairs (containers) together on the same host, allowing them to talk to each other and the host's physical interface (`eth0`).
* **Mechanism:**
    * It maintains a MAC Address Table (CAM Table).
    * If the destination MAC is known, it forwards to the specific port (veth).
    * If unknown, it broadcasts to all ports.
* **CNI Context:** In Kubernetes, this is often named `cni0` or `docker0`.

### C. IPTables & NAT (The Router/Firewall)

**IPTables** (or its successor `nftables`) handles Packet Filtering and Network Address Translation (NAT).

#### 1. Masquerade (Source NAT)

When a container (Private IP: `10.244.1.5`) sends a packet to the Internet (`8.8.8.8`), the return packet must know how to get back.

* **Problem:** The outside world doesn't know about `10.244.1.5`.
* **Solution:** The kernel replaces the Source IP with the Host's Physical IP (`192.168.1.100`) as it leaves the interface. It tracks this connection to reverse the process for the reply.
* **Rule:** `iptables -t nat -A POSTROUTING -s 10.244.0.0/16 -j MASQUERADE`

#### 2. DNAT (Destination NAT)

Used for **Services**.

* **Function:** Intercepts traffic destined for a virtual VIP (ClusterIP) and rewrites the Destination IP to a specific Pod IP.

---

## 3. The Traffic Flow (Life of a Packet)

### Scenario: Container A to Internet

1. **Container:** App sends packet to `8.8.8.8`. Route table says "Default Gateway is `cni0`".
2. **Veth:** Packet travels `eth0` (Container) -> `vethXXXX` (Host).
3. **Bridge:** Bridge receives packet on `vethXXXX`. Sees dest MAC is Gateway. Hands off to Host IP Stack.
4. **Routing:** Host Kernel sees Dest IP `8.8.8.8`. Route table says "Use physical `eth0`".
5. **IPTables (NAT):** POSTROUTING chain sees packet leaving. Replaces Source IP (`10.x`) with Host IP (`192.x`).
6. **Wire:** Packet leaves physical NIC.

---

## 4. IP Forwarding (The Kernel Switch)

By default, Linux drops packets not destined for itself. For a host to act as a router (passing packets from Container -> Internet), **IP Forwarding** must be enabled.

* **Command:** `sysctl -w net.ipv4.ip_forward=1`
* **Impact:** Without this, the Bridge receives the packet, but the Kernel refuses to pass it to the physical interface.

---

## 5. Relationships to CNI

* **Flannel:** Creates a Bridge (`cni0`) and manages Veth pairs. Uses VXLAN (UDP encapsulation) to tunnel traffic between hosts.
* **Calico:** Often avoids Bridges. Uses **Proxy ARP** and BGP routing to treat containers as routable workloads, skipping the Layer 2 switching overhead.
