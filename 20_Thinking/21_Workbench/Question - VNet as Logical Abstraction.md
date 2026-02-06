---
created: 2026-02-06T09:05:00+00:00
modified: 2026-02-06T08:55:35+00:00
status: processing
tags: [domain/cloud, domain/networking, question]
title: Question - VNet as Logical Abstraction
type: question
---

## Question

In the context of cloud-native architecture, how should a Virtual Network (VNet) be defined as a logical abstraction rather than a physical construct, and what are its fundamental components before any compute resources are provisioned?

### Discovery & Answers

The VNet is a Policy Document, not a physical wire.

#### Key Concepts

1. The Logical Definition:
    - A VNet is essentially a JSON document stored in the cloud control plane database (e.g., Azure Resource Manager).
    - It acts as a "Zoning Contract" for the SDN controller, reserving IP space (`CIDR`) and defining isolation boundaries before any physical switches are touched.
    - _Source:_ [[SoT - Azure Resource Manager Architecture#3. The "VNet is a Document" Concept]]

2. Fundamental Components (Pre-Compute):
    - Address Space: The mathematical reservation of IP ranges (e.g., `10.0.0.0/16`).
    - Overlay ID (VNI/Tunnel ID): A unique identifier generated to tag encapsulated traffic (VXLAN/NVGRE), creating the "virtual wire."
    - System Routes: Implicit routing tables for local VNet traffic and Internet egress.
    - DNS Zone: An internal resolution boundary created immediately upon VNet instantiation.
    - _Source:_ [[SoT - Cloud Networking Core Components#1. Universal Concepts & Cloud Mapping]]

#### Related Frameworks

- Conservation of Complexity: The VNet abstraction shifts complexity from physical cabling (Data Center) to logical policy definition (Cloud API). See [[SoT - Conservation of Complexity#3. Case Study: Cloud Control Planes (AWS vs Azure)]].
