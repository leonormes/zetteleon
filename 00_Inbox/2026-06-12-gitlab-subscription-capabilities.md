---
created: 2026-06-11T10:13:52+00:00
date: 2026-06-12
modified: 2026-06-11T10:25:37+00:00
project: FITFILE
source: claude-sonnet-4-6 (delegated reasoning)
status: inbox
tags: [cicd, gitlab, optimization, plan, premium, quota, runner, subscription]
title: 2026-06-12-gitlab-subscription-capabilities
---

## GitLab Premium Subscription—CI/CD Capabilities & Pipeline Impact

Audit Date: 12 June 2026
Group: `fitfile` (ID: 9759878)
Plan: Premium (SaaS)
Primary Project: `fitfile/apps/InsightFILE` (ID: 22023844)

---

### 1. Subscription Overview

| Detail | Value |
|---|---|
| Plan | Premium |
| Billing | SaaS (gitlab.com) |
| Visibility | Private |
| Shared Runner Minutes | 10,000 / month |
| Extra Minutes | 16 |
| SaaS Runner Type | `saas-linux-small-amd64` (default) |
| SaaS Runner Pool | Shared GitLab-managed (~30 parallel slots for Premium) |
| Container Registry | ✅ Enabled |

---

### 2. Pipeline Performance Factors—Enabled Vs Missed

#### ✅ Already Enabled (Good)

| Feature | Setting | Impact on Performance |
|---|---|---|
| Separated Caches | `ci_separated_caches: true` | Caches are isolated per branch—prevents cross-branch cache corruption. No need for manual `$CI_COMMIT_REF_SLUG` keys. |
| Merge Trains | `merge_trains_enabled: true` | Queues MRs together and tests them in a combined pipeline. Reduces merge queue time. |
| Merge Pipelines | `merge_pipelines_enabled: true` | Runs pipeline on the _merged result_ (not just the source branch)—catches merge conflicts before they reach `development`. |
| Auto-cancel Pending | `auto_cancel_pending_pipelines: enabled` | When you push a new commit, GitLab automatically cancels any pending/running pipelines on the same branch. Prevents wasted CI minutes. |
| Container Registry | `container_registry_enabled: true` | Custom images (`fitfile/sonar-nodejs`, `fitfile/gapv`) hosted in the GitLab registry. Already being used alongside ACR. |
| ID Tokens (OIDC) | `ci_id_token_sub_claim_components: [project_path, ref_type, ref]` | Available and configured—can be used to authenticate to Azure without storing service principal secrets. Currently not used. |
| Git Depth | `ci_default_git_depth: 50` | Shallow clone (50 commits)—reduces clone time significantly. However, overridden to `0` (full clone) in SonarQube jobs. |
| Build Timeout | 3,600 seconds (1 hour) | Jobs have an hour to complete. Reasonable for most build/test tasks. |

#### ⚠️ Available But NOT Enabled (Opportunity)

| Feature | Current Setting | What It Does | Impact If Enabled |
|---|---|---|---|
| Forward Deployment | `ci_forward_deployment_enabled: false` | Prevents a newer pipeline from being overwritten by an older one on the same ref. When pushing multiple commits rapidly, the _latest_ pipeline always reflects the newest code—no stale results. | Prevents "last push won race" scenarios. If 2 pushes happen in quick succession, without this the older pipeline's result can overwrite the newer one. Low effort, moderate reliability gain. |
| CI Job Token Scope | `ci_job_token_scope_enabled: false` | Restricts `CI_JOB_TOKEN` to only access projects that are explicitly added. | Security hardening. Currently `CI_JOB_TOKEN` can access any project in the group. Restricting it follows least-privilege. Important because job tokens are used in `gapv.sh` and `build.sh` with `GIT_AUTH_TOKEN`. |
| Allow Merge on Skipped | `allow_merge_on_skipped_pipeline: false` | When a pipeline is skipped (e.g. `[skip ci]` in commit message), MR cannot be merged. | Currently blocked. If intentional, leave as-is. |
| Pipeline Success Required for Merge | `only_allow_merge_if_pipeline_succeeds: false` | MRs can be merged even if the pipeline fails. | ⚠️ This explains why the 10-failure streak on MR!2307 didn't block merging. Enabling it would enforce pipeline gating—a significant policy decision. |

#### ❌ Not Supported on Premium (Would Require Ultimate)

