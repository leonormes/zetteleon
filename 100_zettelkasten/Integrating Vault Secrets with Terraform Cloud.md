---
aliases: []
confidence: 
created: 2025-10-24T15:40:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [dynamic-secrets, secrets-management, security, Vault]
title: Integrating Vault Secrets with Terraform Cloud
type:
uid: 
updated: 
version:
---

For managing secrets for non-cloud or custom systems within Terraform Cloud, integrating with a dedicated secrets management solution like HashiCorp Vault (or HCP Vault Secrets) is a recommended best practice. This extends the principle of [[Short-Lived Credentials Core Principle in Terraform Cloud|short-lived, ephemeral credentials]] to a wider range of services.

How Vault integration works:

- **Dynamic Engines:** Vault's dynamic secret engines can issue on-demand credentials for databases, APIs, SSH keys, and other services. These credentials are short-lived and automatically revoked after use or expiration.
- **DPC Integration:** Terraform Cloud can integrate with Vault via [[Dynamic Provider Credentials (DPC) in Terraform Cloud|Dynamic Provider Credentials]]. This allows Terraform runs to securely request and receive ephemeral secrets from Vault during execution, without ever storing them statically.
- **Centralized Policy:** Vault provides a centralized platform for defining and enforcing access policies for all secrets, unifying secret management across your infrastructure.

This combination ensures that all sensitive data, whether for cloud providers or internal systems, adheres to a consistent ephemeral and Zero Trust model.

Links:

- [[Short-Lived Credentials Core Principle in Terraform Cloud]]
- [[Dynamic Provider Credentials (DPC) in Terraform Cloud]]
- HashiCorp Vault Dynamic Secrets
- Secret Management Solutions
- [[Recommended Best Practices for Cloud-Native Authentication]]
- Modern Cloud-Native Authentication MOC
- [[ArgoCD Terraform Module Architecture]]
- [[FITFILE Platform Terraform Module Wiki]]
- [[Is the Unified Module Approach Optimal]]
- [[Tooling]]
