---
aliases: []

confidence:
created: 2025-10-27T21:22:10Z
epistemic:
last_reviewed:
modified: 2025-11-03T10:32:19Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [sdlc]
title: config rfc
type:
uid:
updated:
version:
---

**Formulating RFC-style document**

Drafting a structured RFC document to formalize ideas around config separation in Terraform IaC, including safety, automation, validation, and examples with Terraform, HCL, and more.

Below is a self‑contained, “RFC‑style” document that formalizes your idea into an implementable, testable pattern for Terraform-based platforms. It emphasizes minimal input, deterministic derivation, separation of configuration from code, strong validation, and change‑evidence—so the builder code can be validated once and then repeatedly trusted.

## RFC-00XX: Deterministic Config Derivation for Terraform (DCD-TF)

**Status:** Draft
**Authors:** *You (Leon Ormes)*
**Reviewers:** *TBD (e.g., Platform Team)*
**Created:** 2025‑10‑27
**Target Release:** *TBD*
**Last Updated:** 2025‑10‑27

### 0. Abstract

This RFC proposes a **Deterministic Config Derivation (DCD)** pattern for Terraform-based infrastructure. The goal is to **minimize the amount of human-supplied configuration**, and instead **derive** the majority of environmentand naming-specific values from a small, validated **Seed Config** (e.g., `base_domain`, `env`, `region`, `service_id`, `tenant`). The derivation logic, implemented as a **Builder**, produces consistent DNS hostnames, resource names, tags/labels, certificate SANs, and other infra identifiers.

The approach aims to make config changes **safe**, **change‑evident**, and **automated** while reducing fragility caused by typos and hand-crafted strings. The Builder is validated via tests and policy checks so that the “surface area” of human input is small, declarative, and resilient.

---

### 1. Problem Statement

Infrastructure deployments often fail due to brittle configuration:

- Single-character mistakes in DNS names, ARNs, role names, or secret values can cause full system outages.
- Configuration lives intermingled with code, growing organically and inconsistently across services and clouds.
- Secrets are sometimes embedded in plans or repos, or they change without an audit trail.
- Environments diverge because of manual overrides and inconsistent naming schemes.

We need an approach where:

1. The **human input** is minimized and **strongly validated**.
2. Most values are **derived deterministically** from a small Seed Config.
3. **Secrets** are referenced safely and excluded from state/repo while still being **change‑evident**.
4. **Policies** enforce correctness (pre-commit, CI, and policy-as-code).
5. **DNS and naming** follow a protocol that’s derived from the Seed, not hand-written.

---

### 2. Goals

- **Minimal Inputs:** A compact **Seed Config** (e.g., `org`, `tenant`, `env`, `region`, `service_id`, `base_domain`) from which most infrastructure values are derived.
- **Determinism:** Reproducible string generation (names, tags, DNS labels), including truncation and stable hash suffixing.
- **Separation:** Configuration independent from Terraform logic; modules consume derived values, not arbitrary strings.
- **Safety & Evidence:** Secrets never committed or stored in Terraform state; changes are visible via checksums and plan diffs.
- **Policy & Testing:** Schema validation, OPA/Conftest policies, static analysis, unit/property tests for the Builder, and plan gates in CI.

#### Non‑Goals

- A universal naming scheme for every provider/resource (we define rules and escape hatches; edge cases may still need overrides).
- Replacing GitOps or your existing CI/CD—this RFC integrates with them.

---

### 3. Terminology

- **Seed Config:** Minimal, typed inputs supplied by humans or a higher-level orchestrator.
- **Builder:** Code + Terraform locals that deterministically derive all secondary values.
- **Derivation Grammar:** Formal rules for generating identifiers (e.g., hostnames) from Seed fields.
- **Change‑Evident:** Changes show up in PR diffs or plan artifacts (e.g., checksum updates), without leaking secrets.

---

### 4. High-Level Design

#### 4.1 Seed Config (minimal, typed)

Canonical fields (examples; your org may tune these):

