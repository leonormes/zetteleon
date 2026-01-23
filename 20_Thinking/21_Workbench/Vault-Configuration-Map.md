---
created: 2026-01-21T12:58:09+00:00
modified: 2026-01-23T15:08:04+00:00
title: Vault-Configuration-Map
---

## HashiCorp Vault Configuration Map

**Generated:** 2026-01-21
**Vault Cluster:** HCP Vault (vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200)
**Root Namespace:** admin/

---

### Overview

This document provides a comprehensive mapping of the current Vault configuration, including namespace hierarchy, authentication methods, policies, and secrets engines. The analysis is based on the root namespace (`admin/`) where current access permissions allow full visibility.

---

### Namespace Structure

The Vault instance uses a hierarchical namespace structure with the following layout:

```sh
admin/ (root namespace)
├── central/
├── deployments/
└── fitfile/
```

#### Namespace Details

##### Root Namespace (admin/)

- **Full Path:** `admin/`
- **Access Level:** Full administrative access with hcp-root policy
- **Current Token:** Service token with hcp-root policy

##### Central Namespace

- **ID:** jPL3k
- **Full Path:** `admin/central/`
- **Access Level:** No access with current token (403 permission denied)
- **Custom Metadata:** None

##### Deployments Namespace

- **ID:** Adw8E
- **Full Path:** `admin/deployments/`
- **Access Level:** No access with current token (403 permission denied)
- **Custom Metadata:** None

##### Fitfile Namespace

- **ID:** 7yQSL
- **Full Path:** `admin/fitfile/`
- **Access Level:** No access with current token (403 permission denied)
- **Custom Metadata:** None

---

### Authentication Methods

All authentication methods are configured in the root namespace (`admin/`).

#### 1. AppRole (Primary)

- **Path:** `approle/`
- **Accessor:** auth_approle_f0941c94
- **Plugin Version:** v1.21.1+builtin.vault
- **Token Type:** default-service
- **TTL:** System default
- **Replication:** Replicated
- **UUID:** 7c57dac1-7e21-570c-ca91-03996cbc8e56
- **Status:** Supported

#### 2. JWT (Primary)

- **Path:** `jwt/`
- **Accessor:** auth_jwt_39c1d7b2
- **Plugin Version:** v0.25.0+builtin
- **Token Type:** default-service
- **TTL:** System default
- **Replication:** Replicated
- **UUID:** c2d46d3a-c429-c6f3-7621-2ad2de936dd8
- **Status:** Supported

#### 3. JWT (Terraform)

- **Path:** `jwt-terraform/`
- **Accessor:** auth_jwt_30371417
- **Plugin Version:** v0.25.0+builtin
- **Token Type:** default-service
- **TTL:** System default
- **Replication:** Replicated
- **UUID:** 0b314a56-5c02-a185-9769-b64d8a960e1d
- **Status:** Supported
- **Purpose:** Dedicated JWT authentication for Terraform workflows

#### 4. Kubernetes

- **Path:** `kubernetes/`
- **Accessor:** auth_kubernetes_8c2a4b7a
- **Plugin Version:** v0.23.1+builtin
- **Token Type:** default-service
- **TTL:** System default
- **Replication:** Replicated
- **UUID:** 5150f5e0-dac1-dd89-fbb5-fcc77c184817
- **Status:** Supported

#### 5. AppRole (Local Dev)

- **Path:** `local-dev-auth-mount/`
- **Accessor:** auth_approle_1b65f67b
- **Plugin Version:** v1.21.1+builtin.vault
- **Token Type:** default-service
- **TTL:** System default
- **Replication:** Replicated
- **UUID:** 9c63e0fc-350a-1e44-666a-13637cd98b7d
- **Status:** Supported
- **Purpose:** Dedicated AppRole mount for local development

#### 6. Token (Default)

