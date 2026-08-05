---
type: agent/briefing
title: Integration Test Pipeline DNS Failure — Context for LLM
actor: agent/hermes/v4
generated: '2026-08-05'
tags:
- pipeline
- dns
- aks
- integration-tests
- gitlab-runner
- ftfl-456
permalink: llmeon/wiki/2026-08-05-ftfl-integration-test-dns-context
---

# Context: Integration Test Pipeline DNS Failure

## Problem

The merge-train pipeline's integration test job (`run_integration_tests`) fails with a DNS resolution error when trying to connect to the AKS cluster:

```
Error: rpc error: code = Internal desc = Post "https://fitfile-cloud-testing-k8s-xja5tx3v.hcp.uksouth.azmk8s.io:443/apis/authorization.k8s.io/v1/selfsubjectaccessreviews": 
dial tcp: lookup fitfile-cloud-testing-k8s-xja5tx3v.hcp.uksouth.azmk8s.io on 169.254.169.254:53: no such host
```

## What we know

- The hostname `fitfile-cloud-testing-k8s-xja5tx3v.hcp.uksouth.azmk8s.io` is the **public FQDN** of the AKS cluster (confirmed via `az aks show`: `privateFqdn: None`)
- The hostname **IS publicly resolvable** — `nslookup` via 8.8.8.8 returns `20.49.231.142` (a public Azure IP)
- The cluster is **running** (`powerState: Running`)
- The DNS resolver `169.254.169.254:53` is the Azure Instance Metadata Service DNS — only reachable from within Azure VMs
- The GitLab runner is a **SaaS runner** (`green-7.saas-linux-small-amd64`) — NOT inside Azure, so it can't reach the Azure DNS at that IP
- The runner still tries `169.254.169.254` as its DNS resolver (from the container's `/etc/resolv.conf`)

## Pipeline Architecture (two repos)

### 1. InsightFILE repo (`fitfile/insightfile`)
The main application repo. The merge-train pipeline:
1. Runs verification jobs (unit tests, lint)
2. Builds Docker images for changed services
3. Triggers the **deployment repo** pipeline via `trigger_integration_tests` (defined in `staging-pipelines.yml`)

### 2. Deployment repo (`fitfile/deployment`)
The infrastructure repo. Its `staging.gitlab-ci.yml` defines the integration test flow:

**Job 1: `prepare_kube_config`**
- Image: `mcr.microsoft.com/azure-cli:latest`
- Runs `az aks get-credentials --name Fitfile-cloud-testing-aks-cluster --resource-group Fitfile-cloud-testing-rg --subscription $SUBSCRIPTION_ID --admin`
- Outputs `kubeconfig` artifact

**Job 2: `sync_argo_app`** (runs in parallel)
- Image: `fitfile/argocdsync:latest`
- Syncs ArgoCD app with built images

**Job 3: `run_integration_tests`** (after both above complete)
- Image: `fitfile/argocli:alpine` (Alpine-based with argo CLI)
- Copies kubeconfig from `prepare_kube_config` artifact
- Runs `argo list -n testing` → fails with DNS error
- Would then submit and wait for an Argo Workflow test suite

## Pipeline files

### Staging pipeline (triggers deployment repo)
`fitfile/insightfile/deployment/pipeline/staging-pipelines.yml`:
```yaml
trigger_integration_tests:
  stage: test
  needs:
    - get_staging_images
  variables:
    STAGING_VALUE_OVERRIDES: $STAGING_VALUE_OVERRIDES
  trigger:
    include:
      - project: fitfile/deployment
        ref: 'master'
        file: staging.gitlab-ci.yml
    strategy: depend
  resource_group: deployment-repo
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"
      changes:
        - 'apps/**/*'
        - 'packages/**/*'
        - 'Dockerfile*'
        - 'yarn.lock'
      when: on_success
    - when: never
```

### Integration test pipeline
`fitfile/deployment/staging.gitlab-ci.yml` (full file):
```yaml
stages:
  - prepare
  - deploy
  - test

variables:
  GIT_AUTH_TOKEN: "${CI_JOB_TOKEN}"
  FF_USE_FASTZIP: "true"
  ARTIFACT_COMPRESSION_LEVEL: "fast"
  CACHE_COMPRESSION_LEVEL: "fast"

prepare_kube_config:
  stage: prepare
  image: mcr.microsoft.com/azure-cli:latest
  resource_group: staging
  variables:
    SUBSCRIPTION_ID: 249df46b-f75d-4492-8e78-b33a00473548
    TENANT_ID: 45e73aa3-1ee9-47c0-ba25-54eda9da021a
    KUBECONFIG: "$CI_PROJECT_DIR/kubeconfig"
  script:
    - az login --service-principal -u $AZ_CLIENT_ID -p $AZ_CLIENT_SECRET --tenant $TENANT_ID
    - az login --service-principal -u $AZ_CLIENT_ID -p $AZ_CLIENT_SECRET --tenant 45e73aa3-1ee9-47c0-ba25-54eda9da021a
    - echo "Testing cluster"
    - az aks get-credentials --name Fitfile-cloud-testing-aks-cluster --resource-group Fitfile-cloud-testing-rg --subscription $SUBSCRIPTION_ID --admin
  artifacts:
    paths:
      - kubeconfig
  rules:
    - if: $CI

sync_argo_app:
  stage: deploy
  image:
    name: fitfile/argocdsync:latest
    entrypoint: [""]
  variables:
    ARGOCD_HOST: testing-argocd.fitfile.net
  cache: {}
  resource_group: staging
  retry: 2
  script:
    - /home/argocd/argocd_sync_testing_images.sh
  rules:
    - if: $CI
  timeout: 5 minutes

run_integration_tests:
  stage: test
  image: fitfile/argocli:alpine
  variables:
    ARGO_BASE_HREF: testing-argo-workflows.fitfile.net
    KUBECONFIG: $CI_PROJECT_DIR/.kube/config
  needs:
    - sync_argo_app
    - prepare_kube_config
  cache: {}
  resource_group: staging
  script:
    - mkdir -p $CI_PROJECT_DIR/.kube
    - cp $CI_PROJECT_DIR/kubeconfig $CI_PROJECT_DIR/.kube/config
    # TODO: https://learn.microsoft.com/en-us/azure/aks/azure-ad-rbac
    # Only needed if --admin flag isn't appended to the az aks get-credentials command
    # - kubelogin convert-kubeconfig -l spn
    # Debug: DNS resolution and kubeconfig check
    - echo "=== DNS Resolution ==="
    - nslookup fitfile-cloud-testing-k8s-xja5tx3v.hcp.uksouth.azmk8s.io 2>&1 || true
    - nslookup fitfile-cloud-testing-k8s-xja5tx3v.hcp.uksouth.azmk8s.io 8.8.8.8 2>&1 || true
    - cat /etc/resolv.conf 2>&1 || true
    - echo "=== Kubeconfig server ==="
    - grep server "$CI_PROJECT_DIR/.kube/config" || true
    - echo "=== End debug ==="
    - argo list -n testing
    - WF_NAME="$(argo submit -n testing --generate-name int-test- --from workflowtemplate/all-integration-tests -o name)"
    - argo wait -n testing "$WF_NAME"
    - sleep 3
    - PHASE="$(argo get -n testing "$WF_NAME" -o json | jq -r '.status.phase')"
    - test "$PHASE" = "Succeeded"
  rules:
    - if: $CI
```

## Relevant GitLab runner info

- Runner type: **GitLab SaaS** (`green-7.saas-linux-small-amd64`), NOT self-hosted
- The `fitfile/argocli:alpine` container inherits the Docker host's DNS resolver
- The host DNS is `169.254.169.254:53` — this is the Azure metadata DNS IP, reachable from Azure VMs
- The GitLab SaaS runner infrastructure IS on Azure, but the runner's DNS may not have access to forward to Azure Private DNS zones
- The AKS cluster's VNet may have a different DNS configuration than the runner's VNet

## Questions to investigate

1. Why does the container's `/etc/resolv.conf` contain `169.254.169.254` as the DNS server? Is this set by the Docker daemon, the runner, or the image?
2. Can the GitLab runner container reach the `169.254.169.254:53` DNS server? A firewall or network policy might be blocking it.
3. Does the `az aks get-credentials --admin` command produce a kubeconfig with the public FQDN or a private one? (The public FQDN is confirmed, but we should verify the kubeconfig)
4. Could the `prepare_kube_config` job (running in `mcr.microsoft.com/azure-cli:latest`) be running on a different runner/network than the `run_integration_tests` job?
5. Is there a way to add `--dns 8.8.8.8` to the container, or override `/etc/resolv.conf` in the `run_integration_tests` job?
6. Could the runner be configured with a custom DNS that forwards to the Azure DNS?
7. Is there a GitLab runner-level variable or configuration that controls DNS for containers?

## Files to review

From **InsightFILE** repo:
- `deployment/pipeline/staging-pipelines.yml` — triggers the deployment repo
- `deployment/pipeline/build-pipelines.yml` — Docker build jobs
- `deployment/pipeline/verification-pipelines.yml` — verification jobs
- `.gitlab-ci.yml` — main pipeline definition
- `deployment/pipeline/common/build.sh` — Docker build script

From **Deployment** repo:
- `staging.gitlab-ci.yml` — the integration test pipeline (problem location)
- Any Dockerfile for `fitfile/argocli:alpine` image
- Any runner configuration files

## What we've tried

1. Added debug lines to `staging.gitlab-ci.yml` (on branch `bugfix/FTFL-456`) that run `nslookup`, `cat /etc/resolv.conf`, and `grep server` on the kubeconfig before the `argo list` command
2. Confirmed the hostname resolves publicly via 8.8.8.8
3. Confirmed the cluster is not private (no `privateFqdn`) and is running

## Task

Review all the pipeline code above and the DNS infrastructure issue. Propose a fix that allows the `run_integration_tests` job to resolve the AKS cluster hostname from the GitLab SaaS runner. Consider options like:
- Overriding the container DNS in the GitLab CI job
- Making the `prepare_kube_config` job produce a different kubeconfig
- Adding a network hop/proxy between the runner and the AKS API
- Changing the GitLab runner configuration
- Any other approach that would work