```yaml
org:           "acme"          # stable organization slug
tenant:        "core"          # business/line-of-service grouping
env:           "prod"          # dev|test|stage|prod|ephemeral-<id>
region:        "eu-west-1"     # cloud region id
service_id:    "payments-api"  # workload identifier
tier:          "app"           # app|db|cache|frontend|backend etc.
base_domain:   "acme.example"  # company apex or subdomain root
zone_type:     "public"        # public|private (DNS split-horizon)
```

**Optional:** `is_internal`, `compliance_tier`, `data_classification`, `az_count`, `shard`, `cluster_id`, etc.

#### 4.2 Builder Responsibilities

1. **Name Derivation**
   - Resource names, tags/labels, role names, KMS aliases, bucket/container names
   - Deterministic truncation and hashing to respect provider limits
2. **DNS Derivation**
   - FQDNs for services and tiers
   - Split-horizon DNS (public/private zones) and zone attachment
   - Cert SANs for ACME/ACM/Key Vault issuance
3. **Secret References**
   - Use references to external secret managers (Vault, AWS Secrets Manager, Azure Key Vault)
   - Compute change‑evident checksums for PRs without revealing values
4. **Validation & Policies**
   - JSON Schema/OPA validation in pre-commit & CI
   - Enforce allowed characters, length, reserved words, and disallowed mutations in prod
5. **Outputs for Modules**
   - A compact map of derived values that Terraform modules consume

#### 4.3 Terraform Integration

- **Root Module** takes Seed Config; **locals** compute derived values via the Builder.
- **Child Modules** accept a single map `derived` and reference fields internally.
- **No Raw Strings:** Modules should avoid re-deriving names; consume `derived` consistently.
- **Provider-Specific Layers:** If multi-cloud, keep providers in submodules but preserve the same input contract.

---

### 5. Detailed Specification

#### 5.1 Naming Grammar (BNF-like)

We define a canonical **Resource ID** grammar and a **Hostname** grammar.

**Resource ID (generic):**

```sh
resource-id    := segment { "-" segment } [ "-" hash-suffix ]
segment        := [a-z0-9]{1,24}    ; normalized, kebab-case
hash-suffix    := [a-z0-9]{6}       ; stable hash to avoid collisions
```

Construction rule (before truncation/rehash):

```sh
resource-id := org "-" tenant "-" env "-" region "-" service_id [ "-" tier ]
```

**Hostname (DNS label-safe):**

```sh
host-label    := [a-z0-9] ( [a-z0-9-]* [a-z0-9] )?
hostname      := svc "." tier "." env "." region "." base_domain
```

**Limits & Normalization Rules:**

- Lowercase alphanumerics and hyphens only.
- Collapse consecutive hyphens, strip leading/trailing hyphens.
- Per provider length caps:
  - DNS label ≤ 63 chars; full hostname ≤ 253 chars.
  - S3 buckets ≤ 63 chars; Azure Storage containers ≤ 63; IAM role names ≤ 64; Key aliases ≤ 256; etc.
- **Truncation policy:** If exceeded, truncate from left-to-right at inflection points, then append `-` + `fnv1a_32(seed)[:6]`.

#### 5.2 Deterministic Hash

Use a stable, fast hash (e.g., **FNV‑1a 32** or **XXH32**) over the **canonical seed string**:

```sh
seed-string := org "|" tenant "|" env "|" region "|" service_id "|" tier "|" base_domain
```

This ensures idempotent shortening with low collision risk. Implementation must be consistent across Builder (TypeScript linter/CLI) and Terraform (`random_id` can’t guarantee stability; use a local function via external data or a small helper binary invoked during generation).

