---
aliases: [IAM GitOps, Infrastructure as Code Permissions, PIM via Terraform, Temporal Permissions]
created: 2025-12-30T12:02:15+00:00
modified: 2026-07-13T08:52:49+00:00
permalink: llmeon/30-library/so-t/so-t-git-ops-for-iam-and-permissions
tags: [gitops, iam, SoftwareEngineering/Architecture, SoftwareEngineering/Security, type_theory]
title: SoT - GitOps for IAM and Permissions
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 1. The Core Principle: Repository as Authority

In a GitOps IAM model, the Git Repository is the sole Source of Truth for _who_ can do _what_.

- Anti-Pattern: ClickOps (changing roles in Azure Portal).
- Pattern: All assignments are defined as code. If it's not in Git, it doesn't exist.

---

## 2. Repo Security as Type Safety

We treat the Git Repository not just as storage, but as a State Machine that enforces invariants.

| GitOps Mechanism | Type Theory Equivalent | Function |
|:--- |:--- |:--- |
| Branch Protection | Immutable Types | Prevents direct mutation of the "Production State" (Main Branch). |
| Merge Request | State Transition | A formal proposal to transition from `State A` to `State B`. |
| Code Review | Witness Generation | An approval is a cryptographic "Witness" required to validly construct the new state. |
| Signed Commits | Origin Authentication | Proof of Authorship attached to the data type. |

---

## 3. Temporal Permissions (PIM as Leased Types)

Static permissions (`User has Admin`) are dangerous because they are unbounded. We replace them with Leased Types (Privileged Identity Management).

### The Concept: `Lease<Role>`

Instead of assigning a Role, we assign Eligibility.

- Static: `User -> Admin` (Always on).
- Temporal: `User -> Eligible<Admin>` (Can request activation).

### Implementation (Terraform + PIM)

We use Terraform to define the Eligibility, not the active assignment.

```hcl
# We do NOT assign the role directly.
# We assign the *Right to Request* the role.
resource "azuread_directory_role_eligibility_schedule_request" "pjm_admin" {
  role_definition_id = "global-admin-id"
  principal_id       = "user-id"
  justification      = "Emergency Access"
  
  # The Type Constraint: Duration
  schedule {
    expiration {
      duration = "PT2H" # 2 Hours Max
    }
  }
}
```

The Safety Guarantee:

The "Admin" state is ephemeral. It automatically decays back to "User" state after $T$ time. This eliminates "Permission Drift" (forgotten admins).

---

## 4. The Approval Witness

To execute a privileged change, we require a Witness (Proof of Approval).

1. The Proposal: Developer creates a PR to add `User A` to `Group B`.
2. The Verification: CI runs `terraform plan`.
3. The Witness: A Security Officer approves the PR.
    - _Crucial:_ The CI pipeline should enforce that `Approve_Count >= 1` before allowing the merge.
4. The Execution: The pipeline applies the change.

---

## 5. Minimum Viable Understanding (MVU)

1. No ClickOps: IAM changes must be PRs.
2. Leased Access: Prefer `Eligible` (PIM) over `Active` (Permanent) assignments.
3. Two-Person Rule: No IAM change happens without a second pair of eyes (Witness).
