---
classification: Blameless post-incident review
created: 2026-06-19T09:52:25+00:00
date: 2026-06-19
modified: 2026-07-04T10:51:36+00:00
permalink: llmeon/30-library/200-projects/ftfl-512-cicd-incident-report
project_name: Pipeline
related_tickets: [FTFL-999]
sources: Two independent read-only investigations (live-cluster probe + LTM/SoT synthesis),
  reconciled
status: Findings consolidated
tags: [1, 1/, 2, 3, 4, 5, 6/]
ticket: FTFL-512
title: FTFL-512_CICD_Incident_Report
---

## TL;DR

A known-bad Ingress change merged, deployed to the wrong environment, and stalled unrelated deployments for ~8¾ hours. Three _independent_ gaps had to line up for that to happen—fixing any one alone would have stopped or contained it:

1. Detection—No CI job validates anything under `charts/`, and the merge button is gated on neither CI nor review. The change is structurally valid YAML, so every client-side check passed. The only thing that enforces the cluster's `allowSnippetAnnotations: false` policy is the admission webhook—exercised at ArgoCD sync, _after_ merge.
2. Containment—Each environment is a single app-of-apps whose child Applications sync in `sync-wave` order. `frontend` (wave 4) failed, so every later wave (`certificates` w5, `mssql` w10) and its wave-4 sibling `mesh-mailbox` were never even attempted. This was _not_ an infinite retry loop—it was a head-of-line block followed by ~7h40m of silent `Degraded` state with no alert.
3. Environment targeting—Only `sandbox-testing-1` pins to a release tag. Every other environment—including the one that self-labels `staging` (`ff-test-a`)—defaults to `targetRevision: master` with self-heal, so it deployed the bad commit the instant it hit `master`, with no tag, no gate, and no relationship to the sandbox release the author intended.

Highest-leverage fix: a ~5-line Rego policy mirroring the cluster's snippet ban, run in the MR pipeline. It would have failed FTFL-512 deterministically, pre-merge, in seconds.

> Blameless framing: the introducing MR was solo-merged by a single engineer with no reviewer—but that is the _finding_, not the cause. The system permitted a chart change to merge with zero validation and zero review. Every recommendation below targets the system, not the person.

---

## 1. What Happened

The change replaced a safe built-in redirect annotation with a snippet annotation in `charts/components/frontend/templates/ingress.yaml`:

```yaml
# before
nginx.ingress.kubernetes.io/app-root: /fitfile
# after
nginx.ingress.kubernetes.io/configuration-snippet: |
  return 200 '<html>…meta refresh…url=/fitfile…</html>';
```

`configuration-snippet` is rejected cluster-wide by the ingress-nginx admission webhook (`validate.nginx.ingress.kubernetes.io`), because `allowSnippetAnnotations` has defaulted to `false` since controller v1.9.0 (CVE-2021-25742 mitigation). The cluster runs ingress-nginx chart `4.14.1` / app `1.14.1`. This is a permanent, known security policy, not a runtime anomaly—so the rejection was deterministic and entirely predictable from the diff alone.

The change passed the only CI run that gated it (pipeline `2611792387`, _success_, 2 jobs), merged to `master`, was auto-deployed to `ff-test-a` (staging) by ArgoCD, rejected at sync, and then sat broken—blocking later sync-waves—until an unrelated ticket (FTFL-999) happened to comment the annotation out.

### Recurrence (Key Synthesis fInding)

This is not a first occurrence. The snippet rejection has now happened across at least two iterations of FTFL-512:

| Iteration | ~Date | MR(s) | Pipeline | Annotation | Outcome |
|---|---|---|---|---|---|
| First | ~01 Jun 2026 |!784 →!785 | `2567082445` (green) | `server-snippet` | Rejected by webhook (Azure serial-console session) |
| Second (this incident) | 18 Jun 2026 |!802 | `2611792387` (green) | `configuration-snippet` | Rejected by webhook; 8h47m incident |

Same failure class, same file, undetected in CI both times. That recurrence is the single strongest argument for encoding the rule as policy rather than relying on memory or review.

---

## 2. Timeline (UTC, 18 Jun 2026)

