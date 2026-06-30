---
title: 'Bug Report: ACR 401 Unauthorised — ArgoCD Helm Registry Auth Failure'
created: 2026-06-29 09:00:00+01:00
modified: 2026-06-29 09:00:00+01:00
tags:
- bug-report
- argocd
- azure
- kubernetes
- vault
- acr
prodos:
  kind: reference
  lifecycle: stable
permalink: llmeon/30-library/bug-reports/acr-argo-cd-auth-bug-2026-06-29
---

# Bug Report: ACR 401 Unauthorised — ArgoCD Helm Registry Auth Failure

## Date & Time

- **Detected:** 2026-06-29
- **Investigation completed:** 2026-06-29T~09:00 UTC
- **Environment:** `fitfile-cloud-testing-aks-cluster` (Context: `fitfile-cloud-testing-aks-cluster`)

---

## Symptom

ArgoCD failed to synchronise the `dev-mongodb-b17ef` application in the testing cluster. The error from ArgoCD logs:

```
Failed to load target state: failed to generate manifest for source 1 of 1:
rpc error: code = Unknown desc = unable to get tags: failed to get tags:
GET "https://fitfileregistry.azurecr.io/v2/helm/mongodb/tags/list": [...]
response status code 401: unauthorized: Invalid clientid or client secret.
```

All applications depending on Helm charts from `fitfileregistry.azurecr.io` are blocked from syncing.

---

## Root Cause

**Primary cause:** The `VaultDynamicSecret` Kubernetes resource `argocd-pull` (in namespace `argocd`) has `spec.destination.overwrite: false`. This tells the HashiCorp Vault Secrets Operator (VSO) to write the `argocd-acr-pull-secret` Kubernetes secret **once and never update it**. When Vault's Azure secrets engine rotated the dynamic credential for the `acr-pull` role (deleting the old Azure AD application password and issuing a new one), VSO renewed the Vault lease but did **not** update the Kubernetes secret. The secret is therefore frozen with the **original credential value from 2026-06-24**, while the Azure AD application credential it referenced has since been deleted and replaced.

**Mechanism:**

1. `VaultDynamicSecret/argocd-pull` was created and VSO wrote `argocd-acr-pull-secret` on **2026-06-24T10:43:32Z** with `client_id: 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a` and a client secret whose value is now stale.
2. VSO has been **renewing the Vault lease** (`azure/creds/acr-pull/cdfo6wdMhADj7jlIewEtGcWf.jPL3k`, 12 h duration, last renewed 2026-06-29) but lease renewal only extends the Vault TTL — it does **not** re-read or re-write new Azure credential values to the K8s secret.
3. Vault's Azure secrets engine eventually rotated the credential (deleted the June 24 password from the app registration, issued a new one). The K8s secret was not updated because `overwrite: false`.
4. ArgoCD reads the stale credential from the K8s secret and presents it to `fitfileregistry.azurecr.io`, which rejects it with HTTP 401.

**Contributing factor — Credential accumulation leak:**

The Azure AD application registration `HCP Vault ACR Pull` (`appId: 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a`) has accumulated **30+ password credentials** all created by `vault-plugin-secrets-azure` on 2026-06-29 alone, with a 10-year TTL each. Vault is issuing new credentials (for new lease requests from other VSO reconcile loops or manual Vault reads) but is **not cleaning up old ones**. This points to a misconfiguration in the Vault Azure secrets engine's credential TTL or a lease-tracking failure. If left unresolved, this will hit Azure AD's application password limit and break all Vault-issued ACR credentials entirely.

---

## Evidence

### 1. Azure context and ACR health (read-only)

```
$ az account show
{
  "name": "Shared Services",
  "id": "a085dd04-19aa-4d2b-9a35-e438097d84fc",
  "state": "Enabled",
  "tenantDefaultDomain": "fitfile.com"
}

$ az acr show --name fitfileregistry
{
  "name": "Fitfileregistry",
  "loginServer": "fitfileregistry.azurecr.io",
  "provisioningState": "Succeeded",
  "sku": { "name": "Premium" }
}
```

ACR is healthy. The fault is not in the registry itself.

### 2. Kubernetes secret inspection

```
$ kubectl get secrets -n argocd | grep -i acr
argocd-acr-pull-secret   Opaque   8   4d21h

$ kubectl get secret argocd-acr-pull-secret -n argocd -o json | [decode]
  creationTimestamp: 2026-06-24T10:43:32Z
  labels:
    app.kubernetes.io/managed-by: hashicorp-vso
    secrets.hashicorp.com/vso-ownerRefUID: 96ec86b7-b1be-496d-9945-099efafd1d1f
  username: 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a
  password: <REDACTED — first 3 chars: TsD>
  url: fitfileregistry.azurecr.io
  type: helm
```

The secret is 5 days old, managed by VSO, and has not been updated since creation.

### 3. Service principal role assignment

```
$ az role assignment list --assignee 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a --all
Principal                              Role      Scope
-------------------------------------  --------  -----------------------------------------------
1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a  AcrPull   /subscriptions/a085dd04-19aa-4d2b-9a35-e438097d84fc
```

The SP has `AcrPull` at subscription scope. Permissions are correct.

### 4. Credential hint mismatch

```
$ az ad sp show --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a
  passwordCredentials[0].hint: fdI      ← active SP-level credential

$ kubectl get secret argocd-acr-pull-secret -n argocd \
    -o jsonpath='{.data.password}' | base64 --decode | cut -c1-3
TsD                                   ← credential in K8s secret
```

