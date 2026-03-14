---
created: 2026-02-23T17:04:39+00:00
modified: 2026-03-14T11:10:55+00:00
title: ARGO_FIX_COMMANDS
---

## Argo Workflows VaultStaticSecret Fix - Execution Guide

Date: 2026-01-26

Status: ✅ Code is correct, ArgoCD needs to sync from Git

---

### Executive Summary

Problem: ArgoCD is deploying `VaultStaticSecret` with incorrect path `argo-workflows`

Root Cause: ArgoCD Application has stale/inline values that override the correct Git source

Solution: Force ArgoCD to sync from the corrected Git repository

Your code in this repo is CORRECT. Validation passed:

✓ All Vault path validations passed

✓ vaultPath: application (correct)

✓ No 'argo-workflows' path found

---

### Commands to Run

#### Step 1: Verify Current State (On Jumpbox)

```bash
# Check what ArgoCD Application is actually using
kubectl -n argocd get application ff-lca-prd-2 -o yaml > /tmp/argocd-app.yaml

# Look for inline values
grep -A 100 "helm:" /tmp/argocd-app.yaml | head -50

# Check if it points to this repo's values
grep -A 20 "source:" /tmp/argocd-app.yaml
```

What to look for:

- Does `source.repoURL` point to the LCA-DP repo?
- Does `source.helm.valueFiles` include `generated/values.yaml`?
- Are there inline `source.helm.values` overriding the file?

---

#### Step 2: Force ArgoCD Hard Refresh

```bash
# Option A: Using argocd CLI (preferred)
argocd app get ff-lca-prd-2 --hard-refresh
argocd app sync ff-lca-prd-2 --prune

# Option B: Using kubectl
kubectl -n argocd patch app ff-lca-prd-2 \
  --type json \
  -p='[{"op": "replace", "path": "/operation", "value": null}]'

# Force reconcile
kubectl -n argocd delete secret -l app.kubernetes.io/instance=ff-lca-prd-2 2>/dev/null || true
kubectl -n argocd annotate app ff-lca-prd-2 argocd.argoproj.io/refresh=normal --overwrite
```

---

#### Step 3: Wait and Verify VSS Updated

```bash
# Wait 2-3 minutes for ArgoCD to sync

# Check VaultStaticSecret path (MUST return 'application')
kubectl -n argo get vaultstaticsecret argo-postgres-config \
  -o jsonpath='{.spec.path}{"\n"}'

# Expected output: application
```

---

#### Step 4: Verify VSO Syncing Successfully

```bash
# Check VSO events (should have no VaultClientError)
kubectl -n argo describe vaultstaticsecret argo-postgres-config | sed -n '/Events:/,$p'

# Expected: SecretSynced events, NO "empty response from Vault" errors
```

---

#### Step 5: Verify Secret Contains Correct Data

```bash
# Check secret keys
kubectl -n argo get secret argo-postgres-config -o jsonpath='{.data}' | jq 'keys'

# Expected: ["password","username"] or ["_raw","password","username"]

# Verify values are NOT template strings
kubectl -n argo get secret argo-postgres-config -o jsonpath='{.data.username}' | base64 -d
# Should show: postg... (actual username, not {{ get .Secrets ... }})
```

---

#### Step 6: Verify Argo Workflows Pods Deploy

```bash
# Check if pods start
kubectl -n argo get pods -l app.kubernetes.io/name=argo-workflows

# Expected: Running pods (may take a few minutes)

# If pods don't appear, check ArgoCD sync status
kubectl -n argocd get app ff-lca-prd-2 -o jsonpath='{.status.sync.status}{"\n"}'
# Expected: Synced
```

---

### Troubleshooting

#### If Step 2 Doesn't Work (Hard Refresh Failed)

The Application may have hardcoded inline values. Check:

```bash
# Extract inline values
kubectl -n argocd get app ff-lca-prd-2 \
  -o jsonpath='{.spec.source.helm.values}' > /tmp/inline-values.yaml

# Check if it contains the wrong path
grep -A 5 "argo-postgres-config" /tmp/inline-values.yaml
```

If you see `path: argo-workflows` in inline values:

Option 1: Remove inline values (if Application is in Git)

- Find the Application YAML in Git (likely in a parent ArgoCD repo)
- Remove the `spec.source.helm.values` section
- Ensure `spec.source.helm.valueFiles` includes `generated/values.yaml`
- Commit and push

Option 2: Patch the Application (GitOps violation, use only if desperate)

```bash
# WARNING: This bypasses GitOps - Application may revert
kubectl -n argocd patch app ff-lca-prd-2 --type=json \
  -p='[{"op": "remove", "path": "/spec/source/helm/values"}]'

# Then immediately sync
argocd app sync ff-lca-prd-2 --force
```

