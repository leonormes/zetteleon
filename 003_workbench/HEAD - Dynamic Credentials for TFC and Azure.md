---
aliases: []
confidence:
created: 2025-12-08T00:00:00Z
epistemic:
last_reviewed:
modified: 2025-12-08T15:01:46Z
purpose: To figure out how to configure dynamic credentials for Terraform Cloud and Azure to remove static keys.
review_interval:
see_also: []
source_of_truth: []
status: defined
tags:
  - azure
  - head
  - security
  - terraform
  - thinking
title: HEAD - Dynamic Credentials for TFC and Azure
type: head
uid:
updated:
---

## The Spark
> [!abstract] The Spark (Contextual Wrapper)
Task: "research how to configure the dynamic credentials for tfc and azure."
We need to move away from long-lived service principal secrets for Terraform Cloud to improve security.

## My Current Model
- Currently using static Client ID / Secret in TFC variables.
- Goal: Use OIDC (OpenID Connect) federation between TFC and Azure.
- Assumption: TFC acts as an identity provider that Azure trusts.

## The Tension
- **Configuration Complexity:** I need to know the exact Azure AD resources (Federated Identity Credential) and TFC workspace settings required.
- **Scope:** Is this per workspace or global?

## The Next Test
- [ ] Find the official HashiCorp/Microsoft tutorial for "Terraform Cloud Azure Dynamic Credentials".
- [ ] Attempt to set up a POC in a sandbox workspace.
