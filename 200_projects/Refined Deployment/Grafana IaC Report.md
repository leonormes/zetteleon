---
aliases: []
confidence: 
created: 2025-10-10T11:03:37Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Grafana IaC Report
type:
uid: 
updated: 
version:
---

## Grafana IaC Analysis Report

Below is a structured analysis of the Terraform codebase in [central-services/grafana/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana:0:0-0:0), with findings and targeted improvements. I validated usage against Grafana provider docs (context7: `/grafana/terraform-provider-grafana`) and cited the relevant files inline.

## Findings

- **Purpose**
  - Manages Grafana Cloud org-level resources and stack-level assets:
    - Stacks and service accounts: [stacks.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/stacks.tf:0:0-0:0)
    - Access policies and tokens (agents + automation): [access_policies.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/access_policies.tf:0:0-0:0)
    - Data sources (Loki + Prometheus lookup): [data_sources.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/data_sources.tf:0:0-0:0)
    - Folders and dashboards: [folders.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/folders.tf:0:0-0:0), [dashboards.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/dashboards.tf:0:0-0:0), [dashboards/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/dashboards:0:0-0:0)
    - Alerting rules (rule groups): [alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts.tf:0:0-0:0), [alerts/kubernetes-cluster-resource-alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts/kubernetes-cluster-resource-alerts.tf:0:0-0:0)
    - Contact points, templates, and notification policy: [contact_points.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/contact_points.tf:0:0-0:0), [notification_template.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/notification_template.tf:0:0-0:0), [notification_policy.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/notification_policy.tf:0:0-0:0)
    - Grafana OnCall integration and schedules: [onCall.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/onCall.tf:0:0-0:0)
    - Plugins: [plugins.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/plugins.tf:0:0-0:0)
    - Variables/outputs: [vars.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/vars.tf:0:0-0:0), [outputs.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/outputs.tf:0:0-0:0)
    - Terraform Cloud workspace config: [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0)
- **[Terraform Cloud integration]**
  - Uses Terraform Cloud with org/project/workspace set: [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0) (`terraform { cloud { ... } }`).
  - Provider pinned to `grafana/grafana` 3.7.0: [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0) (`required_providers`).
- **[Providers and auth model]**
  - Org-level (Grafana Cloud) via access policy token:
    - `provider "grafana" { alias = "cloud"; cloud_access_policy_token = var.cloud_access_policy_token }` in [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0)
  - Stack-level providers per environment:
    - `grafana.non_prod_stack`, `grafana.prod_stack` configured with `url` and `auth` from stack resources/tokens: [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0)
    - OnCall provider: `grafana.oncall` with `oncall_url` and `oncall_access_token`: [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0)
  - Note: There’s also `grafana.uhb_wm_1_stack` referencing resources that don’t exist in repo: [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0) lines 36-41.
- **[Stacks and service accounts]**
  - Creates non-prod and prod stacks and SA tokens: [stacks.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/stacks.tf:0:0-0:0)
    - `grafana_cloud_stack.*`, `grafana_cloud_stack_service_account.*`, `grafana_cloud_stack_service_account_token.*`
  - Demonstrates a dynamic stack-level provider `grafana.my_stack` referencing those resources, then creates a folder: [stacks.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/stacks.tf:0:0-0:0) lines 64-75.
- **[Access policies and token issuance]**
  - Cluster/agent write policies (non-prod/prod) plus per-deployment tokens using locals maps: [access_policies.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/access_policies.tf:0:0-0:0), [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/locals.tf:0:0-0:0)
  - Terraform automation policy and token (org-level): [access_policies.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/access_policies.tf:0:0-0:0) lines 57-78
  - Rich outputs for Prom/Loki/Tempo endpoints and the automation token: [outputs.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/outputs.tf:0:0-0:0)
