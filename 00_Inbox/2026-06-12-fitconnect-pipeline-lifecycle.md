---
tags:
  - pipeline
  - ci-cd
  - fitconnect
  - end-to-end
  - deployment
  - argocd
  - gitops
  - gapv
source: claude-sonnet-4-6 (delegated reasoning)
date: 2026-06-12
project:
status: inbox
---

# Fitconnect — End-to-End CI/CD Pipeline Lifecycle

**Trace of a single change from developer commit to staging cluster deployment.**

---

## Overview: The Chain (7 Phases)

```
┌─────────────────────────────────────────────────────────┐
│  Developer → Feature Branch → MR Pipeline               │
│  ↓                                                        │
│  Merge Train → Build + Integration Test                   │
│  ↓                                                        │
│  Merge to development                                     │
│  ↓                                                        │
│  Merge to main → Release Pipeline (GAPV)                  │
│  ↓                                                        │
│  GAPV commits new version to deployment repo              │
│  ↓                                                        │
│  ArgoCD detects drift → Syncs to AKS                     │
│  ↓                                                        │
│  Staging Verification (merge trains)                      │
└─────────────────────────────────────────────────────────┘
```

**Repos involved (5):**
1. `fitfile/apps/InsightFILE` — source code + CI
2. `fitfile/deployment` — Helm charts + ArgoCD manifests
3. (implied) Azure Container Registry — image storage
4. (implied) AKS cluster — runtime environment
5. `fitfile/workflows-api` — cross-project integration (triggered via child pipeline)

---

## Phase 1: Developer Work — Feature Branch

Developer creates branch from `development`:

```
git checkout -b feature/FFAPP-XXXX-fitconnect-improvement
git commit -m "feat: improve fitconnect data extraction"
git push origin feature/...
```

**What they touch:** `apps/fitconnect/**/*` (and potentially `packages/service-common/**/*`, `packages/types/**/*`)

**No CI runs yet.** The `workflow:rules` in `.gitlab-ci.yml` only trigger on:
- `$CI_PIPELINE_SOURCE == "merge_request_event"`
- `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`

---

## Phase 2: MR Pipeline — Verification

Developer opens MR targeting `development`. Pipeline fires on `refs/merge-requests/XXXX/head`.

### Stages & Jobs

| Stage | Job | Condition | Duration (approx) | Artifact |
|---|---|---|---|---|
| `.pre` | `build_sonar_nodejs` | Only if `Dockerfile.sonar` changed | — | docker image pushed |
| `install` | `install_dependencies` | If `yarn.lock` changed vs `development` | ~113s | `.yarn/`, `node_modules/` (cache, pull-push) |
| `install` | `audit_dependencies` | Same as above | ~70s | — |
| `verification` | **`verify_fitconnect`** | If `apps/fitconnect/**/*`, `packages/service-common/**/*`, or `packages/types/**/*` changed | **~424s** | coverage data |
| `verification` | `verify_ffcloud`, `verify_rest_scheduler`, `verify_scheduler_svc`, `verify_service_common`, `verify_s3_fitfile_cli`, `verify_workflows_api`, `frontend_unit_tests`, `frontend_lint`, `frontend_build_storybook`, `frontend_interaction_tests` | Various change patterns | 70–316s each | — |
| `verification` | `sonarqube-check` | Commented out | — | — |

### `verify_fitconnect` Detail

The job extends `.verify_script` (from `verification-pipelines.yml`):

```yaml
.verify_script:
  coverage: '/Branches\s*:\s*([^%]+)/'
  needs:
    - job: install_dependencies
      optional: true
  script:
    - yarn workspaces focus @fitfile/${SERVICE_NAME}
    - yarn workspace @fitfile/${SERVICE_NAME} build
    - yarn workspace @fitfile/${SERVICE_NAME} lint
    - yarn workspace @fitfile/${SERVICE_NAME} test:ci
    - yarn workspace @fitfile/${SERVICE_NAME} test:sonar || true

verify_fitconnect:
  extends: .verify_script
  variables:
    SERVICE_NAME: 'fitconnect'
```

**Important:** If `install_dependencies` was skipped (no `yarn.lock` change), the `needs:` is `optional: true`, so `verify_fitconnect` runs anyway but must pull dependencies from cache. If cache miss, it runs `yarn install` implicitly.

### Image Used

`default:` block sets:
```yaml
image:
  name: fitfile/sonar-nodejs:1.0.0
  pull_policy: always    # forced pull every time
```

