---
aliases: [FitFile Networking Guide, Network Security SOP]
created: 2026-02-01T15:00:00Z
modified: 2026-02-01T15:07:47+00:00
status: evergreen
tags: [ff_deploy, networking, security, sot]
title: SoT - FitFile Deployment - Networking and Security
type: SoT
---

## 1. Overview

This document defines the applied networking and security architecture for FitFile deployments. While [[SoT - Kubernetes Networking & DNS]] defines the _theory_, this note defines the _implementation_ patterns for AWS and Azure.

---

## 2. Network Topology (Hub & Spoke)

We utilize a **Hub-and-Spoke** model to connect customer environments (Spokes) to Central Services (Hub).

### 2.1 The VNET/VPC Structure

Every deployment resides in a dedicated, isolated network (VNET/VPC) with strict subnet segmentation:

| Subnet | Purpose | Access |
|:---|:---|:---|
| **System** | Control plane components (AKS/EKS ENIs). | Private |
| **Workloads** | Application pods (FFNode). | Private |
| **Ingress/Egress** | Load Balancers and NAT Gateways. | Public (Filtered) |
| **Jumpbox** | Bastion host for administrative access. | Private (SSM/Bastion) |

### 2.2 Peering & Connectivity

- **VNET Peering**: Established between the Customer VNET and the Hub VNET to allow GitOps agents (ArgoCD) and Monitoring to reach the cluster.
- **Transitive Routing**: NOT enabled. Spoke A cannot talk to Spoke B.

---

## 3. DNS Architecture

### 3.1 Split-Horizon DNS

We use Private DNS Zones to manage internal service resolution across the peering link.

- **Zone Name**: `{customer_id}.internal` (e.g., `lca.internal`).
- **Linkage**: The Private DNS Zone must be linked to **BOTH** the Customer VNET and the Hub VNET.
- **Why**: Allows the Hub (ArgoCD) to resolve internal Load Balancer IPs for health checks and API calls.

### 3.2 External DNS

- **Public Zone**: Managed via Cloudflare or Azure DNS.
- **A-Records**: `*.{customer_id}.fitfile.net` -> Ingress Load Balancer IP.

---

## 4. Ingress & TLS

### 4.1 NGINX Ingress Controller

We deploy the NGINX Ingress Controller to manage Layer 7 routing.

- **Service Type**: `LoadBalancer` (Provisioned by Cloud Provider).
- **Annotations**:
  - `service.beta.kubernetes.io/azure-load-balancer-internal: "true"` (for internal-only deployments).

### 4.2 TLS Termination

- **Cert-Manager**: Automates certificate issuance.
- **Issuers**:
  - **LetsEncrypt Prod**: Used for public-facing endpoints (requires HTTP-01 or DNS-01 challenge).
  - **Internal CA**: Used for strictly private environments (requires Hub Vault PKI integration).

---

## 5. Security & Isolation

### 5.1 CNI & Network Policies (Calico)

We use **Calico** as the CNI (Container Network Interface) to enforce Zero Trust at the pod level.

- **Default Policy**: `deny-all` (Implicit).
- **Allow Rules**: Explicitly defined in Helm charts (e.g., "Frontend can talk to Backend on port 8080").

### 5.2 Workload Identity

We strictly avoid long-lived cloud credentials (Access Keys).

- **Azure**: Workload Identity (Federated Identity Credential).
- **AWS**: IRSA (IAM Roles for Service Accounts).
- **Mechanism**: K8s ServiceAccount tokens are exchanged for short-lived Cloud Access Tokens via OIDC.

### 5.3 Secrets Management

- **Source of Truth**: HCP Vault (Central).
- **Delivery**: Vault Secrets Operator (VSO).
- **Policy**: Secrets are injected as K8s Secrets or mounted volumes. No secrets in Git.
- **Reference**: [[SoT - FITFILE Secret Management Architecture]].

---

## 6. Firewall Requirements (Client-Side)

For successful deployment, the client's firewall must allow:

**Inbound (To FitFile):**
- **443/TCP (HTTPS)**: From Client Network -> FitFile Load Balancer IP.

**Outbound (From FitFile):**
- **443/TCP**: To `*.gitlab.com` (Config).
- **443/TCP**: To `*.vault.hashicorp.cloud` (Secrets).
- **443/TCP**: To `*.azurecr.io` / `*.ecr.aws` (Images).
- **443/TCP**: To `*.auth0.com` (Identity).
