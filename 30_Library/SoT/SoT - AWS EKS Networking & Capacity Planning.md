---
aliases: ["AWS VPC CNI vs Calico", "EKS IP Planning", "EKS Networking"]
confidence: "5/5"
created: 2026-01-08T13:30:00Z
epistemic: "technical"
last_reviewed: "2026-01-08"
modified: 2026-01-23T18:09:21+00:00
purpose: "To define the IP addressing architecture, capacity planning formulas, and CNI strategies for AWS EKS clusters."
review_interval: "1 year"
see_also: ["[[SoT - FitFile Deployment - Networking & DNS]]", "[[SoT - Kubernetes Networking & DNS]]"]
source_of_truth: []
status: "stable"
tags: ["aws", "cni", "eks", "ip-planning", "networking"]
title: SoT - AWS EKS Networking & Capacity Planning
type: "SoT"
---

## 1. The EKS Networking Model

EKS networking is tightly coupled with the AWS VPC architecture. The choice of **Container Network Interface (CNI)** plugin determines how Pods consume IP addresses.

### 1.1 Default Mode: AWS VPC CNI

By default, EKS uses the Amazon VPC CNI plugin.

- **Direct VPC IPs:** Every Pod receives a real IP address from the VPC subnet, just like an EC2 instance.
- **Flat Network:** Pods are first-class citizens on the network. They can be reached directly by other VPC resources (VPN, Direct Connect, Peering) without NAT.
- **Constraint:** IP Exhaustion. A large cluster can quickly consume thousands of private IPs.

### 1.2 Alternative Mode: Overlay Networking (Calico/Cilium)

For environments with IP constraints (small VPC CIDRs):

- **Encapsulation:** Pods use a virtual IP range (e.g., `192.168.0.0/16`) that is _not_ part of the VPC.
- **VXLAN:** Traffic between nodes is encapsulated.
- **NAT:** Outbound traffic is NAT'd to the Node's IP.
- **Benefit:** Decouples Pod density from VPC IP limits.

---

## 2. Capacity Planning: The Formula

When using the **AWS VPC CNI**, you must rigorously plan subnet sizes.

### 2.1 The Variables

- **`N` (Nodes):** Total number of EC2 instances.
- **`P` (Pods per Node):** Maximum pods expected per node (Limit varies by instance type).
- **`S` (Services):** ClusterIPs (virtual, but some LoadBalancers consume IPs).
- **`B` (Buffer):** AWS reserves 5 IPs per subnet.

### 2.2 The Calculation

```plaintext
Total IPs Needed = (N × P) + N + LoadBalancers + Buffer
```

### 2.3 Example Scenario (FitFile Scale)

- **Nodes:** 50 (`m5.xlarge`, supports ~58 pods)
- **Pods:** 58 per node (Max density)
- **Services:** 50
- **Total:** `(50 * 58) + 50 + 50 ≈ 3,000 IPs`

**Recommendation:** A `/20` CIDR (4,096 IPs) is the minimum safe allocation for this scale.

| CIDR | Usable IPs | Use Case |
|:--- |:--- |:--- |
| `/24` | 251 | Small Test Cluster |
| `/22` | 1,019 | Standard Production |
| `/20` | 4,091 | High Scale / High Density |

---

## 3. Advanced IP Management Strategies

### 3.1 Secondary CIDR Blocks (Custom Networking)

If the primary VPC CIDR is exhausted (e.g., `10.0.0.0/24` is full), you can attach a secondary CIDR (e.g., `100.64.0.0/16`) to the VPC.

- **Configuration:** Set `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true`.
- **Isolation:** Pods run in the secondary range, keeping the primary range free for Nodes and other AWS services.

### 3.2 Prefix Delegation

Recent AWS VPC CNI versions support **Prefix Delegation**, assigning a `/28` prefix (16 IPs) to a Node instead of individual IPs. This increases Pod density per ENI and reduces API calls.
