---
created: 2026-02-05T10:40:21+00:00
modified: 2026-02-05T10:41:46+00:00
title: 2026-02-05-Debugging-HIE-NNUH
---

## Debugging HIE -> NNUH Networking

### Context

- Workstream: Node Installation NNUH (FTFL-82).
- Specific Task: Configure Inbound Routes (FTFL-88).
- Architecture: Connection required between Central HIE (Reference: `hie-prod-34`) and NNUH Node.
- Status: Currently in "To Do" / "In Progress".

### The Problem

Connectivity between the HIE infrastructure and the NNUH deployment needs verification and potential debugging.

### Investigation Plan (The "Next Test")

#### 1. Verification of HIE Egress

- Check `hie-prod-34` (or relevant HIE cluster) egress capability.
- Reference: [[Protocol - Kubernetes Network Debugging#1. Source Side: Verify Egress (From Netshoot)]]

#### 2. NNUH Ingress & Routing

- Verify Inbound Routes at NNUH.
- Reference: [[SoT - Network Debugging Tools & Patterns#2. Layer 3: Reachability & Routing (The Roads)]]

### Related Resources

- [[SoT - FITFILE Secret Management Architecture]] (Context on HIE `extraDeploy` patterns).
- [[Protocol - Kubernetes Network Debugging]]
- [[SoT - Network Debugging - Cross-Cloud & Hybrid]]

### Related Knowledge (Synthesized)

- [[30_Library/200_projects/20_Development/Debug Wiki/troubleshooting_guide.md|Private Deployment Troubleshooting Guide]]: Contains specific steps for "Clusters Unable to Communicate Across Clouds" (ExpressRoute/DirectConnect).
- [[2026-02-03]]: Daily Log context for FTFL-82 & FTFL-88.
- [[Protocol - Kubernetes Network Debugging]]: General Step-by-Step for pod-to-pod and ingress issues.
