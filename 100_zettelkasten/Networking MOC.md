---
aliases: []
confidence:
created: 2025-10-24T14:25:58Z
epistemic:
last_reviewed:
modified: 2025-10-31T09:31:38Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [moc, topic/technology/networking]
title: Networking MOC
type: map
uid:
updated:
version:
---

This Map of Content (MOC) serves as the top-level entry point for all networking-related concepts, technologies, and implementations.

## Foundational Concepts

### OSI Model
- [[osi_layers]]
- [[Physical Layer]]
- [[Layer 1 Physical Layer]]
- [[Layer 3 Network Layer]]
- [[Layer 4 Transport Layer]]
- [[Layer 7 Application Layer]]
- [[Protocol Data Unit]]
- [[An Example of a Tcp Packet With All Layers]]

### IP Addressing and Routing
- IP Addressing and CIDR
- [[Routing Tables Use Longest Prefix Match for Forwarding Decisions]]

### Network Address Translation
- [[NAT Gateways Enable Private Resources to Access Internet]]
- [[Kubernetes Performs SNAT for Pod Egress Traffic]]

### Load Balancing
- [[Load Balancing MOC]]
- [[A Load Balancer Distributes Traffic for Reliability and Scale]]
- [[Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers]]
- [[Load Balancers Distribute Traffic Across Backend Services]]
- High Availability Concepts

### DNS
- [[DNS is a distributed database]]
- [[DNS Resolvers Translate Domain Requests to IP Queries]]
- [[DNS Resource Records Are Structured Key-Value Pairs]]
- [[DNS Protocol Uses UDP and TCP for Message Transport]]
- [[DNS Delegation Handles Subdomain Authority Transfers]]
- [[MX Records Route Email to Designated Mail Servers]]
- [[Glue Records Solve DNS Chicken-and-Egg Problems]]
- [[DNS Resolver Search Lists Complete Unqualified Domain Names]]
- [[Private DNS Zones Provide Internal Network Name Resolution]]
- [[Private vs Public DNS Resolution Patterns]]
- [[Hybrid Cloud DNS Resolution Flow]]

## Networking Methodologies

- [[Data-Centric Networking Focuses on Packet Journey Through Devices]]
- [[MOC - Cloud Networking Devices Data Flow]]

## Cloud Networking

- [[Cloud Networking MOC]]
- [[AWS Networking MOC]]
- (To be added later, e.g., Azure Networking, GCP Networking)

## Kubernetes Networking

- [[100_zettelkasten/Containers Within a Pod Share Network Namespace and IP Address]]
- [[Kubernetes Performs SNAT for Pod Egress Traffic]]
- [[AWS ENIs Connect EKS Worker Nodes to VPC Networks]]
- [[Kubernetes Ingress Controllers Handle L7 Traffic]]
- [[Services]]
- [[Kubernetes-Native Abstractions for Traffic Control]]
- [[Sequence - Container to Internet Packet Flow in EKS]]

## Security

### Layer 3 Security
- [[Layer 3 Network Security Protects IP Routing and Forwarding]]
- [[Access Control Lists Filter Traffic Based on Protocol and Address Rules]]
- [[MOC - Layer 3 Network Security Concepts]]
- [[Mtri Trees Efficiently Store ACL and Routing Table Entries]]
- [[Bit Manipulation Optimizes Network Prefix Storage and Matching]]

### Cloud Security
- [[Cloud Firewalls Filter Traffic at Network and Transport Layers]]
- AWS Security Groups
- [[Web Application Firewalls Protect Against Layer 7 Attacks]]

---

**Related:** SRE MOC (if applicable)