#### 5.3 JSON Schema for Seed Config

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://acme.internal/schemas/dcd-seed.schema.json",
  "title": "DCD Seed Config",
  "type": "object",
  "required": ["org","tenant","env","region","service_id","tier","base_domain","zone_type"],
  "properties": {
    "org":        {"type":"string","pattern":"^[a-z0-9-]{2,24}$"},
    "tenant":     {"type":"string","pattern":"^[a-z0-9-]{2,24}$"},
    "env":        {"type":"string","pattern":"^(dev|test|stage|prod|ephemeral-[a-z0-9-]+)$"},
    "region":     {"type":"string","minLength":2,"maxLength":32},
    "service_id": {"type":"string","pattern":"^[a-z0-9-]{2,32}$"},
    "tier":       {"type":"string","enum":["app","api","db","cache","frontend","backend","queue","batch"]},
    "base_domain":{"type":"string","pattern":"^[a-z0-9.-]+$"},
    "zone_type":  {"type":"string","enum":["public","private"]},
    "is_internal":{"type":"boolean","default":false}
  },
  "additionalProperties": false
}
```

#### 5.4 Terraform Module Interface

`modules/dcd` (Builder module) – variables:

```hcl
variable "seed" {
  type = object({
    org         = string
    tenant      = string
    env         = string
    region      = string
    service_id  = string
    tier        = string
    base_domain = string
    zone_type   = string # "public" | "private"
    is_internal = optional(bool, false)
  })
}
```

**Derived outputs (partial):**

```hcl
output "derived" {
  value = {
    ns                   = "${local.org}-${local.tenant}-${local.env}-${local.region}-${local.service_id}-${local.tier}"
    name                 = local.resource_name              # post-truncation + hash
    tags = {
      org       = var.seed.org
      tenant    = var.seed.tenant
      env       = var.seed.env
      region    = var.seed.region
      service   = var.seed.service_id
      tier      = var.seed.tier
      owner     = "team-${var.seed.tenant}"
      managedBy = "terraform"
      schema    = "dcd/v1"
    }
    dns = {
      zone_fqdn  = "${var.seed.base_domain}."
      host_fqdn  = "${local.svc}.${var.seed.tier}.${var.seed.env}.${var.seed.region}.${var.seed.base_domain}."
      cert_sans  = [
        "${local.svc}.${var.seed.tier}.${var.seed.env}.${var.seed.region}.${var.seed.base_domain}",
        "${local.svc}.${var.seed.env}.${var.seed.region}.${var.seed.base_domain}"
      ]
      zone_type  = var.seed.zone_type
    }
    storage = {
      logs_bucket = local.logs_bucket_name
      app_bucket  = local.app_bucket_name
    }
    iam = {
      role_name   = local.iam_role_name
      policy_name = local.policy_name
    }
    checkpoints = {
      builder_version = "dcd-tf/1.0.0"
      seed_checksum   = local.seed_checksum # hash of canonical seed-string
    }
  }
}
```

**Usage in a workload module:**

```hcl
module "dcd" {
  source = "../modules/dcd"
  seed   = var.seed
}

module "service_dns" {
  source = "../modules/dns"
  derived = module.dcd.derived
}

module "service_runtime" {
  source  = "../modules/runtime-aws-eks" # or az-aks/others
  derived = module.dcd.derived
  secrets = {
    db_uri = data.aws_secretsmanager_secret_version.db.secret_string
  }
}
```

#### 5.5 DNS Hostnaming Service

- **Protocol:** `svc.tier.env.region.base_domain`
- **Split-Horizon:** If `zone_type == "private"`, create an internal zone (e.g., Route 53 Private Hosted Zone / Azure Private DNS); otherwise public zone.
- **Records:** Provide A/AAAA (or ALIAS) for LBs, CNAMEs for services, and optionally wildcard `*.tier.env.region.base_domain` for dynamic sub-services.
- **Certificates:** Issue via ACM/Let’s Encrypt/Key Vault using `cert_sans` from `derived`, with DNS-01 validation automated through the same zone.
- **TTL Defaults:** 60s for dynamic endpoints; 300s for stable edges (configurable).

#### 5.6 Secrets Handling (Change‑Evident, Safe)

- **Storage:** External secrets only
  - AWS: Secrets Manager / SSM Parameter Store
  - Azure: Key Vault
  - (Optionally) Vault
- **In Terraform:** Use data sources to read references (not values) at apply-time; **avoid** storing secret values in state.
- **PR Evidence:** Store **HMAC/SHA256 checksums** of secret values (or versions) in a generated manifest (e.g., `.dcd/manifest.json`) so PRs show that a secret changed without revealing content.
- **Encryption at Rest:** Use KMS/Key Vault keys with clear key alias conventions derived from Seed.
- **No Secrets in Repo:** Enforce via pre-commit secret scanners (e.g., `gitleaks`) and CI.

#### 5.7 Policy & Validation

- **Pre-commit:** JSON schema lint of Seed; `terraform fmt/validate`; `tflint`; `trivy iac`/`checkov`; `conftest` (OPA) for org policies; `gitleaks`.
- **CI Gates:** Run full plan; attach plan file to PR; block on policy violations; require signed commits.
- **Prod Safety:** Disallow destructive changes in `env == prod` without a `break-glass` label and approval.

---

### 6. Reference Implementation (Sketch)

#### 6.1 Directory Layout

```sh
infra/
  seeds/
    payments-api.prod.eu-west-1.yaml
  modules/
    dcd/                  # builder impl (locals)
    dns/                  # provider-agnostic DNS module
    runtime-aws-eks/
    runtime-az-aks/
  stacks/
    aws-prod/
      main.tf
      versions.tf
      providers.tf
      variables.tf
      outputs.tf
  tools/
    cdctl/                # TypeScript CLI for schema validation + preview
    schemas/
      dcd-seed.schema.json
  .pre-commit-config.yaml
  .tflint.hcl
  .terraform.lock.hcl
