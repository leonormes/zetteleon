---
created: 2026-04-02T11:00:00+01:00
last-synthesis: 2026-04-02
modified: 2026-04-08T18:01:03+00:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: [architecture, kubernetes, secrets, type/SoT, vault, vso]
title: SoT - Vault Secrets Operator (VSO)
trust-level: stable
---

## Minimum Viable Understanding (MVU)

The Vault Secrets Operator (VSO) is a Kubernetes controller that synchronizes secrets from HashiCorp Vault into native Kubernetes `Secret` objects. It turns Vault into a declarative secret generator, allowing workloads to consume credentials without sidecars or Vault-specific SDKs. VSO brokers authentication using Kubernetes ServiceAccount identities, ensuring strict namespace isolation and least-privilege access.

## Working Knowledge

### 1. The 4-Layer Architecture

1. Vault (Source of Truth): Stores raw secrets and governs policies, dynamic generation, and rotation.
2. Kubernetes CRDs (Desired State): `VaultStaticSecret` and `VaultDynamicSecret` describe _what_ to sync and _how_ to authenticate.
3. Operator Loop (The Bridge): Continuously reconciles the CRDs by pulling from Vault and writing to K8s.
4. Kubernetes Secrets (Delivery Layer): Standard Opaque or `dockerconfigjson` secrets consumed by Pods via env vars or volume mounts.

### 2. The Authentication Chain (Identity Brokering)

VSO does not use a master token. It dynamically authenticates using Kubernetes Workload Identity:

- Identity Source: Kubernetes ServiceAccount JWT (projected token).
- Identity Verifier: Vault's `auth/kubernetes` backend (validates via TokenReview API).
- Result: A short-lived Vault token scoped to the specific namespace and policies.

### 3. Namespace Isolation & Security

- Local Resolution: By default, VSO resolves `VaultAuth` references within the _same_ Kubernetes namespace.
- Identity Scoping: Even if two namespaces use a `VaultAuth` named "default", they resolve to distinct principals (e.g., `system:serviceaccount:ns-a:default` vs `system:serviceaccount:ns-b:default`).
- Operator Brokerage: The operator pod is not a single identity; it assumes the identity of the `VaultAuth` in the target namespace, using the namespace-local ServiceAccount or AppRole to broker the connection.

---

## Current Understanding

### Operational Logic

- Operator Thinking: The cluster fetches secrets on behalf of Pods. Responsibility for rotation and lifecycle management shifts from the app to the platform.
- VSO vs. CSI/Agent: VSO is preferred for GitOps friendliness and standard app compatibility, while CSI is chosen for high-security environments where secrets must never touch the K8s API (etcd).

## Related Knowledge

- Automation: [[SoT - Vault Infrastructure Automation]] (`rel:: supports`)
- Operations: [[Protocol - VSO Secret Management & Troubleshooting]] (`rel:: procedure`)
- Theory: [[SoT - Infrastructure Complexity]] (`rel:: broader`)
