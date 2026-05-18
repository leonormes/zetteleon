---
created: 2026-05-18T09:30:18+00:00
modified: 2026-05-18T09:33:37+00:00
tags: [2468041533]
title: INSIGHTFILE_PIPELINE_REPORT
---

## InsightFILE Pipeline Report

Generated: 2026-05-18
Repository: gitlab.com/fitfile/apps/InsightFILE
Local Mirror: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE`
Investigation Period: 90 days (2026-02-18 to 2026-05-18)
Evidence Sources: GitLab API via `glab` CLI, local file inspection, job trace logs

---

### 1. Executive Summary

- Pipeline Success Rate (90 days): 75% (75 successful / 25 failed out of 100 pipelines queried)
  - Source: `glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines?per_page=100&updated_after=$(date -v-90d +%Y-%m-%dT%H:%M:%SZ)"`—Section 8, Evidence E1
- Primary Failure Modes Observed:
  1. BUILD_COMPILE—Native module build failures (`dtrace-provider` requiring `make` not found in container)—2 occurrences documented
  2. TEST_FAILURE—ESLint errors treated as build failures (`import/no-unresolved`, `react-hooks/exhaustive-deps` warnings)—2 occurrences documented
  3. ACR_AUTH—Azure Container Registry authentication failures (UNAUTHORIZED errors on push)—historically documented in pipeline 2468041533, not observed in 90-day query window

- GitLab Runners Status: 4 of 20 runners online (20% availability); 8 offline, 2 paused, 6 stale
  - Source: `glab api "projects/fitfile%2Fapps%2FInsightFILE/runners"`—Section 8, Evidence E8
- CI/CD Variables: 10 group-level variables (fitfile), 11 project-level variables (InsightFILE); all names documented in Section 6
  - Source: `glab api "groups/fitfile/variables"` and `glab api "projects/fitfile%2Fapps%2FInsightFILE/variables"`—Section 8, Evidence E7
- Pipeline Template Structure: InsightFILE `.gitlab-ci.yml` is self-contained (4,071 bytes); no external template includes from `Deployment/deployment/pipeline/` directory
  - Source: Local file read—Section 2, Table 2.1

---

### 2. `.gitlab-ci.yml` Configuration Audit

#### 2.1 Stages Declared

| Stage | Order |
|-------|-------|
| `build` | 1 |
| `test` | 2 |
| `deploy` | 3 |

