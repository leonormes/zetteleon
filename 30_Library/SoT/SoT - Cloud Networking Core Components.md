---
aliases: [Cloud Internet Connectivity, Cloud Networking SoT, Internet Gateway vs NAT Gateway]
confidence: 
created: 2025-12-12T00:00:00Z
epistemic: 
last-synthesis: 2025-12-12
last_reviewed: 
modified: 2025-12-12T18:31:59Z
purpose: To define the essential networking components and architectural patterns required to establish connectivity between private cloud networks (VPC/VNet) and the public internet.
review_interval: 6 months
see_also: ["[[Cloud Networking MOC]]", "[[MOC - Cloud Networking Devices Data Flow]]"]
source_of_truth: true
status: stable
tags: [aws, azure, cloud, infrastructure, networking]
title: SoT - Cloud Networking Core Components
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> Cloud Internet Connectivity is not a default state but an engineered path. It requires three distinct layers to function:
> 1.  **Gateway Device:** A bridge between the private virtual network and the public internet.
> 2.  **Routing:** Explicit rules (`0.0.0.0/0`) directing traffic to that gateway.
> 3.  **Addressing:** Public IPs (identity) and NAT (translation) to permit communication.

---

## 2. Core Component 1: The Gateway (The Edge)

Gateways are the physical/virtual appliances that act as the portal for traffic.

### A. Internet Gateway (Bidirectional)
-   **Function:** Enables **Ingress and Egress**. It creates a 1:1 static NAT between a private instance IP and a Public IP.
-   **Use Case:** Public Web Servers, Load Balancers, Bastion Hosts.
-   **Cloud Implementation:**
    -   **AWS:** **Internet Gateway (IGW)**. Must be explicitly created and attached to the VPC.
    -   **Azure:** **Implicit.** Azure VNets have default outbound access via the backbone. For inbound, you associate a Public IP directly to a NIC or Load Balancer.

### B. NAT Gateway (Egress Only)
-   **Function:** Enables **Egress Only**. It performs Source NAT (SNAT), allowing private instances to initiate outbound connections (e.g., software updates) without accepting inbound connections.
-   **Use Case:** Private databases, application servers, worker nodes.
-   **Cloud Implementation:**
    -   **AWS:** **NAT Gateway**. A managed service deployed in a Public Subnet. Private subnets route to it.
    -   **Azure:** **NAT Gateway**. A managed service attached to a subnet. It takes precedence over default system routing.

---

## 3. Core Component 2: Routing (The Map)

Having a gateway is useless if the network doesn't know how to reach it.

-   **The Mechanism:** **Route Tables**.
-   **The Rule:** The "Default Route" (`0.0.0.0/0` for IPv4) determines the destination of all internet-bound traffic.
-   **Subnet Types:**
    -   **Public Subnet:** Route Table sends `0.0.0.0/0` -> **Internet Gateway**.
    -   **Private Subnet:** Route Table sends `0.0.0.0/0` -> **NAT Gateway**.
    -   **Isolated Subnet:** No route to `0.0.0.0/0`.

---

## 4. Core Component 3: Addressing (The Identity)

-   **Public IP:** A globally routable address.
    -   *AWS:* **Elastic IP (EIP)**. Static public IPs attached to NAT Gateways or Instances.
    -   *Azure:* **Public IP Address**. A standalone resource that can be bound to NAT Gateways, Load Balancers, or VMs.
-   **Private IP:** Non-routable (RFC1918) addresses used internally (e.g., `10.0.0.5`).

---

## 5. AWS vs. Azure Comparison Matrix

| Concept | AWS Component | Azure Component |
| :--- | :--- | :--- |
| **Virtual Network** | VPC | VNet |
| **Public Gateway** | Internet Gateway (IGW) | Implicit (or Public IP on NIC/LB) |
| **Private Egress** | NAT Gateway | Azure NAT Gateway |
| **Traffic Director** | Route Table | Route Table (UDR) |
| **Identity** | Elastic IP (EIP) | Public IP Address |

---

## 6. Architecture Patterns

### Pattern A: The Public Subnet
*Direct access to the internet.*
1.  **Resource:** EC2/VM with Public IP.
2.  **Route:** `0.0.0.0/0` -> Internet Gateway.
3.  **Flow:** Traffic leaves directly via IGW.

### Pattern B: The Private Subnet (Standard)
*Secure outbound access.*
1.  **Resource:** EC2/VM with Private IP only.
2.  **Route:** `0.0.0.0/0` -> NAT Gateway (which sits in a Public Subnet).
3.  **Flow:** Traffic -> NAT GW (SNAT) -> Internet Gateway -> Internet.

---

## 7. Sources and Links
-   [[Core Networking Components for Cloud Internet Connectivity]] (Archived Source)
-   [[Internet Gateway in AWS Networking]]
-   [[NAT Gateways Enable Private Resources to Access Internet]]