| Time | Event |
|---|---|
| 14:01 | MR!802 squash-merged to `master` (`ea78d593`, merge `5e8fa398`); `app-root` → `configuration-snippet`; 0 reviewers, 0 comments |
| 14:05:27 | Burst 1—first admission-webhook denial; ArgoCD sync of `ff-test-a-frontend` fails |
| ~14:10 | Burst 1 exhausts `retry.limit: 5` (backoff 5s→10s→20s→40s→~80s, cap 3m); goes quiet |
| 15:05–15:10:29 | Burst 2—unrelated commit `1ad4b68b` (FTFL-999 / MR!803) advances `master`, re-triggering the _same_ failure. Ends 15:10:29Z—this is the burst your screenshot captured |
| 15:10 → 22:50 | ~7h40m of silent `Degraded`/`SyncError`—no retries, no alert, no noise |
| 22:49 | MR!804 (`73a6368b`, FTFL-999, Ollie Rushton) comments out the snippet in the chart's first Ingress block |
| ~22:50–22:52:37 | Burst 3—still failing: `ff-test-a` renders the chart's second Ingress block (the `else`/single-host branch), which!804 didn't touch |
| 22:53 | MR!805 (`ed47703c`) comments out the second block—the fix that actually cleared `ff-test-a` |
| 22:52:37+ | No further denials in either `argocd-application-controller-0` or `ingress-nginx-controller` logs |

MTTR ≈ 8h47m (first → last denial), ~7h40m of it silent. The same unrelated ticket (FTFL-999) both _re-exposed_ the bug (MR!803) and ultimately _fixed_ it (MR!804/!805)—with zero traceability back to FTFL-512: no linked issue, no regression test, no reference to the original ticket.

---

## 3. Gap 1—Detection (Why it mErged)

### Mechanism

- The merge was gated by pipeline `2611792387`, which ran exactly two jobs: `prepare_kube_config` (fetches an AKS kubeconfig, otherwise a no-op) and `lint_workflows` (`helm template./workflows/… | argo lint`). Neither touches `charts/`, renders the Ingress, runs a policy check, or contacts the admission chain. The entire `validate` stage is gated `changes: [workflows/]` (`.gitlab-ci.yml:92-114`).
- The merge gate itself is effectively absent: `only_allow_merge_if_pipeline_succeeds = false`, `approvals_before_merge = 0`. The gate is _"an MR exists,"_ not _"CI passed"_ or _"someone reviewed it."_
- MR!802's description ("removed ssl-passthrough…") was stale boilerplate that didn't describe the actual diff—a mismatch a single reviewer would likely have caught.
- The webhook's denial text survives in the repo only because someone pasted it into a code comment while fixing it (commit `73a6368b`). There is no test, alert, or doc capturing this failure mode anywhere else.

### Where it Should Have Been Caught (Tooling that Already Exists hEre)

- An OPA/Conftest framework already exists (`policies/*.rego`: `images.rego`, `volumes.rego`, `enforce_automated_sync_policy.rego`, …)—but has no rule for Ingress annotations. `policies/k8s/validating-webhook.yaml` is scoped to `resources: ["pods"]` only; Ingress objects would never reach it.
- `scripts/argo-render` is a homegrown Go tool that renders manifests "exactly as ArgoCD would"—but its README still lists _"Integration with CI/CD pipelines"_ as an unchecked future enhancement. Built, never wired in.
- `prepare_kube_config` already fetches live testing-cluster credentials in this exact pipeline—and that kubeconfig sits unused, when a single `kubectl apply --dry-run=server` against it would catch _any_ admission rejection, including ones nobody thought to encode.

---

## 4. Gap 2—Containment (Why it Blocked Unrelated wOrk)

### Mechanism (Live-confirmed, and Corrected Vs the Secondary sOurce)

Each environment is one app-of-apps `Application` that generates one child `Application` per component, each carrying an `argocd.argoproj.io/sync-wave` annotation. The parent's own task list—logged verbatim on every retry (`syncId 00120-HMGFN`, 15:05:01Z)—orders them:

```text
Sync/-5: cert-manager, prometheus-operator-crds
Sync/-4: grafana-alloy-k8s-monitoring
Sync/-3: ff-test-a-databases-postgresql
Sync/-2: argo-workflows
Sync/0 : ff-test-a-minio, ff-test-a-mongodb-…, VaultStaticSecret nhs-pet, sleuth-secret
Sync/1 : ff-test-a-workflow-templates, spicedb
Sync/2 : ff-test-a-workflows-api
Sync/3 : ff-test-a-ffcloud-service, ff-test-a-fitconnect
Sync/4 : ff-test-a-frontend, mesh-mailbox      <- broken task
Sync/5 : certificates
Sync/10: ff-test-a-mssql
```

