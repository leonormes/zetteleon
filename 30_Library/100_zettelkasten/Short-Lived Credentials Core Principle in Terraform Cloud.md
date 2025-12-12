---
aliases: []
confidence: 
created: 2025-10-24T15:34:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [authentication, CICD, OIDC, security, short-lived-credentials]
title: Short-Lived Credentials Core Principle in Terraform Cloud
type:
uid: 
updated: 
version:
---

The core principle behind best practices for credentials in Terraform Cloud (now HCP Terraform) is the complete elimination of long-lived static secrets. This is achieved by replacing them with **ephemeral, OIDC-issued tokens** that are tightly coupled to each Terraform run.

This approach fundamentally aligns with **Zero Trust** security principles, where no entity is implicitly trusted, and access is granted only for the duration and scope required. It also significantly enhances **secure CI/CD practices** by removing the risk associated with static credentials being compromised or exposed.

At runtime, Terraform Cloud authenticates providers by exchanging an OIDC token for these short-lived, just-in-time credentials. These credentials typically have a very short Time-to-Live (TTL), often just minutes, and are automatically destroyed once the Terraform run concludes. This ensures that no static API keys, manual rotations, or vault-managed secrets are persistently stored within Terraform state or environment variables.

Links:

- [[Authentication Summary for AKS, EKS, and Terraform Cloud]]
- OIDC Workload Identity
- Zero Trust Security Principles
- Secure CI/CD Practices
- Modern Cloud-Native Authentication MOC
