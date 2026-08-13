---
branch: feature/FTFL-673-grafana-alloy-upgrade
created: 2026-06-06T00:00:00+00:00
kind: project-note
lifecycle: active
modified: 2026-08-13T10:53:32+00:00
mr: '!787'
permalink: llmeon/30-library/200-projects/ffnode-templating-analysis
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
related: ["[[ffnode-templating-analysis]]", "[[Grafana k8s-monitoring v2]]", "[[grafana_alloy_audit_report]]"]
tags: [1, 2, 3, complexity, developer-experience, faro, ffnode, FTFL-673, grafana-alloy, helm, kubernetes, metrics, multi-cluster, observability, scaling, seedling, templating, work]
ticket: FTFL-673
title: ffnode-templating-analysis
type: null
---

> Every claim below is grounded in a file or commit that was read directly. File references use `path:line`.
> Scope of evidence: `charts/ffnode/` and `ffnodes/` on `master` as of commit `92caecaa`.

## 0. Important Grounding Corrections (Read fIrst)

The session brief made three assumptions that the repository contradicts. They are corrected here so nothing downstream is built on them:

1. FTFL-673 was not a single clean merge of one feature branch. `master` contains the feature branch _plus_ a follow-up bugfix branch:
   - `b4adee37 FTFL-673 grafana alloy upgrade and frontend observability` (merged via `4bce3f02`)
   - then a string of fixes from `bugfix/FTFL-673-certs-for-faro`: `b5f16268` (certs for faro), `aaa66b6f` (single faro subdomain), `6ae25319` (barts shares prod-1 faro endpoint), `ba621f50` (`FARO_DEPLOYMENT_ENVIRONMENT` env var).
   The "Faro is finished and merged" story is really "Faro shipped, then needed four corrective commits." That history is the single best place to understand the feature's sharp edges.
2. The templating does _not_ live in the files the brief named. There is no separate "VSO bug at `_helpers.tpl` line 80 only." The Faro/Grafana/cert logic lives in `_grafana.tpl`, `_frontend.tpl`, `_certs.tpl` (all created by FTFL-673) plus `values.yaml`. (An earlier directory snapshot during analysis showed the _pre-merge_ layout—`grafana-application.yaml`, no `_grafana.tpl`—because the working tree is on a network volume that briefly served a stale view. The committed/HEAD truth is `grafana-alloy-application.yaml` + `_grafana.tpl`.)
3. `ffnode` is not a Helm umbrella chart. `charts/ffnode/Chart.yaml` has no `dependencies:` block (`type: application`, `version: 1.0.0`). It is an _ArgoCD App-of-Apps generator_—see §1.

This document also surfaces three concrete bugs found while reading (§4 and §8). The most serious is a one-character typo that silently breaks Faro bearer auth on all 9 enabled clusters.

---

## 1. Chart Architecture Overview

### What `ffnode` is

`ffnode` is a Helm chart whose templates render ArgoCD `Application` custom resources, not Kubernetes workloads. One `ffnode` release per customer cluster fans out into ~20 ArgoCD Applications, each of which deploys a real sub-chart (frontend, fitconnect, ffcloud, mongodb, grafana k8s-monitoring, cert-manager, argo-workflows, …). This is the App-of-Apps pattern.

Evidence: every `charts/ffnode/templates/*-application.yaml` emits `kind: Application` / `apiVersion: argoproj.io/v1alpha1` and is feature-gated, e.g. `grafana-alloy-application.yaml:1` (`{{- if eq.Values.deploy.monitoring true }}`), `frontend-application.yaml:1` (`deploy.frontend`), `certificates-application.yaml:1` (`deploy.certManager`).

Two ways a sub-chart is sourced:

- From an OCI/ACR Helm repo—e.g. grafana: `chart: helm/k8s-monitoring`, `repoURL: "fitfileregistry.azurecr.io"`, `targetRevision: 4.1.4` (`grafana-alloy-application.yaml:19-21`).
- From a path inside this same git repo—e.g. frontend: `path: charts/components/frontend`, `repoURL: https://gitlab.com/fitfile/deployment.git`, `targetRevision: {{.Values.argocdApp.targetRevision}}` (`frontend-application.yaml`). The per-cluster `argocdApp.targetRevision` (e.g. `cuh-prod-1-latest-release`, `ffnodes/eoe/cuh-prod-1/values.yaml:18`) is how each cluster pins to a git tag/branch.

### Sync Ordering

Applications carry `argocd.argoproj.io/sync-wave` annotations that sequence rollout:

`cert-manager` = `-5`, `grafana-alloy` = `-4`, `frontend` = `4`, `certificates` = `5`. Cert-manager and its CRDs must exist before the `certificates` Application creates `Certificate` objects.

### The `ffnodes/<hub>/<cluster>/values.yaml` Override Mechanism

`charts/ffnode/values.yaml` holds defaults for every cluster. `ffnodes/<hub>/<cluster>/values.yaml` is a per-cluster overlay merged on top at deploy time (Helm `-f`). Hubs seen under `ffnodes/`: `fitfile`, `kch`, `eoe`, `wmsde`, `barts`, `nwsde`, `stg`—~27 cluster files in total. A few clusters (`kch/prod`, `kch/mn4`, `stg/sandbox`, `fitfile/gh-pt-1`) add a nested `values/` + `templates/` sub-structure for app-specific overrides.

The overlay is deliberately thin: a cluster file typically sets only `namespace`, `deploymentKey`, `host`, `deploy.*` toggles, `argocdApp.targetRevision`, TLS `spec`/ingress `hosts`, and feature blocks like `grafanaAlloy.frontendObservability`. Everything structural (vault secret wiring, alloy config, resource requests) stays in the base chart.

---

## 2. Template Inventory

### `.tpl` Libraries (Named Templates, no Output of Their oWn)

| File | Purpose | Defines | Gotchas |
|---|---|---|---|
| `_helpers.tpl` | Core utilities + the Vault-secret rendering engine | `generateVaultDynamicSecrets`, `renderValuesWithVaultSecretInExtraDeploy`, `concatArrays`, `common.tplvaluesRender`, `escape.tpl`, host/name helpers (`minioHost`, `postgresqlHost`, `mongodbHost`*, `fitfileHost`, `spicedbHost`…), `oauth`, `ffnode.global.corsAllowedOrigins`, `workflows.loadDataConfig` | The whole VSO escaping story lives here (`:40-46`, `:76-101`). The `tpl`-on-transformation path is at `:44`/`:80`. See §4. |
| `_grafana.tpl` | Values factory for the grafana k8s-monitoring (Alloy) sub-chart, incl. Faro receiver, ingress, opencost, collectors | `ffnode.grafana.values` | Contains Bug 1 (always-on Faro gate, `:11` & `:202`). Hand-writes Alloy River config as a heredoc string (`:205-268`). |
| `_frontend.tpl` | Values factory for the frontend sub-chart; merges env-var lists by name; injects Faro secret + env when enabled | `ffnode.frontend.values`, `ffnode.frontend.defaults`, `ffnode.frontend.faroSecret` | List-merge-by-name logic (`:68-85`, `:88-104`) is non-obvious. Faro env block correctly gates on `.enabled` (`:43`). |
| `_certs.tpl` | Conditionally appends a cert-manager `Certificate` definition for the Faro host | `ffnode.certManager.certificates` | Correctly gates on `.enabled AND.tls.createCertificate` (`:3`). |
| `_argoWorkflows.tpl` | Argo Workflows values incl. SSO/RBAC and its vault secrets | `argoWorkflowsHost`, argo vault secrets block | Canonical example of `secretTransformationDisableTpl: true` (`:147`, `:158`). |
| `_common.tpl` | Tiny shared snippets | `bitnami.metrics`, `argocd.app.common.ignoreDifferences` |—|
| `_ffcloud.tpl`, `_fitconnect.tpl`, `_mongodb.tpl` | Per-service value factories | `ffnode.ffcloud.*`, `ffnode.fitconnect.*`, mongo host helpers | `_ffcloud.tpl:33` & `_fitconnect.tpl:31` both consume `ffnode.global.corsAllowedOrigins`. |