```

#### 6.2 Terraform Locals (Builder Core excerpt)

```hcl
locals {
  canon_seed = join("|", [
    lower(var.seed.org),
    lower(var.seed.tenant),
    lower(var.seed.env),
    lower(var.seed.region),
    lower(var.seed.service_id),
    lower(var.seed.tier),
    lower(var.seed.base_domain)
  ])

  seed_checksum = sha256(local.canon_seed) # plan-visible, not secret

  # raw name before enforcement
  raw_name = join("-", [
    var.seed.org, var.seed.tenant, var.seed.env, var.seed.region, var.seed.service_id, var.seed.tier
  ])

  # Enforce 63-char typical limit with stable hash suffix
  name_hash  = substr(local.seed_checksum, 0, 6)
  resource_name = length(local.raw_name) <= 63 ? lower(local.raw_name) :
                  lower(substr(local.raw_name, 0, 63 - 1 - 6)) + "-" + local.name_hash

  svc = replace(var.seed.service_id, "/[^a-z0-9-]/", "")
  host_fqdn = format(
    "%s.%s.%s.%s.%s.",
    local.svc, var.seed.tier, var.seed.env, var.seed.region, var.seed.base_domain
  )

  logs_bucket_raw = "${var.seed.org}-${var.seed.env}-${var.seed.region}-${var.seed.service_id}-logs"
  logs_bucket_name = length(local.logs_bucket_raw) <= 63 ? local.logs_bucket_raw :
                     substr(local.logs_bucket_raw, 0, 63 - 1 - 6) + "-" + local.name_hash

  iam_role_raw = "${var.seed.org}-${var.seed.tenant}-${var.seed.env}-${var.seed.service_id}-role"
  iam_role_name = length(local.iam_role_raw) <= 64 ? local.iam_role_raw :
                  substr(local.iam_role_raw, 0, 64 - 1 - 6) + "-" + local.name_hash
}
```

#### 6.3 Example Seed → Derived

**Seed (**`seeds/payments-api.prod.eu-west-1.yaml`):

```yaml
org: acme
tenant: core
env: prod
region: eu-west-1
service_id: payments-api
tier: app
base_domain: acme.example
zone_type: public
```

**Key Derived:**

- `name`: `acme-core-prod-eu-west-1-payments-api-app`
- `host_fqdn`: `payments-api.app.prod.eu-west-1.acme.example.`
- `tags`: `{ org=acme, tenant=core, env=prod, region=eu-west-1, service=payments-api, tier=app }`
- `logs_bucket`: `acme-prod-eu-west-1-payments-api-logs`
- `iam_role_name`: `acme-core-prod-payments-api-role`

#### 6.4 TypeScript Helper (CLI `cdctl`) — Validation + Preview

> Rationale: You prefer TDD/TypeScript; this gives fast feedback before `terraform plan`.

```ts
// tools/cdctl/src/derive.ts
import Ajv from "ajv";
import schema from "../schemas/dcd-seed.schema.json";
import xxhash from "xxhashjs"; // or implement fnv1a