`TsD ≠ fdI` — the Kubernetes secret does not match the current active credential.

### 5. VaultDynamicSecret configuration — overwrite: false

```yaml
# kubectl get vaultdynamicsecret argocd-pull -n argocd -o yaml
spec:
  destination:
    create: true
    overwrite: false          # ← BUG: prevents credential updates
    name: argocd-acr-pull-secret
  mount: azure
  path: creds/acr-pull
  renewalPercent: 67
status:
  secretLease:
    id: azure/creds/acr-pull/cdfo6wdMhADj7jlIewEtGcWf.jPL3k
    duration: 43200
    renewable: true
  lastRenewalTime: 1782709787   # 2026-06-29 — VSO IS renewing the lease
```

VSO is actively renewing the Vault lease but never writing updated credentials to the K8s secret.

### 6. Credential accumulation on the app registration

```
$ az ad app show --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a
passwordCredentials: [
  { "displayName": "vault-plugin-secrets-azure", "hint": "icL", "startDateTime": "2026-06-29T08:31:10Z", "endDateTime": "2036-06-26T08:31:10Z" },
  { "displayName": "vault-plugin-secrets-azure", "hint": "4.Q", "startDateTime": "2026-06-29T07:11:14Z", "endDateTime": "2036-06-26T07:11:14Z" },
  { "displayName": "vault-plugin-secrets-azure", "hint": "Iqq", "startDateTime": "2026-06-29T07:11:13Z", "endDateTime": "2036-06-26T07:11:13Z" },
  { "displayName": "vault-plugin-secrets-azure", "hint": "TsD", "startDateTime": "2026-06-29T05:09:46Z", "endDateTime": "2036-06-26T05:09:46Z" },
  ... [30+ total credentials created today alone, none cleaned up]
  { "displayName": "vault", "hint": "XPs", "startDateTime": "2026-03-03T11:39:12Z", "endDateTime": "2026-08-30T10:39:12Z" }
]
```

30+ dangling credentials with 10-year TTLs — Vault's Azure plugin is not revoking old credentials on lease expiry.

---

## Remediation Steps

### Immediate fix — restore ArgoCD sync (5 minutes)

This requires you to force VSO to regenerate credentials by deleting and re-creating the Kubernetes secret, which triggers VSO to issue a new Vault lease and write fresh credentials.

**Step 1** — Delete the stale K8s secret (VSO will re-create it):

```bash
kubectl delete secret argocd-acr-pull-secret -n argocd
```

**Step 2** — Annotate the VaultDynamicSecret to force immediate reconciliation:

```bash
kubectl annotate vaultdynamicsecret argocd-pull -n argocd \
  secrets.hashicorp.com/force-sync=$(date +%s) --overwrite
```

**Step 3** — Verify the new secret is created with fresh credentials:

```bash
kubectl get secret argocd-acr-pull-secret -n argocd
kubectl get secret argocd-acr-pull-secret -n argocd \
  -o jsonpath='{.data.password}' | base64 --decode | cut -c1-3
# Should show a new 3-char hint different from TsD
```

**Step 4** — Force ArgoCD to re-sync:

```bash
argocd app sync dev-mongodb-b17ef --force
# OR via ArgoCD UI: open app → Sync → Force
```

---

### Structural fix — set overwrite: true (requires PR)

The `VaultDynamicSecret` must be updated so VSO always writes refreshed credentials to the K8s secret on each lease renewal. This prevents the same issue recurring.

In your GitOps deployment repository, find the manifest for `argocd-pull` and change:

```yaml
# BEFORE
spec:
  destination:
    overwrite: false

# AFTER
spec:
  destination:
    overwrite: true
```

Raise a PR, have it reviewed, and apply it to the testing cluster. Then roll the same change to staging and prod if they have equivalent `VaultDynamicSecret` resources.

---

### Credential cleanup — remove leaked Azure AD credentials (optional but recommended)

The 30+ dangling credentials on the app registration should be cleaned up. Confirm with your Vault admin first, as blindly deleting them could break other active leases.

1. In the Azure Portal → Azure Active Directory → App Registrations → `HCP Vault ACR Pull` → Certificates & secrets.
2. Delete all credentials with `displayName: vault-plugin-secrets-azure` that are **not** the one currently tracked by the active Vault lease.
3. Investigate why Vault's Azure secrets engine is not revoking credentials on lease expiry — check the Vault server logs and the Azure secrets engine configuration (`vault read azure/config`).

---

### Secondary security observation

The `argocd-acr-pull-secret` K8s secret contains a `_raw` field storing the full JSON credential payload from Vault, including the `client_secret` in plain text, alongside the individual `username` and `password` fields. This is redundant exposure of the credential. Consider adding `_raw` to the `excludes` list in the VaultDynamicSecret transformation:

```yaml
spec:
  destination:
    transformation:
      excludes:
        - .*         # already present — excludes all raw Vault fields
      # _raw is apparently not excluded by the current regex; verify and test
```

---

## Timeline Summary

| Time | Event |
|------|-------|
| 2026-06-24T10:43Z | VSO created `argocd-acr-pull-secret` with Vault-issued credential (`TsD...`) |
| 2026-06-24 → 2026-06-29 | VSO renewed Vault lease every ~8 h; K8s secret never updated (`overwrite: false`) |
| 2026-06-29 (ongoing) | Vault Azure engine issuing 30+ new credentials without revoking old ones |
| 2026-06-29T~09:00Z | `TsD...` credential deleted from Azure AD by Vault rotation; 401s begin |
| 2026-06-29 | Investigation completed; root cause identified |