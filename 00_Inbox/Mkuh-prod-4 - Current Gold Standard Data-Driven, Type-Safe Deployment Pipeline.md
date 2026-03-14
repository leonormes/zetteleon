---
created: 2026-02-26T10:50:56+00:00
modified: 2026-03-14T11:10:52+00:00
title: Mkuh-prod-4 - Current Gold Standard Data-Driven, Type-Safe Deployment Pipeline
---

## Data-Driven, Type-Safe Deployment Pipeline—Architecture Prompt

### What This System Is

This is a multi-customer infrastructure deployment system for the FITFILE platform. Each customer gets an isolated AKS cluster on Azure, configured with a fixed set of platform services (Vault, Auth0, ArgoCD, Helm charts). The goal is that onboarding a new customer requires editing one file (`customer.yaml`) and running a pipeline.

The system spans three repositories:

| Repo                             | Purpose                                                                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| LCA-DP (customer deployment)     | Terraform that provisions the AKS cluster, networking, and registers the customer with platform services (Auth0, Vault, GitLab, TFC) |
| Jumpbox (in-cluster Terraform)   | Terraform that runs from inside the private network to bootstrap ArgoCD, Vault auth, and platform Helm charts onto the cluster       |
| CUE / values (config generation) | Shared CUE schema and render logic that transforms infrastructure facts into Helm `values.yaml` for the ArgoCD app                   |

These three repos form a sequential pipeline: LCA-DP provisions infra → exports facts → CUE validates and transforms → Helm values → ArgoCD deploys apps → Jumpbox bootstraps in-cluster resources.

---

### The Core Principle: Data Has One Home

Every value in the system must trace to exactly one authoritative source. There is a strict hierarchy:

```
customer.yaml          ← customer-specific values (name, env, CIDR, feature overrides)
       ↓
locals.tf              ← Terraform derivations (no literals except math/naming conventions)
       ↓
infra_facts output     ← the typed contract passed to CUE
       ↓
CUE schema             ← validates the contract, no data lives here
       ↓
CUE render             ← pure transformation, reads policy.* and infra.*, no literals
       ↓
policy_defaults.cue    ← platform-wide constants that are the same for every customer
       ↓
generated/values.yaml  ← the output; never edited by hand
```

If you find yourself typing a literal string or number anywhere except `customer.yaml` or `policy_defaults.cue`, you are doing it wrong.

---

### Layer Responsibilities

#### Layer 1: `config/customer.yaml`

The single source of truth. Contains everything that differs between customers.

Owns:

- Customer identity (`name`, `full_name`, `env`, `region`, `id`)
- Network assignment (`vnet_address_space`)
- Customer-specific application overrides (`ffcloud.default_organisation_admin_user_id`)
- Customer-specific feature flags (`fitconnect.feature_flags.export_to_s3`)

Does NOT own:

- Platform defaults (those belong in `policy_defaults.cue`)
- Derived values (those belong in `locals.tf`)
- Secrets (those belong in Vault / `secrets.auto.tfvars.json`)

Rule: If a value would be the same for every customer, it does not belong here.

```yaml
# CORRECT — customer-specific
name: "lca"
ffcloud:
  default_organisation_admin_user_id: "auth0|633adad9991af2b9ec7446c1"

# WRONG — platform constant, belongs in policy_defaults.cue
auth0_domain: "fitfile-prod.eu.auth0.com"
```

---

#### Layer 2: `locals.tf`

Transforms `customer.yaml` into every derived value Terraform needs. Contains only computation—no raw literals except for naming convention templates and mapping tables.

Owns:

- All string derivations from YAML inputs (`deployment_key`, `resource_group_name`, etc.)
- CIDR math (`cidrsubnet`, `cidrhost`)
- Environment-to-prefix mapping (`live` → `prd`)
- Feature flag defaults per environment (`standard_deployment` map)
- Extraction of optional customer overrides with safe defaults via `try()`

Does NOT own:

- Customer identity values (read from YAML)
- Infrastructure configuration (passed to modules)
- Generated file content (that belongs in `*_generator.tf` files)

