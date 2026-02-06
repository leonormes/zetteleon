---
created: 2025-12-04T12:02:41Z
last_reviewed: null
modified: 2026-02-06T14:20:21+00:00
status: processing
tags: [state/thinking]
title: HEAD - IP Address Management for Indeterminate, Interconnecting Private Networks
type: head
updated: null
---

## IP Address Management for Indeterminate, Interconnecting Private Networks

This is a genuinely interesting problem space—it's essentially the configuration management challenge you already know, but at the network layer: how do you make distributed, evolving systems composable when you can't predict the final shape?

### The Core Principle: Hierarchical Aggregation with Sparse Allocation

The foundational idea is: allocate from large blocks, assign in small ones, and leave enormous gaps. This is analogous to a lattice—you define constraints at the top and let the structure narrow downward, never widening.

---

### 1. The RFC Standards That Govern This

|RFC|What It Does|
|---|---|
|RFC 1918|Defines the private ranges (10/8, 172.16/12, 192.168/16). The 10/8 space is the only one large enough for serious multi-network planning.|
|RFC 6598 (CGN Shared Space)|100.64.0.0/10—a "semi-private" range useful as a buffer when RFC 1918 collisions are unavoidable.|
|RFC 4632 (CIDR)|Classless Inter-Domain Routing—the mechanism that makes hierarchical, variable-length allocation possible at all.|
|RFC 2050 / RFC 7020|The _policy_ frameworks for how address space _should_ be delegated hierarchically (written for public IP, but the architectural model is what matters).|

Why this matters to you: RFC 2050's delegation model—IANA → RIR → LIR → End User—is the _template_ for any private IPAM hierarchy. You replicate this inside your organisation.

### 2. The Architectural Frameworks

#### A. Hierarchical Tiered Allocation (The "IANA Model" Applied Privately)

This is the industry standard approach used by hyperscalers and multi-cloud enterprises:

```
Organisation Master Block:  10.0.0.0/8
  ├── Region / Business Unit:  10.<region>.0/16   (e.g., 10.1.0.0/16 = EU)
  │     ├── Environment:        10.1.<env>/20     (e.g., 10.1.16.0/20 = prod)
  │     │     ├── VPC / Cluster: 10.1.16.0/24
  │     │     └── VPC / Cluster: 10.1.17.0/24
  │     └── Environment:        10.1.32.0/20        (staging)
  └── Region:                   10.2.0.0/16         (US)
```

Key rules:

- Sparse allocation—you assign /16s but only populate a few /24s within them. The gaps are your future-proofing.
- Summarisability—any tier can be described by a single CIDR prefix, which makes routing tables and firewall rules composable.
- No overlap by construction—if each branch of the tree is a strict subset of its parent and siblings don't overlap, you get non-collision as a _structural guarantee_ rather than a runtime check.

#### B. Cloud-Native IPAM Frameworks

|Framework|How It Handles Indeterminacy|
|---|---|
|AWS IPAM (native service)|Hierarchical pools with scope (region, org). Enforces non-overlap at allocation time.|
|Azure IPAM / vWAN|Hub-spoke with centrally managed address pools.|
|NetBox (open source)|The de facto standard for self-hosted IPAM. Models prefixes hierarchically with role/tenant/site metadata.|
|Infoblox|Enterprise IPAM with DHCP/DNS integration. Dominant in legacy enterprise.|
|phpIPAM|Lightweight open-source alternative to NetBox.|

#### C. Overlay / Tunnelling When Collision Is Unavoidable

When you inherit networks you didn't plan (M&A, partner integrations), overlaps are inevitable. The standard responses:

- RFC 8926 (GENEVE) / VXLAN (RFC 7348)—network overlays that give each tenant a virtual address space decoupled from the underlay. This is what every cloud provider uses internally.
- NAT with RFC 6598 space as a translation zone between colliding 10/8 ranges.
- WireGuard / IPsec tunnels with per-peer NAT—common for site-to-site VPN where neither side will renumber.

### 3. The Protocol Layer: How Peers Discover and Route

When topology is indeterminate, you need dynamic routing, not static:

- BGP (RFC 4271) with private ASNs (64512–65534, or 4-byte range)—the standard for advertising reachability between autonomous private networks. Each network advertises its allocated CIDR prefixes; BGP's path selection prevents loops.
- OSPF (RFC 2328)—for intra-domain dynamic routing within a single administrative boundary.
- BGP + EVPN (RFC 7432)—the modern standard for multi-tenant overlay networks, particularly in data centre fabrics.

The key insight: BGP is essentially a _distributed, eventually-consistent database of reachability claims_. It solves the "indeterminate topology" problem by letting each peer declare what it owns and having the network converge.

---

### The Analogy Back to Your World

This whole structure is strikingly similar to the CUE lattice problem you've been exploring:

|Network IPAM|Configuration Management|
|---|---|
|CIDR hierarchy (10/8 → /16 → /24)|Type hierarchy (top → struct → concrete)|
|Non-overlap by tree structure|Constraint satisfaction by unification|
|BGP advertising reachability|Service discovery / registry|
|Overlay when collision inevitable|Adapter/anti-corruption layer|

Both are about making composition safe when the final shape isn't known at design time.

---

### Concrete Next Action

If you're designing a multi-network strategy now, the single highest-leverage first step:

> Open NetBox (or a spreadsheet if you want zero friction), create your top-level prefix tree—just three levels deep—and assign every _existing_ network to a leaf. The gaps you see are your future allocation space. That map is the source of truth everything else builds on.

