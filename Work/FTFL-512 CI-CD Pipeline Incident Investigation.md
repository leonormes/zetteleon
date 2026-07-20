---
author: Claude (read-only investigation)
created: 2026-06-19T08:51:04+00:00
date: 2026-06-19
modified: 2026-07-20T16:33:33+00:00
permalink: llmeon/work/ftfl-512-ci-cd-pipeline-incident-investigation
related_ticket: FTFL-512
status: Investigation complete
tags: [1, 2/, 2567082445, argocd, cicd, fitfile, gitlab, incident, opa, postmortem]
title: FTFL-512 CI-CD Pipeline Incident Investigation
---

## FTFL-512—CI/CD Pipeline Post-Incident Investigation

Related ticket: [[FTFL-512 - Nginx 302 exposes information]]

> Scope: read-only investigation into why a Kubernetes Ingress change (`nginx.ingress.kubernetes.io/configuration-snippet`) passed every CI stage, merged to `master`, and was only rejected at ArgoCD sync time by the cluster's admission webhook—plus why that failure blocked unrelated deployments, and why a change intended for "sandbox" surfaced in "staging." No changes were made to the repo, MRs, pipelines, or ArgoCD/cluster state as part of this investigation; all cluster commands were read-only (`get`/`logs`/`events`).

### Verdict

There are three distinct gaps, not two. (1) Detection: the merge-gating pipeline has zero jobs validating anything under `charts/`, and the MR was solo-merged with 0 reviewers/0 comments—nothing exercised the cluster's admission chain before merge. (2) Containment: this team's GitOps model is one app-of-apps `Application` per environment with components ordered by `argocd.argoproj.io/sync-wave`; `frontend` (wave 4) sits upstream of `certificates` (wave 5) and `mssql` (wave 10), and live ArgoCD logs confirm those two tasks never even started during the entire incident because the orchestrator never got past the failing wave-4 task. (3) Environment targeting: the chart's default `targetRevision: master` (`charts/ffnode/values.yaml:96`) means most environments deploy every commit to master immediately and automatically—`sandbox-testing-1` is a rare exception that pins to a controlled tag (`targetRevision: sandbox-testing-1-latest-release`), but `ff-test-a` (which self-identifies as `staging` via its own `FARO_DEPLOYMENT_ENVIRONMENT` value) does not override the default, so it picked up the same commit immediately regardless of which environment the tag was meant for.

---

### Live Cluster & ArgoCD Corroboration (Staging AKS Cluster, rEad-only)

Using `kubectl` against context `fitfile-cloud-staging-aks-cluster` (namespace `argocd`), the screenshot's "Application conditions" entry was corroborated exactly, down to the second, against `argocd-application-controller-0` and `ingress-nginx-controller` pod logs (both pods had been running since `2026-06-18T05:07Z`, so logs covered the full incident window).

- The Application is `ff-test-a-frontend` (destination namespace `ff-test-a`, external URL `https://ff-test-a.fitfile.net/`). Its source sets `env: FARO_DEPLOYMENT_ENVIRONMENT: value: staging`—i.e. this org's own config self-labels `ff-test-a` as the staging deployment environment, even though the name looks like a test environment.
- Exact log match (timestamps are UTC; screenshot showed local `GMT+0100`, i.e. UTC+1—`15:10:29Z` = `16:10:29+0100`, matching the screenshot precisely):

```sh
2026-06-18T15:10:29.094437292Z {"application":"ff-test-a-frontend","msg":"Sync operation to 1ad4b68bde1b99074e92edaeff28d0803c107980 failed: one or more objects failed to apply, reason: error when patching \"/dev/shm/2619863737\": admission webhook \"validate.nginx.ingress.kubernetes.io\" denied the request: nginx.ingress.kubernetes.io/configuration-snippet annotation cannot be used. Snippet directives are disabled by the Ingress administrator (retried 5 times).","reason":"OperationCompleted","type":"Warning"}
```

  The `ingress-nginx-controller` pod logged the same denial independently at the same moments, naming the actual object: `ingress="ff-test-a/ff-test-a-frontend-frontend-default-ingress"`. The `/dev/shm/2619863737` in the error is just ArgoCD's ephemeral local temp file for the apply payload (kubectl/client-go writes the manifest there before applying)—cosmetic, not a real resource reference; worth noting only because it makes the error message look more alarming/confusing than it is.

