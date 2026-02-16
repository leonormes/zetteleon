---
aliases: [FitFile Secrets Guide, Secret Management SOP, Vault Secrets Operations]
created: 2026-02-01T15:30:00Z
modified: 2026-02-16T09:40:33+00:00
see_also: ["[[SoT - FitFile Deployment - Implementation Manual]]", "[[SoT - FITFILE Secret Management Architecture]]"]
status: evergreen
tags: [ff_deploy, secrets, security, sot, vault]
title: SoT - FitFile Secrets Operations (Vault & VSO)
type: SoT
updated: 2026-02-01
---

## 1. Overview

This document defines the Standard Operating Procedure (SOP) for creating, managing, and debugging secrets within the FITFILE platform. It operationalizes the architecture defined in [[SoT - FITFILE Secret Management Architecture]].

Core Principle: No secrets in Git. All secrets originate in HCP Vault and are synced to Kubernetes via the Vault Secrets Operator (VSO).

---

## 2. Vault Path Structure

| `…/cloudflare` | DNS/Ingress | `api_token` |

---

## 3. Cross-Namespace Mirroring (Reflector)

When a secret needs to be available in multiple namespaces (e.g., a wildcard TLS certificate or shared image pull secret), we use the Reflector operator.

### Mirroring Logic

1. Annotate Source: Add mirroring permissions to the source secret.

```yaml
reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "argocd,ohdsi,workflows"
```

1. Auto-Create: Reflector will automatically create and update the secret in target namespaces.

---

## 3. Creating New Secrets (The "Golden Path")

### Step 1: Generate Values

Use the CLI to generate strong random credentials (or use 1Password).

```bash
# Example: Generate 32-char alphanumeric password
openssl rand -base64 32
```

### Step 2: Write to Vault (HCP UI or CLI)

1. Navigate to `Secrets > deployments > {key} > secrets > application`.
2. Add the Key/Value pair (e.g., `new_api_key`).
3. Save as a new version.

### Step 3: Map in Helm (`values.yaml`)

Update the customer's `values.yaml` to instruct VSO to fetch this new key.

```yaml
extraVaultSecrets:
  - secretName: "my-new-secret"
    vaultPath: "application"  # Relative to deployment root
    templates:
      apiKey: '{{`{{get .Secrets "new_api_key"}}`}}'
```

### Step 4: Sync & Verify

1. Sync ArgoCD.
2. Verify the Kubernetes Secret exists:

```bash
   kubectl get secret my-new-secret -o jsonpath='{.data.apiKey}' | base64 -d
```

---

## 4. Policy & Access Control

Access is controlled via Vault Policies attached to AppRoles.

### 4.1 The "Deployment Reader" Policy

Every deployment has a dedicated read-only policy.

```hcl
# Policy: lca-prd-2-read
path "admin/data/deployments/lca-prd-2/*" {
  capabilities = ["read", "list"]
}
```

### 4.2 VSO Authentication

VSO uses the AppRole method.

- RoleID: Hardcoded in the VSO Helm release.
- SecretID: Injected into the cluster during Phase 3 via Terraform output.

---

## 5. Troubleshooting VSO

### 5.1 Secret Not Syncing (`VaultStaticSecret` Status `False`)

1. Check Events: `kubectl describe vss <secret-name>`
2. Common Errors:
   - `Permission Denied`: The AppRole policy does not allow reading the specific Vault path.
   - `Key Not Found`: The key name in `values.yaml` (`{{get.Secrets "foo"}}`) does not match Vault.

### 5.2 "Drift Detected" Loop

- Cause: Someone manually edited the Kubernetes Secret.
- Fix: VSO is designed to revert manual changes. Update the source in Vault, not Kubernetes.

### 5.3 Rotation

- Database Creds: Rotate in Vault -> Restart VSO -> Restart App Pods.
- TLS Certs: Managed automatically by Cert-Manager (not VSO).
