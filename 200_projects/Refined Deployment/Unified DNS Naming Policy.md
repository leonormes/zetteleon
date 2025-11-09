---
aliases: []
confidence: 
created: 2025-09-22T16:08:24Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: Unified DNS Naming Policy
type:
uid: 
updated: 
version:
---

## Unified DNS Naming Policy for FITFILE Deployments

### Executive Summary

This policy establishes a uniform DNS naming convention for all FITFILE deployments, regardless of customer environment (private, public, or hybrid). It consolidates the fragmented DNS patterns identified across your deployment documentation and provides clear automation guidelines for Terraform implementation.

### Core Principles

1. **Uniform Deployment Identity**: Every deployment uses a consistent `deployment-key` format
2. **Clear Layer Separation**: Distinct DNS layers for user access vs. machine-to-machine communication
3. **Customer Flexibility**: Support for customer-provided root domains while maintaining internal consistency
4. **Security by Design**: Private PKI for all internal communication, public certificates only for user-facing endpoints
5. **Automation-First**: All DNS records generated programmatically via Terraform

### DNS Layer Architecture

#### Layer 1: User Access (Public/Customer-Facing)

**Purpose**: Human users accessing web interfaces and APIs

##### Scenario A: Customer Provides Root Domain

- **Pattern**: `{service}.{customer-domain}`
- **Examples**:
  - `app.fitfile.nhstrust.co.uk`
  - `argocd.fitfile.nhstrust.co.uk`