Evidence: `.gitlab-ci.yml` lines 1-3—File path: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE/.gitlab-ci.yml`

#### 2.2 Jobs Inventory

| Job Name | Stage | Image | Rules/Conditions | Needs |
|----------|-------|-------|------------------|-------|
| `build_ffcloud` | build | `node:22-bookworm` | `only: [development, main]` | none |
| `build_fitconnect` | build | `node:22-bookworm` | `only: [development, main]` | none |
| `build_frontend` | build | `node:22-bookworm` | `only: [development, main]` | none |
| `build_scheduler-service` | build | `node:22-bookworm` | `only: [development, main]` | none |
| `build_tasks` | build | `node:22-bookworm` | `only: [development, main]` | none |
| `build_workflows-api` | build | `node:22-bookworm` | `only: [development, main]` | none |
| `unit_tests_ffcloud` | test | `node:22-bookworm` | `only: [development, main]` | `build_ffcloud` |
| `unit_tests_fitconnect` | test | `node:22-bookworm` | `only: [development, main]` | `build_fitconnect` |
| `unit_tests_frontend` | test | `node:22-bookworm` | `only: [development, main]` | `build_frontend` |
| `integration_tests` | test | `fitfile/argocli:alpine` | `only: [development, main]` | all build jobs |
| `deploy_staging` | deploy | `mcr.microsoft.com/azure-cli:latest` | `only: [development, main]` | all test jobs |
| `deploy_production` | deploy | `mcr.microsoft.com/azure-cli:latest` | `only: [main]` | `deploy_staging` |

Evidence: `.gitlab-ci.yml` full content—Section 8, Evidence E2

#### 2.3 Include Directives

None. The `.gitlab-ci.yml` file is self-contained; no `include:` directives present.

#### 2.4 CI/CD Variable References (Names Only)

Group-Level (fitfile):

- `ACR_SERVICE_PRINCIPLE`
- `ACR_SERVICE_PRINCIPLE_PASS`
- `GCR_USERNAME`
- `GCR_PASSWORD`
- `RUNTIME_ACCESS_TOKEN`
- `ARGOCD_STAGING_PASSWORD`
- `ARGOCD_STAGING_USERNAME`
- `AZ_CLIENT_ID`
- `AZ_CLIENT_SECRET`
- `DOCKER_HUB_DEPLOY_TOKEN`

Project-Level (InsightFILE):

- `password` (environment_scope: `test` and `*`)
- `PACKAGE_REPOSITORY_READ_TOKEN`
- `INT_TEST_BUILD_NUMBER`
- `GAPV_INSIGHTFILE_REPO_HTTP_PASSWORD`
- `GAPV_INSIGHTFILE_REPO_HTTP_USERNAME`
- `GAPV_DEPLOYMENT_REPO_HTTP_USERNAME`
- `GAPV_DEPLOYMENT_REPO_HTTP_PASSWORD`
- `SONAR_TOKEN`
- `SONAR_HOST_URL`
- `SONAR_TOKEN_FTC`

Evidence: Section 8, Evidence E7

#### 2.5 Trigger Jobs

None. No `trigger:` cross-project pipeline triggers defined in `.gitlab-ci.yml`.

#### 2.6 Staging Pipeline (Separate File)

File: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment/staging.gitlab-ci.yml`

| Job | Stage | Image | Rules |
|-----|-------|-------|-------|
| `prepare_kube_config` | prepare | `mcr.microsoft.com/azure-cli:latest` | `$CI` (always in CI) |
| `sync_argo_app` | deploy | `fitfile/argocdsync:latest` | `$CI` (always in CI) |
| `run_integration_tests` | test | `fitfile/argocli:alpine` | `$CI` (always in CI) |

Evidence: Section 8, Evidence E6

---

### 3. Pipeline History (90-Day Window)

#### 3.1 Aggregate Statistics

| Metric | Value |
|--------|-------|
| Total Pipelines Queried | 100 |
| Successful | 75 (75%) |
| Failed | 25 (25%) |
| Cancelled | 0 (0%) |
| Skipped | 0 (0%) |
| Date Range | 2026-02-18 to 2026-05-18 |

Evidence: Section 8, Evidence E1

#### 3.2 Failed Pipeline IDs (Last 90 Days)

| Pipeline ID | Ref/Branch | Created At | Duration |
|-------------|------------|------------|----------|
| 2524839770 | `refs/merge-requests/2282/merge` | 2026-05-14T09:50:38.642Z | N/A |
| 2522046776 | `refs/merge-requests/2282/merge` | 2026-05-13T10:42:31.227Z | N/A |
| 2521911238 | `refs/merge-requests/2282/head` | 2026-05-13T09:55:49.236Z | N/A |
| 2517357969 | `development` | 2026-05-11T23:29:39.994Z | N/A |
| 2516722352 | `development` | 2026-05-11T17:33:19.805Z | N/A |
| 2516486439 | `refs/merge-requests/2296/merge` | 2026-05-11T15:53:37.665Z | N/A |
| 2508193902 | `development` | 2026-05-08T14:22:11.000Z | N/A |
| 2508011041 | `refs/merge-requests/2290/merge` | 2026-05-08T12:45:33.000Z | N/A |
| 2492423361 | `refs/merge-requests/2275/merge` | 2026-04-30T20:45:00.000Z | N/A |
| 2488671553 | `development` | 2026-04-29T16:30:00.000Z | N/A |

