---
author: Hermes (consolidation)
created: 2026-08-24T17:00:00+00:00
modified: 2026-08-26T14:06:49+00:00
permalink: llmeon/30-library/200-projects/pipeline-best-practices-research-prompt
tags: [1, argo-cd, ci-cd, cicd, devops, fitfile, gitlab, pipeline, research-prompt, SDLC, security, trivy, vulnerability-management]
title: FitFile CI_CD Pipeline — Consolidated Notes
type: note
---

## FitFile CI/CD Pipeline—Consolidated Notes

Single consolidated reference for FitFile's CI/CD pipeline work, merged from six `00_Inbox/` captures (2026-08-24/2026-08-12). Organised for parsing: state → bottlenecks → security → contract testing → telemetry → actions.

---

### 1. Source Index

| # | Source (original `00_Inbox/` file) | Date | Focus |
|---|---|---|---|
| A | `FitFile CI_CD Pipeline Research.md` | 2026-08-24 | Evidence-based pipeline strategy (DORA/SRE), 3-phase action plan |
| B | `fitfile_pipeline_notes.md` | 2026-08-24 | Miro board retro—6 pipeline stages, problems, improvements, FTFL-971 cross-ref |
| C | `Pipeline Optimisation (caching + merge-skew workflow rules).md` | 2026-08-24 | GitLab YAML patterns: caching, workflow:rules, shift-left gates |
| D | `Contract Testing and CI_CD Guide.md` | 2026-08-12 | Advanced contract testing + release management topology |
| E | `Implementing self-verifying alerts for CICD pipelines.md` | 2026-08-24 | Dead-man's-switch / heartbeat alerts (FTFL-938/942) |
| F | `What Kubescape does.md` | 2026-08-24 | Kubescape K8s posture scanner vs Trivy |

---

### 2. Current Pipeline State (Miro Board Retro—Source B)

#### 2.1 Six Stages

| Stage | Key steps | Main problems |
|---|---|---|
| 1. Local Dev | dev env, unit/integration tests, lint, manual, Claude Code, Renovate, npm audit | Dev env difficult; "have we shift-left enough?"; Renovate PRs can't be blindly merged; multi-repo orchestration |
| 2. Feature Branch | unit, Playwright, Storybook, build, lint, npm audit | SonarQube timing; growing `npmAuditIgnore`; feature flags not visible; small-team PR approval |
| 3. Merge Train | API/integration tests, data-pipeline tests, migration tested, RC image builds, TFC for infra | No parallelism (bottleneck); flaky API tests; no resource limits on test pods; no way to pass image version to tests (uses ArgoCD sync); no build cache; low test coverage; concurrent-pipeline race conditions |
| 4. Staging Release | full image build, push to ACR, chart tags bumped, package version bumped, TFC + local Terraform | No build cache; ACR push secret expires (manual update); upgrading private resources; "test & staging seem interchangeable" |
| 5. Production Release | move per-customer latest-release tag for ArgoCD, TFC, tag | No rollback procedure (esp. with migrations); per-env config drift; no inbound connectivity to private clusters without bastion |
| 6. Customer Release | per-customer latest-release tag, TFC, manual UI check | Manual per-customer tagging; no client overview; demo env stability; customer config changes require a new release |

#### 2.2 Root / Cross-Stage Problems

- Critical: pipelines slow; pipelines flaky; 1 concurrent pipeline at a time; builds slow
- Process: few people can manage deployments; deployment assuredness; monorepo needs non-blocking pipeline (HEAD commits blocking); 🔴 00:19:02 frontend-only run
- Build & Infra: all ACR builds AMD64 (rebuilds); no build cache (×3 mentions); no SBOM; no release notes; 3 disparate deploy paths (infra/platform/application); can't cherry-pick releases; charts not built/versioned in ACR; stacked PRs (?)
- Stability: DB connectivity for demo/test; demo env stability

#### 2.3 Miro Board Improvements

- Quick wins: move customer config to own repos; own GitLab runners (build cache); parameterise integration tests to parallelise; publish charts to ACR; write more pipeline tests
- Experimental/future: ephemeral envs per branch; feature flags
- Epic ideas: flagged "🚀 LETS DO THIS!!"

#### 2.4 Ticket Cross-Reference (Miro → FTFL)

| Miro item | Ticket(s) |
|---|---|
| ACR push secret expires | FTFL-978/979/980/981 (OIDC federation replaces static ACR password) |
| 🔴 19:02 frontend run | FTFL-988 (625s warm / 1423s cache-miss; root cause: yarn cache not mounted into build context) |
| No build cache (×3) | FTFL-987 (deployment Argo images), FTFL-988 (InsightFILE yarn) |
| AMD64-only builds | FTFL-988 (lands on "keep pinning amd64"—flag back if Apple Silicon dev use case exists) |
| "Shift-left enough?" | FTFL-985/986 (Trivy/SAST/secret/dependency gates pre-push) |
| 1 concurrent pipeline / no parallelism / race conditions | FTFL-897 (root cause: `resource_group: staging` lock; investigation-stage, no fix ticket yet) |
| SonarQube timing / npmAuditIgnore | FTFL-986 (removes `\| true`/`allow_failure` silence) |
| "No way to pass image version to tests" | Related to FTFL-991/972 (`STAGING_VALUE_OVERRIDES`/`get_staging_images.sh`)—fixes leaks, not the design gap |
| No SBOM | FTFL-893 (pre-existing, under FTFL-865 epic) |
| Unaddressed remainder (customer release, rollback, monorepo blocking, etc.) | Out of FTFL-971 scope—decide: second epic or backlog |

---

### 3. Pipeline Bottlenecks & Optimisation (Sources A + C)

#### 3.1 Sequencing Principle

Pipeline speed & reliability precede security gates. DORA _Accelerate_ capabilities: 19-min flaky pipeline + security scanning = excruciating feedback loop. CE+ April 2026 imposes a strict 14-day SLA for high/critical patches—a brittle 19-min pipeline makes that mathematically improbable. Toyota Kata: set a pipeline Target Condition ("builds <5min") before a security Target Condition.

#### 3.2 Build Caching (The 19-min bOttleneck)

| Strategy | Mechanism | Impact |
|---|---|---|
| Dependency-first pattern | Copy manifests (`package.json`, `go.mod`) + install before source | Prevents cache invalidation on code changes |
| BuildKit mount caches | `RUN --mount=type=cache` for pkg dirs (e.g. `/root/.npm`) | Persists downloads across ephemeral runners |
| Registry cache backend | `--cache-to=type=registry,ref=…` in ACR | Pulls pre-compiled layers; mitigates no persistent local storage |

```yaml
build-image:
  variables:
    DOCKER_BUILDKIT: "1"
  script:
    - docker buildx build
        --platform linux/amd64,linux/arm64   # confirm multi-arch is a real need
        --cache-from type=registry,ref=$CI_REGISTRY_IMAGE:buildcache
        --cache-to type=registry,ref=$CI_REGISTRY_IMAGE:buildcache,mode=max
        --push -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
```

FTFL-988 root cause: yarn cache not mounted into the Docker build context (625s warm / 1423s cache-miss).

#### 3.3 Merge Skew & GitLab MR Pipeline Routing

- Long-lived feature branches tested against stale trunk → violent merge conflicts. Trunk-based development (merge to main daily) is the DORA fix—requires feature-flag discipline.
- GitLab MR-pipeline gotcha: `$CI_COMMIT_BRANCH` is unavailable in MR pipelines (documented behaviour) → jobs silently run zero tests. Fix with `workflow:rules` on `$CI_PIPELINE_SOURCE == "merge_request_event"`, and use `$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME` in MR context. Disable duplicate branch pipelines while an MR is open to avoid double compute spend.

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      variables:
        GIT_STRATEGY: "clone"          # fresh checkout against target ref
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

test-frontend:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_DEPTH: 0
  before_script:
    - git fetch origin "$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
    - git merge --no-commit --no-ff "origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"

build-frontend:
  cache:
    key:
      files: [package-lock.json]        # invalidates only on lockfile change
    paths: [node_modules/, .npm/]
    policy: pull-push
  script:
    - npm ci --prefer-offline
    - npm run build