export type Seed = {
  org: string; tenant: string; env: string; region: string;
  service_id: string; tier: string; base_domain: string; zone_type: "public"|"private";
  is_internal?: boolean;
};

const ajv = new Ajv({allErrors:true});
const validate = ajv.compile(schema as any);

const MAX = { name: 63 };

export function derive(seed: Seed) {
  if (!validate(seed)) {
    const msg = ajv.errorsText(validate.errors, {separator: "n"});
    throw new Error(`Seed validation failed:n${msg}`);
  }
  const canon = [
    seed.org, seed.tenant, seed.env, seed.region, seed.service_id, seed.tier, seed.base_domain
  ].map(s => s.toLowerCase()).join("|");

  const h = xxhash.h32(canon, 0xC0FFEE).toString(16).padStart(8, "0").slice(0, 6);

  const rawName = `${seed.org}-${seed.tenant}-${seed.env}-${seed.region}-${seed.service_id}-${seed.tier}`.toLowerCase();
  const name = rawName.length <= MAX.name ? rawName : `${rawName.slice(0, MAX.name - 1 - 6)}-${h}`;

  const hostFqdn = `${seed.service_id}.${seed.tier}.${seed.env}.${seed.region}.${seed.base_domain}.`.toLowerCase();

  return {
    name,
    dns: {
      host_fqdn: hostFqdn,
      zone_type: seed.zone_type,
      cert_sans: [
        hostFqdn.slice(0,-1),
        `${seed.service_id}.${seed.env}.${seed.region}.${seed.base_domain}`.toLowerCase()
      ]
    },
    tags: {
      org: seed.org, tenant: seed.tenant, env: seed.env, region: seed.region,
      service: seed.service_id, tier: seed.tier, managedBy: "terraform", schema: "dcd/v1"
    },
    checkpoints: { builder_version: "dcd-tf/1.0.0", seed_checksum: h }
  };
}
```

**Property-based tests (fast-check) recommend:**

- Output always lower-case; no invalid chars; length caps obeyed; hash suffix stable; idempotency on same Seed.

#### 6.5 GitHub Actions (CI) — Plan + Policy Gate

```yaml
name: infra-plan
on:
  pull_request:
    paths: ["infra/**"]
jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: npm ci --prefix infra/tools/cdctl
      - run: npm run validate:seeds --prefix infra/tools/cdctl
      - uses: hashicorp/setup-terraform@v3
      - run: terraform -chdir=infra/stacks/aws-prod init
      - run: terraform -chdir=infra/stacks/aws-prod validate
      - run: terraform -chdir=infra/stacks/aws-prod plan -out plan.tfplan
      - run: terraform show -no-color infra/stacks/aws-prod/plan.tfplan > plan.txt
      - uses: aquasecurity/trivy-action@0.20.0
        with:
          scan-type: config
          scan-ref: infra/
      - name: Conftest (OPA)
        run: conftest test infra/ --policy policy/
      - uses: actions/upload-artifact@v4
        with: { name: tf-plan, path: infra/stacks/aws-prod/plan.txt }
