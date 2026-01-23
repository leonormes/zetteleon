---
aliases: ["Host-based Routing", "Networking Indirection", "Path-based Routing"]
confidence: "5/5"
created: 2025-03-14T13:38:49Z
epistemic: "theory"
last_reviewed: "2025-12-23"
modified: 2026-01-23T18:09:17+00:00
purpose: "To define the principles of indirection, stable service endpoints, and routing logic in modern network architecture."
review_interval: "6 months"
see_also: ["[[SoT - Cloud Networking Core Components]]", "[[SoT - The Data Architecture of DNS]]"]
source_of_truth: []
status: "stable"
tags: ["data-centric", "routing", "SoftwareEngineering/Architecture", "SoftwareEngineering/Networking", "topic/technology"]
title: SoT - The Data-Centric Theory of Networking
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> **Data-Centric Networking** treats network addresses not as physical locations, but as **stable service endpoints**. It relies on layers of indirection (Load Balancers, Ingress Controllers) to decouple the public identifier from the transient, physical implementation.

---

## 2. Technical Nuance: DNS Name vs. Host Header

A single network request involves two distinct properties that are often conflated:

1. **The DNS Name:** Used by the client to find the **IP address** of the entry point (The "Where").
2. **The HTTP Host Header:** Sent _inside_ the request to tell the server which service is requested (The "Who").

**The Virtual Hosting Principle:** Because these two can be technically separated (e.g., via `curl`), a single IP address (one Load Balancer) can handle hundreds of distinct hostnames by inspecting the `Host` header.

---

## 3. Routing Patterns

### A. Host-Based Routing

Used to expose distinct domains on shared infrastructure.

- `https://relay.fitfile.net` -> Routes to Relay Pool.
- `https://api.fitfile.net` -> Routes to API Pool.
- **Logic:** The gateway looks at the **Host Header**.

### B. Path-Based Routing (API Gateway)

Used to expose multiple services under a single domain.

- `https://relay.fitfile.net/relay/` -> Routes to Relay Pool.
- `https://relay.fitfile.net/api/` -> Routes to API Pool.
- **Logic:** The gateway looks at the **URL Path**.

---

## 4. The Power of Indirection

By pointing DNS records to a Load Balancer instead of a host, you achieve:

- **Zero-Downtime Maintenance:** Removing nodes from the pool for updates.
- **Geographic Optimization (GeoDNS):** Returning different IPs based on user location to minimize latency.
- **Security Isolation:** Terminating TLS at the edge and protecting backend hosts from direct internet exposure.

---

## 5. Case Study: Kubernetes DNS Resolution

In Kubernetes, "Networking" is simply the propagation of configuration state through three layers of abstraction.

### A. The Configuration Chain

1. **The Pod (Source of Truth):** The Pod spec defines the `dnsPolicy`.
2. **The Container (Runtime):** Kubernetes injects a `/etc/resolv.conf` file based on the Pod's spec.
3. **The Process (Consumer):** The application reads `/etc/resolv.conf` to find the Nameserver IP (CoreDNS).

### B. The Resolution Logic

The application does not "know" networking. It strictly follows the data path:

1. **Query:** `curl relay`
2. **Expansion:** Application appends search domains from `resolv.conf` (e.g., `relay.default.svc.cluster.local`).
3. **Lookup:** Sends query to the Nameserver IP defined in `resolv.conf`.

This demonstrates that "resolution" is not a magic network property, but a file-read operation followed by a structured query.