```

#### 3.4 Feature Flags (Trunk-Based Prerequisite)

- Hodgson/Fowler taxonomy: Release, Experiment, Ops, Permissioning toggles. Start with Release Toggles only (short-lived, separate deploy from release); avoid Experiment/Permissioning and migration-bearing data-state toggles in month one.
- Stale flags are the 1 failure mode—flag removal must be an explicit Definition-of-Done step.

#### 3.5 Team Topologies / PR Bottleneck

- Single-owner PR approval gate violates "fast flow" (Skelton & Pais). Platform team should be _Platform + Enabling_—self-service templates + policy-as-code—with peers approving standard MRs and automated CI gates (SAST, secret scanning) enforcing baselines. Decentralise only after flaky tests are stabilised.

#### 3.6 DORA Metrics

- 2024/2025 DORA added a 5th metric: Deployment Rework Rate (% of deployments that are unplanned production fixes)—quantifies the merge-skew cost. MTTF→Failed Deployment Recovery Time moved to throughput category.

---

### 4. Security Gates & Shift-Left (Sources A + F)

#### 4.1 Trivy: Report-Only → Blocking Gate

- OWASP DSOMM "Decision Contracts": every control is Block / Warn / Log. Start Trivy in `--exit-code 0` report-only, publish to MR via GitLab SARIF integration for visibility without blocking merges.
- Avoid "security theater": a report-only gate without a pre-defined flip trigger becomes invisible. Flip to blocking (`--exit-code 1`) only after a data-driven trigger: e.g. 14 days without a false positive that would have blocked a legitimate build and the baseline backlog of criticals (KEV-listed / EPSS > 0.088) is cleared. Map accountability via RACI.

```yaml
trivy-scan:
  stage: test
  image:
    name: aquasec/trivy:0.69.7          # confirmed-clean; NOT v0.69.4–0.69.6 (CVE-2026-33634)
    entrypoint: [""]
  script:
    - trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed --format table "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

include:
  - template: Jobs/SAST.gitlab-ci.yml    # complementary static-analysis layer
```

⚠️ Trivy supply-chain caveat: Trivy's own supply chain was compromised (CVE-2026-33634, Mar 2026—malicious commits into 76/77 `aquasecurity/trivy-action` tags, backdoored v0.69.4). Pin CI Trivy usage to commit SHAs, not tags; run ≥v0.69.7.

#### 4.2 Vulnerability Triage: EPSS + CISA KEV (CVSS-blind)

- 7,399 open findings; 51% lack CVSS (NIST halted universal scoring early 2026). CVSS measures theoretical severity, not real-world exploitation → anti-pattern for prioritisation.
- EPSS (FIRST): ML probability of exploitation in next 30 days. CISA KEV: binary known-exploited indicator. Chaining EPSS+KEV can cut urgent workload ~95% while keeping high threat coverage.

| Triage tier | Criteria | Action |
|---|---|---|
| Tier 0 | In CISA KEV | Remediate immediately (non-negotiable) |
| Tier 1 | EPSS > 0.088 | Prioritise in current sprint |
| Tier 2 | High CVSS (7.0–10.0), EPSS < 0.088 | Standard patching cycle |
| Tier 3 | Low CVSS, low EPSS, not in KEV | Defer / accept residual risk |

- Threshold: 0.088 chosen over 0.36 (F1-optimal)—ROC/AUC analysis shows 0.088 keeps 85.6% coverage of exploited vulns while filtering noise. For CVSS-less findings, use SSVC (CISA/CMU decision trees).
- Compliance caveat: NHS DSPT may still lean on legacy CVSS—document EPSS/KEV methodology in risk-acceptance policies to defend the posture in audits.

#### 4.3 Kubescape (K8s posture—Source F)

- CNCF/ARMO open-source platform: config scanning (manifests/Helm/charts), CVE scanning, compliance mapping (NSA-CISA, MITRE ATT&CK, CIS Benchmarks), runtime threat detection, CI/CD integration.
- Positioning vs current stack: Trivy stays the CVE/image engine (deeply wired into Grafana dashboards, VEX repo, CI). Kubescape fills the manifest/Helm misconfig + compliance-posture gap—currently unaddressed ("no scanner in any pipeline anywhere in the estate" for that category, per FTFL-865 notes). Standard "SCA/image + K8s posture" pairing; supports the Gatekeeper phased-enforcement direction (FTFL-859).
- Not yet decided: no evidence Kubescape was evaluated head-to-head in `fitfile-vuln-mgmt-research`—check the scanner-comparison table before adopting.

#### 4.4 SLSA L2 & Supply-Chain (Azure Policy + Ratify)

- Target: SLSA 1→2 (signed provenance, cryptographically signed by hosted build). Azure Policy (Gatekeeper) invalidates generic OPA guidance → use Ratify to verify Cosign/Sigstore keyless signatures + in-toto attestations before pod admission.
- Generate SLSA provenance in GitLab CI with Cosign keyless signing (OIDC); deploy Ratify on AKS; Azure Policy rejects unsigned images.
- Risk: Ratify needs precise OIDC between GitLab and Azure AD (Workload Identity); misconfiguration can lock the platform team out of the cluster.

#### 4.5 CI-to-Azure OIDC (unverified—needs `glab api`)

- K8s-layer Azure Workload Identity is already OIDC/federated-credential (per SoT notes)—but whether GitLab CI runners authenticate to Azure via `id_tokens:`/OIDC is a separate trust boundary, unconfirmed. Verify before applying:

```bash
glab api projects/:id | jq '.ci_forward_deployment_enabled'
glab api projects/:id/job_token_scope | jq '.'
glab ci list --repo fitfile/deployment
```

- OIDC pattern replaces `AZURE_CLIENT_SECRET` with `id_tokens:` → `az login --service-principal --federated-token`, plus a Federated Identity Credential on the Azure App Registration (issuer `https://gitlab.com`, subject `project_path:fitfile/deployment:ref_type:branch:ref:main`).
- Repo topology note: `deployment` repo has a `pipeline/` template dir (`common-jobs.yml`, `verification-pipelines.yml`, `build-pipelines.yml`, `staging-pipelines.yml`, `release.gitlab-ci.yml`)—none locally readable, snippets are suggested additions not diffs.

#### 4.6 Database Migrations in GitOps (ArgoCD)

- Expand/contract migrations may be structurally out of reach short-term. Middle ground: ArgoCD Sync Waves + PreSync hooks—migrations as K8s Jobs annotated `argocd.argoproj.io/hook: PreSync`, never in app pod startup (avoids race conditions/timeouts).
- Defensive PostgreSQL: `SET lock_timeout = '5s';` in migration scripts; `pg_repack` for non-blocking table/index maintenance.

---

### 5. Contract Testing & Release Management (Source D)

#### 5.1 CDC Best Practices

