---
aliases: []
confidence: 
created: 2025-10-23T14:42:57Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: thehyve-mkuh-add-variables-guide
type:
uid: 
updated: 
version:
---

## Adding Variables to Thehyve-mkuh Deployment

### Overview

This guide explains how to add environment variables to the **thehyve-mkuh** deployment, including both configuration file changes and HashiCorp Vault secrets.

---

### 1. Adding Environment Variables to Kubernetes

#### Location: Values File

**File Path:**

```sh
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/ff-c/thehyve_values.yaml
```

**Git Repository:**

- Repo: `https://gitlab.com/fitfile/deployment.git`
- Branch: `latest-release`
- Path: `ffnodes/fitfile/ff-c/thehyve_values.yaml`

#### Method 1: Plain Environment Variables (Non-Sensitive)

Add to the `extraEnvVars` section in `thehyve_values.yaml`:

```yaml
extraEnvVars:
  - name: NHS_SITE
    value: mkuh
  # Add your new variable here:
  - name: YOUR_VAR_NAME
    value: "your-value"
  - name: ANOTHER_VAR
    value: "another-value"
```

**Use Case:** Configuration values, feature flags, non-sensitive settings

---

#### Method 2: Secrets from Vault (Sensitive Data)

##### Step A: Add Variable Reference in Values File

Add to `extraEnvVars` section referencing the Vault secret:

```yaml
extraEnvVars:
  - name: NHS_SITE
    value: mkuh
  # Existing Vault secrets
  - name: QCR_BUCKET
    valueFrom:
      secretKeyRef:
        name: thehyve
        key: qcr_bucket
  # Add your new secret reference:
  - name: YOUR_SECRET_VAR
    valueFrom:
      secretKeyRef:
        name: thehyve
        key: your_secret_key
```

##### Step B: Add Secret to Vault Template

In the same `thehyve_values.yaml` file, update the `extraDeploy` VaultStaticSecret section:

**Location:** Lines 96-137 in `thehyve_values.yaml`

Add your secret key to the `transformation.templates` section:

**YAML Snippet**

```yaml
extraDeploy:
  - apiVersion: secrets.hashicorp.com/v1beta1
    kind: VaultStaticSecret
    metadata:
      name: thehyve
      namespace: "{{ .Release.Namespace }}"
    spec:
      namespace: admin/deployments/ff-c # ← Vault namespace
      mount: secrets
      path: thehyve # ← Secret path in Vault
      type: kv-v2
      hmacSecretData: true
      destination:
        create: true
        name: thehyve
        transformation:
          excludes:
            - .*
          templates:
            qcr_bucket:
              text: '{{`{{get .Secrets "qcr_bucket"}}`}}'
            qcr_access_key_id:
              text: '{{`{{get .Secrets "qcr_access_key_id"}}`}}'
            qcr_secret_access_key:
              text: '{{`{{get .Secrets "qcr_secret_access_key"}}`}}'
            qcr_iam_role:
              text: '{{`{{get .Secrets "qcr_iam_role"}}`}}'
            # Add your new secret template here:
            your_secret_key:
              text: '{{`{{get .Secrets "your_secret_key"}}`}}'
```

**Links:**

- [thehyve-mkuh-investigation-report](<thehyve-mkuh-investigation-report.md>)
- [General Principles for Adding Secrets](<General Principles for Adding Secrets.md>)

**Important Notes:**

- The key name in `templates:` must match the key in `secretKeyRef.key`
- Use the exact template format with escaped curly braces

---

### 2. Adding Secrets to HashiCorp Vault

#### Vault Namespace Structure

**Full Vault Path:**

```sh
admin/deployments/ff-c/secrets/thehyve
```

**Breakdown:**

- **Vault Namespace:** `admin/deployments/ff-c`
- **Secrets Mount:** `secrets`
- **Secret Path:** `thehyve`

#### Using Vault CLI

##### Login to Vault

```bash
# Set Vault address
export VAULT_ADDR="https://your-vault-address.com"

# Login (use appropriate auth method)
vault login -method=oidc
# OR
vault login -method=token
```

##### Set Namespace

```bash
# Set the correct namespace
export VAULT_NAMESPACE="admin/deployments/ff-c"
```

##### Add/Update Secrets

**Option 1: Add a Single Key-Value Pair**

