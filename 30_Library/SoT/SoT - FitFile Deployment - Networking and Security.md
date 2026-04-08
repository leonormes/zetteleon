---
aliases: [FitFile Networking Guide, Network Security SOP]
created: 2026-02-01T15:00:00Z
modified: 2026-04-08T18:01:06+00:00
status: evergreen
tags: [ff_deploy, networking, security, sot]
title: SoT - FitFile Deployment - Networking and Security
type: SoT
---

## 1. Overview

This document defines the applied networking and security architecture for FitFile deployments. While [[SoT - Kubernetes Networking & DNS]] defines the _theory_, this note defines the _implementation_ patterns for AWS and Azure.

---

## 2. Network Topology (Hub & Spoke)

We utilize a Hub-and-Spoke model to connect customer environments (Spokes) to Central Services (Hub).

### 2.1 The VNET/VPC Structure

Every deployment resides in a dedicated, isolated network (VNET/VPC) with strict subnet segmentation:

| Subnet | Purpose | Access |
|:---|:---|:---|
| System | Control plane components (AKS/EKS ENIs). | Private |
| Workloads | Application pods (FFNode). | Private |
| Ingress/Egress | Load Balancers and NAT Gateways. | Public (Filtered) |
| Jumpbox | Bastion host for administrative access. | Private (SSM/Bastion) |

### 2.2 Peering & Connectivity

- VNET Peering: Established between the Customer VNET and the Hub VNET to allow GitOps agents (ArgoCD) and Monitoring to reach the cluster.
- Transitive Routing: NOT enabled. Spoke A cannot talk to Spoke B.

---

## 3. Boundary Security: The Hub Firewall Mandate

For environments processing Special Category Data (GDPR Article 9, e.g., medical records), a Layer 4 Network Security Group (NSG) is fundamentally inadequate as a primary boundary.

### 3.1 Why NSGs Are Insufficient

An NSG operates at OSI Layers 3-4 (IP/Port). It cannot:

- Identify application-layer exploits (SQL Injection, XSS).
- Detect data exfiltration concealed in permitted flows.
- Terminate and inspect TLS-encrypted payloads.

### 3.2 The Defence-in-Depth Model

All public inbound traffic MUST traverse the Azure Hub Firewall (Layer 7 / WAF) before reaching the spoke.

1. Layer 7 (Hub): Terminates TLS, applies WAF rulesets, and provides Intrusion Detection (IDPS).
2. Layer 4 (Spoke): The NSG provides a secondary boundary, enforcing network segmentation and restricting source IPs.

> [!danger] The "Trusted Source" Fallacy
> Restricting an NSG to a single trusted external IP address does NOT remove the need for Layer 7 inspection. If the source system is compromised, the attacker inherits the trust conferred by the IP allow-list.

---

## 4. DNS Architecture

### 4.1 Split-Horizon DNS

We use Private DNS Zones to manage internal service resolution across the peering link.

- Zone Name: `{customer_id}.internal` (e.g., `lca.internal`).
- Linkage: Linked to BOTH the Customer VNet and the Hub VNet.
- Verification: `dig {host}` should return the private IP (TTL 0), while `dig +trace {host}` should return the public Cloudflare IP.

---

## 5. Ingress & TLS

### 5.1 NGINX Ingress Controller

- Service Type: `LoadBalancer`.
- Annotations: `service.beta.kubernetes.io/azure-load-balancer-internal: "true"` for internal-only deployments.

### 5.2 TLS Termination

- Cert-Manager: Automates issuance via Let's Encrypt (DNS-01) or Internal CA.
- DNS-01 Requirement: Mandatory for private clusters where HTTP-01 challenges cannot reach the Ingress.

---

## 6. Security & Isolation

### 6.1 CNI & Network Policies (Calico)

We use Calico to enforce Zero Trust at the pod level. Default policy is `deny-all`.

### 6.2 Workload Identity

No long-lived cloud credentials in K8s.

- Azure: Workload Identity (Federated Identity Credential).
- Mechanism: K8s ServiceAccount tokens are exchanged for Cloud Access Tokens via OIDC.

### 6.3 Firewall Requirements (Client-Side)

| Direction | Protocol | Destination | Purpose |
|:---|:---|:---|:---|
| Inbound | 443/TCP | LB IP | Client Access |
| Outbound | 443/TCP | `*.gitlab.com` | Config Sync |
| Outbound | 443/TCP | `*.vault.hashicorp.cloud` | Secrets |
| Outbound | 443/TCP | `*.azurecr.io` | Image Pull |

## Related Documentation

- [[SoT - Azure Resource Manager Architecture]]
- [[SoT - AKS IP Allocation & Subnet Sizing]]
- [[Protocol - Azure Jumpbox Preflight]]
