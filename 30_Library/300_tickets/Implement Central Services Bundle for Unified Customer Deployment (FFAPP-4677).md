---
key: FFAPP-4677
summary: Implement Central Services Bundle for Unified Customer Deployment
status: In Progress
assignee:
tags:
project: FFAPP
issuetype: Story
priority: Medium
reporter:
created: 2025-12-10T14:35:41.801+0000
updated: 2025-12-18T12:27:25.858+0000
url:
---

# `jira-sync-line-summary`Implement Central Services Bundle for Unified Customer Deployment

**Key:** `jira-sync-line-key`FFAPP-4677
**Type:** `jira-sync-line-issuetype`Story
**Status:** `jira-sync-line-status`In Progress
**Priority:** `jira-sync-line-priority`Medium
**Assignee:** `jira-sync-line-assignee`
**Reporter:** `jira-sync-line-reporter`
**Link:** [Open in Jira]({url})

## Description
`jira-sync-section-description`
**Goal**: Eliminate manual operational toil when setting up new customers by creating a "Central Services Bundle" that orchestrates all core services (Auth0, GitLab, TFC, Vault) from a single consumer module with minimal configuration.

**Key Components**:

** **Unified Module*: `terraform-fitfile-central-services-consumer` acts as the single entry point.
** **Minimal Config*: Inputs are reduced to `customer*name`, `deployment*key`, and `environment`.
** **Secret Automation*: Vault secrets (`application`) are automatically populated with generated passwords and external keys (UDE, OpenSSL).
** **Flexible Naming*: Supports consumer-defined naming conventions (e.g., LCRCA) via a `names` map input.
** **Partner APIs*: Auth0 clients are automatically authorized for partner APIs (`enabled_apis`).

**Ultimate Goal**: "Central Services from Input Config" - A new customer deployment requires only a single `main.tf` file and a `secrets.json`, with no manual UI clicking in Auth0, GitLab, or TFC.

**Pilot**: Liverpool City Authority (LCA-DP).
## Comments