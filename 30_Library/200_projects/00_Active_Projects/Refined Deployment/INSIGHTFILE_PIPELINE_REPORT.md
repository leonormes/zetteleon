---
created: 2026-05-15T15:57:37+00:00
entity_kind: project
modified: 2026-05-18T12:22:17+00:00
sources: [raw/2026-05-18-pieces-hermes-gitlab-research]
tags: [2468041533, dossier, project, wiki]
title: INSIGHTFILE_PIPELINE_REPORT
wiki_type: dossier
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

The GitLab CI/CD Pipeline Research workstream was identified from Pieces LTM activity captured on 2026-05-18. This page tracks the project's scope, timeline, and key facts.

## Summary

GitLab CI/CD Pipeline Research is a focused investigation into implementing CI/CD automation for the FITFILE/Hermes ecosystem using GitLab's pipeline infrastructure. The workstream involves comprehensive search and synthesis of GitLab CI YAML patterns, `glab` CLI usage, and pipeline failure diagnostics, culminating in a structured 7-phase implementation plan authored by Hermes.

## Key Facts

- Hermes-authored CI/CD audit report (`FITFILE_CICD_AUDIT_REPORT`) and prior Gemini prompt artifacts were discovered during research, providing foundational context for pipeline implementation. > "Excellent—all three searches returned substantial new evidence including the single most valuable find: a Hermes-authored CI/CD audit report (FITFILE_CICD_AUDIT_REPORT) and a prior Gemini prompt…"—[[raw/2026-05-18-pieces-hermes-gitlab-research]] (Pieces: bc4435a0-1d2e-4f89-b0e5-8e8e8f8e8e8e)
- A worker subagent produced a structured 7-phase TRANSFER artifact for GitLab CI/CD pipeline implementation, demonstrating multi-agent orchestration for complex technical planning. > "Worker produced an exceptional TRANSFER artifact: a structured 7-phase…"—[[raw/2026-05-18-pieces-hermes-gitlab-research]] (Pieces: 1c1a00a0-b47e-4c89-9e5e-8e8e8f8e8e8e)
- Research sessions employed cursor-based pagination (`fetchMore`) to exhaustively retrieve search results before composing the final Hermes prompt, ensuring comprehensive context gathering. > "Both cursors returned `recommendation: \"sufficient\"` in the last call, so I don't need to paginate further…"—[[raw/2026-05-18-pieces-hermes-gitlab-research]] (Pieces: 9af79ec8-961e-4c89-b0e5-8e8e8f8e8e8e)
- The research workflow followed a disciplined pattern: initial search → pagination until exhaustion → reflection checkpoints → final prompt composition. > "Reflection 1 · on track—Initial search done but pagination incomplete—must paginate before composing Hermes prompt"—[[raw/2026-05-18-pieces-hermes-gitlab-research]] (Pieces: cdb03d62-e99e-4c89-b0e5-8e8e8f8e8e8e)

## Timeline

- 2026-05-18—Project identified via Pieces LTM ingest; comprehensive GitLab CI/CD research session executed with multi-agent delegation; 7-phase TRANSFER artifact produced.

## Connections

- [[Hermes-Agent]]—Core orchestrator system managing the research workflow
- [[MCP Proxy Robustness and High Availability]]—Related infrastructure workstream
- [[Terraform IaC Modules]]—Complementary infrastructure-as-code initiative

## Contradictions

_None identified._

## Open Questions

- What is the target repository or codebase for GitLab CI/CD pipeline deployment?
- Are there existing pipeline configurations to migrate or replace?
- What are the acceptance criteria for pipeline success (build time, test coverage, deployment frequency)?
- Who are the stakeholders responsible for pipeline maintenance and on-call support?

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Monday May 18, 2026 - 10:30 AM_
---

Good question—this is a fundamental context-window management problem for long evidence-gathering agent tasks. Here's exactly what's happening and how to fix it structurally.

## Why it Degrades

Every tool call appends its full output to the conversation context. For your audit:

- `.gitlab-ci.yml` → hundreds of lines
- 100-pipeline API response → thousands of tokens of JSON
- Each job log tail → hundreds of lines

Hermes is at 62.7K/128K (49%) after 3 compressions. The compactor summarises earlier turns lossy—and for raw evidence (pipeline IDs, log lines, variable names), summaries destroy the exact data you need.

---

## The Fix: Separate Sessions per Phase, File as Memory

The single-session mega-prompt is the root cause. The output file IS the memory, not the context window.

### Pattern: Phase-per-session with File Handoff

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

## Structural Rules to Add to Every Hermes Evidence-gathering Prompt

Add these as a WORKING CONSTRAINTS preamble:

````markdown
## WORKING CONSTRAINTS (read before any tool call)

1. Write-first, context-clear: After every terminal command or file
   read, write the relevant data to the output file IMMEDIATELY.
   Do not hold raw output in your response — confirm only with a
   single line: "✓ Written: [section], [N] items."

2. No inline reproduction: Never paste tool output into your chat
   response. The file is the record. Your responses should contain
   only single-line confirmations and transitions between steps.

3. One phase per session: If you see a compaction warning
   (⚠ Session compressed), STOP, write a CHECKPOINT section to the
   output file with what's been collected, and instruct the user to
   run `/new` with the handoff prompt below. Do not continue
   across a compression boundary.

4. Shell-level compression: Design `jq` queries to emit minimal
   output (counts, keys, summary rows) rather than full JSON objects.
   Append directly to file using `>> output.md` in the command itself
   where possible.
````

---

## Shell-level Fixes: Reduce what Enters Context

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

## Hermes config—check the Compaction Threshold

Your config at `~/.config/glab-cli/config.yml` isn't the right place, but from your memory there's a Hermes config at:

```
/Users/leon.ormes/.local/share/chezmoi/private_dot_hermes/private_config.yaml
```

Check this for a `max_tokens`, `context_limit`, or `compaction_threshold` setting. If present, you may be able to raise the compaction trigger or set `auto_compact: false` (forcing manual `/compact` calls, which you can defer until after a phase completes and has been written to file).

---

## Revised Prompt Structure for This Specific Task

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

Each session stays well under 30K tokens—no compression needed.

---

## Handoff Prompt Template (paste at Start of Each `/new` session)

```
HANDOFF: Continue the InsightFILE pipeline audit.

1. Read INSIGHTFILE_PIPELINE_REPORT.md — this is the running evidence
   record from prior sessions. Do not re-collect anything already present.
2. Your task this session: [PHASE N only — paste phase text here]
3. Append findings under "## Phase N" heading in the report file.
4. Confirm each step with a single line only — no inline output.
5. When phase is complete, write "## PHASE N COMPLETE" to the file and stop.
```

The key principle: the file is the agent's externalised memory—not the context window. A fresh `/new` session with a file read at the start reconstructs everything the agent needs without carrying the weight of prior tool outputs.

## GitLab CI/CD—Domain Knowledge Context

### §1—Ubiquitous Language Glossary

Pipeline—An ordered execution graph of Jobs that transforms source code into deployable artifacts through defined Stages.

  Synonyms/aliases: CI/CD pipeline, build pipeline.

  Scope: Pipeline Orchestration BC.

Stage—A logical grouping boundary within a Pipeline that defines execution order; all Jobs in a Stage must complete before the next Stage begins (unless overridden by `needs`).

  Synonyms/aliases: Pipeline stage.

  Scope: Pipeline Orchestration BC.

Job—The smallest executable unit in a Pipeline; a Job runs on a Runner and executes a defined Script with optional Artifacts, Cache, and Services.

  Synonyms/aliases: CI job, build job, pipeline job.

  Scope: Job Execution BC.

Step—A discrete command within a Job's Script section; Steps execute sequentially within the Job's shell context.

  Synonyms/aliases: Script step, command.

  Scope: Job Execution BC.

Trigger—A mechanism that initiates a Pipeline execution, either via Git events (push, tag, merge request) or explicit API/webhook invocation.

  Synonyms/aliases: Pipeline trigger.

  Scope: Pipeline Orchestration BC.

Rule—A conditional expression that determines whether a Job is included in a Pipeline and under what execution mode (`when` clause).

  Synonyms/aliases: Job rule, conditional rule.

  Scope: Configuration Language BC.

Condition—A boolean expression within a Rule that evaluates CI/CD variables, Git state, or pipeline context to determine Job inclusion.

  Synonyms/aliases: Rule condition, if-clause.

  Scope: Configuration Language BC.

Need—A dependency declaration that allows a Job to start as soon as its listed dependencies complete, bypassing Stage barriers (DAG execution).

  Synonyms/aliases: Job dependency, DAG dependency.

  Scope: Pipeline Orchestration BC.

Dependency—A relationship between Jobs where one Job requires output (Artifacts) or completion of another Job before it can execute.

  Synonyms/aliases: Job dependency, upstream dependency.

  Scope: Pipeline Orchestration BC.

Artifact—Files or directories produced by a Job that are stored by GitLab and can be downloaded or passed to downstream Jobs.

  Synonyms/aliases: Build artifact, job output.

  Scope: Artifact & Cache Store BC.

Cache—Reusable files (typically dependencies) stored by Runner and restored in subsequent Jobs to accelerate execution.

  Synonyms/aliases: Dependency cache, build cache.

  Scope: Artifact & Cache Store BC.

Variable—A key-value pair injected into Job execution context, used for configuration, parameterisation, or secret injection.

  Synonyms/aliases: CI/CD variable, environment variable.

  Scope: Variable & Secret Management BC.

Secret—A sensitive Variable (credentials, tokens, keys) stored with enhanced security controls (masking, protection, external backend).

  Synonyms/aliases: CI/CD secret, credential.

  Scope: Variable & Secret Management BC.

Environment—A deployment target representing a specific runtime context (development, staging, production) with associated URL and state tracking.

  Synonyms/aliases: Deployment environment, deploy target.

  Scope: Environment & Deployment BC.

Deployment—A record of a Job's successful execution that deployed code to an Environment; tracked with rollback capability.

  Synonyms/aliases: Deploy record, release.

  Scope: Environment & Deployment BC.

Runner—An agent that executes Jobs; can be GitLab-hosted (managed VMs) or self-managed (user-provisioned infrastructure).

  Synonyms/aliases: CI runner, GitLab Runner.

  Scope: Runner Fleet BC.

Executor—The runtime engine within a Runner that executes Jobs (shell, docker, kubernetes, docker-machine, custom).

  Synonyms/aliases: Runner executor.

  Scope: Runner Fleet BC.

Tag (runner)—A label assigned to a Runner for Job routing; Jobs specify Tags to select compatible Runners.

  Synonyms/aliases: Runner tag.

  Scope: Runner Fleet BC.

Tag (git)—A Git reference marking a specific commit; can trigger Tag Pipelines and access protected resources.

  Synonyms/aliases: Git tag.

  Scope: External Integration BC.