Across every captured task line during the incident, waves `-5 → -3` progressed to `Synced/Succeeded` one at a time, while `certificates` (w5) and `ff-test-a-mssql` (w10) stayed at empty status `(,,)`—never attempted, every single time—because the orchestrator never advanced past the failing wave-4 task. `mesh-mailbox` (wave 4 sibling) is an additional casualty.

`charts/ffnode/values.yaml:97-112` sets `syncPolicy.automated.{prune,selfHeal} = true`, and `policies/enforce_automated_sync_policy.rego` _mandates_ this on every Application—so the retry-on-change behaviour is structural, not accidental.

### Two Corrections to the Secondary Investigation

The LTM-based source asserted two mechanics that the live logs do not support:

- "Infinite retry loop" → wrong. `retry.limit` is 5 (bounded, exponential backoff, 3m cap). Failures came in three discrete bursts, each triggered by a _new_ commit landing on `master`, with ~7h40m of total silence between bursts 2 and 3. The app wasn't hammering the webhook for 8 hours—it was silently broken for 8 hours, only re-attempting when an unrelated push nudged it. That is arguably _worse_ for detection: no continuous noise to draw attention.
- "Shared `argocd-application-controller` queue contention" → not observed. The cleaner, evidenced explanation is plain sync-wave head-of-line ordering within one app-of-apps (later waves never _started_). The sibling Applications the other source listed via `kubectl get applications` are consistent with app-of-apps _children_, not a separate flat topology competing for a queue. Queue starvation may exist but was not demonstrated.

### Did it Block Unrelated Work?

Mechanically, yes—`certificates` and `mssql` were frozen for the duration. Whether a _person_ (the FTFL-999 engineer) was blocked from their own deploy, or simply noticed the `Degraded` state and fixed it opportunistically, is unconfirmed (their own component, `grafana-alloy`, is wave `-4` and synced fine each time). Needs Slack history or the engineer.

---

## 5. Gap 3—Environment Targeting (Why Staging, not sAndbox)

- `charts/ffnode/values.yaml:96` sets the default `argocdApp.targetRevision: master` for every ffnode that doesn't override it. `ff-test-a`'s rendered Application uses this default verbatim—no override.
- `ffnodes/fitfile/sandbox-testing-1/values.yaml:17` does override it: `targetRevision: sandbox-testing-1-latest-release`—a git tag, not a branch. Someone must deliberately move that tag (via `release.sh`) for sandbox to deploy. Sandbox has a real promotion gate; `ff-test-a`/staging does not.
- The introducing commit `5e8fa398` carries `tag: sandbox-testing-1-latest-release`—confirming the author _intended_ it for sandbox under that controlled process. But because the commit also became the new tip of `master`, and `ff-test-a` tracks `master` directly with `selfHeal: true`, ArgoCD deployed it to staging immediately and automatically, with no tag, no approval, and no relationship to the sandbox release at all.
- This is the actual mechanism behind _"supposed to be for sandbox, but the problem showed up in staging."_ It's not a misconfigured destination—it's that only one environment in the fleet has an opt-in promotion gate, and every other environment (including the one that calls itself `staging`) deploys every `master` commit the moment it lands.

---

## 6. Source Reconciliation & Confidence

This report fuses two read-only investigations of differing rigour:

- Source A—live-cluster probe (`fitfile-cloud-staging-aks-cluster`, namespace `argocd`, read-only `get`/`logs`/`events`). Strongest evidence: pod logs matched to the screenshot to the second, verbatim sync-wave task lists, against the _actual_ incident environment (`ff-test-a`).
- Source B—LTM/SoT synthesis (Obsidian SoT notes, Pieces/Antigravity sessions, 01 Jun console sessions). Contributes useful context (ingress-nginx version, the earlier `server-snippet` iteration) but several mechanistic claims are superseded by A's live evidence.

