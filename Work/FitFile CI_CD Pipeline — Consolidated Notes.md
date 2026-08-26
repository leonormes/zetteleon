---
author: Hermes (consolidation)
created: 2026-08-26T09:45:00+01:00
modified: 2026-08-26T09:45:00+01:00
permalink: llmeon/work/fitfile-ci-cd-pipeline-consolidated
tags: [fitfile, ci-cd, gitlab, pipeline, devops, security, argo-cd, trivy]
title: FitFile CI/CD Pipeline — Consolidated Notes
type: note
---

# FitFile CI/CD Pipeline — Consolidated Notes

Single consolidated reference for FitFile's CI/CD pipeline work, merged from six `00_Inbox/` captures (2026-08-24/2026-08-12). Organised for parsing: state → bottlenecks → security → contract testing → telemetry → actions.

---

## 1. Source Index

| # | Source (original `00_Inbox/` file) | Date | Focus |
|---|---|---|---|
| A | `FitFile CI_CD Pipeline Research.md` | 2026-08-24 | Evidence-based pipeline strategy (DORA/SRE), 3-phase action plan |
| B | `fitfile_pipeline_notes.md` | 2026-08-24 | Miro board retro — 6 pipeline stages, problems, improvements, FTFL-971 cross-ref |
| C | `Pipeline Optimisation (caching + merge-skew workflow rules).md` | 2026-08-24 | GitLab YAML patterns: caching, workflow:rules, shift-left gates |
| D | `Contract Testing and CI_CD Guide.md` | 2026-08-12 | Advanced contract testing + release management topology |
| E | `Implementing self-verifying alerts for CICD pipelines.md` | 2026-08-24 | Dead-man's-switch / heartbeat alerts (FTFL-938/942) |
| F | `What Kubescape does.md` | 2026-08-24 | Kubescape K8s posture scanner vs Trivy |

---

## 2. Current Pipeline State (Miro Board Retro — Source B)

### 2.1 Six Stages

| Stage | Key steps | Main problems |
|---|---|---|
| **1. Local Dev** | dev env, unit/integration tests, lint, manual, Claude Code, Renovate, npm audit | Dev env difficult; "have we shift-left enough?"; Renovate PRs can't be blindly merged; multi-repo orchestration |
| **2. Feature Branch** | unit, Playwright, Storybook, build, lint, npm audit | SonarQube timing; growing `npmAuditIgnore`; feature flags not visible; small-team PR approval |
| **3. Merge Train** | API/integration tests, data-pipeline tests, migration tested, RC image builds, TFC for infra | No parallelism (bottleneck); flaky API tests; no resource limits on test pods; no way to pass image version to tests (uses ArgoCD sync); no build cache; low test coverage; concurrent-pipeline race conditions |
| **4. Staging Release** | full image build, push to ACR, chart tags bumped, package version bumped, TFC + local Terraform | No build cache; ACR push secret expires (manual update); upgrading private resources; "test & staging seem interchangeable" |
| **5. Production Release** | move per-customer latest-release tag for ArgoCD, TFC, tag | No rollback procedure (esp. with migrations); per-env config drift; no inbound connectivity to private clusters without bastion |
| **6. Customer Release** | per-customer latest-release tag, TFC, manual UI check | Manual per-customer tagging; no client overview; demo env stability; customer config changes require a new release |

### 2.2 Root / Cross-Stage Problems

- **Critical:** pipelines slow; pipelines flaky; 1 concurrent pipeline at a time; builds slow
- **Process:** few people can manage deployments; deployment assuredness; monorepo needs non-blocking pipeline (HEAD commits blocking); 🔴 **00:19:02 frontend-only run**
- **Build & Infra:** all ACR builds AMD64 (rebuilds); no build cache (×3 mentions); no SBOM; no release notes; 3 disparate deploy paths (infra/platform/application); can't cherry-pick releases; charts not built/versioned in ACR; stacked PRs (?)
- **Stability:** DB connectivity for demo/test; demo env stability

### 2.3 Miro Board Improvements

- **Quick wins:** move customer config to own repos; own GitLab runners (build cache); parameterise integration tests to parallelise; publish charts to ACR; write more pipeline tests
- **Experimental/future:** ephemeral envs per branch; feature flags
- **Epic ideas:** flagged "🚀 LETS DO THIS!!"

### 2.4 Ticket Cross-Reference (Miro → FTFL)