```

#### 6.6 Pre-commit Hooks

```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.93.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
  - repo: https://github.com/bridgecrewio/checkov
    rev: 3.2.320
    hooks:
      - id: checkov
        args: ["-d", "."]
  - repo: https://github.com/open-policy-agent/conftest
    rev: v0.55.0
    hooks:
      - id: conftest
        args: ["test", "infra/", "--policy", "policy/"]
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
```

---

### 7. Security Considerations

- **Secrets Never in State/Repo:** Only references. Verify `sensitive = true` on outputs; audit with scanners.
- **KMS/Key Vault:** Derived aliases (e.g., `alias/acme-prod-eu-west-1-payments`) with key rotation policy.
- **DNS Ownership Proof:** ACME DNS‑01 with least privilege for CI roles.
- **Signed Artifacts:** Enable signed commits/tags; verify `.terraform.lock.hcl` changes in PR.
- **RBAC:** Tie IAM roles and Kubernetes RBAC to derived identifiers to maintain least privilege and traceability.

---

### 8. Operational Considerations

- **Drift Detection:** Scheduled `terraform plan` runs; alert on divergence.
- **Blue/Green & Ephemerals:** `env = ephemeral-<id>` creates isolated namespaces; TTL defaults lower; automatic teardown policies.
- **Incident Hygiene:** Because identifiers are deterministic, it’s faster to grep logs and correlate resources across systems.
- **Documented Escape Hatches:** Allow a `derived_overrides` map for rare exceptions (e.g., third‑party name constraints), but log and gate via policy.

---

### 9. Backward Compatibility & Migration

- Introduce Builder alongside legacy stacks.
- For each service:
  1. Create Seed.
  2. Run preview (CLI) to see derived identifiers.
  3. Map legacy → derived names; for incompatible renames, use aliases (e.g., Route 53 CNAME) during cutover.
  4. Roll out environment by environment (dev → prod), with policy gates enabled.

---

### 10. Alternatives Considered

- **Free-form variables everywhere:** Flexible but brittle; high cognitive load.
- **Terragrunt-only approach:** Helpful for orchestration, but still benefits from a deterministic naming Builder.
- **Global Templates:** Often too rigid across clouds; this RFC’s Builder is composable per provider.

---

### 11. Open Questions

1. Which stable hash (FNV‑1a/XXH32) do we standardize on across languages?
2. Do we enforce a **single** hostname pattern or allow a library of patterns (edge/internal/data-plane)?
3. Where should the **secret checksum manifest** live and how is it protected?
4. What’s the threshold for truncation vs. abbreviations (e.g., `eu-west-1` → `euw1`)?

---

### 12. Appendix A: Example Terraform DNS Module (Provider-Agnostic Interface)

```hcl
variable "derived" {
  type = object({
    dns = object({
      host_fqdn = string
      zone_type = string
      cert_sans = list(string)
    })
    tags = map(string)
  })
}

# On AWS (example), one implementation file might do:
# - data "aws_route53_zone" lookup based on base domain
# - aws_route53_record for A/AAAA/CNAME to LB target
# - acm_certificate using cert_sans

