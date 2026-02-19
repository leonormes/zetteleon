# Playbook: ArgoCD OCI Registry Authentication Failure with VSO Dynamic Secrets

> **When to use this:** ArgoCD applications show `Unknown` sync status with a `ComparisonError` mentioning `helm registry login` failures, `401 unauthorized`, or `Invalid clientid or client secret` against an OCI Helm registry — and your registry credentials are managed by HashiCorp Vault Secrets Operator (VSO) dynamic secrets.

---

## Symptoms

- ArgoCD Application sync status: `Unknown`
- ArgoCD Application health status: `Healthy` (previously deployed resources still running)
- Condition type: `ComparisonError`
- Error message contains:

```
failed to login to registry <REGISTRY>/helm: ... response status code 401: unauthorized: Invalid clientid or client secret
```

---

## Understanding the Architecture

Before debugging, it is critical to understand that there are **two separate credential paths** for an OCI container registry in a Kubernetes + ArgoCD + VSO setup:

| Credential Path | Consumer | Used For | K8s Secret Type |
|---|---|---|---|
| Image Pull Secret | kubelet | Pulling container images at pod scheduling time | `kubernetes.io/dockerconfigjson` |
| ArgoCD Repository Secret | ArgoCD repo-server | `helm registry login` to fetch OCI Helm charts | `Opaque` with ArgoCD labels |

Both may be sourced from the **same Vault dynamic secrets engine** (e.g. `azure/creds/acr-pull`) but are written to **different K8s Secrets** by **different VaultDynamicSecret CRs**. Fixing one does not fix the other.

Additionally, ArgoCD has **two types** of repository credential secrets, with a priority order:

| Type | Label | Behaviour |
|---|---|---|
| `repo-creds` | `argocd.argoproj.io/secret-type: repo-creds` | **URL template** — matches any repo starting with the URL. Takes priority. |
| `repository` | `argocd.argoproj.io/secret-type: repository` | Exact match for a specific repo URL. |

If both exist for the same URL, `repo-creds` wins. A stale `repo-creds` secret will silently override a valid `repository` secret.

---

## Phase 1: Confirm the Error

### 1.1 List ArgoCD Applications and Identify Failures

```bash
kubectl get applications -n argocd
```

Look for `Unknown` sync status or `Degraded` health status.

### 1.2 Get the Error Message

```bash
kubectl get application <APP_NAME> -n argocd -o yaml | grep -A 20 "conditions:"
```

### 1.3 Get the Operation State Detail

```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{.status.operationState.message}'
```

### 1.4 Confirm the Helm Source and Registry

```bash
kubectl get application <APP_NAME> -n argocd -o jsonpath='{.spec.source}' | jq .
```

Confirm the application pulls from an OCI registry (look for `repoURL` pointing at your registry, or Helm chart dependencies that reference it).

---

## Phase 2: Identify All Secrets Involved

### 2.1 Find ArgoCD Repository Secrets for the Registry

```bash
kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repository -o json | \
  jq '.items[] | select(.data.url) | {name: .metadata.name, url: (.data.url | @base64d)}'
```

### 2.2 Find ArgoCD Repo-Creds (Template) Secrets

```bash
kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repo-creds -o json | \
  jq '.items[] | select(.data.url) | {name: .metadata.name, url: (.data.url | @base64d)}'
```

### 2.3 Find Image Pull Secrets for the Registry

```bash
kubectl get secrets -n argocd --field-selector type=kubernetes.io/dockerconfigjson -o json | \
  jq '.items[] | {name: .metadata.name, registry: (.data[".dockerconfigjson"] | @base64d | fromjson | .auths | keys[])}'
```

### 2.4 Build the Inventory

For **every secret** targeting your registry, capture:

```bash
# Check if VSO-managed
kubectl get secret <SECRET_NAME> -n argocd -o jsonpath='{.metadata.ownerReferences}' | jq .

# Check labels
kubectl get secret <SECRET_NAME> -n argocd -o jsonpath='{.metadata.labels}' | jq .

# Check creation time
kubectl get secret <SECRET_NAME> -n argocd -o jsonpath='{.metadata.creationTimestamp}'
```

