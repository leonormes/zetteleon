---
created: 2026-06-11T09:56:03+00:00
date: 2026-06-12
modified: 2026-06-11T10:25:38+00:00
project: FITFILE Application
source: claude-sonnet-4-6 (delegated reasoning)
status: inbox
tags: [2579405920, 2591559194, 5443, 5732, 5819, 5849, audit, ci-cd, fitfile, gitlab, health-report, pipeline]
title: 2026-06-12-pipeline-health-report
---

## 🏥 Pipeline Health Report—Fitfile CI/CD Ecosystem

Audit Date: 12 June 2026
Audited Repos: `InsightFILE`, `data-and-analytics`, `workflows-api`, `deployment`, `ude-cli`
Audit Method: Static YAML analysis + `glab` CLI interrogation of live pipelines

---

### 1. Executive Summary

| Metric | Status |
|---|---|
| Overall State | ⚠️ Unhealthy—100% failure rate on last 10 pipelines (MR!2307) |
| Avg Pipeline Duration (InsightFILE) | ~14 min (success) / ~18 min (failure) |
| Architecture Type | Hybrid—mixed DAG (`needs:`) and sequential stage-gated |
| Success Streak | Last green pipeline: 5 days ago (pipeline 2579405920, `development` branch) |
| Stuck Pipelines | 4 pipelines stuck "running" since 2 years ago (#5849, 5819, 5732, 5443) |
| Duplicate Pipeline Risk | Low—`workflow:rules` correctly excludes `[RELEASE]` commits |
| Security Score | ⚠️ Hardcoded IDs in some YAML; `latest` tags in production images; OAuth2 password grant in staging script |

---

### 2. Immediate Fixes

#### 🔴 CRITICAL: ESLint Errors Blocking Merge Pipeline

Pipeline: 2591559194 (MR!2307—`feature/TT-138-configure-faro-sdk`)
Failed Jobs: `frontend_lint`, `frontend_unit_tests`
Root Cause: New Faro SDK test files introduced 7 instances of `react/no-children-prop` violations, and `@typescript-eslint/no-explicit-any` rule definition is missing from the project's ESLint config.

```text
./src/lib/faro/__tests__/FaroProvider.unit.test.tsx
  64:24  Error: Do not pass children as props.  react/no-children-prop
  (repeated 6 more times)

./src/lib/faro/__tests__/faroTracing.unit.test.ts
  19:5  Error: Definition for rule '@typescript-eslint/no-explicit-any' was not found.
  28:9  Error: Definition for rule '@typescript-eslint/no-explicit-any' was not found.
```

Fix options:

1. Fix ESLint violations in the Faro test files (preferred)
2. Add `.eslintignore` override for `src/lib/faro/__tests__/`
3. Install the missing `@typescript-eslint` plugin dependency

#### 🔴 CRITICAL: Test Failures in `verify_ffcloud` (424s—Longest Job)

Duration: 424 seconds (7+ minutes)
Root Cause: Two test suites failing:

- `Userflow.test.ts:91`—Dirty patch expectation mismatch: snapshot expects `undefined` but code now produces `null` for `lastRunAt` and `lastRunStatus`
- `UserflowController.test.ts:217`—API returns 500 (Internal Server Error) instead of 200 when searching userflows with all search params

```
✓ -   "lastRunAt": undefined,
✗ +   "lastRunAt": null,        // snapshot mismatch
-> Test Suites: 3 failed, 1 skipped, 165 passed, 168 of 169 total
-> Tests:       4 failed, 18 skipped, 1348 passed, 1370 total
```

These are genuine code-regression test failures introduced by the MR diff.

#### 🔴 CRITICAL: 4 Zombie Pipelines Stuck Running Since ~2024

| Pipeline ID | Branch | Created |
|---|---|---|
| 5849 | `feature/FFAPP-2209-schema-setup-ui` | ~2 years ago |
| 5819 | `feature/FFAPP-2164-data-set-ui` | ~2 years ago |
| 5732 | `feature/FFAPP-2147-create-upload-file-graphql-endpoint` | ~2 years ago |
| 5443 | `feature/FFAPP-1966-create-permissions-graphql-api` | ~2 years ago |

These consume shared runner capacity and pollute pipeline views. Action:

```bash
glab ci cancel 5849 5819 5732 5443 -R fitfile/apps/InsightFILE
```

---

### 3. Efficiency Upgrades

#### 3.1 Cache NOT Populated for Merge Train Pipelines

Problem: `install_dependencies` (the only job with `policy: pull-push`) is excluded from merge train pipelines:

```yaml
# common-jobs.yml, lines 28-35
install_dependencies:
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"
      when: never           # ← CACHE IS NEVER PUSHED FOR MERGE TRAINS!
```

All downstream build/verification jobs in merge trains rely on a stale fallback cache key (`fitfile-application-cache-key`) or re-download everything from scratch, wasting 60–90s per job on `yarn install`.

Fix: Remove the merge_train exclusion for `install_dependencies`, or at least run it when `yarn.lock` changes:

```yaml
install_dependencies:
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"
      changes:
        paths:
          - yarn.lock
        compare_to: 'refs/heads/development'
    - if: $CI_COMMIT_BRANCH == null || $CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH
      changes:
        paths:
          - yarn.lock
        compare_to: 'refs/heads/development'
```

#### 3.2 No Real DAG Parallelism—`needs:` Adds Nothing Over Stage Ordering

All verification jobs in `InsightFILE` declare `needs: [install_dependencies]` but they're already gated by stage ordering (`install` → `verification`). The `needs:` keyword here is redundant—it doesn't unlock any parallelism.

Upgrade: Remove `needs: [install_dependencies]` from verification jobs and rely on cache. Or if yarn install is genuinely needed per-job, inline it and set `cache:key` deterministically via `yarn.lock`.

#### 3.3 `pull_policy: always` Forces Unnecessary Image Pulls

The custom `fitfile/sonar-nodejs:1.0.0` image is pulled fresh every pipeline run. For a static, versioned tag this is wasteful—adds ~10-20s per job.

Before:

```yaml
image:
  name: fitfile/sonar-nodejs:1.0.0
  pull_policy: always
```

After:

```yaml
image:
  name: fitfile/sonar-nodejs:1.0.0
  pull_policy: if-not-present
```

#### 3.4 Overly Large Base Images by Job

| Job | Current Image | Issue | Suggested |
|---|---|---|---|
| `verify_ffcloud` | `fitfile/sonar-nodejs:1.0.0` | Already custom-built | ✓ Optimise Dockerfile.sonar |
| `prepare_kube_config` | `mcr.microsoft.com/azure-cli:latest` | ~1.5GB, `latest` tag | Pin to `mcr.microsoft.com/azure-cli:2.72.0` |
| All Docker build jobs | `docker:latest` | Mutable `latest`, large image | Pin to `docker:27.4.0-dind` |
| `build_s3_fitfile_cli` | `node:22` | Full Debian (~900MB) | Use `node:22-alpine` (~150MB) |

#### 3.5 Longest-Running Jobs—Optimisation Targets

| Job | Duration | Optimisation Strategy |
|---|---|---|
| `verify_ffcloud` | 424s (7 min) | Split into `parallel:matrix`—separate `lint` / `test:unit` / `test:integration` |
| `frontend_interaction_tests` | 316s | Prebuild storybook; add `--shard=1/2` across 2 parallel jobs |
| `frontend_unit_tests` | 256s | Split into `test:ci --shard=1/3` with `parallel: 3` |
| `install_dependencies` | 113s | Evaluate Yarn PnP / zero-install to eliminate install step |

#### 3.6 Artifacts Missing `expire_in`

`frontend_interaction_tests` and `build_sonar_nodejs` produce artifacts with no `expire_in`, meaning they accumulate indefinitely in GitLab storage.

Fix: Add `expire_in: 1 week` to all artifact-producing jobs.

---

### 4. Security & Best Practices

#### 4.1 Hardcoded Environment IDs in Deployment Repo

```yaml
# deployment/.gitlab-ci.yml, lines 76-77
TENANT_ID: 45e73aa3-1ee9-47c0-ba25-54eda9da021a
SUBSCRIPTION_ID: 249df46b-f75d-4492-8e78-b33a00473548
```

Risk: Low (IDs are UUIDs, not secrets), but violates DRY and makes environment rotation harder.

Fix: Move to CI/CD variables:

```yaml
variables:
  TENANT_ID: $AZURE_TENANT_ID
  SUBSCRIPTION_ID: $AZURE_SUBSCRIPTION_ID
```

#### 4.2 OAuth2 Password Grant Leaks Token to CI Logs

File: `get_staging_images.sh`, lines 10-14

```bash
GetToken() {
  TOKEN_RESPONSE=$(curl -s -X POST \
    -d "grant_type=password&client_id=${ACR_SERVICE_PRINCIPLE}&username=...&password=${ACR_SERVICE_PRINCIPLE_PASS}&scope=...")
  TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | grep -o '[^"]*$')
  echo $token    # ← TOKEN ECHOED TO CI LOGS!
}
```

Risk: Medium—the ACR token is written to CI job logs where it could be accessed by anyone with developer read access.

Fix: Switch to `client_credentials` grant and remove the `echo`:

```bash
GetToken() {
  curl -s -X POST \
    -d "grant_type=client_credentials" \
    -d "service=fitfileregistry.azurecr.io" \
    -d "scope=repository:*:*" \
    -u "${ACR_SERVICE_PRINCIPLE}:${ACR_SERVICE_PRINCIPLE_PASS}" \
    "https://fitfileregistry.azurecr.io/oauth2/token" | jq -r '.access_token'
}
```

#### 4.3 Legacy SAST Template

```yaml
# data-and-analytics/.gitlab-ci.yml
include:
  - template: Security/SAST.gitlab-ci.yml    # ← Legacy/deprecated
```

Fix: Upgrade to `Jobs/SAST.latest.gitlab-ci.yml` to get the latest analyzer versions.

#### 4.4 `latest` Tags Used for Runtime Images

| Image | Tag | Risk |
|---|---|---|
| `fitfile/gapv` | `latest` | Release pipeline image—a broken push blocks all releases |
| `fitfile/argocli` | `latest` | ArgoCD operations image |
| `fitfile/argocdsync` | `latest` | Staging deployment image |

Fix: Always version custom images with semantic tags and use `latest` only as a convenience alias.

#### 4.5 `before_script` Leaks Pipeline ID

```yaml
# data-and-analytics/.gitlab-ci.yml, workflows-api/.gitlab-ci.yml
default:
  before_script:
    - echo ${CI_PIPELINE_ID}
```

Minor—CI_PIPELINE_ID is not a secret, but unnecessary noise in logs. Remove.

---

### 5. Major Code Refactor Suggestion: Collapse 15+ Build Jobs into Parallel Matrix

The `build-pipelines.yml` file contains ~15 near-identical Docker build job definitions (each with its own `PACKAGE_NAME`, `IMAGE_NAME`, `DOCKER_FILE`, `CHANGE_PATH`). This is ~400 lines of repetitive YAML.

Proposed refactor: Use `parallel:matrix` to collapse into a single job:

```yaml
.docker_build_matrix:
  stage: build
  image: docker:27.4.0
  cache: {}
  services:
    - docker:27.4.0-dind
  needs:
    - job: get_next_package_versions
      optional: true
      artifacts: true
  script:
    - ./deployment/pipeline/common/build.sh
  parallel:
    matrix:
      - PACKAGE_NAME: "emis-processing"
        IMAGE_NAME: "emis-processing"
        DOCKER_BUILD_CTX: "./apps/tasks/emis-processing"
        DOCKER_FILE: "./apps/tasks/emis-processing/Dockerfile"
        VERSION_VARIABLE_NAME: "EMIS_PROCESSING_VERSION"
        CHANGE_PATHS: "apps/tasks/emis-processing//*"
      - PACKAGE_NAME: "sftp-loader"
        IMAGE_NAME: "sftp-loader"
        DOCKER_BUILD_CTX: "./apps/tasks/sftp-loader"
        DOCKER_FILE: "./apps/tasks/sftp-loader/Dockerfile"
        VERSION_VARIABLE_NAME: "SFTP_LOADER_VERSION"
        CHANGE_PATHS: "apps/tasks/sftp-loader//*"
      - PACKAGE_NAME: "medcat-annotation"
        IMAGE_NAME: "medcat-annotation"
        DOCKER_BUILD_CTX: "./apps/tasks/medcat-annotation"
        DOCKER_FILE: "./apps/tasks/medcat-annotation/Dockerfile"
        VERSION_VARIABLE_NAME: "MEDCAT_ANNOTATION_VERSION"
        CHANGE_PATHS: "apps/tasks/medcat-annotation//*"
      - PACKAGE_NAME: "default-exit-handler"
        IMAGE_NAME: "default-exit-handler"
        DOCKER_BUILD_CTX: "./apps/tasks/default-exit-handler"
        DOCKER_FILE: "./apps/tasks/default-exit-handler/Dockerfile"
        VERSION_VARIABLE_NAME: "DEFAULT_EXIT_HANDLER_VERSION"
        CHANGE_PATHS: "apps/tasks/default-exit-handler//*"
      - PACKAGE_NAME: "ffcloud"
        IMAGE_NAME: "ffcloud-service"
        DOCKER_BUILD_CTX: ""
        DOCKER_FILE: "./Dockerfile.ffcloud"
        VERSION_VARIABLE_NAME: "FFCLOUD_VERSION"
        CHANGE_PATHS: |
          apps/ffcloud//*
          packages/service-common//*
          packages/types//*
      - PACKAGE_NAME: "frontend"
        IMAGE_NAME: "frontend"
        DOCKER_BUILD_CTX: ""
        DOCKER_FILE: "./Dockerfile.frontend.v2"
        VERSION_VARIABLE_NAME: "FRONTEND_VERSION"
        CHANGE_PATHS: |
          apps/frontend//*
          packages/types//*
      # ... add remaining services
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"
      changes:
        - ${CHANGE_PATHS}
    - if: $RELEASE_PIPELINE == "true"
      changes:
        paths:
          - ${CHANGE_PATHS}
        compare_to: refs/tags/latest-release
```

Benefits:

- Reduces CI YAML by ~400 lines (from ~490 to ~90)
- GitLab auto-generates parallel child jobs per matrix cell
- All jobs share the same image (pulled once), `cache: {}`, and `services`
- Easier to add new services—just append to the matrix

---

### 6. Prioritised Action Plan

| Priority | Action | Effort | Impact | Repo |
|---|---|---|---|---|
| 🔴 P0 | Fix ESLint violations in Faro test files | Low | Unblocks MR!2307 (100% failure rate) | InsightFILE |
| 🔴 P0 | Cancel 4 zombie pipelines (#5849, 5819, 5732, 5443) | Low | Frees shared runner capacity | InsightFILE |
| 🟠 P1 | Fix `Userflow.test.ts` null vs undefined expectations | Medium | Fixes `verify_ffcloud` regression | InsightFILE |
| 🟠 P1 | Fix `UserflowController.test.ts` 500 error | Medium | Fixes `verify_ffcloud` regression | InsightFILE |
| 🟠 P1 | Add `expire_in` to all artifacts | Low | Prevents storage bloat | InsightFILE |
| 🟠 P1 | Pin `docker:latest` → `docker:27.4.0` in all build jobs | Low | Reproducible builds | All |
| 🟡 P2 | Collapse duplicate build jobs into `parallel:matrix` | Medium | -400 lines CI config, faster parallel builds | InsightFILE |
| 🟡 P2 | Fix merge train cache exclusion | Low | Faster merge trains | InsightFILE |
| 🟡 P2 | Move hardcoded IDs to CI/CD variables | Low | Security hardening | deployment |
| 🟡 P2 | Remove `echo $token` from staging script | Low | Prevents token leakage | InsightFILE |
| 🔵 P3 | Switch SAST template to `Jobs/SAST.latest.gitlab-ci.yml` | Low | Future-proofing | data-and-analytics |
| 🔵 P3 | Version `fitfile/gapv` image beyond `latest` | Medium | Release reliability | InsightFILE |
| 🔵 P3 | Evaluate Yarn PnP / zero-install | High | Could cut 1-2 min per pipeline | InsightFILE |
| 🔵 P3 | `pull_policy: if-not-present` for static tags | Low | Faster runner init | InsightFILE |
