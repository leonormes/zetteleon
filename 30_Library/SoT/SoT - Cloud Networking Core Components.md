---
aliases: [AWS vs Azure Networking, Cloud Networking Concepts, VPC and VNet Fundamentals]
created: 2025-12-29T20:01:57+00:00
last_reviewed: null
modified: 2026-07-13T08:45:10+00:00
permalink: llmeon/30-library/so-t/so-t-cloud-networking-core-components
status: Active
tags: [aws, azure, cloud, kubernetes, networking]
title: SoT - Cloud Networking Core Components
type: SoT
updated: null
---

> The Core Abstraction: Cloud networking is an overlay. While the physical implementation differs, both AWS and Azure expose the same logical primitives: Isolation (VPC/VNet), Segmentation (Subnets), Routing (Route Tables), and Filtering (Security Groups/NSGs).

## 1. Universal Concepts & Cloud Mapping

| Universal Concept | Definition | AWS Implementation | Azure Implementation |
|:--- |:--- |:--- |:--- |
| Virtual Network | A logically isolated network slice within the cloud. | VPC (Virtual Private Cloud) | VNet (Virtual Network) |
| Subnet | A segmented range of IP addresses within the virtual network. | Subnet (AZ-specific) | Subnet (Region-wide) |

> Deep Dive: In Azure, a VNet is not physical; it is a JSON Policy Document stored in the [[SoT - Azure Resource Manager Architecture|ARM Database]]. The network effect is achieved by programming the SDN layer to respect this policy.

| Firewall (Stateful) | Rules controlling traffic to/from an instance/interface. | Security Group (Instance level) | Network Security Group (Subnet/NIC level) |

| Firewall (Stateless) | Rules controlling traffic in/out of a subnet. | NACL (Network ACL) | NSG (Can act as both) |

| Routing | Rules defining next-hop paths for traffic. | Route Table | Route Table (UDR) |

| Ingress (L7) | HTTP/HTTPS load balancing. | ALB (Application Load Balancer) | Application Gateway |

| Ingress (L4) | TCP/UDP load balancing. | NLB (Network Load Balancer) | Azure Load Balancer |

| Egress (NAT) | Allowing private instances to reach the internet. | NAT Gateway | NAT Gateway |

| Private Access | Accessing cloud services without public internet. | PrivateLink (Interface Endpoint) | Private Endpoint |

| Interconnect | Dedicated physical link to on-premise. | Direct Connect | ExpressRoute |

## 2. Kubernetes Integration (EKS Vs AKS)

Both platforms use the CNI (Container Network Interface) standard to bridge the Cloud Network with the Cluster Network.

### AWS EKS (VPC CNI)

- Mechanism: Pods receive real IPs from the VPC Subnet.
- Constraint: Pod density is limited by the number of ENIs (Elastic Network Interfaces) and IPs an EC2 instance can hold.
- Security: Security Groups can be applied directly to Pods (Security Groups for Pods).

### Azure AKS (Azure CNI Vs Kubenet)

- Azure CNI: Similar to AWS. Pods get VNet IPs. High performance, high IP consumption.
- Kubenet: Uses a simpler overlay (NAT). Pods get internal IPs not visible to the VNet. Saves IP space but adds a NAT hop.

## 3. The Routing Logic (The Path of a Packet)

Understanding the "Next Hop" is the key to debugging.

1. Local Traffic: Always routed internally within the VNet/VPC (default local route).
2. Internet Traffic:
    - _Public Subnet:_ Route `0.0.0.0/0` -> Internet Gateway.
    - _Private Subnet:_ Route `0.0.0.0/0` -> NAT Gateway.
3. Peered Traffic: Route `Target_CIDR` -> Peering Connection.
4. VPN/On-Prem: Route `OnPrem_CIDR` -> Virtual Private Gateway / VPN Gateway.
5. Traffic Hair-pinning (NAT Loopback): Internal clients accessing internal services via Public IP. The router translates Public IP -> Private IP and reflects traffic back to LAN.

## 4. Debugging Primitives

- Flow Logs: (VPC Flow Logs / NSG Flow Logs). The source of truth for "blocked vs allowed."
- Reachability Analyzer: (AWS Reachability Analyzer / Azure Network Watcher). Simulates a packet to find the configuration error (missing route, blocking NSG).
