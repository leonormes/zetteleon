---
aliases: []
confidence: 
created: 2025-10-24T15:38:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [agents, CICD, ephemeral-infrastructure, security]
title: Ephemeral Agents and Environments in Terraform Cloud
type:
uid: 
updated: 
version:
---

When utilizing Terraform Cloud Agents, especially in conjunction with [[Dynamic Provider Credentials (DPC) in Terraform Cloud|Dynamic Provider Credentials]], it is a critical security best practice to ensure that these agents operate within **ephemeral environments**.

Key considerations for ephemeral agents and environments:

- **Agent Version:** Ensure agents are running version **v1.7.0+** to fully support dynamic credentials and their associated security features.
- **Ephemeral Compute:** All plan and apply operations should be performed in ephemeral compute environments. This means the underlying infrastructure (e.g., virtual machines, containers) hosting the agent is provisioned for a single run and then **destroyed** immediately after execution.
- **No Retained Exposure:** By destroying the compute environment post-run, any potential retained token exposure is prevented. This eliminates the risk of residual credentials lingering on agent infrastructure, even if they are short-lived.

This approach reinforces the Zero Trust model by ensuring that the execution environment itself is transient and clean for each operation, minimizing potential attack vectors.

Links:

- [[Dynamic Provider Credentials (DPC) in Terraform Cloud]]
- Ephemeral Infrastructure
- Secure CI/CD Practices
- [[Recommended Best Practices for Cloud-Native Authentication]]
- Modern Cloud-Native Authentication MOC