Build a table like:

| Secret | ArgoCD Type | VSO-Managed? | Owning VDS |
|---|---|---|---|
| `argocd-acr-pull-secret` | `repository` | ✅ | `argocd-pull` |
| `argocd-acr-repo-creds` | `repo-creds` | ❌ manual | — |
| `fitfile-image-pull-secret` | (image pull) | ✅ | `fitfile-image-pull` |

---

## Phase 3: Compare Credentials Across Secrets

### 3.1 Get the Username and Password from Each ArgoCD Repo Secret

```bash
# For each ArgoCD repo secret
kubectl get secret <SECRET_NAME> -n argocd -o json | \
  jq '{name: .metadata.name, username: (.data.username | @base64d), password: (.data.password | @base64d)}'
```

### 3.2 Get the Current Valid Credentials from the Image Pull Secret

```bash
kubectl get secret <IMAGE_PULL_SECRET> -n argocd \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | \
  jq '{username: .auths["<REGISTRY>"].username, password: .auths["<REGISTRY>"].password}'
```

### 3.3 Compare

If the passwords differ, the ArgoCD repo secret holds stale credentials. If the `client_id` (username) also differs, the secrets may be linked to different Vault leases entirely.

---

## Phase 4: Inspect the VaultDynamicSecret CRs

### 4.1 List All VDS CRs in the ArgoCD Namespace

```bash
kubectl get vaultdynamicsecret -n argocd
```

### 4.2 Get the Full Spec of Each Relevant VDS

```bash
kubectl get vaultdynamicsecret <VDS_NAME> -n argocd -o yaml
```

**Critical fields to check:**

| Field | What to look for |
|---|---|
| `spec.destination.name` | Which K8s Secret this VDS writes to |
| `spec.destination.overwrite` | **If `false`, this is the root cause.** VSO will not overwrite manually edited or pre-existing secrets. |
| `spec.mount` | Vault secrets engine mount (e.g. `azure`) |
| `spec.namespace` | Vault namespace (e.g. `admin/central`) |
| `spec.path` | Vault path (e.g. `creds/acr-pull`) |
| `status.secretLease.duration` | Lease TTL in seconds — tells you how often creds rotate |
| `status.lastRenewalTime` | When VSO last renewed the lease |

### 4.3 Check VDS Status for Errors

```bash
kubectl get vaultdynamicsecret <VDS_NAME> -n argocd -o yaml | grep -A 30 "status:"
```

---

## Phase 5: Fix — Rotate the Stale Secrets

### 5.1 Delete Any Manual (Non-VSO) Secrets

If you found `repo-creds` or `repository` secrets that are **not** VSO-managed and hold stale credentials, delete them. They are silently overriding the VSO-managed ones.

```bash
kubectl delete secret <MANUAL_SECRET_NAME> -n argocd
```

> **⚠️ Warning:** Only delete secrets you have confirmed are stale and not managed by another controller. Check `ownerReferences` and labels first.

### 5.2 Delete VSO-Managed Secrets So VSO Recreates Them

For each VSO-managed secret with stale credentials:

```bash
kubectl delete secret <SECRET_NAME> -n argocd
```

Watch it come back:

```bash
kubectl get secret <SECRET_NAME> -n argocd -w
```

VSO will detect its owned secret is missing and recreate it with fresh dynamic credentials within seconds.

### 5.3 Patch `overwrite: true` on All VaultDynamicSecrets

This is the most important step for preventing recurrence:

```bash
kubectl patch vaultdynamicsecret <VDS_NAME> -n argocd --type='merge' \
  -p '{"spec":{"destination":{"overwrite":true}}}'
```

Repeat for **every** VDS that targets registry credentials.

> **⚠️ Important:** Also update the source manifests (Git/Helm values) so that `overwrite: true` survives the next ArgoCD sync. A `kubectl patch` alone will be reverted if ArgoCD manages the VDS resource.

### 5.4 Verify the New Credentials Are Valid

