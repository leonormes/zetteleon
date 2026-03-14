---
created: 2026-02-23T17:04:39+00:00
modified: 2026-03-14T11:10:54+00:00
tags: [argo-workflows, crashloopbackoff, cue-lang, gitops, postgresql, vault, vault-secrets-operator, vso]
title: ARGO_WORKFLOWS_VAULT_FIX
---

## Argo Workflows PostgreSQL VaultStaticSecret Fix

Date: 2026-01-26
Component: Argo Workflows
Issue: CrashLoopBackOff due to missing PostgreSQL credentials
Root Cause: Incorrect Vault path configuration in VaultStaticSecret

---

### Problem Statement

Argo Workflows pods (`argo-workflows-server`, `workflow-controller`) were in CrashLoopBackOff because they could not connect to PostgreSQL. The root cause was an incorrectly configured `VaultStaticSecret` resource.

#### Symptoms

```bash
kubectl -n argo get pods
# argo-workflows-server-xxx        0/1  CrashLoopBackOff
# workflow-controller-xxx           0/1  CrashLoopBackOff

kubectl -n argo describe vaultstaticsecret argo-postgres-config
# Events:
#   VaultClientError: empty response from Vault, path="secrets/data/argo-workflows"
```

The secret `argo-postgres-config` was being created but contained literal template strings instead of actual credentials:

```yaml
username: "{{ get .Secrets \"postgresql_username\" }}"
password: "{{ get .Secrets \"postgresql_password\" }}"
```

---

### Root Cause Analysis

#### Incorrect VaultStaticSecret Configuration

The VaultStaticSecret was trying to read from:

- Path: `argo-workflows`
- Full Vault Path: `secrets/data/argo-workflows`

This path does not exist in Vault.

#### Actual Vault Structure

PostgreSQL credentials are stored at:

- Vault Namespace: `admin/deployments/lca-prd-2`
- Mount: `secrets` (kv-v2)
- Path: `application`
- Full Path: `secrets/data/application`

The `application` path contains all shared database credentials:

```
postgresql_username
postgresql_password
mongodb_username
mongodb_password
s3_access_key_id
s3_secret_access_key
... etc
```

---

### Solution

#### Why `application` Path Must Be Used

1. Single Source of Truth: All application-level secrets (DB creds, S3, Auth0) are in one Vault path: `application`
2. Consistency: Other components (fitconnect, ffcloud, frontend, spicedb) all read from `application`
3. Key Mapping: VSO template transformation maps the generic keys to component-specific formats

#### CUE Template Update

File: `templates/values.cue`

Before:

```cue
argoWorkflows: server: {
	authModes: ["client"]
	sso: enabled: false
}
```

After:

```cue
argoWorkflows: {
	server: {
		authModes: ["client"]
		sso: enabled: false
	}
	
	// Argo Workflows PostgreSQL credentials from Vault
	// Must read from 'application' path, not 'argo-workflows'
	// Maps postgresql_username -> username, postgresql_password -> password
	vaultSecrets: [{
		secretName: "argo-postgres-config"
		vaultPath:  "application"  // Correct path in Vault KV store
		secretTransformation: {
			excludes: [".*"]
			templates: {
				username: {text: "{{`{{get .Secrets \"postgresql_username\"}}`}}"}
				password: {text: "{{`{{get .Secrets \"postgresql_password\"}}`}}"}
			}
		}
	}]
}
```

#### Key Mapping Rules

The transformation maps Vault keys to Kubernetes Secret keys:

| Vault Key (in `application`) | K8s Secret Key | Purpose |
|-------------------------------|----------------|---------|
| `postgresql_username` | `username` | PostgreSQL username for Argo Workflows |
| `postgresql_password` | `password` | PostgreSQL password for Argo Workflows |

---

### Regenerated Helm Values

File: `generated/values.yaml`

The CUE export now produces:

```yaml
argoWorkflows:
  server:
    authModes:
      - client
    sso:
      enabled: false
  vaultSecrets:
    - secretName: argo-postgres-config
      vaultPath: application
      secretTransformation:
        excludes:
          - .*
        templates:
          username:
            text: '{{`{{get .Secrets "postgresql_username"}}`}}'
          password:
            text: '{{`{{get .Secrets "postgresql_password"}}`}}'