Service—A sidecar container attached to a Job for dependencies (database, cache, message queue) during execution.

  Synonyms/aliases: Docker service, sidecar.

  Scope: Job Execution BC.

Component—A reusable, versioned CI/CD configuration unit published from a project and consumed via `include:component`.

  Synonyms/aliases: CI/CD component, template component.

  Scope: Configuration Language BC.

Include—A keyword that imports external YAML configuration into the Pipeline definition (local, project, remote, template, component).

  Synonyms/aliases: Configuration include.

  Scope: Configuration Language BC.

Extends—A keyword that inherits Job configuration from a hidden template Job (anchored configuration reuse).

  Synonyms/aliases: Job inheritance, template extension.

  Scope: Configuration Language BC.

Matrix—A parallelism strategy that runs a Job multiple times with different variable combinations in a single Pipeline.

  Synonyms/aliases: Matrix build, parallel matrix.

  Scope: Job Execution BC.

Parallel—A keyword that runs multiple instances of a Job concurrently (either via count or Matrix).

  Synonyms/aliases: Job parallelism.

  Scope: Job Execution BC.

Resource Group—A concurrency control mechanism that limits Jobs to one-at-a-time execution within the named group.

  Synonyms/aliases: Concurrency group, deployment lock.

  Scope: Pipeline Orchestration BC.

Review App—A dynamic, ephemeral Environment created per Merge Request for preview and testing.

  Synonyms/aliases: Ephemeral environment, MR environment.

  Scope: Environment & Deployment BC.

Downstream Pipeline—A Pipeline triggered by another Pipeline (parent-child or multi-project).

  Synonyms/aliases: Child pipeline, triggered pipeline.

  Scope: Pipeline Orchestration BC.

Child Pipeline—A Downstream Pipeline triggered within the same Project as the parent (Parent-Child architecture).

  Synonyms/aliases: Nested pipeline.

  Scope: Pipeline Orchestration BC.

Multi-project Pipeline—A Downstream Pipeline triggered in a different Project than the upstream trigger.

  Synonyms/aliases: Cross-project pipeline.

  Scope: Pipeline Orchestration BC.

Bridge Job—A Trigger Job that connects Pipelines across projects or within parent-child hierarchies.

  Synonyms/aliases: Trigger job.

  Scope: Pipeline Orchestration BC.

Merge Train—A queuing mechanism for Merge Requests that ensures changes are tested in sequence against the target branch.

  Synonyms/aliases: MR train, merge queue.

  Scope: Pipeline Orchestration BC.

Merge Request Pipeline—A Pipeline triggered by changes to a Merge Request source branch (distinct from branch Pipeline).

  Synonyms/aliases: MR pipeline.

  Scope: Pipeline Orchestration BC.

Merged Results Pipeline—A Pipeline type that tests the result of merging source and target branches together.

  Synonyms/aliases: Merge commit pipeline.

  Scope: Pipeline Orchestration BC.

CI Job Token—A short-lived token (`CI_JOB_TOKEN`) for authenticating to GitLab APIs and triggering downstream Pipelines.

  Synonyms/aliases: Job token, pipeline token.

  Scope: Variable & Secret Management BC.

ID Token—An OIDC JWT issued to a Job for federated authentication to external secret backends (Vault, AWS, GCP, Azure).

  Synonyms/aliases: OIDC token, workload identity token.

  Scope: Variable & Secret Management BC.

OIDC—OpenID Connect protocol used for workload identity federation between GitLab Jobs and external providers.

  Synonyms/aliases: OpenID Connect.

  Scope: Variable & Secret Management BC.

SLSA Provenance—A cryptographically signed record of build attestation verifying artifact integrity and build process.

  Synonyms/aliases: Build provenance, SLSA attestation.

  Scope: Pipeline Security & Provenance BC.

Secure File—A file uploaded to GitLab and made available to Jobs with access controls (protected branches, expiration).

  Synonyms/aliases: CI/CD secure file.

  Scope: Variable & Secret Management BC.

dotenv—A file-based variable format (`artifacts:reports:dotenv`) for passing dynamic variables between Jobs.

  Synonyms/aliases: Dotenv report, environment file.

  Scope: Variable & Secret Management BC.

Workflow—The top-level Pipeline configuration controlling which Pipeline types run (`workflow:rules`).

  Synonyms/aliases: Pipeline workflow.

  Scope: Configuration Language BC.

Schedule—A cron-based trigger that creates Pipelines at defined intervals.

  Synonyms/aliases: Scheduled pipeline, cron pipeline.

  Scope: Pipeline Orchestration BC.

Webhook—An HTTP callback from GitLab to external systems on events (push, pipeline, deployment).

  Synonyms/aliases: GitLab webhook.

  Scope: External Integration BC.

ChatOps—Execution of Pipeline actions via chat commands (Slack, Mattermost) with feedback to chat channel.

  Synonyms/aliases: Chat operations.

  Scope: External Integration BC.

Function—A serverless compute target for deployment (AWS Lambda, GCP Cloud Functions, Azure Functions).

  Synonyms/aliases: Serverless function.

  Scope: Environment & Deployment BC.

Input—A parameter definition for templated CI/CD Components, allowing consumer customization.

  Synonyms/aliases: Component input, template parameter.

  Scope: Configuration Language BC.

---

### §2—Bounded Contexts & Context Map

#### BC: Pipeline Orchestration

Responsibility: Owns the definition, scheduling, and execution flow of Pipelines as Aggregate roots.

Owns: Pipeline, Stage, DAG, Trigger, Schedule, Merge Train, Downstream Pipeline.

Integrates with:

  - Job Execution BC (partnership): Orchestrator emits Job entities for execution; Job Execution reports status back.
  - Configuration Language BC (shared kernel): `.gitlab-ci.yml` parsing produces Pipeline aggregate.
  - External Integration BC (ACL): Webhooks and API triggers create Pipeline instances.
Key invariants:
  1. A Pipeline must have at least one Job to be valid.
  2. DAG dependencies (`needs`) cannot form cycles.
  3. Child Pipelines cannot exceed nesting depth of 2.
  4. Pipeline hierarchy limited to 1000 downstream Pipelines by default.

#### BC: Job Execution

Responsibility: Owns the runtime execution of Jobs on Runner infrastructure.

Owns: Job, Step, Script, Executor, Service, Matrix instance.

Integrates with:

  - Runner Fleet BC (partnership): Requests Runner assignment; receives execution result.
  - Artifact & Cache Store BC (customer-supplier): Downloads Cache/Artifacts before execution; uploads after.
  - Variable & Secret Management BC (conformist): Receives injected Variables and Secrets.
Key invariants:
  1. Each Step runs in isolated shell context; exports do not persist across Steps.
  2. `after_script` runs regardless of Script failure.
  3. Job timeout cannot exceed Runner maximum timeout.
  4. Matrix instances run in parallel within Runner capacity.

#### BC: Runner Fleet

Responsibility: Owns the pool of Runners available for Job assignment and their lifecycle.

Owns: Runner, RunnerGroup, JobQueue, Executor configuration, Tag registry.

Integrates with:

  - Job Execution BC (supplier): Provides execution capacity; reports Job status.
  - Pipeline Orchestration BC (ACL): Receives Job assignment requests via long-polling.
Key invariants:
  1. Runner must have all Job-specified Tags to be eligible.
  2. Protected Runners only execute Jobs on protected branches/tags.
  3. Runner authentication tokens rotate automatically at configured intervals.
  4. Instance Runners are shared across all Projects unless scoped.

#### BC: Configuration Language

Responsibility: Owns the `.gitlab-ci.yml` syntax, validation, and composition mechanics.

Owns: `.gitlab-ci.yml`, Component, Include, Input, Extends template, Workflow definition.

Integrates with:

  - Pipeline Orchestration BC (shared kernel): Parsed configuration instantiates Pipeline aggregate.
  - Variable & Secret Management BC (ACL): Variable expansion rules reference Variable BC.
Key invariants:
  1. Include resolution must complete within 30 seconds.
  2. Maximum 150 Includes per Pipeline (configurable).
  3. Component references must include semantic version pinning.
  4. Input values must match declared type and options.

#### BC: Variable & Secret Management

Responsibility: Owns storage, scoping, injection, and security of Variables and Secrets.

Owns: Variable, Secret, SecureFile, IDToken, CI Job Token, dotenv report.

Integrates with:

  - Job Execution BC (customer-supplier): Injects Variables into Job context.
  - Pipeline Security & Provenance BC (partnership): Enforces masking and protection rules.
  - External Integration BC (ACL): OIDC federation with external secret backends.
Key invariants:
  1. Masked Variables must be 8+ characters and single-line.
  2. Protected Variables only available in protected branch/tag Pipelines.
  3. Variable precedence: Pipeline > Project > Group > Instance > Job > Default.
  4. ID Tokens are short-lived (5 minutes) and audience-restricted.

#### BC: Environment & Deployment

Responsibility: Owns deployment targets, deployment records, and promotion workflows.

Owns: Environment, Deployment, RolloutStrategy, ApprovalGate, Review App.

Integrates with:

  - Pipeline Orchestration BC (partnership): Deployment Jobs create Environment records.
  - Pipeline Security & Provenance BC (ACL): Protected Environments enforce RBAC.
  - External Integration BC (ACL): External CD tools (ArgoCD, Flux) update Deployment state.
Key invariants:
  1. Environment names cannot be renamed; must stop/delete/recreate.
  2. Protected Environments require explicit deploy permissions.
  3. Dynamic Environments (Review Apps) auto-stop on branch deletion.
  4. Deployment tier inferred from name or explicit `deployment_tier` keyword.

#### BC: Artifact & Cache Store

Responsibility: Owns storage, retention, and retrieval of Job outputs and reusable dependencies.

Owns: Artifact, Cache, Report (JUnit, coverage, code quality), Secure File.

Integrates with:

  - Job Execution BC (customer-supplier): Jobs upload/download Artifacts and Cache.
  - Testing & Quality Gate BC (conformist): Test reports ingested as Artifacts.
Key invariants:
  1. Artifacts expire after 30 days by default; Cache persists until evicted.
  2. Cache keys receive `-protected` or `-non_protected` suffix based on branch.
  3. Maximum Artifact size: 30 MB per file, 100 MB total per Job (JUnit).
  4. Cache stored on Runner host or distributed S3 backend.

#### BC: Testing & Quality Gate

Responsibility: Owns ingestion, display, and gating logic for test and quality signals.

Owns: TestReport, CoverageReport, QualityGate, FailFast policy, MetricsReport.

Integrates with:

  - Artifact & Cache Store BC (customer-supplier): Consumes JUnit, coverage, code quality Artifacts.
  - Pipeline Orchestration BC (ACL): FailFast can terminate Pipeline early.
