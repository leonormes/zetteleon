---
aliases: []
tags: []
title: Problem Definition
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-28T09:55:34+00:00
modified: 2025-12-28T09:56:35+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# Problem Definition

## 1. Context & Background

Modern Kubernetes deployments rely heavily on **Helm Charts** to package applications. In secure environments (enterprise, government, regulated industries), clusters cannot pull images directly from public registries (Docker Hub, Quay.io) due to:

- **Security Policies**: Prevention of supply chain attacks.
- **Rate Limiting**: Docker Hub pull limits.
- **Reliability**: Dependence on external availability.

Therefore, a **Private Container Registry (ACR)** is mandatory. All public charts must be "internalized": existing image references in `values.yaml` must be rewritten to point to the private registry.

## 2. The Core Problems

### 🔴 Problem A: The "Manual Synchronization" Toil

**Current State without Tool**:
1. Users manually find every image in a Chart (often scattered across `values.yaml`, `deployments`, `statefulsets`).
2. Users manually `docker pull`, `docker tag`, and `docker push` images to their private ACR.
3. Users manually edit `values.yaml` to update `repository` and `tag` fields.

**Impact**:
- **High Error Rate**: Typographical errors break deployments.
- **Staleness**: Private images drift from upstream versions.
- **Time Sink**: Hours wasted on trivial "plumbing" tasks.

### 🔴 Problem B: The "Architecture Mismatch" Risk

Most production clusters (e.g., AWS EKS) run on **linux/amd64** nodes.

However, many modern upstream images (especially from Mac M1/M2 developers) might default to `arm64` or specific multi-arch manifests that don't deploy correctly on strict amd64 node pools without explicit selection.

**Impact**:
- `exec format error` crashes in production.
- Silent failures where pods enter `CrashLoopBackOff`.

### 🔴 Problem C: "State Drift"

When teams manage chart overrides via ad-hoc `values-override.yaml` files, they often forget to apply them, or the overrides become incompatible with new chart versions.

**Impact**:
- Deployments work in "Dev" (where overrides happened to be applied) but fail in "Prod".

## 3. The Solution Strategy: "Stateless Batch Processor"

The **Chart Manager** solves these problems by inverting the workflow:

1. **Single Source of Truth**: A `config.yaml` ("Ledger") defines *what* the world should look like.
2. **Automated Internalization**: Machine-speed `pull -> tag -> push` pipeline.
3. **Direct Modification**: The tool effectively "patches" the local Helm chart in-place to use the private registry, removing the need for fragile override files.
4. **Gatekeeper Validation**: Enforces `amd64` architecture before a chart can even be effectively used.

### The Mental Model

> *"I define the charts I want. The machine ensures their images are in my registry and my local files point to them."*