| Claim | Confidence | Basis |
|---|---|---|
| No `charts/` validation in CI; merge gate ≈ none | High | Pipeline `2611792387` job list; project settings; `.gitlab-ci.yml:92-114` |
| Containment = sync-wave head-of-line block (w5/w10 never attempted) | High | Live `argocd-application-controller-0` task logs (`ff-test-a`), verbatim, every retry |
| Retry was bursty/bounded (`limit:5`), not infinite | High | Live logs; 3 commit-triggered bursts; ~7h40m silent gap |
| MTTR ≈ 8h47m, ~7h40m silent | High | First denial 14:05:27Z → last 22:52:37Z (live logs) |
| Env targeting: `master` default vs sandbox tag override | High | `charts/ffnode/values.yaml:96`; `ffnodes/…/sandbox-testing-1/values.yaml:17`; rendered Application |
| Recurrence—earlier `server-snippet` iteration (~01 Jun) | Medium | LTM / console session; not re-verified live |
| ingress-nginx chart `4.14.1` / app `1.14.1` | Medium | Jumpbox `helm get metadata`, 29 May (LTM) |
| "Shared controller queue contention" as a cause | Low / unconfirmed | Asserted in Source B; not seen in live logs; superseded by wave-ordering |
| FTFL-999 engineer was _personally_ blocked (vs opportunistic fix) | Unknown | Needs Slack / engineer recollection |

---

## 7. Recommendations (Consolidated & rAnked)

Ranked by leverage (impact ÷ effort). Tags: [D] detection · [T] targeting · [C] containment.

| # | Change | Gap | What it catches / contains | Effort | Blast radius | First file to touch |
|---|---|---|---|---|---|---|
| 1 | Rego rule denying `configuration-snippet` / `server-snippet` / `location-snippet` on `Ingress`, mirroring the cluster's `allowSnippetAnnotations: false` (text already in commit `73a6368b`) | [D] | _This exact incident, deterministically, in seconds_—both iterations | Low | None (new file) | `policies/ingress_snippets.rego` (+ `_test.rego`) |
| 2 | Wire chart validation into CI—`validate:policy` job gated `changes: [charts/]`: `helm template <changed chart> \| conftest test --policy policies/ -` | [D] | 1 plus every future policy in this framework, for every chart | Low–Med | CI-only | `.gitlab-ci.yml` |
| 3 | Pin non-promotion environments to a release tag—add `argocdApp.targetRevision` override, copying the sandbox pattern | [T] | Stops _any_ bad commit reaching staging regardless of CI gaps—only deploys on a deliberate tag move | Low | Changes when staging updates—needs promotion-cadence buy-in | `ffnodes/fitfile/ff-test-a/values.yaml` |
| 4 | Strengthen the merge gate—enable `only_allow_merge_if_pipeline_succeeds`; require ≥1 approver for `charts/` diffs | [D] | Makes 1/#2 actually gate the button; a reviewer catches stale descriptions + annotation swaps | Low | Process | GitLab → Settings → Merge requests |
| 5 | Alert on `Degraded`/sync-failed > N minutes | [C] (MTTR) | The ~7h40m _silent_ window—would have surfaced this in minutes, not hours | Low–Med | Alerting only | ArgoCD notifications / Grafana rule _(location TBC—see open Qs)_ |
| 6 | Server-side dry-run in CI—`kubectl apply --dry-run=server`, reusing the kubeconfig `prepare_kube_config` already fetches | [D] | _Any_ admission rejection, including classes nobody has encoded as policy | Med (private network / jumpbox) | Read/dry-run only | `.gitlab-ci.yml` (job `needs: [prepare_kube_config]`) |
| 7 | Curb the blast radius of a stuck sync—move `frontend` off a wave shared with `certificates`/`mssql`, and/or migrate toward a per-service `ApplicationSet` so one service's failure can't freeze the rest | [C] | Confirmed live: would have kept `certificates`/`mssql`/`mesh-mailbox` syncing while `frontend` failed | Med–High (architectural) | All ffnode environments | `charts/ffnode/templates/frontend-application.yaml` (+ siblings) |

Suggested sequencing: 1 today (local, zero-risk) → 2 + 4 to make it a real gate → 3 to close the targeting hole → 5 to kill the silent-failure MTTR → 6/#7 as the deeper detection/containment investments.

---

## 8. Smallest First Steps (Two Parallel, Different gAps)

Both are low-risk, independently shippable, and use patterns/tools the team already owns.