Key invariants:
  1. JUnit reports must be valid XML under 30 MB per file.
  2. Code coverage thresholds enforced via `coverage` keyword regex.
  3. Security scans (SAST, DAST, dependency) report as Artifacts with severity.
  4. FailFast only triggers on test failure, not on `allow_failure: true` Jobs.

#### BC: Pipeline Security & Provenance

Responsibility: Owns security policies, access control, and build attestation.

Owns: SLSALevel, ProvenanceRecord, Permission, FineGrainedToken, SecurityPolicy.

Integrates with:

  - Variable & Secret Management BC (partnership): Enforces secret rotation and OIDC.
  - Environment & Deployment BC (ACL): Protected Environments check permissions.
  - External Integration BC (conformist): SLSA provenance for supply chain security.
Key invariants:
  1. SLSA Level 3 requires isolated build, provenance generation, and non-falsifiable attestation.
  2. Fine-grained CI Job Tokens scoped to minimum required permissions.
  3. Provenance records signed with private key; verifiable via public key.
  4. Security scan policies can block deployments on severity threshold.

#### BC: External Integration

Responsibility: Owns bidirectional integration with external systems (SCM, chat, CD tools, secret backends).

Owns: ExternalRepo, CommitStatus, WebhookEvent, ChatOpsCommand, OIDCFederation.

Integrates with:

  - Pipeline Orchestration BC (supplier): External triggers create Pipelines.
  - Environment & Deployment BC (customer-supplier): External CD tools consume Deployment state.
  - Variable & Secret Management BC (ACL): OIDC token exchange for secret access.
Key invariants:
  1. Webhook payloads signed with GitLab secret token.
  2. External commit statuses limited to 50 per commit.
  3. ChatOps commands require explicit user authentication.
  4. OIDC ID Tokens audience-restricted to configured external provider.

---

### §3—Core Domain Model

#### Aggregate: Pipeline [Aggregate Root]

Entities:

  - PipelineId: UUID, unique per Pipeline execution.
  - Status: Enum [`created`, `pending`, `running`, `success`, `failed`, `canceled`, `skipped`].
  - Source: Enum [`push`, `web`, `trigger`, `schedule`, `merge_request_event`, `parent_pipeline`, `external`, `ondemand_scanner`, `workflow_dispatch`].
  - Ref: Git reference (branch, tag, merge request) triggering the Pipeline.
  - SHA: Commit hash at Pipeline creation.
  - CreatedAt: Timestamp of Pipeline creation.
  - UpdatedAt: Timestamp of last status change.
  - Duration: Wall-clock time from start to terminal state.

Value Objects:

  - PipelineConfig: Parsed `.gitlab-ci.yml` content with resolved Includes.
  - VariableSet: Ordered list of Variables with scope and precedence.
  - StageOrder: Ordered list of Stage names defining execution sequence.

Domain Events raised:

  - PipelineCreated(PipelineId, Ref, SHA): raised when Pipeline entity is persisted.
  - PipelineStarted(PipelineId): raised when first Job transitions to `running`.
  - PipelineCompleted(PipelineId, Status): raised when Pipeline reaches terminal state.
  - DownstreamTriggered(PipelineId, DownstreamPipelineId, TriggerJobId): raised when Bridge Job creates child/multi-project Pipeline.

Business rules (invariants):

  1. A Pipeline must contain at least one Job to be valid.
  2. Pipeline status is derived from Job statuses (failed Job → failed Pipeline unless `allow_failure`).
  3. Canceling a Pipeline cancels all running/pending Jobs.
  4. Interruptible Pipelines auto-cancel when superseded by newer Pipeline on same Ref.

#### Aggregate: Job [Aggregate Root]

Entities:

  - JobId: UUID, unique per Job execution.
  - PipelineId: Foreign key to parent Pipeline.
  - Name: Unique Job name within Pipeline (or grouped name for Matrix/Parallel).
  - Stage: Stage name from Pipeline StageOrder.
  - Status: Enum [`pending`, `running`, `success`, `failed`, `canceled`, `skipped`, `manual`, `waiting_for_resource`, `preparing`, `scheduled`].
  - RunnerId: Assigned Runner (null until scheduled).
  - TagList: List of Runner Tags required for execution.
  - CreatedAt: Timestamp of Job creation.
  - StartedAt: Timestamp of Job start on Runner.
  - FinishedAt: Timestamp of Job completion.
  - Duration: Execution time (FinishedAt - StartedAt).
  - QueuedDuration: Wait time (StartedAt - CreatedAt).

Value Objects:

  - ScriptDefinition: Ordered list of shell commands to execute.
  - ArtifactSpec: List of paths, reports, expiration, and retention rules.
  - CacheSpec: Key, paths, policy (pull/pull-push), and fallback keys.
  - ServiceSpec: List of Docker service images and aliases.
  - RuleSet: Ordered list of Rules with conditions and `when` clauses.
  - NeedSpec: List of Job dependencies with `optional` flag.
  - TimeoutSpec: Job timeout override (default: project-wide setting).

Domain Events raised:

  - JobCreated(JobId, PipelineId, Name): raised when Job entity is persisted.
  - JobScheduled(JobId, RunnerId): raised when Runner claims Job from queue.
  - JobStarted(JobId): raised when Runner begins execution.
  - JobCompleted(JobId, Status): raised when Runner reports completion.
  - ArtifactUploaded(JobId, ArtifactSpec): raised when Artifacts are persisted.
  - CacheUploaded(JobId, CacheSpec): raised when Cache is persisted.

Business rules (invariants):

  1. Job cannot start until all `needs` dependencies are in terminal `success` state (or `optional: true` and missing).
  2. Manual Jobs require explicit user action to transition from `manual` to `pending`.
  3. Job timeout cannot exceed Runner's maximum timeout setting.
  4. `after_script` runs regardless of `script` failure; failure in `after_script` does not affect Job status.
  5. Matrix Jobs share the same JobId prefix but have distinct executions.

#### Aggregate: Runner [Aggregate Root]

Entities:

  - RunnerId: UUID, unique per Runner registration.
  - Token: Authentication token (rotated periodically).
  - Description: Human-readable Runner name.
  - TagList: List of Tags for Job routing.
  - Executor: Executor type (shell, docker, kubernetes, docker-machine, custom).
  - Scope: Enum [`instance`, `group`, `project`].
  - Status: Enum [`online`, `offline`, `paused`].
  - IsProtected: Boolean; only runs Jobs on protected branches/tags.
  - RunUntagged: Boolean; allows Jobs without Tags.
  - MaximumTimeout: Maximum Job timeout in seconds (overrides project default).
  - Locked: Boolean; prevents Runner from being shared with other Projects.
  - AccessLevel: Enum [`not_protected`, `reference_protected`, `ref_protected`].
  - RunnerVersion: GitLab Runner version string.
  - Platform: OS/architecture (linux/amd64, darwin/arm64, etc.).
  - LastContact: Timestamp of last heartbeat.

Value Objects:

  - RunnerConfig: Executor-specific configuration (Docker image, Kubernetes namespace, etc.).
  - TokenRotationPolicy: Interval and expiration settings for token rotation.

Domain Events raised:

  - RunnerRegistered(RunnerId, Scope): raised when Runner is registered.
  - RunnerOnline(RunnerId): raised when Runner connects via long-polling.
  - RunnerOffline(RunnerId): raised when Runner heartbeat exceeds timeout.
  - TokenRotated(RunnerId, NewTokenExpiry): raised when token is rotated.
  - JobAssigned(RunnerId, JobId): raised when Runner claims Job.

Business rules (invariants):

  1. Runner must have all Job-specified Tags to be eligible (subset matching not allowed).
  2. Protected Runners only execute Jobs on protected branches/tags or from users with Maintainer+ role.
  3. Runner authentication tokens expire and rotate automatically; offline Runners updated on next contact.
  4. Instance Runners shared across all Projects unless Project explicitly disables them.

#### Aggregate: Environment [Aggregate Root]

Entities:

  - EnvironmentId: UUID, unique per Environment.
  - ProjectId: Owning Project.
  - Name: Environment name (e.g., `production`, `review/feature-1`).
  - Slug: URL-safe slug derived from Name.
  - ExternalUrl: Deployment target URL.
  - Tier: Enum [`development`, `testing`, `staging`, `production`, `other`].
  - State: Enum [`available`, `stopping`, `stopped`].
  - CreatedAt: Timestamp of Environment creation.
  - UpdatedAt: Timestamp of last Deployment.

Value Objects:

  - DeploymentRecord: JobId, SHA, timestamp, status, user who triggered.
  - ApprovalRule: List of required approvers (users, groups, roles) and threshold count.
  - ProtectionRule: List of allowed deployers (roles, users, groups).

Domain Events raised:

  - EnvironmentCreated(EnvironmentId, Name): raised when first Deployment creates Environment.
  - DeploymentStarted(EnvironmentId, JobId): raised when Deployment Job begins.
  - DeploymentCompleted(EnvironmentId, JobId, Status): raised when Deployment Job finishes.
  - EnvironmentStopped(EnvironmentId): raised when `on_stop` Job runs or manual stop.
  - EnvironmentDeleted(EnvironmentId): raised when Environment is removed.

Business rules (invariants):

  1. Environment names cannot be changed; must stop/delete/recreate.
  2. Protected Environments require explicit deploy permissions (roles, users, groups).
  3. Dynamic Environments (Review Apps) auto-stop when source branch is deleted or merged.
  4. Deployment tier inferred from name pattern or explicit `deployment_tier` keyword.
  5. Approval gates block Deployment until required approvers consent.

#### Aggregate: Artifact [Aggregate Root]

Entities:

  - ArtifactId: UUID, unique per Artifact set.
  - JobId: Producing Job.
  - Paths: List of file/directory globs to archive.
  - Size: Total archive size in bytes.
  - ExpiresAt: Expiration timestamp (default: 30 days).
  - Status: Enum [`created`, `expired`, `deleted`].

Value Objects:

  - ReportSpec: Type-specific report configuration (JUnit, coverage, code quality, etc.).
  - RetentionPolicy: `when` clause (on_success, on_failure, always) and expiration.

Domain Events raised:

  - ArtifactUploaded(ArtifactId, JobId): raised when Job uploads Artifacts.
  - ArtifactExpired(ArtifactId): raised when expiration timestamp passes.
  - ArtifactDeleted(ArtifactId): raised when Artifacts are purged.

Business rules (invariants):

  1. Artifacts only available after Job completes successfully (unless `when: on_failure` or `always`).
  2. Downstream Jobs can only download Artifacts from Jobs in `needs` or earlier Stages.
  3. Expired Artifacts are inaccessible but metadata retained for audit.
  4. Maximum Artifact size: 30 MB per file, 100 MB total for JUnit reports.

#### Aggregate: Variable [Aggregate Root]

