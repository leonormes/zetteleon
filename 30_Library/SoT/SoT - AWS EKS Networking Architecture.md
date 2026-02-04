---
aliases: ["AWS VPC CNI vs Calico", "EKS IP Planning", "EKS Networking Requirements", "EKS Networking"]
created: 2026-02-01T21:19:14+00:00
last-synthesis: 2026-02-01
modified: 2026-02-04T07:27:24+00:00
source_of_truth: true
status: evergreen
synthesis-count: 2
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
    - Outbound for DNS on `TCP/UDP 53`.
    - Inter-node communication protocols.

---

### 2. Pod Networking Layer (CNI & IP Management)

The choice of Container Network Interface (CNI) plugin determines how Pods consume IP addresses.

#### 2.1 Default Mode: AWS VPC CNI

By default, EKS uses the Amazon VPC CNI plugin.

- Direct VPC IPs: Every Pod receives a real IP address from the VPC subnet, just like an EC2 instance.
- Flat Network: Pods are first-class citizens. They can be reached directly by other VPC resources (VPN, Direct Connect) without NAT.
- Constraint: IP Exhaustion. A large cluster can quickly consume thousands of private IPs.

#### 2.2 Capacity Planning: The Formula

When using the AWS VPC CNI, you must rigorously plan subnet sizes.

Calculation: `Total IPs Needed = (N × P) + N + LoadBalancers + Buffer`

- `N`: Number of Nodes
- `P`: Max pods per node (Instance limit)
- `Buffer`: 5 IPs reserved by AWS per subnet

Example (FitFile Scale):

50 Nodes (`m5.xlarge`, 58 pods/node) ≈ 3,000 IPs.

- Recommendation: Minimum `/20` CIDR (4,096 IPs).

---

## Current Understanding

### 3. Advanced Configurations

#### 3.1 Overlay Networking (Calico/Cilium)

For environments with IP constraints (small VPC CIDRs):

- Encapsulation: Pods use a virtual IP range (e.g., `192.168.0.0/16`) outside the VPC.
- Benefit: Decouples Pod density from VPC IP limits.

#### 3.2 Secondary CIDR Blocks

If the primary VPC CIDR is exhausted, you can attach a secondary CIDR (e.g., `100.64.0.0/16`) to the VPC and configure the CNI to place pods there (`AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true`).

#### 3.3 Hybrid Node Networking

Connecting on-premises infrastructure to EKS:

- Constraint: Requires reliable connection (VPN/Direct Connect) with <200ms latency.
- IP Addressing: IPv4 only. RFC1918 CIDRs for on-prem nodes/pods must not overlap with VPC or Service CIDRs.
- Routing: VPC Route Tables must direct traffic for on-prem CIDRs to the VPN/DX Gateway.
- Security: Hybrid nodes require Security Group rules allowing inbound traffic from on-prem CIDRs.
