---
created: 2026-05-18T00:00:00+00:00
entity_kind: project
modified: 2026-05-18T13:52:46+00:00
sources: [INSIGHTFILE_PIPELINE_REPORT]
tags: [cicd, dossier, gitlab, pipeline, project]
title: INSIGHTFILE_PIPELINE_IMPROVEMENT_PLAN
wiki_type: dossier
---

## InsightFILE Pipeline Improvement Plan

Generated: 2026-05-18

Repository: `gitlab.com/fitfile/apps/InsightFILE`

Local Mirror: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE`

Based on: [[INSIGHTFILE_PIPELINE_REPORT]]

---

## Key Finding: Report Vs Reality Mismatch

The investigation report (Section 2.2) documented an older, monolithic `.gitlab-ci.yml`. The actual current pipeline is already significantly more sophisticated—modular includes, buildx registry caching, GAPV versioning, merge-train gating. The failures documented (`sonar_scan`, `frontend_lint`, `frontend_unit_tests`) come from the modular files, not a missing include system.

---

## Priority 1—Fix Active Failures

> Target: now—unblock the 25% failure rate

### P1.1—`dtrace-provider` / `make` Not Found

- Root cause: `fitfile/sonar-nodejs:1.0.0` is missing the `make` build tool. `dtrace-provider@0.8.8` is a native module that compiles during `yarn install`, and its `gyp` build fails with `Error: not found: make`.
- Evidence: Job traces E4 & E5, pipelines 2522046776 and 2521911238.
- Fix options (pick one):
  1. Add `RUN apk add --no-cache make g++ python3` to `Dockerfile.sonar`—rebuilds the base image once, affects no jobs downstream.
  2. Add `before_script: - apk add --no-cache make` to the verify jobs that trigger in the `sonar-nodejs` image—quicker, no image rebuild needed but adds ~10 seconds per job.
  3. Add `dtrace-provider` to a `.yarnrc.yml` `ignoredBuilds` list so the native compile is skipped entirely (valid since this is a devDependency for DTrace instrumentation, not needed in CI).
- Recommended: Option 3 (add to `ignoredBuilds`)—zero image changes, most surgical.

### P1.2—ESLint `import/no-unresolved` For `koa-bodyparser`

- Root cause: The ESLint `import` plugin can't resolve `koa-bodyparser`'s types. Happens in `frontend_lint` / `verify_ffcloud` or `verify_fitconnect`. Likely a missing `@types/koa-bodyparser` or an eslint `settings.import/resolver` gap.
- Fix: Check the `eslintrc` for the affected service. Either add `@types/koa-bodyparser` to devDependencies, or add `koa-bodyparser` to the `import/ignore` rule in the relevant eslint config.

### P1.3—Retrieve And Classify Remaining 21 Unknown Failures

Run targeted `glab` trace queries against the 21 unanalysed failed pipeline IDs to find if there are other systemic failure modes hiding in the UNKNOWN bucket.

```bash
glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines?status=failed&per_page=100" \
  | jq '.[].id' \
  | xargs -I{} glab api "projects/fitfile%2Fapps%2FInsightFILE/pipelines/{}/jobs" \
  | jq '[.[] | select(.status == "failed") | {id, name, failure_reason}]'