This is a custom image containing Node.js + Sonar scanner tooling. Built locally in `.pre` stage.

### Runner Details

- Type: `saas-linux-small-amd64` (2 vCPU, ~7 GB RAM)
- Cache policy: `pull` (read-only from cache, only `install_dependencies` can push)

---

## Phase 3: Merge Train Pipeline — Build + Integration Test

When the MR is accepted into the merge train, GitLab creates a "merged results" pipeline on `refs/merge-requests/XXXX/merge`. This tests the **combined** result of the target branch + MR.

### Key Differences from MR Pipeline

| Aspect | MR Pipeline (head) | Merge Train (merge) |
|---|---|---|
| What runs | Only verification | Verification + Build + Integration Tests |
| `install_dependencies` | ✅ Runs | ❌ Excluded (`when: never`) |
| Verification jobs | ✅ All run | ✅ All run (same rules) |
| Build jobs (`build_fitconnect`) | ❌ Not triggered | ✅ Only if source paths changed |
| Integration tests | ❌ Not triggered | ✅ `get_staging_images` + `trigger_integration_tests` |

### Build Stage Detail (`build_fitconnect`)

```yaml
build_fitconnect:
  extends: .docker_build
  variables:
    PACKAGE_NAME: fitconnect
    IMAGE_NAME: fitconnect-service
    VERSION_VARIABLE_NAME: FITCONNECT_VERSION
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"
      changes:
        - apps/fitconnect/**/*
        - packages/service-common/**/*
        - packages/types/**/*
    - if: $RELEASE_PIPELINE == "true"
      changes:
        paths: [apps/fitconnect/**/*, packages/service-common/**/*, packages/types/**/*]
        compare_to: refs/tags/latest-release
```

`.docker_build` (defined in `build-pipelines.yml`):

```yaml
.docker_build:
  stage: build
  image: docker:latest
  cache: {}
  services:
    - docker:dind
  needs:
    - job: get_next_package_versions
      optional: true
      artifacts: true
  rules:
    - if: $RELEASE_PIPELINE == "true"
      when: always
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"
      when: always
    - when: never
  script:
    - apk update && apk add bash
    - ./deployment/pipeline/common/build.sh
```

### The Build Script (`build.sh`)

This is the core of the Docker build process:

```bash
source ./output/${CI_PIPELINE_ID}/env.sh  # load version vars from gapv artifacts

if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
  PACKAGE_VERSION=${!VERSION_VARIABLE_NAME}  # semver from gapv
else
  PACKAGE_VERSION="${CI_COMMIT_SHORT_SHA}-rc"  # short SHA + -rc for non-main
fi

CACHE_IMAGE="fitfileregistry.azurecr.io/${IMAGE_NAME}:buildcache"

docker buildx create --use --name ci-builder --driver docker-container 2>/dev/null || docker buildx use ci-builder

docker buildx build \
  -f $DOCKER_FILE_ACTUAL \
  --push \
  -t fitfileregistry.azurecr.io/"${IMAGE_NAME}":"${PACKAGE_VERSION}" \
  --label commit_sha="${CI_COMMIT_SHA}" \
  --build-arg GIT_AUTH_TOKEN="${CI_JOB_TOKEN}" \
  --build-arg PACKAGE_NAME="${PACKAGE_NAME}" \
  --cache-from type=registry,ref="${CACHE_IMAGE}" \
  --cache-to type=registry,ref="${CACHE_IMAGE}",mode=max \
  ${DOCKER_BUILD_ADDITIONAL_ARGS} \
  ${DOCKER_BUILD_CTX_ACTUAL}
```

**Key details:**
- Uses `docker buildx` with containerd snapshotter for efficient layer caching
- Build cache stored in ACR as `<image>:buildcache` tag
- On merge train: image tagged as `fitconnect-service:abc1234-rc`
- Image is pushed **directly to ACR** (no intermediate `--load`)
- `--cache-to mode=max` caches all layers (not just exported)

### Integration Test Trigger

Alongside builds, the merge train also triggers integration tests:

```yaml
get_staging_images:
  stage: test
  script:
    - ./deployment/pipeline/common/get_staging_images.sh  # queries ACR for -rc tags
    - echo "STAGING_VALUE_OVERRIDES=$(cat ./staging-values.yaml | base64 -w 0)" > staging.env
  artifacts:
    reports:
      dotenv: staging.env
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"

# This triggers the deployment repo's staging pipeline
trigger_integration_tests:
  stage: test
  needs: [get_staging_images]
  trigger:
    include:
      - project: fitfile/deployment
        ref: 'master'
        file: staging.gitlab-ci.yml
    strategy: depend
  resource_group: deployment-repo
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"
```