```hcl
# CORRECT — derived from inputs
deployment_key = "${local.workload}-${local.env_prefix}-${local.id}"
ingress_ip     = cidrhost(local.subnets.system.address_prefixes[0], 50)

# CORRECT — safe extraction of optional customer override
ffcloud_admin_user_id = try(local.config.ffcloud.default_organisation_admin_user_id, "")

# WRONG — literal that belongs in customer.yaml
customer_name = "lca"

# WRONG — literal that belongs in policy_defaults.cue
mongo_version = "16.5.*"
```

---

#### Layer 3: `values_generator.tf`—The Contract

Assembles the `infra_facts` Terraform output: the typed data object that crosses the boundary from Terraform into CUE. Everything CUE needs must be in this object.

Everything in this object must be declared in `schema_infra.cue`.

Rule: Treat `infra_facts` as a typed API. The CUE schema is its OpenAPI spec.

Adding a new value requires changes to both `values_generator.tf` AND `schema_infra.cue`.

```hcl
# values_generator.tf — assembles the contract
infra_facts = {
  deployment_key            = local.deployment_key
  public_fqdn               = local.public_fqdn
  deploy                    = local.deploy           # feature flags
  ffcloud_admin_user_id     = local.ffcloud_admin_user_id
  fitconnect_feature_flags  = local.fitconnect_feature_flags
  cert_manager_host_network = local.cert_manager_host_network
  # ... all fields that CUE needs
}
```

---

#### Layer 4: `cue/schema_infra.cue`—Type Boundary

Declares every field that Terraform passes to CUE. Purely structural—no values, only types. This is the contract definition; the CUE validator enforces it.

Owns:

- Type declarations for all `infra_facts` fields
- Default values for fields that Terraform always provides (e.g., `bool | *false`)
- Optional markers (`?`) for fields that may be absent

Does NOT own:

- Any concrete values
- Any platform configuration
- Any transformation logic

```cue
// CORRECT — pure type contract
#InfraFacts: {
    deployment_key:            string
    cert_manager_host_network: bool | *false
    ffcloud_admin_user_id:     string | *""
    fitconnect_feature_flags: {
        export_to_s3?:          bool
        omop_and_export_to_s3?: bool
    } | *{}
}

// WRONG — value in the schema
#InfraFacts: {
    auth0_domain: string | *"fitfile-prod.eu.auth0.com"  // NO — belongs in policy
}
```

---

#### Layer 5: `cue/policy_defaults.cue`—Platform Constants

The only place platform-wide constants live. Values here are the same for every customer deployment. This is the CUE equivalent of a platform config file.

Owns:

- Auth0 domain and audience (platform-wide)
- Image pull secret name
- Helm chart version constraints (mongo, etc.)
- Persistence sizes
- Probe timings (initialDelaySeconds, timeoutSeconds)
- Frontend feature flags and env vars (platform defaults)
- ArgoCD target revision
- Registry URL (`fitfileregistry.azurecr.io`)
- GitLab group URL (`https://gitlab.com/fitfile`)
- TFC organisation name and workspace names

Does NOT own:

- Customer-specific values (those come via `infra.*`)
- Transformation logic (that belongs in `render_fitfile.cue`)
- Infrastructure-derived values (those come via `infra.*`)

```cue
// CORRECT — platform constant
platform: #PlatformPolicy & {
    auth0: domain: "fitfile-prod.eu.auth0.com"
    fitconnect: probe: { initialDelaySeconds: 120, timeoutSeconds: 60 }
    platform: registry_url: "fitfileregistry.azurecr.io"
}

// WRONG — customer value sneaking into platform policy
platform: #PlatformPolicy & {
    ffcloud_admin_user: "auth0|633adad9991af2b9ec7446c1"  // NO — customer.yaml
}
```

---

#### Layer 6: `cue/render_fitfile.cue`—Pure Transformation

Maps `infra.*` (customer facts) and `policy.*` (platform constants) to the Helm values YAML structure. Contains zero literals. Every value is either read from `infra` or from `policy`.

Owns:

