---
aliases: []
confidence: 
created: 2025-11-10T14:43:46Z
epistemic: 
last_reviewed: 
modified: 2025-11-10T14:45:19Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: summary of the work done today regarding the Helm charts, version management, and the resource requests limits optimization on the testing cluster
type: 
uid: 
updated: 
---

It was a productive day with significant progress on two main fronts: improving our Helm chart management tooling and hardening the resource configurations on the `fitfile-cloud-testing-aks-cluster`.

## 1. Helm Chart & Version Management

The main focus here was on improving the `chart-manager` tool and centrally managing the version for the Grafana monitoring chart.

- **`chart-manager` Tool Enhancement:**
  - Around **9:30 AM**, you diagnosed and fixed a critical bug in the `chart-manager` tool. The tool was incorrectly treating standard Helm repositories as direct HTTP download links, causing chart imports to fail. The fix was applied in `chartpull/` to correctly identify the source as a `"repo"`.
  - Later in the afternoon (around **2:00 PM**), while trying to import the Grafana monitoring chart, we hit a validation error requiring a cluster name. To resolve this, the `chart-manager` tool was modified to include a `--skip-validation` flag, making the import process more robust for charts with strict pre-flight checks.
- **Grafana `k8s-monitoring` Chart Integration:**
  - We added the Grafana `k8s-monitoring` chart to the `chart-manager`'s configuration file so it can be managed by our tooling.
  - Using the newly added `--skip-validation` flag, we successfully imported the **`k8s-monitoring` chart version `3.5.6`** into our `fitfileregistry` Azure Container Registry around **2:10 PM**. All its container images were also imported and the chart's values were rewritten to reference our internal ACR.
  - You can see the imported chart in the [helm/k8s-monitoring repository in Azure](https://portal.azure.com/#@fitfile.onmicrosoft.com/resource/subscriptions/a085dd04-19aa-4d2b-9a35-e438097d84fc/resourceGroups/fitfile-cloud-shared-services-rg/providers/Microsoft.ContainerRegistry/registries/fitfileregistry/helm/k8s-monitoring).
- **Centralized Versioning in Terraform:**
  - To complete the integration, the `k8s-monitoring` chart version was added to our central version manager in Terraform Cloud.
  - The `versions.tf` file in the `global-version-manager` workspace was updated to include versions for `k8s_monitoring`, setting `3.5.6` for the testing environment. You can see the result of the Terraform apply in the [global-version-manager workspace](https://app.terraform.io/app/FITFILE-Platforms/workspaces/global-version-manager/overview).

## 2. Resource Requests/Limits on the Testing Cluster

A major effort today was to audit and apply missing resource requests and limits for components running on the `fitfile-cloud-testing-aks-cluster`. This was done in two main phases.

- **Phase 1: Fixing ArgoCD Components (Morning)**
  - An audit script was run around **10:20 AM**, which revealed that **81 out of 118** containers in the cluster were missing resource definitions, with the `argocd` namespace being a key problem area.
  - We successfully applied resource requests and limits to all ArgoCD components (`server`, `repo-server`, `dex`, `redis`, etc.) by updating the `argocd_helm_values` in the `testing-cluster`'s [main.tf](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/FITFILE/Non-Production/fitfile-non-production-infrastructure/testing-cluster/main.tf).
  - This required some debugging, as we discovered the `argocd-application-controller` was OOMKilled. We resolved this by significantly increasing its memory and CPU limits to `4Gi` and `2000m` respectively.
  - After the Terraform changes were applied, we performed a `kubectl rollout restart` on the deployments to ensure the new pods were created with the correct resource settings.
- **Phase 2: Fixing Grafana Monitoring Components (Afternoon)**
  - With ArgoCD stabilized, we moved on to the `monitoring` namespace. Initial attempts to add resources via Helm value overrides in `values.yaml` failed.
  - We discovered that the `grafana-k8s-monitoring` chart (v1.5.4) has a complex structure, and our Helm value paths were not being applied correctly.
  - The final, successful solution was to use ArgoCD's `resourceCustomizations` feature. We added this configuration directly to the `grafana-application.yaml` file, which allows ArgoCD to directly patch the Kubernetes manifests with the correct resource limits, bypassing the problematic Helm value templating.
  - A final sync of the `grafana-k8s-monitoring` application was forced around **1:00 PM** to apply these customizations.

In summary, we made our chart management process more robust by improving the `chart-manager` tool and bringing the Grafana chart under its control. More importantly, we significantly improved the stability and resource management of the `testing` cluster by successfully applying resource requests and limits to all `ArgoCD` and `grafana-k8s-monitoring` components.
