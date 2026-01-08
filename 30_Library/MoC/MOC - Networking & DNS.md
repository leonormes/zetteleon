---
aliases: ["DNS Index", "Networking Map"]
confidence: "5/5"
created: 2025-12-23T22:10:31Z
epistemic: "reference"
last_reviewed: "2025-12-23"
modified: 2026-01-08T10:49:46+00:00
purpose: "The central entry point for navigating networking, naming, and routing architectures."
review_interval: "6 months"
see_also: ["[[MOC - ProdOS]]"]
source_of_truth: []
status: "stable"
tags: ["index", "SoftwareEngineering/Architecture", "SoftwareEngineering/Networking", "SoftwareEngineering/networking/dns"]
title: MOC - Networking & DNS
type: "map"
uid: 
updated: 
---

## Networking & DNS - Map of Content

> [!hint] Overview
> This map organizes the foundational principles of hierarchical naming, the theory of data-centric networking, and the practical implementation of these concepts in cloud-native and Kubernetes environments.

---

### 1. Naming & Identity (The Hierarchy)

How resources are uniquely identified across networks.

- **[[SoT - The Data Architecture of DNS]]**—_The Domain Name System, FQDNs, and the Hostname vs. Service Name abstraction._
- **[[SoT - Digital Identity]]**—_The logical mapping of identity to network resources._

---

### 2. Data Mechanics (The Stack)

How information is structured and transformed as it moves through the network.

- **[[SoT - Protocol Data Units (PDU)]]**—_Layer-specific names (Segments, Packets, Frames) and the scope of responsibility._
- **[[SoT - The Data Anatomy of a URL]]**—_Deconstructing schemes, hostnames, paths, and queries._
- **[[SoT - Encapsulation & De-encapsulation]]**—_The Russian Doll mechanism and the SDU vs. PDU relationship._
- **[[SoT - Network Overhead & MTU]]**—_The mathematics of bandwidth loss, fragmentation, and MSS clamping._

---

### 3. Theory & Routing (The Logic)

The principles of how traffic is directed and service endpoints are abstracted.

- **[[SoT - The Data-Centric Theory of Networking]]**—_Indirection, stable endpoints, and Host-based vs. Path-based routing._
- **[[SoT - Cloud Networking Core Components]]**—_Gateways (IGW/NAT), Subnet routing, and Load Balancer (L4/L7) layers._

---

### 3. Cloud-Native Implementation (The Runtime)

Practical execution of networking within modern clusters.

- **[[SoT - Kubernetes Networking & DNS]]**—_CNIs, Service discovery, CoreDNS, and the Ingress-to-Pod traffic flow._
- **[[SoT - secure-cross-cloud-data-transport]]**—_Securing data movement between cloud providers (AWS <-> Azure)._

---

### 4. Troubleshooting & Tools

- **[[SoT - Git]]**—_Version control for infrastructure-as-code (Terraform)._
- **[[SoT - Data-Centric Infrastructure (Terraform)]]**—_Declarative management of network state._