# On Azure equivalent:
# - azurerm_dns_zone / private_dns_zone
# - azurerm_dns_a_record / cname_record
# - Key Vault cert or Azure-managed certs
```

---

### 13. Appendix B: Developer Experience (DX)

- **One file to edit:** `seeds/<service>.<env>.<region>.yaml`
- **Fast feedback:** `cdctl preview seeds/foo.stage.eu-west-1.yaml` → prints derived names/DNS before any `plan`
- **Guardrails:** Pre-commit stops typos; CI blocks unsafe plans
- **TDD-friendly:** Builder has unit + property tests; Terraform modules have integration tests (e.g., `terratest`)

---

### 14. Summary

By constraining human input to a tightly validated Seed and deriving everything else deterministically, you gain resilience: fewer typos, predictable names, repeatable DNS and cert issuance, and auditable configuration changes. The Builder is the single place to perfect, test, and review—once it’s correct, your incremental inputs are small and far less error-prone.

---

### Suggested Next Steps

1. **Pick the Seed fields** you want to standardize (above defaults are a good start).
2. **Create the Builder module** (`modules/dcd`) and the **TypeScript CLI** for validation/preview.
3. **Add pre-commit & CI gates** from this RFC.
4. **Pilot** on one service (e.g., `payments-api` in `dev`), then roll out progressively.

---

Would you like me to:

- generate a working **Terraform module skeleton** for `modules/dcd` and `modules/dns`, or
- scaffold the **TypeScript CLI (**`cdctl`) with tests so you can iterate TDD-style?
  I am a developer. I have always tried to make robust flexible code. I have this sense that loosely coupled code is more resilient. But the config for a particular app deployment is so delicate and fragile. 1 wrong character in a string, 1 byte wrong in some encrypted secret cause the whole system to stop working. I would like to be able to separate out config in my terraform IAC and keep it safe and change evident. Having as much automated as possible. For instance, having a DNS Hostnaming service naming protocol that means I supply minimal config, like the base domain and the code generates the rest based on it. That way, once the builder code is validated as correct my input is small and so less error prone. Formalise this idea for me and describe it in a RFC type doc

Title: RFC-XXXX — Declarative, Generative Configuration for Robust Terraform Deployments

Status: Draft

Author(s): [Your Name]

Date: 2025-10-27

Date of last update: 2025-10-27

1. Introduction
   This document defines a methodology and a minimal, automatable protocol for generating deployment configuration from a small, well-formed input surface. The goal is to reduce human error, improve resilience to changes, and enable safer, more auditable infrastructure as code (IaC) by separating concerns between intent and implementation. The approach emphasizes determinism, validation, and automated regeneration of environment-specific configurations from a concise base input.

2. Problem Statement

- Small mistakes in strings, secrets, or hard-coded values can destabilize deployments.
- Traditional IaC often mixes high-level intent with numerous environment-specific overrides, increasing fragility.
- There is a need for a reproducible builder that, given minimal input, can produce a complete, validated Terraform configuration and related artifacts.
- Change management should be automated and traceable, with strong guarantees about what was generated and applied.

3. Scope

- Applicable to Terraform-based deployments and closely related IaC artifacts (e.g., Helm charts, Kubernetes manifests generated from Terraform, ancillary secret management).
- Covers generation of:
  - DNS naming and resource identifiers
  - Environment-specific overrides
  - Secrets handling (encrypted or externalized)
  - Validation and dry-run capabilities
  - Observability of the generation process (audit logs, diffs)

4. Principles

- Minimum Input, Maximum Safety: Users provide a concise base input; the system derives the remainder.
- Determinism: Given the same base input and builder version, generation is deterministic.
- Separation of Concerns: The base input encodes intent; the builder encodes policy, naming, and environment specifics.
- Validation by Design: All generated configurations pass a defined validation pipeline before deployment.
- Immutable Artifacts: Generated artifacts are versioned and immutable post-generation.
- Security by Default: Secrets are never stored in plain text; use secret managers or envelope encryption.

5. Core Concepts

5.1 Base Input Model

- Purpose: Capture the minimal, unambiguous surface from which all configuration is derived.
- Components:
  - BaseDomain: string (e.g., [example.com](http://example.com))
  - Environment: string (e.g., dev, staging, prod)
  - BuilderVersion: semantic version of the generation tool
  - NamingPolicy: reference to a policy module (see 5.2)
  - SecretMode: enum (encrypted-stores, external-secret-manager)
  - OptionalFlags: map&lt;string, string&gt; for feature toggles

5.2 Naming and DNS Policy

- Objective: Derive all hostnames, DNS records, and resource names from a centralized naming policy to minimize drift and errors.
- Policy Modules: Pluggable generators that implement:
  - HostnameBase(domain, environment)
  - ResourceName(base, resource-type, environment)
  - DNSRecordSets(input) producing A/AAAA/CNAME/TXT records as needed
- Example:
  - Hostname for API: api.{environment}.{base-domain}
  - Service endpoints: {service}-{env}.{domain}
- Validation: Ensure all derived names conform to DNS/name length constraints and provider limits.

5.3 Secrets and Sensitive Data

- Approach: Secrets are never embedded verbatim in generated Terraform files.
- Options:
  - Encrypted Secret Store: Secrets are retrieved at apply time via a secure backend (e.g., AWS Secrets Manager, Vault) and injected through provider configurations or dynamic secrets.
  - External Secret Manager: Use Terraform external data sources or secret manager integrations to populate values at runtime.
- Secret Versioning: Include a secret version or checksum in the generated artifacts for traceability without exposing content.

5.4 Generation Pipeline

- Steps:
  1. Input Validation: Syntactic and semantic checks on the base input.
  2. Policy Loading: Load naming, DNS, and environment policies.
  3. Artifact Generation: Produce Terraform module configurations, variable files, and any ancillary manifests.
  4. Dry-Run Validation: Run plan in a controlled, read-only mode to catch issues.
  5. Diff and Audit: Produce humanand machine-readable diffs; record provenance.
  6. Commit/Publish: Store generated artifacts in version control or artifact registry with a immutable tag.
- Reproducibility: Every build uses a deterministic seed (if applicable) and fixed policy versions.

5.5 Validation Rules

- Correctness: Generated names must pass DNS and provider constraints.
- Completeness: All required resources for the given environment are present.
- Consistency: Resource references are coherent across modules.
- Security: Secrets handling adheres to policy (no plaintext exposure).
- Idempotence: Applying the generated Terraform plan should converge to the same state.

6. RFC Semantics and Interfaces

6.1 Interfaces

- BaseInput: JSON/YAML schema describing the minimal surface.
- PolicyInterface: Plugins implementing naming and DNS derivation.
- Builder: The orchestrator that coordinates validation, generation, and publishing.
- OutputArtifacts: Terraform configurations, variables, and manifests.

6.2 Data Formats (Illustrative)

- BaseInput (YAML):
  baseDomain: [example.com](http://example.com)
  environment: prod
  builderVersion: 1.2.0
  namingPolicy: standard-v1
  secretMode: encrypted-stores
  flags:
  enableObservability: "true"
- GeneratedOutput (Terraform files and supporting artifacts) produced by the Builder.

6.3 Workflow Scenarios

- Scenario A: New deployment with minimal base input; builder derives all hostnames, resource names, and secrets references, then validates and outputs ready-to-apply Terraform code.
- Scenario B: Change domain policy; builder re-generates all affected names while preserving environment-specific resource state references, enabling smooth drift control.

7. Security Considerations

- Never embed secrets in generated files.
- Enforce least privilege for any secret access during generation.
- Store provenance metadata to enable traceability of changes.
- Protect the base input from accidental leakage; consider access controls and encryption at rest.

8. Operational Guidelines

8.1 Tooling

- Use a dedicated generation tool (the Builder) with:
  - Versioned policies for naming and DNS
  - Pluggable secret retrieval adapters
  - Strict, typed base input schema
  - Integrated validation, plan, and diff capabilities

8.2 Deployment Workflow

- Developers provide only the BaseInput.
- The system outputs a complete, versioned Terraform bundle and manifests.
- The bundle is reviewed via diffs before applying.
- Secrets are resolved at apply via the selected secret backend.

8.3 Rollbacks

- Generated artifacts are versioned; rollbacks revert to a prior artifact set.
- Terraform state management should be aligned with the artifact version to ensure reproducibility.

9. Evaluation Metrics

- Change rate of configuration drift after adopting the generator approach.
- Time-to-plan and time-to-apply reductions due to reduced input surface.
- Frequency of plan failures due to human input errors.
- Security incidents related to secret exposure (goal: zero).

10. Risks and Mitigations

- Risk: Policy drift between naming policy and actual resource usage.
  Mitigation: Strict policy versioning and automated cross-checks against resource schemas.
- Risk: Secret exposure through misconfigured outputs.
  Mitigation: Enforce secret omission in artifacts and use dynamic injection only.

11. References

- None specified in this draft. Extend with internal policy documents and provider guidelines as needed.

12. Change Log

- Initial draft.

Appendix A: Minimal Example

BaseInput (YAML):

baseDomain: [example.com](http://example.com)

environment: prod

builderVersion: 1.2.0

namingPolicy: standard-v1

secretMode: encrypted-stores

flags:

enableObservability: "true"

GeneratedArtifacts (conceptual):

- modules/
  - network/
  - dns/
  - app/
- environments/prod/terraform/
  - [main.tf](http://main.tf) (references derived hostnames like [api.prod.example.com](http://api.prod.example.com))
  - [variables.tf](http://variables.tf)
  - secret_refs.tf (encrypted references)
- secrets/
  - references to external secret manager IDs, not plaintext

Appendix B: Typical Acceptance Criteria for Generated Output

- plan shows all intended resources with expected counts
- no plaintext secrets in any output
- DNS records generated match the naming policy
- Terraform state alignment with artifact version

Would you like this RFC to be tailored to a specific toolchain or cloud provider (e.g., AWS with Route 53, Terraform Cloud, GitOps workflow), and should I provide a concrete example repo layout and sample code skeleton to start implementing the Builder?
