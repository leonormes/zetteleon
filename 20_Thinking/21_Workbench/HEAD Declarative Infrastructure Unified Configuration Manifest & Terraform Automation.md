---
captured: "2026-03-07T16:55:07+00:00 2026-03-07T16:55:07+00:00"
created: 2026-03-07T16:55:08+00:00
modified: 2026-03-14T11:10:41+00:00
source: "https://claude.ai/chat/0cfaf733-afd5-4ef0-8349-8d24e3be7cd5"
status: "processing"
tags: ["input"]
title: HEAD Declarative Infrastructure Unified Configuration Manifest & Terraform Automation
type: "head"
---

## Raw Output / Content

\## SYSTEM ROLE: Principal Site Reliability Engineer (Infrastructure-as-Code Specialist) You are an expert in GitOps, Declarative Infrastructure, and System Bootstrapping. You specialize in converting manual, error-prone sysadmin tasks into idempotent, data-driven automation. Your primary tools are Terraform/OpenTofu, Helm, and the native APIs of HCP Vault and Grafana. ## THE USER CONTEXT The user is a DevOps Engineer migrating from an "Imperative/Manual" workflow to a "Data-Centric/Declarative" workflow. They are managing a Kubernetes-based cluster environment. They have "Contextual Baggage" from manual configurations in Grafana and HCP Vault and need to eliminate human error through schema-driven generation. ## PEDAGOGICAL/OPERATIONAL CONSTRAINTS 1. \*\*Declarative Supremacy\*\*: Every suggestion must be driven by a central configuration file (YAML/JSON). Do not suggest "clicking" or "one-off CLI commands." 2. \*\*Idempotency Check\*\*: Before providing code, verify if the resource can be re-applied without destroying state. 3. \*\*Schema Validation\*\*: You must insist on a defined schema for the "input data." If the user provides messy data, your first task is to propose a structured YAML schema that covers Providers, Auth, and Observability. 4. \*\*Provider Mapping\*\*: Map "Config Keys" directly to "Resource Arguments" (e.g., `config.vault.seal_type` -> `vault_generic_secret`). ## IMMEDIATE GOAL Analyze the user's current 'manual steps' for Grafana and HCP Vault. Design a unified Configuration Manifest schema and the corresponding Terraform/Logic blocks to automate the instantiation of these services based on that manifest.

---

## Declarative Infrastructure: Unified Configuration Manifest & Terraform Automation

Before writing a single resource block, we need to establish truth. The manifest comes first—Terraform is just a rendering engine for it. Let me walk through the full design, from schema to execution.

---

## Phase 1: Threat Model—What Manual Steps Are We Eliminating?

The typical "contextual baggage" in this stack looks like this:

| Manual Step | Failure Mode | Declarative Fix |
| --- | --- | --- |
| Clicking "Add Data Source" in Grafana UI | Config lost on pod restart | `grafana_data_source` resource |
| `vault operator init` then copy-paste root token | Root token in Slack/Notepad | HCP Vault auto-unseal + Terraform output to K8s secret |
| Hand-editing `vault policy write` | Policy drift across envs | `vault_policy` from `.hcl` template files |
| Creating Grafana folders/teams manually | No audit trail | `grafana_folder`, `grafana_team` resources |
| Manually adding K8s auth method to Vault | Forgotten in DR scenarios | `vault_auth_backend` + `vault_kubernetes_auth_backend_config` |

---

## Phase 2: The Unified Configuration Manifest Schema

This is the single source of truth. Everything else is generated from it.

yaml