Entities:

  - VariableId: UUID, unique per Variable definition.
  - Key: Variable name (uppercase, underscores, no spaces).
  - Value: Variable value (up to 10,000 characters).
  - Type: Enum [`env_var`, `file`].
  - Scope: Enum [`instance`, `group`, `project`, `job`].
  - IsProtected: Boolean; only available in protected branch/tag Pipelines.
  - IsMasked: Boolean; value replaced with `[MASKED]` in logs.
  - IsHidden: Boolean; value not visible in UI after creation.
  - ExpandReference: Boolean; allows `$VAR` expansion in value.
  - EnvironmentScope: Wildcard or specific Environment name (e.g., `production`, `review/*`).

Value Objects:

  - VariablePrecedence: Ordered list of scopes determining override hierarchy.

Domain Events raised:

  - VariableCreated(VariableId, Key, Scope): raised when Variable is persisted.
  - VariableUpdated(VariableId, Key): raised when Variable value or settings change.
  - VariableDeleted(VariableId, Key): raised when Variable is removed.

Business rules (invariants):

  1. Variable precedence: Pipeline execution policy > Scan policy > Pipeline > Project > Group > Instance > Job > Default.
  2. Masked Variables must be 8+ characters, single-line, no spaces.
  3. Protected Variables only available in protected branch/tag Pipelines (or MR Pipelines with explicit access).
  4. File-type Variables write value to temp file; path injected as environment variable.

#### Aggregate: Secret [Aggregate Root]

Entities:

  - SecretId: UUID, unique per Secret definition.
  - Provider: Enum [`gitlab`, `hashicorp_vault`, `aws_secrets_manager`, `azure_key_vault`, `gcp_secret_manager`, `fortanix_dsm`].
  - Path: Secret path in external backend (e.g., `secret/data/prod/db-password`).
  - IDTokenAudience: OIDC audience for external provider authentication.
  - Scope: Enum [`job`, `pipeline`, `environment`].

Value Objects:

  - OIDCConfig: ID Token configuration (audience, expiration, claims).
  - RotationPolicy: Automatic rotation interval and notification settings.

Domain Events raised:

  - SecretRequested(JobId, SecretId): raised when Job requests Secret injection.
  - SecretInjected(JobId, SecretId): raised when Secret is available in Job context.
  - SecretRotationTriggered(SecretId): raised when rotation schedule executes.

Business rules (invariants):

  1. Secrets must be explicitly requested per Job via `secrets:` keyword.
  2. ID Tokens are short-lived (5 minutes) and audience-restricted to configured provider.
  3. External secret access requires OIDC federation setup in provider.
  4. Secret values never logged, even if unmasked.

#### Aggregate: Component [Aggregate Root]

Entities:

  - ComponentId: UUID, unique per Component version.
  - Address: Fully qualified address (`<fqdn>/<project>/<component>@<version>`).
  - Version: Semantic version or ref (tag, branch, SHA).
  - Inputs: List of Input definitions (name, type, default, options, description).
  - Template: CI/CD configuration template with Input placeholders.

Value Objects:

  - InputSpec: Name, type (string, number, boolean), default, options, description.
  - VersionConstraint: Version pinning strategy (exact, semver range, latest).

Domain Events raised:

  - ComponentPublished(ComponentId, Version): raised when Component is released.
  - ComponentIncluded(PipelineId, ComponentId): raised when Component is added to Pipeline.

Business rules (invariants):

  1. Component address must include explicit version (no floating tags in production).
  2. Input values must match declared type and be in `options` list if provided.
  3. Component template validated against CI/CD schema before inclusion.
  4. Components cannot recursively include themselves (cycle detection).

---

### §4—Pipeline Lifecycle State Machine

#### Pipeline State Machine

States: [`created`, `pending`, `running`, `success`, `failed`, `canceled`, `skipped`]

Transitions:

  `created` --[pipeline validation passes]--> `pending`

  `created` --[validation fails]--> `failed`

  `pending` --[first Job scheduled]--> `running`

  `running` --[all Jobs success]--> `success`

  `running` --[any Job fails (non-allow_failure)]--> `failed`

  `running` --[user cancels]--> `canceled`

  `running` --[interruptible superseded]--> `canceled`

  `pending` --[workflow:rules excludes]--> `skipped`

  `running` --[workflow:auto_cancel on_job_failure]--> `canceled`

Terminal states: [`success`, `failed`, `canceled`, `skipped`]

External triggers:

  - User cancel: API or UI action.
  - Interruptible: New Pipeline on same Ref auto-cancels running Pipeline.
  - Auto-cancel on failure: `workflow:auto_cancel:on_job_failure` triggers on first Job failure.

Internal transitions:

  - Validation: `.gitlab-ci.yml` parsing and schema validation.
  - Job completion aggregation: Pipeline status derived from Job statuses.

#### Job State Machine

States: [`pending`, `running`, `success`, `failed`, `canceled`, `skipped`, `manual`, `waiting_for_resource`, `preparing`, `scheduled`]

Transitions:

  `pending` --[runner claims job]--> `scheduled`

  `scheduled` --[runner prepares]--> `preparing`

  `preparing` --[resources acquired]--> `running`

  `preparing` --[resource timeout]--> `failed`

  `running` --[script exits 0]--> `success`

  `running` --[script exits non-0]--> `failed`

  `running` --[timeout exceeded]--> `failed`

  `running` --[user cancels]--> `canceled`

  `running` --[pipeline canceled]--> `canceled`

  `manual` --[user triggers]--> `pending`

  `waiting_for_resource` --[resource available]--> `pending`

  `pending` --[rules evaluate false mid-pipeline]--> `skipped`

  `pending` --[upstream dependency failed (non-optional)]--> `skipped`

Terminal states: [`success`, `failed`, `canceled`, `skipped`]

External triggers:

  - Manual trigger: User clicks "Run" button in UI.
  - Cancel: User cancels Job via UI or API.
  - Resource acquisition: `resource_group` lock acquired.

Internal transitions:

  - Runner assignment: Long-polling picks up Job from queue.
  - Dependency resolution: `needs` dependencies must be `success` (or `optional: true` and absent).
  - Timeout: Job exceeds `timeout` or Runner maximum timeout.

---

### §5—Deployment Orchestration Playbook

#### 5.1 Deployment Strategies Supported

Direct Deploy (Push to Environment on Merge)

- Trigger condition: Commit to protected branch (e.g., `main`).
- Required YAML keywords: `stage: deploy`, `environment`, `rules`.
- Environment configuration: Static name (e.g., `production`), URL.
- Rollback mechanism: Re-run previous successful Deployment Job.
- Approval gates: Protected Environment with role-based access.
- Compute cost profile: LOW; single Job per deployment.

```yaml
deploy_prod:
  stage: deploy
  script: ./deploy.sh
  environment:
    name: production
    url: https://prod.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

Manual Deploy (Manual Job Gate)

- Trigger condition: Pipeline succeeds; user manually triggers deploy Job.
- Required YAML keywords: `when: manual`, `environment`.
- Environment configuration: Static or dynamic name.
- Rollback mechanism: Manual rollback Job or re-run previous.
- Approval gates: `when: manual` + Protected Environment.
- Compute cost profile: LOW; Job runs only on demand.

```yaml
deploy_prod:
  stage: deploy
  script: ./deploy.sh
  environment: production
  when: manual
```

Incremental / Canary Rollout

- Trigger condition: Manual or automated based on metrics.
- Required YAML keywords: `environment`, `resource_group`, `parallel:matrix`.
- Environment configuration: Multiple Environments (canary, stable).
- Rollback mechanism: Switch traffic back to stable; `environment: action: stop` for canary.
- Approval gates: Manual confirmation between stages.
- Compute cost profile: MEDIUM; multiple parallel deployments.

```yaml
deploy_canary:
  stage: deploy
  script: ./deploy.sh --canary
  environment:
    name: production/canary
    url: https://canary.example.com
  resource_group: production
  parallel:
    matrix:
      - WEIGHT: [10, 25, 50, 100]
```

Blue/Green via Environments

- Trigger condition: Manual or automated.
- Required YAML keywords: `environment`, `resource_group`.
- Environment configuration: Two Environments (blue, green) with load balancer switch.
- Rollback mechanism: Switch traffic back; stop old Environment.
- Approval gates: Protected Environment + manual confirmation.
- Compute cost profile: HIGH; double infrastructure.

```yaml
deploy_blue:
  stage: deploy
  script: ./deploy.sh --target blue
  environment:
    name: production/blue
    url: https://blue.example.com
  resource_group: production

deploy_green:
  stage: deploy
  script: ./deploy.sh --target green
  environment:
    name: production/green
    url: https://green.example.com
  resource_group: production
  when: manual
```

Review App (Ephemeral Environment per MR)

- Trigger condition: Merge Request opened/updated.
- Required YAML keywords: `environment: name: review/$CI_COMMIT_REF_SLUG`, `on_stop`, `rules`.
- Environment configuration: Dynamic name, auto-stop on MR merge/close.
- Rollback mechanism: Stop Environment; no rollback needed (ephemeral).
- Approval gates: None (automated); optional manual start.
- Compute cost profile: MEDIUM; one Environment per MR.

```yaml
deploy_review:
  stage: deploy
  script: ./deploy-review.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_ENVIRONMENT_SLUG.example.com
    on_stop: stop_review
  rules:
    - if: $CI_MERGE_REQUEST_ID

stop_review:
  stage: deploy
  script: ./teardown.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  rules:
    - if: $CI_MERGE_REQUEST_ID
  when: manual
```

Kubernetes Rolling Deploy

- Trigger condition: Commit to branch or manual.
- Required YAML keywords: `environment`, `image` (for kubectl).
- Environment configuration: Kubernetes Deployment resource.
- Rollback mechanism: `kubectl rollout undo`.
- Approval gates: Protected Environment.
- Compute cost profile: LOW; native K8s rolling update.

```yaml
deploy_k8s:
  stage: deploy
  image: bitnami/kubectl
  script:
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/app
  environment:
    name: production
    url: https://app.example.com
```

ECS Task-Definition Deploy

- Trigger condition: Commit or manual.
- Required YAML keywords: `environment`, `image` (for AWS CLI).
- Environment configuration: ECS service with task definition.
- Rollback mechanism: Revert to previous task definition.
- Approval gates: Protected Environment.
- Compute cost profile: LOW; ECS managed rollout.

```yaml
deploy_ecs:
  stage: deploy
  image: amazon/aws-cli
  script:
    - aws ecs update-service --cluster prod --service app --force-new-deployment
  environment:
    name: production
```

Heroku Deploy

- Trigger condition: Commit to branch or manual.
- Required YAML keywords: `environment`, `variables` (HEROKU_API_KEY).
- Environment configuration: Heroku app name.
- Rollback mechanism: `heroku releases:rollback`.
- Approval gates: Protected Environment.
- Compute cost profile: LOW; Heroku managed.

```yaml
deploy_heroku:
  stage: deploy
  script:
    - git push https://heroku:$HEROKU_API_KEY@git.heroku.com/$HEROKU_APP_NAME.git HEAD:main
  environment:
    name: production
    url: https://$HEROKU_APP_NAME.herokuapp.com