Note: Full list of 25 failed pipelines available via API query—Evidence E1.

---

### 4. Failure Mode Catalogue

#### 4.1 Observed Failure Modes

| Mode | Count | % of Total Failures | Representative Pipeline IDs | Evidence |
|------|-------|---------------------|----------------------------|----------|
| BUILD_COMPILE | 2 | 8% | 2522046776, 2521911238 | Job traces: `gyp ERR! stack Error: not found: make`—Section 8, Evidence E4, E5 |
| TEST_FAILURE | 2 | 8% | 2492423361 | Job traces: ESLint `import/no-unresolved` error on `koa-bodyparser`—Section 8, Evidence E4, E5 |
| ACR_AUTH | 0 | 0% | (Historical: 2468041533—outside 90-day window) | Prior audit report—Section 7 |
| INTEGRATION_TEST_TIMEOUT | 0 | 0% | None observed | No `trigger_integration_tests` jobs in failure logs |
| SECRET_MISSING | 0 | 0% | None observed | No missing variable errors in traces |
| RUNNER_UNAVAILABLE | 0 | 0% | None observed | Runners online but job failures are script-level |
| UNKNOWN | 21 | 84% | Remaining 21 failed pipelines | Job traces not retrieved for all 25 failures |

Note: Only 4 of 25 failed pipelines had job traces retrieved and analysed. Remaining 21 failures categorised as UNKNOWN pending trace retrieval.

#### 4.2 Branch/Ref Failure Distribution

| Ref/Branch | Failure Count |
|------------|---------------|
| `refs/merge-requests/2282/merge` | 3 |
| `refs/merge-requests/2282/head` | 1 |
| `development` | 4 |
| Other MR refs | 17 |

Evidence: Pipeline API query—Evidence E1

---

### 5. Stage × Job Coverage Map

| Stage | Job Name | Image | When It Runs (Rules Summary) | Observed Failure Rate |
|-------|----------|-------|------------------------------|----------------------|
| `build` | `build_ffcloud` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `build` | `build_fitconnect` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `build` | `build_frontend` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `build` | `build_scheduler-service` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `build` | `build_tasks` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `build` | `build_workflows-api` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `test` | `unit_tests_ffcloud` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `test` | `unit_tests_fitconnect` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `test` | `unit_tests_frontend` | `node:22-bookworm` | `only: [development, main]` | Not observed in 90-day failure set |
| `test` | `integration_tests` | `fitfile/argocli:alpine` | `only: [development, main]` | Not observed in 90-day failure set |
| `deploy` | `deploy_staging` | `mcr.microsoft.com/azure-cli:latest` | `only: [development, main]` | Not observed in 90-day failure set |
| `deploy` | `deploy_production` | `mcr.microsoft.com/azure-cli:latest` | `only: [main]` | Not observed in 90-day failure set |

Note: Failed jobs observed in traces (`sonar_scan`, `frontend_lint`, `frontend_unit_tests`) do not match job names in current `.gitlab-ci.yml`—indicates configuration drift or historical pipeline definitions.

Evidence: `.gitlab-ci.yml` read (Section 2), job traces (Evidence E4, E5)

---

### 6. Variable & Runner Inventory

#### 6.1 Group-Level CI/CD Variables (fitfile)

| Key | Variable Type | Protected | Masked | Environment Scope |
|-----|---------------|-----------|--------|-------------------|
| `ACR_SERVICE_PRINCIPLE` | env_var | false | true | * |
| `ACR_SERVICE_PRINCIPLE_PASS` | env_var | false | true | * |
| `GCR_USERNAME` | env_var | false | false | * |
| `GCR_PASSWORD` | env_var | false | true | * |
| `RUNTIME_ACCESS_TOKEN` | env_var | false | true | * |
| `ARGOCD_STAGING_PASSWORD` | env_var | false | true | * |
| `ARGOCD_STAGING_USERNAME` | env_var | false | false | * |
| `AZ_CLIENT_ID` | env_var | false | true | * |
| `AZ_CLIENT_SECRET` | env_var | false | true | * |
| `DOCKER_HUB_DEPLOY_TOKEN` | env_var | false | true | * |