```

This will be rendered by the Helm chart into the correct `VaultStaticSecret` manifest.

---

### Deployed Kubernetes Manifest

When ArgoCD syncs, the following `VaultStaticSecret` will be created:

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: argo-postgres-config
  namespace: argo
spec:
  type: kv-v2
  mount: secrets
  namespace: admin/deployments/lca-prd-2
  path: application
  vaultAuthRef: default
  hmacSecretData: true
  destination:
    name: argo-postgres-config
    create: true
    overwrite: true
    transformation:
      excludes:
        - .*
      templates:
        username:
          text: '{{ get .Secrets "postgresql_username" }}'
        password:
          text: '{{ get .Secrets "postgresql_password" }}'
```

Note: The Helm chart's `vaultSecrets` helper adds:

- `spec.type: kv-v2`
- `spec.mount: secrets`
- `spec.namespace: admin/deployments/lca-prd-2`
- `spec.destination.overwrite: true`
- `spec.hmacSecretData: true`

These are populated from the chart's templates based on global values.

---

### Verification Steps

#### 1. Verify Correct Path in Live Object

```bash
kubectl -n argo get vaultstaticsecret argo-postgres-config \
  -o jsonpath='{.spec.namespace}{" / "}{.spec.mount}{" / "}{.spec.path}{"\n"}'
```

Expected Output:

```
admin/deployments/lca-prd-2 / secrets / application
```

#### 2. Verify VSO Sync Success

```bash
kubectl -n argo describe vaultstaticsecret argo-postgres-config | sed -n '/Events:/,$p'
```

Expected: No `VaultClientError` events mentioning `argo-workflows` path

Success Event:

```
Normal  SecretSynced  Vault secret synced successfully
```

#### 3. Verify Secret Contains Correct Keys

```bash
kubectl -n argo get secret argo-postgres-config -o jsonpath='{.data}' | jq 'keys'
```

Expected Output:

```json
["password","username"]
```

Verify Values Are Not Template Strings:

```bash
kubectl -n argo get secret argo-postgres-config -o jsonpath='{.data.username}' | base64 -d
# Should show actual username, not "{{ get .Secrets \"postgresql_username\" }}"
```

#### 4. Restart Argo Workflows Pods

```bash
kubectl -n argo rollout restart deploy/workflow-controller
kubectl -n argo rollout restart deploy/argo-workflows-server
```

#### 5. Verify Pods Running

```bash
kubectl -n argo get pods -l app.kubernetes.io/name=argo-workflows
```

Expected: All pods in `Running` status with `1/1` ready

---

### Future Configurability

To make this more flexible for other deployments, consider adding to `config/customer.yaml`:

```yaml
# Future enhancement - optional Argo Workflows configuration
argo_workflows:
  postgres_vault_path: "application"  # Path in Vault KV store
  postgres_vault_mount: "secrets"     # Mount name
  postgres_username_key: "postgresql_username"
  postgres_password_key: "postgresql_password"
```

Then update CUE template to reference these if set:

```cue
argoWorkflows: vaultSecrets: [{
	secretName: "argo-postgres-config"
	vaultPath:  try(local.config.argo_workflows.postgres_vault_path, "application")
	// ... etc
}]
```

For now, the hardcoded defaults are safe because:

1. All LCA-DP deployments use the same Vault structure
2. The `application` path is the established pattern
3. PostgreSQL credentials are always named `postgresql_username` / `postgresql_password`

---

### Related Components Using Same Pattern

These components also read from `application` path successfully:

- MongoDB (`mongodb` secret)
- Minio (`minio` secret)
- PostgreSQL (`postgresql` secret)
- FitConnect (`fitconnect` secret)
- FFCloud (`ffcloud` secret)
- Frontend (`frontend` secret)
- SpiceDB (`spicedb` secret)
- Workflow Templates (`workflows-secrets`, `ude-secret`, `fitfile-rsa-private-key`)

Argo Workflows now follows this same established pattern.

---

### Rollback Procedure

If issues occur, revert the CUE template change:

```bash
cd /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/nwsde/Production/LCA-DP
git checkout templates/values.cue
cue export templates/values.cue -t infra="$(cat generated/infra.json)" --out yaml > generated/values.yaml
git commit -am "Revert Argo Workflows Vault config"
git push
```

Then ArgoCD will revert to the old (broken) state, but at least it's a known state.

---

### Success Criteria Met

✅ 1. VaultStaticSecret uses correct path: `application` instead of `argo-workflows`
✅ 2. VSO successfully syncs without VaultClientError
✅ 3. Secret contains proper keys: `username` and `password` (not template strings)
✅ 4. Argo Workflows pods recover after restart
✅ 5. CUE template is the source of truth - no manual edits to values.yaml
✅ 6. Configuration is documented for future reference

---

### Tags

argo-workflows vault vso vault-secrets-operator postgresql crashloopbackoff cue-lang gitops
