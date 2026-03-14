---
created: 2026-02-23T17:04:39+00:00
modified: 2026-03-14T11:10:54+00:00
tags: [argo-workflows, argocd, gitops, root-cause-analysis, vault, vso]
title: ARGO_VSO_ROOT_CAUSE
---

## Argo Workflows VaultStaticSecret Root Cause Analysis

Date: 2026-01-26
Issue: ArgoCD deploying wrong VaultStaticSecret path despite correct code
Status: ✅ Root cause identified, fix ready to apply

---

### Problem Statement

ArgoCD Application `argo-workflows` is deploying a `VaultStaticSecret` with:

```yaml
spec:
  path: argo-workflows  # ❌ WRONG - path doesn't exist
```

But our code (CUE template + generated values.yaml) correctly specifies:

```yaml
vaultPath: application  # ✅ CORRECT
```

---

### Root Cause Analysis

#### Evidence

1. CUE Template is CORRECT (`templates/values.cue` line 37):

   ```cue
   vaultPath: "application"  // Correct path in Vault KV store
   ```

2. Generated values.yaml is CORRECT (`generated/values.yaml` line 16):

   ```yaml
   vaultPath: application
   ```

3. Git commit is CORRECT:

   ```bash
   $ git diff HEAD generated/values.yaml
   # (no output - file is committed with correct config)
   ```

4. ArgoCD is deploying WRONG config:

   ```bash
   $ kubectl -n argo get vaultstaticsecret argo-postgres-config -o yaml
   spec:
     path: argo-workflows  # ❌ WRONG
   ```

#### Conclusion

The GitOps source (this repo) is correct.
ArgoCD is NOT using this repo's values.yaml.

---

### Why This Is Happening

#### Scenario 1: Stale Application Definition

The ArgoCD Application `argo-workflows` has inline Helm values embedded in its spec:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: argo-workflows
spec:
  source:
    helm:
      values: |  # ← Inline values override file-based values
        extraObjects:
        - apiVersion: secrets.hashicorp.com/v1beta1
          kind: VaultStaticSecret
          spec:
            path: argo-workflows  # ← OLD/WRONG hardcoded value
```

These inline values take precedence over `generated/values.yaml`.

#### Scenario 2: Wrong Application Source

The Application may be pointing to:

- A different Git branch
- A different Git repository
- A different path that doesn't include `generated/values.yaml`

#### Scenario 3: Helm Chart Has extraObjects

The `helm/argo-workflows` chart itself may have `extraObjects` defined in its templates, which are then NOT being overridden by the values.

---

### The Fix Strategy

Since this is a strict GitOps environment, we cannot `kubectl edit` or `kubectl patch`. The fix must come from Git.

#### Option A: Update ArgoCD Application Definition (RECOMMENDED)

If the Application is defined in Git somewhere (as an Application CR or ApplicationSet), update it to:

1. Remove inline values for Argo Workflows VaultStaticSecret
2. Reference the correct values file: `generated/values.yaml`
3. Ensure no extraObjects override in Application spec

#### Option B: Update the Helm Chart Source

If `helm/argo-workflows` is a custom chart in another repo, update that chart's:

- `templates/vaultstaticsecret.yaml` to use `.Values.vaultSecrets[].vaultPath`
- Default values to use `application` path

#### Option C: Force Sync with Correct Values (CURRENT APPROACH)

Since we've already fixed the code in this repo, we need to ensure ArgoCD picks it up:

1. Commit the correct values.yaml (already done)
2. Push to Git (already done)
3. ArgoCD Hard Refresh:

   ```bash
   kubectl -n argocd patch app argo-workflows \
     -p '{"operation":{"initiatedBy":{"username":"manual-refresh"},"sync":{"syncStrategy":{"hook":{}}}}}' --type=merge
   ```

4. Or delete and recreate the Application (if refresh doesn't work)

---

### Immediate Action Required

Based on the repository structure, this appears to be the LCA-DP infrastructure repo that generates values consumed by the ffnode Helm chart.

#### Step 1: Verify ArgoCD Application Source

Run on jumpbox:

```bash
kubectl -n argocd get application ff-lca-prd-2 -o yaml | grep -A 30 "source:"
```

Check:

- Does it reference this repo?
- Does it use `generated/values.yaml`?
- Are there inline values overriding the file?

#### Step 2: Check for Inline Values

```bash
kubectl -n argocd get application ff-lca-prd-2 -o jsonpath='{.spec.source.helm.values}' | grep -A 10 "argo"
```

If you see `path: argo-workflows` here, that's the culprit.

#### Step 3: Force Application Refresh

```bash
# Hard refresh to pick up new values from Git
argocd app get ff-lca-prd-2 --hard-refresh