```yaml
# config/manifest.yaml
# =============================================================================
# UNIFIED INFRASTRUCTURE MANIFEST
# Schema Version: 1.0.0
# All Terraform modules read from this file. No resource is created
# without a corresponding entry here.
# =============================================================================

schema_version: "1.0.0"
environment: production          # drives naming conventions & feature flags
cluster_name: "aks-prod-westeu"  # injected into Vault K8s auth & Grafana labels

# =============================================================================
# SECTION 1: VAULT (HCP or Self-Managed)
# =============================================================================
vault:
  mode: "hcp"                    # "hcp" | "self-managed" — gates HCP-specific resources
  address: "https://vault-cluster.vault.hashicorp.cloud:8200"
  namespace: "admin"             # HCP root namespace; child namespaces defined below

  # --- Auth Methods ---
  auth_backends:
    - type: kubernetes
      path: "kubernetes"         # vault_auth_backend.path
      description: "K8s ServiceAccount auth for cluster workloads"
      config:
        kubernetes_host: "https://your-aks-api.example.com:443"
        # token_reviewer_jwt and ca_cert injected at plan time from K8s secrets
        issuer: "https://oidc.prod.azure.com/"

    - type: approle
      path: "approle"
      description: "AppRole auth for CI/CD pipelines"
      config: {}

  # --- Secrets Engines ---
  secrets_engines:
    - type: kv-v2
      path: "secret"
      description: "Application secrets — KV v2"
      options:
        version: "2"

    - type: pki
      path: "pki"
      description: "Internal CA for service-to-service mTLS"
      options:
        max_lease_ttl: "87600h"  # 10 years for root CA

    - type: database
      path: "database"
      description: "Dynamic credentials for PostgreSQL"
      options: {}

  # --- Namespaces (HCP / Enterprise only) ---
  namespaces:
    - name: "platform"
      description: "Platform engineering secrets"
    - name: "app-team-a"
      description: "Namespace for team-a application secrets"

  # --- Policies ---
  policies:
    - name: "app-read-only"
      rules_file: "vault/policies/app-read-only.hcl"  # path relative to repo root

    - name: "ci-pipeline"
      rules_file: "vault/policies/ci-pipeline.hcl"

    - name: "grafana-agent"
      rules_file: "vault/policies/grafana-agent.hcl"

  # --- Roles (K8s Auth) ---
  kubernetes_roles:
    - name: "app-team-a"
      bound_service_account_names: ["app-team-a-sa"]
      bound_service_account_namespaces: ["team-a", "team-a-staging"]
      policies: ["app-read-only"]
      ttl: "1h"
      max_ttl: "24h"

    - name: "grafana"
      bound_service_account_names: ["grafana"]
      bound_service_account_namespaces: ["monitoring"]
      policies: ["grafana-agent"]
      ttl: "1h"
      max_ttl: "4h"

  # --- Static Secrets (seeded, non-sensitive values only) ---
  # Sensitive values come from TF_VAR_ env vars or a bootstrap secret
  seed_secrets:
    - path: "secret/data/platform/cluster-info"
      data:
        cluster_name: "aks-prod-westeu"
        region: "westeurope"
        environment: "production"

# =============================================================================
# SECTION 2: GRAFANA
# =============================================================================
grafana:
  url: "https://grafana.internal.example.com"
  # auth via env var: TF_VAR_grafana_auth

  # --- Organizations ---
  # For Grafana OSS, this is usually just "Main Org."
  # For Grafana Enterprise/Cloud, multiple orgs are meaningful.
  organization:
    name: "Platform Engineering"
    id: 1  # existing org id; use 0 to let Terraform create

  # --- Folders ---
  folders:
    - title: "Platform / SRE"
      uid: "platform-sre"
    - title: "Application Teams / Team-A"
      uid: "app-team-a"
    - title: "Infrastructure / Kubernetes"
      uid: "infra-k8s"

  # --- Data Sources ---
  data_sources:
    - name: "Prometheus-Production"
      type: "prometheus"
      url: "http://kube-prometheus-stack-prometheus.monitoring.svc:9090"
      access: "proxy"
      is_default: true
      uid: "prometheus-prod"
      json_data:
        httpMethod: "POST"
        timeInterval: "30s"

    - name: "Loki-Production"
      type: "loki"
      url: "http://loki-gateway.monitoring.svc:3100"
      access: "proxy"
      uid: "loki-prod"
      json_data:
        maxLines: 5000

    - name: "Vault-Metrics"
      type: "prometheus"
      url: "http://vault.vault.svc:8200/v1/sys/metrics?format=prometheus"
      access: "proxy"
      uid: "vault-metrics"
      with_credentials: true
      json_data:
        httpMethod: "GET"

  # --- Teams ---
  teams:
    - name: "SRE Platform"
      email: "sre@example.com"
      folder_permissions:
        - folder_uid: "platform-sre"
          permission: "Editor"
        - folder_uid: "infra-k8s"
          permission: "Viewer"

    - name: "App Team A"
      email: "team-a@example.com"
      folder_permissions:
        - folder_uid: "app-team-a"
          permission: "Editor"
        - folder_uid: "platform-sre"
          permission: "Viewer"

  # --- Alert Contact Points ---
  contact_points:
    - name: "pagerduty-critical"
      type: "pagerduty"
      settings:
        integrationKey: "${pagerduty_integration_key}"  # resolved from TF var

    - name: "slack-warnings"
      type: "slack"
      settings:
        url: "${slack_webhook_url}"
        channel: "#alerts-warnings"

  # --- Notification Policies ---
  notification_policy:
    contact_point: "pagerduty-critical"
    group_by: ["alertname", "cluster", "namespace"]
    group_wait: "30s"
    group_interval: "5m"
    repeat_interval: "4h"
\`\`\`

---

## Phase 3: Terraform Project Structure
\`\`\`
terraform/
├── main.tf                  # Root orchestrator — reads manifest, calls modules
├── variables.tf             # Sensitive vars only (tokens, passwords)
├── outputs.tf
├── providers.tf
├── locals.tf                # Manifest parsing & derived locals live here
│
├── modules/
│   ├── vault-config/
│   │   ├── main.tf
│   │   ├── auth.tf          # Auth backends & roles
│   │   ├── engines.tf       # Secrets engines
│   │   ├── policies.tf      # Policy files from HCL templates
│   │   ├── namespaces.tf    # HCP namespaces
│   │   └── variables.tf
│   │
│   └── grafana-config/
│       ├── main.tf
│       ├── datasources.tf
│       ├── folders.tf
│       ├── teams.tf
│       ├── alerting.tf
│       └── variables.tf
│
├── vault/
│   └── policies/
│       ├── app-read-only.hcl
│       ├── ci-pipeline.hcl
│       └── grafana-agent.hcl
│
└── config/
    └── manifest.yaml        # ← THE SINGLE SOURCE OF TRUTH
```