---

#### If VSS Path Doesn't Update

Check if ArgoCD is actually using the correct Git ref:

```bash
# Check current Git commit ArgoCD is synced to
kubectl -n argocd get app ff-lca-prd-2 \
  -o jsonpath='{.status.sync.revision}{"\n"}'

# Compare with latest commit in this repo
git log -1 --oneline

# If different, force sync to HEAD
argocd app sync ff-lca-prd-2 --revision HEAD
```

---

#### If VSO Still Shows Errors

```bash
# Restart VSO to clear any cached state
kubectl -n vault-secrets-operator-system rollout restart deployment \
  vault-secrets-operator-controller-manager

# Wait 30 seconds, then check VSS again
sleep 30
kubectl -n argo describe vaultstaticsecret argo-postgres-config | tail -20
```

---

#### Nuclear Option: Delete and Recreate VSS

```bash
# Only if all else fails - this is safe because:
# 1. Secret data will be preserved (destination.overwrite: false)
# 2. VSO will recreate the VSS from ArgoCD's spec

kubectl -n argo delete vaultstaticsecret argo-postgres-config

# Wait for ArgoCD to recreate it (auto-sync)
# Or manually sync
argocd app sync ff-lca-prd-2 --resource secrets.hashicorp.com:VaultStaticSecret:argo/argo-postgres-config

# Verify new VSS has correct path
kubectl -n argo get vaultstaticsecret argo-postgres-config \
  -o jsonpath='{.spec.path}{"\n"}'
```

---

### Success Criteria

After all steps complete, you should see:

✅ VaultStaticSecret path:

```bash
$ kubectl -n argo get vaultstaticsecret argo-postgres-config -o jsonpath='{.spec.path}{"\n"}'
application
```

✅ No VSO errors:

```bash
$ kubectl -n argo describe vaultstaticsecret argo-postgres-config | grep -A 5 Events:
Events:
  Type    Reason        Age   From               Message
  ----    ------        ----  ----               -------
  Normal  SecretSynced  1m    VaultStaticSecret  Vault secret synced successfully
```

✅ Secret contains real values:

```bash
$ kubectl -n argo get secret argo-postgres-config -o jsonpath='{.data.username}' | base64 -d
postgres
```

✅ Argo Workflows pods healthy:

```bash
$ kubectl -n argo get pods -l app.kubernetes.io/name=argo-workflows
NAME                                     READY   STATUS    RESTARTS   AGE
argo-workflows-server-xxx                1/1     Running   0          5m
workflow-controller-xxx                  1/1     Running   0          5m
```

---

### Post-Fix: Prevent Regression

#### 1. Run Validation Locally Before Commits

```bash
# Add to your workflow
./scripts/validate-vault-paths.sh
```

#### 2. Add to CI/CD Pipeline

```yaml
# .gitlab-ci.yml or similar
validate-values:
  stage: test
  script:
    - ./scripts/validate-vault-paths.sh
  only:
    changes:
      - generated/values.yaml
      - templates/values.cue
```

#### 3. Document the Fix

```bash
# Update CHANGELOG or commit message
git log -1 --pretty=format:"%H %s" > docs/CHANGELOG_ARGO_FIX.txt
```

---

### Related Documentation

- [ARGO_WORKFLOWS_VAULT_FIX.md](./ARGO_WORKFLOWS_VAULT_FIX.md) - Technical details
- [ARGO_VAULT_FIX_DECISION.md](./ARGO_VAULT_FIX_DECISION.md) - Decision record
- [ARGO_VSO_ROOT_CAUSE.md](./ARGO_VSO_ROOT_CAUSE.md) - Root cause analysis
- [check_argo_vault_config.sh](../scripts/check_argo_vault_config.sh) - Pre-fix validation
- [validate-vault-paths.sh](../scripts/validate-vault-paths.sh) - Values validation

---

### Questions?

If you encounter issues not covered here:

1. Check ArgoCD UI for sync errors
2. Review ArgoCD Application logs: `kubectl -n argocd logs deployment/argocd-application-controller | grep lca-prd`
3. Check if there's a parent ApplicationSet controlling this Application
4. Verify the Git repo URL in Application spec matches this repo

---

### TL;DR

```bash
# Your code is correct. Force ArgoCD to use it:
argocd app get ff-lca-prd-2 --hard-refresh
argocd app sync ff-lca-prd-2 --prune

# Wait 2 min, then verify:
kubectl -n argo get vaultstaticsecret argo-postgres-config -o jsonpath='{.spec.path}{"\n"}'
# Must show: application
```