```bash
vault kv put -mount=secrets thehyve \
  your_secret_key="your-secret-value"
```

**Option 2: Update Existing Secret (Preserve Other Keys)**

```bash
# Read existing secret first
vault kv get -mount=secrets thehyve

# Update with patch (adds/updates only specified keys)
vault kv patch -mount=secrets thehyve \
  your_secret_key="your-secret-value" \
  another_key="another-value"
```

**Option 3: Replace Entire Secret**

```bash
vault kv put -mount=secrets thehyve \
  qcr_bucket="existing-bucket" \
  qcr_access_key_id="existing-key-id" \
  qcr_secret_access_key="existing-secret" \
  qcr_iam_role="existing-role" \
  your_secret_key="your-new-secret" \
  another_key="another-secret"
```

##### Verify Secret

```bash
# List all keys in the secret
vault kv get -mount=secrets thehyve

# Get specific field
vault kv get -mount=secrets -field=your_secret_key thehyve
```

#### Using Vault UI

1. **Navigate to Vault UI:** `https://your-vault-address.com/ui/`
2. **Select Namespace:** Choose `admin/deployments/ff-c` from namespace dropdown
3. **Navigate to Secrets Engine:**
   - Click on `secrets/` mount
   - Navigate to path `thehyve/`
4. **Edit Secret:**
   - Click on the secret
   - Click "Create new version +"
   - Add your new key-value pairs
   - Click "Save"

---

### 3. Deployment Workflow

#### Step-by-Step Process

1. **Add Secrets to Vault** (if needed)

   ```bash
   export VAULT_NAMESPACE="admin/deployments/ff-c"
   vault kv patch -mount=secrets thehyve your_secret_key="value"
   ```

2. **Update Values File**

   ```bash
   cd /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment

   # Edit the file
   vim ffnodes/fitfile/ff-c/thehyve_values.yaml
   ```

3. **Commit and Push Changes**

   ```bash
   git add ffnodes/fitfile/ff-c/thehyve_values.yaml
   git commit -m "FFAPP-XXXX: feat(thehyve-mkuh): add YOUR_VAR_NAME environment variable"
   git push origin latest-release
   ```

4. **Wait for ArgoCD Sync**
   - ArgoCD will automatically detect the change
   - Sync is triggered every 3 minutes (default)
   - Or manually sync via ArgoCD UI

5. **Verify Deployment**

   ```bash
   # Check ArgoCD sync status
   kubectl get application thehyve-mkuh -n argocd -o jsonpath='{.status.sync.status}'

   # Verify environment variables in pod
   kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- env | grep YOUR_VAR_NAME

   # Check if secret is loaded
   kubectl describe secret thehyve -n thehyve-mkuh
   ```

---

### 4. Current Configuration Reference

#### Existing Environment Variables

**Plain Variables:**

- `NHS_SITE=mkuh`

**Vault-Sourced Secrets:**

- `QCR_BUCKET` → from `thehyve.qcr_bucket`
- `QCR_ACCES_KEY_ID` → from `thehyve.qcr_access_key_id`
- `QCR_SECRET_ACCESS_KEY` → from `thehyve.qcr_secret_access_key`
- `QCR_IAM_ROLE` → from `thehyve.qcr_iam_role`

**Auto-Generated (from Chart):**

- `OMOP_TARGET_DB` → from database config
- `AIRFLOW__CORE__SQL_ALCHEMY_CONN` → from database config
- `AIRFLOW_ADMIN_*` → from airflow.initAdmin config

#### Vault Secret Sync Behavior

- **Refresh Interval:** 10 minutes
- **Auto Rollout Restart:** Yes (deployment restarts on secret change)
- **Drift Detection:** Enabled (HMAC validation)

---

### 5. Examples

#### Example 1: Add Database Connection String (Vault)

**1. Add secret to Vault:**

```bash
export VAULT_NAMESPACE="admin/deployments/ff-c"
vault kv patch -mount=secrets thehyve \
  external_db_url="postgresql://user:pass@host:5432/dbname"
```

**2. Update `thehyve_values.yaml`:**

```yaml
extraEnvVars:
  # ... existing vars ...
  - name: EXTERNAL_DB_URL
    valueFrom:
      secretKeyRef:
        name: thehyve
        key: external_db_url

extraDeploy:
  - apiVersion: secrets.hashicorp.com/v1beta1
    kind: VaultStaticSecret
    # ... existing config ...
    spec:
      # ... existing spec ...
      destination:
        transformation:
          templates:
            # ... existing templates ...
            external_db_url:
              text: '{{`{{get .Secrets "external_db_url"}}`}}'
```

