---
created: 2026-08-26T13:36:09+00:00
modified: 2026-08-26T13:36:13+00:00
permalink: llmeon/00-inbox/dev-events-to-trigger-on
title: Dev events to trigger on
type: note
---

## SDLC Trigger Events and Automated Quality Gates

This reference guide maps the triggers across the Software Development Life Cycle (SDLC)—spanning local development, version control, CI/CD orchestration, and GitOps deployments—to their corresponding automated checks and quality gates.

### 1. SDLC Trigger Matrix: Events vs. Automated Checks

|SDLC Stage|Trigger Event|Trigger Mechanism / Hook|Typical Automated Checks & Actions|
|---|---|---|---|
|Local / IDE (Inner Loop)|File modified / saved|IDE watcher / Language server|Instant syntax linting, type checking, auto-formatting.|
||Commit staged / created|Git `pre-commit` / `commit-msg` hook|Secret detection, local linting, commit message convention validation, fast unit test subsets.|
||Local branch push initiated|Git `pre-push` hook|Fast unit tests, branch naming policy enforcement, local smoke tests.|
|Branch & Code Review|Branch created|Git server push event|Branch protection verification, initialization of branch-level baseline checks.|
||Push / updates to feature branch|GitLab CI `push` pipeline|Compiling, unit testing, initial code smell and linting analysis.|
||Merge Request (MR) opened / updated|GitLab CI `merge_request_event`|Full commit test suite, static application security testing (SAST), dependency/license vulnerability scanning, diff code coverage.|
||MR marked as Draft / Work in Progress|GitLab CI workflow rules (`$CI_MERGE_REQUEST_TITLE`)|Lightweight linting, skipping heavy or costly end-to-end suites to preserve CI capacity.|
||Diff comments / review approval|Code review platform webhooks|Policy gating requiring approvals before merge, review-app deployments, automated verification comments.|
|Trunk Integration (Mainline)|MR merged / New HEAD on default branch|GitLab CI `push` to default branch|Full integration build, database migration compatibility tests, binary artifact assembly, artifact publishing.|
||Pipeline job success|Pipeline DAG / `when: on_success`|Downstream job execution, test report generation, artifact forwarding.|
||Pipeline job failure|Pipeline failure handler / `when: on_failure`|Team alert notifications, failure triage logs, auto-cancellation of downstream stages.|
|Artifact & Image Registry|Docker / OCI container build completed|CI build stage|Container image vulnerability scanning (CVE scanning), SBOM (Software Bill of Materials) generation.|
||Push new images to registry (e.g., ACR)|Registry webhook / CI post-build|Registry-level image signing, dynamic security validation, trigger downstream GitOps manifest updates.|
|GitOps Deployment (e.g., ArgoCD)|Manifest change detected|GitOps controller sync trigger|Kubernetes manifest validation, OPA / policy compliance checks.|
||Pre-Sync phase|`argocd.argoproj.io/hook: PreSync`|Database schema migrations, backup verification, prerequisite infrastructure provisioning.|
||Sync phase|`argocd.argoproj.io/hook: Sync`|Resource manifest application, pod health verification.|
||Post-Sync phase|`argocd.argoproj.io/hook: PostSync`|Smoke tests, post-deployment health checks, notification dispatches.|
||Sync failure|`argocd.argoproj.io/hook: SyncFail`|Automated rollback, failure alerts, operational incident logging.|
|Release & Verification|Git release tag pushed|GitLab CI `tag` pipeline (`$CI_COMMIT_TAG`)|Release candidate packaging, changelog generation, deployment to production/staging environments.|
||Customer-specific tag moved|Git tag update webhook|Targeted tenant deployment, tenant-specific configuration validation, automated regression suites.|
||Production rollout|Canary / Blue-Green rollout controller|Automated canary analysis (error rates, latency thresholds), synthetic traffic validation.|
|Out-of-Band & Maintenance|Scheduled / Cron interval|GitLab CI `schedule` pipeline|Long-running capacity/performance tests, full DAST scans, chaos engineering experiments, dependency updates.|
||Security policy execution|GitLab `security_orchestration_policy`|Enforced compliance scans, periodic image rescoring.|
||External API / ChatOps trigger|GitLab `trigger`, `api`, or `chat`|On-demand environment provisioning, ad-hoc diagnostic suites.|

### 2. GitLab CI/CD Pipeline Sources Reference

GitLab CI/CD exposes the `$CI_PIPELINE_SOURCE` predefined variable to control job execution via `rules:`.

YAML

```
# Example: Differentiating Merge Request pipelines from Default Branch pipelines
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

#### Supported Pipeline Sources (`$CI_PIPELINE_SOURCE`)

- `push`: Triggered by standard Git push events to branches or tags.
- `merge_request_event`: Triggered when an MR is created, updated, or re-run via the MR interface.
- `schedule`: Triggered by recurring cron-based pipeline schedules.
- `parent_pipeline`: Triggered within child pipelines executed by a downstream parent pipeline.
- `pipeline`: Triggered by multi-project pipeline triggers.
- `trigger`: Triggered using CI trigger tokens.
- `api`: Triggered through direct pipeline REST API calls.
- `web` / `webide`: Triggered manually via the GitLab UI or the Web IDE.
- `chat`: Triggered via ChatOps commands (e.g., Slack / Mattermost).
- `ondemand_dast_scan` / `ondemand_dast_validation`: Triggered by dynamic application security scans.
- `security_orchestration_policy`: Triggered by centralized scan execution policies.
- `external` / `external_pull_request_event`: Triggered when integrating external CI services or external GitHub pull requests.

### 3. Recommended Quality Gate Architecture

```
[ Developer Workspace ]
   │  Hooks: Lint, Format, Fast Unit Tests[cite: 6]
   ▼
[ Push / Merge Request Event ]
   │  CI: SAST, Dependency Scans, Unit & Commit Tests, Code Coverage[cite: 2, 13]
   ▼
[ Merge to Mainline / Trunk ]
   │  CI: Full Build, Integration Tests, Image Packaging & Push[cite: 2, 13]
   ▼
[ GitOps Manifest Sync (ArgoCD) ]
   ├── PreSync:  Schema Migrations[cite: 2]
   ├── Sync:     Apply Manifests[cite: 2]
   ├── PostSync: Smoke Tests, Health Verification[cite: 2, 22]
   └── SyncFail: Auto-Rollback & Notifications[cite: 2]
   ▼
[ Post-Deployment / Scheduled ]
   │  Schedules: DAST, Chaos Testing, Capacity & Performance Tests[cite: 1, 13, 27]
```

#### Key Strategies for Pipeline Efficiency

- Prevent Duplicate Pipelines: Use `workflow: rules` to ensure pushes to branches with open merge requests trigger either a branch pipeline or a merge request pipeline, not both simultaneously.
- Fast Commit Stage: Design commit stage test suites to run within five to ten minutes, deferring expensive capacity and integration tests to downstream or scheduled stages.
- Feature Flag Testing: When testing changes behind feature flags, configure the test stage to run suites against both dormant (`OFF`) and active (`ON`) flag states to ensure baseline safety and feature correctness.
- Interruptible Jobs: Configure `interruptible: true` for development branches so that newer commits automatically cancel obsolete runs, reducing queue bottlenecks.