- Structural mapping from flat facts to nested Helm values
- Conditional logic (`if infra.deploy.monitoring { … }`)
- YAML key naming conventions

Does NOT own:

- Any string or number literals
- Any platform configuration (read from `policy.*`)
- Any customer-specific values (read from `infra.*`)

```cue
// CORRECT — reads from policy and infra, no literals
certManager: webhook: {
    hostNetwork: infra.cert_manager_host_network  // from infra_facts
    securePort:  10260                             // this should be in policy!
}

frontend: {
    features: policy.frontend.features             // from policy_defaults
    env:      policy.frontend.env                  // from policy_defaults
}

// CORRECT — conditional on infra data
if infra.ffcloud_admin_user_id != "" {
    appConfig: defaultOrganisationAdminUserId: infra.ffcloud_admin_user_id
}

// WRONG — literal in the render layer
certManager: webhook: hostNetwork: true           // should be infra.cert_manager_host_network
ffcloud: appConfig: defaultOrganisationAdminUserId: "auth0|633adad9991af2b9ec7446c1"
```

---

#### Layer 7: `templates/jumpbox.tftpl`—Jumpbox Bootstrap

A Terraform templatefile that generates `generated/genjump.tf` via `jumpbox_generator.tf` during `terraform apply`. The template receives all dynamic values as explicit named variables—nothing is hardcoded inside the template body except formatting.

Key escaping rules inside a `.tftpl` file:

- `${variable}` → templatefile substitution (dynamic value from Terraform)
- `$${hcl_expr}` → produces `${hcl_expr}` in the output (HCL interpolation in generated file)
- `$$argocd_ref` → produces `$argocd_ref` in the output (ArgoCD `$values` reference syntax)
- `%{ for x in list ~}` / `%{ endfor ~}` → templatefile for-loop, `~` strips whitespace

The namespace list is computed by Terraform from `local.deploy` feature flags (in `jumpbox_generator.tf`), not hardcoded—so it automatically contracts when features are disabled for dev deployments.

---

### Type Safety: How It Works

CUE enforces the contract at the `infra_facts` boundary. The flow:

```
terraform output -json infra_facts | jq -c '.'
          ↓
cue vet -c ./cue/*.cue -t "infra=$INFRA_JSON"
          ↓ FAILS if:
          - required field is missing
          - field has wrong type
          - field value violates a constraint
          ↓ PASSES
cue export ... -e values --out yaml > generated/values.yaml
```

The schema is the test. If `cue vet` passes, the downstream Helm deployment will receive well-formed, complete values. You never need to debug a half-rendered `values.yaml`.

---

### Adding a New Customer

The complete checklist for onboarding a new customer:

1. Copy an existing deployment repo (e.g. copy LCA-DP to `NEWCUSTOMER-DP`)
2. Edit `config/customer.yaml`—change name, env, region, id, vnet_address_space, and any app-level overrides
3. Run `make generate-providers`—regenerates `providers.tf` with the new TFC workspace name
4. Run `terraform init && terraform apply`—provisions all infrastructure and generates `genjump.tf`
5. Run `make generate-values`—generates `values.yaml` from CUE
6. Commit and push—ArgoCD picks up the values, Jumpbox Terraform runs

You do not touch:

- `locals.tf`—all derivations are already generic
- `main.tf`—modules are already parameterised
- Any CUE render file—values come through the data pipeline
- `policy_defaults.cue`—platform constants are not customer-specific

---

### Anti-Patterns to Reject

When reviewing or writing code in this system, reject the following:

#### ❌ Literals in the Render Layer

```cue
// render_fitfile.cue — WRONG
argocdApp: targetRevision: "master"           // belongs in policy_defaults.cue
ffcloud: appConfig: someUserId: "auth0|abc"   // belongs in customer.yaml
```

#### ❌ Customer Data in Platform Policy

```cue
// policy_defaults.cue — WRONG
platform: specificCustomerFlag: true           // belongs in customer.yaml
```

#### ❌ Values in the CUE Schema

```cue
// schema_infra.cue — WRONG
#InfraFacts: {
    registry: string | *"fitfileregistry.azurecr.io"  // belongs in policy_defaults.cue
}
```