| Feature | Why It Matters | Alternative on Premium |
|---|---|---|
| SaaS Linux Medium/Medium 2x Runners | `saas-linux-medium-amd64` offers 2x CPU/RAM over `small`. Only available on Ultimate. | Use dedicated runners or self-managed runners with beefier instances. |
| Dedicated Runner Autoscaling | Fully managed runner fleets per group. | Already have SaaS runners; evaluate if `saas-linux-small` is a bottleneck. |
| Analytics / CI CD Analytics | Per-job performance dashboards. | Use `glab ci get --output json` + `jq` to extract metrics manually. |

---

### 3. Shared Runner Details

The project currently uses GitLab SaaS Linux shared runners (`saas-linux-small-amd64`).

#### Runner Specifications

| Property | saas-linux-small-amd64 |
|---|---|
| CPU | 2 vCPUs |
| RAM | ~7.5 GB |
| Disk | ~50 GB ephemeral |
| OS | Ubuntu 22.04 LTS |
| Concurrent Jobs | ~30 per group (Premium tier) |
| Cost | Included in Premium (10,000 min/month) |

From the pipeline data, runners assigned to jobs come from a pool of ~10+ named instances:

```
1-blue.shared-gitlab-org.runners-manager.gitlab.com
2-blue.shared-gitlab-org.runners-manager.gitlab.com  
4-blue.saas-linux-small-amd64.runners-manager.gitlab.com
5-blue.saas-linux-small-amd64.runners-manager.gitlab.com
7-blue.saas-linux-small-amd64.runners-manager.gitlab.com
8-blue.saas-linux-small-amd64.runners-manager.gitlab.com
9-blue.saas-linux-small-amd64.runners-manager.gitlab.com
```

Windows runners are paused (not used).

#### Runner Minutes Consumption Estimate

InsightFILE successful pipeline: ~826 seconds = ~14 minutes
With ~7 verification/build jobs running in parallel → approximately ~2 minutes of billable time per pipeline job.

A single successful pipeline completion costs roughly 10–15 billable minutes. With 10,000 minutes/month, that's room for approximately 650–1,000 full pipeline runs per month—assuming no wasted minutes on failed jobs.

The last 10 failed pipelines on MR!2307 each ran ~18 minutes × ~7 parallel jobs = wasted ~25–30 billable minutes per failure. That's roughly 250–300 minutes burned on one MR's failed pipeline retries.

---

### 4. Constraints & Bottlenecks

#### 4.1 Runner Instance Type (Medium Not Available)

All jobs run on `saas-linux-small-amd64` (2 vCPU, 7.5 GB RAM). No option to request larger instances (e.g. medium with 4 vCPU) without upgrading to Ultimate or deploying self-managed runners.

Impact: `verify_ffcloud` (424s) and `frontend_interaction_tests` (316s) are likely CPU/memory-bound on small runners. Jest runs 4 parallel workers (`-n 4` on Python, unknown for yarn workspace test). A larger runner would reduce wall-clock time proportionally.

Options:

1. Upgrade to Ultimate to access `saas-linux-medium-amd64` (4 vCPU, 15 GB RAM)
2. Deploy self-managed runners on Azure (e.g. `Standard_D4s_v5` 4 vCPU, 16 GB RAM)—billed via Azure, not GitLab minutes
3. Optimise job-level parallelism instead (split tests into `parallel:matrix` shards)

#### 4.2 Forward Deployment Not Enabled

Without forward deployment, when you push multiple commits to the same branch in quick succession, GitLab runs the pipeline on each commit. The old pipeline's result can overwrite the new one in the MR status check—causing a "last-writer-wins" race condition.

Mitigation: Enable `ci_forward_deployment_enabled: true` in project CI/CD settings. This ensures that only the latest pipeline on a ref is used for MR status.

#### 4.3 Merge Pipeline Strategy—Merge Trains Already in Use

The pipeline YAML uses `CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"` as a trigger condition for verification and build jobs. This is good—merge trains test the combined result of multiple MRs.

However, there's a subtlety: not all jobs run on merge train. `install_dependencies` and most verification jobs exclude merge trains with `when: never`, meaning merge trains skip verification entirely and go straight to building Docker images. They rely on the assumption that _individual MR pipelines_ already passed verification.

This is correct for performance (avoiding redundant verification) but creates a window where a merge train pipeline could fail at build time due to a conflict that the individual MR verification didn't catch.

#### 4.4 No Method To Check Remaining Runner Minutes From API

The `/groups/fitfile/ci_quotas` and `/ci/quotas` endpoints return 404. Runner minute consumption must be checked via the GitLab UI at:

```
Settings → CI/CD → Pipeline quotas → View runners
```