```

---

## Priority 2—Security Hardening

> Target: 1–2 weeks

### P2.1—Protect CI/CD Variables

Currently, 7 of 10 group-level variables have `protected: false`. This means they are injected into jobs on any branch, including contributor branches and MRs from forks. Variables that should be immediately set to `protected: true`:

| Variable | Reason |
|---|---|
| `ACR_SERVICE_PRINCIPLE` | Azure registry write credentials |
| `ACR_SERVICE_PRINCIPLE_PASS` | Same |
| `DOCKER_HUB_DEPLOY_TOKEN` | Docker Hub push token |
| `AZ_CLIENT_ID` / `AZ_CLIENT_SECRET` | Azure AD application credentials |
| `GCR_PASSWORD` | Google Container Registry |
| `RUNTIME_ACCESS_TOKEN` | Runtime service credential |

At project level: `GAPV_INSIGHTFILE_REPO_HTTP_PASSWORD` and `GAPV_DEPLOYMENT_REPO_HTTP_PASSWORD` are both masked but not protected—fix both.

### P2.2—ACR Client Secret Rotation

> Hard deadline: 2026-07-27

The `GitLaB CICD` Azure AD app client secret (ID `214c2d39-565e-4b88-a4a4-faf851ca3f38`) expires in ~10 weeks. Rotate it by 2026-07-10 (2-week buffer). Update `ACR_SERVICE_PRINCIPLE_PASS` in GitLab group variables immediately after.

### P2.3—Migrate ACR Auth to OIDC Workload Identity Federation

The current pattern (`docker login … --password "${ACR_SERVICE_PRINCIPLE_PASS}"`) uses a static rotating secret. GitLab supports `id_tokens:` (OIDC) which can federate to Azure AD Workload Identity—eliminating the static credential entirely.

Benefits:

- Removes secret rotation risk permanently
- Allows per-job scoped access
- Aligns with GitLab's recommended post-`CI_JOB_JWT` auth pattern

Implementation:

1. Configure Azure federated credential on the `FITFILE Gitlab Integration Test Pipelines` app registration
2. Add `id_tokens:` block to build jobs in `build-pipelines.yml`
3. Replace `docker login --password` with `az login --federated-token` in `deployment/pipeline/common/build.sh`

---

## Priority 3—Reliability

> Target: 2–4 weeks

### P3.1—Re-enable `resource_group` On the Release Job

`.gitlab-ci.yml:97` has it commented out with `# Temporarily removing`. Two simultaneous merges to `development` can trigger competing release pipelines that both run `gapv.sh update`, producing a race condition in the deployment repo's chart values.

```yaml
# .gitlab-ci.yml
release:
  stage: deploy
  resource_group: deployment-repo   # ← restore this
```

### P3.2—Pin Floating Image Tags

| Current | Recommended |
|---|---|
| `docker:latest` (all task build jobs) | `docker:27.4.1-cli` |
| `fitfile/gapv:latest` (release pipeline) | `fitfile/gapv:x.y.z` (pin to semver or digest) |

Floating `latest` tags make builds non-reproducible and can introduce silent breakage when upstream images update.

### P3.3—Add Retry to Docker Build Jobs

The task build jobs (`build_default_exit_handler`, `build_emis_processing`, etc.) have no `retry:`. DinD startup failures and ACR push timeouts are transient. All Docker build jobs should add:

```yaml
retry:
  max: 2
  when:
    - runner_system_failure
    - stuck_or_timeout_failure
```

### P3.4—Fix Cleanup Job Scope

`cleanup` currently only runs when `CI_PIPELINE_SOURCE == "pipeline"` (child pipelines), but `output/${CI_PIPELINE_ID}/` is written by the parent pipeline's build jobs too.