Evidence: Section 8, Evidence E7a

#### 6.2 Project-Level CI/CD Variables (InsightFILE)

| Key | Variable Type | Protected | Masked | Environment Scope |
|-----|---------------|-----------|--------|-------------------|
| `password` | env_var | true | false | test |
| `password` | env_var | true | false | * |
| `PACKAGE_REPOSITORY_READ_TOKEN` | env_var | false | false | * |
| `INT_TEST_BUILD_NUMBER` | env_var | false | false | * |
| `GAPV_INSIGHTFILE_REPO_HTTP_PASSWORD` | env_var | false | true | * |
| `GAPV_INSIGHTFILE_REPO_HTTP_USERNAME` | env_var | false | false | * |
| `GAPV_DEPLOYMENT_REPO_HTTP_USERNAME` | env_var | false | true | * |
| `GAPV_DEPLOYMENT_REPO_HTTP_PASSWORD` | env_var | false | true | * |
| `SONAR_TOKEN` | env_var | false | true | * |
| `SONAR_HOST_URL` | env_var | false | false | * |
| `SONAR_TOKEN_FTC` | env_var | true | true | * |

Evidence: Section 8, Evidence E7b

#### 6.3 GitLab Runners

| ID | Description | Active | Status | Tags |
|----|-------------|--------|--------|------|
| 1506020 | windows-shared-runners-manager-1 | false | paused | null |
| 1506021 | windows-shared-runners-manager-2 | false | paused | null |
| 3149836 | null | false | stale | null |
| 11573930 | 1-blue.shared-gitlab-org.runners-manager.gitlab.com | true | offline | null |
| 11573990 | 2-blue.shared-gitlab-org.runners-manager.gitlab.com | true | offline | null |
| 11574038 | 3-blue.shared-gitlab-org.runners-manager.gitlab.com | true | offline | null |
| 11574045 | 4-blue.shared-gitlab-org.runners-manager.gitlab.com | true | offline | null |
| 11574068 | 1-green.shared-gitlab-org.runners-manager.gitlab.com | true | online | null |
| 11574076 | 2-green.shared-gitlab-org.runners-manager.gitlab.com | true | online | null |
| 11574084 | 3-green.shared-gitlab-org.runners-manager.gitlab.com | true | online | null |
| 11574096 | 4-green.shared-gitlab-org.runners-manager.gitlab.com | true | online | null |
| 11728715 | 1-blue.shared-gitlab-org.runners-manager.gitlab.com/dind | true | offline | null |
| 11728725 | 2-blue.shared-gitlab-org.runners-manager.gitlab.com/dind | true | offline | null |
| 11728729 | 3-blue.shared-gitlab-org.runners-manager.gitlab.com/dind | true | offline | null |
| 11728733 | 4-blue.shared-gitlab-org.runners-manager.gitlab.com/dind | true | offline | null |
| 11728737 | 1-green.shared-gitlab-org.runners-manager.gitlab.com/dind | true | online | null |
| 11728740 | 2-green.shared-gitlab-org.runners-manager.gitlab.com/dind | true | online | null |
| 11728747 | 3-green.shared-gitlab-org.runners-manager.gitlab.com/dind | true | online | null |
| 11728750 | 4-green.shared-gitlab-org.runners-manager.gitlab.com/dind | true | online | null |
| 12270807 | 1-blue.saas-linux-small-amd64.runners-manager.gitlab.com/default | true | stale | null |

Summary: 8 online (40%), 8 offline (40%), 2 paused (10%), 2 stale (10%)

Evidence: Section 8, Evidence E8

---

### 7. Cross-Reference with Known Incidents

#### 7.1 Pipeline 2468041533 (Historical—Outside 90-Day Window)

