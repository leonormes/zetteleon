---
aliases: [Cluster Networking, K8s Networking, Pod Networking]
confidence: 5/5
created: 2025-12-16T14:10:00Z
epistemic: technical
last_reviewed: 2025-12-18
modified: 2025-12-19T10:12:36Z
purpose: To define the fundamental networking model of Kubernetes, including Pod-to-Pod communication, Services, DNS resolution, and Network Policies.
related-soTs: ["[[SoT - Cloud Networking Core Components]]", "[[SoT - Kubernetes Cluster State Architecture]]"]
review_interval: 1 year
see_also: ["[[Kubernetes Network Configuration Kubernetes Configures Each Pod with]]", "[[MOC - Container Networking Model]]"]
source_of_truth: true
status: stable
tags: [cni, dns, kubernetes, networking, service_discovery]
title: SoT - Kubernetes Networking & DNS
type: SoT
uid: 2025-12-16-K8S-NET
updated:
---

## 1. The Core Model: Flat Network

> [!definition] The IP-per-Pod Rule
> Kubernetes mandates a **Flat Network** model where:
> 1.  Every Pod gets its own IP address (from the Pod CIDR range).
> 2.  Every Pod can communicate with every other Pod across Nodes without NAT (Network Address Translation).
> 3.  The IP that a Pod sees itself as is the same IP that others see it as.

This model allows Pods to be treated like VMs or physical hosts. It decouples networking from the underlying Node infrastructure.

### The Implementation: CNI (Container Network Interface)

The actual wiring is pluggable. **CNI Plugins** (like **Calico**, **Flannel**, **Cilium**) implement this flat network using different strategies:

-   **Overlay Networks (VXLAN/IP-in-IP):** Encapsulate packets to span across Nodes (e.g., Flannel).
-   **Direct Routing (BGP):** Route packets natively without encapsulation (e.g., Calico).

*For the deep dive on Linux primitives (Namespaces, Veth pairs), see [[MOC - Container Networking Model]].*

---

## 2. Service Discovery (DNS & Services)

Since Pods are ephemeral (IPs change), we need a stable address mechanism.

### The Service Abstraction

A **Service** provides a stable **ClusterIP** and DNS name. It acts as an internal, Layer 4 Load Balancer.

-   **ClusterIP:** Exposes the Service on an internal IP. Reachable only within the cluster.
-   **NodePort:** Exposes the Service on a static port on each Node's IP.
-   **LoadBalancer:** Provisions an external cloud load balancer (AWS ELB, GCP LB) to expose the Service.

### CoreDNS (The Cluster Phonebook)
-   **Role:** The internal DNS server.
-   **Resolution:** Resolves `my-service.namespace.svc.cluster.local` to the Service's stable ClusterIP.
-   **Flow:** Pod -> CoreDNS -> Service IP -> iptables/IPVS -> Target Pod IP.

---

## 3. External Traffic & Ingress

How traffic enters the cluster from the outside world.

| Feature | Service (Layer 4) | Ingress (Layer 7) |
| :--- | :--- | :--- |
| **Protocol** | TCP/UDP | HTTP/HTTPS |
| **Routing** | IP/Port based | Host/Path based (`api.com/v1`) |
| **Role** | Internal Plumbing / Simple External | The "Front Door" / Router |
| **Implementation** | `kube-proxy` (iptables) | **Ingress Controller** (Nginx, Traefik) |

-   **Ingress Controller:** A specialized Pod (usually exposed via a LoadBalancer Service) that routes HTTP traffic to internal Services based on rules defined in the `Ingress` resource.

---

## 4. Network Security (Policies)

By default, Kubernetes networking is **Open** (All-Allow). Any Pod can talk to any other Pod.

### Network Policies

To restrict traffic, we use **Network Policies**. These act as a firewall for Pods.

-   **Selector-Based:** Rules apply to Pods matching specific Labels (e.g., `app: database`).
-   **Default Deny:** A best practice is to deny all traffic and then explicitly allow required flows (Zero Trust).
-   **Requirement:** The underlying CNI plugin must support Network Policies (e.g., Calico supports them, Flannel does not).

---

## 5. Cross-Cloud DNS (Hybrid Connectivity)

In complex setups (AWS EKS <-> Azure AKS), services need to resolve names across cloud boundaries.

### The Resolution Chain
1.  **Pod:** Queries CoreDNS.
2.  **CoreDNS:** Configured with **Conditional Forwarding**. "If name ends in `.aws.internal`, forward to Azure VPN Gateway."
3.  **VPN:** Tunnel carries the query to AWS.
4.  **Route53:** AWS Resolver answers with the private IP.
5.  **Return:** Answer travels back -> CoreDNS -> Pod.

*See [[SoT - Cloud Networking Core Components]] for the underlying infrastructure.*

---

## 6. IPv4/IPv6 Dual Stack

Kubernetes supports assigning both IPv4 and IPv6 addresses to Pods and Services.

-   **Usage:** Enables incremental migration and compliance with IPv6 mandates.
-   **Config:** Requires `ipFamilies: [ipv4, ipv6]` in Pod/Service specs and a CNI that supports dual-stack.

---

## 7. Troubleshooting Heuristics

When networking fails, check layers bottom-up:

1.  **Pod-to-Pod:** Are Pods running? Is the CNI healthy? (Check `ip addr`, `ping` other Pod IPs).
2.  **Service Discovery:** Is CoreDNS running? Can you resolve the Service name? (`nslookup my-service`).
3.  **Service Connectivity:** Is `kube-proxy` running? Are endpoints populated? (`kubectl get endpoints`).
4.  **Network Policy:** Is a policy silently dropping traffic?