\* `mongodbHost` is referenced (`values.yaml:587,730`, `_frontend.tpl:33`) and defined in `_mongodb.tpl`.

### Application Templates (Emit One ArgoCD `Application` eAch)

`argo-workflows`, `blob-csi-driver`, `cert-manager`, `certificates`, `ffcloud`, `fitconnect`, `frontend`, `grafana-alloy`, `minio`, `mongodb`, `mongodb-next`, `mssql`, `mutating-proxy-webhook`, `postgresql`, `prometheus-crds`, `seed`, `spicedb`, `workflow-templates`, `workflows-api`, `workflows-integration-tests-templates`. Plus `extra-deploy.yaml` (raw `extraDeploy` + `extraVaultSecrets` passthrough) and `mongodb-copy-data-job.yaml`.

Each follows the same skeleton: `{{- if.Values.deploy.X }}` → `Application` metadata → `helm.values: |` block built by a factory and piped through `renderValuesWithVaultSecretInExtraDeploy`.

---

## 3. Templating Patterns Catalogue

### P1—Named-template Values Factory (`include … | fromYaml` → `mergeOverwrite`)

The defining pattern of this chart. A `.tpl` builds a sub-chart's values as YAML text, which is parsed back to a dict, merged with user overrides, and injected.

```yaml
# grafana-alloy-application.yaml:25-26
{{- $values := mergeOverwrite (include "ffnode.grafana.values" . | fromYaml) (dict "vaultSecrets" .Values.grafanaAlloy.vaultSecrets) -}}
{{- include "renderValuesWithVaultSecretInExtraDeploy" (list . $values "extraObjects") | indent 8 }}
```

Solves: keeps deeply nested sub-chart values DRY and computable (hostnames, CORS lists, conditional blocks).

Risk: `include → toYaml → fromYaml` round-trips lose types and silently swallow templating errors as strings. No schema guards what the factory emits. A typo in a factory key is invisible until ArgoCD rejects the rendered sub-chart.

### P2—Feature-flag Gating on `deploy.*` (Application lEvel) and Feature Blocks (Values lEvel)

```yaml
{{- if eq .Values.deploy.monitoring true }}   # grafana-alloy-application.yaml:1
{{- if .Values.grafanaAlloy.frontendObservability.enabled }}  # _frontend.tpl:43 (correct)
```

Solves: per-cluster opt-in. Risk: the _truthiness target_ is easy to get wrong—see Bug 1, where `_grafana.tpl` gates on the map instead of `.enabled`.

### P3—Vault Secret Wiring via `generateVaultDynamicSecrets`

`vaultSecrets:` / `extraVaultSecrets:` entries are declarative specs that `renderValuesWithVaultSecretInExtraDeploy` turns into VSO `VaultStaticSecret`/`VaultDynamicSecret` CRDs and appends to `extraDeploy`/`extraObjects`. See §4 for the full mechanism.

### P4—Global Propagation to Sub-charts

Every factory injects `global:` so bitnami sub-charts see shared config:

```yaml
global: {{ .Values.global | toYaml | nindent 2 }}   # _grafana.tpl:6, _frontend.tpl:19
{{- $values := merge .Values.grafanaAlloy (dict "global" .Values.global) -}}   # (pre-factory style, still used elsewhere)
```

### P5—List-merge-by-name (Env Vars, extraVaultSecrets)

`_frontend.tpl:68-85` merges default `env` with user `env` keyed by `.name` so a cluster can override `RESULT_DETAILS_LIMIT` without dropping defaults; `:88-104` does the same for `extraVaultSecrets` keyed by `.secretName` to splice in the Faro secret. Risk: bespoke, repeated, and easy to copy wrong; this is exactly what a library helper should own.

### P6—`fromYamlArray` Vs `fromYaml`

`fromYamlArray` is used where the value is a YAML list (`_grafana.tpl:3` CORS origins; `certificates-application.yaml` certificates list); `fromYaml` where it is a map. Mixing them up yields `nil`. The CORS helper returns a list literal (`_helpers.tpl:248`) and is consumed with `fromYamlArray` + per-item `quote` to build the Alloy `allowed_origins` array (`_grafana.tpl:2-5,225`).

### P7—`tpl` Double-evaluation / VSO Escaping

The headline complexity. Two coexisting escaping conventions (single raw-string vs string-literal-wrapped raw-string) plus an opt-out flag. Full treatment in §4.

---

## 4. The VSO Double-evaluation Mechanism (And the `disableTpl` Escape hAtch)

### What `generateVaultDynamicSecrets` Does

`_helpers.tpl:17-109` takes `(root, config)` and emits a VSO CRD (`VaultDynamicSecret` if `config.dynamic`, else `VaultStaticSecret`). The interesting part is the `destination.transformation` block:

```gotemplate
# _helpers.tpl:40-46 (dynamic) and :76-81 (static) — identical logic
{{- if hasKey $config "secretTransformation" }}
{{- if hasKey $config "secretTransformationDisableTpl"}}
transformation: {{ $config.secretTransformation | toYaml | nindent 6}}      # path A: NO tpl
{{- else }}
transformation: {{ tpl ($config.secretTransformation | toYaml) $ | nindent 6}}  # path B: tpl applied
{{- end }}
{{- end }}
```

### Why `tpl` on a Transformation Block is Dangerous

A VSO `transformation.templates[].text` is meant to contain a VSO-runtime Go template, e.g. `{{ get.Secrets "prometheus_password" }}`. VSO evaluates that _at secret-sync time_, against the secret material it pulled from Vault. `.Secrets` exists only in VSO's runtime scope—it does not exist in Helm's scope.

When path B runs `tpl` over that block, Helm tries to evaluate `{{ get.Secrets "x" }}` itself, fails to find `.Secrets`, and aborts the whole render (`nil pointer evaluating interface {}.Secrets` / `can't evaluate field Secrets`). That is the "double-evaluation bug": the expression is intended for VSO's evaluation pass, but Helm's `tpl` greedily takes a pass at it first.

### How the Codebase Copes Today (Two conventions—itself a fOotgun)

The author-side fix is to escape the `{{ … }}` so it survives Helm's `tpl` pass and lands in the manifest as a literal for VSO:

- String-literal-wrapped raw string (monitoring secret, `values.yaml:538-559`):
  `'{{"{{`{{get.Secrets \"prometheus_host\"}}`}}"}}'`
- Single raw-string (workflows/fitconnect, `values.yaml:587,730`):
  `mongodb://{{`{{get.Secrets "mongodb_username"}}`}}:…@{{ include "mongodbHost". }}/…`
—here the `{{ include … }}` part _must_ be tpl'd (path B) while the `{{`…`}}` raw-string protects the VSO part.

So whether you need single or double wrapping depends on whether the same string also contains a real Helm expression that must be evaluated. That coupling is the source of the bus-factor.

### `secretTransformationDisableTpl: true`—the Clean Escape Hatch

Introduced in `FFAPP-4566 / 11d4719e "Allows disabling TPL for secret transformations"`. It selects path A: the transformation is `toYaml`'d straight through with no `tpl`, so VSO templates need no Helm escaping at all. Canonical use: `_argoWorkflows.tpl:147,158`. The frontend Faro secret deliberately does the opposite—`secretTransformationDisableTpl: false` (`_frontend.tpl:2`)—i.e. it opts _into_ path B and therefore must double-escape (`_frontend.tpl:15`).

### Who is at risk of the Double-eval Failure

Every `secretTransformation` that uses path B (no `disableTpl`) and references `{{ get.Secrets … }}` must hand-escape _every_ occurrence. Forgetting one escape = full render failure for that cluster. Path-B callers found via `grep "secretTransformation" charts/ffnode/`:

- `values.yaml`: `grafanaAlloy.monitoring` (:534), `workflowTemplates` (:582,603,619), `fitconnect` (:725), `ffcloud` (:779/779+), `seed`, `mongodb`, `minio`, `postgresql` blocks (multiple).
- `_frontend.tpl` faro secret (path B by explicit `false`).
Path-A (safe) callers: `_argoWorkflows.tpl` (both argo secrets). The asymmetry—most secrets path B, argo path A, frontend path B-by-choice—is exactly what a new engineer cannot guess.

---

## 5. Multi-cluster Configuration Analysis

### Inventory

~27 cluster override files across 7 hubs (`ffnodes/`): `fitfile` (13: ff-a/b/c, ff-test-a/b/c, development, testing, sandbox-testing-1, acr-test, pv-aks-1, wm-dev-1, gh-pt-1), `eoe` (7: hie-prod-34, hie-test-34, cuh-prod-1, nnuh-prod-1, ff-eoe-sde, ff-hyve-1, ff-hyve-2), `kch` (2), `nwsde` (2), `barts` (1), `wmsde` (1), `stg` (1).

### Shared Vs Per-cluster

- Shared (base `values.yaml`): all vault-secret wiring, Alloy River config, default resource requests, CORS default (`https://<fitfileHost>`), oauth defaults, the entire `grafanaAlloy` structure.
- Per-cluster (`ffnodes/…/values.yaml`): `namespace`/`deploymentKey`, `host`, `deploy.*` toggles, `argocdApp.targetRevision` + `globalIgnoreDifferences` (esp. the verbose proxy-env jq excludes for CUH, `cuh-prod-1/values.yaml:19-49`), `proxy.{enabled,proxyUrl}`, TLS `spec` / ingress `hosts`, and `grafanaAlloy.frontendObservability.{enabled,ingress.host}`.

### `frontendobservability` enable/disable Per Cluster

A cluster opts in with just:

```yaml
grafanaAlloy:
  frontendObservability:
    enabled: true
    ingress:
      host: faro-cuh-prod-1.privatelink.fitfile.net
```

(`cuh-prod-1/values.yaml:102-106`). Enabled on 9 clusters: ff-test-a (`faro-staging`), sandbox-testing-1, testing, ff-a (`faro-app`), barts/prod (`faro-app`—same host as ff-a, intentional per commit `6ae25319`), hie-prod-34, hie-test-34, cuh-prod-1, nnuh-prod-1.

### Drift Risks (Real)

1. `ingress.host` is the single point of truth for three different things—the Faro Ingress rule (`_grafana.tpl:37,55`), the cert-manager `Certificate` `dnsNames` (`_certs.tpl:7`), and the frontend's `FARO_COLLECTOR_URL` env (`_frontend.tpl:45`). It must also have a matching Cloudflare DNS record and (for `privatelink` hosts) private DNS. Nothing in the chart validates that the DNS record exists; a typo in the host produces a cert that never validates and a frontend that POSTs to a dead URL.
2. Vault path drift. `vaultPath` strings (`application`, `monitoring`, `mesh`, `argo-workflows`, `cloudflare`) and the per-key names in `secretTransformation` must match what actually exists in HCP Vault at `admin/deployments/<deploymentKey>` (`_helpers.tpl:20`). No CI check ties chart keys to Vault contents.
3. Shared Faro host across clusters (ff-a + barts) means one ingress/cert namespace owns a hostname used by two deployments—fine if deliberate, fragile if one cluster's cert config diverges.

---

## 6. Complexity & Bus-factor Assessment

Genuinely hard without prior context:

