---
aliases: [Cluster Networking, K8s Networking, Pod Networking]
confidence: 5/5
created: 2025-12-16T14:10:00Z
epistemic: technical
last_reviewed: 2025-12-16
modified: 2025-12-16T13:53:14Z
purpose: To define the fundamental networking model of Kubernetes, including Pod-to-Pod communication, Services, and DNS resolution.
related-soTs: ["[[SoT - Cloud Networking Core Components]]", "[[SoT - Kubernetes Cluster State Architecture]]"]
review_interval: 1 year
see_also: ["[[A Detailed Examination of the TCP Packet and the Encapsulation Process]]", "[[Kubernetes Network Configuration Kubernetes Configures Each Pod with]]"]
source_of_truth: true
status: stable
tags: [dns, kubernetes, networking, service_discovery]
title: SoT - Kubernetes Networking & DNS
type: SoT
uid: 2025-12-16-K8S-NET
updated: 
---

## 1. The Core Model: Flat Network

> [!definition] The IP-per-Pod Rule
> Kubernetes mandates a **Flat Network** model where:
> 1.  Every Pod gets its own IP address.
> 2.  Every Pod can communicate with every other Pod without NAT (Network Address Translation).
> 3.  The IP that a Pod sees itself as is the same IP that others see it as.

---

## 2. Service Discovery (DNS)

Since Pods are ephemeral (IPs change), we need a stable address mechanism.

### The Service Abstraction

A **Service** provides a stable **ClusterIP** and DNS name. It acts as an internal Load Balancer.

-   **Mechanism:** `kube-proxy` (iptables) captures traffic to the Service IP and forwards it to a healthy backend Pod.

### CoreDNS (The Cluster Phonebook)
-   **Role:** The internal DNS server.
-   **Resolution:** Resolves `my-service.namespace.svc.cluster.local` to the Service's stable ClusterIP.
-   **Flow:** Pod -> CoreDNS -> Service IP -> iptables -> Target Pod IP.

---

## 3. Cross-Cloud DNS (The Hybrid Challenge)

In complex setups (AWS EKS <-> Azure AKS), services need to resolve names across cloud boundaries.

### The Resolution Chain
1.  **Pod:** Queries CoreDNS.
2.  **CoreDNS:** Configured with **Conditional Forwarding**. "If name ends in `.aws.internal`, forward to Azure VPN Gateway."
3.  **VPN:** Tunnel carries the query to AWS.
4.  **Route53:** AWS Resolver answers with the private IP.
5.  **Return:** Answer travels back -> CoreDNS -> Pod.

*See [[SoT - Cloud Networking Core Components]] for the underlying infrastructure.*

---

## 4. Ingress vs. Service

| Feature | Service | Ingress |
| :--- | :--- | :--- |
| **Layer** | Layer 4 (TCP/UDP) | Layer 7 (HTTP/HTTPS) |
| **Scope** | Internal (ClusterIP) or Single Port (NodePort) | External Entrypoint |
| **Routing** | IP/Port based | Host/Path based (`api.com/v1`) |
| **Role** | Internal Plumbing | The Front Door |

*See [[SoT - Kubernetes Cluster State Architecture#4. The Network Bridge: Ingress & Services|The Network Bridge]].*