---

## Phase 4: Development Branch Pipeline

MR merges to `development`. A pipeline runs on the development branch:

```yaml
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

("default branch" is `development`, not `main` — see project settings)

This pipeline:
- Runs verification (same jobs as MR pipeline)
- Runs **all** Docker build jobs (no change-path filtering for default branch)
- Images tagged with `{CI_COMMIT_SHORT_SHA}-rc`
- **Does not** run integration tests
- Does **not** trigger the release child pipeline

---

## Phase 5: Release Pipeline — Main Branch

When `development` is merged to `main`, the release pipeline fires.

### Parent Pipeline (`InsightFILE/.gitlab-ci.yml`)

```yaml
release:
  stage: deploy
  variables:
    RELEASE_PIPELINE: "true"
  trigger:
    include: /deployment/pipeline/release.gitlab-ci.yml
    strategy: depend
  rules:
    - if: "$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH"
```

Triggers a **child pipeline** using `release.gitlab-ci.yml`.

### Release Child Pipeline (`InsightFILE/release.gitlab-ci.yml`)

```yaml
workflow:
  rules:
    - if: $RELEASE_PIPELINE == "true"
      when: always
    - when: never

stages:
  - install
  - build
  - release
```

| Stage | Job | What It Does |
|---|---|---|
| `install` | `build_latest_cache` | Warm yarn cache with fallback key |
| `install` | `get_next_package_versions` | Run `gapv.sh read` — detect changed packages, compute next semver |
| `build` | `build_fitconnect` (via `.docker_build`) | Build & push image to ACR with **semantic version** (e.g. `fitconnect-service:1.0.741`) |
| `release` | `commit_next_chart_versions` | Run `gapv.sh update --repoType=chart` — bump tag in deployment repo's Helm values |
| `release` | `commit_next_package_versions` | Run `gapv.sh update --repoType=code` — bump versions in `package.json` files |

### How GAPV Version Detection Works

1. `gapv.sh read` compares current commit vs `latest-release` tag
2. Detects changed packages from `gapv-packages.yaml`
3. Checks dependency graph (fitconnect depends on `service-common` + `types`)
4. Outputs environment file `output/{CI_PIPELINE_ID}/env.sh`:
   ```bash
   FITCONNECT_VERSION=1.0.741
   FFCLOUD_VERSION=2.5.12
   ```
5. `build.sh` sources this file → uses `$FITCONNECT_VERSION` as image tag

### Helm Values Updated by GAPV

From `gapv-deployment.yaml`:
```yaml
- name: fitconnect
  deployment:
    helm:
      - imageName: fitconnect-service
        chartPath: charts/components/fitconnect
        valuesFile:
          property: "fitconnect.image.tag"
```

GAPV updates `charts/components/fitconnect/values.yaml`:
```yaml
fitconnect:
  image:
    repository: fitfileregistry.azurecr.io/fitconnect-service
    tag: 1.0.741      # ← updated by GAPV
```

This commit is pushed to `fitfile/deployment` `master` branch.

---

## Phase 6: ArgoCD Auto-Sync

### ArgoCD Application Definition

`fitfile/deployment` contains ArgoCD Application manifests in `charts/argo/`. The fitconnect component is registered as an ArgoCD Application (App of Apps pattern).

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fitconnect
spec:
  source:
    repoURL: https://gitlab.com/fitfile/deployment.git
    path: charts/components/fitconnect
    targetRevision: master
  destination:
    namespace: fitfile
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### The Sync Cycle

1. GAPV pushes commit to `fitfile/deployment` `master`
2. ArgoCD detects drift (new Helm chart version)
3. ArgoCD syncs: produces Kubernetes Deployment with `image: fitfileregistry.azurecr.io/fitconnect-service:1.0.741`
4. K8s rolling update: new pod starts, old pod terminates
5. Init container runs `yarn db:migrate:remote:up` before main container starts
6. Readiness probe passes → pod enters service

### Deployment Manifest (simplified)

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      initContainers:
        - name: fitconnect-init
          image: fitfileregistry.azurecr.io/fitconnect-service:1.0.741
          command: ['yarn', 'db:migrate:remote:up']
      containers:
        - image: fitfileregistry.azurecr.io/fitconnect-service:1.0.741
          command: ["node", "--require", "./instrumentation.js", "server.js"]
          readinessProbe:
            httpGet:
              path: /fitconnect/readyz?...
```

