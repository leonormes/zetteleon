*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Thursday Jun 11, 2026 - 11:07 AM*
---
Both cursors are now exhausted of the most material evidence. The `ask_memory` page adds important confirmatory detail on runner availability (4 of 20 online, 20% at time of audit), the ACR client secret expiry date, and the job-name mismatch between failure traces and the current config. The `search_memory` cursor confirmed sufficient. Here is the continuation of the report from where it was cut off.

---

### Bottleneck 5 — Three-tier deployment pipeline adds unavoidable latency

The FITFILE delivery flow is inherently multi-hop: code commit → GitLab CI build/push → version bump PR → `fitfile-version-manager` Terraform output → `helm_chart_deployment` CUE export → ArgoCD sync → AKS apply. Each hop is a gate. The `ask_memory` digest confirmed the delivery chain explicitly:

> "Code commit → GitLab CI Build → ACR Push → Version Bump → Deployment Repo Update → ArgoCD Sync → AKS Deployment"
> (from `INSIGHTFILE_PIPELINE_REPORT - LLMeon - Obsidian 1.12.7`, 18 May 2026)

The staging pipeline — `staging.gitlab-ci.yml` — was found to run on **every push without path filters**, meaning every commit, including README changes, triggered the full ArgoCD sync + integration test cycle. This was confirmed during the 28 May 2026 pipeline optimisation session ([GitLab CI/CD Pipeline Optimization Summary](https://gitlab.com/fitfile/deployment/-/jobs/14582650690)):

> "None of these jobs should run when you push a README, a CUE schema change, a chart tweak, etc. They were running on every single push."

Fixes applied 28 May 2026 added `rules: changes:` path filters to the deployment pipeline, but the **application pipeline** (`InsightFILE/.gitlab-ci.yml`) still uses the legacy `only: [development, main]` syntax with no path filtering and runs all 6 build jobs serially (no `needs:` DAG parallelism).

---

### Bottleneck 6 — Single-owner review gate is blocking merge throughput (identified in meeting 10 Jun 2026)

The "Release Catch Up" meeting on 10 Jun 2026 — attended by Leon Ormes, **Yasir Mansoor**, **Weronika Jastrzebska**, and **Robin Mofakham** — produced the most raw and direct statement of the systemic bottleneck:

> "It is blocking in one person and I think he would also say he would love to not be that person but we need to improve quality... we need to be able to move forwards and will not rely on him to be improving every PR"

> "So I've been here a year and a half I still don't understand the back-end property because so overly complex so over-engineered and then constantly the my Dev environment work broken"

This is unambiguous: **one engineer is the de facto gate for all PRs reaching staging**, creating a single point of failure that prevents parallelism and burns out the individual involved. The team discussed trunk-based development vs. long-lived branches, feature flags, and the inability to spin up ephemeral environments ("we can't do a femoral environment, which cannot"). The lack of a CI quality gate means this human review is the only quality gate — and it is not scalable.

---

### Bottleneck 7 — Helm chart templating has no CI lint coverage for `charts/ffnode`

Confirmed 6 Jun 2026 during the ffnode Helm chart analysis session ([Analyze ffnode Helm chart templating architecture](https://gitlab.com/fitfile/deployment)):

> "CI renders `workflows/src` and `workflows/integration-tests` but **never renders or lints `charts/ffnode/`** or any `ffnodes/*` — there's a `validate` stage with `lint_workflows` but no equivalent for the chart that deploys every cluster."

This means the primary chart driving every customer cluster deployment has zero automated validation. Breakage only surfaces at ArgoCD sync time or live on a cluster. The `lint_workflows` job ([job #14582650690](https://gitlab.com/fitfile/deployment/-/jobs/14582650690)) validates Argo Workflows definitions but does not cover ffnode.

---

### Bottleneck 8 — Terraform state conflicts and multi-workspace drift accumulate silently

The MKUH Terraform spike ([FTFL-658](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281)) confirmed **MKUH Terraform runs have been failing for over a month** due to a missing `argocd_path` attribute in `generators/variables.tf`. Root cause fixed 5 Jun 2026. The workspace is currently apply-blocked by an active change freeze. Multiple other incidents surfaced the same class of problem:

- **`cuh-poc-1`** workspace: subnet IP overlap + resource-already-exists state conflicts requiring manual `terraform import` remediation (19 May 2026)
- **`test-cluster`**: `upgrade_override` constraint error + undeclared `cloudflare_issuer_api_token` variable in `tfvars` (27 May 2026)
- **`lca-prd-2`**: 403 Insufficient scope on GitLab API during apply (13 Apr 2026)

There is a documented three-generation architecture transition in progress (`Gen1 → Gen2 → Gen3` data-driven pipeline: `customer.yaml → Terraform → infra_facts → CUE → values.yaml`). The system is mid-transition — clusters at different generations have different fix patterns — and this is the root cause of the state drift recurrence. From `MASTER_REMEDIATION_PLAN.md`:

> "The system is mid-transition between three overlapping deployment models... Generation 3 — data-driven pipeline: customer.yaml → Terraform → infra_facts → CUE → values.yaml. The correct target model. Partially implemented..."

---

## What to build — prioritised roadmap

Ranked by: **impact × urgency × effort** (higher number = build first). Evidence for each is grounded in the investigations above.

### Tier 1 — Ship immediately (unblock the pipeline now)

| # | Item | Impact | Effort | Evidence |
|---|---|---|---|---|
| **T1.1** | Fix `fitfile/sonar-nodejs:1.0.0` base image — add `make g++ python3` via `RUN apk add` (or pin `docker install ignoredBuilds` as workaround) | Stops `BUILD_COMPILE` failures (8% of ALL pipeline failures) | Low (Dockerfile 1-liner) | Pipelines `2522046776`, `2521911238`; `INSIGHTFILE_PIPELINE_IMPROVEMENT_PLAN` |
| **T1.2** | Fix `koa-bodyparser` ESLint `import/no-unresolved` — add `@types/koa-bodyparser` to devDependencies or update eslint config | Stops `TEST_FAILURE` failures (8% of ALL failures) | Low | `INSIGHTFILE_PIPELINE_REPORT`, Evidence E4/E5 |
| **T1.3** | Rotate ACR service principal (`FITFILE Gitlab Integration Test Pipelines`, AppID `aa9d88df-26fd-4239-a48a-19068e0502c5`) **before 27 Jul 2026** | Prevents ACR_AUTH pipeline meltdown that took down build jobs in Apr 2026 ([pipeline 2468041533](https://gitlab.com/fitfile/apps/InsightFILE/-/pipelines/2468041533)) | Low (Azure portal task) | `INSIGHTFILE_PIPELINE_REPORT` §7; ACR_AUTH Slack thread with Yasir Mansoor |
| **T1.4** | Set 7 of 10 group-level CI variables to `protected: true` | Prevents credential leakage to non-protected branches | Low | `INSIGHTFILE_PIPELINE_IMPROVEMENT_PLAN` P2.1 |

### Tier 2 — Build in the next sprint (structural fixes)

| # | Item | Impact | Effort | Evidence |
|---|---|---|---|---|
| **T2.1** | Add `changes:` path filters to `InsightFILE/.gitlab-ci.yml` — only trigger builds on actual code changes, not docs/configs | Eliminates ~40% of unnecessary pipeline runs based on staging analysis | Medium | 28 May 2026 pipeline optimisation session; [SOT - CI-CD Pipelines](https://fitfile.atlassian.net/wiki/spaces/~633ae2b9fedc6169aed8f601/pages/2812477441) |
| **T2.2** | Convert `InsightFILE` jobs to DAG using `needs:` — run unit tests in parallel rather than sequentially after all builds | Cuts wall-clock pipeline time by ~50% | Medium | `FITFILE_CICD_AUDIT_REPORT` §5, pipeline coverage map |
| **T2.3** | Add `helm lint` + `helm template` job for `charts/ffnode` in the deployment pipeline validate stage — identical pattern to existing `lint_workflows` | Catches chart regressions before they hit ArgoCD on live clusters | Low | 6 Jun 2026 ffnode architecture session |
| **T2.4** | Replace `docker/argocli:alpine` in deployment pipeline with a pinned versioned tag — stop using `docker:latest` in build jobs | Reproducible builds; eliminates transient upstream breakage | Low | `INSIGHTFILE_PIPELINE_IMPROVEMENT_PLAN` P3.1 |
| **T2.5** | Retrieve and classify the **21 UNKNOWN failures** from the 90-day InsightFILE window using `glab trace` | Uncovers any hidden failure mode that may dwarf the known 16% | Medium | `INSIGHTFILE_PIPELINE_REPORT` §4.1; Evidence E1 |

### Tier 3 — Build in the next 4–6 weeks (quality gates + architecture)

| # | Item | Impact | Effort | Evidence |
|---|---|---|---|---|
| **T3.1** | Implement a **merge-request quality gate** (automated test pass + linter pass) — replace the informal one-person human gate with CODEOWNERS + required pipeline approvals | Removes the single-owner review bottleneck identified in the 10 Jun 2026 Release Catch Up meeting | High | "Release Catch Up" meeting audio, 10 Jun 2026 |
| **T3.2** | Complete the **Generation 3 IaC migration** for all active customer workspaces — move remaining Gen1/Gen2 clusters to the `customer.yaml → Terraform → infra_facts → CUE → values.yaml` data-driven pipeline | Eliminates the class of Terraform state drift/collision errors that have hit CUH, MKUH, test-cluster, lca-prd-2 | High | `MASTER_REMEDIATION_PLAN.md`; FTFL-658; cuh-poc-1 state conflicts |
| **T3.3** | Add a `merge_request_event` Terraform plan job to all customer cluster repos (currently `test_terraform_plan` had no `rules:` — fixed 28 May 2026 but not propagated to all repos) | Catches plan-breaking changes before merge | Medium | 28 May 2026 pipeline optimisation: "Had no rules at all - was running compare_plan.sh automatically on every push" |
| **T3.4** | Re-enable the **SonarQube quality gate** in InsightFILE (currently disabled — job `fitfile/sonar-nodejs:1.0.0` was the source of the build failures, and it was removed rather than fixed) | Restores code quality signal for the main application | Medium | `INSIGHTFILE_PIPELINE_IMPROVEMENT_PLAN` P4.3 |
| **T3.5** | Implement **Grafana Alloy automatic recovery** — the testing cluster lost all log ingestion entirely on 5 Jun 2026 due to Helm chart schema changes not being caught | Prevents the recurrent "no logs for 30 days" silent failure (staging had zero logs for 30+ days before detection) | High | 28 May 2026 Grafana monitoring sync failure investigation; staging alloy-logs `logs_service` secret naming mismatch |

### Tier 4 — Strategic investments (3–6 month horizon)

| # | Item | Impact | Effort | Evidence |
|---|---|---|---|---|
| **T4.1** | Introduce **trunk-based development** with feature flags — eliminate the long-lived feature branches that cause merge skew and staging breakage discussed in the 10 Jun 2026 Release Catch Up meeting | Moves FITFILE toward the DORA high-performer model (discussed via [Merge Skew: CI/CD Problem and Solution](https://gemini.google.com/app/d11f43edf54e6164) research, 22 May 2026) | High (cultural) | Release Catch Up meeting; Merge Skew research session |
| **T4.2** | Build **per-cluster Terraform drift detection** into the pipeline — scheduled daily plan runs with alerting on drift, not just run-time discovery | Stops the accumulation of silent drift that forces manual `terraform import` remediations | High | MKUH drift; CUH-DP state conflicts; test-cluster `upgrade_override` error |
| **T4.3** | Add `mypy` type checking for `workflows-api` (Python service) and re-enable GitLab SAST template | Uplifts code quality signal for the Python services that represent a significant failure surface | Medium | `INSIGHTFILE_PIPELINE_IMPROVEMENT_PLAN` P4.4/P4.5 |
| **T4.4** | Instrument **Four Key Metrics** (DORA: deployment frequency, lead time, MTTR, change fail rate) — baseline captured via GitOps Deployment Pipeline Optimisation project scoped 23 May 2026 | Turns subjective "the pipeline feels slow" into data-driven decision-making | Medium | [GitOps Deployment Pipeline Optimisation](https://fitfile.atlassian.net/wiki/spaces/~633ae2b9fedc6169aed8f601), 23 May 2026 |

---

**Open loops to close before planning begins:**
- 21 UNKNOWN InsightFILE failures uncategorised — retrieve traces before sprint planning
- MKUH change freeze status — unblock T2.x Terraform remediation once freeze lifts
- ffnode chart lint coverage gap — T2.3 is a small PR that can ship in the current sprint without coordination cost
- ACR secret rotation deadline: **27 Jul 2026** — T1.3 is time-critical