- **Path:** `token/`
- **Accessor:** auth_ns_token_8395ce45
- **Plugin Version:** v1.21.1+builtin.vault
- **Token Type:** default
- **TTL:** System default
- **Replication:** Replicated
- **UUID:** b4ed47c5-d249-333a-8188-b6ccfd6caca1
- **Description:** Token based credentials

---

### Policies

All policies listed below are configured in the root namespace (`admin/`).

#### 1. Hcp-root (Super Admin)

**Purpose:** Full administrative access across all Vault paths

```hcl
path "*" {     
    capabilities = ["sudo","read","create","update","delete","list","patch","subscribe"]
    subscribe_event_types = ["*"]
}
```

**Risk Level:** 🔴 CRITICAL - Full unrestricted access

#### 2. Admin (Administrative)

**Purpose:** Broad administrative capabilities for managing Vault configuration

**Key Capabilities:**
- System health monitoring
- ACL policy management (full CRUD)
- Auth method management (full CRUD)
- Secrets engine management (full CRUD)
- Access to secrets at `secrets/*`, `secret/*`, and `kv/*` paths

```hcl
# System health
path "sys/health" {
  capabilities = ["read", "sudo"]
}

# ACL Policies
path "sys/policies/acl" {
  capabilities = ["list"]
}
path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Auth methods
path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
path "sys/auth/*" {
  capabilities = ["create", "update", "delete", "sudo"]
}
path "sys/auth" {
  capabilities = ["read"]
}

# Secrets
path "secrets/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
path "kv/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Secrets engines
path "sys/mounts/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
path "sys/mounts" {
  capabilities = ["read"]
}
```

**Risk Level:** 🔴 HIGH - Administrative access

#### 3. Default (Standard User)

**Purpose:** Basic token management and self-service capabilities

**Key Capabilities:**
- Token self-lookup, renewal, and revocation
- Cubbyhole access
- Response wrapping
- Entity lookup
- Control group requests

**Risk Level:** 🟢 LOW - Standard user operations only

#### 4. Argocd-acr-pull

**Purpose:** Azure credential access for ArgoCD

```hcl
path "azure/creds/argocd" {
   capabilities = ["read"]
}
```

**Risk Level:** 🟡 MEDIUM - Read-only access to Azure credentials
**Note:** References an Azure secrets engine that may not be mounted in root namespace

#### 5. Argocd-secrets-lca-prd-2

**Purpose:** ArgoCD access to deployment secrets in production environment

```hcl
path "deployments/lca-prd-2/secrets/data/*" {
  capabilities = ["read", "list"]
}
```

**Risk Level:** 🟡 MEDIUM - Read-only access to production secrets
**Note:** References the `deployments` namespace which is inaccessible from root

#### 6. Engine-policy

**Purpose:** Secrets engine management and PKI operations

```hcl
# Secrets engine management
path "sys/mounts/*" {
  capabilities = [ "create", "read", "update", "delete", "list" ]
}
path "sys/mounts" {
  capabilities = [ "read", "list" ]
}

# PKI operations
path "pki*" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}

# Application secrets
path "deployments/lca-prd-2/secrets/data/application" {
  capabilities = ["read"]
}
```

**Risk Level:** 🔴 HIGH - Can manage secrets engines and PKI infrastructure
**Note:** References PKI paths and deployments namespace

#### 7. Tester

**Purpose:** Testing and namespace management

```hcl
# Test secrets
path "secret/data/test/*" {
  capabilities = [ "create", "read", "update" ]
}

# Namespace management
path "sys/namespaces/*" {
   capabilities = [ "create", "read", "update", "delete", "list" ]
}
```

**Risk Level:** 🔴 HIGH - Can create and delete namespaces
**Note:** Namespace management is a privileged operation

#### 8. Vso-auth-policy-operator

**Purpose:** Vault Secrets Operator (VSO) client cache encryption/decryption

```hcl
path "vso-transit/encrypt/vso-client-cache" {
   capabilities = ["create", "update"]
}
path "vso-transit/decrypt/vso-client-cache" {
   capabilities = ["create", "update"]
}
```