- **[Data sources]**
  - Reads non-prod Prometheus as data source: `data "grafana_data_source" "non_prod_prometheus"` in [data_sources.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/data_sources.tf:0:0-0:0)
  - Creates non-prod Loki as a managed data source with derivedFields (traceID): `resource "grafana_data_source" "non_prod_loki"` in [data_sources.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/data_sources.tf:0:0-0:0)
- **[Dashboards]**
  - Kubernetes pod health dashboards (simple native panels; Polystat currently disabled): [dashboards.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/dashboards.tf:0:0-0:0), `dashboards/kubernetes-pod-health*.json`
  - Separate folders for non-prod/prod dashboards: [dashboards.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/dashboards.tf:0:0-0:0)
- **[Alerting]**
  - A comprehensive set of rule groups targeting:
    - Workflow and ArgoCD application state: [alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts.tf:0:0-0:0)
    - Mesh/API log errors, MongoDB exporter errors, Pod restart loops, Calico infra checks, K8s API deprecations: [alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts.tf:0:0-0:0)
    - Cluster capacity/optimization alerts parameterized by a Prom datasource UID: [alerts/kubernetes-cluster-resource-alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts/kubernetes-cluster-resource-alerts.tf:0:0-0:0) (exposes `variable "prometheus_datasource_uid"`)
  - Uses Grafana’s unified alerting constructs: `grafana_rule_group` with `notification_settings`, `labels`, `annotations` (aligned with docs).
- **[Contact points, notification policy, templates]**
  - OnCall contact point with webhook link: [contact_points.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/contact_points.tf:0:0-0:0)
  - Notification policy routing (non-prod): [notification_policy.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/notification_policy.tf:0:0-0:0)
  - Grafana message templates for Slack: [notification_template.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/notification_template.tf:0:0-0:0)
- **[Grafana OnCall]**
  - Integration, schedule, escalation chain, and notification steps: [onCall.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/onCall.tf:0:0-0:0)
  - Fetches OnCall users by email (`data "grafana_oncall_user"`) driven by `locals.users`: [onCall.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/onCall.tf:0:0-0:0)
- **[Variables/locals/outputs]**
  - [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/locals.tf:0:0-0:0) defines deployments mapping -> token issuance per cluster (`local.deployments`, `local.{non_prod,prod}_deployments`)
  - [vars.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/vars.tf:0:0-0:0) defines tokens and some URLs; several var names use hyphens and look unused
  - [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/main.tf:0:0-0:0) is empty

## Issues and Risks

- **[Bootstrap dependency in provider configurations]**
  - Providers `grafana.non_prod_stack`, `grafana.prod_stack`, and `grafana.my_stack` reference attributes of resources created in the same run (e.g., `grafana_cloud_stack.*.url`, service account tokens) in [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0) and [stacks.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/stacks.tf:0:0-0:0).
  - Provider configurations must be known during planning; referencing resources often causes bootstrapping/cycle issues on first apply. This pattern typically works only after an initial bootstrap (values already in state).
  - Recommendation: split bootstrap (org/stack/SA/token) from stack resource management into separate workspaces, or provide stack URLs/tokens via TFC variables/remote state.
- **[Undefined provider alias usage]**
  - `provider "grafana" { alias = "uhb_wm_1_stack" ... }` in [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0) references `grafana_cloud_stack.uhb_wm_1_stack` and `grafana_cloud_stack_service_account_token.uhb_wm_1_cloud_sa_token`, which do not exist in the repo. This will fail planning unless they exist in state from elsewhere.
- **[Secrets exposed in comments]**
  - [contact_points.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/contact_points.tf:0:0-0:0) contains a commented Slack webhook URL (lines 5-7). Even commented, it’s in the repo. This is a security risk and should be removed or templated.
- **[Inconsistent datasource references]**
  - Some alerts use literal `datasource_uid = "grafanacloud-prom"` or `"grafanacloud-logs"` ([alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts.tf:0:0-0:0)), while others use data-source resources/variables. This is brittle across stacks and migrations.
