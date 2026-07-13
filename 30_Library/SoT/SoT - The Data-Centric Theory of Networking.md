---
aliases: [Host-based Routing, Networking Indirection, Path-based Routing, The Packet Journey]
created: 2025-03-14T13:38:49+00:00
modified: 2026-07-13T08:52:54+00:00
permalink: llmeon/30-library/so-t/so-t-the-data-centric-theory-of-networking
tags: [data-centric, routing, SoftwareEngineering/Architecture, SoftwareEngineering/Networking, topic/technology]
title: SoT - The Data-Centric Theory of Networking
---

## 1. Definitive Statement

> [!definition] Definition
> Data-Centric Networking treats network addresses not as physical locations, but as stable service endpoints. It relies on layers of indirection (Load Balancers, Ingress Controllers) to decouple the public identifier from the transient, physical implementation.

---

## 2. The Packet Journey: Sequential Transformations

A data-centric approach examines how packets are transformed by each network device, revealing the logic of the distributed system.

### 2.1 Load Balancer (Layer 7)

- Incoming: `Source: Client IP` | `Dest: LB Public IP` | `Port: 443`
- Transformation: LB terminates TLS, parses headers, selects target.
- Outgoing: `Source: LB Internal IP` | `Dest: Target IP` | `Port: 8080` (with `X-Forwarded-For` header).

### 2.2 NAT Gateway (Egress)

- Incoming: `Source: Private IP` | `Dest: External IP`
- Transformation: Gateway maps Private IP:Port to its own Public IP:Ephemeral Port in a state table.
- Outgoing: `Source: Gateway Public IP` | `Dest: External IP`

### 2.3 VPN Gateway (Encapsulation)

- Incoming: `Source: Private IP` | `Dest: Remote IP`
- Transformation: Gateway encrypts payload (AES) and wraps it in an ESP (IPsec) header.
- Outgoing: `Source: Gateway Public IP` | `Dest: Remote VPN IP` (Protocol 50).

### 2.4 API Gateway (Management)

- Transformation: Injects `X-Correlation-ID`, validates JWT, and routes based on URI path (e.g., `/api/v1/orders` $\to$ `orders-service`).

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

## 6. Case Study: ArgoCD Protocol-Based Routing

The ArgoCD API server demonstrates the complexity of Protocol-Based Routing, where a single service exposes both gRPC (CLI) and HTTP (UI) on the same port (443). This requires sophisticated L7 indirection to resolve.

### A. The Challenge: Multiplexing gRPC and HTTP

- UI (HTTP/1.1 or 2): Standard web traffic.
- CLI (gRPC): Requires HTTP/2 with specific headers (`Content-Type: application/grpc`).
- The Constraint: Most Ingress controllers (e.g., NGINX) bind a specific backend protocol to an entire rule set, creating a conflict when mixing protocols on a single host.

### B. Indirection Strategies

1. Host-Based Separation (L7): Define two Ingress objects with different subdomains (e.g., `argocd.example.com` for UI and `grpc.argocd.example.com` for CLI). Each Ingress uses a protocol-specific annotation (e.g., `backend-protocol: "GRPC"`).
2. SSL Passthrough (L4): Bypass L7 processing by using `ssl-passthrough: "true"`. The Ingress acts as a raw TCP proxy, sniffing the SNI header to route traffic but leaving TLS termination to the `argocd-server` pod.
    - _Trade-off_: Higher CPU load on the pod; loss of L7 features (WAF, header injection) at the edge.
3. Protocol Multiplexing (L7): Modern controllers (Traefik, Contour) can inspect the `Content-Type` header to route traffic to different backend configurations on the same host/port without splitting.

This case study illustrates that Routing is an inspection operation: the deeper the gateway looks into the data (L4 vs L7 vs Header-specific), the more sophisticated the indirection becomes.