Want me to help you sketch that prefix tree for your actual infrastructure?

If you need scalable, non-overlapping connectivity between private networks even as sites/segments appear over time and the "final" topology isn't known, the industry-standard approach is to combine:

1. an addressing + routing architecture that supports _hierarchical delegation and summarization_, and
2. automated prefix/address allocation mechanisms (what most people practically mean by "IPAM protocols").

## Architectural Frameworks that Are the De Facto Standard

### 1) Hierarchical Addressing with Delegated Blocks (designed for aggregation)

Core idea: allocate big blocks "top-down" (org → region → site → segment), so _new_ networks can be added without collisions and routes can be summarized.

- IPv4 typically uses RFC1918 space (10/8, 172.16/12, 192.168/16) with a strict allocation policy. ([RFC Editor](https://www.rfc-editor.org/rfc/rfc1918.html?utm_source=chatgpt.com "RFC 1918: Address Allocation for Private Internets"))
- IPv6 commonly uses Unique Local Addresses (ULA) with randomly generated /48s per domain/site to make overlaps _unlikely_ even when groups connect later. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc4193?utm_source=chatgpt.com "RFC 4193 - Unique Local IPv6 Unicast Addresses - Datatracker"))

Why this fits "topology indeterminate": you can reserve/allocate contiguous space per future site/tenant and still keep route tables small via summarization.

---

### 2) VRF-based Segmentation with BGP/MPLS L3VPN (or Equivalent VRF overlays)

Core idea: treat each private network (tenant, environment, acquired company, etc.) as its own routing domain (VRF), then stitch them together in controlled ways.

- BGP/MPLS IP VPNs (RFC4364) are the canonical standard for scalable multi-site connectivity with isolation, using BGP to distribute VPN routing info. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/rfc4364/?utm_source=chatgpt.com "RFC 4364 - BGP/MPLS IP Virtual Private Networks (VPNs)"))

This becomes crucial when you _temporarily_ can't guarantee non-overlap (M&A is the classic case) while you migrate toward a clean global plan.

---

### 3) Overlay Networking for Scale and Mobility (datacenter / cloud)

If the "private networks" are virtualized/DC heavy, overlays are the norm:

- VXLAN (RFC7348) provides L2-over-L3 overlays to scale multi-tenant fabrics. ([RFC Editor](https://www.rfc-editor.org/rfc/rfc7348.html?utm_source=chatgpt.com "RFC 7348: Virtual eXtensible Local Area Network (VXLAN)"))
- EVPN (RFC7432) is a standard control-plane for Ethernet VPN services (often paired with VXLAN in modern fabrics). ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc7432?utm_source=chatgpt.com "RFC 7432 - BGP MPLS-Based Ethernet VPN"))

These are less about IPAM directly and more about keeping connectivity scalable while endpoints and segments churn.

---

## "IPAM protocols" That Are Actually Standard in Practice

Strictly speaking, IPAM is usually a system (DDI: DNS/DHCP/IPAM), but the standards that make automated, non-overlapping allocation work are:

### A) DHCP for Addresses, and DHCPv6 Prefix Delegation for _networks_

- DHCPv4: hands out host addresses from centrally managed pools (often with reservations).
- DHCPv6 Prefix Delegation (RFC3633): a key building block when topology is indeterminate—_it delegates whole prefixes to downstream routers_ and is explicitly intended to work without the delegator needing to know the downstream topology. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc3633?utm_source=chatgpt.com "RFC 3633 - IPv6 Prefix Options for Dynamic Host ..."))

This is the closest thing to an "industry-standard IPAM protocol" for _evolving site networks_.

### B) IPv6 ULA Generation Rules (to Prevent Collisions when Domains Later interconnect)

ULA is designed to be globally unique in practice (within the ULA universe) via pseudo-random generation. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc4193?utm_source=chatgpt.com "RFC 4193 - Unique Local IPv6 Unicast Addresses - Datatracker"))

### C) Dynamic DNS Updates (optional but Common in DDI automation)

- RFC2136 Dynamic DNS (DNS UPDATE) is widely used so that "who got which address/prefix" stays reflected in DNS automatically. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc2136?utm_source=chatgpt.com "RFC 2136 - Dynamic Updates in the Domain Name System ..."))

---

## What's Considered "standard practice" in Real Deployments

If your priority is non-overlap from day 1 while the edge keeps changing:

- Prefer IPv6-first internal addressing with ULA /48 per site/tenant (or GUAs if you have them), plus DHCPv6-PD for downstream prefix allocation. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc4193?utm_source=chatgpt.com "RFC 4193 - Unique Local IPv6 Unicast Addresses - Datatracker"))
- For IPv4, use RFC1918 with strict central allocation and aggressive summarization. ([RFC Editor](https://www.rfc-editor.org/rfc/rfc1918.html?utm_source=chatgpt.com "RFC 1918: Address Allocation for Private Internets"))
- Use VRFs (often via RFC4364-style L3VPN) to keep domains isolated and allow controlled connectivity. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/rfc4364/?utm_source=chatgpt.com "RFC 4364 - BGP/MPLS IP Virtual Private Networks (VPNs)"))
- Where overlap is unavoidable (common in multi-level private NAT "accidents"), recognize it as a known failure mode of NAT+DHC P sprawl and treat it as a migration smell, not an end state. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/rfc5684/?utm_source=chatgpt.com "RFC 5684 - Unintended Consequences of NAT ..."))
    