- **[Hyphenated variable names and unused vars]**
  - [vars.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/vars.tf:0:0-0:0) includes several variables with hyphens (`cluster-name`, `prometheus-username`, `prometheus-url`, `loki-username`, `loki-url`, `cloud-access-token`), many seemingly unused. Hyphens complicate references (require bracket syntax) and should be avoided.
- **[Environment coverage asymmetry]**
  - Alert rule groups and contact points target non-prod in many places (`provider = grafana.non_prod_stack`). Production equivalents are defined for dashboards/folders but alerting/notification policies appear focused on non-prod.
- **[Provider version pinning]**
  - Pinned to [grafana](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana:0:0-0:0) provider `3.7.0`: [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0). This is fine, but consider a `~>` constraint and periodic updates (with lockfile control), as new alerting/OnCall features are actively added.
- **[org_id hardcoded]**
  - Some rule groups set `org_id = 1` (e.g., [alerts/kubernetes-cluster-resource-alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts/kubernetes-cluster-resource-alerts.tf:0:0-0:0)). In Grafana Cloud this can be implicit via the authenticated stack; consider removing to avoid mismatches.
- **[Plugins managed as “no-op”]**
  - [plugins.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/plugins.tf:0:0-0:0) sets `prevent_destroy = true` and `ignore_changes = all` for `grafana_cloud_plugin_installation`. If the provider supports managing that plugin for your plans, prefer true declarative management (or remove if intentionally manual-only).

## Areas for Improvement

- **[Split bootstrap from runtime management]**
  - Create two TFC workspaces (or modules):
    - Bootstrap: org-level `grafana.cloud` resources (`grafana_cloud_stack`, SAs/tokens, access policies/tokens).
    - Runtime: stack-level resources (folders, data sources, dashboards, alerting, contact points, templates, OnCall).
  - Supply runtime with `url` and token via:
    - TFC workspace variables (sensitive), or
    - Remote state outputs from the bootstrap workspace.
  - This aligns with Terraform best practices and avoids cyclic provider config dependencies.
- **[Remove undefined provider alias or add missing resources]**
  - Either remove `grafana.uhb_wm_1_stack` from [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0) or define the corresponding stack/SA resources in [stacks.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/stacks.tf:0:0-0:0).
- **[Harden secrets handling]**
  - Delete the commented Slack webhook from [contact_points.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/contact_points.tf:0:0-0:0). If needed, drive via variable (`TF_VAR_slack_webhook_url`) in TFC. Never commit real webhooks.
- **[Normalize data source usage]**
  - Replace hardcoded `datasource_uid` strings with:
    - Prometheus: `data.grafana_data_source.non_prod_prometheus.uid` (or equivalent for prod).
    - Loki: `grafana_data_source.non_prod_loki.uid` (or a data source lookup if not managing DS in TF).
  - For reusable alert modules such as [alerts/kubernetes-cluster-resource-alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts/kubernetes-cluster-resource-alerts.tf:0:0-0:0), pass `prometheus_datasource_uid` from a single central data source lookup to avoid drift.
- **[Fix variable names and remove unused vars]**
  - Rename hyphenated variables in [vars.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/vars.tf:0:0-0:0) to underscores, e.g., `cluster_name`, `prometheus_username`, etc. Remove unused variables to reduce confusion.
  - Add `required_version` in [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0) (e.g., `>= 1.5.0`) and consider a `versions.tf` for clarity (or keep provider block consolidated if that’s the style across repos).
- **[Environment parity for alerting]**
  - Introduce production-equivalent alert rule groups, contact points, and notification policies. Parameterize by provider alias (non-prod/prod) and share HCL modules where possible.
