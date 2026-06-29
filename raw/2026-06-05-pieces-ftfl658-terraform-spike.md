---
title: FTFL-658 — MKUH Terraform Failure Spike Investigation
created: 2026-06-05 13:52:21+00:00
source: pieces-ltm
pieces_ids:
- 9c005f05-45d6-4a43-8256-54ed7cf360ae
- 990f2d90-c3fa-4705-99df-0b1901f78e89
tags:
- raw
- pieces
permalink: llmeon/raw/2026-06-05-pieces-ftfl658-terraform-spike
---

# FTFL-658 — MKUH Terraform Failure Spike Investigation

## Asset 1 — User Prompt (13:52:21)

for ticket FTFL-658 I downloaded the terraform cloud plan and asked llm for a summary. What happened to that? The ticket says
Terraform runs for MKUH have been failing for over a month. This spike investigates the root cause and produces a safe remediation plan.

Goals:

Identify deployment differences — compare current Terraform state vs. expected state; surface any drift between environments or recent infra changes that correlate with the failures.
Assess infrastructure components — determine which existing MKUH infrastructure components should be retained, replaced, or removed.
Define what needs to change — document the specific Terraform config/module/provider changes required to restore successful runs.
Draft a rollout plan — outline a safe, staged approach to applying fixes that avoids any disruption to the MKUH live service.
Out of scope: Implementing the fix (that follows in a subsequent task).

Acceptance criteria:

- Root cause of Terraform failures documented
- List of infra components to keep/change/remove agreed
- Rollout plan reviewed and signed off by team
- Follow-up implementation ticket(s) created
Timebox: 2–3 days

## Asset 2 — Agent Synthesis (13:58:59)

Comprehensive answer delivered covering:

**Root Cause (already fixed):** A missing `argocd_path` attribute in `generators/variables.tf` caused the `templatefile` function to fail when rendering `jumpbox.tftpl`. Fixed 5 May 2026.

**Secondary Issues (remain open):** After the template fix, the plan succeeds but reveals significant infrastructure drift:
- Auth0 configuration deleted out-of-band — 6 Auth0 resources are gone
- AKS `workflows` node pool requires replace — immutable field changed
- Grafana Cloud policy token expired
- 11 resources modified out-of-band
- 6 new TFE variables for credential bootstrapping

**Risk Level:** 🟡 Medium (with 🔴 High sub-risks). Plan shows 17 to add, 13 to change, 1 to destroy.

**Staged Rollout Plan produced:** Phase 1 (pre-apply gates), Phase 2 (lower env test), Phase 3 (MKUH production apply), Phase 4 (post-apply verification), Phase 5 (guardrails).