---

## Phase 4: Root Module—Manifest Parsing

hcl

```
# terraform/locals.tf
# =============================================================================
# MANIFEST LOADER
# This is the single point of ingestion. Everything else references \`local.cfg\`
# =============================================================================

locals {
  # Decode the manifest once; all modules consume this object
  cfg = yamldecode(file("${path.module}/config/manifest.yaml"))

  # Convenience aliases with type-safe defaults
  vault_cfg   = local.cfg.vault
  grafana_cfg = local.cfg.grafana
  environment = local.cfg.environment
  cluster     = local.cfg.cluster_name

  # Pre-process: index slices into maps for for_each (avoids count index drift)
  vault_auth_backends_map    = { for b in local.vault_cfg.auth_backends : b.path => b }
  vault_secrets_engines_map  = { for e in local.vault_cfg.secrets_engines : e.path => e }
  vault_policies_map         = { for p in local.vault_cfg.policies : p.name => p }
  vault_k8s_roles_map        = { for r in local.vault_cfg.kubernetes_roles : r.name => r }
  vault_namespaces_map       = { for n in local.vault_cfg.namespaces : n.name => n }
  vault_seed_secrets_map     = { for s in local.vault_cfg.seed_secrets : s.path => s }

  grafana_folders_map        = { for f in local.grafana_cfg.folders : f.uid => f }
  grafana_datasources_map    = { for d in local.grafana_cfg.data_sources : d.uid => d }
  grafana_teams_map          = { for t in local.grafana_cfg.teams : t.name => t }
  grafana_contact_points_map = { for c in local.grafana_cfg.contact_points : c.name => c }
}
```

---

## Phase 5: Vault Module—Full Implementation

hcl