```yaml
# .gitlab-ci.yml
cleanup:
  when: always
  rules:
    - if: $CI_PIPELINE_SOURCE == "pipeline"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

---

## Priority 4—Code Quality & DRY

> Target: 4–8 weeks

### P4.1—Consolidate Task Build Jobs onto `.docker_build` Template

`build-pipelines.yml` has a `.docker_build` hidden job template, but ~11 task builds duplicate the `image`, `cache: {}`, `services`, and `script` blocks verbatim instead of using `extends:.docker_build`. Fixing this would shrink the file by ~40% and ensure any change to the template (retry, updated image, etc.) propagates automatically.

Jobs to migrate: `build_default_exit_handler`, `build_emis_processing`, `build_set_intersection_estimator`, `build_medcat_annotation`, `build_sftp_loader`, `build_integration_tester`, `build_s3_fitfile_cli_image`, `build_workflows_api`, `build_mutating_proxy_webhook`, `build_mock_rest`, `build_nhs_pet`.

### P4.2—Fix `sftp-loader` Glob Pattern

`build_sftp_loader` uses a single-level glob:

```yaml
changes:
  - apps/tasks/sftp-loader/*   # ← misses nested files
```

All other services use `//*`. A change to any nested file in `sftp-loader/` won't trigger the build. Fix:

```yaml
changes:
  - apps/tasks/sftp-loader//*
```

### P4.3—Re-enable SonarQube Quality Gate

The `sonarqube-check` stage is commented out in `.gitlab-ci.yml:73–83`. The individual `test:sonar` commands in `verification-pipelines.yml` run with `|| true` (silenced). Code quality signals exist but the pipeline never blocks on them.

Options:

1. Re-enable the standalone `sonarqube-check` job on MRs with `allow_failure: false`
2. Remove `|| true` from `test:sonar` runs and let failures surface

### P4.4—Enable Mypy for Workflows-api

`verify_workflows_api` has `# - mypy src/` commented out. Re-enabling type checking catches a class of Python bugs that pytest won't:

```yaml
# deployment/pipeline/verification-pipelines.yml
- $POETRY_HOME/bin/poetry run pytest workflows_api/tests
- mypy src/   # ← un-comment
```

### P4.5—Add GitLab SAST (free tier)

GitLab provides free static analysis scanning via the `SAST.gitlab-ci.yml` template. Add to `.gitlab-ci.yml`:

```yaml
include:
  - local: /deployment/pipeline/common-jobs.yml
  - local: /deployment/pipeline/verification-pipelines.yml
  - local: /deployment/pipeline/build-pipelines.yml
  - local: /deployment/pipeline/staging-pipelines.yml
  - template: Jobs/SAST.gitlab-ci.yml   # ← add this
```

---

## Priority 5—Performance

> Target: ongoing

The current build already uses `docker buildx` with ACR registry cache (`--cache-from` / `--cache-to type=registry,mode=max`) in `deployment/pipeline/common/build.sh`. This is the correct pattern per GitLab's registry caching docs. No change needed there.

One improvement: the `verify_*` jobs all run `yarn workspaces focus <pkg>` independently. If multiple verify jobs run in parallel and the `install_dependencies` cache is cold, they each re-fetch. Consider ensuring `install_dependencies` always completes before verification fans out, and that its cache key is aggressive enough to stay warm across the merge-train cycle.

---

## Summary Table

| ID | Change | File | Impact | Effort |
|---|---|---|---|---|
| P1.1 | Fix `make` / `dtrace-provider` (add to `ignoredBuilds`) | `.yarnrc.yml` | Stops BUILD_COMPILE failures | Trivial |
| P1.2 | Fix ESLint `koa-bodyparser` resolution | service eslintrc | Stops TEST_FAILURE failures | Low |
| P1.3 | Retrieve 21 unknown failure traces |—(glab query) | Uncover hidden failure modes | Low |
| P2.1 | Set CI vars to `protected: true` | GitLab UI / API | Prevents credential leakage | Low |
| P2.2 | Rotate ACR secret before 2026-07-27 | Azure Portal + GitLab | Prevents auth outage | Medium |
| P2.3 | Migrate to OIDC Workload Identity | `build.sh` + Azure | Eliminates static ACR secret | High |
| P3.1 | Re-enable `resource_group` on release | `.gitlab-ci.yml:97` | Prevents release race condition | Trivial |
| P3.2 | Pin `docker:latest` → versioned tag | `build-pipelines.yml` | Reproducible builds | Low |
| P3.3 | Add retry to task build jobs | `build-pipelines.yml` | Reduces transient DinD failures | Low |
| P3.4 | Fix cleanup job scope | `.gitlab-ci.yml` | Prevents artifact accumulation | Low |
| P4.1 | Consolidate builds onto `.docker_build` | `build-pipelines.yml` | Reduces duplication | Medium |
| P4.2 | Fix sftp-loader `/*` → `//*` | `build-pipelines.yml` | Prevents missed build triggers | Trivial |
| P4.3 | Re-enable SonarQube quality gate | `.gitlab-ci.yml` | Restores quality blocking | Low |
| P4.4 | Enable mypy for workflows-api | `verification-pipelines.yml` | Catches Python type errors | Low |
| P4.5 | Add GitLab SAST template | `.gitlab-ci.yml` | Free security scanning | Low |

---

## Recommended Starting Point

Two one-line changes with immediate impact, safe to do today:

1. P3.1—restore `resource_group: deployment-repo` in `.gitlab-ci.yml:97`
2. P1.1—add `dtrace-provider` to `.yarnrc.yml` `ignoredBuilds`

These together address the race-condition risk and the most common documented failure mode without touching any image or infrastructure.
