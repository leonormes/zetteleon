---
alias: [Secret Management Protocol, Vault Onboarding]
created: 2026-02-05T00:00:00+00:00
modified: 2026-07-04T10:51:06+00:00
permalink: llmeon/30-library/so-t/protocol-vault-deployment-secret-management
status: stable
tags: [fitfile, onboarding, protocol, secrets, terraform, vault]
title: Protocol - Vault Deployment Secret Management
type: protocol
---

## Logic Map

- Objective: Systematically provision and populate HashiCorp Vault resources for a new customer deployment.
- Strategy: Use Infrastructure-as-Code (Terraform) to scaffold the namespace and manual population for sensitive values that cannot be automated yet.
- Dependencies:
    - Access to Central Services repository.
    - HCP Vault Admin Token.
    - Local `openssl` for key generation.

---

## The Algorithm

### 1. Infrastructure Scaffolding (Terraform)

_Initialize the Vault namespace and empty secret objects._

1. Navigate: Go to the `hcp/vault` directory in the Central Services repository.
2. Define Deployment: Open `locals.tf` and append a new block to the `deployments` variable:

```hcl
"${DEPLOYMENT_KEY}" = {
  secrets = tomap({
    "application"    = {},
    "spicedb"        = {},
    "cloudflare"     = {}, # Optional: Only if using Cloudflare
    "monitoring"     = {}, # Required for Grafana credentials
    "argo-workflows" = {}, # Required for Argo Workflows SSO
  })
}
```

1. Deploy: Commit, push, and approve the Terraform apply in Terraform Cloud.

### 2. Signing Key Generation

_Generate the Tenant PKCS8 signing keys required for the `application` secret._

```bash
mkdir ${DEPLOYMENT_KEY} && cd ${DEPLOYMENT_KEY}
# 1. Generate RSA keypair
openssl genrsa -out keypair.pem 4096
# 2. Convert to PKCS8 (Private Key)
openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in keypair.pem -out pkcs8.key
# 3. Extract Public Certificate
openssl rsa -in keypair.pem -pubout -out publickey.crt
```

### 3. Vault Population (Manual)

_Access the Vault UI and populate the keys. CRITICAL: Vault will reject JSON containing comments._

1. Access: Log in via HCP Portal -> `ops-project` -> Vault Dedicated -> Generate Admin Token.
2. Navigate: Go to the `deployments/${DEPLOYMENT_KEY}` namespace -> Secrets Engines -> `secrets`.
3. Populate `application`: Create a new version with the following mapping:

| Key | Value / Source |
|:--- |:--- |
| `mongodb_password` | Secure alphanumeric (min 10) |
| `mongodb_replica_set_key` | Secure alphanumeric (length 64) |
| `postgresql_password` | Secure alphanumeric (min 10) |
| `ude_key` | Output of `cargo run key-gen` from `ude_cli` |
| `spicedb_pre_shared_key` | Copy from `admin/fitfile/production/spicedb_secrets` |
| `fitfile_tenant_pkcs8.key` | Content of `pkcs8.key` |
| `fitfile_tenant_public.crt` | Content of `publickey.crt` |

1. Populate `spicedb`: Ensure `postgresql_password` and `spicedb_preshared_key` match the `application` secret.
2. Populate `monitoring`: Use values from the Grafana module outputs (`prometheus_password`, `loki_password`, `tempo_password`).

---

## Error Handling

- JSON Parse Error: Ensure all trailing commas and comments (`//`) are removed before saving in the Vault UI.
- Namespace Missing: If the deployment namespace is not visible, verify that the Terraform apply was successful and that you are logged in with an Admin token.

---

## Unit Test (Verification)

_Run from a cluster jumpbox to verify the sync._

```bash
# 1. Check VSO status
kubectl get vaultstaticsecret -n ${NAMESPACE} application

# 2. Verify Kubernetes secret was created
kubectl get secret -n ${NAMESPACE} application -o jsonpath='{.data}'
```

### 3. Vault Population (Manual)

### 4. Integration Layer: ArgoCD & Argo Workflows

_Specific configuration requirements for GitOps and Workflow engines._

- ArgoCD: Requires `admin_password` (hashed via `htpasswd`), GitLab deploy tokens for repository access, and Azure SSO client secrets.
- Argo Workflows: Primarily uses the same `postgresql` credentials as the main application for its internal database state.
