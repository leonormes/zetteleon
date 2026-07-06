---
author: Claude Sonnet 4.6 (rust-chart-manager session)
created: 2026-06-24T00:00:00+00:00
date: 2026-06-24
modified: 2026-07-04T10:50:34+00:00
permalink: llmeon/work/ffapp-4566-k8s-monitoring-alloy-image-pull-back-off-investigation-and-v4.1.6-upgrade
related_project: rust-chart-manager (FFAPP-4566)
status: Config fix applied locally (uncommitted); ACR image mirroring still outstanding
tags: [acr, argocd, ffapp-4566, fitfile, grafana-alloy, helm, imagepullbackoff, kubernetes, rust-chart-manager]
title: FFAPP-4566 k8s-monitoring Alloy ImagePullBackOff Investigation and v4.1.6 Upgrade
---

## k8s-monitoring Alloy ImagePullBackOff—Root Cause Investigation & V4.1.6 Upgrade

> Scope: working session in `/Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/rust-chart-manager`—the in-house Rust CLI/TUI (`rust-chart-manager`, tracked under FFAPP-4566) that rewrites vendored Helm charts' `values.yaml` to point image references at FITFILE's private ACR (`fitfileregistry`) before charts are pushed for ArgoCD to deploy. The immediate trigger was a live `ImagePullBackOff` on the Grafana `k8s-monitoring` chart in the `monitoring` namespace. All changes below are local working-tree edits (config + vendored chart); nothing has been committed, pushed, or applied to the cluster. One remediation step (`az acr import`) was identified but deliberately not executed, pending explicit user go-ahead, since it writes to the shared `fitfileregistry` ACR.

---

### 1. Verdict

Two independent, stacked bugs, not one:

1. Detection/config bug (fixed): `config.yaml`'s `overrides:` block for the `k8s-monitoring` chart was targeting top-level YAML keys (`alloy:`, `alloy-events:`, `alloy-logs:`, `alloy-profiles:`) that no template in k8s-monitoring v4.x reads. The chart moved to a CRD/operator architecture (`kind: Alloy`, reconciled by `alloy-operator`) where per-collector settings only flow through `collectorCommon.alloy.*` or `collectors.<name>.*`. Helm merges unknown keys silently—no error, no warning—so the override looked like it worked and never did.
2. ACR content gap (diagnosed, not yet fixed): even with the override path corrected, the specific image tags the Alloy operator actually requests at runtime (`grafana/alloy:v1.16.1`, `prometheus-operator/prometheus-config-reloader:v0.91.0@sha256:…`) are not present in `fitfileregistry` ACR—only older tags are. Worse, this tool's automatic image-discovery mechanism (`src/analysis.rs`) is structurally incapable of finding these images at all, because the operator's default image is filled in by its own Go binary at reconcile time and never appears in any `helm template` output.

A live pod (`grafana-alloy-k8s-monitoring-alloy-events-5458b7dc67-m8f7n`, namespace `monitoring`) was stuck for 9+ minutes in `ImagePullBackOff` on both containers as a direct result.

---

### 2. Symptom (As rEported)

```
Normal   Scheduled  9m28s                   default-scheduler  Successfully assigned monitoring/grafana-alloy-k8s-monitoring-alloy-events-5458b7dc67-m8f7n to aks-system-23892849-vmss00001a
Warning  Failed     8m46s (x3 over 9m28s)   kubelet            Error: ErrImagePull
Warning  Failed     8m6s (x5 over 9m27s)    kubelet            Error: ImagePullBackOff
Normal   Pulling    7m55s (x4 over 9m28s)   kubelet            Pulling image "docker.io/grafana/alloy:v1.16.1"
Warning  Failed     7m54s (x4 over 9m28s)   kubelet            Failed to pull image "docker.io/grafana/alloy:v1.16.1": ... authenticationrequired
Normal   Pulling    7m54s (x4 over 9m28s)   kubelet            Pulling image "quay.io/prometheus-operator/prometheus-config-reloader:v0.91.0@sha256:7d9e4eea5f1139e602508871f422b0116c60e87c662f3dcd234d5ab60cd0d8c1"
Warning  Failed     7m54s (x4 over 9m28s)   kubelet            Failed to pull image "quay.io/prometheus-operator/prometheus-config-reloader:..." ... authenticationrequired
Normal   BackOff    7m20s (x8 over 9m27s)   kubelet            Back-off pulling image "quay.io/prometheus-operator/prometheus-config-reloader:v0.91.0@sha256:..."
Normal   BackOff    4m16s (x21 over 9m27s)  kubelet            Back-off pulling image "docker.io/grafana/alloy:v1.16.1"
```

