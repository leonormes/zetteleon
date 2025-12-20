---
aliases: []
confidence: 
created: 2024-11-26T16:59:12Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:50Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: updateing_the_argocd
type: 
uid: 
updated: 
version: 
---

## Updateing the ArgoCD Chart/Image

This is true for all our charts.

### Import the Public charts/images to Our Container Registry

#### Find Latest Version

`helm search repo argo-cd --versions`

#### Use Import Script

`/Fitfile/gitlab/FITFILE/deployment/scripts/import_chart_to_acr.sh`

```sh
./import_chart_to_acr.sh --repo-name argo-helm --repo-url https://argoproj.github.io/argo-helm --chart-name argo-cd --chart-version 7.7.5 --acr-name FITFILEPublic --chart-dir argoproj/argocd
```

This ends with us having a copy in our own repository. All the naming and versions are the same as the public one just a different path to repo.

`/Volumes/DAL/Fitfile/gitlab/FITFILE/Terraform Infrastructure/TFC-Modules/terraform-helm-fitfile-platform/argocd/main.tf`

```json
resource "helm_release" "argocd" {
  name = "argocd"
  chart = "helm/argo-cd"
  namespace = "argocd"
  version = "7.7.5" \<-- Here is the version to update
  repository = "oci://fitfilepublic.azurecr.io" \<-- our own repo
```

I made changes in the

I then added a new tag by incrementing the current one.

```sh
git describe --tags --abbrev=0
git tag '<the next version number>'
git push origin <tag_name>
```

This triggers a release of the terraform module in the registry.

Then update the version to this module in the terraform used to deploy the ffnode you are looking for. In my case `FITFILE/Terraform Infrastructure/Deploy/Non-Production/fitfile-non-production-infrastructure/staging-cluster-2/main.tf`

[patching_box](<../../Core/Deployment/patching_box.md>)

To get the tags for a particular image in your Azure Container Registry (ACR) using Azure CLI, you can run the following command:

```sh
az acr repository show-tags -n FITFILEPublic --repository argoproj/argocd --top 1 --orderby time_desc
[
  "v2.13.1"
]
```
