---
aliases: []
confidence:
created: 2025-10-31T10:36:00Z
criteria: Focus on packet transformations through each device.
epistemic:
exclusions: Physical network devices.
last_reviewed:
modified: 2025-10-31T10:42:03Z
purpose: Organize cloud networking devices by packet flow.
review_interval: 180
scope: Data-centric view of cloud networking devices.
see_also: []
source_of_truth: []
status:
tags:
  - cloud
  - networking
title: MOC - Cloud Networking Devices Data Flow
type: map
uid:
updated:
---

## MOC - Cloud Networking Devices Data Flow

This map organizes cloud networking devices by their role in processing and transforming packets.

### Core Approach
- [[Data-Centric Networking Focuses on Packet Journey Through Devices]] rel:: methodology

### Packet Journey Sequence
1. [[Cloud Firewalls Filter Traffic at Network and Transport Layers]] rel:: first-step
2. [[Load Balancers Distribute Traffic Across Backend Services]] rel:: distributes
3. [[API Gateways Manage and Secure Application Interfaces]] rel:: transforms
4. [[NAT Gateways Enable Private Resources to Access Internet]] rel:: enables
5. [[Web Application Firewalls Protect Against Layer 7 Attacks]] rel:: inspects

### Key Differentiators

| Device          | OSI Layer | Primary Function                  |
|-----------------|-----------|-----------------------------------|
| Firewall        | 3-4       | Filter by IP/port                 |
| Load Balancer   | 4-7       | Distribute traffic                |
| API Gateway     | 7         | Manage API interfaces             |
| WAF            | 7         | Block application-layer attacks   |
| NAT Gateway     | 3-4       | Enable outbound internet access   |

### Implementation Patterns
- Design security perimeters with firewall → WAF → API Gateway layers
- Use NAT for private subnets needing outbound access
- Combine load balancing with health checks for resilience

### Conceptual Diagrams
- [[Diagram - Philosophy-Productivity Connections]] (for system design principles)
