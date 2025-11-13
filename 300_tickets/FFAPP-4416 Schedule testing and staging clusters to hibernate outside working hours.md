---
aliases: []
confidence:
created: 2025-11-13T11:42:04Z
epistemic:
last_reviewed:
llm-action: redirect-created
modified: 2025-11-13T16:06:43Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status: superseded
superseded-by: "[[Automated Cloud Resource Hibernation SoT]]"
tags: []
title: FFAPP-4416 Schedule testing and staging clusters to hibernate outside working hours
type: ticket
uid:
updated:
---

This note's unique thinking has been integrated into [[Automated Cloud Resource Hibernation SoT]] on 2025-11-13.

Of course, here is a summary of the work to implement auto-shutdown scheduling for the testing and staging AKS clusters as per ticket **FFAPP-4416 Schedule testing and staging clusters to hibernate outside working hours**

This work is part of a wider cost-saving initiative tracked under the **FFAPP-4315** (Azure Production Cost Optimization) ticket, which I saw on the [Jira board earlier today](https://comet.scriven.ai/ui/link/9079a405-b049-436f-b27b-58679f223126). The goal is to power down these non-production clusters outside of working hours (6 am to 9 pm, Monday to Friday).

The implementation relies on our private `aks-automation` Terraform module, which is available in our [HCP Terraform registry](https://comet.scriven.ai/ui/link/a73c9f2b-980b-466d-a7f2-1a48c413b5fc). This module creates an Azure Automation Account with runbooks and schedules to start and stop an AKS cluster.

Here is a breakdown of the work for each cluster:

## Staging Cluster

The scheduling for the staging cluster has been configured and is awaiting final application.

-   **Merge Request:** The changes were introduced in GitLab merge request [!11 FFAPP-4418 turn on schedule for the staging cluster](https://comet.scriven.ai/ui/link/be788220-3b02-4ed0-9993-9c5957b42790). This MR has already been **merged into `master`**.
-   **Terraform Configuration:** The `aks_automation` module was added to the Terraform configuration for the `staging-cluster-v2` workspace. The module is configured with the requested schedule:
    -   `start_time`: `2025-11-14T06:00:00Z` (6 am UTC)
    -   `stop_time`: `2025-11-14T21:00:00Z` (9 pm UTC)
-   **Terraform Cloud Run:** The merge triggered the run [run-Kievm5hcTNinJX5n](https://comet.scriven.ai/ui/link/987c2b3d-1a06-4447-b286-9a2f26038fdc) in HCP Terraform, which is currently in an **"Apply pending"** state. Once applied, it will create 7 new Azure resources to manage the schedule.

## Testing Cluster

Work for the testing cluster is in progress and currently under review.

-   **Merge Request:** You are working on this under the branch `feature/FFAPP-4416-schedule-testing-and-staging-clusters-to-hibernation`. The work seems to have been combined with backup configuration changes in merge request [!12 FFAPP-4418 add backup config for testing-cluster](https://comet.scriven.ai/ui/link/8118080f-9017-48f8-b39d-21010368812c).
-   **Terraform Configuration:** The configuration for the testing cluster in [central-services/main.tf](file:///Volumes/DAL/Zettelkasten/LLMeon/central-services/main.tf) has also been updated to include the `aks_automation` module.
-   **Terraform Cloud Run:** The pull request triggered a plan-only run, [run-VyrCRfz3jajBHftR](https://comet.scriven.ai/ui/link/20967523-96b6-455b-8007-88ca9e3347f3), for the `test-cluster` workspace. The plan shows it will add resources for both the backup and automation.
-   **Status:** This MR is awaiting review and approval before it can be merged and the changes applied.

In short, the staging cluster work is merged and just needs to be applied in Terraform Cloud, while the testing cluster work is configured and awaiting merge request approval. Let me know if you need any more details