- The VSO escaping conventions (§4). The triple-nested `{{"{{`{{get.Secrets \"x\"}}`}}"}}` is unreadable and undocumented; knowing _when_ to use single vs double wrapping vs `disableTpl` is tribal knowledge.
- The factory round-trip (`include → fromYaml → mergeOverwrite → renderValues…`). Errors surface as ArgoCD sync failures three layers removed from the typo.
- `_frontend.tpl`'s manual list-merge-by-name (env and extraVaultSecrets).
- The hand-written Alloy River heredoc in `_grafana.tpl:205-268`—a second DSL embedded as a string inside Helm inside YAML, with its own auth/CORS/exporter wiring.

A new engineer will struggle to: know which `deploy.*` flag turns a thing on; know that `frontendObservability.ingress.host` fans out to 3 consumers + DNS + Vault; understand why `monitoring` secret escaping differs from `workflowTemplates`; trust that editing a factory won't silently break a `fromYaml`.

Minimum viable documentation: (a) a one-paragraph "this is an App-of-Apps generator, not an umbrella chart" header in `Chart.yaml`/README; (b) a `vaultSecrets` authoring guide with the decision rule _"use `secretTransformationDisableTpl: true` unless your `text` also contains a Helm expression that must be evaluated"_; (c) a Faro feature doc listing the 3 consumers of `ingress.host`; (d) inline comments on `_grafana.tpl:11` and `:202` explaining the intended gate.

---

## 7. Bugs Found while Reading (Verify & fIx)

### Bug 1—Faro Receiver is Gated on the Map, not `.enabled` (Always-on)

`_grafana.tpl:11` `{{- if.Values.grafanaAlloy.frontendObservability }}` and `:202` `{{- if.Values.grafanaAlloy.frontendObservability }}` test the whole map, which is always defined in `values.yaml:470`, so the Faro `applicationObservability`, the `alloy-faro` Ingress, and the `alloy-faro` collector render on every monitored cluster regardless of `enabled: false`. The frontend (`_frontend.tpl:43,88`) and certs (`_certs.tpl:3`) correctly test `.enabled`, so the two halves disagree: a cluster with `enabled:false` still gets a Faro receiver + Ingress (referencing an empty `ingress.host`) but no cert and no frontend env. Fix: `if.Values.grafanaAlloy.frontendObservability.enabled` in both places. (Note `ingress.host` has a `required` only inside the `tls` branch at `:37`, so an always-on render with empty host may still slip through via the `else` path at `:55`.)

### Bug 2—`fargo-bearer-token` Typo Breaks Faro Bearer Auth on All 9 Enabled Clusters

`values.yaml:558` writes the destination key as `fargo-bearer-token` (from `faro_bearer_token`), but the Alloy receiver reads `faro-bearer-token`: `_grafana.tpl:213` `remote.kubernetes.secret.monitoring.data["faro-bearer-token"]`. The key the consumer expects is never created, so `otelcol.auth.bearer.creds.token` is empty and the receiver rejects/!authenticates browser traffic. Blast radius confirmed: the typo exists at exactly one line (`grep fargo` → only `values.yaml:558`) but feeds the shared `monitoring` secret used by every Faro-enabled cluster. Fix: rename the key to `faro-bearer-token`.

### Bug 3 (latent)—two Escaping Conventions Invite the next Render Failure

Not currently broken, but `values.yaml` mixes single-raw-string and string-literal-wrapped escaping for VSO templates with no comment explaining which to use. The first engineer who copies the wrong pattern into a path-B secret breaks that cluster's render. Mitigated structurally by §8.

---

## 8. Recommendations for Type-safe, Flexible Multi-cluster Management

### 8.1 `values.schema.json` (Highest ROI)

Add a JSON schema to `charts/ffnode/` enforcing at least:

- `deploymentKey`, `namespace`—required `string`.
- `deploy.*`—all `boolean`.
- `grafanaAlloy.frontendObservability`—object with required `enabled: boolean`; `if enabled then require `ingress.host` (string, hostname format)` via `if/then`. This alone would have caught the empty-host always-on case from Bug 1.
- `grafanaAlloy.frontendObservability.tls.createCertificate` / `existingSecret` typed.
- `proxy`—`if enabled then require proxyUrl`.
- `*.vaultSecrets[]`—require `secretName` + `vaultPath`; make `secretTransformationDisableTpl` a documented `boolean`.

### 8.2 CI Linting

- `helm template ffnodes/<hub>/<cluster>/values.yaml | kubeconform` (or ArgoCD `--dry-run`) for every `ffnodes/*` file in CI—render is the real test for this chart, since most bugs only appear at render time.
- `helm lint --strict` with the schema above.
- A grep-gate forbidding new `secretTransformation` blocks that lack `secretTransformationDisableTpl` unless the `text` contains `{{ include` / `{{.` (i.e. a real Helm expr)—nudges authors to path A by default.
- A cross-check test asserting every `faro-*` data key produced in `values.yaml` is referenced in `_grafana.tpl`/`_frontend.tpl` and vice-versa (would have caught Bug 2).

### 8.3 Make `ingress.host` / DNS a Single Source of Truth

Define the Faro host once and derive everything: compute `ingress.host` from `deploymentKey` in a helper (`faro-{{ deploymentKey }}.{{ zone }}`) with an explicit per-cluster override only when needed; have `_certs.tpl`, `_grafana.tpl`, and `_frontend.tpl` all consume that one helper (two of them already read `.ingress.host`—close the third). Pair with a CI job that asserts a Cloudflare DNS record exists for each rendered Faro host (the chart can't enforce DNS, but CI can).

### 8.4 Make `secretTransformation` Safe by Default

Flip the default: treat path A (no tpl) as the norm and require an explicit `secretTransformationEnableTpl: true` only for the rare blocks that genuinely need Helm interpolation (the `mongodbHost` connection strings). This removes the escaping burden from ~90% of secrets and makes the dangerous case opt-in and greppable. Until then, add a comment block above `_helpers.tpl:40` stating the rule.

### 8.5 Replace Bespoke Patterns with Library-chart Helpers

- The list-merge-by-name in `_frontend.tpl:68-104` and the `concatArrays`/`renderValuesWithVaultSecretInExtraDeploy` plumbing should move into a small Helm library chart (`type: library`) shared by all `*-application.yaml` templates, so the merge/escaping logic is defined once and unit-tested with `helm-unittest`.
- Extract the Alloy River heredoc (`_grafana.tpl:205-268`) into its own named template (`ffnode.alloy.faroConfig`) so it can be reviewed independently of the values factory.

---

## Appendix—key file:line Index

- App-of-Apps proof: `grafana-alloy-application.yaml:1-28`, `frontend-application.yaml`, `certificates-application.yaml`.
- VSO engine: `_helpers.tpl:17-109` (generate), `:121-143` (renderValues…), `:145-147` (`escape.tpl`).
- Faro factory: `_grafana.tpl:11-66` (gate+ingress), `:202-293` (collector+River config).
- Faro frontend wiring: `_frontend.tpl:1-16` (secret), `:43-53` (env), `:88-104` (secret splice).
- Faro cert: `_certs.tpl:3-9`.
- Escaping examples: `values.yaml:538-559` (double-wrap), `:587` (single), `_argoWorkflows.tpl:147-166` (disableTpl).
- Bugs: 1 `_grafana.tpl:11,202`; 2 `values.yaml:558` vs `_grafana.tpl:213`.
- FTFL-673 history: `b4adee37`, `4bce3f02`, `b5f16268`, `aaa66b6f`, `6ae25319`, `ba621f50`.

## Context

Over 4–5 Jun 2026 you and Ollie Rushton worked on `FTFL-673 — grafana alloy upgrade and frontend observability` ([GitLab MR !787](https://gitlab.com/fitfile/deployment/-/merge_requests/787), branch `feature/FTFL-673-grafana-alloy-upgrade`).

The work added Faro frontend observability to the `ffnode` umbrella chart—the chart that manages every FITFILE k8s cluster via ArgoCD. The chart is complex, largely Ollie's invention, and currently hard for anyone else to reason about independently.

Your goal: have a type-safe, self-documenting, multi-cluster-safe process for managing k8s observability configuration across all clusters (testing, staging, barts/prod, cuh-prod-1, nnuh-prod-1, hie-prod-34, mkuh-prd-4, sandbox-testing-1, ff-test-a, etc.).

---

## What Was Changed (FTFL-673 sUmmary)

| File | Change |
|---|---|
| `charts/ffnode/templates/grafana-alloy-application.yaml` | Renamed from `grafana-application.yaml`; bumped `targetRevision` to `4.1.4`; now references `_grafana.tpl` helper |
| `charts/ffnode/templates/_grafana.tpl` | New helper `ffnode.grafana.values`—builds the entire `k8s-monitoring` values block, including `frontendobservability`, CORS origins, Vault secrets wiring, and the `alloy-faro` extraConfig |
| `charts/ffnode/templates/_certs.tpl` | Conditionally appends a `cert-manager` certificate for the Faro ingress when `grafanaAlloy.frontendobservability.enabled=true` |
| `charts/ffnode/templates/_frontend.tpl` | Added `ffnode.frontend.faroSecret` helper—injects `FARO_COLLECTOR_TOKEN` from Vault into the frontend deployment |
| `charts/ffnode/templates/_ffcloud.tpl` / `_fitconnect.tpl` | Updated `allowedOrigin` configuration |
| `charts/ffnode/values.yaml` | Added `grafanaAlloy.frontendobservability` block (disabled by default), `ingress.host`, `tls.existingSecret: faro-tls` |
| `ffnodes/fitfile/ff-test-a/values.yaml` | Enabled frontendobservability in staging/test |
| `ffnodes/eoe/cuh-prod-1/values.yaml` + others | Faro ingress set to `faro.cuh-prod-1.privatelink.fitfile.net` pattern |
| `infrastructure/central-services/cloudflare/locals.tf` | Added `faro.\<cluster>.fitfile.net` DNS A-records for each customer cluster |
| `infrastructure/production/mkuh-prd-4/generated/values.yaml` | Alloy upgrade committed on branch `feature/FTFL-673-mkuh-grafana-alloy-upgrade` |
| `charts/integrations/thehyve-v2/values.yaml` | Updated for alloy 4.1.4 |

### Vault Secrets Involved

- `admin/deployments/\<env>/secrets/monitoring` → keys: `loki_host`, `loki_password`, `prometheus_host`, `faro_bearer_token`, `faro_collector_url`
- `admin/deployments/\<env>/secrets/application` → key: `faro_collector_token` (used by frontend deployment via `_frontend.tpl`)

### Bugs Hit during the Work

1. `fromYaml` arity error—`ffnode.frontend.values` at `_frontend.tpl:29` called `fromYaml` with 3 args; fixed to 1.
2. `$out` undefined—`_frontend.tpl:84` had an undefined variable; fixed.
3. VSO double-evaluation bug—`_helpers.tpl:80` function `generateVaultDynamicSecrets` passes `$config.secretTransformation` through Helm's `tpl` function; if the caller's `values.yaml` contains bare `{{get.Secrets "key"}}` expressions, Helm evaluates them immediately and crashes with `wrong type for value; expected map[string]interface{}`. Fix: `secretTransformationDisableTpl: true` in the relevant secret block.
4. Type coercion in `_grafana.tpl`—`global` value passed as a YAML list rather than map; fix was `toYaml` wrapping.

---

## Templating Patterns Used in `ffnode`

### Pattern 1—Named Template as Values Factory (`_grafana.tpl`, `_frontend.tpl`)

```go-template
{{- define "ffnode.grafana.values" -}}
{{- $quoted := list -}}
{{- range (include "ffnode.global.corsAllowedOrigins" . | fromYamlArray) -}}
{{- $quoted = append $quoted (. | quote) -}}
{{- end -}}
applicationObservability:
enabled: true
receivers:
otlp:
  grpc:
    enabled: true
    port: 4317
  http:
    enabled: true
    port: 4318
{{- end -}}
```

The application YAML consumes it:

```yaml
helm:
values: |
{{- mergeOverwrite (include "ffnode.grafana.values" . | fromYaml) (.Values.grafanaAlloy | toYaml | fromYaml) | toYaml | nindent 4 }}
```

Risk: `mergeOverwrite + fromYaml + toYaml` chain—any type mismatch silently drops keys or panics.

### Pattern 2—Feature-flag Gating

```yaml
# values.yaml default
grafanaAlloy:
frontendobservability:
enabled: false
```

```go-template
{{- if .Values.grafanaAlloy.frontendobservability.enabled }}
# inject faro ingress, cert, alloy extraConfig
{{- end }}
```

Per-cluster override:

```yaml
# ffnodes/fitfile/ff-test-a/values.yaml
grafanaAlloy:
frontendobservability:
enabled: true
ingress:
  host: faro.ff-test-a.fitfile.net
tls:
  existingSecret: faro-tls
```

### Pattern 3—Vault Secret Wiring via `generateVaultDynamicSecrets` Helper

```go-template
{{- define "ffnode.frontend.faroSecret" -}}
secretTransformationDisableTpl: false
secretName: "faro"
vaultPath: {{ include "applicationVaultPath" . }}
rolloutRestartTargets:
- kind: Deployment
name: {{ printf "%s-frontend-frontend" .Release.Name }}
refreshAfter: 5m
secretTransformation:
excludeRaw: true
excludes:
- .*
templates:
FARO_COLLECTOR_TOKEN:
  text: '{{ get Secrets "faro_collector_token" }}'
{{- end -}}
```

Critical: the `{{ get Secrets "…" }}` expression must NOT be evaluated by Helm—it is a Vault Secrets Operator template string. Use `secretTransformationDisableTpl: true` or backtick-escape when nesting inside a `tpl` call.

### Pattern 4—Umbrella Chart Passing `global` down to Sub-charts

```yaml
# grafana-alloy-application.yaml
values: |
global: {{ .Values.global | toYaml | nindent 2 }}
applicationObservability:
enabled: true
```

The `global` block carries cluster-wide values (cluster name, node selectors, proxy settings) down into the `k8s-monitoring` sub-chart.

---

## Known Complexity / risk Areas

- `_helpers.tpl:generateVaultDynamicSecrets`—the `tpl` double-evaluation hazard affects every caller that passes raw VSO templates. Needs either a global `DisableTpl` default or a schema-validated wrapper.
- No type-checked values schema—`ffnode` has no `values.schema.json`. Large optional blocks like `grafanaAlloy.frontendobservability` can be silently misconfigured.
- Multi-cluster ingress host management—currently split across `ffnodes/\<env>/values.yaml` (the Helm value) AND `locals.tf` in `central-services/cloudflare` (the DNS record). These can drift.
- `fromYamlArray` vs `fromYaml`—inconsistent use across tpl files; `fromYamlArray` is non-standard and errors silently on map inputs.
- Only Ollie fully understands `_grafana.tpl`—confirmed by your own Todoist inbox item "analyse the helm templating thing Ollie has created" (captured 5 Jun 2026).

---

## Goal: Type-safe, Flexible Multi-cluster Management

Target architecture:

1. `values.schema.json` on `ffnode`—enforce required fields, enum the `ingressClassName`, type-check `enabled` booleans.
2. Replace `tpl`-inside-`generateVaultDynamicSecrets` with a static template mode where VSO expressions are emitted as literal strings.
3. Single source of truth for cluster DNS—derive `ingress.host` from a cluster manifest rather than duplicating in `values.yaml` + `locals.tf`.
4. Per-cluster `values.yaml` files should only override, never re-define—enforce with a linting step in CI (`helm lint --strict`).

---

## Claude Code prompt—ffnode Helm Chart Analysis

Paste this verbatim into Claude Code inside the `deployment` repo root. It will read git history, analyse the templating patterns, and produce the structured summary you need.

```md
## Context

You are reviewing the `ffnode` Helm chart in the FITFILE `deployment` repository (GitLab: gitlab.com/fitfile/deployment).

The chart lives at `charts/ffnode/`. It is an umbrella chart used to deploy every FITFILE customer k8s cluster via ArgoCD. Each cluster gets its own `ffnodes/\<hub>/\<cluster>/values.yaml` override file.

We recently merged feature branch `feature/FTFL-673-grafana-alloy-upgrade` (GitLab MR !787) which added Grafana Alloy `frontendobservability` (Faro SDK ingress + bearer-token auth + cert-manager certificate) to the chart.

The problem: The templating is now complex enough that only one engineer (Ollie Rushton) fully understands it. We need to document, analyse, and simplify it.

Your goal for this session: Produce a structured analysis of the chart's templating architecture, patterns, and risks — grounded entirely in the git history and file contents. Do not guess; read the files.

---

## Phase 1 — Git history analysis

Run the following and read the output carefully:

```bash
# All commits on the feature branch and master that touch charts/ffnode/
git log --oneline --all -- charts/ffnode/ | head -40

# Full diff of the FTFL-673 work
git log --oneline --all --grep="FTFL-673" | head -20
git diff $(git log --oneline --all --grep="FTFL-673" | tail -1 | awk '{print $1}')~1 HEAD -- charts/ffnode/

# List all tpl files
ls -la charts/ffnode/templates/*.tpl

# Full content of every tpl file
for f in charts/ffnode/templates/*.tpl; do echo "=== $f ==="; cat "$f"; echo; done

# The main values file
cat charts/ffnode/values.yaml

# The grafana alloy application template
cat charts/ffnode/templates/grafana-alloy-application.yaml 2>/dev/null || cat charts/ffnode/templates/grafana-application.yaml

# A representative cluster values file (test environment)
cat ffnodes/fitfile/ff-test-a/values.yaml

# A production cluster values file  
cat ffnodes/eoe/cuh-prod-1/values.yaml 2>/dev/null || ls ffnodes/eoe/

# The helpers file — this is where the VSO templating bug lives
cat charts/ffnode/templates/_helpers.tpl

---

## Phase 2 — What to analyse

After reading all files, produce a structured report with these sections:

### 1. Chart architecture overview
- What is `ffnode` responsible for? What does it delegate to sub-charts?
- How does the `ffnodes/\<env>/\<cluster>/values.yaml` override mechanism work?
- How does the chart get deployed (ArgoCD Application of Applications pattern)?

### 2. Template inventory
For each `.tpl` file, describe:
- Its purpose (one sentence)
- The named templates it defines
- Any non-obvious patterns or gotchas

Pay special attention to:
- `_helpers.tpl` — especially `generateVaultDynamicSecrets` and the `tpl` call at line ~80
- `_grafana.tpl` — the Grafana Alloy values factory
- `_certs.tpl` — the conditional cert-manager certificate injection
- `_frontend.tpl` — the Faro secret injection pattern

### 3. Templating patterns catalogue
Identify and name each distinct pattern used across the chart. For each:
- Name the pattern
- Show a representative code snippet
- Explain what problem it solves
- Flag any type-safety or maintainability risks

Known patterns to look for:
- Named template as values factory (`mergeOverwrite + fromYaml`)
- Feature-flag gating (`if .Values.X.enabled`)
- Vault secret wiring via `generateVaultDynamicSecrets`
- Global value propagation to sub-charts
- `fromYamlArray` vs `fromYaml` usage
- `tpl` double-evaluation (VSO template escaping)

### 4. The VSO double-evaluation bug
Explain precisely:
- What `generateVaultDynamicSecrets` does
- Why passing a `secretTransformation` block through Helm's `tpl` function breaks when the block contains `{{get .Secrets "key"}}` expressions
- How `secretTransformationDisableTpl: true` fixes it
- Which other callers in the codebase are at risk of the same bug

Search for all usages: `grep -rn "generateVaultDynamicSecrets\|secretTransformation" charts/ffnode/`

### 5. Multi-cluster configuration analysis
- How many clusters use this chart? List them from `ffnodes/`.
- What varies per-cluster vs what is shared?
- Where is the risk of drift between `ffnodes/\<env>/values.yaml` and other infrastructure (e.g. Cloudflare DNS records, Vault secret paths)?
- How does `frontendobservability` get enabled/disabled per cluster?

### 6. Complexity and bus-factor assessment
Be honest:
- Which parts of the chart are genuinely hard to understand without prior context?
- What would a new engineer struggle with?
- What is the minimum viable documentation that would make this chart self-explanatory?

### 7. Recommendations for type-safe, flexible multi-cluster management
Specific, actionable improvements:
- `values.schema.json` — what fields need type enforcement?
- CI linting — what `helm lint` flags would catch the most common mistakes?
- How to make the `ingress.host` / DNS single source of truth?
- How to make `secretTransformation` safe by default?
- Any patterns that should be replaced with Helm library chart helpers?

---

## Phase 3 — Deliverable

Write the findings as a Markdown document suitable for pasting into Obsidian. Use this frontmatter:

```yaml
---
title: "ffnode Helm Chart — Templating Analysis"
created: \<today>
tags: [helm, kubernetes, grafana-alloy, faro, ffnode, templating, observability, multi-cluster]
ticket: FTFL-673
---

The document should be written so that a mid-level platform engineer with no prior ffnode context can:
1. Understand the chart's architecture in 10 minutes
2. Safely add a new per-cluster feature flag
3. Debug a VSO secret templating error without Ollie's help
4. Understand why certain patterns were chosen and what the risks are

Do not summarise from training data. Every claim must be grounded in a specific file or git commit you actually read.

---
title: "ffnode Helm Chart — Templating Analysis"
created: 2026-06-06
tags: [helm, kubernetes, grafana-alloy, faro, ffnode, templating, observability, multi-cluster]
ticket: FTFL-673
---

# ffnode Helm Chart — Templating Analysis

This document provides a comprehensive analysis of the `ffnode` umbrella Helm chart (GitLab: `fitfile/deployment`), specifically focusing on templating architecture, patterns, and risks. The analysis is grounded in the current state of the chart and the recent `FTFL-673` feature branch.

---

## 1. Chart Architecture Overview

What is `ffnode` responsible for?
`ffnode` is the core "umbrella chart" that defines the topology of a complete FITFILE environment. It does not contain actual application deployments itself. Instead, it delegates to external and internal sub-charts (e.g., MongoDB, PostgreSQL, SpiceDB, Argo Workflows, Grafana Alloy, FITConnect, FFCloud, and Frontend) by defining ArgoCD `Application` Custom Resources (the "App of Apps" pattern). It acts as the central router for global configuration, cross-component wiring, and Vault secret bindings.

How does the `ffnodes/<env>/<cluster>/values.yaml` override mechanism work?
The chart provides a massive `charts/ffnode/values.yaml` acting as the base configuration with sensible defaults. For each customer or environment (e.g., `ffnodes/eoe/cuh-prod-1/values.yaml`), a specific overrides file is maintained. When ArgoCD deploys a cluster, it applies the environment-specific values over the base chart, allowing per-cluster toggling of infrastructure (e.g., `deploy.mssql: true`), resource scaling, and hostnames while keeping the foundational topology identical.

How does the chart get deployed?
It uses the ArgoCD Application of Applications pattern. The main `ffnode` chart loops through its templates (e.g., `grafana-alloy-application.yaml`), emitting ArgoCD `Application` manifests. Each generated `Application` manifest instructs ArgoCD to fetch a specific sub-chart (like `helm/k8s-monitoring` from the FITFILE ACR registry) and deploys it into the target namespace using the synthesized sub-values.

---

## 2. Template Inventory

### `_helpers.tpl`
- Purpose: Central repository for shared logic, naming conventions, global variables, and custom functions.
- Named Templates: `common.tplvaluesRender`, `namespace`, `generateVaultDynamicSecrets`, `renderValuesWithVaultSecretInExtraDeploy`, `escape.tpl`, among others.
- Gotchas: The `generateVaultDynamicSecrets` template performs dynamic generation of Vault Operator CRDs, but suffers from complex `tpl` evaluation problems when dealing with Vault string templating (detailed in Section 4).

### `_grafana.tpl`
- Purpose: A dynamic values factory for constructing the massive Grafana Alloy configuration.
- Named Templates: `ffnode.grafana.values`
- Gotchas: It dynamically builds the `k8s-monitoring` chart values by merging `global` values, constructing receiver/destination blocks (Prometheus, Loki, Tempo), and defining complex nested `alloy-faro` collector configurations if `frontendObservability` is enabled. 

### `_certs.tpl`
- Purpose: Handles conditional injection of cert-manager certificates for dynamically toggled features.
- Named Templates: `ffnode.certManager.certificates`
- Gotchas: It uses the `append` function to inject the `fitfile-frontend-observability` certificate into the global certificate list if `grafanaAlloy.frontendObservability.enabled` and `tls.createCertificate` are true.

### `_frontend.tpl`
- Purpose: Constructs the values payload for the `frontend` application sub-chart.
- Named Templates: `ffnode.frontend.defaults`, `ffnode.frontend.values`, `ffnode.frontend.faroSecret`
- Gotchas: It defines the Faro Bearer Token secret requirement as a `VaultStaticSecret` template (`ffnode.frontend.faroSecret`) and conditionally appends it to `extraVaultSecrets` if Faro is enabled, wiring the retrieved secret as the `FARO_COLLECTOR_TOKEN` environment variable.

---

## 3. Templating Patterns Catalogue

### Pattern 1: Named Template as Values Factory
- Snippet:
  ```yaml
  # grafana-alloy-application.yaml
  values: |
    {{- $values := mergeOverwrite (include "ffnode.grafana.values" . | fromYaml) (dict "vaultSecrets" .Values.grafanaAlloy.vaultSecrets) -}}
    {{include "renderValuesWithVaultSecretInExtraDeploy" (list . $values "extraObjects") | indent 8 }}
  ```

- Solves: Allows for programmable, conditional construction of complex YAML payloads (like the intricate `alloy-faro` configuration) that standard Helm value merging cannot handle easily.
- Risks: Type-safety and Silent Failures. The pipeline `include -> fromYaml -> mergeOverwrite -> toYaml` is dangerous. If the included template produces invalid YAML, `fromYaml` silently fails or produces `null`, resulting in silently broken configurations.

### Pattern 2: Vault Secret Wiring Abstraction

- Snippet:

  ```yaml
  # _helpers.tpl
  {{- $secrets = append $secrets ((include "generateVaultDynamicSecrets" (list $root $item)) | fromYaml) }}
  ```

- Solves: Reduces the boilerplate required to define HashiCorp Vault Secrets Operator (VSO) CRDs. Developers just pass an array of `vaultSecrets` objects in `values.yaml`, and the chart renders full `VaultStaticSecret` or `VaultDynamicSecret` definitions.
- Risks: The abstraction leaks when developers need to use VSO's own templating (see Section 4).

### Pattern 3: VSO Escaping Hack (`escape.tpl` / Escaped Strings)

- Snippet:

  ```yaml
  text: '{{"{{`{{get .Secrets \"mongodb_password\"}}`}}"}}'
  ```

- Solves: Vault Secrets Operator relies on Go templates inside the `VaultStaticSecret` CRD (e.g., `{{ get.Secrets "key" }}`). Because Helm _also_ uses Go templates, passing a literal `{{` through Helm requires intense escaping so Helm ignores it and passes it to VSO.
- Risks: Highly unreadable and prone to syntax errors.

---

## 4. The VSO Double-Evaluation Bug

What `generateVaultDynamicSecrets` does:

It loops over `vaultSecrets` configurations and translates them into HashiCorp VSO `VaultStaticSecret` or `VaultDynamicSecret` CRD YAML definitions.

The Bug:

By default, `generateVaultDynamicSecrets` tries to evaluate the `secretTransformation` block using Helm's `tpl` function:

```yaml
transformation: {{ tpl ($config.secretTransformation | toYaml) $ | nindent 6}}
```

If a developer defines a VSO template like `{{get.Secrets "key"}}` inside `secretTransformation`, Helm's `tpl` function attempts to evaluate it _during the Helm phase_. Because Helm has no `get` function for a `.Secrets` object, the deployment fails with a template rendering error.

The Fix:

Passing `secretTransformationDisableTpl: true` triggers an `if/else` block that skips the `tpl` function, rendering the transformation as raw YAML:

```yaml
{{if hasKey $config "secretTransformationDisableTpl"}}
transformation: {{ $config.secretTransformation | toYaml | nindent 6}}
```

This forces Helm to leave the block untouched, allowing VSO to evaluate it later.

Callers at Risk:

Any component appending to `vaultSecrets` that forgets to include `secretTransformationDisableTpl: true` is at risk if they attempt to use raw VSO template strings instead of the `{{"{{` escaping hack. Currently, `argoWorkflows` and `frontend` (via `_frontend.tpl`) correctly use the disable flag, but most of `values.yaml` still relies on the aggressive escaping strings.

---

## 5. Multi-Cluster Configuration Analysis

- Cluster Footprint: The chart currently orchestrates approximately 27 clusters across different environments (`ffnodes/`), including `barts/prod`, `eoe/cuh-prod-1`, `fitfile/ff-test-a`, `nwsde/nwsde-prod-1`, and `wmsde/ff-wmsde-1`.
- What Varies: Cluster-specific toggles for infrastructure (`deploy.mssql`, `deploy.mongodbNext`), custom hostnames (`host: staging-ac.fitfile.net`), resource request overrides, and feature flags.
- Drift Risk: External dependencies (like Cloudflare DNS, Vault secret mounts/paths, or Azure Storage account names) are loosely coupled via strings in `values.yaml`. If infrastructure changes outside of ArgoCD, Helm will successfully template but the pods will crash at runtime (e.g., missing Vault paths).
- Frontend Observability Flag: Easily enabled per-cluster by setting `.Values.grafanaAlloy.frontendObservability.enabled = true` in the cluster's override file. The templating automatically spins up the `alloy-faro` receiver, requests the certs, and wires the `FARO_COLLECTOR_TOKEN` to the frontend pods.

---

## 6. Complexity and Bus-Factor Assessment

Assessment: High Complexity & Low Bus-Factor

The `ffnode` chart has outgrown standard Helm usages. The utilization of the "Values Factory" pattern (`_grafana.tpl`, `_frontend.tpl`)—where templates generate YAML strings that are immediately parsed back into objects to be merged with other objects—creates a steep learning curve.

What a new engineer would struggle with:

1. Traceability: It is extremely difficult to `grep` for where an environment variable comes from because it might be generated inside an `append` loop in `_frontend.tpl`, merged with defaults, then pushed to ArgoCD application values.
2. The VSO Escape Hatch: Seeing `{{"{{`{{get.Secrets \"api_token\"}}`}}"}}` for the first time is deeply confusing without understanding the Go-template-within-a-Go-template problem.

Minimum Viable Documentation Needed:

A simple architectural map explaining the flow:

`Base values.yaml` + `Cluster values.yaml` -> `Factory Templates (_*.tpl)` -> `ArgoCD Applications` -> `Sub-Charts`.

---

## 7. Recommendations for Type-Safe, Flexible Management

1. Implement `values.schema.json`:
   Helm supports JSON Schema validation. A schema should be added to strictly enforce the types and required fields for critical global variables, Ingress `host` strings, and ensure that `vaultSecrets` arrays have the correct structure.

2. Fix `secretTransformation` default behavior:
   The `secretTransformationDisableTpl: true` should not be a flag; it should be the default behavior. Helm should never attempt to `tpl` evaluate a block destined for VSO unless explicitly requested. This would allow developers to write standard `{{ get.Secrets "foo" }}` without the `{{"{{` hacks.

3. Global DNS Source of Truth:
   Instead of forcing each cluster override to specify `host: staging-argo-workflows.fitfile.net` in multiple places, derive everything automatically from a single global config:

   ```yaml
   global:
     baseDomain: fitfile.net
     environmentSubdomain: staging
   ```

   Then templates can automatically generate deterministic hostnames: `{{.Values.global.environmentSubdomain }}-argo-workflows.{{.Values.global.baseDomain }}`.

4. Linting in CI:
   Add a strict CI step that runs `helm template` against _every_ `ffnodes/<env>/<cluster>/values.yaml` file on every MR. This guarantees that changes to `_helpers.tpl` or base `values.yaml` don't silently break downstream cluster templates.

> A scoring framework for the `ffnode` `.tpl` templating layer, plus a grounded rating of the current setup, viewed through two goals: keeping multiple clusters aligned and maintaining sub-chart versions as the fleet scales.
> Every score is backed by a file/CI fact that was read directly. Companion to [[ffnode-templating-analysis]].

## TL;DR

- Overall ≈ 2.1 / 5, but the profile is bimodal—that's the real finding.
- The architecture is good and scales (App-of-Apps, thin per-cluster overlays, default-with-override version pinning): D1/D2/B2 score 4. Do not re-architect.
- The templating mechanics + safety net are the liability (tpl-on-tpl escaping, no schema, no tests, no CI render): A3/B3/C1/C2/C3/C4 score 1.
- Root causes are two: (1) the VSO secret-transform layer is over-engineered; (2) there is no automated feedback before ArgoCD sync.
- Confirmed anchor fact: CI renders `workflows/*` only—zero `helm template`/lint of `ffnode` or `ffnodes/*` (`.gitlab-ci.yml:106-107`, `validate` stage has only `lint_workflows`).

---

## The framework—4 Dimensions, 13 Metrics

Each metric has an objective proxy you can compute in CI and trend over time. The trend matters more than the absolute value: as cluster count grows, you want each curve flat or falling.

### A. Authoring Complexity (Cognitive Load to Change a tHing)

| Metric | How to measure (proxy) | Why it matters at scale |
|---|---|---|
| A1 Indirection depth | Max chain of `include`/factory hops between a values edit and rendered YAML | Each hop is a place the change can be silently transformed/lost |
| A2 Serialization round-trips | Count of `toYaml→fromYaml` cycles per render path | Every round-trip drops types and turns errors into strings |
| A3 Meta-templating depth | Layers of `tpl`-over-`tpl` / escape nesting | The escaping is the single hardest thing to onboard |
| A4 Convention count | Number of distinct ways to do one task (e.g. secret transforms) | N ways = N×learning + the next dev copies the wrong one |

### B. Coupling & Drift Control (Keeping Clusters aLigned)

| Metric | Proxy | Why |
|---|---|---|
| B1 Value fan-out | For a key, count consumers (templates + external systems) | High fan-out without a single helper = guaranteed drift |
| B2 Base-vs-overlay DRY | Lines in `ffnodes/*` overlay ÷ total config lines | Thin overlays = aligned-by-construction |
| B3 External-contract validation | % of Vault paths / DNS hosts checked in CI | Unvalidated contracts fail per-cluster, at runtime |
| B4 Blast-radius containment | Can a base edit break all clusters with no gate? (y/n) | Determines whether scaling multiplies risk |

### C. Safety Net & Feedback (Ease + cOnfidence)

| Metric | Proxy | Why |
|---|---|---|
| C1 Schema enforcement | `values.schema.json` coverage of required/typed fields | Catches typos at lint, not sync |
| C2 Test coverage | `helm-unittest` cases over the `.tpl` factories | Locks in escaping/merge behaviour |
| C3 CI render coverage | % of `ffnodes/*` rendered+validated per MR | Render _is_ the real test for this chart |
| C4 Feedback latency | Where a mistake surfaces: lint / render / sync / runtime | Earlier = cheaper; runtime-silent = worst |
| C5 Discoverability | Naming consistency + grep-ability of a value | Determines time-to-find |

### D. Version Maintenance at Scale

| Metric | Proxy | Why |
|---|---|---|
| D1 Pin clarity | Every sub-chart version pinned + per-cluster overridable? | Reproducibility |
| D2 Upgrade surface | Edits needed to bump one sub-chart across N clusters | Should be O(1), not O(clusters) |
| D3 Drift visibility | A "which cluster runs which version" report? | You can't align what you can't see |

---

## Scorecard (1 = Poor, 5 = Excellent)

| # | Metric | Score | Grounded evidence |
|---|---|---|---|
| A1 | Indirection depth | 2 | ~5 hops: `ffnode.grafana.values` → `fromYaml` → `mergeOverwrite` → `renderValuesWithVaultSecretInExtraDeploy` → `generateVaultDynamicSecrets` (`grafana-alloy-application.yaml:25-26`) |
| A2 | Serialization round-trips | 2 | 16 `toYaml/fromYaml` calls in `_helpers.tpl` alone; ≥3 full round-trips per app render |
| A3 | Meta-templating depth | 1 | tpl-over-tpl + triple-nested escaping `{{"{{`{{get.Secrets..`}}"}}` (`values.yaml:538-559`) |
| A4 | Convention count | 2 | 3 secret-transform modes (`disableTpl` true×3, false×1, implicit default) + 2 escaping styles |
| B1 | Value fan-out | 2 | `frontendObservability.ingress.host` → 3 in-chart consumers (`_grafana.tpl:37/55`, `_certs.tpl:7`, `_frontend.tpl:45`) + Cloudflare DNS + Vault, no single helper |
| B2 | Base-vs-overlay DRY | 4 | Overlays are thin (namespace/host/toggles); all structure centralised in base `values.yaml` |
| B3 | External-contract validation | 1 | No CI check ties chart keys to Vault paths or DNS records |
| B4 | Blast-radius containment | 2 | A base `values.yaml` edit ships to all clusters; the `fargo` typo proves a base edit breaks 9 clusters silently |
| C1 | Schema enforcement | 1 | No `values.schema.json` (confirmed absent) |
| C2 | Test coverage | 1 | No `tests/` dir, no `helm-unittest` |
| C3 | CI render coverage | 1 | CI renders `workflows/*` only; zero `helm template`/lint of `ffnode` or `ffnodes/*` (`.gitlab-ci.yml:106-107`) |
| C4 | Feedback latency | 1 | Errors surface at ArgoCD sync (render bugs) or runtime (`fargo` typo is runtime-silent—no error at all) |
| C5 | Discoverability | 3 | Consistent `ffnode.*` helper + `deploy.*` flag naming; grep works. Hurt by the `fargo` typo slipping grep |
| D1 | Pin clarity | 4 | `targetRevision: 4.1.4` default + per-cluster override (`grafana-alloy-application.yaml:21`); git-sourced charts pin via `argocdApp.targetRevision` |
| D2 | Upgrade surface | 4 | Bump default once, opt-in stagger per cluster—FTFL-673 rolled 11 non-prod first (`92c88f09`), prod excluded. Already works |
| D3 | Drift visibility | 2 | No automated version-per-cluster report; you'd grep `ffnodes/*` by hand |

Dimension averages: A = 1.75 · B = 2.25 · C = 1.4 · D = 3.3 · Overall ≈ 2.1 / 5.

---

## What the Scores Actually Say

The setup splits cleanly into two halves:

- Architecture is good and scales (D1/D2/B2 = 4s). App-of-Apps + thin per-cluster overlays + default-with-override version pinning is the right shape for "many aligned clusters, staged version rollout." The FTFL-673 rollout (non-prod first, prod held back) proves it in practice. Don't re-architect this.
- Templating mechanics and safety net are the liability (A3/B3/C1/C2/C3/C4 = 1s). Everything weak traces to two root causes:
  1. The VSO secret-transform layer is over-engineered—`tpl`-on-`tpl` plus multiple escaping conventions.
  2. There is no automated feedback before ArgoCD sync—no schema, no tests, no render-in-CI.

The scaling danger: B4 + C4 compound. Every new cluster widens the blast radius of a base edit, while feedback latency means you discover the break at sync or runtime. The `fargo-bearer-token` typo is the canonical case—one character, 9 clusters, zero error emitted.

---

## Three Highest-leverage Moves (In oRder)

1. Add `helm template ffnodes/<each>/values.yaml | kubeconform` to the `validate` stage.
   Biggest single jump: converts C3/C4 from runtime → per-MR, and catches the always-on-Faro class of bug. Cheapest item here.
2. Add `values.schema.json` with `if frontendObservability.enabled then require ingress.host` and typed `deploy.*`.
   Fixes C1; catches the empty-host / missing-required class at lint.
3. Flip the secret-transform default to no-`tpl` (make interpolation opt-in).
   Collapses A3/A4—removes the escaping footgun for ~90% of secrets and the hardest onboarding hurdle.

These touch only the weak dimensions, not the strong architecture. Realistic post-fix landing: ≈ 3.3–3.5 / 5, with the two stated goals (cluster alignment, version maintenance) being the parts that are _already_ strong—they mainly need drift visibility (D3) added: a small CI job that emits a "cluster → sub-chart version" table from `ffnodes/*`.

---

## How to Instrument This (So the Scores Become a Tracked tRend)

- A1/A2: static count of `include`/`toYaml`/`fromYaml` per render path—a `grep | wc` in CI, alert if it rises.
- B1: for each "hot" value (e.g. `ingress.host`), a grep-count of consumers; fail if a value has >1 consumer and no helper.
- B2: ratio of `wc -l ffnodes//values.yaml` to base `values.yaml`; watch it stay low.
- C3: % of `ffnodes/*` that render clean—the CI job from move 1 produces this for free.
- D3: a generated Markdown table, committed per release, of `targetRevision` per cluster.

Track these four numbers per release; if they hold flat while cluster count climbs, the templating layer is scaling. If A1/A2/B1 climb, complexity is outrunning the team.

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Saturday Jun 6, 2026 - 8:41 AM_
---

The March 2026 hotfix evidence is the missing piece that makes the library chart argument conclusive. Here is what it adds to the picture:

---

## The Real Cost of not Having a Library Chart

The `secretTransformationDisableTpl` fix was not a one-time patch—it was a manual chase across individual cluster `render_fitfile.cue` files after each cluster hit the VSO corruption bug in production. Your LTM confirms at least two clusters required explicit remediation: LCA-DP and mkuh-prod-4 (March 2026 Cursor session). Both required the pattern:

```yaml
# render_fitfile.cue
vaultPath: "{{ include \"applicationVaultPath\" . }}"
# Required: ffnode generateVaultDynamicSecrets runs tpl() on secret
secretTransformationDisableTpl: true
```

This is exactly the failure mode a library chart prevents: one correct implementation with a safe default, versioned and consumed by all 27 clusters via `dependencies`, rather than 27 individual files each capable of silently omitting the flag.

## Immediate audit—run This before Any Refactor

```bash
# Find all vaultSecrets blocks that are missing the disableTpl flag
grep -rn "secretTransformation" ffnodes/ \
  | grep -v "DisableTpl" \
  | grep -v "^Binary"
```

Any file appearing in that output is currently vulnerable to the VSO double-evaluation bug. Fix those first—before any library chart extraction—per the sequencing principle your "Additions to the Data-First Customer IaC Plan" note (April 2026) already stated: _"Extracting a broken locals.tf into a shared module amplifies bugs across all customers."_ Same principle applies here.

## Final Verdict on the Question

Library charts partially replace the umbrella patterns—but the more important immediate win is making `disableTpl: true` the default inside the library, so the bug that has already hit LCA-DP and mkuh-prod-4 cannot be reintroduced by any future cluster onboarding. The App-of-Apps topology and the `ffnodes/<env>/values.yaml` per-cluster override mechanism stay exactly as-is. The library chart refactor addresses only the named template layer—and on that layer, it is the correct and sufficient answer.