| Miro item | Ticket(s) |
|---|---|
| ACR push secret expires | FTFL-978/979/980/981 (OIDC federation replaces static ACR password) |
| 🔴 19:02 frontend run | FTFL-988 (625s warm / 1423s cache-miss; root cause: yarn cache not mounted into build context) |
| No build cache (×3) | FTFL-987 (deployment Argo images), FTFL-988 (InsightFILE yarn) |
| AMD64-only builds | FTFL-988 (lands on "keep pinning amd64" — flag back if Apple Silicon dev use case exists) |
| "Shift-left enough?" | FTFL-985/986 (Trivy/SAST/secret/dependency gates pre-push) |
| 1 concurrent pipeline / no parallelism / race conditions | FTFL-897 (root cause: `resource_group: staging` lock; investigation-stage, no fix ticket yet) |
| SonarQube timing / npmAuditIgnore | FTFL-986 (removes `\| true`/`allow_failure` silence) |
| "No way to pass image version to tests" | Related to FTFL-991/972 (`STAGING_VALUE_OVERRIDES`/`get_staging_images.sh`) — fixes leaks, not the design gap |
| No SBOM | FTFL-893 (pre-existing, under FTFL-865 epic) |
| Unaddressed remainder (customer release, rollback, monorepo blocking, etc.) | Out of FTFL-971 scope — decide: second epic or backlog |

---

## 3. Pipeline Bottlenecks & Optimisation (Sources A + C)

### 3.1 Sequencing Principle

Pipeline speed & reliability **precede** security gates. DORA *Accelerate* capabilities: 19-min flaky pipeline + security scanning = excruciating feedback loop. CE+ April 2026 imposes a strict **14-day SLA** for high/critical patches — a brittle 19-min pipeline makes that mathematically improbable. Toyota Kata: set a pipeline Target Condition ("builds <5min") before a security Target Condition.

### 3.2 Build Caching (the 19-min bottleneck)

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

**FTFL-988 root cause:** yarn cache not mounted into the Docker build context (625s warm / 1423s cache-miss).

### 3.3 Merge Skew & GitLab MR Pipeline Routing

- Long-lived feature branches tested against stale trunk → violent merge conflicts. **Trunk-based development** (merge to main daily) is the DORA fix — requires feature-flag discipline.
- **GitLab MR-pipeline gotcha:** `$CI_COMMIT_BRANCH` is unavailable in MR pipelines (documented behaviour) → jobs silently run zero tests. Fix with `workflow:rules` on `$CI_PIPELINE_SOURCE == "merge_request_event"`, and use `$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME` in MR context. Disable duplicate branch pipelines while an MR is open to avoid double compute spend.

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

### 3.4 Feature Flags (Trunk-Based Prerequisite)

- Hodgson/Fowler taxonomy: Release, Experiment, Ops, Permissioning toggles. **Start with Release Toggles only** (short-lived, separate deploy from release); avoid Experiment/Permissioning and migration-bearing data-state toggles in month one.
- **Stale flags** are the #1 failure mode — flag removal must be an explicit Definition-of-Done step.

### 3.5 Team Topologies / PR Bottleneck

- Single-owner PR approval gate violates "fast flow" (Skelton & Pais). Platform team should be *Platform + Enabling* — self-service templates + policy-as-code — with peers approving standard MRs and automated CI gates (SAST, secret scanning) enforcing baselines. Decentralise only after flaky tests are stabilised.

### 3.6 DORA Metrics

- 2024/2025 DORA added a **5th metric: Deployment Rework Rate** (% of deployments that are unplanned production fixes) — quantifies the merge-skew cost. MTTF→Failed Deployment Recovery Time moved to throughput category.

---

## 4. Security Gates & Shift-Left (Sources A + F)

### 4.1 Trivy: Report-Only → Blocking Gate

- OWASP DSOMM "Decision Contracts": every control is Block / Warn / Log. Start Trivy in **`--exit-code 0` report-only**, publish to MR via GitLab **SARIF** integration for visibility without blocking merges.
- **Avoid "security theater":** a report-only gate without a pre-defined flip trigger becomes invisible. Flip to blocking (`--exit-code 1`) only after a data-driven trigger: e.g. 14 days without a false positive that would have blocked a legitimate build **and** the baseline backlog of criticals (KEV-listed / EPSS > 0.088) is cleared. Map accountability via RACI.

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

