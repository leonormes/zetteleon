---
aliases: []
confidence: null
created: 2025-10-24T14:25:58Z
epistemic: null
last_reviewed: null
modified: 2025-12-25T11:40:46+00:00
purpose: null
review_interval: null
see_also: []
source_of_truth: []
status: null
tags:
  - moc
  - topic/technology/networking
title: Networking MOC
type: map
version: null
id: Networking MOC
---

This Map of Content (MOC) serves as the top-level entry point for all networking-related concepts, technologies, and implementations.

## Foundational Concepts

### Models & Units

- [[MOC - OSI Model]]
- [[SoT - Protocol Data Units (PDU)]]
- [[SoT - Encapsulation & De-encapsulation]]
- [[OSI Data Link Layer vs TCP/IP Link Layer]]
- [[Physical Layer]]

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

- [[SoT - The Data Architecture of DNS]]
- [[DNS is a distributed database]]
- [[DNS Resolvers Translate Domain Requests to IP Queries]]
- [[DNS Resource Records Are Structured Key-Value Pairs]]
- [[Private DNS Zones Provide Internal Network Name Resolution]]
- [[Split-Horizon DNS Decouples Service Names from Network Topology]]
- [[Host-Based Routing Enables Virtual Hosting in Cloud Infrastructure]]
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

- [[30_Library/100_zettelkasten/Containers Within a Pod Share Network Namespace
- and IP Address]]
- [[Kubernetes Performs SNAT for Pod Egress Traffic]]
- [[AWS ENIs Connect EKS Worker Nodes to VPC Networks]]
- [[Kubernetes Ingress Controllers Handle L7 Traffic]]
- [[Services]]
- [[Kubernetes-Native Abstractions for Traffic Control]]
- [[Sequence - Container to Internet Packet Flow in EKS]]

## Security

### Firewall Technology & Evolution

- [[Next-Generation Firewalls (NGFW) Provide Application-Aware Security]]
- [[Web Application Firewalls Protect Against Layer 7 Attacks]]
- [[Cloud Firewalls Filter Traffic at Network and Transport Layers]]

### Layer 3 Security

- [[Layer 3 Network Security Protects IP Routing and Forwarding]]
- [[Access Control Lists Filter Traffic Based on Protocol and Address Rules]]
- [[MOC - Layer 3 Network Security Concepts]]
- [[Mtri Trees Efficiently Store ACL and Routing Table Entries]]
- [[Bit Manipulation Optimizes Network Prefix Storage and Matching]]

---

**Related:** SRE MOC (if applicable)
