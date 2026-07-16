---
aliases: [Data-Oriented IaC, DevOps Philosophy, FitFile Infrastructure Model, Infrastructure Strategy]
created: 2026-01-02T23:30:00+00:00
modified: 2026-07-13T08:52:46+00:00
permalink: llmeon/30-library/so-t/so-t-dev-ops-infrastructure-architecture-strategy
tags: [devops, fitfile, iac, SoftwareEngineering/Architecture, strategy]
title: SoT - DevOps & Infrastructure Architecture Strategy
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 1. The Core Tension: Complexity vs. Cognition

Current DevOps practices often fail because they exceed human cognitive limits. We build intricate, brittle systems (ArgoCD chains, Helm dependencies) that are impossible to hold in working memory.

- The Trap: "Satisficing" (doing just enough to make it work) leads to sub-optimal legacy code that resists change.
- The Reality: A distributed system is a complex graph of state, but we try to manage it with linear scripts (IaC).

## 2. The Strategic Pivot: Data-Oriented Infrastructure

We must shift from Imperative Scripting (telling the cloud what to do) to Data-Oriented Modeling (defining what the cloud _is_).

### 2.1 The Network as Data

Instead of disjointed config files, view the network as a rigorous data model:

- Resources: A set of IP addresses (Identity).
- Reachability: A map of allowed connections (Public vs. Private).
- Constraint: Private IPs have restricted reachability. This should be a Type Constraint, not just a firewall rule.

### 2.2 Unifying Identity

Identity concepts are currently scattered across boundaries (Hostname in DNS, Certificate in Vault/Store).

- The Goal: Represent the dependency `Hostname <-> Certificate <-> IP` as a single logical unit.
- The Enforcement: Make broken configurations (e.g., a Certificate without a matching DNS record) uncodable at the schema level.

## 3. Operational Reality: The Human & Systemic Factor

### 3.1 The Inherent Complexity of Distributed Systems

Cloud-native systems are rarely "up" or "down"; they exist in a state of partial degradation.

- Transient Faults: Strategies must account for the fact that _nothing is ever completely right aboard a ship_. Retry logic and circuit breakers are mandatory, not optional.
- Misconfigurations: The primary attack vector is not zero-day exploits but simple misconfigurations (e.g., running containers as root, exposing secrets in env vars).

### 3.2 DevOps as an Organizational Challenge

DevOps is not a role but a collaborative standard.

- Blurring Lines: The distinction between "Dev" and "Ops" is artificial. _It is all just software now._
- Shift-Left Security: Vulnerabilities must be caught in the CI/CD pipeline (image scanning, static analysis) because fixing them in production is exponentially more expensive.

### 3.3 Managed Services (AKS/EKS) vs. Self-Hosted

- The Trade-off: Managed services abstract the control plane (Master nodes) but introduce a "Shared Responsibility Model." You still own the workload security.
- Decision: Default to Managed Services to minimize operational toil, unless specific kernel-level control is required.

## 4. FitFile Deployment Context

- Environment: Managed K8s (Cloud), Private Networking.
- Release Strategy: Unique tags per environment/customer (Multi-tenant).
- Shared Responsibility: We must define clear boundaries where our automation ends and the platform begins.

> Next Action: Build a "Data-First" object model of the deployment to expose these hidden dependencies.

- [[SoT - Accelerate & DORA]]