**Risk Level:** 🟡 MEDIUM - Limited to VSO transit operations
**Note:** References a `vso-transit` secrets engine that may not be mounted in root namespace

---

### Secrets Engines

Currently, only system secrets engines are visible in the root namespace. Application-specific secrets engines likely exist in child namespaces.

#### 1. Cubbyhole

- **Path:** `cubbyhole/`
- **Type:** ns_cubbyhole
- **Accessor:** ns_cubbyhole_d39803dd
- **Version:** v1.21.1+builtin.vault
- **Replication:** Local (not replicated)
- **TTL:** System default
- **UUID:** aa6dd06b-6e63-0377-2552-dcdf5f4c705c
- **Description:** Per-token private secret storage

#### 2. Identity

- **Path:** `identity/`
- **Type:** ns_identity
- **Accessor:** ns_identity_2e70efd9
- **Version:** v1.21.1+builtin.vault
- **Replication:** Replicated
- **TTL:** System default
- **UUID:** 60954663-11c9-5913-504d-1f7436341ea7
- **Description:** Identity store for entity and group management

#### 3. System

- **Path:** `sys/`
- **Type:** ns_system
- **Accessor:** ns_system_ea99883f
- **Version:** v1.21.1+builtin.vault
- **Replication:** Replicated
- **Seal Wrap:** Enabled
- **TTL:** System default
- **UUID:** 8457a0cb-4109-00be-332c-8d75d38fa648
- **Description:** System endpoints for control, policy, and debugging

---

### Current Token Analysis

**Token Details:**
- **ID:** [REDACTED]
- **Accessor:** h95D54QdLqrmFZivasUmAX38.GzdOO
- **Display Name:** token-hcp-root
- **Policies:** default, hcp-root
- **Entity ID:** e73517fd-a2b3-1ced-a97b-b043d29d85aa
- **Creation Time:** 2026-01-21 09:00:05 UTC
- **Expire Time:** 2026-01-21 15:00:05 UTC
- **TTL Remaining:** ~2h7m (at time of analysis)
- **Renewable:** No
- **Orphan:** Yes
- **Path:** auth/token/create/hcp-root
- **Namespace:** admin/

---

### Security Observations & Refactoring Recommendations

#### 🔴 Critical Issues

1. **Over-Privileged Root Access**
   - The `hcp-root` policy grants unrestricted access to all paths
   - **Recommendation:** Create more granular administrative policies and use hcp-root only for emergency access

2. **Namespace Isolation Broken**
   - Policies in root namespace reference paths in child namespaces (deployments, central, fitfile)
   - Current token cannot access child namespaces despite having hcp-root policy
   - **Recommendation:** Move namespace-specific policies into their respective namespaces

3. **Multiple Admin Policies**
   - Both `admin` and `hcp-root` provide broad administrative access
   - **Recommendation:** Consolidate or clearly differentiate their use cases

#### 🟡 High Priority Issues

1. **Tester Policy Too Powerful**
   - Can create/delete namespaces, which is a critical operation
   - **Recommendation:** Create a restricted testing environment or limit namespace operations

2. **Engine Policy Overlap**
   - `engine-policy` can manage all secrets engines, which overlaps with `admin` policy
   - **Recommendation:** Scope to specific engine types or paths

3. **Inconsistent Path References**
   - Policies reference paths that don't exist in the same namespace (azure/creds, pki*, vso-transit)
   - **Recommendation:** Audit and align policy paths with actual mount points

#### 🟢 Medium Priority Issues

1. **Multiple AppRole Mounts**
   - Two AppRole auth methods: `approle/` and `local-dev-auth-mount/`
   - **Recommendation:** Clarify separation of concerns; consider environment-based namespaces

2. **Multiple JWT Mounts**
   - Two JWT auth methods: `jwt/` and `jwt-terraform/`
   - **Recommendation:** Document which applications use which mount