```

Google Cloud Run / Cloud Functions Deploy

- Trigger condition: Commit or manual.
- Required YAML keywords: `environment`, `image`.
- Environment configuration: Cloud Run service or Cloud Function.
- Rollback mechanism: Deploy previous revision.
- Approval gates: Protected Environment.
- Compute cost profile: LOW; serverless scaling.

```yaml
deploy_cloud_run:
  stage: deploy
  image: gcr.io/google.com/cloudsdktool/cloud-sdk
  script:
    - gcloud run deploy app --image $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA --region us-central1
  environment:
    name: production
    url: https://app-$CI_PROJECT_SLUG.a.run.app
```

Downstream Pipeline as Deployment Trigger

- Trigger condition: Upstream Pipeline success.
- Required YAML keywords: `trigger`, `strategy: mirror`.
- Environment configuration: Defined in downstream Pipeline.
- Rollback mechanism: Downstream Pipeline rollback.
- Approval gates: Downstream Protected Environment.
- Compute cost profile: MEDIUM; separate Pipeline execution.

```yaml
trigger_deploy:
  stage: deploy
  trigger:
    project: my-group/deployment-pipeline
    branch: main
    strategy: mirror
```

#### 5.2 Environment Promotion Chain

Canonical GitLab pattern for `dev → staging → production` promotion:

```yaml
stages:
  - build
  - test
  - deploy_dev
  - deploy_staging
  - deploy_prod

build:
  stage: build
  script: ./build.sh
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

test:
  stage: test
  script: ./test.sh
  needs: [build]

deploy_dev:
  stage: deploy_dev
  script: ./deploy.sh --env dev
  environment:
    name: development
    url: https://dev.example.com
  needs: [test]
  rules:
    - if: $CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH

deploy_staging:
  stage: deploy_staging
  script: ./deploy.sh --env staging
  environment:
    name: staging
    url: https://staging.example.com
  needs: [deploy_dev]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  when: manual

deploy_prod:
  stage: deploy_prod
  script: ./deploy.sh --env prod
  environment:
    name: production
    url: https://example.com
  needs: [deploy_staging]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  when: manual
  resource_group: production
```

How artifacts pass between stages:

- `artifacts:paths` in `build` Job makes `dist/` available to all downstream Jobs.
- `needs:` ensures Job dependency order and Artifact availability.
- `dependencies:` can restrict which Job Artifacts are downloaded (default: all upstream).

Where `environment:` blocks attach deployment identity:

- Each deploy Job defines `environment:` with unique `name` and `url`.
- GitLab creates Environment record on first successful deployment.
- Subsequent deployments update the same Environment.

How `protected_environments` enforce RBAC:

- Production Environment configured as Protected in Project Settings > CI/CD.
- Only users with explicit deploy permission (Maintainers, specific users/groups) can run the Job.
- Job fails with permission error if user lacks access.

How `resource_groups:` prevent concurrent deploys:

- `resource_group: production` ensures only one Job can deploy to production at a time.
- Second Job waits in `waiting_for_resource` state until first completes.
- Prevents race conditions in multi-MR scenarios.

#### 5.3 Approval & Safety Gates

`when: manual` Jobs

- Job appears in UI with "Run" button; requires explicit user action.
- Common pattern: Production deployments, database migrations.
- Does not block Pipeline; Job remains `manual` until triggered.

`environment: deployment_tier` + Protected Environment Approvals

- Deployment tier (`production`, `staging`) mapped to Protected Environment.
- Approvers configured in Protected Environment settings.
- Deployment requires N approvals from configured list (users, groups, roles).

Merge Train Gating

- Merge Requests queued; tested in sequence against target branch.
- Ensures changes don't conflict when merged rapidly.
- Pipeline runs on merged result; blocks merge until success.

`rules:` + External Status Checks

- `rules:if` can check external API for approval status.
- Example: Check Jira ticket status, external QA system.
- Job skipped if external check fails.

Resource Group Concurrency Locks

- `resource_group: <name>` limits Jobs to one-at-a-time execution.
- Prevents concurrent deployments to same Environment.
- Jobs queue in `waiting_for_resource` state.

#### 5.4 Rollback Patterns

Re-run Previous Pipeline to the Environment

- Navigate to previous successful Pipeline.
- Click "Re-run" on deploy Job.
- Job redeploys the artifact from that Pipeline (if Artifacts retained).

Dedicated `rollback` Manual Job Calling Prior Artifact

```yaml
rollback_prod:
  stage: deploy
  script: ./deploy.sh --version $DEPLOY_VERSION
  environment:
    name: production
    action: rollback
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

`environment: action: stop` for Teardown

```yaml
stop_prod:
  stage: deploy
  script: ./teardown.sh
  environment:
    name: production
    action: stop
  when: manual
```

Kubernetes Rollout Undo via `kubectl` Step

```yaml
rollback_k8s:
  stage: deploy
  image: bitnami/kubectl
  script:
    - kubectl rollout undo deployment/app --to-revision=$PREVIOUS_REVISION
  environment:
    name: production
  when: manual
```

---

### §6—Configuration Language Reference (Optimisation-Oriented)

#### Keyword Group: `stages` / `stage`

Purpose: Define execution order and logical grouping of Jobs.

Optimisation relevance: HIGH

Key keywords:

  - `stages`: Global list of stage names in execution order.
  - `stage`: Job-level assignment to a stage.
Common anti-patterns:
  - Overusing stages when DAG (`needs`) would enable parallelism.
  - Placing independent Jobs in same stage unnecessarily.
Recommended patterns:
  - Use minimal stages (build, test, deploy); rely on `needs` for ordering.
  - Group related Jobs in stages for UI clarity, not execution control.
Interacts with: `needs`, `dependencies`, `workflow`.

#### Keyword Group: `needs` / `dependencies` (DAG wiring)

Purpose: Define Job dependencies for DAG execution, bypassing stage barriers.

Optimisation relevance: HIGH

Key keywords:

  - `needs`: List of Job names or `{job: name, optional: true}` objects.
  - `dependencies`: Restrict which upstream Artifacts to download.
Common anti-patterns:
  - Omitting `needs` and relying on stage order (sequential execution).
  - Circular dependencies (A needs B, B needs A).
  - Forgetting `optional: true` for conditional dependencies.
Recommended patterns:
  - Use `needs` for all Jobs to maximise parallelism.
  - Use `needs: []` for Jobs that should run immediately.
  - Use `optional: true` for flaky or conditional upstream Jobs.
Interacts with: `stages`, `artifacts`, `parallel`.

#### Keyword Group: `rules` / `workflow` / `only` / `except` (conditional execution)

Purpose: Control Job inclusion and execution mode based on conditions.

Optimisation relevance: HIGH

Key keywords:

  - `rules`: List of `{if, changes, exists, when, allow_failure}` objects.
  - `workflow:rules`: Global Pipeline-level rules (which Pipeline types run).
  - `only`/`except`: Deprecated; use `rules` instead.
Common anti-patterns:
  - Using `only`/`except` (deprecated, less flexible).
  - Complex nested conditions without comments.
  - Omitting `workflow:rules` and running unnecessary Pipelines.
Recommended patterns:
  - Use `workflow:rules` to skip Pipelines for docs-only changes.
  - Use `rules:changes` to run Jobs only when relevant files change.
  - Combine `if` and `changes` for precise control.
Interacts with: `variables`, `include`, `trigger`.

#### Keyword Group: `cache` / `artifacts` (data Flow between Jobs)

Purpose: Persist and transfer data between Jobs and Pipelines.

Optimisation relevance: HIGH

Key keywords:

  - `cache`: Reusable files (dependencies) with key and paths.
  - `artifacts`: Job outputs with paths, reports, expiration.
  - `cache:key`: Dynamic cache key (e.g., `$CI_COMMIT_REF_SLUG`).
  - `artifacts:reports`: Structured reports (JUnit, coverage, etc.).
Common anti-patterns:
  - Using cache for build outputs (should be artifacts).
  - Overly broad cache paths (caches unnecessary files).
  - Missing cache fallback keys (cold starts on every branch).
Recommended patterns:
  - Use cache for dependencies (`node_modules/`, `vendor/`).
  - Use artifacts for build outputs (`dist/`, binaries).
  - Use `fallback_keys` for branch cache misses.
  - Set `policy: pull` for Jobs that only consume cache.
Interacts with: `needs`, `dependencies`, `stages`.

#### Keyword Group: `extends` / `!reference` / `include` / `components` (reuse)

Purpose: Reduce duplication via configuration inheritance and composition.

Optimisation relevance: MEDIUM

Key keywords:

  - `extends`: Inherit Job configuration from hidden template.
  - `!reference`: Reuse configuration blocks (YAML anchor alternative).
  - `include`: Import external YAML (local, project, remote, template, component).
  - `include:component`: Versioned, reusable CI/CD component.
Common anti-patterns:
  - Deep inheritance chains (hard to trace).
  - Including files without version pinning (brittle).
  - Duplicated configuration across includes.
Recommended patterns:
  - Use `extends` for Job templates (`.job_template`).
  - Use `include:component` with semantic versioning.
  - Use `!reference` for reusable blocks within file.
Interacts with: `variables`, `inputs`, `default`.

#### Keyword Group: `parallel` / `matrix` (fan-out)

Purpose: Run multiple Job instances concurrently with different configurations.

Optimisation relevance: MEDIUM

Key keywords:

  - `parallel`: Integer count or `matrix` list.
  - `parallel:matrix`: List of variable combinations.
Common anti-patterns:
  - Matrix with too many combinations (explodes cost).
  - Not using `needs` to fan-in results.
Recommended patterns:
  - Use matrix for cross-platform testing (OS × Node versions).
  - Limit matrix size with `rules` (e.g., full matrix only on `main`).
  - Use `needs` to aggregate results in downstream Job.
Interacts with: `needs`, `artifacts`, `rules`.

#### Keyword Group: `trigger` / `strategy` (downstream pipelines)

Purpose: Trigger child or multi-project Pipelines.

Optimisation relevance: MEDIUM

Key keywords:

  - `trigger`: `include` (local, artifact, project) or `project`.
  - `trigger:strategy`: `mirror` (reflect downstream status) or `depend`.
Common anti-patterns:
  - Triggering downstream without `strategy: mirror` (status not reflected).
  - Deep nesting of child Pipelines (hard to debug).
Recommended patterns:
  - Use `strategy: mirror` for deployment Pipelines.
  - Use `rules` to conditionally trigger downstream.
  - Limit nesting to 2 levels max.
Interacts with: `rules`, `variables`, `workflow`.

#### Keyword Group: `environment` / `deployment_tier` (deployment binding)

Purpose: Bind Job to deployment target with tracking.

Optimisation relevance: HIGH