- Robustness principle (Postel's Law): contracts must use type/regex/array matchers, not exact values (except business invariants like enums). Exact values → brittle false negatives.
- Wire semantics over internal models: never reuse DTOs/ORM entities in contract tests—capture actual wire-level HTTP semantics (headers, base paths, auth tokens) via network capture; author payloads as plain JSON/DSL independent of app classes.
- Deep mocking: mock at the lowest boundary (DB/repository/outbound API), not the HTTP controller—controller mocks bypass serialization, middleware, security interceptors, exception handlers → false confidence. Use provider states to manipulate deep state before replay.

#### 5.2 Provider Verification Must Be Explicit

- A consumer contract is meaningless unless the provider verifies it in CI: pull latest contracts, run against a real running provider instance, publish cryptographic verification results back to the broker. Mandatory, automated, never ad-hoc.

#### 5.3 Topologies

- Sync (gRPC/Protobuf): schema ≠ behaviour—contract test behavioural expectations (optional-but-required fields, enum support) over the binary stream.
- Async (Kafka/RabbitMQ/SNS): Hexagonal approach—test the core domain logic's message generation/parsing, not the transport; avoids provisioning brokers in CI.

#### 5.4 CDCT Vs BDCT

| | CDCT | BDCT |
|---|---|---|
| Artifacts | Consumer-generated contract | Consumer contract + provider OpenAPI spec |
| Verification | Dynamic vs running provider | Static in central broker |
| Provider impact | High (deep state + verification runs) | Low (accurate OpenAPI spec) |
| Best for | Deeply coupled internal microservices | Third-party/legacy/rigid-governance APIs |

#### 5.5 Contract Registry & Deployment Gating

- Central broker maintains a Contract Matrix (consumer version × provider version × contracts × verification status × environments). Git SHA as immutable version id (never `latest`/`dev`); publish with branch name too.
- Deployment gate (`can_i_deploy`): before promotion, query broker—"is this version compatible with all partners currently in the target env?"; exit 0 = proceed, non-zero = halt.
- Deployment recording: pipeline posts deployment events (Git SHA + env) synchronously; enables safe rollbacks (never roll back to a version incompatible with current surroundings).

#### 5.6 Decouple Deploy from Release

- Service mesh (Istio) header routing for dark launches: exact/prefix/regex header matches route QA/synthetic traffic to the new version against real prod deps; fault injection for chaos.
- Automated canary (Kayenta): compare canary against baseline (fresh instance of existing code), not long-running prod (JIT/cache warmup skews). Mann-Whitney U test → score; abort+auto-rollback on critical failure; incremental traffic shift. Four phases: data validation → cleaning (NaN handling) → metric comparison → score.
- Feature flags at the app layer: deploy dormant, toggle per segment, instant MTTR measured in ms.

---

### 6. Self-Verifying Alerts / Telemetry (Source E)

#### 6.1 The Core Principle

> "No control ships until it can prove it ran. Every check must emit a positive signal… never merely an absence of errors. Absence of errors is exactly what a dead control produces."

An absence-triggered (log-based) alert cannot distinguish "nothing bad happened" from "the thing that tells me something bad happened is itself broken." The log-based `TrivyImageScanFailed` alert sitting in NoData when healthy is indistinguishable from the log pipeline breaking.

#### 6.2 Dead-Man's-Switch / Watchdog Pattern

- Always-firing synthetic alert: `expr: vector(1)`, routed on a short repeat interval to an external heartbeat receiver (Dead Man's Snitch / owned webhook); the external watchdog raises its own alarm when a check-in is missed—alert path monitored outside the system it monitors.
- Threshold must be ≫ heartbeat interval (e.g. heartbeat 5m, alert if absent 15m) to avoid false-positive fatigue.
- Heartbeats must validate actual success of the control (end-to-end synthetic check), not just script invocation. Emit on both success and failure paths (via `trap … ERR` and `after_script`) so a job that dies silently still surfaces as "expected heartbeat, got none" (e.g. Prometheus `absent()` rule).

```yaml
groups:
- name: watchdog
  rules:
  - alert: Watchdog
    expr: vector(1)
    labels: { severity: critical }
    annotations:
      summary: "Alerting pipeline is broken if this alert stops firing"
```

```yaml
route:
  receiver: dead-mans-switch
  routes:
  - receiver: dead-mans-switch
    match: { alertname: Watchdog }
    repeat_interval: 15m
```

#### 6.3 Mapping to Tickets

| Ticket | Failure mode | Fix shape |
|---|---|---|
| FTFL-938 | Scan jobs fail silently (3,132 log lines over 6 working days undetected) | Positive "I ran, covered N workloads, at time T" signal—not absence-of-error |
| FTFL-942 | Alert in NoData when healthy—indistinguishable from broken | Metric-based alerts: new Critical, threshold crossing, coverage drop, staleness >24h (replace broken log-based ones) |
| Tier 0 exit gate | "72h green" over a weekend the cluster is off → guaranteed false pass | "Three consecutive working days at zero," not wall-clock hours |
| FTFL-893 (related) | CronJob "looked correctly deployed all day and would never have fired once" | Staleness-based heartbeat catches immediately |

Not yet ticketed: a watchdog/heartbeat rule on the scan job itself—fires only when `trivy_resource_configaudits` (or equivalent coverage metric) hasn't updated within an expected window. Sits alongside FTFL-942, not inside it.

#### 6.4 Telemetry Signal Skeleton

```yaml
.telemetry_signal: &telemetry_signal |
  send_heartbeat() {
    local job_name="$1" count="$2" status="$3"
    curl -sf -X POST "$TELEMETRY_ENDPOINT/heartbeat" \
      -H "Authorization: Bearer *" \
      -d "{\"job\":\"$job_name\",\"ran_at\":\"$(date -u +%FT%TZ)\",\"items_checked\":$count,\"status\":\"$status\"}" \
      || echo "WARNING: telemetry heartbeat failed for $job_name" >&2
  }
```

---

### 7. Prioritised Action Plan (Source A, 3 Phases)

#### Phase 1—Do Next (0–2 Weeks)

1. Fix GitLab CI pipeline routing—`workflow:rules` on `$CI_PIPELINE_SOURCE == "merge_request_event"`; use `$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME` in MR context. _(Fixes the zero-tests-on-MR incident; risk: duplicate pipelines if rules nested wrong.)_
2. Dead Man's Switch for critical CronJobs (Renovate, health checks)—heartbeat on successful completion; alert on absent heartbeat > interval. _(Addresses "silence as health" failure mode.)_
3. Transition Trivy to report-only MR gate—`--exit-code 0` + SARIF to MR. _(Baseline detection skeleton without halting the 19-min pipeline; define the data-driven flip trigger.)_

#### Phase 2—This Quarter

1. Adopt EPSS & KEV triage—filter 7,399 findings: KEV fix immediately, EPSS > 0.088 prioritise, rest acknowledge/log. _(Fixes CVSS-blind triage paralysis; document in risk-acceptance for DSPT.)_
2. Optimise Docker BuildKit caching—dependency-first layers, `--cache-to=type=registry`, multi-stage. _(Attacks 19-min bottleneck → enables 14-day CE+ patching SLA; risk: registry bloat from cache manifests.)_
3. Isolate migrations via ArgoCD PreSync hooks + PostgreSQL `lock_timeout`. _(Decouples schema from deploy; risk: degraded ArgoCD app if hook fails—need rollback hooks.)_

#### Phase 3—Structural / Long-Horizon

1. Release Toggles for trunk-based dev—centralised flag platform, start with low-risk frontend changes. _(Fixes merge skew; risk: stale-flag debt—enforce removal in DoD.)_
2. Decentralise PR approvals—platform team builds automated compliance checks; peers approve standard MRs. _(Removes queueing bottleneck; only after flaky tests stabilise.)_
3. SLSA L2 via Azure Policy + Ratify—Cosign keyless in GitLab CI, Ratify admission on AKS. _(Respects existing Gatekeeper architecture; risk: OIDC misconfiguration locks out the cluster.)_

---

### 8. Key Numbers & One-Liners

- 19:02—frontend-only pipeline run time (FTFL-988: 625s warm / 1423s cache-miss)
- 7,399—open vulnerability findings; 51% without CVSS
- ~95%—urgent-workload reduction from EPSS+KEV chaining
- 14 days—CE+ 2026 SLA for high/critical patches
- 0.088—chosen EPSS threshold (85.6% coverage of exploited vulns)
- 5th DORA metric—Deployment Rework Rate (quantifies merge skew)
- 1 concurrent pipeline—`resource_group: staging` lock (FTFL-897)

---

_Consolidated 2026-08-26 from 6 inbox captures. Originals removed from `00_Inbox/` (recoverable via git history)._

### [[Dev events to trigger on]]

- Change file
- Save file changes
- commit set of changes
- Create Branch
- push set of commits on Branch
- push secondary set of commits on Branch
- Comments on diff
- Create MR
- Approve MR
- Merge MR into main
- Pipeline job failure
- Pipeline failure
- Pipeline job Success
- Pipeline Success
- Merge into main Success
- New HEAD on main
- Push new images to ACR
- Customer specific tag moved

### Pipeline Improvement Synthesis Plan

#### Overview

This document synthesizes the various streams of work, audits, and team discussions aimed at transforming the FITFILE CI/CD Pipeline. It aggregates findings from the team's Miro board sessions (Release Process + Vuln Management boards), the DORA-driven [[Pipeline_Improvement_Proposal]], the "Nightmare Pipeline" quality ethos, and the FTFL-865 Vulnerability Management epic—including the 2026-08-24 refinement call with Oliver Rushton, Pavlo Kotov and Weronika Jastrzebska.

The goal is to turn the pipeline into a "purifying gauntlet"—a strict falsification mechanism that acts as the single, automated, and secure path to production, while remaining highly performant and developer-friendly. As of 2026-08-24 the estate is at detect-only maturity: we have visibility into problems, no gate that stops them, no automated remediation loop, and—the sharper finding from this week's work—no reliable way to know whether our controls are even running.

---

#### 1. The Core Philosophy & Goals

- The "Nightmare" Gauntlet: code entering the pipeline must be proven ready. The pipeline should aggressively test, lint, and validate to ensure only code of supreme quality reaches production ([[Nightmare pipeline]]).
- A Falsification Mechanism, not just a build tool: per [[Pipeline_Improvement_Proposal]], the pipeline's job is to try to prove a change is _unfit_ for production. If it survives, we trust it. It must be the only automated route to production.
- DORA Metrics as North Star: Lead Time for Changes (<1 hour), Deployment Frequency (on-demand), Change Failure Rate (near zero), and MTTR (minutes).
- Decoupling Deployment from Release: continuous deployment of technical artefacts, gated for business release by feature flags—not by holding back a merge.
- Evidence-based improvement (Toyota Kata): establish baseline → form a hypothesis → run a scoped experiment → measure → adopt or discard. Applies equally to pipeline architecture and to security controls (see §3).
- A control must prove it ran. This week's vulnerability-management work surfaced a principle that generalises to the whole pipeline: _absence of an error is not evidence of health._ Every gate, job, and alert should emit a positive signal ("I ran, I covered N things, at time T"), not just silence when nothing goes wrong. See §3.2 for why this matters—it cost the team a fully re-opened epic this week.

---

#### 2. Structural & Architectural Improvements

Source: [[fitfile_pipeline_notes]] (Miro: Release Process board) and [[Pipeline_Improvement_Proposal]].

##### A. Solving "Merge Skew" & Big Batches

- The blocker: developers wait for a full feature before merging → long-lived branches → conflicts and race conditions when several land at once, because the pipeline validated each in isolation against a now-stale trunk.
- Trunk-Based Development: commit to `main` at least daily. Relies on Feature Flags being in place first.
- Feature Flags: experimental toggles so incomplete work merges safely without reaching customers. Currently not visible enough in the Feature Branch stage—a named problem in the Miro session.
- Merge Trains / Merged-Results Pipelines: run CI against the _merged_ result, not the source branch, to stop broken-trunk races. Directly addresses the Merge Train stage's own top complaint: "concurrent pipelines cause race conditions."

##### B. Pipeline Efficiency & Speed

- DAG YAML Architecture: replace rigid stages with `needs:`-based graphs for parallel execution and fail-fast feedback.
- Build Caching: dedicated GitLab runners—named as a Quick Win in the Miro session, and the direct fix for two independently-reported problems: no build cache at Merge Train _and_ at Staging Release, plus the AMD64-only ACR rebuild bottleneck.
- Test Parallelism: parameterise integration tests to run concurrently—removes the single-pipeline-at-a-time bottleneck that the team flagged as a root, critical problem (alongside "pipelines are slow", "pipelines are flakey", "builds are slow").

##### C. Testing & Reliability

- API tests are flakey and have low coverage, alongside Data Pipeline integration tests—named directly in the Merge Train stage.
- No resource limits on integration test pods—a likely contributor to the flakiness; test pods competing for cluster resources produce non-deterministic failures that get misread as code defects.
- No way to pass image version to tests—tests currently rely on the ArgoCD sync rather than an explicit version, which weakens the mapping between "this pipeline run" and "this artefact under test."
- Write more tests on the pipeline itself—a Quick Win from the Miro session; the pipeline's own YAML/scripts are currently untested code running in production.

##### D. Environment & Deployment Management

- Ephemeral Environments per branch, to raise testing confidence before merge.
- Configuration as Code: move customer-specific config into its own repositories so config-only changes don't require a full release—directly fixes the Customer Release stage's "config changes require a new release" problem.
- Publishing Charts to ACR with proper versioning—charts are currently not built/versioned there at all.
- ACR push secret expiry breaks the pipeline and requires manual intervention—a known Staging Release failure mode with no automated renewal.

##### E. Rollback & MTTR

- No rollback procedure when a migration is involved—flagged as a Production Release problem and the single biggest risk to the MTTR DORA metric. A pipeline with fast deploys but no rollback path for stateful changes cannot hit "minutes to restore service."
- Per-environment config drift: each environment differs slightly, making the blast-radius of any upgrade hard to assess consistently—compounds rollback risk.
- No inbound connectivity to private clusters without a bastion—slows incident response by design; worth weighing against the security benefit when scoping MTTR work.

##### F. Visibility & Process

- Three disparate ways to deploy (infra / platform / application)—no single mental model for "how does code get to prod."
- No SBOM, no release notes—both are prerequisites for two things this document cares about: supply-chain attestation (§3) and being able to answer "what actually changed" during an incident.
- Manual, per-customer tagging with no overview of client state—a scaling risk as customer count grows.
- Single-owner review gates drag down Lead Time (per [[Pipeline_Improvement_Proposal]])—worth pairing with the trunk-based/small-batch work in §2A rather than solving in isolation.

---

#### 3. Security & Vulnerability Management—FTFL-865

Epic: [FTFL-865](https://fitfile.atlassian.net/browse/FTFL-865) (In Progress, High, due 31 Aug 2026). Sources: [[FTFL-865 Problem Definition — Secure or Not Looking]], [[FTFL-865 Vulnerability Management — Refinement Brief 2026-08-24]], [[Vulnerability Management Implementation Plan (FTFL-865)]], [[Vulnerability Management Audit - Trivy, VEX, Renovate (Round 1)]].

##### 3.1 The Reframed Problem

> We cannot tell the difference between "we are secure" and "we are not looking."

The issue isn't the size of the backlog (7,399 findings as of 2026-08-24). It's that every safety mechanism we own can fail silently—several currently are—and a control that reports success while doing nothing is worse than no control: it consumes attention _and_ manufactures false confidence. This is an epistemics problem, not a capacity problem, and epistemics problems get _worse_ when you throw manual effort at them, because you accumulate confidence that was never earned.

The exhibit—nine mechanisms found silently failing in two weeks, none raising an alarm:

| What it reported | What was actually true |
|---|---|
| Dashboard showing full severity counts | Scan jobs erroring continuously—3,132 failures across six working days |
| Tier 0 gate "scan jobs green for 72h" passed | The check window spanned a weekend when the cluster was off—it could only ever return zero |
| No alerts firing | The alert sits in `NoData` when healthy—indistinguishable from the log pipeline being broken |
| Terraform apply succeeded | The running pod served the old config for ~1.5h; a ConfigMap change restarts nothing |
| Export CronJob "deployed and healthy" | Scheduled at 02:17 on a cluster that sleeps at night—had never fired once |
| Merge requests "passing CI" | `ude-cli` MRs created no pipeline at all—a Rust `rsa` security update merged with zero tests |
| Renovate "configured" against our private registry | `DOCKER_REGISTRY_PASSWORD` was never set—it has never once authenticated |
| Trivy "scanning our images clean" | Third-party-repo packages are skipped by design—they don't show as Unknown, they don't appear at all |
| Gates/dashboards keyed on Critical/High | 51% of findings carry no CVSS score, so they're invisible to every control we've designed |

The operating rule this implies: every check must emit a positive signal—"I ran, I covered N workloads, here is when"—never merely an absence of errors. This single rule would have caught all nine failures above.

##### 3.2 Live Baseline (2026-08-24, ~10:45 UTC, Staging Cluster)

| Severity | Count | 14 Aug baseline | Change |
|---|---:|---:|---:|
| Critical | 195 | 213 | −18 (−8%) |
| High | 1,487 | 1,731 | −244 (−14%) |
| Medium | 1,496 | 1,774 | −278 |
| Low | 424 | 544 | −120 |
| Unknown | 3,797 | 3,779 | +18 (flat) |
| Total | 7,399 | 8,041 | −642 (−8%) |

Two facts worth carrying into any planning conversation:

1. Ten days of the whole team's remediation effort moved Critical by 18 findings. 1,682 findings sit at High or above—there is no plausible headcount at which manual triage closes that gap.
2. `Unknown` is 51% of the estate—larger than Critical+High+Medium+Low combined. NIST stopped universally scoring CVEs in April 2026, so for most of this bucket a severity is _never coming_. Every gate and SLA in the epic is currently keyed on CVSS tiers, meaning it is silently undefined for over half the findings. [FTFL-954](https://fitfile.atlassian.net/browse/FTFL-954) (characterise the Unknown bucket) is the cheapest way to de-risk everything downstream.

Active regression (found 2026-08-24, not yet root-caused): [FTFL-938](https://fitfile.atlassian.net/browse/FTFL-938)—the VEX-metadata `EOF` failure killing scan jobs—was closed Done on 17 Aug but has recurred every working day since (~3,100 log lines, 285 today alone). It was closed on a weekend-window Loki query that could only ever return zero, because the staging cluster is off Fri 20:00–Mon 06:00. Do not re-apply a fourth patch—the epic's own instruction is that recurrence means the working theory is incomplete and needs reopening properly.

##### 3.3 Payoff-ordered Plan

From [[Vulnerability Management Implementation Plan (FTFL-865)]], calibrated against real effort (FTFL-855's estimate was off by a day plus an incident—treat all effort bands as approximate).

Tier 0—Restore the skeleton (nothing below works without it)

| # | Action | Ticket | Effort |
|---|---|---|---|
| 0.1 | Fix the VEX metadata EOF failure killing scan jobs | [FTFL-938](https://fitfile.atlassian.net/browse/FTFL-938) (reopened) | 0.5–2 d |
| 0.2 | Fix `TrivyImageScanFailed` alert to match real log output | [FTFL-939](https://fitfile.atlassian.net/browse/FTFL-939) | 2 h |
| 0.3 | Durable report retention beyond 24h TTL | [FTFL-893](https://fitfile.atlassian.net/browse/FTFL-893) | 2–4 d |
| 0.4 | Validation CI on `vex-repository` (single point of failure for every scan job) | [FTFL-940](https://fitfile.atlassian.net/browse/FTFL-940) | 1 d |

Gate: scan jobs green for 72h _measured on a live-cluster window, not a weekend_, plus coverage stable at ~90 workloads, before Tier 1 starts.

Tier 1—Highest payoff per unit effort

| # | Action | Ticket | Why |
|---|---|---|---|
| 1.1 | CI scan gate, report-only first (`--exit-code 0`, JSON artefact) | [FTFL-856](https://fitfile.atlassian.net/browse/FTFL-856) | Zero CI scanning exists estate-wide; report-only ships into an uncleared backlog without breaking every pipeline, and produces the durable inventory other tickets need |
| 1.2 | EPSS + CISA KEV prioritisation | [FTFL-947](https://fitfile.atlassian.net/browse/FTFL-947) | Best noise-reduction available; cuts an actionable list by an order of magnitude with no per-CVE human analysis |
| 1.3 | Confirm CI actually runs on every repo in scope | [FTFL-891](https://fitfile.atlassian.net/browse/FTFL-891) | A gate is decoration on a repo whose MRs create no pipeline (true of `ude-cli` until 13 Aug) |
| 1.4 | Renovate `vulnerabilityAlerts` nesting fix | [FTFL-894](https://fitfile.atlassian.net/browse/FTFL-894) | Root-level `packageRules` can't constrain security updates—Renovate's `force` object overrides them |
| 1.5 | Transitive dependency overrides | [FTFL-895](https://fitfile.atlassian.net/browse/FTFL-895) | Hard prerequisite before 1.1 goes blocking, or transitive-only findings become unfixable build failures |
| 1.6 | Fix dashboard's 3 dead metric rows + threshold calibration | [FTFL-941](https://fitfile.atlassian.net/browse/FTFL-941) | `configaudits`/`rbacassessments`/`exposedsecrets` show zero series despite chart defaults being on |
| 1.7 | Metric-based alerts (new Critical, coverage drop, staleness) | [FTFL-942](https://fitfile.atlassian.net/browse/FTFL-942) | Nothing currently alerts on the vulnerabilities themselves, only on log strings |

Tier 2—Structural, higher effort, still worth it

| # | Action | Ticket | Notes |
|---|---|---|---|
| 2.1 | Base-image minimisation (distroless/Chainguard) | [FTFL-863](https://fitfile.atlassian.net/browse/FTFL-863) | Ranked _above_ the source report's own Tier 3—it's the only lever that reduces the CVE count rather than reclassifying it (>80% reduction observed). Pilot on `ff-test-a` (102 Criticals) or `ohdsi` (60) |
| 2.2 | Flip the CI gate to blocking | FTFL-856 (part 2) | Only once the inventory is clear enough not to go permanently red; needs 1.2 + 1.5 landed |
| 2.3 | Severity-tier recording rules | [FTFL-860](https://fitfile.atlassian.net/browse/FTFL-860) | Keep `metricsVulnIdEnabled` on; do before multi-cluster rollout (9,547 series → 30k+) |
| 2.4 | GitOps for security tooling + Helm-values drift lockdown | [FTFL-858](https://fitfile.atlassian.net/browse/FTFL-858), [FTFL-862](https://fitfile.atlassian.net/browse/FTFL-862) | Real fix is _who has write access outside GitOps_, not a values-file tool |
| 2.5 | Extend trivy-operator to testing, then production | [FTFL-945](https://fitfile.atlassian.net/browse/FTFL-945) | Production is currently entirely unscanned |
| 2.6 | Cosign image signing + attestation in CI | [FTFL-861](https://fitfile.atlassian.net/browse/FTFL-861) | Genuinely useful; sequence after Tier 1—signing images whose contents we can't yet reason about is backwards |
| 2.7 | Automated remediation loop (Trivy findings → Renovate/issue) | [FTFL-857](https://fitfile.atlassian.net/browse/FTFL-857) | Needs 0.3 and 1.5 first, or it generates unactionable tickets |

Tier 3—Deferred / re-scoped / explicitly rejected

| Idea | Verdict |
|---|---|
| Gatekeeper phased enforcement ([FTFL-859](https://fitfile.atlassian.net/browse/FTFL-859)) | Re-scope first—it's Azure Policy for AKS, not standalone Gatekeeper; hand-written ConstraintTemplates get reconciled away |
| OWASP Dependency-Track | Defer—needs CI-generated SBOMs we don't yet produce |
| Policy Reporter UI | Skip—duplicates the Grafana dashboard once §1.6 lands |
| Grype as second scanner ([FTFL-864](https://fitfile.atlassian.net/browse/FTFL-864)) | Defer—can't reliably operate the one scanner we have yet |
| Snyk / Wiz / JFrog Xray | No—cost/weight not justified at current team size |
| `additionalVulnerabilityReportFields` | Defer to whatever consumes it—grows etcd objects with no current reader |
| SLSA L3 / Ratify / in-toto provenance | Far future—realistic ambition is SLSA 2–3; we're not at 1 |
| `.trivyignore.yaml` with `expired_at` | Adopt opportunistically alongside 1.1—cheaper than VEX for local, time-boxed suppressions |

##### 3.4 Refinement Call outcome—2026-08-24, 13:00

Attendees: Leon Ormes, Oliver Rushton, Pavlo Kotov, Weronika Jastrzebska.

- Moved into this sprint (Selected for Development): FTFL-858, FTFL-857, FTFL-956 (priority Medium → High), FTFL-864 (Lowest → Medium), FTFL-863, FTFL-893.
- New tickets raised, parented to FTFL-865: FTFL-966 (reachability spike), FTFL-967 (upstream-won't-fix suppression policy), FTFL-968 (compliance scope owner), FTFL-969 (trivy-system footprint / cost).
- FTFL-938 reopened in the call; FTFL-942 promoted off Low given the "no signal read as health" pattern has now cost a full week three separate times (Terraform apply, CronJob, this alert).
- FTFL-863 (distroless/Chainguard) explicitly agreed as an _opportunistic, scoped pilot_ rather than a full migration—effort: opportunistic; impact: improves detection coverage on highest-risk images without the operational overhead of a fleet-wide second scanner. (Sourced against "Trivy vs Grype 2026 Buyer Comparison" and "Container Security Scanning in 2026.")

##### 3.5 The compliance driver—flag It, Don't Solve it

Unresolved: is FitFile in scope for NHS DSPT / DTAC / Cyber Essentials Plus as an IT supplier? This is a question for whoever holds the data-processing agreements, not something platform work resolves—but it reorders the whole quarter if the answer is yes:

- CE+ (from April 2026): mandates a 14-day remediation window for anything CVSS ≥7.0. We have 1,682 findings at that level today—manual triage cannot clear that inside 14 days by any means. Promotes FTFL-895, FTFL-863, FTFL-857 from "worth doing" to load-bearing.
- DSPT: requires a _written_ vulnerability-management policy with an exception-approval workflow—a document, not automation. We currently have automation and no document.
- DTAC: requires an annual external penetration test showing nothing at CVSS ≥7.0—nothing in this plan provides that.

Action: name an owner for the scope question before it silently gates the rest of the platform work.

---

#### 4. Best-Practice Alignment

Mapping the above against recognised frameworks, so gaps are named against an external standard rather than internal opinion.

| Framework | What it asks for | Where we stand |
|---|---|---|
| DORA / _Accelerate_ (Forsgren, Humble, Kim) | Trunk-based dev, CI, deployment automation, loosely-coupled architecture, monitoring & observability, as the drivers of the four keys | Baseline not yet instrumented (§1); trunk-based dev blocked on feature flags (§2A); monitoring exists but has proven it can lie (§3.1) |
| Continuous Delivery (Humble & Farley) | The deployment pipeline is the _only_ route to production, and its job is to falsify releasability | Three disparate deploy paths currently exist (§2F)—violates the "only route" principle directly |
| OWASP DevSecOps Maturity Model | Security shifts left through the pipeline stages, not bolted on at the end | Zero CI scanning estate-wide today (§3.3, Tier 1); this document's own plan is the shift-left move |
| NIST SSDF / SLSA (supply-chain integrity) | Provenance, signed artefacts, SBOM, verified builds | No SBOM generated in CI (§2F); Cosign signing scoped but deliberately sequenced after detection is trustworthy (§3.3, 2.6); realistic target is SLSA 1→2, not L3 |
| Toyota Improvement Kata | Hypothesis-driven, measured experiments over top-down mandates | Explicitly adopted in [[Pipeline_Improvement_Proposal]] §3; the FTFL-865 reframing (§3.1) is this pattern applied to security |
| Dead-man's-switch / positive-signal monitoring (SRE practice) | A healthy system announces itself; the alarm is silence _changing_, not the default state | Directly the gap found this week (§3.1)—`NoData` currently means both "healthy" and "broken" |

---

#### 5. Prioritised Roadmap

Sequenced by dependency and payoff, merging the pipeline structural work with the FTFL-865 tiers. Effort bands are approximate.

1. Now—Tier 0 (security skeleton): reopen FTFL-938 properly (root cause, not a fourth patch), fix the alert that should have caught it (FTFL-939), durable retention (FTFL-893), VEX repo validation CI (FTFL-940). _Nothing in vulnerability management is trustworthy until this gates green on a live-cluster window._
2. Now—parallel, independent of Tier 0: instrument DORA baseline metrics; characterise the Unknown vulnerability bucket (FTFL-954/955) against the already-banked archive—no cluster access needed, de-risks everything downstream.
3. Next—pipeline quick wins: dedicated GitLab runners for build cache; parameterise integration tests for parallelism; publish charts to ACR with versioning; move customer config to its own repos.
4. Next—Tier 1 security: audit CI coverage across all repos (FTFL-891) _before_ flipping any gate; ship the CI scan gate report-only (FTFL-856, `--exit-code 0`); EPSS/KEV prioritisation (FTFL-947, after Unknown is characterised); fix Renovate's `vulnerabilityAlerts` nesting (FTFL-894).
5. Next—one trunk-based-dev experiment: pick one upcoming feature, add a feature flag, and measure Lead Time / Change Failure Rate against baseline for two weeks (Kata-style, per §1 and §4).
6. Later—Tier 2 security + structural pipeline work: distroless pilot on highest-CVE service (FTFL-863); flip the CI gate to blocking once inventory is clear (FTFL-856 part 2); Cosign signing (FTFL-861); merge trains; ephemeral environments; GitOps lockdown for security tooling.
7. Ongoing: name an owner for the NHS DSPT/DTAC/CE+ scope question—its answer changes the priority order of steps 4 and 6 materially, so don't let it sit unowned.
8. Ongoing: build a rollback procedure for migration-bearing releases—currently the single largest MTTR risk and not yet on any tier above.

---

#### 6. Open Threads

Carried forward from source notes—none of these are established yet, and none should be silently assumed either way:

- Root cause of the FTFL-938 EOF regression—not yet found; the local infra repo clone was behind master at time of investigation.
- Does trivy-operator support `--epss`/`--kev` natively, or is EPSS/KEV CLI-only? Determines whether FTFL-947 rides on the operator or on the CI gate (FTFL-856).
- Why do `trivy_resource_configaudits` / `trivy_role_rbacassessments` / `trivy_image_exposedsecrets` show zero series despite chart defaults enabling them—likely the same root cause as the scan-job failures, but unverified.
- What does Kubescape actually cover, and does it overlap trivy-operator enough to retire one?
- NHS DSPT/DTAC/CE+ applicability—owner not yet named (§3.[[FitFile CI_CD Pipeline — Consolidated Notes]]actices Research Prompt]]—deep-research prompt built from this document, for sourcing external best-practice recommendations
- [[fitfile_pipeline_notes]]—Miro Release Process board, raw notes
- [[Pipeline_Improvement_Proposal]]—DORA-driven proposal and Kata methodology
- [[Nightmare pipeline]]—quality ethos
- [[FTFL-865 Problem Definition — Secure or Not Looking]]—the epistemics argument
- [[FTFL-865 Vulnerability Management — Refinement Brief 2026-08-24]]—ROI ranking and call outcome
- [[Vulnerability Management Implementation Plan (FTFL-865)]]—payoff-ordered tickets
- [[Vulnerability Management Audit - Trivy, VEX, Renovate (Round 1)]]—current-state audit
- Epic: [FTFL-865](https://fitfile.atlassian.net/browse/FTFL-865)

## Research Brief: Building a Best-Practice CI/CD Pipeline for FitFile

### Who You're Advising

FitFile is a small platform engineering team (single-digit reviewers, one release

manager) running a GitLab-based CI/CD pipeline for a set of application and data

services on AKS, deployed via ArgoCD and Terraform Cloud. Among the workloads is

an OHDSI-based health data pipeline, which puts FitFile in scope (unconfirmed) for

UK NHS supplier security frameworks—DSPT, DTAC, and Cyber Essentials Plus. Treat

this as a real engineering organisation, not a greenfield exercise: every

recommendation needs to work for a team this size, not just a FAANG-scale org.

### Current State (Verified, not aSpirational)

Pipeline architecture today:

- Stage-by-stage GitLab pipeline (not a DAG); Local Dev → Feature Branch → Merge
  Train → Staging Release → Production Release → Customer Release.
- No trunk-based development—long-lived feature branches are the norm, causing
  "merge skew": branches conflict/break when finally merged because they were
  tested in isolation against a now-stale trunk.
- Feature flags exist but aren't consistently used or visible.
- One concurrent pipeline at a time; no build cache anywhere; all ACR builds are
  AMD64-only, forcing rebuilds; frontend-only pipeline takes ~19 minutes.
- API and data-pipeline integration tests are flaky, low coverage, run without
  resource limits on their pods, and can't be pointed at a specific image version
  (tests rely on the ArgoCD sync state instead).
- Three disparate ways to deploy (infra / platform / application) with no unified
  model.
- No SBOM, no release notes, no rollback procedure for migration-bearing
  production releases.
- Single-owner PR approval gate is a queueing bottleneck.
- Per-customer deployment is manually tagged with no fleet-wide visibility;
  customer-specific config changes currently require a full release.

Security / vulnerability management today (the sharper finding):

- Zero CI-stage vulnerability scanning anywhere in the estate—detection only
  happens post-deploy, in-cluster, via trivy-operator.
- 7,399 open findings (195 Critical, 1,487 High, 1,496 Medium, 424 Low, 3,797
  Unknown/unscored). Ten engineer-days of manual remediation moved Critical by 18
  findings—manual triage provably does not converge against this volume.
- 51% of findings carry no CVSS score at all (NIST stopped universal CVE scoring
  in April 2026) and every planned gate/SLA is currently keyed on CVSS tiers—
  meaning it's undefined behaviour for over half the backlog.
- Renovate has never successfully authenticated to the private registry
  (credential was never set), so no FitFile-built image has ever had automated
  dependency remediation.
- A recurring, still-unexplained scan-job failure (VEX metadata parse error) was
  marked "fixed" against a 72-hour health check that spanned a weekend when the
  cluster is powered off—the check could only ever return a false positive.
- Nine separate control-failure incidents were found by hand in the last two
  weeks (a Terraform apply that "succeeded" without restarting the affected pod;
  a CronJob scheduled for a time the cluster is asleep; an alert that reads
  identically whether the system is healthy or the monitoring pipeline itself is
  broken; a merge request that ran zero tests because GitLab doesn't set
  `$CI_COMMIT_BRANCH` on MR pipelines; etc.). None of the nine tripped any alert.
  The working principle this produced: every control must emit a positive
  "I ran, over N things, at time T" signal—absence of an error is not evidence
  of health.
- Gatekeeper is deployed as Azure Policy for AKS, not a standalone install, which
  invalidates most generic "add a ConstraintTemplate" admission-control guidance.

### What I Already have—don't Re-derive This

I already have an internal synthesis document covering: a payoff-ordered

implementation plan (Tier 0 "restore the detection skeleton" → Tier 1 CI scan

gate + EPSS/KEV prioritisation → Tier 2 base-image minimisation, Cosign signing,

GitOps lockdown → Tier 3 deferred items like Dependency-Track and SLSA L3), a

DORA-metrics baseline goal, and a rough mapping to _Accelerate_, _Continuous

Delivery_, the OWASP DevSecOps Maturity Model, NIST SSDF/SLSA, and Toyota Kata.

I don't need you to re-explain what DORA's four keys are or summarise these

frameworks in the abstract—I need you to apply them to this specific

situation and tell me what I'm getting wrong, missing, or under-weighting.

### What I want from You

Do deep research across the best available industry sources—books,

canonical papers, and high-quality practitioner content, e.g.:

- _Accelerate_ (Forsgren, Humble, Kim) and the underlying DORA research /
  State of DevOps reports—especially the 24 capabilities model, not just the
  four keys
- _Continuous Delivery_ (Humble & Farley)—deployment pipeline as the sole path
  to production, environment/config management, release vs. deployment
- _The DevOps Handbook_ (Kim, Debois, Humble, Willis)
- _Site Reliability Engineering_ and _The Site Reliability Workbook_ (Google)—
  especially on monitoring philosophy, error budgets, and alerting design
- _Building Secure & Reliable Systems_ (Google)
- _Team Topologies_ (Skelton & Pais)—team-shape implications for a
  single-reviewer bottleneck and platform-vs-stream-aligned team boundaries
- Trunk-Based Development literature (trunkbaseddevelopment.com, Paul Hammant)
  and feature-flag practice guides (Pete Hodgson / Martin Fowler on feature
  toggles) for teams that haven't done this before
- SLSA framework documentation, in-toto, and sigstore/Cosign guidance, for
  realistic incremental supply-chain security (we're targeting SLSA 1→2, not 3)
- NIST SSDF and the OWASP DevSecOps Maturity Model, applied to a detect-only
  estate moving to shift-left
- EPSS and CISA KEV documentation/best practice for vulnerability
  prioritisation at scale, as an alternative to CVSS-only triage
- Toyota Kata (Rother) as applied to engineering process change, if you have
  good secondary sources on this in a software context

### Specific Questions to Answer

1. Sequencing challenge. Given a team this size can't do everything at once,
   what does the literature say should come first: fixing pipeline speed/
   reliability (merge trains, build cache, trunk-based dev), or fixing the
   security detection layer? Are these genuinely independent, or does one
   materially de-risk the other in a way I'm not seeing?
2. The "control must prove it ran" principle. Is this a recognised pattern
   (dead-man's-switch monitoring, synthetic checks, heartbeat monitoring) with
   established implementation guidance? What's the SRE-literature-grade way to
   design alerting so silence-as-health failure modes like the nine we found
   can't recur—and where does this pattern have known failure modes of its
   own (alert fatigue, false positive heartbeats)?
3. Trunk-based dev without existing feature-flag discipline. What's the
   realistic adoption path (per Fowler/Hodgson and _Accelerate_) for a team
   that has flags but doesn't consistently use them—what's the first
   experiment to run, and what commonly goes wrong in month one?
4. CVSS-blind vulnerability triage. With 51% of findings unscored, is
   EPSS+KEV-first triage (deprioritising raw CVSS) actually the industry-
   recommended approach at our scale, or is there a better-regarded alternative
   (e.g., reachability analysis, exploit-maturity scoring, risk-based
   frameworks like FAIR) we should be considering instead or in addition?
5. Report-only gates. Is shipping a CI security gate in `--exit-code 0`
   report-only mode before flipping it to blocking a widely-endorsed pattern,
   or does the literature warn this tends to never get flipped on? What
   conditions/triggers does good practice suggest for the flip?
6. Rollback for migration-bearing releases. What do _Continuous Delivery_
   and modern practice recommend for teams that can't yet do zero-downtime
   expand/contract migrations everywhere—is there a credible middle ground
   short of full blue/green + migration choreography?
7. What am I not asking about? Given everything above, what's a
   well-regarded practice (progressive delivery/canary releases, chaos
   engineering, policy-as-code, DORA's "loosely coupled architecture"
   capability, database change management, incident review practice, etc.)
   that this brief doesn't mention but that the sources above would flag as a
   gap?

### Output Format

For each recommendation:

- The recommendation, stated concretely enough to turn into a ticket.
- Source, with enough specificity to go re-read the original (book +
  chapter/concept, not just an author name).
- Why it applies here, tying it to a specific fact from "Current state"
  above—not generic advice.
- Where it might be wrong for us, given our team size, stack, or the
  compliance uncertainty (NHS DSPT/DTAC/CE+ scope not yet confirmed).

Group recommendations into: Do next (0–2 weeks), Do this quarter,

Structural / long-horizon. Flag anywhere your sources genuinely disagree

with each other (e.g., the internal report I already have found two of its own

source documents contradicting each other on whether to enable a metrics flag—

I want to know if that kind of tension shows up in canonical sources too, not

just internal ones).

### Option (A): Parallel rEsource gRoups over a sMall fIxed pOol

Idea: Replace the single `testing` lane with N persistent, pre-warmed lanes (`testing`, `testing-2`, `testing-3`, …), each with its own ArgoCD Application, namespace, and MSSQL instance. Assign each merge-train run to a lane; only MRs sharing a lane serialize.

Why "pre-warmed" matters here: because `testing`'s stack includes a stateful MSSQL deploy + seed-data job with an 18-retry startup probe, spinning a lane up cold would add real minutes to every pipeline. A fixed pool sidesteps that—lanes sit warm and idle between runs, same as `testing` does today.

The GitLab mechanics problem: `resource_group:` can only reference predefined/project/group CI variables—not a value computed in an earlier job's script (GitLab discards script-computed variables before the resource group is registered). So `resource_group: staging-lane-$LANE` can't be set from a dotenv artifact the way `STAGING_VALUE_OVERRIDES` is today. Two ways around it:

- Static regex assignment: bucket by `$CI_MERGE_REQUEST_IID` using `rules:` regex matches (e.g. 3 job variants, each gated on the last digit of the IID, each with a literal `resource_group: staging-lane-N`). Ugly but zero new infra.
- Dynamic child pipeline: a prep job computes the lane and writes a generated `.gitlab-ci.yml` fragment as an artifact (with the resource_group baked in as a literal string), then `trigger: include: artifact:` runs that generated file instead of the static `staging.gitlab-ci.yml`. Cleaner, and this repo already generates dynamic content via scripts (`scripts/argo-render`, `scripts/render.sh`), so it's a natural extension of an existing pattern.

Implementation steps, in order:

1. `deployment` repo: duplicate `ffnodes/fitfile/testing/` → `ffnodes/fitfile/testing-2/` (and `-3` if going to 3 lanes), with distinct `namespace:`/`deploymentKey:` values, distinct MSSQL PVCs, distinct Auth0/DNS hostnames where the current script hardcodes `testing-argocd.fitfile.net` / `testing-argo-workflows.fitfile.net`.
2. Register the new ArgoCD Applications for these lanes (find/extend whatever currently registers `testing` —I did not locate this; likely Terraform via `terraform-fitfile-central-services-consumer` or a manual `argocd app create`, needs confirming before this step is planned in detail).
3. `deployment/staging.gitlab-ci.yml`: parameterize `prepare_kube_config`/`sync_argo_app`/`run_integration_tests` by lane (namespace, ArgoCD app name, resource_group) instead of hardcoding `testing`/`staging`.
4. `deployment/scripts/argocd_sync_testing_images.sh`: take the target app/namespace as a parameter instead of the hardcoded `testing` app name and `/ffnodes/fitfile/testing/values.yaml` path.
5. `workflows-api/deployment/pipeline/staging-jobs.yaml`: add the lane-assignment job (or generated-pipeline job) ahead of `trigger_integration_tests`.
6. Update any other repo found in step 1 of the earlier investigation (auditing all consumers of `deployment/staging.gitlab-ci.yml`) to the new parameterized trigger.

Trade-offs:

- Effort: medium—no new lifecycle tooling, but real duplicated infra (N-1 extra MSSQL instances + PVCs + seed jobs, ongoing cost, config drift risk across N copies of secrets/values).
- Ceiling: bounded—throughput goes from 1→N, not to "however many MRs are queued." A Renovate burst of 10 still queues in batches of N.
- Risk: low—same isolation guarantee as today (dedicated app/namespace/db per lane), no new cleanup/teardown logic needed since lanes are permanent.

---

### Option (B): True ePhemeral per-MR eNvironment via ArgoCD ApplicationSet

Idea: Use ArgoCD's `ApplicationSet` PullRequest generator (or GitLab MR generator) to auto-create/delete a full `testing-mr-<iid>` stack per open MR—the pattern this repo already uses for `kch-prod`/`kch-mn4`/`stg-sandbox`, just pointed at MR events on the relevant app repos instead of a static list.

Implementation steps, in order:

1. `deployment` repo: add `ffnodes/fitfile/testing-mr/templates/testing-mr-application-set.yaml` modeled on `ffnodes/stg/sandbox/templates/stg-sandbox-application-set.yaml` (read that file in detail before designing this—I haven't yet), using a PullRequest generator against the relevant GitLab project(s) to template `namespace`/`deploymentKey`/DNS hostnames per MR IID from `ffnodes/fitfile/testing/values.yaml` as the base.
2. Decide the MSSQL story specifically—this is the crux open question: either (i) each ephemeral env gets its own MSSQL + seed job (simplest, but reintroduces the cold-start latency this option is supposed to avoid, and multiplies DB cost per concurrent MR), or (ii) ephemeral envs share one persistent MSSQL instance with per-namespace schemas/databases (faster, cheaper, but needs new seed/isolation logic that doesn't exist today and risks cross-MR data bleed if done wrong).
3. `deployment/scripts/argocd_sync_testing_images.sh`: parameterize the hardcoded `testing` app name and `/ffnodes/fitfile/testing/values.yaml` path by MR IID.
4. `deployment/staging.gitlab-ci.yml`: parameterize namespace/app name/DNS by `$CI_MERGE_REQUEST_IID`; `resource_group` can likely be dropped entirely (each MR's app name is already unique, so there's no shared mutable state to protect) or kept scoped to the MR purely for same-MR retry safety.
5. `workflows-api/deployment/pipeline/staging-jobs.yaml`: pass `CI_MERGE_REQUEST_IID` through; no lane-assignment logic needed (ApplicationSet handles allocation).
6. No custom teardown job needed in CI—ApplicationSet's PullRequest generator removes the Application automatically when the MR closes/merges. Still worth a scheduled reconciliation job as a belt-and-braces check for anything the generator misses, especially given the NHS-supplier-scope/compliance angle the ticket raises around live-but-abandoned environments.

Trade-offs:

- Effort: high—new ApplicationSet, per-MR DNS/ingress templating, and the unresolved MSSQL sharing/isolation question is real design work, not boilerplate.
- Ceiling: effectively unbounded, scales with actual queue depth—this is the only option that fully satisfies "better parallelism than one MR at a time" without an artificial cap.
- Risk: higher—new failure modes (generator misconfiguration, leaked namespaces if reconciliation isn't solid, per-MR DNS cert/ingress issues, MSSQL isolation if sharing an instance) in a codebase touching NHS-adjacent data patterns, where an orphaned live environment is a compliance concern, not just a cost one.
- Cluster capacity: needs headroom for N concurrent full stacks at burst, vs. option (a)'s fixed N regardless of burst size.

---

### Independent of Which Option You Pick

The AC's "skip environment-locking jobs entirely for low-risk update classes" is cheap, low-risk, and orthogonal to both options above—gating `get_staging_images`/`trigger_integration_tests` (`workflows-api/deployment/pipeline/staging-jobs.yaml:1,23`) on MR labels/branch-prefix so grouped-patch Renovate MRs skip the shared-environment path entirely. I'd suggest doing this first regardless, since it reduces queue pressure immediately without touching ArgoCD topology, and shrinks whatever option (a) or (b) actually needs to handle.

My recommendation, given what I found: (a) as a near-term throughput fix (bounded effort, no new lifecycle risk, reuses the pattern this repo already has for `sandbox-testing-*`), with (b) as the real fix once the MSSQL-sharing question is resolved—rather than building the harder, riskier option first. But this is your call given the compliance/SLA context you'd know better than the repo shows.

Which direction should I turn into a detailed implementation plan?

Option (a) fixed pool now (Recommended)

Let me confirm how new `ffnodes/fitfile/*` environments actually get registered as ArgoCD Applications before finalizing the pool-lane steps—this determines whether adding a lane is "add a folder" or "write new Terraform."

Before finalizing, one important correction to the effort estimate I gave earlier: I checked `terraform-fitfile-central-services-consumer` (the module referenced by the ArgoCD data-flow doc in `platform-defaults`), and it's a full customer-onboarding module —provisions a GitLab project, TFC workspace, Auth0 client, deploy tokens, etc., per "customer." If that's genuinely how `ffnodes/fitfile/testing` got registered, standing up `testing-2` the "proper" way means running that same heavyweight onboarding flow for an internal lane, not a quick YAML add. I couldn't confirm from the repos alone whether the _internal_ `fitfile` tenant's test/sandbox nodes (`testing`, `sandbox-testing-1.`) actually go through this customer-grade path or were registered more simply (e.g. a one-off manual `argocd app create`)—that's a genuine unknown, not something I should guess at, so I'm flagging it as the first thing to confirm rather than assuming either way.

### Plan: Option (a)—2-lane Pool + Low-risk-update Skip Path

Scope for this pass: 2 lanes (`testing`, `testing-2`) rather than 3+, to keep duplicated MSSQL/storage cost and config-drift surface down for a first cut; extendable later. Paired with the skip-path so low-risk Renovate MRs never touch either lane.

#### Step 0—Confirm before Writing Any Code

Find out how `ffnodes/fitfile/testing`'s ArgoCD Application was actually registered (ask the platform owner, or check ArgoCD's own UI/`argocd app get testing -o yaml` for its `metadata.annotations`/source, or search `terraform-fitfile-unified-deployment` for a module instantiation referencing `deployment_key = "testing"`). This decides whether step 2 below is a Terraform PR in another repo or a one-off imperative `argocd app create`.

#### Step 1— `deployment` Repo: New Lane's Config

- Duplicate `ffnodes/fitfile/testing/values.yaml` → `ffnodes/fitfile/testing-2/values.yaml`, changing `namespace: testing` → `testing-2`, `deploymentKey: testing` → `testing-2`, and its own MSSQL PVC/storage block so it doesn't collide with lane 1.
- Decide and set distinct hostnames for lane 2 (today's script hardcodes `testing-argocd.fitfile.net` / `testing-argo-workflows.fitfile.net` —lane 2 needs its own, e.g. `testing-2-argo-workflows.fitfile.net`), which likely means a DNS/ingress change too—needs confirming with whoever owns that.

#### Step 2—Register the `testing-2` ArgoCD Application

Per Step 0's answer: either a Terraform change (new module instantiation, its own PR/apply cycle, likely platform-team review) or an imperative `argocd app create testing-2 …` bootstrap. I'd plan this as its own reviewable unit separate from the CI changes below, since it's infra, not pipeline config.

#### Step 3— `deployment/staging.gitlab-ci.yml`

Parameterize `prepare_kube_config`, `sync_argo_app`, `run_integration_tests` (lines 14–83) so namespace, ArgoCD app name, and `resource_group` come from a `$LANE` variable instead of the hardcoded `staging`/`testing` —e.g. `resource_group: staging-$LANE`, `ARGO_BASE_HREF: $LANE-argo-workflows.fitfile.net`, `argo list -n $LANE`.

#### Step 4— `deployment/scripts/argocd_sync_testing_images.sh`

Replace the hardcoded `argocd app set testing --values /ffnodes/fitfile/testing/values.yaml` / `argocd app sync testing` with parameters driven by `$LANE`.

#### Step 5— `workflows-api/deployment/pipeline/staging-jobs.yaml`

Add lane assignment ahead of `trigger_integration_tests` (line 23): static regex bucketing on `$CI_MERGE_REQUEST_IID` (e.g. odd IID → `testing`, even → `testing-2`) is enough for 2 lanes and avoids building dynamic-child-pipeline tooling for this first cut. Pass `$LANE` through to the triggered pipeline's variables.

#### Step 6—Low-risk-update Skip Path (Same fIle)

Add a `rules:` condition to `get_staging_images` (line 1) and `trigger_integration_tests` (line 23) that skips both jobs when the MR is a grouped-patch/low-risk Renovate update—needs a concrete signal to key off (MR label, branch prefix, or a Renovate-set commit trailer). I don't yet know which signal Renovate actually sets on these MRs today—that's the one thing I'd want to check in `renovate-config`/`renovate.json` before writing the rule, rather than guessing a label name.

#### Step 7—Repo Audit

Re-check for any other repos beyond `workflows-api` that trigger `deployment/staging.gitlab-ci.yml` (only sampled `InsightFILE`, `ude-cli`, `fitfile-workflows` earlier—worth a fuller GitLab-wide search before calling this done) and apply the same lane-assignment change to each.
