---
created: 2026-08-24T15:31:29+00:00
modified: 2026-08-24T17:52:31+00:00
permalink: llmeon/00-inbox/fitfile-pipeline-notes
title: fitfile_pipeline_notes
type: note
---

## FITFILE CI/CD Pipeline - Miro Board Notes

### Pipeline Stages

#### 1. Local Development

- Dev environment setup
- Unit Tests
- Integration Tests
- Lint
- Manual Checks
- Claude Code
- AI / Automation (Renovate)
- npm audit

Local Problems:

- Dev env difficult, many moving parts
- Have we shift-left enough
- Renovate PRs cannot be blindly merged
- Multiple repositories require orchestration for dev env

Local Improvements:

- (No improvements listed for Local stage)

---

#### 2. Feature Branch

- Unit Tests
- Frontend Integration tests (Playwright)
- Frontend Interaction tests (Storybook)
- Frontend Build
- Lint
- Storybook build
- verify rest scheduler (?)
- npm audit

Feature Branch Problems:

- When should SonarQube run
- npmAuditIgnore ever growing list
- Feature Flags not visible
- PR approval process, small team

Feature Branch Improvements:

- (No improvements listed for Feature stage)

---

#### 3. Merge Train

- API (integration) Tests
- Data Pipeline integration Tests
- Migration Tested
- Release Candidate Image Builds
- Terraform Cloud for Infra

Merge Train Problems:

- No parallelism - Bottleneck
- API Tests Flakey
- No resource limits on integration test pods
- No way to pass image version to tests - just uses the argocd sync
- No Build Cache
- Low coverage of API Tests and Data Pipeline Tests
- Concurrent pipelines cause race conditions

Merge Train Improvements:

- Parameterize Integration tests to parallize
- Write more tests on pipeline

---

#### 4. Staging Release

- Full Image Build (again)
- Images Pushed to ACR
- Deployment Chart Tags incremented
- Package repo version file incremented
- Terraform Cloud for Infra
- Local Terraform for helm-platform

Staging Release Problems:

- No Build Cache
- ACR Push Secret expires and breaks pipeline - requires manual update
- Upgrading private resources
- Test & Staging seem interchangeable

Staging Release Improvements:

- Our own GitLabs Runners - for build cache
- Publish our charts to ACR

---

#### 5. Production Release

- Move per customer latest-release tag for ArgoCD
- Terraform Cloud for Infra
- Local Terraform for helm-platform
- Tag

Production Release Problems:

- No rollback procedure (WHEN THERE IS A MIGRATION)
- Each environment has slightly different config - burden to assess impact of upgrades across all environments
- No inbound connectivity to private clusters, without a bastion

Production Release Improvements:

- Feature flags (experimental)
- Ephemeral envs per branch

---

#### 6. Customer Release

- Move per customer latest-release tag for ArgoCD
- Terraform Cloud for Infra
- Local Terraform for helm-platform
- Manually Checking UI

Customer Release Problems:

- Each customer is manually tagged
- Difficult to see overview of clients
- Stability of envs, esp for Demo's
- Database connectivity for demo/test/etc
- Customer Deployment config changes require a new release

Customer Release Improvements:

- Move Customer Config into their own Repositories

---

### General/Cross-Stage Problems

#### Root Problems (Critical)

- Pipelines are Slow
- Pipelines are Flakey
- 1 concurrent pipeline at a time
- Builds are slow

#### Process Problems

- Not many people can manage deployments
- Assuredness of deployments
- Monorepo needs non-blocking pipeline (i.e. we must solve HEAD commits blocking)
- 🔴 00:19:02 time to run (frontend only)

#### Build & Infrastructure Problems

- All ACR builds are AMD64 - requires rebuilds
- No Build Cache (mentioned multiple times)
- No SBOM
- No Release Notes
- 3 disparate ways to deploy (infra/platform/application)
- Unable to cherrypick what we want to release
- Charts are not built in ACR - no proper versioning
- Stacked PRs (?)