---

## Phase 7: Staging Verification (Merge Train Only)

For merge trains, integration tests run before the MR is finalised:

### Deployment Repo `staging.gitlab-ci.yml`

| Job | What It Does |
|---|---|
| `prepare_kube_config` | `az login` with SP, `az aks get-credentials` for testing cluster |
| `sync_argo_app` | Runs `argocd_sync_testing_images.sh` — syncs staging ArgoCD apps |
| `run_integration_tests` | Runs `argo submit` with integration test workflow template, waits for completion |

After `run_integration_tests` passes, the merge train proceeds to merge.

---

## End-to-End Timeline (Estimated)

| Step | Duration |
|---|---|
| MR pipeline (verification) | ~14 min |
| Merge train pipeline | ~18 min (verification + build + integration tests) |
| Release pipeline | ~8 min (version detection + builds + chart commits) |
| ArgoCD sync | ~1–2 min (drift detection + rolling update) |
| **Total: commit → staging cluster** | **~16 min** (MR pipeline + merge train) |
| **Total: commit → production cluster** | **~24 min** (MR + merge + release + ArgoCD sync) |

*(Assumes fitconnect is the only changed component. Real time is higher due to other parallel jobs.)*

---

## Cross-Repo Dependency Graph

```
InsightFILE (source)
  │
  ├── build.sh → pushes image to ACR
  │   └── ACR: fitfileregistry.azurecr.io/fitconnect-service:{tag}
  │
  ├── gapv.sh update --repoType=chart
  │   └── deployment (git push chart values)
  │       └── ArgoCD syncs to AKS
  │           ├── testing cluster (if staging pipeline)          
  │           └── production cluster (on main branch release)
  │
  └── trigger_integration_tests (merge train only)
      └── deployment/staging.gitlab-ci.yml
          ├── prepare_kube_config (testing AKS)
          ├── sync_argo_app (deploy to testing)
          └── run_integration_tests (Argo workflow)
```

---

## Pipeline Configuration Files Involved

| File | Purpose |
|---|---|
| `InsightFILE/.gitlab-ci.yml` | Top-level workflow, stages, default image, cache, release trigger |
| `InsightFILE/deployment/pipeline/common-jobs.yml` | `install_dependencies`, `audit_dependencies` |
| `InsightFILE/deployment/pipeline/verification-pipelines.yml` | `.verify_script` template + all verify_* jobs |
| `InsightFILE/deployment/pipeline/build-pipelines.yml` | `.docker_build` template + all build_* jobs |
| `InsightFILE/deployment/pipeline/staging-pipelines.yml` | Integration test triggers (`get_staging_images`, `trigger_integration_tests`) |
| `InsightFILE/deployment/pipeline/release.gitlab-ci.yml` | Release child pipeline (gapv + versioning) |
| `InsightFILE/deployment/pipeline/common/build.sh` | Docker buildx script (shared by all build jobs) |
| `InsightFILE/deployment/pipeline/common/get_staging_images.sh` | ACR tag query for staging |
| `InsightFILE/deployment/pipeline/common/gapv-packages.yaml` | Package definitions + dependency graph |
| `InsightFILE/deployment/pipeline/common/gapv-deployment.yaml` | Helm chart mapping + image tag updates |
| `deployment/.gitlab-ci.yml` | Infra pipeline: builds ArgoCD images, kubeconfig, lint |
| `deployment/staging.gitlab-ci.yml` | Staging deploy + integration test pipeline |

---

## Bottlenecks & Failure Points (Fitconnect-Specific)

| Step | Bottleneck | Mitigation |
|---|---|---|
| `verify_fitconnect` (424s) | Single sequential script: build → lint → test → sonar | Split into `parallel:matrix`, separate lint from test |
| `build_fitconnect` | `apk update && apk add bash` each run + Docker buildx daemon creation | Pre-install bash in `fitfile/sonar-nodejs` image; reuse buildx instance |
| `install_dependencies` skips on merge train | Merge train relies on stale fallback cache | Always run `yarn install` if cache miss — remove `when: never` |
| `get_staging_images` | Echoes token to CI logs + uses password grant | Switch to client_credentials grant, remove `echo $token` |
| ArgoCD sync | Manual sync policy (auto-sync may be disabled per environment) | Verify `automated.syncPolicy` on each ArgoCD Application |
| Chart commit race condition | `resource_group: deployment-repo` is **temporarily removed** | Re-enable `resource_group` to serialise release commits |