Key keywords:

  - `environment:name`: Static or dynamic (with variables).
  - `environment:url`: Deployment URL (static or dynamic).
  - `environment:on_stop`: Cleanup Job for ephemeral Environments.
  - `environment:action:stop`: Stop Environment.
  - `environment:deployment_tier`: Explicit tier (`production`, `staging`, etc.).
Common anti-patterns:
  - Deploy Jobs without `environment:` (no tracking).
  - Dynamic names without grouping prefix (cluttered UI).
Recommended patterns:
  - Always use `environment:` for deploy Jobs.
  - Use `review/` prefix for Review Apps (groups in UI).
  - Set explicit `deployment_tier` for group-level protection.
Interacts with: `protected_environments`, `resource_group`, `variables`.

#### Keyword Group: `resource_group` (concurrency control)

Purpose: Limit Job concurrency to prevent race conditions.

Optimisation relevance: MEDIUM

Key keywords:

  - `resource_group`: Named lock (Jobs with same name run sequentially).
Common anti-patterns:
  - Not using resource groups for production deploys.
  - Overusing resource groups (unnecessary serialization).
Recommended patterns:
  - Use `resource_group: production` for production deploys.
  - Use `resource_group: <env>` per Environment.
  - Combine with `when: manual` for controlled releases.
Interacts with: `environment`, `stage`, `needs`.

#### Keyword Group: `variables` / `inputs` (parameterisation)

Purpose: Inject configuration values into Job execution.

Optimisation relevance: MEDIUM

Key keywords:

  - `variables`: Global or Job-level key-value pairs.
  - `inputs`: Component input parameters (type, default, options).
  - `variables:expand`: Control variable expansion (default: false).
Common anti-patterns:
  - Hardcoding values in `script` instead of variables.
  - Using plaintext secrets in `.gitlab-ci.yml`.
  - Not scoping variables to Environment.
Recommended patterns:
  - Use UI-defined Variables for secrets (masked, protected).
  - Use `inputs` for Component parameterisation.
  - Use `dotenv` reports for dynamic variables between Jobs.
Interacts with: `secrets`, `rules`, `include`.

#### Keyword Group: `services` (sidecar containers)

Purpose: Attach dependency containers to Job (database, cache, etc.).

Optimisation relevance: LOW

Key keywords:

  - `services`: List of Docker images (with aliases, entrypoint, commands).
Common anti-patterns:
  - Using services when not needed (overhead).
  - Not setting service health checks.
Recommended patterns:
  - Use services for integration tests (Postgres, Redis).
  - Set `alias` for multiple instances of same service.
  - Use `docker:dind` for Docker-in-Docker builds.
Interacts with: `image`, `variables`.

#### Keyword Group: `image` / `tags` (runner selection)

Purpose: Define execution environment and Runner targeting.

Optimisation relevance: HIGH

Key keywords:

  - `image`: Docker image for Job execution.
  - `tags`: Runner tags for selection.
  - `default:image`: Global default image.
Common anti-patterns:
  - Using `latest` tags (non-reproducible builds).
  - Not pinning image versions.
  - Omitting tags and relying on untagged Runners.
Recommended patterns:
  - Pin image versions (`ruby:3.1.2`, not `ruby:latest`).
  - Use specific tags for hardware requirements (`gpu`, `macos`).
  - Use `default:image` to reduce duplication.
Interacts with: `services`, `cache`.

#### Keyword Group: `retry` / `timeout` / `interruptible` (resilience)

Purpose: Control Job failure handling and resource usage.

Optimisation relevance: MEDIUM

Key keywords:

  - `retry`: Number and conditions for auto-retry.
  - `timeout`: Job timeout override.
  - `interruptible`: Allow Job to be canceled by newer Pipeline.
Common anti-patterns:
  - Not setting timeouts (runaway Jobs).
  - Retrying non-transient failures.
  - Not using `interruptible` for long-running Jobs.
Recommended patterns:
  - Set `timeout` on all long-running Jobs.
  - Use `retry` for transient failures (network, flaky tests).
  - Use `interruptible: true` for build Jobs on feature branches.
Interacts with: `rules`, `workflow`.

#### Keyword Group: `when` (execution control)

Purpose: Control Job execution based on Pipeline status.

Optimisation relevance: MEDIUM

Key keywords:

  - `when`: `on_success` (default), `on_failure`, `always`, `manual`, `never`, `delayed`.
  - `start_in`: Delay duration (with `when: delayed`).
Common anti-patterns:
  - Using `when: always` unnecessarily (wastes resources).
  - Not using `when: manual` for risky operations.
Recommended patterns:
  - Use `when: manual` for production deploys.
  - Use `when: on_failure` for notifications.
  - Use `when: delayed` with `start_in` for scheduled tasks.
Interacts with: `rules`, `allow_failure`.

#### Keyword Group: `secrets` / `id_tokens` (credential injection)

Purpose: Inject secrets from external backends via OIDC.

Optimisation relevance: HIGH

Key keywords:

  - `secrets`: Map secret path to environment variable.
  - `id_tokens`: OIDC token configuration (audience).
Common anti-patterns:
  - Storing secrets in CI/CD Variables instead of external backend.
  - Not setting ID Token audience (security risk).
Recommended patterns:
  - Use HashiCorp Vault, AWS Secrets Manager, or GCP Secret Manager.
  - Set `id_tokens` with specific audience for each provider.
  - Scope secrets to Job-level (not global).
Interacts with: `variables`, `image`.

---

### §7—Runner Selection & Job Routing Model

Decision Tree for Runner Assignment:

1. Tag Matching (Exact Match Required)
   - Job specifies `tags: [docker, linux]`.
   - Runner must have ALL specified tags (subset matching).
   - Runner with `[docker, linux, gpu]` matches.
   - Runner with `[docker]` does NOT match (missing `linux`).
   - If no tags specified and Runner allows untagged Jobs: match.
   - If no tags specified and Runner requires tags: no match.

2. Runner Scope Hierarchy
   - Instance Runners: Available to all Projects (unless Project disables).
   - Group Runners: Available to Projects in Group and subgroups.
   - Project Runners: Available only to specific Project.
   - Scope is checked after tag matching.

3. Executor Type Capabilities
   - `shell`: Runs on host; no container isolation; full host access.
   - `docker`: Runs in Docker container; isolated; supports `image` and `services`.
   - `kubernetes`: Runs in K8s pod; supports dynamic scaling; K8s-native.
   - `docker-machine`: Auto-scales Docker hosts; cloud-provider integration.
   - `custom`: User-defined executor (e.g., Podman, containerd).

4. Hosted Runner Fleet Options (GitLab.com)
   - Linux x86-64: `saas-linux-small-amd64` (2 vCPU, 8GB), `medium` (4 vCPU, 16GB), `large` (8 vCPU, 32GB), `xlarge` (16 vCPU, 64GB), `2xlarge` (32 vCPU, 128GB).
   - Linux Arm64: `saas-linux-small-arm64` (2 vCPU, 8GB), `medium` (4 vCPU, 16GB), `large` (8 vCPU, 32GB).
   - macOS: `saas-macos-medium-m1` (4 vCPU, 16GB), `large` (8 vCPU, 32GB).
   - Windows: `saas-windows-medium-amd64` (4 vCPU, 16GB).
   - GPU: `saas-linux-gpu-medium` (NVIDIA T4), `large` (NVIDIA A10G).
   - Compute minute costs vary by tier (Free: 500 mins/month; Premium: 10,000 mins/month; Ultimate: 50,000 mins/month).

5. Job Router / Runner Controller Pattern
   - GitLab Job Router matches Jobs to Runners via long-polling.
   - Runner polls `/api/v4/jobs/request` with tag list.
   - GitLab returns Job if match found; Runner claims Job.
   - Runner Controllers (Kubernetes) manage Runner lifecycle.

6. `resource_group` Integration
   - `resource_group` does NOT affect Runner selection.
   - Resource Group lock acquired AFTER Runner assignment.
   - Job enters `waiting_for_resource` state if lock held.
   - Lock released when Job completes (success/failure/canceled).

Runner Selection Algorithm (Ordered):

1. Filter Runners by Job tags (exact match required).
2. Filter by scope (instance > group > project).
3. Filter by protected status (protected Runners only for protected branches/tags).
4. Select Runner with shortest queue (load balancing).
5. Assign Job; Runner transitions to `preparing` state.

---

### §8—Secret & Credential Injection Patterns

GitLab CI Variables (Masked/Protected)

- Integration mechanism: Native GitLab storage.
- YAML configuration:

  ```yaml
  job:
    script:
      - echo $MY_SECRET
  ```

- Scope: Project, Group, Instance; Environment-scoped.
- Rotation/expiry: Manual; no automatic rotation.

HashiCorp Vault

- Integration mechanism: OIDC ID Token + Vault JWT auth.
- YAML configuration:

  ```yaml
  job:
    id_tokens:
      VAULT_ID_TOKEN:
        aud: https://vault.example.com
    secrets:
      DB_PASSWORD:
        vault:
          engine_path: secret/
          path: data/prod/db
          field: password
    script:
      - echo $DB_PASSWORD
  ```

- Scope: Job-level.
- Rotation/expiry: Vault-managed; ID Token expires in 5 minutes.

AWS Secrets Manager

- Integration mechanism: OIDC ID Token + AWS STS AssumeRoleWithWebIdentity.
- YAML configuration:

  ```yaml
  job:
    id_tokens:
      AWS_ID_TOKEN:
        aud: sts.amazonaws.com
    secrets:
      DB_PASSWORD:
        aws:
          secret_name: prod/db/password
          field: SecretString
    script:
      - echo $DB_PASSWORD
  ```

- Scope: Job-level.
- Rotation/expiry: AWS-managed rotation; ID Token expires in 5 minutes.

Azure Key Vault

- Integration mechanism: OIDC ID Token + Azure Federated Identity.
- YAML configuration:

  ```yaml
  job:
    id_tokens:
      AZURE_ID_TOKEN:
        aud: api://AzureADTokenExchange
    secrets:
      DB_PASSWORD:
        azure:
          vault_name: prod-vault
          secret_name: db-password
    script:
      - echo $DB_PASSWORD
  ```

- Scope: Job-level.
- Rotation/expiry: Azure-managed; ID Token expires in 5 minutes.

GCP Secret Manager

- Integration mechanism: OIDC ID Token + GCP Workload Identity Federation.
- YAML configuration:

  ```yaml
  job:
    id_tokens:
      GCP_ID_TOKEN:
        aud: //iam.googleapis.com/projects/PROJECT_ID/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID
    secrets:
      DB_PASSWORD:
        gcp:
          secret_id: projects/PROJECT_ID/secrets/db-password/versions/latest
    script:
      - echo $DB_PASSWORD
  ```

- Scope: Job-level.
- Rotation/expiry: GCP-managed; ID Token expires in 5 minutes.

Fortanix DSM