3. **No Secrets Engines Visible**
   - Only system engines visible in root namespace
   - Application secrets engines likely in child namespaces
   - **Recommendation:** Document the secrets engine layout in each namespace

#### 🔵 Low Priority / Organizational

1. **Namespace Access Model**
   - Child namespaces are completely isolated from root namespace admin
   - **Recommendation:** Define clear access delegation model

2. **Policy Naming Convention**
   - Mix of descriptive names (argocd-acr-pull) and generic names (tester, engine-policy)
   - **Recommendation:** Establish consistent naming: `<service>-<environment>-<permission-level>`

3. **Missing Documentation**
   - No visible descriptions for most auth methods
   - **Recommendation:** Add descriptions to all auth methods and policies

---

### Recommended Refactoring Plan

#### Phase 1: Assessment & Documentation (Current)

- ✅ Map current configuration
- ⬜ Document all child namespace configurations (requires elevated access)
- ⬜ Identify all applications and their Vault integration points
- ⬜ Map policies to actual users/services

#### Phase 2: Namespace Restructuring

```sh
admin/ (root)
├── system/          # System-level operations
├── infrastructure/  # Platform services (ArgoCD, VSO, etc.)
├── applications/    # Application secrets
│   ├── production/
│   ├── staging/
│   └── development/
└── shared/         # Cross-cutting concerns (PKI, Transit, etc.)
```

#### Phase 3: Policy Refinement

1. Create tiered admin policies:
   - `super-admin`: Break-glass only
   - `platform-admin`: Infrastructure management
   - `namespace-admin`: Per-namespace administration
   - `developer`: Application secret access

2. Move namespace-specific policies into namespaces:
   - `argocd-secrets-lca-prd-2` → deployments namespace
   - `argocd-acr-pull` → infrastructure or deployments namespace

3. Create role-based policies:
   - `readonly-auditor`
   - `secret-manager`
   - `auth-manager`
   - `policy-manager`

#### Phase 4: Auth Method Consolidation

1. Standardize on primary auth methods per use case:
   - Kubernetes → `kubernetes/`
   - CI/CD → `jwt-terraform/` or dedicated AppRole
   - Applications → `approle/` per namespace
   - Development → namespace-specific methods

2. Document and label all auth methods with descriptions

#### Phase 5: Secrets Engine Organization

1. Mount application-specific engines in appropriate namespaces
2. Use consistent paths: `<app-name>/secrets/`, `<app-name>/config/`
3. Enable Transit and PKI in shared namespace for cross-cutting use

#### Phase 6: Security Hardening

1. Implement least-privilege access
2. Enable audit logging and monitoring
3. Regular policy review cadence
4. Rotate long-lived tokens
5. Implement token TTL limits

---

### Next Steps

To complete the audit and proceed with refactoring:

1. **Gain Access to Child Namespaces:**
   - Obtain tokens or policies with access to central/, deployments/, and fitfile/ namespaces
   - Re-run this audit for each namespace

2. **Document Secrets Engines:**
   - List all mounted secrets engines in each namespace
   - Identify KV, PKI, Transit, Database, and cloud provider integrations

3. **Map Users and Services:**
   - Identify all service accounts and their associated policies
   - Document which applications use which auth methods

4. **Review Application Integration:**
   - Audit how applications authenticate and access secrets
   - Identify opportunities for Vault Secrets Operator or agent injection

5. **Implement Changes Incrementally:**
   - Start with non-production namespaces
   - Test policy changes thoroughly
   - Have rollback plans for all changes

---

### Appendix: Commands Used

```sh
# Namespace listing
vault namespace list
vault read sys/namespaces/central
vault read sys/namespaces/deployments
vault read sys/namespaces/fitfile

# Authentication methods
vault auth list
vault auth list -detailed

# Policies
vault policy list
vault policy read <policy-name>

# Secrets engines
vault secrets list
vault secrets list -detailed

# Token information
vault token lookup
```
