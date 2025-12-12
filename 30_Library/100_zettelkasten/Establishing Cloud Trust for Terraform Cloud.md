---
aliases: []
confidence: 
created: 2025-10-24T15:36:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [AWS, Azure, GCP, identity-federation, OIDC, security]
title: Establishing Cloud Trust for Terraform Cloud
type:
uid: 
updated: 
version:
---

To enable Terraform Cloud to use [[Dynamic Provider Credentials (DPC) in Terraform Cloud|Dynamic Provider Credentials]], a crucial step is to establish a trust relationship between Terraform Cloud and your cloud provider. This allows the cloud provider to recognize Terraform Cloud as a trusted identity provider, enabling the exchange of OIDC tokens for short-lived credentials.

Configuration steps for major cloud providers:

- **AWS:** Create an IAM role with a trust policy that explicitly permits Terraform Cloud's OIDC issuer (`app.terraform.io`) to assume the role. This IAM role will have the necessary permissions for Terraform operations.
- **Azure:** Utilize **Workload Identity Federation** with an Azure Entra ID (formerly Azure AD) app registration. This app registration is configured to trust Terraform Cloud's OIDC issuer, allowing it to exchange OIDC tokens for Azure access tokens.
- **GCP:** Configure **Workload Identity Pools** within Google Cloud Platform. This involves setting up a pool that trusts Terraform Cloud's OIDC provider, enabling secure, token-based authentication for Terraform runs.

This trust relationship is fundamental for a secure, passwordless, and ephemeral authentication flow in Terraform Cloud.

Links:

- [[Dynamic Provider Credentials (DPC) in Terraform Cloud]]
- Terraform Cloud OIDC Integration
- AWS IAM Roles for OIDC
- Azure Workload Identity Federation
- GCP Workload Identity Pools
- Modern Cloud-Native Authentication MOC