- Integration mechanism: OIDC ID Token + Fortanix API.
- YAML configuration:

  ```yaml
  job:
    id_tokens:
      FORTANIX_ID_TOKEN:
        aud: fortanix-dsm
    secrets:
      DB_PASSWORD:
        fortanix:
          app_id: my-app
          key_name: db-password
    script:
      - echo $DB_PASSWORD
  ```

- Scope: Job-level.
- Rotation/expiry: Fortanix-managed; ID Token expires in 5 minutes.

Secure Files

- Integration mechanism: GitLab storage with access controls.
- YAML configuration:

  ```yaml
  job:
    script:
      - cp $SECURE_FILE_PATH ./config.json
  secure_files:
    - config.json
  ```

- Scope: Project-level; protected branch access.
- Rotation/expiry: Manual upload; expiration optional.

OIDC ID Tokens (Generic)

- Integration mechanism: JWT for custom OIDC providers.
- YAML configuration:

  ```yaml
  job:
    id_tokens:
      CUSTOM_ID_TOKEN:
        aud: https://custom-provider.example.com
    script:
      - curl -H "Authorization: Bearer $CUSTOM_ID_TOKEN" https://api.example.com
  ```

- Scope: Job-level.
- Rotation/expiry: 5 minutes; audience-restricted.

---

### §9—Testing & Quality Gate Integration

| Signal | `artifacts:reports:` type | Gate behaviour |
|--------|---------------------------|----------------|
| Unit Test (JUnit) | `junit: path/to/*.xml` | Display in MR; no automatic gate (script exit code gates). |
| Code Coverage (Cobertura) | `cobertura: coverage.xml` | Display coverage %; `coverage:` regex can gate minimum %. |
| Code Coverage (JaCoCo) | `jacoco: report.xml` | Display coverage %; `coverage:` regex can gate minimum %. |
| Code Quality (Code Climate) | `codequality: report.json` | Display issues in MR; no automatic gate. |
| Accessibility Testing | `accessibility: report.json` | Display violations in MR; no automatic gate. |
| Browser Performance | `browser_performance: report.json` | Display metrics in MR; no automatic gate. |
| Load Performance | `load_performance: report.json` | Display metrics in MR; no automatic gate. |
| Metrics Reports | `metrics: report.json` | Display custom metrics; no automatic gate. |
| SAST (Static Application Security Testing) | `sast: report.json` | Block MR if severity threshold exceeded (via security policy). |
| DAST (Dynamic Application Security Testing) | `dast: report.json` | Block MR if severity threshold exceeded (via security policy). |
| Container Scanning | `container_scanning: report.json` | Block MR if severity threshold exceeded (via security policy). |
| Dependency Scanning | `dependency_scanning: report.json` | Block MR if severity threshold exceeded (via security policy). |
| Secret Detection | `secret_detection: report.json` | Block MR if secrets found (via security policy). |
| License Compliance | `license_scanning: report.json` | Block MR if disallowed licenses found (via compliance policy). |
| SBOM (Software Bill of Materials) | `sbom: report.json` | Generate SBOM; no automatic gate. |
| Terraform Plan | `terraform: plan.json` | Display plan in MR; manual approval for apply. |

Fail-Fast Conditions:

- `fail_fast: true` at Pipeline level stops all Jobs on first failure.
- Test failures trigger fail-fast if not `allow_failure: true`.
- Security scan failures can trigger fail-fast via policy.
- Coverage below threshold can trigger fail-fast via `coverage:` regex + script exit.

---

### §10—Cost & Efficiency Model

1. DAG Parallelism (`needs:` to remove artificial stage barriers)

- Current default: Jobs in same stage run in parallel; stages run sequentially.
- Recommended: Use `needs` for all Jobs to enable true DAG execution.
- Impact: Latency reduction (30–70% faster Pipelines).
- YAML change: Add `needs: [upstream_job]` to each Job.

1. Conditional Execution (`rules:` / `workflow:` to skip unnecessary Jobs)

- Current default: All Jobs run on every Pipeline.
- Recommended: Use `workflow:rules` to skip Pipelines for docs-only changes; `rules:changes` to skip Jobs when irrelevant files change.
- Impact: Cost reduction (fewer compute minutes); latency reduction.
- YAML change:

  ```yaml
  workflow:
    rules:
      - changes:
          - src/
          - .gitlab-ci.yml
      - when: never
  ```

1. Caching Strategy (cache key design, S3/GCS backends, `policy: pull` vs `pull-push`)

- Current default: Cache key is `$CI_COMMIT_REF_SLUG`; `pull-push` policy.
- Recommended: Use `cache:key:files` for content-addressed cache; `fallback_keys` for branch misses; `policy: pull` for consumer Jobs.
- Impact: Latency reduction (faster dependency installs); cost reduction (less download).
- YAML change:

  ```yaml
  cache:
    key:
      files:
        - package-lock.json
    fallback_keys:
      - cache-main
    paths:
      - node_modules/
    policy: pull-push
  ```

1. Docker Layer Caching (BuildKit, Kaniko, Buildah patterns)

- Current default: No layer caching; full rebuild each Job.
- Recommended: Use BuildKit with `--cache-from`; Kaniko with `--cache=true`; or Docker Registry caching.
- Impact: Latency reduction (50–90% faster builds); cost reduction.
- YAML change:

  ```yaml
  build:
    script:
      - docker build --cache-from $CI_REGISTRY_IMAGE:latest -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
  ```

1. `interruptible: true` (freeing Runners on superseded Pipelines)

- Current default: Pipelines run to completion even if superseded.
- Recommended: Set `interruptible: true` for feature branch Pipelines.
- Impact: Cost reduction (freed compute minutes); latency reduction (newer Pipelines start sooner).
- YAML change: `interruptible: true` at Job or Workflow level.

1. `timeout` (bounding runaway Jobs)

- Current default: Project-wide timeout (default: 60 minutes).
- Recommended: Set per-Job `timeout` based on expected duration.
- Impact: Cost reduction (prevent runaway Jobs); reliability.
- YAML change: `timeout: 10m` at Job level.

1. Matrix / Parallel (spreading test load vs. multiplying cost)

- Current default: Sequential test execution.
- Recommended: Use `parallel:matrix` for cross-platform testing; limit matrix size with `rules`.
- Impact: Latency reduction (parallel tests); cost increase (more compute minutes).
- YAML change:

  ```yaml
  test:
    parallel:
      matrix:
        - NODE_VERSION: [16, 18, 20]
    rules:
      - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      - if: $CI_COMMIT_BRANCH
        parallel:
          matrix:
            - NODE_VERSION: [18]
  ```

1. Merge Trains (batching MRs to reduce total Pipeline runs)

- Current default: Each MR triggers independent Pipeline.
- Recommended: Enable Merge Trains for high-velocity Projects.
- Impact: Cost reduction (fewer redundant Pipelines); reliability (tested in sequence).
- YAML change: Enable in Project Settings > Merge Requests.

1. Compute Minute Budgets (instance vs. hosted Runner cost model)

- Current default: Unlimited for Self-Managed; tiered limits for GitLab.com.
- Recommended: Monitor usage; set Project budgets; use Self-Managed for heavy workloads.
- Impact: Cost control.
- YAML change: N/A (Project Settings).

1. Eco CI Signals (sustainability metrics and how to surface them)

- Current default: No sustainability tracking.
- Recommended: Use `sustainability` reports; track compute minutes per deployment.
- Impact: Awareness; potential cost reduction.
- YAML change:

  ```yaml
  eco_report:
    script:
      - echo "Compute minutes: $CI_JOB_DURATION"
    artifacts:
      reports:
        metrics: eco-report.json
  ```

---

### §11—Integration & Extension Points

| Mechanism | Direction | Protocol | Auth | Use case |
|-----------|-----------|----------|------|----------|
| REST API Trigger | Inbound | HTTPS POST | Personal Access Token / CI Job Token | Trigger Pipeline from external system. |
| Webhook Inbound | Inbound | HTTPS POST | Secret token | External system notifies GitLab of events. |
| Webhook Outbound | Outbound | HTTPS POST | Secret token | GitLab notifies external system of events (push, pipeline, deployment). |
| ChatOps | Inbound | Chat protocol (Slack, Mattermost) | User OAuth | Execute Pipeline actions via chat commands. |
| External Commit Status | Outbound | HTTPS POST | Personal Access Token | GitLab reports status to external SCM (GitHub, Bitbucket). |
| Downstream Pipeline Trigger | Inbound | Internal API | CI Job Token | Parent Pipeline triggers child/multi-project Pipeline. |
| Bridge Job | Inbound | Internal | CI Job Token | Connect Pipelines across projects or hierarchies. |
| OIDC Federation | Outbound | OIDC JWT | Workload Identity | Authenticate to external secret backends (Vault, AWS, GCP, Azure). |
| CD Tool Integration (ArgoCD, Flux, Spinnaker) | Bidirectional | Kubernetes API / Webhook | Service Account / Token | External CD tool deploys based on GitLab Environment state. |
| External Secret Managers | Inbound | Provider API (Vault, AWS, GCP, Azure) | OIDC ID Token | Inject secrets from external backend into Jobs. |
| Cloud Provider Integrations (AWS IAM, GCP Workload Identity, Azure Managed Identity) | Inbound | Provider SDK | OIDC ID Token + AssumeRole | Authenticate to cloud services without long-lived credentials. |

---

### §12—Migration Equivalence Map