Both the main `alloy` container and the `configReloader` sidecar were failing—both images were being pulled from their public upstream registries (`docker.io`, `quay.io`) instead of `fitfileregistry.azurecr.io`, despite `config.yaml` appearing to set registry overrides for exactly these images.

---

### 3. Gap 1—Override Path Bug (Root Cause, now fIxed)

#### Mechanism

`k8s-monitoring` (Grafana's `k8s-monitoring-helm` chart) restructured around v4.x to deploy Alloy collectors via a CRD (`apiVersion: collectors.grafana.com/v1alpha1, kind: Alloy`) reconciled by a separate controller, `alloy-operator` (a Chart.yaml dependency, pinned at `0.5.9` in the vendored 4.1.5 copy found on disk). This is not the older architecture where `alloy`, `alloy-events`, `alloy-logs`, `alloy-profiles` were real Helm subchart aliases with their own `image.registry` value paths.

Traced the actual template path (`templates/alloy.yaml` → `templates/collectors/_collector_helpers.tpl`, function `collector.alloy.values`):

```gotemplate
{{- $defaultValues := "collectors/alloy-values.yaml" | .Files.Get | fromYaml }}
{{- $userCommonValues := $.Values.collectorCommon.alloy }}
{{- $globalValues := include "collector.alloy.values.global" . | fromYaml }}
{{- $userValues := (index $.Values.collectors .collectorName) }}
{{ mergeOverwrite $defaultValues $presetValues (deepCopy $globalValues) (deepCopy $userCommonValues) $clusterNameValues (deepCopy $userValues) | toYaml }}
```

Only `collectorCommon.alloy.*` (applies to every Alloy collector instance) and `collectors.<collectorName>.*` (applies to one) ever reach the rendered CR spec. The chart's own local default file (`collectors/alloy-values.yaml`) has no `image`/`configReloader` key at all—and crucially, the CR's `spec.image`/`spec.configReloader.image` is left completely absent unless one of those two value paths supplies it. There is no top-level `alloy:`/`alloy-events:` key read anywhere in the chart.

#### Empirical Verification

Confirmed by rendering the chart directly (`helm template … --show-only templates/alloy.yaml`) for a synthetic `alloy-events` collector:

- Before fix (old `overrides:` block setting `alloy-events.image.registry` etc.): rendered `Alloy` CR had no `image:` or `configReloader:` field whatsoever—proving the override was completely inert. This is exactly why the operator fell back to its own built-in defaults (`docker.io/grafana/alloy:v1.16.1`, `quay.io/…/prometheus-config-reloader:v0.91.0`).
- After fix (`overrides.collectorCommon.alloy.image.registry` / `…configReloader.image.registry` set to `fitfileregistry.azurecr.io`): rendered CR correctly shows:

  ```yaml
  spec:
    image:
      registry: fitfileregistry.azurecr.io
    configReloader:
      image:
        registry: fitfileregistry.azurecr.io
  ```

Note `kube-state-metrics`, `prometheus-node-exporter`, and `opencost` were unaffected by this bug—those genuinely are real Helm subchart aliases (declared as dependencies under the `telemetry-services` feature chart), so their existing `<alias>.image.registry` overrides work as a normal Helm pass-through.

#### Pre-existing Partial Fix Attempt (Found in the Working Tree before This sEssion)

`git status` at session start already showed `config.yaml` as modified (uncommitted), pre-dating this conversation. The pre-existing diff against `HEAD` included an earlier, also-incorrect attempt to fix the same symptom: the `gitops.images` "alloy" entry had been changed from `registry_path: "global.image.registry"` / `tag_path: "alloy-metrics.image.tag"` to `registry_path: "alloy.image.registry"` / `tag_path: "alloy.image.tag"`—i.e. someone had already noticed `global.image.registry` was wrong and "fixed" it, but landed on `alloy.image.registry`, which is equally dead for the reason above. This confirms the CRD-architecture nuance was the actual blocker, not a typo.

#### Fix Applied (config.yaml)

Replaced four duplicated, dead per-collector override blocks with one block targeting the path the templates actually read:

```yaml
overrides:
  # k8s-monitoring v4.x deploys Alloy via the alloy-operator CRD, not subchart
  # aliases. The per-collector image only flows through `collectorCommon.alloy`
  # (applies to every Alloy instance) or `collectors.<name>`. Top-level keys like
  # `alloy:` / `alloy-events:` are not read by any template and silently no-op.
  collectorCommon:
    alloy:
      image:
        registry: "fitfileregistry.azurecr.io"
      configReloader:
        image:
          registry: "fitfileregistry.azurecr.io"
  kube-state-metrics: { image: { registry: "fitfileregistry.azurecr.io" } }
  prometheus-node-exporter: { image: { registry: "fitfileregistry.azurecr.io" } }
  opencost: { ... unchanged, still valid subchart aliases ... }
```

Also corrected the still-active `gitops.images` "alloy" entry (used by `src/rewriter.rs`'s registry-forcing loop, independent of `overrides:`) from the dead `alloy.image.*` path to the correct one:

```yaml
- name: "alloy"
  tag_path: "collectorCommon.alloy.image.tag"
  registry_path: "collectorCommon.alloy.image.registry"
  repository_path: "collectorCommon.alloy.image.repository"
```

---

### 4. Gap 2—ACR Content Gap (Diagnosed; Remediation pending aPproval)

#### Mechanism

Even with the value path fixed, fixing _where_ the registry override lands doesn't help if the resulting image:tag doesn't exist in that registry. Live ACR check (`az acr repository show-tags`) at investigation time:

| Image | Tags present in `fitfileregistry` ACR | Tag the operator actually requests |
|---|---|---|
| `grafana/alloy` | `v1.11.2`, `v1.12.2`, `v1.3.1` | `v1.16.1` |
| `prometheus-operator/prometheus-config-reloader` | `v0.81.0` | `v0.91.0@sha256:7d9e4eea5f1139e602508871f422b0116c60e87c662f3dcd234d5ab60cd0d8c1` |

The repositories themselves exist in ACR (`grafana/alloy`, `prometheus-operator/prometheus-config-reloader`, `grafana/alloy-operator`, plus `bitnami/grafana-alloy` and `helm/grafana-alloy` artifacts)—only the specific tags the v4.x operator needs are missing.

#### Why This Tool Can Never Auto-discover This (Structural fInding)

Traced the image-mirroring pipeline fully:

- `src/analysis.rs::scan_blueprint` runs `helm template`, then `traverse_yaml` walks the rendered manifests looking for mapping keys literally named `image` whose value is a string (`image: "repo:tag"`).
- The Alloy CR's image config is a nested object (`image: {registry, repository, tag}`), not a flat string—`traverse_yaml` does not match it (`if let Value::String(s) = img_val` fails for a `Mapping`).
- Even if it did match the shape, the actual tag (`v1.16.1` / `v0.91.0@sha256:…`) never appears in any rendered manifest at all—the operator's default tag is a constant compiled into its Go binary, filled in only at live reconcile time, completely outside Helm's rendering reach. Confirmed by diffing `collectors/alloy-values.yaml` (the chart's local defaults file) and `collectors/upstream/alloy-values.yaml` (the reference upstream-chart defaults)—neither is wired into the CR-building template path, and the chart ships no `annotations.images` metadata in `Chart.yaml` that could have served as an escape hatch (the tool's `scan_chart_metadata` function checks for exactly that, and it's absent here).
- This means `src/importer.rs::internalize_chart` (which drives `az acr import` based on what `analysis.rs` discovers) never had a chance to mirror these two images. This is a genuine blind spot for any operator/CRD-pattern chart, not specific to a misconfiguration—Alloy is the first chart in this config where it bites.

#### Proposed Remediation (Not executed—needs Explicit Confirmation, Writes to Shared ACR)

```sh
az acr import --name fitfileregistry --source docker.io/grafana/alloy:v1.16.1 --image grafana/alloy:v1.16.1

az acr import --name fitfileregistry \
  --source quay.io/prometheus-operator/prometheus-config-reloader@sha256:7d9e4eea5f1139e602508871f422b0116c60e87c662f3dcd234d5ab60cd0d8c1 \
  --image prometheus-operator/prometheus-config-reloader:v0.91.0
```

The second command imports by digest specifically and tags it `v0.91.0` in ACR—preserving the exact `v0.91.0@sha256:7d9e…` combined reference the operator requests, since `az acr import` copies the manifest byte-for-byte (same digest, new registry).

---

### 5. V4.1.6 Upgrade

User requested upgrading the vendored chart from 4.1.5 → 4.1.6 (separately from the bug fix above).

#### What Changed (Verified via `helm pull` + Diff, not aSsumed)

- `Chart.yaml`: chart version 4.1.5 → 4.1.6; `alloy-operator` dependency 0.5.9 → 0.5.10; `kube-state-metrics` dependency 7.3.0 → 7.5.1 (per `CHANGELOG.md`, also Beyla bump unrelated to this).
- `CHANGELOG.md` (4.1.6 entries):
  - Fix deployment-notes empty "It will:" section when no local features enabled.
  - Fix OTLP destination `timeout` rendering at the wrong nesting level—"Alloy 1.16.3+ rejects the misplaced attribute (`unrecognized attribute name "timeout"`), causing the collector to fail to start." (Confirms the live fleet is tracking the Alloy 1.16.x line generally—consistent with, though not proof of, the `v1.16.1` tag the operator requested pre-fix.)
  - Expanded platform detection (AKS/GKE/EKS recognition via node labels/cloud provider IDs) feeding into `remotecfg` reporting.
- `templates/collectors/_collector_helpers.tpl` and `templates/alloy.yaml` (the files this entire investigation hinges on): byte-identical between 4.1.5 and 4.1.6—no change to how `collectorCommon.alloy` flows into the CR spec.
- `collectors/upstream/alloy-values.yaml`: one cosmetic addition (`externalTrafficPolicy: Cluster` under a service block)—no change to image defaults.
- Pulled `alloy-operator` 0.5.10 standalone for comparison: its own `alloy-values.yaml` reference defaults file is identical to 0.5.9's except for the same `externalTrafficPolicy` line—no visible change to default image tag/registry fields in any file we have access to. (Caveat: the operator's actual runtime default is compiled into its Go binary and cannot be confirmed from static chart files either way—see Gap 2. The ACR tag gap identified above should be assumed to still apply post-upgrade until verified live.)

#### Actions Taken

1. `config.yaml`: `gitops.upstream.version` corrected from a stale `"^3.7.5"` (which didn't even match the _previously_ vendored 4.1.5 chart—a pre-existing drift, unrelated to this session's bug) to `"4.1.6"`.
2. `helm/k8s-monitoring/` (gitignored vendor directory, not tracked in git): replaced wholesale via `helm pull oci://ghcr.io/grafana/helm-charts/k8s-monitoring --version 4.1.6 --untar`, fully vendored with subcharts (confirmed `charts/alloy-operator`, `charts/telemetry-services`, all `feature-*` subcharts present, ~3.3MB).
3. Re-applied the registry overrides into the fresh `values.yaml` using `yq` (replicating exactly what `src/rewriter.rs::rewrite_with_gitops` would produce): `collectorCommon.alloy.image.registry`, `collectorCommon.alloy.configReloader.image.registry`, plus the legitimate subchart-alias overrides (`kube-state-metrics`, `prometheus-node-exporter`, `opencost.*`, `alloy-operator.image.registry`). Removed a stray dead top-level `alloy.image.registry` key left over from mirroring the old (now-corrected) `gitops.images` path.
4. Re-verified via `helm template` (both the targeted `templates/alloy.yaml` render for a synthetic `alloy-events` collector, and a full-chart render using the exact `analysis_overrides` already in `config.yaml`) that the fix holds identically on 4.1.6: `image.registry` and `configReloader.image.registry` both appear correctly in the rendered `Alloy` CR, and the full chart renders without error.

---

### 6. Current Repo State

All changes are local, uncommitted working-tree edits. Nothing pushed, nothing committed, no cluster changes made, no ACR writes made.

- `config.yaml`—modified (diff includes this session's changes layered on top of pre-existing uncommitted changes from before this session: a `trivy-operator` restructure, an `analysis_overrides.destinations` shape fix, and the earlier partial/incorrect "alloy" path attempt described in §3).
- `helm/k8s-monitoring/`—gitignored (`.gitignore:23`), so the chart-version swap and re-applied overrides do not appear in `git status`/`git diff` at all; only `config.yaml` does.
- `src/azure.rs`, `src/lib.rs`, `src/model.rs`, `src/pusher.rs`, `test_overrides.yaml`—pre-existing uncommitted changes from before this session, unrelated to this investigation (Azure/Helm registry login plumbing for pushes, and a `k8s-monitoring`-specific guardrail rejecting list-shaped `analysis_overrides.destinations`). Not touched this session.

#### Codebase Mechanics Worth Recording for Future Work on This Tool (FFAPP-4566)

- `src/rewriter.rs::rewrite_with_gitops`: merges `blueprint.overrides` (blind deep-merge, zero schema validation—this is _why_ the dead-key bug was silent) then, separately, for each `gitops.images[]` entry with a `registry_path`, force-writes the target ACR domain at that path via `set_value_by_path` (which creates the nested map path if missing). `tag_path` / `repository_path` are parsed into the model (`src/model.rs`) but are explicitly marked `// 2. Repository/Tag Replacement (Future Scope)`—not yet implemented. Only `registry_path` is live.
- `src/analysis.rs::traverse_yaml`: the sole image-discovery mechanism feeding `src/importer.rs::internalize_chart`'s `az acr import` calls. Only matches flat string `image:` values in rendered manifests, plus `annotations.images` metadata in `Chart.yaml` if present. Cannot discover CRD/operator-pattern images (nested `image: {registry,repository,tag}` objects, or any image whose value is decided by controller code rather than rendered by Helm). This is a structural limitation, not a bug—worth a deliberate design decision if more operator-pattern charts get added to `config.yaml` in future (cert-manager, trivy-operator, etc. are unaffected since they use plain Deployments).

---

### 7. Open Questions for Humans

1. Confirm before running: should the two `az acr import` commands in §4 be executed now to unblock the live `monitoring` namespace pods? (Writes to shared `fitfileregistry` ACR—deliberately not run without sign-off.)
2. Is the `alloy-operator` 0.5.10 binary's default Alloy/config-reloader image tag actually still `v1.16.1`/`v0.91.0`, or did it change alongside the 0.5.9→0.5.10 bump? Static chart inspection cannot answer this (see §3/§5)—only observing what image a freshly-synced pod actually requests post-upgrade will confirm it. If it changed, the `az acr import` targets in §4 need to be re-derived from the new pod's `kubectl describe pod` output rather than assumed.
3. Should the tool (`rust-chart-manager`) gain a guardrail that validates `overrides:` keys against the chart's actual rendered output (e.g. round-trip the merged values through `helm template` and warn if a key never appears in any rendered manifest)? This would have caught Gap 1 automatically instead of requiring manual chart-architecture archaeology.
4. Is there an appetite for extending `src/analysis.rs` to special-case known operator CRDs (e.g. explicitly enumerate `Alloy` CR's `image`/`configReloader.image` fields) so this class of chart gets proper auto-mirroring instead of relying on manually maintained `gitops.images` entries plus manual `az acr import`?

---

### 8. Key Evidence Index

- Live pod: `monitoring/grafana-alloy-k8s-monitoring-alloy-events-5458b7dc67-m8f7n`—`kubectl describe pod` events (verbatim in §2).
- Chart source: `helm/k8s-monitoring/templates/alloy.yaml`, `helm/k8s-monitoring/templates/collectors/_collector_helpers.tpl` (function `collector.alloy.values`, `collector.alloy.valuesToSpec`).
- Chart defaults compared: `helm/k8s-monitoring/collectors/alloy-values.yaml` (local, no image keys) vs `helm/k8s-monitoring/collectors/upstream/alloy-values.yaml` (upstream Alloy chart reference defaults—`image.registry: docker.io`, `image.repository: grafana/alloy`, `configReloader.image.registry: quay.io`, `configReloader.image.tag: v0.91.0@sha256:7d9e…`).
- Tool source: `src/rewriter.rs` (`rewrite_with_gitops`, `set_value_by_path`, `merge_values`), `src/analysis.rs` (`scan_blueprint`, `traverse_yaml`, `scan_chart_metadata`), `src/importer.rs` (`internalize_chart`, `import_single_image`), `src/model.rs` (`GitOps`/image struct defs).
- Config: `config.yaml`—`k8s-monitoring` chart block (`overrides:`, `gitops:`), lines ~293–375 at time of writing.
- ACR snapshot (`az acr repository show-tags --name fitfileregistry`): `grafana/alloy` → `v1.11.2, v1.12.2, v1.3.1`; `prometheus-operator/prometheus-config-reloader` → `v0.81.0`.
- Chart version diff source: `helm pull oci://ghcr.io/grafana/helm-charts/k8s-monitoring --version 4.1.6` vs the previously-vendored 4.1.5 copy; `helm pull oci://ghcr.io/grafana/helm-charts/alloy-operator --version 0.5.10` for standalone comparison.
- Git history: `git log --oneline` shows this tool's development tracked under commit messages `FFAPP-4566` (e.g. `c7c1bea`, `6951049`, `047e939 FFAPP-4566 add a tui`), most recent two commits (`4af5e00`, `27c98c1`) are `feat:`-style and reference Grafana OCI registry / alloy config work directly relevant to this investigation.
