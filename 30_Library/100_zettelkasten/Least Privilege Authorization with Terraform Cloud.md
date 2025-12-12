---
aliases: []
confidence: 
created: 2025-10-24T15:37:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [authorization, IAM, least-privilege, RBAC, security]
title: Least Privilege Authorization with Terraform Cloud
type:
uid: 
updated: 
version:
---

Applying the principle of **least privilege** is critical when configuring authorization for Terraform Cloud, especially when using [[Dynamic Provider Credentials (DPC) in Terraform Cloud|Dynamic Provider Credentials]]. This means granting only the minimum necessary permissions for Terraform runs to perform their intended operations, and nothing more.

Key practices for least privilege authorization:

- **Per-Workspace IAM Roles:** Create narrowly-scoped IAM roles (for AWS), Azure RBAC roles, or GCP IAM policies for each Terraform workspace. These roles should be specific to the environment (e.g., `terraform-dev-role`, `terraform-prod-role`) and the resources managed by that workspace.
- **Isolate Access:** Strictly limit each workspace to only the resources it provisions or manages. Avoid using shared accounts or broad, cross-environment roles, as this can lead to privilege escalation and wider impact in case of compromise.
- **Granular Permissions:** Define permissions at the most granular level possible. For example, instead of granting `s3:*`, grant `s3:GetObject`, `s3:PutObject` only to specific buckets.

By implementing least privilege, you significantly reduce the potential blast radius of a compromised credential or a misconfigured Terraform run, enhancing the overall security posture of your infrastructure-as-code deployments.

Links:

- [[Dynamic Provider Credentials (DPC) in Terraform Cloud]]
- Least Privilege Principle
- AWS IAM Roles
- Azure RBAC
- GCP IAM
- [[Recommended Best Practices for Cloud-Native Authentication]]
- Modern Cloud-Native Authentication MOC