**⚠️ Trivy supply-chain caveat:** Trivy's own supply chain was compromised (CVE-2026-33634, Mar 2026 — malicious commits into 76/77 `aquasecurity/trivy-action` tags, backdoored v0.69.4). **Pin CI Trivy usage to commit SHAs, not tags**; run ≥v0.69.7.

### 4.2 Vulnerability Triage: EPSS + CISA KEV (CVSS-blind)

- 7,399 open findings; **51% lack CVSS** (NIST halted universal scoring early 2026). CVSS measures theoretical severity, not real-world exploitation → anti-pattern for prioritisation.
- **EPSS** (FIRST): ML probability of exploitation in next 30 days. **CISA KEV**: binary known-exploited indicator. Chaining EPSS+KEV can cut urgent workload **~95%** while keeping high threat coverage.

| Triage tier | Criteria | Action |
|---|---|---|
| Tier 0 | In CISA KEV | Remediate immediately (non-negotiable) |
| Tier 1 | EPSS > 0.088 | Prioritise in current sprint |
| Tier 2 | High CVSS (7.0–10.0), EPSS < 0.088 | Standard patching cycle |
| Tier 3 | Low CVSS, low EPSS, not in KEV | Defer / accept residual risk |

- **Threshold:** 0.088 chosen over 0.36 (F1-optimal) — ROC/AUC analysis shows 0.088 keeps 85.6% coverage of exploited vulns while filtering noise. For CVSS-less findings, use **SSVC** (CISA/CMU decision trees).
- **Compliance caveat:** NHS DSPT may still lean on legacy CVSS — document EPSS/KEV methodology in risk-acceptance policies to defend the posture in audits.

### 4.3 Kubescape (K8s posture — Source F)

- CNCF/ARMO open-source platform: config scanning (manifests/Helm/charts), CVE scanning, **compliance mapping (NSA-CISA, MITRE ATT&CK, CIS Benchmarks)**, runtime threat detection, CI/CD integration.
- **Positioning vs current stack:** Trivy stays the CVE/image engine (deeply wired into Grafana dashboards, VEX repo, CI). Kubescape fills the **manifest/Helm misconfig + compliance-posture gap** — currently unaddressed ("no scanner in any pipeline anywhere in the estate" for that category, per FTFL-865 notes). Standard "SCA/image + K8s posture" pairing; supports the Gatekeeper phased-enforcement direction (FTFL-859).
- **Not yet decided:** no evidence Kubescape was evaluated head-to-head in `fitfile-vuln-mgmt-research` — check the scanner-comparison table before adopting.

### 4.4 SLSA L2 & Supply-Chain (Azure Policy + Ratify)

- Target: SLSA 1→2 (signed provenance, cryptographically signed by hosted build). Azure Policy (Gatekeeper) invalidates generic OPA guidance → use **Ratify** to verify Cosign/Sigstore keyless signatures + in-toto attestations before pod admission.
- Generate SLSA provenance in GitLab CI with **Cosign keyless signing (OIDC)**; deploy Ratify on AKS; Azure Policy rejects unsigned images.
- **Risk:** Ratify needs precise OIDC between GitLab and Azure AD (Workload Identity); misconfiguration can lock the platform team out of the cluster.

### 4.5 CI-to-Azure OIDC (unverified — needs `glab api`)

- K8s-layer Azure Workload Identity is already OIDC/federated-credential (per SoT notes) — but whether **GitLab CI runners** authenticate to Azure via `id_tokens:`/OIDC is a separate trust boundary, **unconfirmed**. Verify before applying:
```bash
glab api projects/:id | jq '.ci_forward_deployment_enabled'
glab api projects/:id/job_token_scope | jq '.'
glab ci list --repo fitfile/deployment
```
- OIDC pattern replaces `AZURE_CLIENT_SECRET` with `id_tokens:` → `az login --service-principal --federated-token`, plus a Federated Identity Credential on the Azure App Registration (issuer `https://gitlab.com`, subject `project_path:fitfile/deployment:ref_type:branch:ref:main`).
- **Repo topology note:** `deployment` repo has a `pipeline/` template dir (`common-jobs.yml`, `verification-pipelines.yml`, `build-pipelines.yml`, `staging-pipelines.yml`, `release.gitlab-ci.yml`) — none locally readable, snippets are suggested additions not diffs.

### 4.6 Database Migrations in GitOps (ArgoCD)

