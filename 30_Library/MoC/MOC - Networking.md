---
aliases: []
created: 2025-10-24T14:25:58Z
id: Networking MOC
last_reviewed: 2026-02-06
modified: 2026-02-11T08:20:00+00:00
status: stable
tags: ["SoftwareEngineering/Networking", type/moc]
title: MOC - Networking
type: map
---

This Map of Content (MOC) serves as the top-level entry point for all networking-related concepts, technologies, and implementations.

## Foundational Concepts

### Models & Primitives

- [[SoT - Protocol Data Units (PDU)]]: The atomic units of data at each layer.
- [[SoT - Encapsulation & De-encapsulation]]: The process of wrapping data for transport.
- [[SoT - Linux Networking Primitives]]: How the kernel handles packets (Namespaces, veth pairs, bridges).
- [[MOC - Computer Science Foundations]]: Broader context including OSI/TCP-IP models.

### IP Addressing and Routing

- [[SoT - Scalable Private Networking & IPAM]]: Architectural patterns for indeterminate growth and non-overlapping connectivity.
- [[SoT - Cloud Networking Core Components]]: The fundamental building blocks (VNet/VPC, Subnets, Routing).
- [[SoT - Network Overhead & MTU]]: Physical constraints of packet size.

### DNS & Service Discovery

- [[SoT - The Data Architecture of DNS]]: The structural hierarchy of the Domain Name System.
- [[SoT - DNS Core Components and Environments]]: Resolvers, zones, and records.
- [[MOC - Networking & DNS]]: Index of DNS-specific concepts.

## Networking Methodologies

- [[SoT - The Data-Centric Theory of Networking]]: Networking as a data transformation pipeline.
- [[MOC - Cloud Networking Devices Data Flow]]: Visualizing the path of a packet.
- [[SoT - Network Debugging Tools & Patterns]]: Practical diagnosis (tcpdump, wireshark).

## Cloud Networking

### General Cloud

- [[MOC - Cloud Networking]]: General cloud networking concepts.
- [[SoT - Cloud Networking Core Components]]: Universal abstractions (VPC/VNet).
- [[SoT - Secure Cross-Cloud Data Transport]]: VPNs, Peering, and Interconnects.

### AWS

- [[AWS Networking MOC]]: AWS-specific implementations.
- [[SoT - AWS EKS Networking Architecture]]: VPC CNI and pod networking.

### Azure

- [[SoT - Azure Hybrid Networking (ExpressRoute)]]: Connectivity to on-premise.
- [[SoT - Azure Resource Manager Architecture]]: How VNets exist as logical resources.
- [[Cheatsheet - Azure AKS Networking]]: Quick reference for AKS IPs.

## Kubernetes Networking

- [[SoT - Kubernetes Networking Model]]: The "Flat Network" requirement.
- [[SoT - Kubernetes Networking & DNS]]: Services, Ingress, and CoreDNS.
- [[SoT - Calico CNI Architecture]]: Network policies and overlay networks.
- [[SoT - Calico Observability]]: Monitoring in-cluster traffic.
- [[Kubernetes Provides NodePort and LoadBalancer for External Service Access]].

## Traffic Management (Load Balancing)

- [[MOC - Load Balancing]]: Index of load balancing strategies.
- [[MOC - AWS ALB Step-by-Step Tutorial]]: Implementation details.
- [[SoT - External Ingress & SSL Architecture]]: Handling TLS termination at the edge.

## Security

### Firewalls & Filtering

- [[SoT - External Ingress & SSL Architecture]]: WAF and Edge security.
- [[SoT - Zero Knowledge Architecture]]: Networking implications of Zero Trust.

### Layer 3/4 Security

- [[MOC - Layer 3 Network Security Concepts]].
- [[Access Control Lists Filter Traffic Based on Protocol and Address Rules]].

---

Related: [[MOC - ProdOS]], [[MOC - Software Architecture Principles]]
