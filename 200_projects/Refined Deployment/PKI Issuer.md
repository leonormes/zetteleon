---
aliases: []
confidence: 
created: 2025-09-08T03:19:05Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [certificates, infrastructure, pki, security, vault]
title: PKI Issuer
type:
uid: 
updated: 
version:
---

## Current PKI Architecture

Your setup follows PKI best practices with:

1. **Root CA**: Single self-signed root CA in the `central` namespace
2. **Intermediate CAs**: One per deployment (`pki_int_${deployment}`)
3. **Roles**: Deployment-specific roles with domain restrictions (`${deployment}.fitfile.net`)
4. **Access Policies**: Deployment-specific policies that only allow certificate issuance from their own intermediate CA

## Analysis: Multiple Issuers Vs Single Issuer

### Your Current Approach (Multiple Issuers) ✅ **RECOMMENDED**

**Advantages:**

- **Security Isolation**: Each deployment has its own intermediate CA, limiting blast radius
- **Domain Enforcement**: Built-in domain restriction (`${deployment}.fitfile.net`) at the CA level
- **Compliance**: Easier to audit and demonstrate separation of concerns
- **Revocation Control**: Can revoke an entire deployment's certificate authority if compromised
- **Operational Flexibility**: Can set different TTLs, key sizes, or policies per deployment
- **Zero Trust**: Follows principle of least privilege - deployments can only issue certs for their domain

**Current Implementation:**

```hcl
# Each deployment gets its own intermediate CA
resource "vault_mount" "pki_intermediate" {
  for_each = local.deployments
  path     = "pki_int_${each.key}"
  # ...
}

# Domain restrictions enforced at the role level
resource "vault_pki_secret_backend_role" "deployment_server" {
  allowed_domains = ["${each.key}.fitfile.net"]
  # ...
}
```

### Alternative: Single Issuer with Access Policies

**Disadvantages:**

- **Shared Risk**: Single point of failure - if intermediate CA is compromised, all deployments affected
- **Policy Complexity**: Would require complex policy management to prevent cross-deployment certificate issuance
- **Audit Complexity**: Harder to track which deployment issued which certificates
- **Limited Flexibility**: All deployments share same CA configuration (TTL, key size, etc.)

## Recommendation: Keep Your Current Architecture

Your current multi-issuer approach is **superior** for several reasons:

1. **Security**: Each deployment is cryptographically isolated
2. **Simplicity**: Domain restrictions are enforced at the CA level, not just policy level
3. **Scalability**: Easy to add new deployments without policy conflicts
4. **Compliance**: Clear audit trail and separation of duties

## Potential Improvements

Consider these enhancements to your current setup:

1. **Certificate Transparency Logging**:

```hcl
resource "vault_pki_secret_backend_role" "deployment_server" {
  # Add CT logging
  use_csr_common_name = false
  use_csr_sans        = false
  # ...
}
```

2. **Automated Certificate Rotation** via cert-manager integration (which I see you already have policies for)
3. **Certificate Monitoring** - track certificate expiry across all deployments

Your current architecture follows PKI security best practices and provides excellent isolation between deployments. The slight overhead of managing multiple intermediate CAs is far outweighed by the security and operational benefits.
