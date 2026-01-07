---
confidence: high
epistemic: confirmed
purpose: "Track the refactoring of Helm charts to a Data-Centric Compiler pattern"
modified: 2026-01-07T10:17:07+00:00
last_reviewed: 2026-01-07
review_interval: weekly
see_also: 
  - "[[Pattern - Helm Chart as a Compiler]]"
source_of_truth: []
aliases:
  - "Project - FitFile Helm Refactor"
created: 2026-01-07T10:14:15+00:00
status: active
tags:
  - project
  - devops
  - helm
  - refactor
title: "Refactor: Helm Chart Compiler"
type: project
---

# Refactor: Helm Chart Compiler

> [!abstract] The "Why" (Top-Down Context)
> **Goal:** Eliminate "configuration drift" and "magic numbers" in multi-tenant deployments.
> **The Problem:** Current `ffnode` chart is a "Wrapper" that exposes raw vendor complexity (Bitnami/Argo) to the user. Adding a tenant requires 50+ lines of fragile YAML copy-paste.
> **The Solution:** A **Data-Centric "Compiler" Pattern**. Users declare *Intent* (`class: production-ha`), and the Chart *compiles* it into vendor-specific config.

---

## 1. Reentry Protocol (Ignition)

*How to pick up where you left off.*

**The Experiment:**
We are building a new 2-repo structure:
1. `fitfile-platform` (The Logic/Compiler)
2. `customer-experiment-1` (The State/Input)

**Verify Current State:**
To prove the compiler is working (turning "Intent" into "Config"), run this:

```sh
# 1. Enter the customer release dir
cd customer-experiment-1/release

# 2. Update dependencies (Links the local compiler chart)
helm dependency update

# 3. Compile the manifest
helm template test .
```

**Success Criteria:**
- Output should show `replicaCount: 3` (because `values.yaml` requests `production-ha`).
- Output should show `resources.requests.cpu: 500m` (Standard Profile auto-injected).

---

## 2. The Map (Roadmap)

### Phase 1: The Foundation (Core Logic)

*Goal: Prove we can compile a simple service (Mongo) from a high-level Class.*
- [x] **Mission 1:** Create Repo Structure (`fitfile-platform` vs `customer-repo`).
- [x] **Mission 2:** Define `_specs.yaml` (The Source of Truth).
- [x] **Mission 3:** Implement MongoDB Compiler (`_compiler.tpl`).
- [x] **Verification:** `helm template` outputs correct HA config.

### Phase 2: Feature Flags & Identity

*Goal: Support complex, conditional deployments (Hutch, PGWeb).*
- [ ] **Mission 4:** Implement **Feature Toggles**.
    - Add `features: { hutch: true }` to schema.
    - Write `fitfile.compile.hutch` logic to inject `COLLECTION_ID`.
- [ ] **Mission 5:** Implement **Identity/Ingress**.
    - Auto-generate Ingress rules based on `identity.domain`.
- [ ] **Mission 6:** Migration Test (`customer-nhs-trust-b`).
    - Prove we can deploy a second tenant with different features in isolation.

### Phase 3: The Shadow Deploy

*Goal: Validate against the running cluster without breaking it.*
- [ ] **Mission 7:** Generate "Legacy" manifest (`helm template ffnode`).
- [ ] **Mission 8:** Generate "New" manifest (`helm template fitfile-deploy`).
- [ ] **Mission 9:** Diff & Refine until "Physics" match (ignoring whitespace).

---

## 3. The Architecture

See: [[Pattern - Helm Chart as a Compiler]]

**Key Concepts:**
- **Product Type:** `Class` (SLA) + `Vendor` (Implementation).
- **Torvalds Loop:** Shape -> Data -> Logic.
- **Hardware Sympathy:** T-Shirt sized resource profiles (`micro`, `standard`) mapped to real node pools.

---

## 4. Current Context

- **Active Directory:** `fitfile-platform` and `customer-experiment-1` (created in root).
- **Status:** Core MongoDB compiler is working.
- **Next Action:** Implement the Hutch/Bunny compiler logic to support `features.hutch: true`.