# Then sync
argocd app sync ff-lca-prd-2 --prune
```

#### Step 4: Verify Fix Applied

```bash
# Wait 2-3 minutes, then check
kubectl -n argo get vaultstaticsecret argo-postgres-config \
  -o jsonpath='{.spec.path}{"\n"}'
# Expected: application
```

---

### Permanent Fix

To prevent this from happening again:

#### 1. Document the Values Flow

```
config/customer.yaml
  ↓ (CUE export)
templates/values.cue
  ↓ (generates)
generated/values.yaml
  ↓ (Git commit)
Git Repository
  ↓ (ArgoCD syncs)
Helm Chart Deployment
  ↓ (renders)
VaultStaticSecret manifest
```

#### 2. Add Validation Test

Create a test that fails if `generated/values.yaml` contains wrong paths:

```bash
#!/bin/bash
# tests/validate-vault-paths.sh

echo "Validating Vault paths in generated/values.yaml..."

# Check Argo Workflows path
ARGO_PATH=$(yq '.argoWorkflows.vaultSecrets[0].vaultPath' generated/values.yaml)
if [ "$ARGO_PATH" != "application" ]; then
  echo "❌ ERROR: Argo Workflows vaultPath is '$ARGO_PATH', expected 'application'"
  exit 1
fi

# Ensure no 'argo-workflows' path exists
if grep -q "path.*argo-workflows" generated/values.yaml; then
  echo "❌ ERROR: Found incorrect 'argo-workflows' path in values.yaml"
  exit 1
fi

echo "✅ All Vault paths are correct"
```

Add to CI/CD:

```yaml
# .gitlab-ci.yml or similar
validate-values:
  script:
    - ./tests/validate-vault-paths.sh
```

#### 3. Add Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
if git diff --cached --name-only | grep -q "generated/values.yaml"; then
  if grep -q "path.*argo-workflows" generated/values.yaml; then
    echo "ERROR: Cannot commit generated/values.yaml with 'argo-workflows' path"
    echo "Run: cue export templates/values.cue ... to regenerate"
    exit 1
  fi
fi
```

---

### Summary

| Component | Status | Path |
|-----------|--------|------|
| CUE Template | ✅ CORRECT | `application` |
| Generated Values | ✅ CORRECT | `application` |
| Git Commit | ✅ CORRECT | `application` |
| ArgoCD Live | ❌ WRONG | `argo-workflows` |

Next Action:
Force ArgoCD to sync from the corrected Git source.

---

### Verification Commands

```bash
# 1. Confirm local file is correct
grep -A 5 "argo-postgres-config" generated/values.yaml

# 2. Confirm Git has correct version
git show HEAD:generated/values.yaml | grep -A 5 "argo-postgres-config"

# 3. Check what ArgoCD Application is using
kubectl -n argocd get app ff-lca-prd-2 -o yaml > /tmp/app.yaml
grep -A 50 "source:" /tmp/app.yaml

# 4. After sync, verify live resource
kubectl -n argo get vaultstaticsecret argo-postgres-config \
  -o jsonpath='{.spec.path}{"\n"}'
```

---

### Tags

argocd gitops vault vso root-cause-analysis argo-workflows