```
# terraform/modules/vault-config/auth.tf
# =============================================================================
# IDEMPOTENCY NOTE: vault_auth_backend uses \`path\` as the unique identifier.
# Re-applying will update config, NOT destroy and recreate the backend.
# vault_kubernetes_auth_backend_role is similarly path+name keyed.
# =============================================================================

# ── Auth Backends ─────────────────────────────────────────────────────────────
resource "vault_auth_backend" "this" {
  for_each = var.auth_backends_map

  type        = each.value.type
  path        = each.value.path
  description = each.value.description
}

# ── Kubernetes Auth Backend Configuration ─────────────────────────────────────
# Only runs for entries where type == "kubernetes"
resource "vault_kubernetes_auth_backend_config" "this" {
  for_each = {
    for k, v in var.auth_backends_map : k => v
    if v.type == "kubernetes"
  }

  backend            = vault_auth_backend.this[each.key].path
  kubernetes_host    = each.value.config.kubernetes_host
  kubernetes_ca_cert = var.kubernetes_ca_cert   # injected from K8s secret at plan time
  token_reviewer_jwt = var.token_reviewer_jwt   # injected from K8s secret at plan time
  issuer             = try(each.value.config.issuer, null)
}

# ── Kubernetes Auth Roles ──────────────────────────────────────────────────────
resource "vault_kubernetes_auth_backend_role" "this" {
  for_each = var.k8s_roles_map

  backend                          = vault_auth_backend.this["kubernetes"].path
  role_name                        = each.key
  bound_service_account_names      = each.value.bound_service_account_names
  bound_service_account_namespaces = each.value.bound_service_account_namespaces
  token_policies                   = each.value.policies
  token_ttl                        = each.value.ttl
  token_max_ttl                    = each.value.max_ttl

  # Explicit dependency: role cannot exist before its backend is configured
  depends_on = [vault_kubernetes_auth_backend_config.this]
}
```

---

## Phase 6: Grafana Module—Full Implementation

hcl

```
# terraform/modules/grafana-config/datasources.tf
# =============================================================================
# IDEMPOTENCY NOTE: grafana_data_source is keyed by \`uid\`.
# Always set uid in the manifest. Without it, every plan will show drift
# because Grafana auto-generates one that Terraform can't predict.
# =============================================================================

resource "grafana_data_source" "this" {
  for_each = var.datasources_map

  name       = each.value.name
  type       = each.value.type
  url        = each.value.url
  access_mode = try(each.value.access, "proxy")
  is_default = try(each.value.is_default, false)
  uid        = each.key

  # Dynamically serialize json_data from manifest
  # This handles any future datasource types without code changes
  json_data_encoded = try(
    jsonencode(each.value.json_data),
    jsonencode({})
  )

  # Sensitive fields — injected via TF vars, never in manifest
  secure_json_data_encoded = try(
    jsonencode({
      basicAuthPassword = var.datasource_passwords[each.key]
    }),
    jsonencode({})
  )
}
```

hcl

```
# terraform/modules/grafana-config/teams.tf

resource "grafana_team" "this" {
  for_each = var.teams_map

  name  = each.key
  email = try(each.value.email, "")
}

# ── Folder Permissions per Team ───────────────────────────────────────────────
# Flattens the nested team -> folder_permissions structure into a flat map
# suitable for for_each.

locals {
  # Produces entries like:
  # "SRE Platform__platform-sre" = { team = "SRE Platform", folder_uid = "platform-sre", permission = "Editor" }
  team_folder_permissions = merge([
    for team_name, team in var.teams_map : {
      for perm in try(team.folder_permissions, []) :
      "${team_name}__${perm.folder_uid}" => {
        team_name  = team_name
        folder_uid = perm.folder_uid
        permission = perm.permission
      }
    }
  ]...)
}

resource "grafana_folder_permission" "team" {
  for_each = local.team_folder_permissions

  folder_uid = each.value.folder_uid

  permissions {
    team_id    = grafana_team.this[each.value.team_name].id
    permission = each.value.permission
  }
}
```

---

## Phase 7: Root main.tf—Wiring It Together

hcl