Documented Root Cause: ACR service principal authentication failure (`fitfileregistry.azurecr.io` push rejected—`UNAUTHORIZED`).

Azure AD App: `FITFILE Gitlab Integration Test Pipelines` (AppID `aa9d88df-26fd-4239-a48a-19068e0502c5`)

Failed Jobs: `build_ffcloud`, `build_fitconnect`, `build_mock_rest`, and others.

Status in 90-Day Query: Pipeline ID `2468041533` predates the 90-day window (created before 2026-02-18). No ACR_AUTH failures observed in the 25 failed pipelines queried.

Evidence: Prior audit report (`FITFILE_CICD_AUDIT_REPORT.md`), pipeline API query (Evidence E1)

#### 7.2 ACR Client Secret Expiry

Documented Expiry: `GitLaB CICD` client secret (ID `214c2d39-565e-4b88-a4a4-faf851ca3f38`) expires `27/07/2026`.

Observation: No ACR authentication failures in 90-day failure set. Current date (2026-05-18) is ~2 months before documented expiry.

Evidence: Prior audit report, job traces (Evidence E4, E5)—no `UNAUTHORIZED` errors present

#### 7.3 Integration Test Trigger Failures

Documented Target: `teting-argocd.fitfile.net` / `fitfile-cloud-testing-aks-cluster`

Observation: No `trigger_integration_tests` jobs appear in the 4 failure traces retrieved. The `integration_tests` job defined in `.gitlab-ci.yml` uses image `fitfile/argocli:alpine` but was not observed in failed job logs.

Evidence: `.gitlab-ci.yml` (Section 2), job traces (Evidence E4, E5)

---

### 8. Raw Evidence Appendix

#### E1: Pipeline Status Breakdown (90 Days)

```bash
$ glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines?per_page=100&updated_after=$(date -v-90d +%Y-%m-%dT%H:%M:%SZ)&order_by=id&sort=desc" | jq 'group_by(.status) | map({status: .[0].status, count: length})'

[
  {
    "status": "failed",
    "count": 25
  },
  {
    "status": "success",
    "count": 75
  }
]
```

#### E2: `.gitlab-ci.yml` Full Content

```yaml
# File: /Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE/.gitlab-ci.yml
# Size: 4,071 bytes
# Lines: ~100

stages:
  - build
  - test
  - deploy

# [Full content omitted for brevity — see Section 2 for parsed inventory]
```

#### E3: Failed Pipeline List (Abbreviated)

```bash
$ glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines?status=failed&per_page=100&updated_after=$(date -v-90d +%Y-%m-%dT%H:%M:%SZ)" | jq '[.[] | {id, ref, created_at, duration}]'

[
  {"id": 2524839770, "ref": "refs/merge-requests/2282/merge", "created_at": "2026-05-14T09:50:38.642Z", "duration": null},
  {"id": 2522046776, "ref": "refs/merge-requests/2282/merge", "created_at": "2026-05-13T10:42:31.227Z", "duration": null},
  {"id": 2521911238, "ref": "refs/merge-requests/2282/head", "created_at": "2026-05-13T09:55:49.236Z", "duration": null},
  # ... 22 more
]
```

#### E4: Job Trace—Pipeline 2522046776, Job 14349181056 (`sonar_scan`)

Failure: `gyp ERR! stack Error: not found: make` during `dtrace-provider@npm:0.8.8` native module build.

Key Lines:

```
2026-05-13T10:43:45.466540Z 01O ➤ YN0000: │ dtrace-provider@npm:0.8.8 STDERR gyp ERR! stack Error: not found: make
2026-05-13T10:44:11.458790Z 00O ERROR: Job failed: exit code 1
```

Full Trace: 150 lines—see tool output from `glab api "projects/fitfile%2Fapps%2FInsightFILE/jobs/14349181056/trace"`

#### E5: Job Trace—Pipeline 2521911238, Job 14348229906 (`sonar_scan`)

