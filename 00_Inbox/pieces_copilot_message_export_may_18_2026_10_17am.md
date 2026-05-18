---
created: 2026-05-18T09:17:55+00:00
modified: 2026-05-18T09:18:42+00:00
title: pieces_copilot_message_export_may_18_2026_10_17am
---

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