#### ❌ Hardcoded Values in Terraform that Belong in customer.yaml

```hcl
// locals.tf — WRONG
hub_group = "nwsde"  // fine as a legacy LCA-specific constant, but for new customers
                     // this should come from customer.yaml
```

#### ❌ Generating Structured Output (Terraform/YAML) as Raw Strings in CUE

```cue
// WRONG — CUE generating HCL as a multiline string
content: """
  resource "kubernetes_namespace" "deployment" {
    metadata { name = "\(infra.deployment_key)" }
  }
"""
```

Use `templatefile()` in Terraform with a `.tftpl` file instead. CUE's string interpolation has no syntax checking for the target language, no editor support, and the escaping is a maintenance hazard.

#### ❌ Static Lists that Should React to Feature Flags

```cue
// WRONG — static list of namespaces ignoring deploy.monitoring = false
image_pull_secret_namespaces = ["argo", "argocd", "monitoring", ...]
```

Compute conditional lists in Terraform from `local.deploy.*` and pass them as template variables. Then the list shrinks automatically for dev/partial deployments.

#### ❌ Broken CUE String Concatenation

```cue
// WRONG — + concatenation puts the expression literally into the output
text: "prefix" + _key + "suffix"

// CORRECT — \(expr) interpolation resolves at evaluation time
text: "prefix\(_key)suffix"
```

---

### The `#VSO.map` Helper Pattern

When generating Vault Secrets Operator (VSO) template strings in CUE, use the `#VSO.map` helper with CUE's `\(expr)` interpolation:

```cue
// templates_vault.cue
#VSO: {
    map: {
        _key: string
        text: "{{`{{get .Secrets \"\(_key)\"}}`}}"
    }
}

// Usage in render_fitfile.cue
username: #VSO.map & {_key: "postgresql_username"}
// Produces: text: '{{`{{get .Secrets "postgresql_username"}}`}}'
```

The `{{` `}}` are Helm template delimiters. The backtick-quoted inner `{{…}}` is Helm's raw string syntax (prevents double-evaluation). CUE's `\(_key)` substitutes the concrete key name at CUE evaluation time.

---

### What `infra_facts` Contains (Contract Summary)

```
customer identity:    customer_short_name, deployment_key, public_fqdn, fit_connect_code
feature flags:        deploy.{certManager, spicedb, persistence, monitoring, ...}
network:              ingress_ip
cluster:              oidc_issuer_url
repos:                values_repo_url, chart_repo_url
secrets config:       vault_address
data stores:          s3_export.{enabled, vault_path, secret_name}
cert config:          cert_manager_host_network, pki_issuer.{enabled, ...}
node config:          node_placement.{nodeSelector, tolerations}
multi-node:           ffcloud_service_accounts, fitconnect_hosts
app overrides:        ffcloud_admin_user_id, fitconnect_feature_flags
```

All of these flow from `customer.yaml` → `locals.tf` → `values_generator.tf`.

None of them originate in CUE.

---

### File Ownership Quick Reference

| Where to put it | What goes there |
|---|---|
| `config/customer.yaml` | Customer name, env, region, CIDR, any per-customer app overrides |
| `locals.tf` | Derivations, CIDR math, naming conventions, feature flag defaults |
| `values_generator.tf` | Assembles `infra_facts`; one entry per field in schema |
| `cue/schema_infra.cue` | Type declarations only; mirrors `infra_facts` exactly |
| `cue/policy_defaults.cue` | Platform constants; same value for all customers |
| `cue/render_fitfile.cue` | Structural transformation; reads `infra.*` and `policy.*` only |
| `cue/templates_vault.cue` | Reusable CUE helpers (`#VSO.map`, `#VaultTemplates`) |
| `templates/jumpbox.tftpl` | Jumpbox Terraform template; receives all values as `${variables}` |
| `jumpbox_generator.tf` | Computes namespace list from deploy flags; calls `templatefile()` |
| `templates/providers.tftpl` | TFC workspace name template; only varies by deployment_key |