#### Stability & Connectivity

- Database connectivity for demo/test/etc
- Stability of envs, esp for Demo's

---

### Cross-Cutting Improvements

#### Quick Wins (Light Green)

- Move Customer Config into their own Repositories
- Our own GitLabs Runners - for build cache
- Parameterize Integration tests to parallize
- Publish our charts to ACR
- Write more tests on pipeline

#### Experimental/Future Ideas (Yellow)

- Ephemeral envs per branch
- Feature flags (experimental)

#### Epic Ideas (Light Green - Priority)

- 🚀 LETS DO THIS!! (Rocket emoji highlights priority initiatives)

---

### Problem Analysis Structure

#### Root Causes (Yellow/Orange Sticky Notes)

- These appear to be organized by symptom (Problem) → Root Causes → Effects

#### Color Coding Summary

- 🟡 Light Yellow: Frontend/Local testing, code quality
- 🟠 Orange: Merge Train testing, platform readiness checks
- 🔵 Cyan: Staging/Release infrastructure & deployment
- 🟣 Violet: Production Terraform & deployment steps
- 🔴 Red: Customer Release & deployment issues
- 🟢 Green: General problems & architectural concerns
- 🟢 Light Green: Improvement suggestions
- 🟡 Yellow: Experimental/future improvements

---

### Key Observations

1. Performance is a bottleneck: Multiple stages reference slow builds and lack of parallelism
2. Test coverage gaps: API Tests and Data Pipeline Tests have low coverage
3. Infrastructure complexity: Three disparate ways to deploy (infra/platform/application)
4. Deployment process: Manual steps for customer tagging; difficult visibility
5. Build caching: Missing at multiple stages; identified improvement opportunity
6. Flakey tests: API tests and integration tests need stabilization
7. Dependency management: Growing npmAuditIgnore list; Renovate PRs need human review
8. Configuration management: Customers require manual tagging; config changes require full releases

---

### Next Steps for Refinement

- [ ] Prioritize improvements by impact & effort
- [ ] Assign owners to each improvement epic
- [ ] Break down large initiatives (e.g., "Our own GitLabs Runners") into tasks
- [ ] Define success metrics for each improvement
- [ ] Timeline planning for implementation

Here's the full cross-reference instead—happy to save it as a standalone file somewhere I _do_ have write access (scratchpad, or this deployment repo) if you want a copy, and you can route it into the vault yourself however your ingest process expects.

### Cross-reference: Miro Board Items → FTFL-971 Tickets

#### Directly Addressed

