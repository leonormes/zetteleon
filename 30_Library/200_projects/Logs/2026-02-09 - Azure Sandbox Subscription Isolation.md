---
created: 2026-02-09T16:20:00Z
modified: 2026-02-09T16:51:34+00:00
tags: [azure, fitfile, governance, subscription, troubleshooting]
title: 2026-02-09 - Azure Sandbox Subscription Isolation
type: project_log
---

## Context ("The Why")

The user needed to provision a "clean" Azure subscription for a sandbox environment that bypasses the organizational policies and RBAC assignments inherited by the `FITFILE` Management Group (MG). The goal was to ensure zero-toil isolation for testing without "contamination" from production-grade guardrails.

## Investigation Log

1. Hierarchy Discovery: Confirmed that `FITFILE` is a child of the `Tenant Root Group`. Any subscription under `FITFILE` or its children (`Landing Zones`, `Platform`) inherits all parent policies.
2. Permission Blockers:
    - RBAC: User was `Reader` on `FITFILE` but `Not Authorized` on the `Tenant Root Group`, preventing the creation of a sibling MG (e.g., `Sandbox`).
    - Billing: `az billing account list` returned empty, indicating the user lacked the Azure subscription creator role on the Invoice Section (MCA billing hierarchy).
3. CLI Failures: `az account alias list` failed due to a broken `mise` Python environment (missing `pip`), preventing the diagnosis of "ghost" Subscription Aliases causing "Already exists" errors.
4. Resolution Strategy:
    - Drafted a request for Jon Bradshaw to grant `Azure subscription creator` (Billing) and `Owner` on a new `Sandbox` MG directly under the Root.
    - Identified that `az rest` can be used as a fallback to query aliases when extensions fail.

## The Nugget (Infrastructure Insights)

- Billing!= Governance: In Azure MCA, Management Group `Owner` permissions are insufficient for subscription creation; you must have the Subscription Creator role in the Billing Hierarchy (Invoice Section).
- Stuck Aliases: The "Already exists" error on subscription creation is often a dangling Subscription Alias (a logical name reservation) rather than a visible subscription resource. Use `az account alias list` (or `az rest --url https://management.azure.com/providers/Microsoft.Subscription/aliases?api-version=2020-09-01`) to find and delete them.
- Root Isolation: To achieve a "clean" start in a heavily governed tenant, create a Management Group directly under the Tenant Root Group. You cannot "block" inheritance; you must move to a sibling branch.

## Related Knowledge

- [[SoT - FitFile Deployment - Strategy & Architecture]]: Describes the canonical Management Group structure.
- [[SoT - Azure Kubernetes Service (AKS) Operations]]: Related to cross-tenant identity issues.

## Mentioned In

- [[Clean Azure Subscription Creation]] (Original Workbench Note)