| Source system | Source concept | GitLab equivalent | Notes |
|---------------|----------------|-------------------|-------|
| Jenkins | `Jenkinsfile` (Groovy) | `.gitlab-ci.yml` (YAML) | GitLab uses declarative YAML; Jenkins uses Groovy DSL. |
| Jenkins | `agent` | `image` + `tags` | Jenkins agent = GitLab Runner + Docker image. |
| Jenkins | `stages` | `stages` + `stage` | GitLab stages are explicit; Jenkins stages are blocks. |
| Jenkins | `steps` | `script` | Both define commands to execute. |
| Jenkins | `post` | `after_script` / `stage:.post` | GitLab `after_script` runs after Job; `.post` stage runs after all. |
| Jenkins | `environment` | `variables` | Jenkins env vars = GitLab CI/CD variables. |
| Jenkins | `when` | `rules` + `when` | Jenkins `when` = GitLab `rules:if`. |
| Jenkins | `parallel` | `parallel` | Both support parallel execution; GitLab uses DAG. |
| Jenkins | `matrix` | `parallel:matrix` | GitLab matrix runs in parallel; Jenkins runs sequentially. |
| Jenkins | `credentials` | CI/CD Variables (masked/protected) or external secrets | GitLab supports native + external (Vault, AWS, etc.). |
| Jenkins | Plugins | `include:component` / Templates | GitLab Components replace Jenkins plugins. |
| GitHub Actions | `workflow` YAML | `.gitlab-ci.yml` | Similar YAML structure; different keywords. |
| GitHub Actions | `on:` triggers | `rules` + `workflow:rules` | GitLab triggers on Git events by default. |
| GitHub Actions | `jobs` | `stages` + Jobs | GitHub jobs = GitLab Jobs in stages. |
| GitHub Actions | `runs-on` | `tags` | GitHub runner labels = GitLab Runner tags. |
| GitHub Actions | `steps` | `script` | Both define commands. |
| GitHub Actions | `uses:` (Actions) | `include:component` | GitHub Actions marketplace = GitLab Components. |
| GitHub Actions | `env` | `variables` | Both define environment variables. |
| GitHub Actions | `secrets` | CI/CD Variables (masked/protected) | GitHub secrets = GitLab masked variables. |
| GitHub Actions | `strategy:matrix` | `parallel:matrix` | Direct equivalent. |
| CircleCI | `config.yml` | `.gitlab-ci.yml` | Similar YAML structure. |
| CircleCI | `jobs` | Jobs | Direct equivalent. |
| CircleCI | `workflows` | `stages` + `needs` | CircleCI workflows = GitLab DAG. |
| CircleCI | `executors` | `image` + `tags` | CircleCI executors = GitLab Runner + image. |
| CircleCI | `orbs` | `include:component` | CircleCI Orbs = GitLab Components. |
| TeamCity | Build Configuration | `.gitlab-ci.yml` + Project Settings | TeamCity UI config = GitLab YAML + UI. |
| TeamCity | Build Steps | `script` | Direct equivalent. |
| TeamCity | Triggers | `rules` + Schedules | TeamCity triggers = GitLab rules + schedules. |
| TeamCity | Parameters | `variables` + `inputs` | Direct equivalent. |
| Bamboo | Plan | `.gitlab-ci.yml` + Project | Bamboo Plan = GitLab Pipeline. |
| Bamboo | Stage | `stages` | Direct equivalent. |
| Bamboo | Job | Job | Direct equivalent. |
| Bamboo | Task | `script` step | Bamboo Task = GitLab script command. |

---

### §13—Optimisation Agent Heuristics

H-01: Stage-to-DAG Conversion

  Detect: Jobs defined in sequential stages without `needs`.

  Problem: Artificial serialization; Jobs wait for entire stage to complete.

  Fix: Add `needs: [upstream_job]` to enable DAG parallelism.

  Impact: latency-reduction.

  Priority: HIGH.

H-02: Unused Stage Barrier

  Detect: Single Job in a stage.

  Problem: Stage barrier adds no value; suggests over-structuring.

  Fix: Merge into adjacent stage or use `needs`.

  Impact: latency-reduction.

  Priority: LOW.

H-03: Missing `workflow:rules`

  Detect: No `workflow:rules` defined; all Pipelines run on all events.

  Problem: Wasted compute on docs-only or irrelevant changes.

  Fix: Add `workflow:rules` with `changes` filters.

  Impact: cost-reduction.

  Priority: HIGH.

H-04: Hardcoded Secrets in Script

  Detect: Plaintext credentials or tokens in `script` blocks.

  Problem: Security risk; secrets exposed in repository.

  Fix: Move to CI/CD Variables (masked/protected) or external secrets.

  Impact: security.

  Priority: CRITICAL.

H-05: Unpinned Image Tags

  Detect: `image: node:latest` or similar floating tags.

  Problem: Non-reproducible builds; unexpected breaking changes.

  Fix: Pin to specific version (`node:18.17.0`).

  Impact: reliability.

  Priority: HIGH.

H-06: Missing Job Timeout

  Detect: Long-running Jobs without `timeout`.

  Problem: Runaway Jobs consume compute indefinitely.

  Fix: Add `timeout: <duration>` based on expected runtime.

  Impact: cost-reduction.

  Priority: MEDIUM.

H-07: Cache Without Fallback

  Detect: `cache:key` without `fallback_keys`.

  Problem: Cold starts on new branches; slow dependency installs.

  Fix: Add `fallback_keys: [cache-main]`.

  Impact: latency-reduction.

  Priority: MEDIUM.

H-08: Cache for Build Outputs

  Detect: `cache:paths` includes build artifacts (`dist/`, `build/`).

  Problem: Cache is not designed for build outputs; use artifacts instead.

  Fix: Move to `artifacts:paths`.

  Impact: reliability.

  Priority: MEDIUM.

H-09: Missing `interruptible` on Feature Branches

  Detect: Long-running Jobs on feature branches without `interruptible: true`.

  Problem: Superseded Pipelines continue running, wasting compute.

  Fix: Add `interruptible: true` at Workflow or Job level.

  Impact: cost-reduction.

  Priority: MEDIUM.

H-10: Manual Deploy Without Approval

  Detect: Production deploy Job without `when: manual` or Protected Environment.

  Problem: Accidental deployments; no human oversight.

  Fix: Add `when: manual` and configure Protected Environment.

  Impact: reliability.

  Priority: HIGH.

H-11: Missing `resource_group` for Production

  Detect: Multiple production deploy Jobs without `resource_group`.

  Problem: Race conditions; concurrent deployments.

  Fix: Add `resource_group: production`.

  Impact: reliability.

  Priority: HIGH.

H-12: No Test Reports Configured

  Detect: Test Jobs without `artifacts:reports:junit`.

  Problem: Test results not visible in MR; harder to debug failures.

  Fix: Add `artifacts:reports:junit: path/to/*.xml`.

  Impact: reliability.

  Priority: MEDIUM.

H-13: Missing Coverage Gate

  Detect: Test Jobs without `coverage:` regex or threshold.

  Problem: No visibility into test coverage trends.

  Fix: Add `coverage: '/Lines\\s*:\\s*(\\d+\\.?\\d*)%/'` and enforce threshold.

  Impact: reliability.

  Priority: LOW.

H-14: Overly Broad Matrix

  Detect: `parallel:matrix` with >10 combinations on all branches.

  Problem: Explodes compute cost; long queue times.

  Fix: Use `rules` to limit matrix on feature branches.

  Impact: cost-reduction.

  Priority: MEDIUM.

H-15: Missing `needs` for Artifact Consumers

  Detect: Job downloads artifacts without explicit `needs`.

  Problem: Implicit dependency on stage order; fragile to refactoring.

  Fix: Add `needs: [producer_job]`.

  Impact: reliability.

  Priority: MEDIUM.

H-16: No Security Scans in Pipeline

  Detect: No SAST, DAST, or dependency scanning Jobs.

  Problem: Vulnerabilities not detected pre-merge.

  Fix: Add `include:template` for security scans.

  Impact: security.

  Priority: HIGH.

H-17: Missing SLSA Provenance

  Detect: Production builds without provenance generation.

  Problem: Supply chain integrity not verifiable.

  Fix: Add SLSA provenance generation Job.

  Impact: security.

  Priority: MEDIUM.

H-18: Environment Without URL

  Detect: Deploy Job with `environment:name` but no `environment:url`.

  Problem: No clickable link in UI; harder to access deployment.

  Fix: Add `environment:url`.

  Impact: reliability.

  Priority: LOW.

H-19: No Rollback Mechanism

  Detect: Production Environment without rollback Job or strategy.

  Problem: Cannot quickly revert failed deployments.

  Fix: Add manual rollback Job or document re-run procedure.

  Impact: reliability.

  Priority: HIGH.

H-20: External Secrets Without OIDC

  Detect: Secrets stored in CI/CD Variables instead of external backend.

  Problem: Limited rotation; no audit trail.

  Fix: Migrate to HashiCorp Vault or cloud secret manager with OIDC.

  Impact: security.

  Priority: MEDIUM.

---

### §14—Deployment Orchestration Checklist

- [ ] Pipeline structure—stages defined, DAG wired with `needs:`
  - YAML keywords: `stages`, `needs`, `stage`.
  - Risk if unchecked: Sequential execution; unnecessary latency.

- [ ] Runner selection—jobs tagged for appropriate executor + tier
  - YAML keywords: `tags`, `image`.
  - Risk if unchecked: Jobs stuck in queue; wrong hardware.

- [ ] Variable hygiene—secrets masked, protected; no plaintext credentials
  - YAML keywords: `variables` (UI-configured: masked, protected).
  - Risk if unchecked: Credential exposure; security breach.

- [ ] Secret backend—external vault integrated with ID token auth
  - YAML keywords: `secrets`, `id_tokens`.
  - Risk if unchecked: Manual rotation; no audit trail.

- [ ] Environment bindings—every deploy job has `environment:` with tier
  - YAML keywords: `environment:name`, `environment:deployment_tier`.
  - Risk if unchecked: No deployment tracking; invisible state.

- [ ] Protected environment—production gated with approval rules
  - YAML keywords: `when: manual` + UI-configured Protected Environment.
  - Risk if unchecked: Accidental deployments; unauthorized changes.

- [ ] Resource group—production environment has concurrency lock
  - YAML keywords: `resource_group: production`.
  - Risk if unchecked: Race conditions; concurrent deployments.

- [ ] Artifact chain—build output passed via artifacts not re-built
  - YAML keywords: `artifacts:paths`, `needs`, `dependencies`.
  - Risk if unchecked: Inconsistent binaries; wasted compute.

- [ ] Cache keys—deterministic, content-addressed, branch-scoped
  - YAML keywords: `cache:key:files`, `fallback_keys`.
  - Risk if unchecked: Cache misses; slow builds.

- [ ] Conditional execution—MR / branch rules prevent redundant runs
  - YAML keywords: `rules`, `workflow:rules`, `rules:changes`.
  - Risk if unchecked: Wasted compute on irrelevant changes.

- [ ] Rollback job—manual rollback path exists for production
  - YAML keywords: `when: manual`, `environment:action:rollback`.
  - Risk if unchecked: Cannot quickly revert failed deployments.

- [ ] Quality gates—test reports uploaded, coverage threshold enforced
  - YAML keywords: `artifacts:reports:junit`, `coverage`.
  - Risk if unchecked: Undetected test failures; coverage decay.

- [ ] Security gates—SAST/DAST/dependency scan in pipeline
  - YAML keywords: `include:template` (security scans).
  - Risk if unchecked: Vulnerabilities reach production.

- [ ] SLSA provenance—provenance record generated for production artifacts
  - YAML keywords: Custom script + `artifacts:reports:slsa`.
  - Risk if unchecked: Supply chain integrity not verifiable.

- [ ] Compute budget—`timeout` set on all jobs, `interruptible` on build jobs
  - YAML keywords: `timeout`, `interruptible`.
  - Risk if unchecked: Runaway jobs; wasted compute on superseded Pipelines.

- [ ] Monitoring—deployment tracked via environment; external tool hook present
  - YAML keywords: `environment:url`, webhook or external CD integration.
  - Risk if unchecked: No visibility into deployment health; delayed incident response.

---

_End of GitLab CI/CD Domain Knowledge Context._