```bash
# Check new creation timestamp
kubectl get secret <SECRET_NAME> -n argocd -o jsonpath='{.metadata.creationTimestamp}'

# Check new password
kubectl get secret <SECRET_NAME> -n argocd -o jsonpath='{.data.password}' | base64 -d
```

---

## Phase 6: Force ArgoCD to Pick Up the New Credentials

### 6.1 Restart the Repo-Server

The ArgoCD repo-server caches registry credentials in-process. A fresh secret in the K8s API is not enough — the repo-server must be restarted to re-read it.

```bash
kubectl rollout restart deployment argocd-repo-server -n argocd
kubectl rollout status deployment argocd-repo-server -n argocd
```

### 6.2 Hard-Refresh the Affected Applications

A `hard` refresh clears ArgoCD's manifest generation cache, which includes cached `helm registry login` results:

```bash
kubectl patch application <APP_NAME> -n argocd --type='merge' \
  -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"hard"}}}'
```

### 6.3 Watch for Recovery

```bash
kubectl get application <APP_NAME> -n argocd -w
```

You should see the sync status transition from `Unknown` → `Synced`.

### 6.4 Bulk-Refresh All Failing Applications

```bash
kubectl get applications -n argocd -o json | \
  jq -r '.items[] | select(.status.sync.status == "Unknown") | .metadata.name' | \
  xargs -I{} kubectl patch application {} -n argocd --type='merge' \
    -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"hard"}}}'
```

---

## Phase 7: Verify Reflector Mirrors (If Applicable)

If the image pull secret uses Ember Stack Reflector annotations, verify the mirrored copies are in sync:

```bash
# Find which namespaces receive the mirror
kubectl get secret <IMAGE_PULL_SECRET> -n argocd \
  -o jsonpath='{.metadata.annotations.reflector\.v1\.k8s\.emberstack\.com/reflection-auto-namespaces}'

# Compare data hashes across namespaces
for ns in <NS1> <NS2> <NS3>; do
  echo -n "$ns: "
  kubectl get secret <IMAGE_PULL_SECRET> -n $ns \
    -o jsonpath='{.data}' 2>/dev/null | md5sum || echo "NOT FOUND"
done
```

---

## Post-Incident Checklist

- [ ] All ArgoCD repo/repo-creds secrets for the registry are VSO-managed (no manual secrets)
- [ ] All relevant `VaultDynamicSecret` CRs have `overwrite: true`
- [ ] The `overwrite: true` change is committed to Git source manifests (not just `kubectl patch`)
- [ ] No `repo-creds` secrets silently overriding `repository` secrets for the same URL
- [ ] Repo-server restarted and all affected applications show `Synced`
- [ ] Reflector-mirrored copies of image pull secrets are up to date
- [ ] `debug-acr-secret` and any other ad-hoc test secrets are cleaned up

---

## Architectural Recommendations

### 1. Always Use `overwrite: true` for Dynamic Secrets

`overwrite: false` is a safety net for static secrets where you don't want VSO to clobber manual edits. For dynamic secrets with finite leases, it **breaks rotation** and is the single most common cause of this failure.

### 2. Avoid Duplicate Credential Secrets for the Same Registry

Each registry URL should have **one** ArgoCD repo secret, managed by **one** VaultDynamicSecret. Multiple secrets for the same URL (especially mixing `repo-creds` and `repository` types) create priority conflicts and make debugging harder.

### 3. Understand the ArgoCD Repo-Server Credential Cache

Even after updating K8s Secrets, the repo-server must be restarted to pick up new values. Factor this into your rotation strategy — if Vault rotates credentials faster than ArgoCD re-reads them, you will get intermittent auth failures.

### 4. Monitor VDS Lease Health

Set up alerts for `VaultDynamicSecret` resources with sync errors or expired leases:

```bash
kubectl get vaultdynamicsecret -A -o json | \
  jq '.items[] | select(.status.error != null) | {namespace: .metadata.namespace, name: .metadata.name, error: .status.error}'
```

---

## Quick Reference: Vault Path Formula

Assemble the full Vault path from three VDS spec fields:

```
{spec.namespace}/{spec.mount}/{spec.path}
```

Example: `admin/central/azure/creds/acr-pull`
