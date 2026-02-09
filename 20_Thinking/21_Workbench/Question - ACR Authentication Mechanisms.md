---
created: 2026-02-06T10:35:00+00:00
modified: 2026-02-06T20:54:09+00:00
status: processing
tags: [domain/cloud, domain/security, fitfile, question]
title: Question - ACR Authentication Mechanisms
type: question
---

## Question

question:: How do our azure clusters authenticate with acr in order to pull images?

### Discovery & Answers

The authentication mechanism is context-dependent, relying on two distinct patterns based on the cluster's location and tenancy.

#### 1. Node-Level Authentication (Managed Identity)

_Used by: Production, Staging (Internal Clusters)_

In native Azure environments (AKS), the authentication is transparently handled by the underlying infrastructure.

- Mechanism: The Virtual Machine Scale Sets (VMSS) backing the Kubernetes nodes are assigned a User Assigned Managed Identity.
- Role: This identity holds the `AcrPull` role on the `fitfileregistry`.
- Flow: The Kubelet uses this identity to pull images without any explicit secrets in the Pod definition.
- Source: [[acr_authentication_wiki#1. AKS Managed Identity (Node-Level Authentication)]]

#### 2. Explicit Secret Injection (Vault Dynamic Secret)

_Used by: Customer Clusters (LCA), Testing, Debugging_

For environments outside our primary tenant or where node identity is insufficient (e.g., current `testing` cluster limitations), we inject specific credentials.

- Mechanism: Vault Secrets Operator (VSO) synchronizes a `VaultDynamicSecret` from HashiCorp Vault.
- Credential: This generates a short-lived password for the `HCP Vault ACR Pull` Service Principal.
- Artifact: Results in a Kubernetes Secret named `fitfile-image-pull-secret` (type: `kubernetes.io/dockerconfigjson`).
- Flow: Pods must explicitly reference this in their `imagePullSecrets`.
- Source: [[SoT - FITFILE Secret Management Architecture#2.1 Dynamic Infrastructure Secrets (ACR)]] and [[acr_authentication_wiki#2. Explicit Image Pull Secret (`fitfile-image-pull-secret`)]]

#### Environment Matrix

| Environment | Method | Identity |
|:--- |:--- |:--- |
| Prod/Stg | Managed Identity | Node Identity |
| Testing | Explicit Secret | `fitfile-image-pull-secret` |
| Customer | Explicit Secret | `fitfile-image-pull-secret` |