- **[Policy scoping review]**
  - Validate `local.scopes` and `local.terraform_scopes` in [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/locals.tf:0:0-0:0) against least-privilege principles (e.g., “read” scopes included where not needed).
  - Confirm tokens in [access_policies.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/access_policies.tf:0:0-0:0) are unique per deployment and rotated through TFC processes.
- **[Tidy the repo]**
  - Remove [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/main.tf:0:0-0:0) if intentionally unused or move a high-level structure comment into it to reduce confusion.
  - Consider grouping alert rule groups into modules (e.g., `modules/alerts/*`) and instantiating per environment to DRY repeated patterns (notification settings, labels, intervals).
- **[Provider version lifecycle]**
  - Keep the [.terraform.lock.hcl](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/.terraform.lock.hcl:0:0-0:0) updated via Renovate/Dependabot and pin providers with a compatible range (e.g., `~> 3.7`) to receive patch updates. Validate against the current provider docs before upgrading (alerting and OnCall evolve quickly).

## Notable File References

- [provider.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/provider.tf:0:0-0:0): TFC config, provider versions, aliases for `cloud`, `non_prod_stack`, `prod_stack`, `oncall`, and `uhb_wm_1_stack`.
- [stacks.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/stacks.tf:0:0-0:0): `grafana_cloud_stack` resources, service accounts/tokens, dynamic provider example (`grafana.my_stack`).
- [access_policies.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/access_policies.tf:0:0-0:0): non-prod/prod agent write policies, per-deployment tokens, Terraform automation policy/token.
- [data_sources.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/data_sources.tf:0:0-0:0): non-prod Prometheus datasource (data), non-prod Loki datasource (managed).
- [dashboards.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/dashboards.tf:0:0-0:0) and [dashboards/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/dashboards:0:0-0:0): Kubernetes dashboards (simple and polystat variant disabled).
- [alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts.tf:0:0-0:0): workflow, ArgoCD, mesh, MongoDB, pod restarts, Calico, K8s API deprecation alerts.
- [alerts/kubernetes-cluster-resource-alerts.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/alerts/kubernetes-cluster-resource-alerts.tf:0:0-0:0): capacity/optimization rule groups with parameterized Prometheus UID.
- [contact_points.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/contact_points.tf:0:0-0:0), [notification_policy.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/notification_policy.tf:0:0-0:0), [notification_template.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/notification_template.tf:0:0-0:0): routing and Slack templates.
- [onCall.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/onCall.tf:0:0-0:0): OnCall integration, schedule, escalation chain, and notification rules.
- [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/locals.tf:0:0-0:0): deployments map and token scoping logic.
- [vars.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/vars.tf:0:0-0:0): variables (some hyphenated, some unused).
- [outputs.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/outputs.tf:0:0-0:0): endpoint outputs and automation token + usage instructions.

## Recommended Next Steps

- **[High]** Split bootstrapping vs runtime management workspaces; pass stack URL/token via TFC variables or remote state; remove provider references to TF-managed resources in provider blocks.
- **[High]** Remove or fix `grafana.uhb_wm_1_stack` provider alias.
- **[High]** Remove the commented Slack webhook from [contact_points.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/contact_points.tf:0:0-0:0); replace with a variable.
- **[Medium]** Standardize `datasource_uid` usage via data sources/variables and apply to all alerts.
- **[Medium]** Rename hyphenated variables in [vars.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana/vars.tf:0:0-0:0), delete unused ones, add `required_version`.
- **[Medium]** Achieve environment parity for alerting and notification policies (add prod equivalents).
- **[Low]** Consider refactoring alerts into modules; keep provider pinned with a reasonable range and set up automated updates.

## Task Completion Status

- Analysis completed using the context-engine MCP across all key files in [central-services/grafana/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/grafana:0:0-0:0).
- Best-practice validation cross-checked with Grafana provider docs (context7).
- Concrete improvement plan provided with prioritized actions. If you want, I can implement the bootstrap/runtime workspace split and normalize datasource and secrets handling in follow-up commits.