- Expand/contract migrations may be structurally out of reach short-term. Middle ground: **ArgoCD Sync Waves + PreSync hooks** — migrations as K8s Jobs annotated `argocd.argoproj.io/hook: PreSync`, never in app pod startup (avoids race conditions/timeouts).
- Defensive PostgreSQL: `SET lock_timeout = '5s';` in migration scripts; `pg_repack` for non-blocking table/index maintenance.

---

## 5. Contract Testing & Release Management (Source D)

### 5.1 CDC Best Practices

- **Robustness principle (Postel's Law):** contracts must use type/regex/array matchers, not exact values (except business invariants like enums). Exact values → brittle false negatives.
- **Wire semantics over internal models:** never reuse DTOs/ORM entities in contract tests — capture actual wire-level HTTP semantics (headers, base paths, auth tokens) via network capture; author payloads as plain JSON/DSL independent of app classes.
- **Deep mocking:** mock at the lowest boundary (DB/repository/outbound API), not the HTTP controller — controller mocks bypass serialization, middleware, security interceptors, exception handlers → false confidence. Use **provider states** to manipulate deep state before replay.

### 5.2 Provider Verification Must Be Explicit

- A consumer contract is meaningless unless the provider verifies it in CI: pull latest contracts, run against a real running provider instance, publish cryptographic verification results back to the broker. Mandatory, automated, never ad-hoc.

### 5.3 Topologies

- **Sync (gRPC/Protobuf):** schema ≠ behaviour — contract test behavioural expectations (optional-but-required fields, enum support) over the binary stream.
- **Async (Kafka/RabbitMQ/SNS):** Hexagonal approach — test the core domain logic's message generation/parsing, not the transport; avoids provisioning brokers in CI.

### 5.4 CDCT vs BDCT

| | CDCT | BDCT |
|---|---|---|
| Artifacts | Consumer-generated contract | Consumer contract + provider OpenAPI spec |
| Verification | Dynamic vs running provider | Static in central broker |
| Provider impact | High (deep state + verification runs) | Low (accurate OpenAPI spec) |
| Best for | Deeply coupled internal microservices | Third-party/legacy/rigid-governance APIs |

### 5.5 Contract Registry & Deployment Gating

- Central broker maintains a **Contract Matrix** (consumer version × provider version × contracts × verification status × environments). Git SHA as immutable version id (never `latest`/`dev`); publish with branch name too.
- **Deployment gate** (`can_i_deploy`): before promotion, query broker — "is this version compatible with all partners currently in the target env?"; exit 0 = proceed, non-zero = halt.
- **Deployment recording:** pipeline posts deployment events (Git SHA + env) synchronously; enables safe rollbacks (never roll back to a version incompatible with current surroundings).

### 5.6 Decouple Deploy from Release

- **Service mesh (Istio) header routing** for dark launches: exact/prefix/regex header matches route QA/synthetic traffic to the new version against real prod deps; fault injection for chaos.
- **Automated canary (Kayenta):** compare canary **against baseline** (fresh instance of existing code), not long-running prod (JIT/cache warmup skews). Mann-Whitney U test → score; abort+auto-rollback on critical failure; incremental traffic shift. Four phases: data validation → cleaning (NaN handling) → metric comparison → score.
- **Feature flags** at the app layer: deploy dormant, toggle per segment, instant MTTR measured in ms.

---

## 6. Self-Verifying Alerts / Telemetry (Source E)

### 6.1 The Core Principle

> "No control ships until it can prove it ran. Every check must emit a positive signal... never merely an absence of errors. Absence of errors is exactly what a dead control produces."

An absence-triggered (log-based) alert cannot distinguish "nothing bad happened" from "the thing that tells me something bad happened is itself broken." The log-based `TrivyImageScanFailed` alert sitting in NoData when healthy is indistinguishable from the log pipeline breaking.

### 6.2 Dead-Man's-Switch / Watchdog Pattern

- **Always-firing synthetic alert:** `expr: vector(1)`, routed on a short repeat interval to an external heartbeat receiver (Dead Man's Snitch / owned webhook); the external watchdog raises its own alarm when a check-in is missed — alert path monitored outside the system it monitors.
- Threshold must be ≫ heartbeat interval (e.g. heartbeat 5m, alert if absent 15m) to avoid false-positive fatigue.
- Heartbeats must validate **actual success** of the control (end-to-end synthetic check), not just script invocation. Emit on **both** success and failure paths (via `trap ... ERR` and `after_script`) so a job that dies silently still surfaces as "expected heartbeat, got none" (e.g. Prometheus `absent()` rule).

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

### 6.3 Mapping to Tickets

| Ticket | Failure mode | Fix shape |
|---|---|---|
| FTFL-938 | Scan jobs fail silently (3,132 log lines over 6 working days undetected) | Positive "I ran, covered N workloads, at time T" signal — not absence-of-error |
| FTFL-942 | Alert in NoData when healthy — indistinguishable from broken | Metric-based alerts: new Critical, threshold crossing, coverage drop, staleness >24h (replace broken log-based ones) |
| Tier 0 exit gate | "72h green" over a weekend the cluster is off → guaranteed false pass | "Three consecutive working days at zero," not wall-clock hours |
| FTFL-893 (related) | CronJob "looked correctly deployed all day and would never have fired once" | Staleness-based heartbeat catches immediately |

**Not yet ticketed:** a watchdog/heartbeat rule on the scan job itself — fires only when `trivy_resource_configaudits` (or equivalent coverage metric) hasn't updated within an expected window. Sits alongside FTFL-942, not inside it.

### 6.4 Telemetry Signal Skeleton

```yaml
.telemetry_signal: &telemetry_signal |
  send_heartbeat() {
    local job_name="$1" count="$2" status="$3"
    curl -sf -X POST "$TELEMETRY_ENDPOINT/heartbeat" \
      -H "Authorization: Bearer ***" \
      -d "{\"job\":\"$job_name\",\"ran_at\":\"$(date -u +%FT%TZ)\",\"items_checked\":$count,\"status\":\"$status\"}" \
      || echo "WARNING: telemetry heartbeat failed for $job_name" >&2
  }
```

---

## 7. Prioritised Action Plan (Source A, 3 Phases)

### Phase 1 — Do Next (0–2 weeks)

1. **Fix GitLab CI pipeline routing** — `workflow:rules` on `$CI_PIPELINE_SOURCE == "merge_request_event"`; use `$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME` in MR context. *(Fixes the zero-tests-on-MR incident; risk: duplicate pipelines if rules nested wrong.)*
2. **Dead Man's Switch for critical CronJobs** (Renovate, health checks) — heartbeat on successful completion; alert on absent heartbeat > interval. *(Addresses "silence as health" failure mode.)*
3. **Transition Trivy to report-only MR gate** — `--exit-code 0` + SARIF to MR. *(Baseline detection skeleton without halting the 19-min pipeline; define the data-driven flip trigger.)*

### Phase 2 — This Quarter

4. **Adopt EPSS & KEV triage** — filter 7,399 findings: KEV fix immediately, EPSS > 0.088 prioritise, rest acknowledge/log. *(Fixes CVSS-blind triage paralysis; document in risk-acceptance for DSPT.)*
5. **Optimise Docker BuildKit caching** — dependency-first layers, `--cache-to=type=registry`, multi-stage. *(Attacks 19-min bottleneck → enables 14-day CE+ patching SLA; risk: registry bloat from cache manifests.)*
6. **Isolate migrations via ArgoCD PreSync hooks** + PostgreSQL `lock_timeout`. *(Decouples schema from deploy; risk: degraded ArgoCD app if hook fails — need rollback hooks.)*

### Phase 3 — Structural / Long-Horizon

7. **Release Toggles for trunk-based dev** — centralised flag platform, start with low-risk frontend changes. *(Fixes merge skew; risk: stale-flag debt — enforce removal in DoD.)*
8. **Decentralise PR approvals** — platform team builds automated compliance checks; peers approve standard MRs. *(Removes queueing bottleneck; only after flaky tests stabilise.)*
9. **SLSA L2 via Azure Policy + Ratify** — Cosign keyless in GitLab CI, Ratify admission on AKS. *(Respects existing Gatekeeper architecture; risk: OIDC misconfiguration locks out the cluster.)*

---

## 8. Key Numbers & One-Liners

- **19:02** — frontend-only pipeline run time (FTFL-988: 625s warm / 1423s cache-miss)
- **7,399** — open vulnerability findings; **51%** without CVSS
- **~95%** — urgent-workload reduction from EPSS+KEV chaining
- **14 days** — CE+ 2026 SLA for high/critical patches
- **0.088** — chosen EPSS threshold (85.6% coverage of exploited vulns)
- **5th DORA metric** — Deployment Rework Rate (quantifies merge skew)
- **1 concurrent pipeline** — `resource_group: staging` lock (FTFL-897)

---
*Consolidated 2026-08-26 from 6 inbox captures. Originals removed from `00_Inbox/` (recoverable via git history).*