|Miro item|Ticket(s)|
|---|---|
|"ACR Push Secret expires and breaks pipeline—requires manual update" (Staging Release)|[FTFL-978](https://fitfile.atlassian.net/browse/FTFL-978)/[979](https://fitfile.atlassian.net/browse/FTFL-979)/[980](https://fitfile.atlassian.net/browse/FTFL-980)/[981](https://fitfile.atlassian.net/browse/FTFL-981)—OIDC federation replaces the static, expiring ACR password entirely. This is the strongest single match on the board.|
|"🔴 00:19:02 time to run (frontend only)"|[FTFL-988](https://fitfile.atlassian.net/browse/FTFL-988)—this is the exact complaint the ticket's measured-evidence comment re-confirms (625s warm / 1423s cache-miss), with a root-cause diagnosis (yarn cache not mounted into the Docker build context) the Miro note didn't have.|
|"No Build Cache" (Merge Train + Staging Release + Build & Infra, mentioned 3×)|[FTFL-987](https://fitfile.atlassian.net/browse/FTFL-987) (deployment Argo images), [FTFL-988](https://fitfile.atlassian.net/browse/FTFL-988) (InsightFILE yarn)|
|"All ACR builds are AMD64—requires rebuilds"|[FTFL-988](https://fitfile.atlassian.net/browse/FTFL-988)—directly engages with this, but lands on "keep pinning `linux/amd64`, don't build multi-arch speculatively, since runners and AKS are already amd64"—an answer, not the fix the note seems to want. Worth flagging back to whoever raised it on the board in case there's an Apple Silicon dev-machine use case this doesn't cover.|
|"Have we shift-left enough" (Local Dev)|[FTFL-985](https://fitfile.atlassian.net/browse/FTFL-985)/[986](https://fitfile.atlassian.net/browse/FTFL-986)—Trivy/SAST/Secret-Detection/Dependency-Scanning gates before push directly answer this for the security dimension.|

#### Partially / Indirectly Related

|Miro item|Relation|
|---|---|
|"1 concurrent pipeline at a time" (Root Problem) + "No parallelism–Bottleneck" (Merge Train) + "Concurrent pipelines cause race conditions"|Root cause now documented on [FTFL-897](https://fitfile.atlassian.net/browse/FTFL-897) (pre-existing ticket, found during this work, not created by it)—the `resource_group: staging` lock. Referenced as a caveat on [FTFL-983](https://fitfile.atlassian.net/browse/FTFL-983). No fix ticket exists yet for the throughput problem itself—FTFL-897 is still investigation-stage.|
|"When should SonarQube run" / "npmAuditIgnore ever growing list"|[FTFL-986](https://fitfile.atlassian.net/browse/FTFL-986) removes the `\| true`/`allow_failure` that currently makes both silent—forces the question to be answered, doesn't answer it.|
|"Assuredness of deployments" (Process Problem)|No single ticket, but the epic's overall thrust (FTFL-975 pipelines-must-succeed, FTFL-984 merge-train verification, FTFL-989/990 telemetry) is aimed squarely at this.|
|"No way to pass image version to tests—just uses the argocd sync"|Touches the same mechanism as [FTFL-991](https://fitfile.atlassian.net/browse/FTFL-991)/[972](https://fitfile.atlassian.net/browse/FTFL-972) (`STAGING_VALUE_OVERRIDES`/`get_staging_images.sh`), but those fix leaks/silent failures in that mechanism, not the design limitation the note is describing.|
|"No SBOM"|Not in this epic—lives on the pre-existing [FTFL-893](https://fitfile.atlassian.net/browse/FTFL-893) (SBOM/vuln-finding retention, under the separate FTFL-865 epic). Trivy scanning added by FTFL-985/986 could produce SBOM as a side effect but wasn't scoped that way.|

#### Not addressed—genuine Gaps, out of Scope for FTFL-971

Everything below was either explicitly out of scope for a CI/CD auth-and-security hardening epic, or not something a pipeline change fixes:

- Dev env complexity, multi-repo orchestration (Local Dev)
- Renovate PR review burden, feature-flag visibility, small-team PR approval process (Feature Branch)
- API/integration test flakiness, low test coverage, pod resource limits (Merge Train)
- "Test & Staging seem interchangeable" (Staging)
- Rollback procedure, per-environment config drift, bastion/private-cluster connectivity (Production)
- Everything under Customer Release (per-customer tagging, client overview, demo env stability, config-per-release)
- "Monorepo needs non-blocking pipeline / solve HEAD commits blocking" (Process)
- No release notes, 3 disparate deploy paths, can't cherry-pick releases, charts not versioned in ACR, stacked PRs (Build & Infra)
- Database connectivity for demo/test envs
- "Our own GitLab runners", "Move Customer Config into their own repositories", "Publish our charts to ACR" (Quick Wins)
- Ephemeral envs per branch, feature flags (Experimental Ideas)

That's a genuinely large remainder—the Miro board was a full pipeline retro across all six stages; FTFL-971 only ever covered auth/secrets, merge-gate honesty, shift-left scanning, build caching, and telemetry. Worth deciding whether the rest becomes a second epic, or stays as backlog the board itself already tracks.
