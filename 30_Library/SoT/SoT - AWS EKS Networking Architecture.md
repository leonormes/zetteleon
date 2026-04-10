---
aliases: ["AWS VPC CNI vs Calico", "EKS IP Planning", "EKS Networking Requirements", "EKS Networking"]
created: 2026-02-01T21:19:14+00:00
last-synthesis: 2026-04-04
modified: 2026-04-10T16:52:06+00:00
source_of_truth: true
status: evergreen
synthesis-count: 3
tags: [domain/cloud, networking, provider/aws, service/eks, type/SoT]
title: SoT - AWS EKS Networking Architecture
trust-level: working-knowledge
---

## Minimum Viable Understanding (MVU)

EKS networking relies on a dual-layer architecture: the Infrastructure Layer (VPC, Subnets, Security Groups) and the Pod Networking Layer (CNI, IP Assignment). Success requires ensuring at least two subnets in different AZs, defining strict Security Groups for Control Plane access, and rigorously planning IP capacity using the `(N*P) + B` formula to prevent exhaustion.

## Working Knowledge

### 1. Infrastructure Requirements (The Foundation)

Before pods can run, the cluster infrastructure must be established.

#### 1.1 VPC & Subnet Architecture

- VPC: Must use an existing VPC or create a new one. Once associated with a cluster, the VPC cannot be changed.
- Subnets: Minimum of 2 subnets in different AZs.
    - _Public Subnets:_ Route to Internet Gateway (IGW). Nodes need Public IPs.
    - _Private Subnets:_ No direct internet access. Nodes require a NAT Gateway for outbound access or VPC Endpoints for private AWS service access.
- Connectivity:
    - _Public Endpoint:_ Traffic travels via internet/NAT.
    - _Private Endpoint:_ Traffic stays within VPC (more secure).

#### 1.2 Security Groups (Firewalls)

EKS uses Security Groups to control traffic boundaries:

- Cluster SG: Created by EKS automatically. Allows Cluster ↔ VPC traffic.
- Control Plane SG: Must allow inbound `TCP 443` from management networks (e.g., VPN, Bastion).
- Node SG: Must allow:
    - Outbound to Cluster SG on `TCP 443` (API) & `TCP 10250` (Kubelet).
    - Outbound from Node SG to Control Plane SG on `TCP 443`.
    - Inbound from Control Plane SG on `TCP 443` and `TCP 10250`.

#### 1.3 Common Operational Scenarios

##### Scenario: Outbound Connectivity from a Private Subnet (The Jumpbox Pattern)

To enable a resource (like a jumpbox) in a private subnet to make external requests, the following chain must be intact:

1. Private Subnet: Hosts the resource.
2. NAT Gateway: Located in a Public Subnet within the same VPC.
3. Route Table (Private): Must have a route `0.0.0.0/0` pointing to the `nat-gateway-id`.
4. Internet Gateway (IGW): Attached to the VPC.
5. Route Table (Public): Must have a route `0.0.0.0/0` pointing to the `igw-id`.
6. Network ACLs/Security Groups: Must allow outbound traffic on the required ports and return traffic (ephemeral ports).

---

## 2. Pod Networking Layer (The Runtime)

(Reserved for CNI, Calico, and IP Planning details)

---

## 3. Advanced Configurations

### 3.1 Custom Networking (Secondary CIDR)

Assigning a secondary CIDR range to pods to bypass VPC IP exhaustion.

### 3.2 Security Group for Pods

Assigning specific Security Groups directly to Kubernetes pods for fine-grained network control.

### 3.3 Hybrid Node Networking

Connecting on-premises infrastructure to EKS:

- Constraint: Requires reliable connection (VPN/Direct Connect) with <200ms latency.
- IP Addressing: IPv4 only. RFC1918 CIDRs for on-prem nodes/pods must not overlap with VPC or Service CIDRs.
- Routing: VPC Route Tables must direct traffic for on-prem CIDRs to the VPN/DX Gateway.
- Security: Hybrid nodes require Security Group rules allowing inbound traffic from on-prem CIDRs.