### A. Detection—create One Policy File

Create `policies/ingress_snippets.rego` (match the Rego syntax of your existing `policies/*.rego`):

```rego
package main

deny[msg] {
  input.kind == "Ingress"
  banned := {
    "nginx.ingress.kubernetes.io/configuration-snippet",
    "nginx.ingress.kubernetes.io/server-snippet",
    "nginx.ingress.kubernetes.io/location-snippet",
  }
  k := banned[_]
  input.metadata.annotations[k]
  msg := sprintf(
    "Ingress %q uses banned snippet annotation %q (cluster sets allowSnippetAnnotations=false)",
    [input.metadata.name, k],
  )
}
```

Runnable immediately, locally, no CI or cluster needed:

```sh
helm template charts/components/frontend | conftest test --policy policies/ -
```

That single command would have failed FTFL-512 before the MR was ever opened. Wiring it into the pipeline (rec 2) is the next step; add a `_test.rego` per your existing `*_test.rego` convention.

### B. Targeting—add One line

Add a `targetRevision` override to `ffnodes/fitfile/ff-test-a/values.yaml`, copying the proven `sandbox-testing-1` pattern, so staging stops auto-pulling every `master` commit. One line, low-risk, closes Gap 3 using a mechanism the team already trusts.

---

## 9. Open Questions for Humans

| # | Question | Why it matters | How to answer |
|---|---|---|---|
| 1 | Was the FTFL-999 engineer's own deploy actually _blocked_, or did they fix opportunistically? | Distinguishes "real cross-team blast radius" from "lucky catch" | Slack history / ask the engineer |
| 2 | Do `ff-test-b/c` and other envs also default to `targetRevision: master` with no gate? | Likely yes by default—scopes how widespread Gap 3 is | `kubectl get applications -n argocd -o jsonpath='{range.items[*]}{.metadata.name}{" "}{.spec.source.targetRevision}{"\n"}{end}'` |
| 3 | Confirm `retry`/`syncPolicy` fleet-wide (resolved as `limit:5` for `ff-test-a`) | Ensures the bounded-retry assumption holds everywhere | `kubectl get application <name> -n argocd -o jsonpath='{.spec.syncPolicy}'` |
| 4 | Is there any ArgoCD alerting/notifications? | Logs show nothing fired during the ~7h40m silent window—likely a blind spot | Locate ArgoCD notifications config / Grafana alert rules |
| 5 | Is the high background `lint_workflows` failure rate (≈50 reds, mostly that one job) normalising "pipeline red = noise"? | Red-pipeline blindness is a cultural risk that undermines every gate above | Sample recent failed master pipelines; raise with the team |
| 6 | Confirm the live webhook blocks `server-snippet` and `configuration-snippet` equally | Both are in the `ConfigurationSnippet` risk group; web sources say yes—verify against the live ConfigMap | `kubectl get configmap ingress-nginx-controller -n ingress-nginx -o yaml \| grep -E 'allow-snippet\|annotations-risk'` |

---

## 10. Key Evidence Index

- MR!802 (merged, 0 reviewers/0 comments)—introduces the bug—`https://gitlab.com/fitfile/deployment/-/merge_requests/802`
- MR!804 / MR!805 (FTFL-999)—the fix—`…/merge_requests/804`, `…/merge_requests/805`
- Gating pipeline (2 jobs)—`https://gitlab.com/fitfile/deployment/-/pipelines/2611792387`
- Earlier iteration—pipeline `2567082445` (MR!784/!785, `server-snippet`)
- Commits—`ea78d593` (intro), `73a6368b` + `ed47703c` (fix; capture the webhook denial text)
- Live cluster—context `fitfile-cloud-staging-aks-cluster`; Application `argocd/ff-test-a-frontend`; denial log `2026-06-18T15:10:29Z` matches the screenshot to the second
- `charts/ffnode/values.yaml:96` (`targetRevision: master` default) vs `ffnodes/fitfile/sandbox-testing-1/values.yaml:17` (tag override)
- `.gitlab-ci.yml:92-114` (validate stage—workflows-only scope)
- `charts/ffnode/templates/frontend-application.yaml:8` (sync-wave `4`)
- `policies/k8s/validating-webhook.yaml:7-11` (Pods-only scope)
- `scripts/argo-render/README.md:143` (CI/CD integration unchecked)
