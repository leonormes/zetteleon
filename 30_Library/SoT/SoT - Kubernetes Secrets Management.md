---
aliases: [K8s Secrets, Kubernetes Security, Secret Management]
confidence: 5/5
created: 2025-12-16T14:05:00Z
epistemic: technical
last_reviewed: 2025-12-16
modified: 2025-12-16T13:53:11Z
purpose: To define the technical implementation, security risks, and management patterns for Kubernetes Secrets.
related-soTs: ["[[SoT - FITFILE Secret Management Architecture]]", "[[SoT - Kubernetes Cluster State Architecture]]"]
review_interval: 1 year
see_also: ["[[Kubernetes Secrets in Helm Chart Deployment]]", "[[Vault to Kubernetes Secrets Management Guide]]"]
source_of_truth: true
status: stable
tags: [devops, kubernetes, secrets, security, vault]
title: SoT - Kubernetes Secrets Management
type: SoT
uid: 2025-12-16-K8S-SECRETS
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> A **Kubernetes Secret** is a standard API object (`v1/Secret`) designed to decouple sensitive data from Pod configuration.
>
> Crucially, **Base64 Encoding is NOT Encryption.** A standard Secret is essentially a ConfigMap with obfuscation. Security relies entirely on **RBAC** (Who can read it?) and **Encryption at Rest** (How it is stored in Etcd).

---

## 2. Core Data Structure

### The Object

```yaml
apiVersion: v1
kind: Secret
type: Opaque
data:
  # Base64 encoded values
  username: YWRtaW4=
  password: cGFzc3dvcmQ=
```

### Consumption Models

1. **Volume Mount (Recommended):**
    - Secrets appear as files in `/etc/secrets/`.
    - **Updates:** Automatic (eventual consistency). Kubelet syncs changes.
    - **Security:** Data lives in `tmpfs` (RAM), never written to disk.
2. **Environment Variable:**
    - Injected at startup: `valueFrom: secretKeyRef`.
    - **Updates:** **None.** Requires Pod restart.
    - **Risk:** Leaked in crash dumps and `ps` output.

---

## 3. Storage & Encryption

### The Default Risk

By default, Kubernetes stores secrets as **plaintext** Protobuf in Etcd. Anyone with access to Etcd files or API `list secrets` permission can read all passwords.

### The Fix: Envelope Encryption

To secure this, the API Server must be configured with an **EncryptionConfiguration**.

1. **DEK (Data Encryption Key):** Encrypts the payload.
2. **KEK (Key Encryption Key):** Encrypts the DEK. Stored in an external KMS (Vault/AWS KMS).

---

## 4. Management Patterns (GitOps)

Since you cannot commit secrets to Git:

| Pattern | Mechanism | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Sealed Secrets** | Asymmetric Encryption. Commit encrypted CRD (`SealedSecret`) to Git. Controller decrypts. | Simple, Git-native. | Key rotation is hard. |
| **External Secrets** | Controller polls external Vault (AWS/HashiCorp) and syncs to K8s Secret. | Centralized, secure. | High complexity. |
| **Vault Secrets Operator (VSO)** | **FITFILE Standard.** Connects directly to HashiCorp Vault. | Enterprise-grade, Dynamic Secrets. | Heavy dependencies. |

*See [[SoT - FITFILE Secret Management Architecture]] for our specific VSO implementation.*

---

## 5. Security Hardening

1. **Immutable Secrets:** Set `immutable: true` to prevent accidental overwrites and improve performance (no API watching).
2. **RBAC Least Privilege:** Never grant `list` on Secrets cluster-wide.
3. **AutomountServiceAccountToken:** Set to `false` for Pods that don't need API access to prevent credential leakage.