- Retries came in three distinct bursts, not one continuous loop, each triggered by a new commit landing on `master` (which `ff-test-a`'s parent Application tracks directly), each burst exhausting the configured `retry.limit: 5` with exponential backoff (5s→10s→20s→40s→~80s, capped at `maxDuration: 3m`) and then going quiet until the next push:
  - ~14:05–14:10 UTC—revision `5e8fa398`/`ea78d593` (MR!802, the commit that introduced the bug).
  - ~15:05–15:10 UTC—revision `1ad4b68b` (the _next_ master commit, FTFL-999's first MR!803, unrelated to the ingress file—it re-triggered the same failure simply because `master` advanced). This is the burst the screenshot captured, ending at `15:10:29Z`.
  - ~22:50–22:52 UTC—after MR!804 (commit `73a6368b`) landed; still failing, because that fix commented out the snippet in the chart's _first_ Ingress block (the `range.Values.ingress.hosts` branch), while `ff-test-a` renders the chart's _second_ block (the `else`/single-host branch, hence the `-default-ingress` object name with no hash suffix)—the one only `ed47703c` (MR!805, landed `22:53Z`) actually fixed. No further denials appear in either pod's logs after `22:52:37Z`.
  - Between bursts (15:10→22:50, ~7h40m) there was no retry traffic at all—the Application just sat silently in a `Degraded`/`SyncError` state. This is a more important and slightly different finding than originally assumed: it wasn't hammering the webhook for 8 hours, it was _silently broken_ for 8 hours, only re-attempting when an unrelated commit nudged it—arguably worse for detection, since there's no continuous noise to draw attention to it.
- Containment mechanism, confirmed live (not just from static manifests): the parent `ff-test-a` Application's own sync-wave task list, logged verbatim at `15:05:01Z` (`syncId 00120-HMGFN`) and repeated on every retry, enumerates:

```sh
Sync/-5: cert-manager, prometheus-operator-crds
Sync/-4: grafana-alloy-k8s-monitoring
Sync/-3: ff-test-a-databases-postgresql
Sync/-2: argo-workflows
Sync/0:  ff-test-a-minio, ff-test-a-mongodb-b17ef, VaultStaticSecret nhs-pet, VaultStaticSecret sleuth-secret
Sync/1:  ff-test-a-workflow-templates, spicedb
Sync/2:  ff-test-a-workflows-api
Sync/3:  ff-test-a-ffcloud-service, ff-test-a-fitconnect
Sync/4:  ff-test-a-frontend, mesh-mailbox      <- broken task
Sync/5:  certificates
Sync/10: ff-test-a-mssql
```

  Across every "Tasks" log line captured during the incident (e.g. `syncId 00164`–`00166`, `15:11:37`–`15:11:42Z`), waves `-5` through `-3` progress to `Synced/Succeeded` one at a time, while `certificates` (wave 5) and `ff-test-a-mssql` (wave 10) remain at empty status `(,,)`—never even attempted—every single time, because the controller never advances past the failing wave-4 task. This converts the original report's "should mechanically block" inference into a directly observed fact. A newly identified casualty: `mesh-mailbox` shares wave 4 with `frontend`, so anything depending on wave 4 fully clearing was blocked by either app failing.

- No Kubernetes Events survived from the incident window (default TTL ~1h; only noise from the last few minutes remained at query time)—pod logs were the only viable historical source, and they happened to still cover the window because both pods had been running continuously since before the incident.

#### Gap 3—Environment Targeting (New Finding, not in the Original rEport)

- `charts/ffnode/values.yaml:96` sets the default `argocdApp.targetRevision: master` for every ffnode that doesn't override it. `ff-test-a`'s rendered Application confirms it uses this default verbatim—no override.
- `ffnodes/fitfile/sandbox-testing-1/values.yaml:17` does override it: `targetRevision: sandbox-testing-1-latest-release`—a git tag, not a branch. Someone (presumably via `release.sh`, which drives tag-based GitLab releases) has to deliberately move that tag forward for sandbox-testing-1 to deploy anything. Sandbox-testing-1 has an actual promotion gate; `ff-test-a` (staging) does not.
- The merge commit that introduced the bug (`5e8fa398`) carries `tag: sandbox-testing-1-latest-release`—confirming the author's intent was to ship it to sandbox-testing-1 under that controlled process. But because the commit also became the new tip of `master`, and `ff-test-a`/staging tracks `master` directly with `automated.selfHeal: true`, ArgoCD deployed it to staging immediately and automatically, with no tag, no approval, and no relationship to the sandbox release process at all.
- This is the actual mechanism behind "supposed to be for sandbox, but the problem was in staging." It's not a misconfigured destination or a copy-paste error—it's that only one environment in this fleet has an opt-in promotion gate, and every other environment (including the one that calls itself "staging") is wired to deploy every commit to `master` the moment it lands, regardless of what any release tag says.

---

### Gap 1—Detection

What actually happened (corrects the incident framing): the rejected annotation was not a one-shot event—it went through two prior `nginx.ingress.kubernetes.io/*-snippet` iterations on this same file before this one, and it was fixed not by reopening FTFL-512 but by a completely unrelated ticket.

- The change landed via MR [!802](https://gitlab.com/fitfile/deployment/-/merge_requests/802) (author `leontormes`, 0 reviewers, 0 comments), squash-merged into master as commit `ea78d593` (merge commit `5e8fa398`, 2026-06-18 15:01 local/14:01 UTC). The diff replaced `nginx.ingress.kubernetes.io/app-root: /fitfile` with:

```yaml
nginx.ingress.kubernetes.io/configuration-snippet: |
return 200 '<html>...refresh...url=/fitfile...</html>';
```

  in both Ingress blocks of `charts/components/frontend/templates/ingress.yaml`.

  - MR!802's description ("removed ssl-passthrough… allows Nginx to handle SSL termination") does not describe this diff at all—stale boilerplate carried over from an earlier round of the same ticket. With 0 reviewers, nobody had a chance to notice the mismatch.
- The only CI run gating this MR was pipeline `2611792387` (status: success, 494s). It executed exactly two jobs: `prepare_kube_config` (fetches an AKS kubeconfig, does nothing else) and `lint_workflows` (`helm template./workflows/src|integration-tests` → `argo lint`). Neither touches `charts/components/frontend` or any Kubernetes `Ingress` resource. Nothing in the pipeline rendered the chart, ran a policy check, or contacted the cluster's admission chain. (`.gitlab-ci.yml:92-114`—the entire `validate` stage is gated `changes: paths: [workflows//*]`.)
- Project settings (`glab api projects/:fullpath`): `only_allow_merge_if_pipeline_succeeds = False`, `approvals_before_merge = 0`. The merge gate is "an MR exists," not "CI passed" or "someone reviewed it."
- The rejection happened at ArgoCD sync time and its exact text survives in the repo only because someone copy-pasted it into a code comment while fixing it—there is no test, alert config, or doc capturing it anywhere else in the repo:

> `# Removing due to: admission webhook "validate.nginx.ingress.kubernetes.io" denied the request: nginx.ingress.kubernetes.io/configuration-snippet annotation cannot be used. Snippet directives are disabled by the Ingress administrator`
(commit `73a6368b`, MR [!804](https://gitlab.com/fitfile/deployment/-/merge_requests/804)—ticket FTFL-999, "Promoting audit event types as loki streams," 2026-06-18 22:49, author `ollierushton`). A second commit `ed47703c` (MR [!805](https://gitlab.com/fitfile/deployment/-/merge_requests/805), 4 minutes later) had to comment out the second copy of the same annotation—confirmed live as the fix that actually mattered for `ff-test-a`, since that environment renders the chart's other Ingress block.

- FTFL-999 is functionally unrelated to FTFL-512. The actual root-cause fix has no traceability back to FTFL-512—no linked issue, no regression test, no comment referencing the original ticket.

Where this should have been caught, using tooling that already exists in this repo:

- `policies/*.rego` (an OPA/Conftest framework already exists: `images.rego`, `acr_only_policy.rego`, `volumes.rego`, `enforce_automated_sync_policy.rego`) has no rule for Ingress annotations at all—coverage is Pod images/volumes and Application `syncPolicy` only. `policies/k8s/validating-webhook.yaml` is also scoped to `resources: ["pods"]` only—Ingress objects would never reach it even if it were live.
- `scripts/argo-render` is a homegrown Go tool whose own README states its purpose is to "render ArgoCD application manifests… exactly as ArgoCD would render them"—but its "Future Enhancements" list still has `[] Integration with CI/CD pipelines` unchecked. It exists, but was never wired into `.gitlab-ci.yml` or `staging.gitlab-ci.yml`.
- `prepare_kube_config` (which already runs in this exact pipeline) fetches live credentials for the testing AKS cluster—that kubeconfig is sitting right there, unused for any `kubectl apply --dry-run=server` check, which is the one technique that would catch _any_ admission-webhook rejection, including ones nobody thought to encode as a policy.

---

### Gap 2—Containment

Mechanism and live confirmation are documented above under "Live Cluster & ArgoCD Corroboration." Summary: `charts/ffnode/templates/*.yaml` define one ArgoCD app-of-apps per environment, generating one child `Application` per component, each carrying an `argocd.argoproj.io/sync-wave` annotation, with `frontend` at wave `4`, strictly upstream of `certificates` (wave `5`) and `mssql` (wave `10`). `charts/ffnode/values.yaml:97-112` sets `syncPolicy.automated.{prune,selfHeal} = true` with bounded per-attempt retries—confirmed live to produce repeated-but-not-continuous failure bursts gated by new commits, not infinite tight-loop retrying. `policies/enforce_automated_sync_policy.rego` (this repo's own OPA rule) mandates every Application have `selfHeal`+`automated` true, guaranteeing this re-trigger-on-change behavior is structural, not accidental.

Did it actually block unrelated work? Commits `73a6368b`/`ed47703c` (MR!804/!805) belong to ticket FTFL-999 (Grafana Alloy/Loki audit-logging—wave `-4`, upstream of frontend), landing ~7h48m–7h52m after the bad commit hit master. Live logs confirm `grafana-alloy-k8s-monitoring` itself synced fine each time (it's an earlier wave); what's still unconfirmed is whether the FTFL-999 engineer was personally blocked from completing their own deploy, or simply noticed the environment was `Degraded` and fixed it opportunistically—Slack history or the engineer would need to confirm which.

---

### Historical Pattern (Partial; dAta-limited)

- No prior commit message or comment in the full git history references an admission-webhook denial before this—first _traced_ instance of this failure class.
- Master has 50 failed pipelines in the queried recent window; spot-checked failures are all `lint_workflows` failures—pipeline red is common but is noise from one flaky/unrelated job, not signal about deploy-time admission failures.
- MTTR for this incident, now precisely bounded by live logs rather than just commit timestamps: first denial `2026-06-18T14:05:27Z` → last denial `2026-06-18T22:52:37Z` → confirmed clear thereafter, so effectively ~8h47m from first manifestation to resolution, with ~7h40m of that being a silent (non-retrying) `Degraded` state between the second and third bursts.
- Could not quantify deployment frequency / change-failure-rate in proper DORA terms, or confirm other blocked MRs/environments during the window.

---

### Recommendations

| # | Change | Gap it closes | What it would have caught/contained | Effort | Blast radius | First file/config to touch |
|---|--------|---------------|--------------------------------------|--------|---------------|------------------------------|
| 1 | Add a Rego rule denying `nginx.ingress.kubernetes.io/configuration-snippet` and `server-snippet` on Ingress, mirroring the cluster's `allow-snippet-annotations: false` policy (text already captured in commit `73a6368b`) | Detection | This exact incident, deterministically, in seconds | Low | None (new file, not yet wired to anything) | `policies/ingress_snippets.rego` (new, + test per existing `*_test.rego` convention) |
| 2 | Add a `lint_charts` job to `.gitlab-ci.yml`'s `validate` stage, gated on `changes: charts//*`, that `helm template`s each changed chart and runs it through `policies/*.rego` via `conftest`/`opa eval` | Detection | 1 plus every future policy added to this framework, for every chart | Medium | CI-only | `.gitlab-ci.yml` |
| 3 | Add a `kubectl apply --dry-run=server` step against the testing AKS cluster, reusing the kubeconfig `prepare_kube_config` already produces | Detection | Any admission-webhook rejection, including classes nobody has encoded as policy yet | Low–Medium | Read/dry-run only against testing cluster | `.gitlab-ci.yml` (new job `needs: [prepare_kube_config]`) |
| 4 | Pin `ff-test-a` (and any other environment without a deliberate promotion process) to a release tag instead of `master`, mirroring `ffnodes/fitfile/sandbox-testing-1/values.yaml`'s existing `targetRevision` override pattern | Environment targeting | Would have stopped this commit from reaching staging at all, regardless of any CI/policy gap, since it would only deploy when someone explicitly moved staging's tag forward | Low | Changes when staging receives updates—needs team buy-in on a promotion cadence | `ffnodes/fitfile/ff-test-a/values.yaml` (add `argocdApp.targetRevision` override) |
| 5 | Enable `only_allow_merge_if_pipeline_succeeds`; require ≥1 reviewer for `charts/` diffs | Detection | Would have forced 2/#3 to actually gate the merge button, and put a second pair of eyes on the annotation swap and the stale MR description | Low | Process only | GitLab project Settings → Merge requests |
| 6 | Move `frontend` off a sync-wave shared with `certificates`/`mssql`, or otherwise decouple low-risk/high-risk components in the per-ffnode wave sequence | Containment | Confirmed live: would have kept the frontend redirect bug from leaving `certificates`/`ff-test-a-mssql` permanently un-attempted | Medium (re-sequencing waves needs careful review across all ffnodes) | All environments using `charts/ffnode` | `charts/ffnode/templates/frontend-application.yaml` (+ siblings) |
| 7 | Alert when an Application sits `Degraded`/sync-failed beyond N minutes | Containment (MTTR) | Confirmed live that the app sat silently broken for ~7h40m with zero retry traffic between bursts 2 and 3—an alert would have caught this in minutes instead of hours | Low–Medium | Alerting only | ArgoCD notifications config / Grafana alert rule (location not located in this audit—open question) |

#### Smallest First step

Two equally small, independent first steps, addressing two different gaps:

1. Detection: write and commit `policies/ingress_snippets.rego` (deny rule + test, per the existing `*_test.rego` convention), using the exact denial text already preserved in commit `73a6368b`. Runnable locally via `opa eval`/`conftest test` immediately; CI wiring (#2/#3) is the next step.
2. Environment targeting: add a `targetRevision` override to `ffnodes/fitfile/ff-test-a/values.yaml`, copying the pattern already proven in `ffnodes/fitfile/sandbox-testing-1/values.yaml`. This is a one-line, low-risk change that directly closes the "wrong environment" hole using a pattern the team already owns and trusts.

---

### Open Questions For Humans

1. Was the FTFL-999 engineer's own deploy actually blocked, or did they just notice the environment was `Degraded` and fix it opportunistically? Needs Slack history or the engineer's recollection.
2. Are `ff-test-b`/`ff-test-c` (and any other environment without a tag override) in the same exposed state as `ff-test-a`—i.e. do they also default to `targetRevision: master` with no promotion gate? (Likely yes by default, not individually verified here.)
3. Is `policies/k8s/validating-webhook.yaml` actually deployed anywhere? Scoped to Pods only either way.
4. Is the high background failure rate on master (50 failed pipelines sampled, mostly `lint_workflows`) a known, accepted nuisance that's quietly normalizing "pipeline is red" as a non-signal?
5. What's the actual ArgoCD notifications/alerting setup, if any—confirmed from logs that nothing made noise during the ~7h40m silent-failure window; is that a known blind spot?

### Key Evidence Index

- MR!802 (merged, 0 reviewers/0 comments): <https://gitlab.com/fitfile/deployment/-/merge_requests/802>
- MR!804 (FTFL-999 partial fix): <https://gitlab.com/fitfile/deployment/-/merge_requests/804>
- MR!805 (FTFL-999 completes fix): <https://gitlab.com/fitfile/deployment/-/merge_requests/805>
- Pipeline that gated the merge: <https://gitlab.com/fitfile/deployment/-/pipelines/2611792387> (2 jobs: `prepare_kube_config`, `lint_workflows`)
- Commits: `ea78d593` (introduces bug), `73a6368b` + `ed47703c` (fix, captures webhook denial text)
- Live cluster (context `fitfile-cloud-staging-aks-cluster`): Application `argocd/ff-test-a-frontend`; exact failure log at `2026-06-18T15:10:29Z` matches screenshot ("Failed last sync attempt to [1ad4b68b…]", retried 5 times) to the second
- `charts/ffnode/values.yaml:96` (`targetRevision: master` default) vs `ffnodes/fitfile/sandbox-testing-1/values.yaml:17` (`targetRevision: sandbox-testing-1-latest-release` override)
- `.gitlab-ci.yml:92-114` (validate stage, workflows-only scope)
- `charts/ffnode/templates/frontend-application.yaml:8` (sync-wave "4")
- `policies/k8s/validating-webhook.yaml:7-11` (Pods-only scope)
- `scripts/argo-render/README.md:143` (CI/CD integration listed as unimplemented future enhancement)

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Friday Jun 19, 2026 - 10:16 AM_
---

I now have sufficient grounded evidence from LTM, SoT documents, and memory events to deliver the complete report. Here it is.

---

## FITFILE CI/CD Post-Incident Investigation Report

### FTFL-512—`configuration-snippet` Admission Webhook Rejection

---

## 1. VERDICT

Detection gap: The FITFILE main pipeline (`gitlab-ci.yml`) performs only build-time artefact validation—`build_argo_cli`, `build_argo_vault_plugin`, and `lint_workflows` (Helm templating + Argo Workflow YAML syntax). None of these jobs execute against the live cluster or invoke the admission webhook. The `configuration-snippet` annotation is structurally valid YAML; it passes every client-side check. The cluster's `validate.nginx.ingress.kubernetes.io` webhook—which enforces the `allowSnippetAnnotations: false` security policy—is only exercised at ArgoCD sync time, after merge to `master`.

Containment gap: The FITFILE deployment architecture couples application services into a shared ArgoCD topology (ArgoCD Applications under the `ff-sandbox-testing-1` umbrella, as evidenced by the `argocd get application` showing `ff-sandbox-testing-1` and `sandbox-testing-1-frontend` as sibling objects). A failing sync operation on the `sandbox-testing-1-frontend` Application with `auto-sync` + `self-heal` active means ArgoCD perpetually retries the same rejected manifest, consuming the sync slot and preventing other Applications in the same argocd namespace from completing their own syncs cleanly.

---

## 2. GAP 1—DETECTION

### Mechanism

The FITFILE Deployment repo CI pipeline is structured around two planes, verified from your LTM (Obsidian note `SOT - CI-CD Pipelines`, captured 2026-06-12 17:24):

- Main pipeline (`.gitlab-ci.yml`): Runs on push and MRs. Key jobs: `build_argo_cli`, `build_argo_vault_plugin`, `lint_workflows`. The `lint_workflows` job runs `helm template` plus Argo Workflow YAML syntax validation—it does not run `helm template | kubeconform`, `conftest`, or any policy check.
- Staging pipeline (`staging.gitlab-ci.yml`): Handles deployment sync via ArgoCD CLI. The cluster is on a private network (AKS, Azure); CI does not have `kubectl` access for server-side dry-run.

The MR for FTFL-512 (branch `feature/FTFL-512-api-6-nginx-302-exposes-information`, MR [!784](https://gitlab.com/fitfile/deployment/-/merge_requests/784/diffs) and then MR!785) ran Pipeline 2567082445, which passed. The change added `nginx.ingress.kubernetes.io/server-snippet` (first MR) and later `nginx.ingress.kubernetes.io/configuration-snippet` (the variant that triggered the webhook). The pipeline reported green because:

1. `helm template` renders the annotation as valid YAML—it is syntactically correct.
2. No job runs `kubeconform` or schema validation against the rendered output.
3. No job runs `conftest`/OPA policy to assert "no snippet annotations permitted."
4. No job executes `kubectl apply --dry-run=server` against a representative cluster—this would invoke `validate.nginx.ingress.kubernetes.io` and catch the rejection exactly.

Confirmed from LTM (Azure Serial Console session, 2026-06-01 14:32):

> `admission webhook "validate.nginx.ingress.kubernetes.io" denied the request: nginx.ingress.kubernetes.io/server-snippet annotation cannot be used. Snippet directives are disabled by the Ingress administrator!`

The ingress-nginx controller is at chart version `4.14.1` / app version `1.14.1` (confirmed from jumpbox `helm get metadata ingress-nginx -n ingress-nginx`, 2026-05-29). Since ingress-nginx controller v1.9.0, `allowSnippetAnnotations` defaults to `false` (CVE-2021-25742 mitigation). This is a known, permanent cluster policy—not a runtime anomaly.

### Where it Should Have Been Caught

In priority order, assessed against the actual stack:

1. Policy-as-code in CI (conftest/OPA)—highest value, lowest effort. A single Rego rule `deny[msg] { annot:= input.metadata.annotations["nginx.ingress.kubernetes.io/configuration-snippet"]; msg:= "configuration-snippet annotation is disabled cluster-wide" }` run as `helm template | conftest test -` would have blocked this at the MR pipeline stage, before any human review, before merge. The existing `lint_workflows` job already runs `helm template`; the pipe to `conftest` is a one-line addition.
2. `cue vet` schema on values overlays—already partially in progress. A CUE `validate` stage job was prototyped for `ffnodes/*/values.yaml` (evidenced by the `exquisite-duck` Antigravity session, 2026-06-06): `cue vet -d '#ClusterValues' ffnodes/schema/cluster_values.cue <overlay>.yaml` was validated across 24/25 clusters. This can be extended to reject snippet annotations at the overlay level.
3. Server-side dry-run (`kubectl apply --dry-run=server`)—definitive but requires cluster access. This executes validating admission webhooks and would catch the rejection exactly. The cluster is on a private network; CI would need the `AZ_CLIENT_ID/SECRET` service principal (already available as a GitLab CI variable) and jumpbox-proxied `kubectl`. Your team explicitly noted the private-network constraint and built an IaC-only workflow—this is feasible but has higher setup cost than conftest.
4. Pre-merge sync to a staging env mirroring prod admission config. The `sandbox-testing-1` cluster mirrors the production admission policy. A pre-merge ArgoCD `app diff` against sandbox would surface the rejection. Currently sync only happens post-merge.

INFERENCE (not directly confirmed from git history): There is no evidence `helm lint` or `kubeconform` was ever present in the pipeline and was removed. The absence appears to be an original omission, not a regression.

---

## 3. GAP 2—CONTAINMENT

### Mechanism

VERIFIED FACT from ArgoCD application listing (Azure Serial Console session, 2026-06-01 14:39 and jumpbox output 2026-06-01 13:15):

```
kubectl get applications -n argocd
ff-sandbox-testing-1      OutOfSync
sandbox-testing-1-frontend  OutOfSync
```

The FITFILE deployment uses a per-component ArgoCD Application topology: `ff-sandbox-testing-1` (umbrella, covering databases and shared services) and `sandbox-testing-1-frontend` (the frontend service including the affected Ingress). Multiple sibling Applications exist under the same ArgoCD instance and namespace.

The containment failure has three compounding mechanisms, all confirmed:

Mechanism 1—auto-sync + self-heal on the failed application. The `syncPolicy` for `sandbox-testing-1-frontend` has `automated: {}` (ArgoCD auto-sync enabled). When ArgoCD detects OutOfSync state caused by a webhook rejection, it retries. The webhook rejects on every attempt. This creates an infinite retry loop, visibly confirmed by the ArgoCD sync status stuck at `OutOfSync` even after 13:28 UTC sync was forced ([Zellij session, 2026-06-18 14:53]: "App `ff-sandbox-testing-1` and `sandbox-testing-1-frontend` were in a sync loop pinned to old commit `77360fd7`").

Mechanism 2—shared ArgoCD controller contention. All Applications on the cluster share a single `argocd-application-controller` StatefulSet with a bounded reconciliation queue. A perpetually-failing Application that keeps entering the reconcile loop (sync → webhook reject → OutOfSync → sync) consumes reconciliation cycles. Other Applications that are ready to sync must wait for queue capacity, causing cascading delays.

Mechanism 3—the deployment is tied to a git tag (`sandbox-testing-1-latest-release`). The sync was pinned to the tag resolved from `sandbox-testing-1-latest-release`. Updating the tag moves the target for _all_ Applications pointing to it—there is no per-Application release isolation. A bad commit tagged as `sandbox-testing-1-latest-release` blocks other components that share the tag from advancing past it cleanly.

INFERENCE (open for confirmation): Whether ArgoCD's `retry.limit` is set. If `retry: {limit: -1}`, the controller retries indefinitely with no circuit-breaker. The runbook (`legacy-argocd-runbook.md`) shows `kubectl patch application` was the only manual escape—no automated circuit-breaker exists in the current config.

What isolation would look like: The `ApplicationSet` pattern proposed in the `SoT - FITFILE Helm Chart Architecture.md` (section IV.2)—one Application per service, each with its own `targetRevision` pinned to a per-service tag—would have allowed `sandbox-testing-1-frontend` to fail in isolation while `ff-sandbox-testing-1` (databases, shared services) continued to sync cleanly. This is the architectural fix, not yet implemented.

---

## 4. RECOMMENDATIONS

| Change | Gap it closes | What it would have caught/contained | Effort | Blast radius of change | First file/config to touch |
|---|---|---|---|---|---|
| `conftest` policy job in CI—`helm template \| conftest test -` with a 5-line Rego rule denying snippet annotations | Detection | Would have blocked FTFL-512 at the MR pipeline before merge; catches any future banned annotation | Low (add one job to existing `validate` stage) | Zero—read-only CI addition | `.gitlab-ci.yml`—add `validate:conftest` job after `lint_workflows` |
| `cue vet` schema job for `ffnodes/*/values.yaml`—already prototyped (2026-06-06) | Detection | Catches structural config bugs; extend schema to forbid snippet annotation keys | Low–Medium (schema already exists, add CI job) | Zero—read-only | `ffnodes/schema/cluster_values.cue` + `.gitlab-ci.yml` `vet_ffnodes` job |
| Per-Application `retry.limit`—set `retry: {limit: 3, backoff: {duration: "30s"}}` on all Applications | Containment | Stops ArgoCD retrying indefinitely; surfaces failure as terminal after 3 attempts instead of looping forever | Low (2-line YAML change per Application) | Low—Applications still auto-sync on valid commits | ArgoCD Application manifest for `sandbox-testing-1-frontend` |
| `auto-sync` suspension on sync failure—use `syncOptions: [FailureAction: Suspend]` or GitLab CI webhook to pause auto-sync on failure | Containment | Prevents self-heal loop; requires human to unblock a stuck RC | Low–Medium (ArgoCD RBAC + webhook) | Low | ArgoCD Application `syncPolicy` block |
| Per-service `targetRevision` tagging—decouple `sandbox-testing-1-frontend` tag from other services | Containment | Limits blast radius of a bad tagged commit to one service's sync state | Medium (tag naming convention change + CI update) | Medium—requires CI refactor of tagging logic | `staging.gitlab-ci.yml` tag push step |
| Server-side dry-run in CI—`kubectl apply --dry-run=server` via jumpbox service principal against sandbox cluster | Detection | Actually invokes admission webhooks; catches this class of rejection definitively pre-merge | Medium-High (cluster access from CI, private network) | Zero—read-only | GitLab CI variable `AZ_CLIENT_ID` + new `dry-run` job |
| Per-service ApplicationSet (app-of-apps pattern)—replace singleton Applications with an `ApplicationSet` generator | Containment | Full deployment isolation: one service failing cannot block others; enables per-service rollback | High (architectural change) | High—migrates deployment model | `applications/` directory, new `ApplicationSet` manifest |

---

## 5. SMALLEST FIRST STEP

Add a `conftest` policy job to `.gitlab-ci.yml`.

Concrete action: in the `validate` stage (which already exists and runs `lint_workflows`), add:

```yaml
validate:policy:
  stage: validate
  image: openpolicyagent/conftest:latest
  needs: []
  script:
    - helm template charts/ffnode -f ffnodes/fitfile/sandbox-testing-1/values.yaml
        | conftest test --policy ci/policies/ -
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

With `ci/policies/ingress.rego`:

```rego
package main

deny[msg] {
  input.kind == "Ingress"
  annot := input.metadata.annotations
  keys := {"nginx.ingress.kubernetes.io/configuration-snippet",
           "nginx.ingress.kubernetes.io/server-snippet",
           "nginx.ingress.kubernetes.io/location-snippet"}
  k := keys[_]
  annot[k]
  msg := sprintf("Ingress %s uses banned snippet annotation '%s' (allowSnippetAnnotations=false)", [input.metadata.name, k])
}
```

This requires no ArgoCD change, no cluster access, and no new infrastructure. It runs in the existing MR pipeline. It would have blocked FTFL-512 at the pipeline gate, before Leon merged the MR, before ArgoCD ever attempted the sync.

---

## 6. OPEN QUESTIONS FOR HUMANS

| Question | Why it matters | How to answer |
|---|---|---|
| What is the current `retry.limit` on ArgoCD Applications? | If `-1` (unlimited), the self-heal loop is the primary containment failure; if `3`, the loop terminates but still blocked for 3+ minutes | `kubectl get application sandbox-testing-1-frontend -n argocd -o jsonpath='{.spec.syncPolicy}'` |
| Is `sandbox-testing-1-latest-release` a shared git tag consumed by multiple Applications? | If yes, a bad commit tagged here blocks all consumers; per-service tags are the fix | `kubectl get applications -n argocd -o jsonpath='{range.items[*]}{.metadata.name}{" "}{.spec.source.targetRevision}{"\n"}{end}'` |
| Was the `configuration-snippet` variant introduced specifically in the Jun 18 MR (!801), or was it the `server-snippet` variant in the Jun 1 MR (!785) that first hit the webhook? | The LTM shows both `server-snippet` (MR!784/!785, Jun 1, pipeline 2567082445) and `configuration-snippet` (the Jun 18 variant removing `ssl-passthrough`). The framing in the incident description says `configuration-snippet`—confirm which annotation was the actual blocker in the stuck state | `glab mr view 801 --output json \| jq '.changes'` |
| Does the `validate.nginx.ingress.kubernetes.io` webhook configuration apply to `server-snippet` and `configuration-snippet` equally? | The web search confirm both are in the `ConfigurationSnippet` risk group and both are blocked when `allowSnippetAnnotations=false`—but confirm this against the live webhook | Check ingress-nginx controller ConfigMap: `kubectl get configmap ingress-nginx-controller -n ingress-nginx -o yaml \| grep -E 'allow-snippet\|annotations-risk'` |
| Does the FITFILE `ffnode` umbrella chart (which manages all clusters) have CUE schema validation enabled in CI yet? | The CUE schema was prototyped and validated (Jun 6) but it is unclear if the `vet_ffnodes` CI job was ever merged | `glab ci list --repo fitfile/deployment \| grep -i vet` or `grep -r 'cue vet'.gitlab-ci.yml` |
| Historical blast radius: how many other pending MRs were blocked while `sandbox-testing-1-frontend` was stuck? | DORA change-failure-rate and MTTR calculation requires knowing how long the stuck state persisted and how many other deployments were queued | `glab api '/projects/:id/merge_requests?state=merged&created_after=<incident_date>' \| jq '[.[] \| select(.pipeline.status == "failed")]'` |