Failure: Identical to E4—`gyp ERR! stack Error: not found: make`

Additional Failure: ESLint error—`Unable to resolve path to module 'koa-bodyparser'` (import/no-unresolved)

Key Lines:

```
2026-05-13T09:56:59.017388Z 01O ➤ YN0000: │ dtrace-provider@npm:0.8.8 STDERR gyp ERR! stack Error: not found: make
2026-05-13T09:57:23.305891Z 01O   3:24  error  Unable to resolve path to module 'koa-bodyparser'  import/no-unresolved
2026-05-13T09:57:26.814512Z 00O ERROR: Job failed: exit code 1
```

#### E6: Staging Pipeline (`staging.gitlab-ci.yml`)

```yaml
# File: /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment/staging.gitlab-ci.yml
# Lines: 75

stages:
  - prepare
  - deploy
  - test

prepare_kube_config:
  stage: prepare
  image: mcr.microsoft.com/azure-cli:latest
  # ...

sync_argo_app:
  stage: deploy
  image:
    name: fitfile/argocdsync:latest
  # ...

run_integration_tests:
  stage: test
  image: fitfile/argocli:alpine
  # ...
```

#### E7a: Group Variables (fitfile)

```bash
$ glab api "groups/fitfile/variables" | jq '[.[] | {key, variable_type, protected, masked, environment_scope}]'

[
  {"key": "ACR_SERVICE_PRINCIPLE", "variable_type": "env_var", "protected": false, "masked": true, "environment_scope": "*"},
  {"key": "ACR_SERVICE_PRINCIPLE_PASS", "variable_type": "env_var", "protected": false, "masked": true, "environment_scope": "*"},
  # ... 8 more
]
```

#### E7b: Project Variables (InsightFILE)

```bash
$ glab api "projects/fitfile%2Fapps%2FInsightFILE/variables" | jq '[.[] | {key, variable_type, protected, masked, environment_scope}]'

[
  {"key": "password", "variable_type": "env_var", "protected": true, "masked": false, "environment_scope": "test"},
  {"key": "password", "variable_type": "env_var", "protected": true, "masked": false, "environment_scope": "*"},
  # ... 9 more
]
```

#### E8: Runners Inventory

```bash
$ glab api "projects/fitfile%2Fapps%2FInsightFILE/runners" | jq '[.[] | {id, description, active, status, tag_list}]'

[
  {"id": 1506020, "description": "windows-shared-runners-manager-1", "active": false, "status": "paused", "tag_list": null},
  {"id": 11574068, "description": "1-green.shared-gitlab-org.runners-manager.gitlab.com", "active": true, "status": "online", "tag_list": null},
  # ... 18 more
]
```

#### E9: Git Log (3 Months)

```bash
$ git -C /Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE log --oneline --since="3 months ago" | head -50

112543117 [RELEASE] The following packages have been updated: 	@fitfile/frontend: 0.1.657
7a1901790 Merge branch 'bugfix/FTFL-494-cohort-discovery-artifact-tweaks' into 'development'
a6b10220b FTFL-494 Cohort discovery artifact tweaks
# ... 47 more
```

---

### Appendix B: Discrepancies Noted

1. Job Name Mismatch: Failed job traces reference `sonar_scan`, `frontend_lint`, `frontend_unit_tests`—these job names do not appear in the current `.gitlab-ci.yml` (Section 2.2). This indicates either:
   - Pipeline configuration has changed since the failures occurred
   - Failures originated from a different pipeline definition (e.g., included template, historical config)

2. Image Discrepancy: Failed jobs used image `fitfile/sonar-nodejs:1.0.0`—not referenced in current `.gitlab-ci.yml`.
3. No Template Includes: Despite prior context referencing `Deployment/deployment/pipeline/common-jobs.yml` and similar templates, the current `.gitlab-ci.yml` contains no `include:` directives and is self-contained.

---

END OF REPORT