```
# terraform/main.tf

module "vault" {
  source = "./modules/vault-config"

  is_hcp               = local.vault_cfg.mode == "hcp"
  auth_backends_map    = local.vault_auth_backends_map
  secrets_engines_map  = local.vault_secrets_engines_map
  policies_map         = local.vault_policies_map
  k8s_roles_map        = local.vault_k8s_roles_map
  namespaces_map       = local.vault_namespaces_map
  seed_secrets_map     = local.vault_seed_secrets_map

  # Sensitive — sourced from K8s secret or CI secret store at plan time
  kubernetes_ca_cert   = var.kubernetes_ca_cert
  token_reviewer_jwt   = var.token_reviewer_jwt
}

module "grafana" {
  source = "./modules/grafana-config"

  folders_map          = local.grafana_folders_map
  datasources_map      = local.grafana_datasources_map
  teams_map            = local.grafana_teams_map
  contact_points_map   = local.grafana_contact_points_map
  notification_policy  = local.grafana_cfg.notification_policy

  # Sensitive values — never in manifest
  datasource_passwords      = var.grafana_datasource_passwords
  sensitive_alert_settings  = var.grafana_alert_sensitive_settings
}
\`\`\`

---

## Phase 8: The Idempotency & Drift Detection Contract

This is the operational guarantee the schema buys you:
\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│              IDEMPOTENCY CONTRACT PER RESOURCE TYPE             │
├──────────────────────────────┬──────────────┬───────────────────┤
│ Resource                     │ Stable Key   │ Update Behavior   │
├──────────────────────────────┼──────────────┼───────────────────┤
│ vault_auth_backend           │ path         │ In-place update   │
│ vault_kubernetes_auth_*      │ path+role    │ In-place update   │
│ vault_policy                 │ name         │ In-place update   │
│ vault_mount                  │ path         │ In-place update   │
│ vault_namespace              │ path         │ In-place update   │
│ vault_kv_secret_v2           │ mount+name   │ New version added │
│ grafana_folder               │ uid (manual) │ In-place update   │
│ grafana_data_source          │ uid (manual) │ In-place update   │
│ grafana_team                 │ name         │ In-place update   │
│ grafana_contact_point        │ name         │ In-place update   │
│ grafana_notification_policy  │ singleton    │ In-place update   │
└──────────────────────────────┴──────────────┴───────────────────┘

⚠  DANGER ZONES:
   - Removing a vault_mount entry WILL destroy the engine + all secrets.
     Protect with \`lifecycle { prevent_destroy = true }\` on stateful mounts.
   - Changing grafana_folder uid = destroy + recreate (breaks dashboard refs).
     Never change a uid once set. Treat it as an immutable primary key.
```

---

## Phase 9: CI/CD Execution Pipeline

yaml

```yaml
# .github/workflows/terraform-platform.yaml

name: Platform Infrastructure
on:
  push:
    paths: ["terraform/", "config/manifest.yaml", "vault/policies/"]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Schema validation BEFORE any Terraform runs
      - name: Validate manifest schema
        run: |
          pip install pyyaml jsonschema
          python scripts/validate_manifest.py config/manifest.yaml

      - name: Terraform Init
        run: terraform -chdir=terraform init

      - name: Terraform Validate
        run: terraform -chdir=terraform validate

      - name: Terraform Plan
        env:
          VAULT_TOKEN: ${{ secrets.VAULT_TOKEN }}
          TF_VAR_grafana_auth: ${{ secrets.GRAFANA_AUTH }}
          TF_VAR_kubernetes_ca_cert: ${{ secrets.K8S_CA_CERT }}
          TF_VAR_token_reviewer_jwt: ${{ secrets.K8S_REVIEWER_JWT }}
        run: terraform -chdir=terraform plan -out=tfplan

  apply:
    needs: validate
    if: github.ref == 'refs/heads/main'
    environment: production   # requires manual approval in GitHub
    runs-on: ubuntu-latest
    steps:
      - name: Terraform Apply
        run: terraform -chdir=terraform apply tfplan
\`\`\`

---

## The Mental Model: How Changes Flow
\`\`\`
Developer changes manifest.yaml
          │
          ▼
  CI validates YAML schema          ← catches typos, wrong types
          │
          ▼
  terraform plan generates diff     ← shows exactly what changes
          │
          ▼
  PR review of plan output          ← human reviews declarative diff
          │
          ▼
  terraform apply on merge          ← Vault + Grafana updated atomically
          │
          ▼
  State stored in Azure Blob        ← drift detection on next run
```

The key architectural win here: the manifest is the only thing engineers ever edit. Adding a new Vault Kubernetes role for a new team is a three-line YAML addition under `kubernetes_roles`. Adding a new Grafana data source is five lines under `data_sources`. No CLI, no clicking, no tribal knowledge—just a diff.

The next logical step would be implementing the JSON Schema validator (`scripts/validate_manifest.py`) so malformed manifests fail in CI before Terraform ever sees them—want me to build that out?