- **DNS Management**: Customer's DNS provider
- **Certificate Method**: HTTP-01 ACME challenge (Let's Encrypt)
- **CNAME Target**: Points to canonical FITFILE hostname

##### Scenario B: FITFILE Managed Domain (Private Deployment)

- **Pattern**: `{deployment-key}.privatelink.fitfile.net`
- **Examples**:
  - `cuh-prod-1.privatelink.fitfile.net`
  - `hie-prod-34.privatelink.fitfile.net`
- **DNS Management**: Azure Private DNS
- **Certificate Method**: DNS-01 ACME challenge

##### Scenario C: FITFILE Managed Domain (Public Deployment)

- **Pattern**: `{deployment-key}.fitfile.net`
- **Examples**:
  - `barts.fitfile.net`
  - `nhs-provider-1.fitfile.net`
- **DNS Management**: Cloudflare
- **Certificate Method**: DNS-01 ACME challenge

#### Layer 2: Machine-to-Machine Communication (Internal)

**Purpose**: Secure service-to-service communication with mTLS

##### Primary Internal Domain

- **Pattern**: `{service}.{deployment-key}.m2m.fitfile.internal`
- **Examples**:
  - `relay.cuh-prod-1.m2m.fitfile.internal`
  - `coordinator.hie-prod-34.m2m.fitfile.internal`
  - `api.barts-prod-1.m2m.fitfile.internal`
- **DNS Management**: Azure Private DNS / Kubernetes CoreDNS
- **Certificate Authority**: HCP Vault PKI (Private CA)
- **Security**: mTLS required for all communication

##### NHS-Specific Internal Services

- **Pattern**: `{service}.{deployment-key}.nhs.fitfile.internal`
- **Examples**:
  - `proxy.cuh-prod-1.nhs.fitfile.internal`
  - `integration.barts-prod-1.nhs.fitfile.internal`
- **Purpose**: NHS trust-specific integrations and proxy services

### Deployment Key Format

#### Standard Format

`{customer-code}-{environment}-{instance}`

#### Components

- **customer-code**: 2-4 character customer identifier (e.g., `cuh`, `barts`, `hie`)
- **environment**: `prod`, `dev`, `test`, `staging`
- **instance**: Sequential number for multiple deployments (`1`, `2`, `3`)

#### Examples

- `cuh-prod-1` (Cambridge University Hospitals, Production, Instance 1)
- `barts-dev-1` (Barts Health NHS Trust, Development, Instance 1)
- `hie-prod-34` (Health Information Exchange, Production, Instance 34)

### Service Naming Convention

#### Core Services

| Service       | Purpose                  | Example                                        |
| ------------- | ------------------------ | ---------------------------------------------- |
| `app`         | Main application UI      | `app.cuh-prod-1.privatelink.fitfile.net`       |
| `api`         | REST API endpoints       | `api.cuh-prod-1.m2m.fitfile.internal`          |
| `relay`       | FitConnect relay service | `relay.cuh-prod-1.m2m.fitfile.internal`        |
| `coordinator` | FFCloud coordinator      | `coordinator.cuh-prod-1.m2m.fitfile.internal`  |
| `argocd`      | GitOps management        | `argocd.cuh-prod-1.privatelink.fitfile.net`    |
| `workflows`   | Argo Workflows           | `workflows.cuh-prod-1.privatelink.fitfile.net` |
| `proxy`       | NHS integration proxy    | `proxy.cuh-prod-1.nhs.fitfile.internal`        |

### Certificate Management Strategy

#### Public Certificates (User Access Layer)

- **Authority**: Let's Encrypt via cert-manager
- **Challenge Type**:
  - DNS-01 for FITFILE-managed domains
  - HTTP-01 for customer-provided domains
- **Automation**: Automatic renewal via cert-manager

#### Private Certificates (M2M Layer)

- **Authority**: HCP Vault PKI
- **Certificate Type**: mTLS (mutual TLS)
- **Rotation**: 30-day automatic rotation
- **Scope**: Per-deployment intermediate CA for isolation

### Implementation Guidelines

#### DNS Record Creation Priority

1. **Customer Domain** (if provided)
2. **Private Link Domain** (for private deployments)
3. **Public FITFILE Domain** (for public deployments)

#### Terraform Variable Structure

```hcl
variable "deployment_config" {
  type = object({
    deployment_key    = string
    customer_domain   = optional(string)
    is_private        = bool
    tld_preference    = string # "customer" | "privatelink" | "public"
  })
}
```

#### DNS Zone Selection Logic

```hcl
locals {
  # Determine primary DNS zone based on configuration
  primary_zone = var.deployment_config.customer_domain != null ? var.deployment_config.customer_domain :
                 var.deployment_config.is_private ? "privatelink.fitfile.net" :
                 "fitfile.net"

  # Internal zone is always consistent
  internal_zone = "m2m.fitfile.internal"
  nhs_zone     = "nhs.fitfile.internal"
}
```

### Migration Strategy

#### Phase 1: Consolidate Existing Patterns

- Map all current hostnames to new naming convention
- Create CNAME records for backward compatibility
- Update application configurations gradually

#### Phase 2: Implement Automation

- Deploy Terraform modules for automated DNS management
- Integrate with HCP Vault for certificate automation
- Establish monitoring for DNS resolution and certificate expiry

#### Phase 3: Deprecate Legacy Patterns

- Remove old DNS records after migration period
- Update documentation and runbooks
- Train operations team on new conventions

### Compliance and Security

#### Security Requirements

- All M2M communication must use private PKI certificates
- Public certificates only for user-facing endpoints
- Network policies to enforce DNS layer separation
- Regular certificate rotation (30 days for private, 90 days for public)

#### Audit Trail

- All DNS changes logged via Terraform state
- Certificate issuance tracked in HCP Vault
- Deployment registry maintains canonical record of all hostnames

### Operational Benefits

1. **Predictable Naming**: Any team member can determine the correct hostname for any service
2. **Automated Provisioning**: New deployments automatically get correct DNS setup
3. **Security Isolation**: Clear separation between public and private communication
4. **Customer Flexibility**: Support for customer branding while maintaining operational consistency
5. **Simplified Troubleshooting**: Consistent patterns make debugging DNS issues easier

### Exception Handling

#### Legacy System Integration

- Maintain compatibility mappings for existing integrations
- Document any deviations from standard naming
- Establish sunset timeline for non-compliant hostnames

#### Special Requirements

- NHS trust-specific naming requirements accommodated via `.nhs.fitfile.internal`
- Regulatory compliance domains handled through customer domain delegation
- Development/testing environments use `.fitfile.dev` for isolation

This policy provides the foundation for uniform, secure, and scalable DNS management across all FITFILE deployments while accommodating the diverse requirements of your customer base.
