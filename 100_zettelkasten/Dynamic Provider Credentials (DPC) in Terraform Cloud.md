---
aliases: []
confidence: 
created: 2025-10-24T15:35:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [authentication, DPC, OIDC, security, short-lived-credentials]
title: Dynamic Provider Credentials (DPC) in Terraform Cloud
type:
uid: 
updated: 
version:
---

**Dynamic Provider Credentials (DPC)** is a key feature in Terraform Cloud (now HCP Terraform) designed to eliminate static credentials for cloud providers and other services. It should be the default authentication mechanism for all major cloud providers (AWS, Azure, GCP) and HashiCorp Vault integrations.

How DPC works:

- **Workload Identity Token:** DPC authenticates Terraform runs by utilizing a **workload identity token** that is signed via OpenID Connect (OIDC).
- **Unique, Short-Lived Credentials:** Each Terraform run is provisioned with a **unique, short-lived credential**, typically valid for only a few minutes. These credentials are automatically destroyed after the run completes.
- **No Static Storage:** Providers never store static credentials within Terraform state files or environment variables, significantly reducing the risk of exposure.

This mechanism ensures that access is granted just-in-time and is ephemeral, aligning with modern security best practices and minimizing the attack surface.

Links:

- [[Short-Lived Credentials Core Principle in Terraform Cloud]]
- OIDC Workload Identity
- [[Recommended Best Practices for Cloud-Native Authentication]]
- Modern Cloud-Native Authentication MOC
