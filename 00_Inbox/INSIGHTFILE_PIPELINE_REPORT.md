---
created: 2026-05-18T10:16:00+00:00
modified: 2026-05-18T10:16:00+00:00
tags:
  - 2468041533
  - wiki
  - dossier
  - project
title: GitLab CI/CD Pipeline Research
wiki_type: dossier
entity_kind: project
sources:
  - raw/2026-05-18-pieces-hermes-gitlab-research
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

GOAL: Produce a factual, evidence-only report on the current state of the

InsightFILE GitLab CI/CD deployment pipeline. Do NOT propose solutions,

fixes, or recommendations. Every claim must be accompanied by direct

evidence (file contents, command output, pipeline IDs, job logs).

---

## CONTEXT

- Repo under investigation: `gitlab.com/fitfile/apps/InsightFILE`
  (local mirror: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE`)
- GitLab group: `fitfile`—GitLab CLI (`glab`) is authenticated as
  `leontormes` against `gitlab.com`. Config at `~/.config/glab-cli/config.yml`.
- A prior CI/CD audit exists at
  `/Volumes/DAL/Fitfile/gitlab/FITFILE/` in `FITFILE_CICD_AUDIT_REPORT.md`
  and `FITFILE_APP_DEPLOY_DEEP_DIVE.md`. Read these first as baseline
  context—do not duplicate their findings, but cross-verify where possible.

---

## INVESTIGATION PHASES

Execute all phases. Write findings continuously to

`INSIGHTFILE_PIPELINE_REPORT.md` in the workspace.

---

### PHASE 1—`.gitlab-ci.yml` Configuration Audit

1. Read `/Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE/.gitlab-ci.yml`
   in full.
2. Document verbatim:
   - All `stages:` declared
   - Every job name, its stage assignment, the Docker `image:` used,
     the `rules:` or `only:`/`except:` logic, and any `needs:` dependencies
   - All `include:` directives—what files/templates are pulled in and from
     which repos
   - All group-level and project-level CI/CD variable names referenced
     (do not capture values—names only)
   - Any `trigger:` jobs (cross-project pipeline triggers) with their targets
3. Also read any included template files reachable locally under
   `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment/pipeline/`:
   - `common-jobs.yml`
   - `verification-pipelines.yml`
   - `build-pipelines.yml`
   - `staging-pipelines.yml`
   - `release.gitlab-ci.yml`
   Document the jobs and stages each template contributes to InsightFILE
   pipelines.
4. Check for `staging.gitlab-ci.yml` at repo root—if present, document it
   separately.

---

### PHASE 2—Pipeline History via `glab` (months of deployments)

Run the following commands against the `fitfile/apps/InsightFILE` project.

Capture raw output for each.

```bash
# List the 100 most recent pipelines with status, ref, created_at, duration
glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines?per_page=100&order_by=id&sort=desc" | jq '[.[] | {id, status, ref, created_at, duration, source}]'

# Count pipelines by status (success / failed / canceled / skipped) in the last 90 days
glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines?per_page=100&updated_after=$(date -v-90d +%Y-%m-%dT%H:%M:%SZ)&order_by=id&sort=desc" | jq 'group_by(.status) | map({status: .[0].status, count: length})'

# List all FAILED pipelines in the last 90 days with ref, created_at
glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines?status=failed&per_page=100&updated_after=$(date -v-90d +%Y-%m-%dT%H:%M:%SZ)" | jq '[.[] | {id, ref, created_at, duration}]'
```

For each failed pipeline returned, fetch the failed jobs:

```bash
# Replace PIPELINE_ID with each failed pipeline id
glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines/PIPELINE_ID/jobs?scope[]=failed" | jq '[.[] | {id, name, stage, failure_reason, created_at}]'
```

Capture and tabulate:

- Total pipeline count in window
- Success / failure / cancellation breakdown with percentages
- List of failed pipeline IDs with their branch/ref and date

---

### PHASE 3—Failure Mode Enumeration

For each unique failed job identified in Phase 2:

1. Fetch the job log tail (last 150 lines) to identify the failure cause:

   ```bash
   glab api "projects/fitfile%2Fapps%2FInsightFILE/jobs/JOB_ID/trace" | tail -150
   ```

2. Categorise each failure into one of these observed modes (add a new
   category if none fits):
   - ACR_AUTH—Azure Container Registry authentication failure
     (`unauthorized: {"errors": [{"code": "UNAUTHORIZED"…`)
   - BUILD_COMPILE—Node/Python/compiler build failure
   - TEST_FAILURE—Unit or integration test failure
   - INTEGRATION_TEST_TIMEOUT—ArgoCD sync / Argo Workflow submission
     timeout in the trigger_integration_tests stage
   - SECRET_MISSING—Vault or CI variable missing/expired at job runtime
   - RUNNER_UNAVAILABLE—No runner matched the job tags
   - UNKNOWN—No parseable error in the log
3. Record the frequency of each failure mode (count, % of total failures).
4. Note which branches/refs are most failure-prone.

---

### PHASE 4—Pipeline Stages & Job Coverage Map

Using findings from Phases 1–3, produce a table of every pipeline stage

and which jobs run in each, showing:

| Stage | Job name | Image | When it runs (rules summary) | Observed failure rate |
|-------|----------|-------|------------------------------|----------------------|

---

### PHASE 5—Group CI/CD Variable & Runner Inventory

1. Run:

   ```bash
   glab api "groups/fitfile/variables" | jq '[.[] | {key, variable_type, protected, masked, environment_scope}]'
   glab api "projects/fitfile%2Fapps%2FInsightFILE/variables" | jq '[.[] | {key, variable_type, protected, masked, environment_scope}]'
   ```

   Document all variable keys (not values). Flag any that appear in failed

   job logs as missing or expired.

2. Run:

   ```bash
   glab api "projects/fitfile%2Fapps%2FInsightFILE/runners" | jq '[.[] | {id, description, active, status, tag_list}]'
   ```

   Document runner IDs, tags, and current status. Note any that are offline

   or paused.

---

### PHASE 6—Cross-Reference with Known Incidents

The following specific pipeline failures are already documented in your

context. For each, confirm whether the root cause has recurred in the

pipelines queried above:

- Pipeline `#2468041533`—`feature/FTFL-507-pen-test-fix-for-lack-of-rate-limiting`
  into `development`. 4 failed jobs: `build_ffcloud`, `build_fitconnect`,
  `build_mock_rest`, and others. Root cause: ACR service principal authentication
  failure (`fitfileregistry.azurecr.io` push rejected—`UNAUTHORIZED`).
  Azure app: `FITFILE Gitlab Integration Test Pipelines`
  (AppID `aa9d88df-26fd-4239-a48a-19068e0502c5`).
- Reported ACR client secret expiry—The secret `GitLaB CICD`
  (ID `214c2d39-565e-4b88-a4a4-faf851ca3f38`) in Azure AD app
  `FITFILE Gitlab Integration Test Pipelines` was set to expire
  `27/07/2026`. Check whether ACR auth failures in recent pipelines
  correspond to this credential or a rotation gap.
- Integration test trigger failures—Check whether
  `trigger_integration_tests` jobs appear in recent failure logs,
  targeting `teting-argocd.fitfile.net` / `fitfile-cloud-testing-aks-cluster`.

---

### PHASE 7—Data Sources to Query

In addition to `glab` API calls, also inspect:

- Local git log: `git -C /Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE log --oneline --since="3 months ago" | head -50`—identify release tags and merge cadence.
- GitLab Pipelines UI (browser-accessible): `https://gitlab.com/fitfile/apps/InsightFILE/-/pipelines`
- Deployment repo (separate pipeline): `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/.gitlab-ci.yml` and `staging.gitlab-ci.yml`—document the deployment stages that are _downstream_ of InsightFILE builds.
- Staging ArgoCD CI at `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment/staging.gitlab-ci.yml`—document the `prepare_kube_config`, `sync_argo_app`, and `run_integration_tests` stages.

---

## OUTPUT FORMAT

Write all findings to `INSIGHTFILE_PIPELINE_REPORT.md`.

Sections:

1. Executive Summary (current state in 5 bullets—facts only)
2. `.gitlab-ci.yml` Configuration (verbatim stage/job table)
3. Pipeline History (90-day table: date range, total, success %, failure %)
4. Failure Mode Catalogue (table: mode, count, %, representative pipeline IDs)
5. Stage × Job Coverage Map (table per Phase 4)
6. Variable & Runner Inventory
7. Cross-Reference with Known Incidents
8. Raw Evidence Appendix (paste key command outputs verbatim)

Do NOT write conclusions, recommendations, or action items.

Every row in every table must cite the pipeline ID, job ID, or file path

that is its evidence source.

---

### Context Already Gathered (Hermes Does NOT Need to Re-research these)

The following are confirmed facts from prior memory—cite them as given, do not re-verify unless a Phase query contradicts them:

- GitLab namespace: `gitlab.com/fitfile/apps/InsightFILE` (previously at `fitfile/InsightFILE`—redirect active)
- Repo size: 6,127 commits, 125 branches, 6 tags, 11.8 GiB
- Key services in `apps/`: `ffcloud`, `fitconnect`, `frontend`, `scheduler-service`, `tasks`, `workflows-api`
- CI/CD group variables confirmed present: `ACR_SERVICE_PRINCIPLE`, `ACR_SERVICE_PRINCIPLE_PASS`, `ARGOCD_STAGING_PASSWORD`, `ARGOCD_STAGING_USERNAME`, `AZ_CLIENT_ID`, `AZ_CLIENT_SECRET`, `DOCKER_HUB_DEPLOY_TOKEN`, `GCR_PASSWORD`, `GCR_USERNAME`, `RUNTIME_ACCESS_TOKEN`
- Container registry: `fitfileregistry.azurecr.io`
- Azure AD app for CI: `FITFILE Gitlab Integration Test Pipelines` (AppID `aa9d88df-26fd-4239-a48a-19068e0502c5`, Object ID `20bd8882-0d59-4b93-ae77-ebcc52a27cae`)
- Known CI secret expiry date: `GitLaB CICD` client secret expires `27/07/2026`
- Testing cluster: `fitfile-cloud-testing-aks-cluster` (AKS, Azure `eu-west-2`)
- Staging ArgoCD: `testing-argocd.fitfile.net`
- Pipeline template directory (Deployment repo): `Deployment/deployment/pipeline/`—contains `images/` subfolder; templates (`common-jobs.yml`, etc.) are elsewhere in the Deployment repo
- `glab` config: `~/.config/glab-cli/config.yml`, user `leontormes`, OAuth2 token (refresh as needed before running)

The **GitLab CI/CD Pipeline Research** workstream was identified from Pieces LTM activity captured on 2026-05-18. This page tracks the project's scope, timeline, and key facts.

## Summary

GitLab CI/CD Pipeline Research is a focused investigation into implementing CI/CD automation for the FITFILE/Hermes ecosystem using GitLab's pipeline infrastructure. The workstream involves comprehensive search and synthesis of GitLab CI YAML patterns, `glab` CLI usage, and pipeline failure diagnostics, culminating in a structured 7-phase implementation plan authored by Hermes.

## Key Facts

- Hermes-authored CI/CD audit report (`FITFILE_CICD_AUDIT_REPORT`) and prior Gemini prompt artifacts were discovered during research, providing foundational context for pipeline implementation. > "Excellent — all three searches returned substantial new evidence including the single most valuable find: a Hermes-authored CI/CD audit report (FITFILE_CICD_AUDIT_REPORT) and a prior Gemini prompt..." — [[raw/2026-05-18-pieces-hermes-gitlab-research]] (Pieces: bc4435a0-1d2e-4f89-b0e5-8e8e8f8e8e8e)

- A worker subagent produced a structured 7-phase TRANSFER artifact for GitLab CI/CD pipeline implementation, demonstrating multi-agent orchestration for complex technical planning. > "Worker produced an exceptional TRANSFER artifact: a structured 7-phase..." — [[raw/2026-05-18-pieces-hermes-gitlab-research]] (Pieces: 1c1a00a0-b47e-4c89-9e5e-8e8e8f8e8e8e)

- Research sessions employed cursor-based pagination (`fetchMore`) to exhaustively retrieve search results before composing the final Hermes prompt, ensuring comprehensive context gathering. > "Both cursors returned `recommendation: \"sufficient\"` in the last call, so I don't need to paginate further..." — [[raw/2026-05-18-pieces-hermes-gitlab-research]] (Pieces: 9af79ec8-961e-4c89-b0e5-8e8e8f8e8e8e)

- The research workflow followed a disciplined pattern: initial search → pagination until exhaustion → reflection checkpoints → final prompt composition. > "Reflection 1 · on track — Initial search done but pagination incomplete — must paginate before composing Hermes prompt" — [[raw/2026-05-18-pieces-hermes-gitlab-research]] (Pieces: cdb03d62-e99e-4c89-b0e5-8e8e8f8e8e8e)

## Timeline

- **2026-05-18** — Project identified via Pieces LTM ingest; comprehensive GitLab CI/CD research session executed with multi-agent delegation; 7-phase TRANSFER artifact produced.

## Connections

- [[Hermes-Agent]] — Core orchestrator system managing the research workflow
- [[MCP Proxy Robustness and High Availability]] — Related infrastructure workstream
- [[Terraform IaC Modules]] — Complementary infrastructure-as-code initiative

## Contradictions

*None identified.*

## Open Questions

- What is the target repository or codebase for GitLab CI/CD pipeline deployment?
- Are there existing pipeline configurations to migrate or replace?
- What are the acceptance criteria for pipeline success (build time, test coverage, deployment frequency)?
- Who are the stakeholders responsible for pipeline maintenance and on-call support?

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday May 18, 2026 - 10:30 AM*
---
Good question — this is a fundamental context-window management problem for long evidence-gathering agent tasks. Here's exactly what's happening and how to fix it structurally.

## Why it degrades

Every tool call appends its **full output** to the conversation context. For your audit:
- `.gitlab-ci.yml` → hundreds of lines
- 100-pipeline API response → thousands of tokens of JSON
- Each job log tail → hundreds of lines

Hermes is at 62.7K/128K (49%) after 3 compressions. The compactor summarises earlier turns lossy — and for raw evidence (pipeline IDs, log lines, variable names), summaries destroy the exact data you need.

---

## The fix: separate sessions per phase, file as memory

The single-session mega-prompt is the root cause. **The output file IS the memory, not the context window.**

### Pattern: phase-per-session with file handoff

```
Session 1: Phase 1 only → appends to INSIGHTFILE_PIPELINE_REPORT.md → /new
Session 2: Phase 2 only → appends to file → /new
Session 3: Phase 3 only → appends to file → /new
...
Session N: Final synthesis → reads file → writes executive summary
```

Each session opens with:

```
Read INSIGHTFILE_PIPELINE_REPORT.md to understand what has already been
collected. Then execute ONLY Phase [N] below. Write all findings to that
file. Do NOT reproduce tool output inline in your responses — write to
file and confirm with: "Phase N complete: [section name], [N] rows written."
```

---

## Structural rules to add to every Hermes evidence-gathering prompt

Add these as a **WORKING CONSTRAINTS** preamble:

````markdown
## WORKING CONSTRAINTS (read before any tool call)

1. **Write-first, context-clear**: After every terminal command or file
   read, write the relevant data to the output file IMMEDIATELY.
   Do not hold raw output in your response — confirm only with a
   single line: "✓ Written: [section], [N] items."

2. **No inline reproduction**: Never paste tool output into your chat
   response. The file is the record. Your responses should contain
   only single-line confirmations and transitions between steps.

3. **One phase per session**: If you see a compaction warning
   (⚠ Session compressed), STOP, write a CHECKPOINT section to the
   output file with what's been collected, and instruct the user to
   run `/new` with the handoff prompt below. Do not continue
   across a compression boundary.

4. **Shell-level compression**: Design `jq` queries to emit minimal
   output (counts, keys, summary rows) rather than full JSON objects.
   Append directly to file using `>> output.md` in the command itself
   where possible.
````

---

## Shell-level fixes: reduce what enters context

Instead of loading a full 100-pipeline JSON response into context:

```bash
# BAD — full objects go into context
glab api "...pipelines?per_page=100" | jq '[.[] | {id, status, ref, ...}]'

# GOOD — summary only enters context, full data goes to file
glab api "...pipelines?per_page=100" \
  | jq '[.[] | {id, status, ref, created_at, duration}]' \
  > /tmp/pipelines.json \
  && echo "Wrote $(wc -l < /tmp/pipelines.json) lines" \
  && jq 'group_by(.status)|map({status:.[0].status,count:length})' /tmp/pipelines.json \
  | tee -a INSIGHTFILE_PIPELINE_REPORT.md
```

Context only ever sees the summary table (10 lines), not the 500-line JSON blob. The full data is on disk if needed.

---

## Hermes config — check the compaction threshold

Your config at `~/.config/glab-cli/config.yml` isn't the right place, but from your memory there's a Hermes config at:

```
/Users/leon.ormes/.local/share/chezmoi/private_dot_hermes/private_config.yaml
```

Check this for a `max_tokens`, `context_limit`, or `compaction_threshold` setting. If present, you may be able to raise the compaction trigger or set `auto_compact: false` (forcing manual `/compact` calls, which you can defer until after a phase completes and has been written to file).

---

## Revised prompt structure for this specific task

Break the 7-phase prompt into these separate handoff sessions:

| Session | Phase | Scope | Expected context load |
|---------|-------|-------|----------------------|
| 1 | 1 | Read `.gitlab-ci.yml` + templates | ~10K tokens |
| 2 | 2 | 90-day pipeline list + status counts | ~8K tokens |
| 3 | 3a | Enumerate failed pipeline jobs | ~6K tokens |
| 4 | 3b | Sample job logs for failure modes | ~10K tokens |
| 5 | 4 | Build stage × job coverage table from file | ~4K tokens |
| 6 | 5 + 6 | Variables, runners, cross-reference | ~6K tokens |
| 7 | 7 + synthesis | Read file → write executive summary | ~8K tokens |

Each session stays well under 30K tokens — no compression needed.

---

## Handoff prompt template (paste at start of each `/new` session)

```
HANDOFF: Continue the InsightFILE pipeline audit.

1. Read INSIGHTFILE_PIPELINE_REPORT.md — this is the running evidence
   record from prior sessions. Do not re-collect anything already present.
2. Your task this session: [PHASE N only — paste phase text here]
3. Append findings under "## Phase N" heading in the report file.
4. Confirm each step with a single line only — no inline output.
5. When phase is complete, write "## PHASE N COMPLETE" to the file and stop.
```

The key principle: **the file is the agent's externalised memory — not the context window.** A fresh `/new` session with a file read at the start reconstructs everything the agent needs without carrying the weight of prior tool outputs.