or the group-level page:

```
https://gitlab.com/groups/fitfile/-/settings/ci_cd
```

This means automated quota monitoring (e.g. a cron job that warns when minutes are low) requires either UI scraping or a billing API endpoint with higher permissions.

---

### 5. Recommendations Ranked by Impact

| # | Action | Effort | Performance Impact | Resilience Impact |
|---|---|---|---|---|
| 1 | Enable `ci_forward_deployment_enabled: true` | 1 click in UI | ⭐ None—it just stops race conditions | ✅ Prevents stale pipeline results overwriting fresh ones |
| 2 | Enable `ci_job_token_scope_enabled: true` | Med—requires whitelisting projects | ⭐ None | ✅ Removes broad token access (supply-chain hardening) |
| 3 | Leverage ID tokens for Azure auth | Med—rewrite `az login` in CI to use OIDC | ⭐ None | ✅ Eliminates stored service principal secrets |
| 4 | Adopt `parallel:matrix` for test sharding | Low—config change only | ✅ Splits 424s verify job into 3 parallel shards (~140s each) | ⭐ Redundant execution—one shard failure doesn't block others |
| 5 | Evaluate self-managed runners | High—infra setup | ✅ 4 vCPU runners cut test time by ~40% | ⭐ More consistent availability than shared pool |
| 6 | Set `only_allow_merge_if_pipeline_succeeds: true` | 1 click in UI | ⭐ None | ✅ Prevents merging broken code (policy decision) |
| 7 | Add automated quota monitoring | Med—external cron script | ⭐ None | ✅ Prevents surprise out-of-minutes blockage |

---

### 6. Premium Vs Ultimate Gap Analysis

| Capability | Premium | Ultimate | Impact on Fitfile |
|---|---|---|---|
| Merge Trains | ✅ Yes | ✅ Yes | Already using |
| Separated Caches | ✅ Yes | ✅ Yes | Already using |
| ID Tokens / OIDC | ✅ Yes | ✅ Yes | Available but unused |
| SaaS Runner Concurrency | ~30 jobs | ~50+ jobs | Current bottleneck is _per-job duration_, not concurrency |
| SaaS Linux Medium Runners | ❌ No | ✅ Yes | Would directly speed up `verify_ffcloud` (424s) by 2x |
| CI/CD Analytics Dashboard | ❌ No | ✅ Yes | Would help identify bottlenecks visually |
| Security Dashboard | ❌ No | ✅ Yes | SAST results summarised |
| Dependencies / License Compliance | ❌ No | ✅ Yes | Audit dependencies (currently done manually via `yarn npm audit`) |

Verdict: Upgrading to Ultimate would primarily buy medium-sized runners and analytics dashboards. If pipeline speed is the priority, a self-managed runner fleet on Azure may be more cost-effective than the Ultimate upgrade.

---

### 7. Quick Actions

#### Enable Forward Deployment

```bash
# Via API (requires maintainer access)
curl --request PUT \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --data "ci_forward_deployment_enabled=true" \
  "https://gitlab.com/api/v4/projects/22023844"
```

#### Enable CI Job Token Scope

```bash
# Via API — enables scope, then add the deployment repo as allowed
curl --request PUT \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --data "ci_job_token_scope_enabled=true" \
  "https://gitlab.com/api/v4/projects/22023844"

# Add deployment repo to allowed list
curl --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --data "target_project_id=26866916" \
  "https://gitlab.com/api/v4/projects/22023844/job_token_scope/allowlist"
```

_(Find the deployment project ID with `glab api /projects/fitfile%2Fdeployment 2>&1 | jq '.id'`)_

#### Check Remaining Runner Minutes (UI Only)

```
https://gitlab.com/groups/fitfile/-/settings/ci_cd
```

Look for "Pipeline quota" in the right-hand panel.

---

### 8. Runner Minutes Budget Calculation

| Item | Value |
|---|---|
| Monthly allowance | 10,000 min |
| Successful pipeline cost (approx) | ~12 min |
| Failed pipeline cost (approx) | ~15 min (longer due to retries + no early abort) |
| Pipeline runs per month (est.) | 300–400 (branch + MR + release) |
| Estimated monthly consumption | 3,600–6,000 min |
| Buffer | ~4,000 min (40% room for retries) |

At current velocity, minutes are unlikely to be a constraint. The bigger risk is wasting minutes on long-running failed jobs—the 10-failure streak on MR!2307 likely burned ~300 minutes unnecessarily. Early-abort patterns (fail-fast) in the CI YAML would preserve this buffer.
