---
aliases: [Automated Privilege Management, GitOps PIM, JIT Access with IaC]
created: 2025-07-04T07:32:01+00:00
last_reviewed: null
modified: 2026-07-04T10:50:58+00:00
permalink: llmeon/30-library/so-t/so-t-git-ops-for-privileged-identity-management
status: Active
tags: [azure, gitops, iam, pim, security, terraform]
title: SoT - GitOps for Privileged Identity Management
type: SoT
updated: null
---

## SoT - GitOps for Privileged Identity Management

> Core Principle: Privileged access is not a static state; it is a temporary, time-bound lease granted via code. By treating access requests as Pull Requests (Intent) and leveraging IaC for provisioning (Implementation), we achieve automatic expiration, auditability, and Zero Trust enforcement.

### 1. The Architecture: Code-Based Access Request

#### The Workflow

1. Request (PR): A user submits a Pull Request to the IAM Repository proposing a temporary change to `access.tf` (e.g., adding themselves to the `PIM-Admin` group).
2. Validation (Policy): CI/CD pipelines trigger OPA (Open Policy Agent) to validate the request against policy (e.g., "Is the duration < 4 hours?", "Is this user eligible?").
3. Approval (Merge): A designated approver (or automated bot for low-risk) merges the PR.
4. Provisioning (Apply): Terraform applies the change, creating a Time-Bound Assignment in the Identity Provider (e.g., Entra ID).
5. Expiration (Automatic): The Identity Provider automatically revokes access when the time-to-live (TTL) expires. No manual cleanup is required.

### 2. Implementation Mechanics (Terraform & Entra ID)

We utilize specific Terraform resources that support TTL.

#### 2.1 Active vs. Eligible Assignments

- Active Assignment: The user _has_ the permission immediately upon merge.
    - _Resource:_ `azuread_privileged_access_group_assignment_schedule`
- Eligible Assignment: The user is _allowed to activate_ the permission (via portal/API) for a set duration.
    - _Resource:_ `azuread_privileged_access_group_eligibility_schedule`

#### 2.2 The Expiration Contract

Crucially, the IaC resource MUST define the `expiration`:

```hcl
resource "azuread_privileged_access_group_assignment_schedule" "temp_access" {
  group_id        = azuread_group.pim_admins.object_id
  principal_id    = data.azuread_user.requester.object_id
  assignment_type = "member"
  
  # The Core Mechanism: Automatic Expiration
  expiration {
    duration = "PT4H" # 4 Hours
    # OR
    end_date = "2025-12-31T23:59:59Z"
  }
}
```

### 3. Policy Enforcement (OPA Gatekeeper)

Before the PR is merged, Open Policy Agent (OPA) acts as the Policy Decision Point (PDP).

- Contextual Checks:
    - _Time:_ "Is this request within business hours?"
    - _Role:_ "Does this user have the 'On-Call' tag?"
    - _Duration:_ "Deny if requested duration > 8 hours."
- Result: The PR check fails if the policy is violated, preventing the IaC from ever being applied.

### 4. Why This is Zero Trust

1. Least Privilege: Access is zero by default; it is only granted when needed.
2. Verify Explicitly: Every request is authenticated (Git commit signature) and authorized (PR Approval + OPA).
3. Assume Breach: Access is ephemeral. If credentials are stolen after the window, they are useless.

### 5. Integration with ProdOS

- Domain III (Data-Centric Systems): Access is defined as data (HCL), not ad-hoc clicks.
- Domain IV (Generative Infra): The "Access Kernel" (Who/What/When) generates the complex PIM schedules.
