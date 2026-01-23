---
aliases: ["Container Networking Primitives", "IPTables Masquerade", "Linux Bridges", "Veth Pairs"]
confidence: "High"
created: 2025-12-30T13:53:16+00:00
epistemic: "Technical"
last_reviewed: 
modified: 2026-01-23T18:09:19+00:00
purpose: "To define the low-level Linux kernel networking constructs that underpin all container networking abstractions."
review_interval: "1 year"
see_also: ["[[SoT - Kubernetes Networking & DNS]]", "[[SoT - Linux Container Primitives]]"]
source_of_truth: []
status: "Active"
tags: ["kernel", "SoftwareEngineering/Containers", "SoftwareEngineering/Linux", "SoftwareEngineering/Networking"]
title: SoT - Linux Networking Primitives
type: "SoT"
uid: 
updated: 
---

## SoT - Linux Networking Primitives

> **Definitive Statement:** Container networking is not magic; it is the automation of standard Linux kernel primitives. Understanding these three components—**Veth Pairs**, **Bridges**, and **IPTables**—demystifies how a container communicates with the world.

### 1. The Core Primitives

#### A. Network Namespaces (The Isolation Layer)

A **Network Namespace (`netns`)** is a logical copy of the network stack. Each namespace has its own:

- Routing Table.
- IP Address space.
- Firewall rules (iptables).
- Network Interfaces (`lo`, `eth0`).

**Key Concept:** The "Host" is just the root namespace. Containers are just processes running in a child namespace.

#### B. Veth Pairs (The Virtual Cable)

A **Virtual Ethernet (veth)** pair is a linked pair of network interfaces. Packets transmitted on one interface immediately appear on the other.

- **Function:** To tunnel traffic between the **Host Namespace** and a **Container Namespace**.
- **Architecture:**
    - `veth0` (Host side): Attached to a Bridge.
    - `veth1` (Container side): Renamed to `eth0` inside the container namespace.

#### C. Linux Bridge (The Virtual Switch)

A **Linux Bridge** is a software implementation of a Layer 2 Ethernet switch. It forwards packets based on MAC addresses.

- **Function:** To connect multiple veth pairs (containers) together on the same host, allowing them to talk to each other and the host's physical interface (`eth0`).
- **Mechanism:**
    - It maintains a MAC Address Table (CAM Table).
    - If the destination MAC is known, it forwards to the specific port (veth).
    - If unknown, it broadcasts to all ports.

#### D. IPTables & NAT (The Router/Firewall)

**IPTables** (or its successor `nftables`) handles Packet Filtering and Network Address Translation (NAT).

##### 1. Masquerade (Source NAT)

When a container (Private IP: `10.244.1.5`) sends a packet to the Internet (`8.8.8.8`), the return packet must know how to get back.

- **Problem:** The outside world doesn't know about `10.244.1.5`.
- **Solution:** The kernel replaces the Source IP with the Host's Physical IP (`192.168.1.100`) as it leaves the interface.
- **Rule:** `iptables -t nat -A POSTROUTING -s 10.244.0.0/16 -j MASQUERADE`

##### 2. DNAT (Destination NAT)

Used for **Services**.

- **Function:** Intercepts traffic destined for a virtual VIP (ClusterIP) and rewrites the Destination IP to a specific Pod IP.

---

### 2. The Traffic Flow (Life of a Packet)

#### Scenario: Container A to Internet

1. **Container:** App sends packet to `8.8.8.8`. Route table says "Default Gateway is `cni0`".
2. **Veth:** Packet travels `eth0` (Container) -> `vethXXXX` (Host).
3. **Bridge:** Bridge receives packet on `vethXXXX`. Sees dest MAC is Gateway. Hands off to Host IP Stack.
4. **Routing:** Host Kernel sees Dest IP `8.8.8.8`. Route table says "Use physical `eth0`".
5. **IPTables (NAT):** POSTROUTING chain sees packet leaving. Replaces Source IP (`10.x`) with Host IP (`192.x`).
6. **Wire:** Packet leaves physical NIC.

---

### 3. IP Forwarding (The Kernel Switch)

By default, Linux drops packets not destined for itself. For a host to act as a router, **IP Forwarding** must be enabled.

- **Command:** `sysctl -w net.ipv4.ip_forward=1`

---

### 4. Observability (CLI Archeology)

#### Breakdown: `ip addr show`

The command `ip addr show` displays the link-layer (MAC) and network-layer (IP) state of all interfaces.

##### Interface 1: Loopback (`lo`)

`1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000`

- **Flags:** `<LOOPBACK,UP,LOWER_UP>` means it is a local interface, software-enabled, and the link layer is active.
- **MTU 65536:** High MTU because traffic never leaves the RAM.
- **Scope host:** IP `127.0.0.1` is only reachable from within the machine.
- **Lifetime:** `valid_lft forever` means the address does not expire.

##### Interface 2: Ethernet (`eth0`)

`2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000`

- **Flags:** `<BROADCAST,MULTICAST>` indicates capability for one-to-many communication.
- **MTU 1500:** Standard Ethernet frame size.
- **Scope global:** IP `192.168.x.x` is accessible on the local network.
- **Dynamic:** The address was assigned via DHCP.
- **Scope link:** IPv6 `fe80::` address is valid only for the local segment.
