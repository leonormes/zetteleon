---
aliases: ["Host-based Routing", "Networking Indirection", "Path-based Routing", "The Packet Journey"]
created: 2025-03-14T13:38:49Z
last_reviewed: "2026-04-04"
modified: 2026-04-04T12:00:00Z
status: "stable"
tags: ["data-centric", "routing", "SoftwareEngineering/Architecture", "SoftwareEngineering/Networking", "topic/technology"]
title: SoT - The Data-Centric Theory of Networking
type: "SoT"
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> Data-Centric Networking treats network addresses not as physical locations, but as stable service endpoints. It relies on layers of indirection (Load Balancers, Ingress Controllers) to decouple the public identifier from the transient, physical implementation.

---

## 2. The Packet Journey: Sequential Transformations

A data-centric approach examines how packets are transformed by each network device, revealing the logic of the distributed system.

### 2.1 Load Balancer (Layer 7)
- **Incoming:** `Source: Client IP` | `Dest: LB Public IP` | `Port: 443`
- **Transformation:** LB terminates TLS, parses headers, selects target.
- **Outgoing:** `Source: LB Internal IP` | `Dest: Target IP` | `Port: 8080` (with `X-Forwarded-For` header).

### 2.2 NAT Gateway (Egress)
- **Incoming:** `Source: Private IP` | `Dest: External IP`
- **Transformation:** Gateway maps Private IP:Port to its own Public IP:Ephemeral Port in a state table.
- **Outgoing:** `Source: Gateway Public IP` | `Dest: External IP`

### 2.3 VPN Gateway (Encapsulation)
- **Incoming:** `Source: Private IP` | `Dest: Remote IP`
- **Transformation:** Gateway encrypts payload (AES) and wraps it in an ESP (IPsec) header.
- **Outgoing:** `Source: Gateway Public IP` | `Dest: Remote VPN IP` (Protocol 50).

### 2.4 API Gateway (Management)
- **Transformation:** Injects `X-Correlation-ID`, validates JWT, and routes based on URI path (e.g., `/api/v1/orders` $\to$ `orders-service`).

---

## 3. Technical Nuance: DNS Name vs. Host Header

A single network request involves two distinct properties that are often conflated:

1. The DNS Name: Used by the client to find the IP address of the entry point (The "Where").
2. The HTTP Host Header: Sent _inside_ the request to tell the server which service is requested (The "Who").

The Virtual Hosting Principle: Because these two can be technically separated (e.g., via `curl`), a single IP address (one Load Balancer) can handle hundreds of distinct hostnames by inspecting the `Host` header.

---

## 3. Routing Patterns

### A. Host-Based Routing

Used to expose distinct domains on shared infrastructure.

- `https://relay.fitfile.net` -> Routes to Relay Pool.
- `https://api.fitfile.net` -> Routes to API Pool.
- Logic: The gateway looks at the Host Header.

### B. Path-Based Routing (API Gateway)

Used to expose multiple services under a single domain.

- `https://relay.fitfile.net/relay/` -> Routes to Relay Pool.
- `https://relay.fitfile.net/api/` -> Routes to API Pool.
- Logic: The gateway looks at the URL Path.

---

## 4. The Power of Indirection

By pointing DNS records to a Load Balancer instead of a host, you achieve:

- Zero-Downtime Maintenance: Removing nodes from the pool for updates.
- Geographic Optimization (GeoDNS): Returning different IPs based on user location to minimize latency.
- Security Isolation: Terminating TLS at the edge and protecting backend hosts from direct internet exposure. See [[SoT - Network Security Architecture]] for the broader taxonomy of enforcement points.

---

## 5. Case Study: Kubernetes DNS Resolution

In Kubernetes, "Networking" is simply the propagation of configuration state through three layers of abstraction.

### A. The Configuration Chain

1. The Pod (Source of Truth): The Pod spec defines the `dnsPolicy`.
2. The Container (Runtime): Kubernetes injects a `/etc/resolv.conf` file based on the Pod's spec.
3. The Process (Consumer): The application reads `/etc/resolv.conf` to find the Nameserver IP (CoreDNS).

### B. The Resolution Logic

The application does not "know" networking. It strictly follows the data path:

1. Query: `curl relay`
2. Expansion: Application appends search domains from `resolv.conf` (e.g., `relay.default.svc.cluster.local`).
3. Lookup: Sends query to the Nameserver IP defined in `resolv.conf`.

This demonstrates that "resolution" is not a magic network property, but a file-read operation followed by a structured query.