#### Example 2: Add Feature Flag (Plain Value)

**Update `thehyve_values.yaml`:**

```yaml
extraEnvVars:
  # ... existing vars ...
  - name: ENABLE_NEW_FEATURE
    value: "true"
  - name: LOG_LEVEL
    value: "INFO"
```

#### Example 3: Add API Key (Vault)

**1. Add to Vault:**

```bash
export VAULT_NAMESPACE="admin/deployments/ff-c"
vault kv patch -mount=secrets thehyve \
  api_key="sk_live_1234567890abcdef"
```

**2. Update values file:**

```yaml
extraEnvVars:
  - name: API_KEY
    valueFrom:
      secretKeyRef:
        name: thehyve
        key: api_key

extraDeploy:
  - apiVersion: secrets.hashicorp.com/v1beta1
    kind: VaultStaticSecret
    spec:
      destination:
        transformation:
          templates:
            api_key:
              text: '{{`{{get .Secrets "api_key"}}`}}'
```

---

### 6. Troubleshooting

#### Secret Not Appearing in Pod

**Check VaultStaticSecret Status:**

```bash
kubectl get vaultstaticsecret thehyve -n thehyve-mkuh -o yaml
kubectl describe vaultstaticsecret thehyve -n thehyve-mkuh
```

**Check Vault Secrets Operator Logs:**

```bash
kubectl logs -n vault-secrets-operator deployment/vault-secrets-operator-controller-manager
```

**Verify Secret Exists:**

```bash
kubectl get secret thehyve -n thehyve-mkuh -o yaml
```

#### ArgoCD Not Syncing

**Check Application Status:**

```bash
kubectl get application thehyve-mkuh -n argocd -o yaml
```

**Manual Sync:**

```bash
kubectl patch application thehyve-mkuh -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"latest-release"}}}'
```

**Check ArgoCD UI:**

- URL: <https://argocd.your-cluster.com>
- Navigate to `thehyve-mkuh` application

#### Environment Variable Not Set

**Check Pod Environment:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- env | sort
```

**Check Deployment Spec:**

```bash
kubectl get deployment thehyve-mkuh -n thehyve-mkuh -o jsonpath='{.spec.template.spec.containers[0].env}' | jq
```

#### Vault Authentication Issues

**Check VaultAuth:**

```bash
kubectl get vaultauth -n thehyve-mkuh
kubectl describe vaultauth default -n thehyve-mkuh
```

---

### 7. Best Practices

#### Security

- ✅ **Always use Vault for sensitive data** (passwords, API keys, tokens)
- ✅ Use `kv patch` to avoid overwriting existing secrets
- ✅ Never commit secrets to Git
- ❌ Don't use plain values for credentials

#### Naming Conventions

- Use `UPPER_SNAKE_CASE` for environment variable names
- Use `lower_snake_case` for Vault secret keys
- Prefix related variables (e.g., `DB_HOST`, `DB_PORT`, `DB_NAME`)

#### Version Control

- Follow commit message convention: `FFAPP-XXXX: type(scope): description`
- Create feature branches for significant changes
- Test in non-production first

#### Documentation

- Document new variables in application README
- Include purpose and expected values
- Note any dependencies or prerequisites

---

### Quick Reference

| Task                       | Namespace/Path                             |
| -------------------------- | ------------------------------------------ |
| **Kubernetes Values File** | `ffnodes/fitfile/ff-c/thehyve_values.yaml` |
| **Vault Namespace**        | `admin/deployments/ff-c`                   |
| **Vault Secrets Mount**    | `secrets`                                  |
| **Vault Secret Path**      | `thehyve`                                  |
| **Vault Full Path**        | `admin/deployments/ff-c/secrets/thehyve`   |
| **Kubernetes Namespace**   | `thehyve-mkuh`                             |
| **Secret Name**            | `thehyve`                                  |
| **ArgoCD Application**     | `thehyve-mkuh` (in `argocd` namespace)     |

---

**Last Updated:** 2025-10-23  
**Cluster:** fitfile-cloud-prod-1-aks-cluster
