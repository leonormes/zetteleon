---
aliases: [FitFile Security Index, Secret Management Map]
created: 2026-01-08T12:45:00Z
epistemic: index
last_reviewed: 2026-01-08
modified: 2026-01-11T18:59:23+00:00
purpose: "To serve as the central navigation hub for FITFILE's security architecture, secret management, and hardening protocols."
status: active
tags: [fitfile, moc, secrets, security]
title: 1. Core Architecture
type: map
---

# 1. Core Architecture

- **Secret Management:** [[SoT - FITFILE Secret Management Architecture]]
    - Defines the VSO implementation, "Canonical" vs. "Legacy" paths, and the "Golden Config" for rotation.
- **General K8s Secrets:** [[SoT - Kubernetes Secrets Management]]
    - Covers the underlying concepts (Etcd encryption, External Secrets pattern).

# 2. Operational Procedures

- **Rotation & Troubleshooting:** [[SoT - FitFile Deployment - Operations & Troubleshooting]]
    - See Section 1.3 for the **Rotation Policy**.
    - See Section 2.1 for **Stale Secret** debugging.
- **Audit Reports:**
    - [[Audit - FITFILE Secret Management (Oct 2025)]] (Historical context for current architecture).

# 3. Hardening Standards

- **Container Security:** [[SoT - Container Security & Hardening]]
    - Best practices for image building (Distroless), runtime security (PSA), and supply chain.
- **Infrastructure:** [[SoT - DevOps & Infrastructure Architecture Strategy]]
    - Philosophy on "Shift-Left" security and immutable infrastructure.
