---
title: FITFILE k8s-monitoring Config Audit
date: 2026-06-25
tags:
- kubernetes
- observability
- grafana
- helm
- alloy
- argocd
- fitfile
source: /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment
chart-version-pinned: 4.1.6
related: '[[k8s-monitoring-helm Deep Analysis]], [[FTFL-747 Alloy Metrics Coverage
  - Verification Report]]'
permalink: llmeon/fitfile-k8s-monitoring-config-audit
---

# FITFILE Deployment Repo — k8s-monitoring Config Audit

Companion note to [[k8s-monitoring-helm Deep Analysis]]. This audit applies that report's knowledge of `grafana/k8s-monitoring-helm` v4.x internals to the actual config in `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment`, under `charts/` and `ffnodes/`.

## Update — 2026-06-25: fixes pulled in

A pull landed commit range `96118a27..50b483f4` (checked via `sem diff`/`git diff` against that range) touching `charts/ffnode/templates/_grafana.tpl`, `charts/ffnode/templates/grafana-alloy-application.yaml`, `charts/ffnode/values.yaml`, `charts/local-dev/argocd-apps-values.yaml`, and two EOE site values files. Three of these are genuine fixes to issues this audit either flagged or would have flagged; details folded into the tables below, with status notes on the resolved rows.

## Update — 2026-06-25: FTFL-747 and the metrics coverage extension

Issue #1 (`clusterMetrics.scrapeJobs`, the dead trivy-operator scrape config) is now resolved — see [[FTFL-747 Alloy Metrics Coverage - Verification Report]] for full implementation + live Grafana Cloud query evidence. Same fix pattern (`prometheusOperatorObjects` scoped by namespace) was then extended to argocd, argo-workflows, minio, mongodb, postgresql, and spicedb in a follow-up MR — all now confirmed flowing real metrics in the staging/testing clusters, with two minor partial-scrape findings (`argocd-dex-server` fully down, Argo Workflows' `telemetry` endpoint down but its main `metrics` endpoint healthy) tracked in that report rather than duplicated here. vault-secrets-operator was deferred (its metrics sit behind `kube-rbac-proxy`, real TLS/RBAC work, separate follow-up).

Issues #2–#6 and #8 are untouched by any of this and remain open exactly as before.

## Architecture: how monitoring is actually wired here

The `ffnode` chart is a wrapper. It deploys **one** ArgoCD `Application` per site (`charts/ffnode/templates/grafana-alloy-application.yaml`) pointing at `fitfileregistry.azurecr.io/helm/k8s-monitoring`, now `targetRevision: 4.1.6` by default (`charts/ffnode/values.yaml:527`, bumped from `4.1.4` — see Resolved #7 below). The entire `destinations`/`telemetryServices`/`clusterMetrics`/`clusterEvents`/`podLogsViaLoki`/`collectors` config is **hardcoded in one shared template**, `charts/ffnode/templates/_grafana.tpl`, with only a handful of per-site knobs exposed through `values.grafanaAlloy.*` (`frontendObservability`, `opencost`, `structuredMetadataPilot`, plus top-level `proxy.*`). Per-site `values.yaml` files are deliberately thin — most sites only set Faro ingress host/TLS.

This is good design intent (one source of truth, no per-site drift on the hard parts) but it also means a bug in `_grafana.tpl` is a bug everywhere, and a few things have drifted.

## What's done well (matches the upstream report's best practices)

- **Secrets**: every destination uses `secret.create: false` + `usernameKey`/`passwordKey` against one `monitoring` K8s Secret, populated from Vault — exactly the "external secret" pattern flagged as the production-grade choice in the upstream report. They've gone further: the **host/URL** is also pulled from Vault via `urlFrom` raw Alloy expressions (`remote.kubernetes.secret.<name>.data["...-host"]`), so even the Grafana Cloud stack endpoint is per-site and never hardcoded in git.
- **Explicit `collector:` on every feature** (`clusterMetrics`, `costMetrics`, `hostMetrics`, `clusterEvents`, `podLogsViaLoki`, `applicationObservability`, and now `prometheusOperatorObjects`/`annotationAutodiscovery`) — exactly the rule that becomes mandatory the moment you have >1 collector.
- **Cardinality tuning already applied**: `kube_secret_metadata_resource_version` excluded, and a `labeldrop` on cAdvisor's `id`/`container_id` — both textbook applications of the levers documented in the upstream report.
- **`alloy-logs` correctly shaped** (`presets: [filesystem-log-reader]` + `controller.type: daemonset`) and **`alloy-faro`** correctly carries `--stability.level=experimental` (required for `otelcol.receiver.faro`).
- **The FTFL-638 job-label bug is fixed, and fixed in the right place.** `GRAFANA_ALLOY_FIX_PLAN.md` documents a real upstream v3.7.5 bug (`replacement = "$1"` only capturing the namespace half of `namespace/container`). That corrective `extraDiscoveryRules` rule is baked directly into the shared `podLogsViaLoki` block (`_grafana.tpl:236-242`) — so every site gets it automatically.
- **All collector and config-reloader images are now pulled through the private ACR mirror** (`collectorCommon.alloy.image.registry` / `collectorCommon.alloy.configReloader.image.registry` → `fitfileregistry.azurecr.io`).
- **Several existing-but-unused `ServiceMonitor`s discovered and put to use** (argocd ×6, argo-workflows, minio, mongodb), plus one missing one fixed (postgresql) and one annotation-discovery path enabled (spicedb) — see the FTFL-747 report for detail.

## Issues found (still open)

| # | Finding | Confidence | Citation |
|---|---|---|---|
| 2 | **`costMetrics.enabled: false` is hardcoded unconditionally**, while `telemetryServices.opencost.deploy` *is* correctly gated on `.Values.grafanaAlloy.opencost.enabled`. Cost dashboards in Grafana Cloud likely show nothing on any site with OpenCost enabled. | High | `_grafana.tpl:142-175` (templated) vs `:210-213` (not templated) |
| 3 | **OpenCost's external Prometheus query endpoint is hardcoded** to `https://prometheus-prod-05-gb-south-0.grafana.net/api/prom`, while every other destination URL is resolved dynamically per-site from Vault. (Confirmed via `gcx datasources list` during FTFL-747 verification — this is the same URL/stack the staging/testing clusters actually use, so at least correct for those two; still wrong for any site on a different stack.) | High | `_grafana.tpl:154` |
| 4 | **`structuredMetadataPilot` is a dead flag.** Set `enabled: true` for `testing`, but `_grafana.tpl`'s `structuredMetadata:` block is static and never references it. | High (on this checkout) | `charts/ffnode/values.yaml:552-558`; zero matches under `charts/ffnode/templates/` |
| 5 | **`ffnodes/nwsde/mcnft-prod-1/values.yaml`'s entire `grafana:` block appears to be dead configuration** — the chart only reads `.Values.grafanaAlloy.*`. Caveat: can't rule out an older deployed chart ref still reading `.Values.grafana`. | Medium-high | `ffnodes/nwsde/mcnft-prod-1/values.yaml:59-194`; not touched by either pull |
| 6 | **`kch/prod` and `kch/mn4` have no k8s-monitoring/Grafana Alloy deployment at all.** | High | grep across `ffnodes/kch/{prod,mn4}/templates/*.yaml` → no matches; not touched |
| 8 | Minor: `eoe/cuh-prod-1/values.yaml` carries a dead commented-out "Legacy grafana k8s-monitoring configuration" block. Cosmetic only — the real `proxy.enabled`/`proxyUrl` fix is correctly in place. | Confirmed, cosmetic | `ffnodes/eoe/cuh-prod-1/values.yaml:98-176` |
| 11 (new) | **`argocd-dex-server`'s metrics endpoint doesn't respond** (`up=0` on both staging and testing clusters, 2/2 endpoints). Scrape config is correct (proven by FTFL-747's coverage extension) — Dex itself isn't answering on port 5558. | Confirmed live | See [[FTFL-747 Alloy Metrics Coverage - Verification Report]] |
| 12 (new) | **Argo Workflows' `telemetry` endpoint (port 8081) doesn't respond**, but its main `metrics` endpoint (port 9090) is healthy with real data. Low severity — the app is monitored, just not on that one extra endpoint. | Confirmed live | Same report |

## Resolved

| # | Finding | Resolution | Citation |
|---|---|---|---|
| 1 | `clusterMetrics.scrapeJobs` (the trivy-operator scrape config) is not a real key in this chart and does nothing — silently accepted, silently dropped, no scrape, no data. | ✅ **Fixed via FTFL-747.** Replaced with `prometheusOperatorObjects`, scoped to existing `ServiceMonitor`s by namespace, then extended to argocd/argo-workflows/minio/mongodb/postgresql/spicedb in a follow-up. Live Grafana Cloud queries confirm real metrics flowing (`argocd_app_info`, `mongodb_up`, `pg_up`, etc.) — see [[FTFL-747 Alloy Metrics Coverage - Verification Report]] for the full before/after evidence. | `charts/ffnode/templates/_grafana.tpl` |
| 7 | Chart was pinned two patch releases behind (`4.1.4` vs `4.1.6`). | ✅ **Fixed.** `targetRevision` default bumped `4.1.4` → `4.1.6` in both `charts/ffnode/values.yaml:527` and `charts/ffnode/templates/grafana-alloy-application.yaml:21`. Picks up the 4.1.6 OTLP `timeout`-placement fix and 4.1.5's Node Exporter port-conflict guard before either becomes load-bearing. | `git diff 96118a27 50b483f4 -- charts/ffnode/values.yaml charts/ffnode/templates/grafana-alloy-application.yaml` |
| 9 | **`alloy-faro`'s Alloy config had an unquoted `proxy_url`** — invalid River/Alloy syntax. Would have broken the `alloy-faro` receiver collector's config parse on any site with both `proxy.enabled: true` and `frontendObservability.enabled: true` (matches `eoe/cuh-prod-1` exactly). | ✅ **Fixed** (FTFL-673 "grafana alloy chart image fix"). Changed to `proxy_url = "{{ .Values.proxy.proxyUrl }}"`. Worth a quick check that CUH's `alloy-faro` pod is now actually Running and the Faro ingress is receiving frontend telemetry, since it may have been silently broken until now. | `_grafana.tpl` diff: `git diff 96118a27 50b483f4 -- charts/ffnode/templates/_grafana.tpl` |
| 10 | Alloy and config-reloader images weren't pinned to the private ACR mirror, unlike other components in this repo. | ✅ **Fixed.** Added to `_grafana.tpl`: `collectorCommon.alloy.image.registry` and `collectorCommon.alloy.configReloader.image.registry` → `fitfileregistry.azurecr.io`. **Correction to the companion deep-dive report**: that report's Phase 3 table originally said the config-reloader sidecar was "not found by any research pass" — it does exist (upstream Alloy chart's second DaemonSet container, `alloy.configReloader.*`), and the deep-dive note has since been corrected to reflect this. | `_grafana.tpl` diff, same range |

## Other changes observed in the latest pull (informational, not bugs)

- EOE HIE Faro ingress switched from a dedicated private-link host to fanout mode on both `hie-prod-34` and `hie-test-34` (`grafanaAlloy.frontendObservability.ingress.fanoutEnabled: true`, reusing `tls.existingSecret: fitfile-eoe-tls` instead of issuing a new cert) — part of the broader FTFL-999 theme (avoiding new DNS/firewall allowances for dedicated Faro subdomains, same reasoning seen earlier for CUH). Both sites also added a cert `secretTemplate` with `reflector.v1.k8s.emberstack.com` annotations to replicate the TLS secret into the `monitoring` namespace.
- Local-dev (`charts/local-dev/argocd-apps-values.yaml`) gained a `grafanaAlloy` block and a placeholder `monitoring` Secret manifest so local dev clusters can stand up the full Alloy + Faro stack.

## One thing worth knowing, not fixing

`telemetryServices.node-exporter.hostNetwork: false` (`_grafana.tpl:139-141`) sidesteps the AKS-port-9100-clash problem the original fix plan worked around with `hostNetwork: true` + remapping to port 9101. Disabling `hostNetwork` entirely is a cleaner, more portable fix — at the cost of `node_network_*` metrics reflecting the pod's virtual interface rather than the host's real NICs.

## Suggested next actions, roughly in priority order

1. Confirm intent on **#2 (costMetrics hardcoded off)** and **#3 (hardcoded OpenCost query URL)** — these together likely mean cost dashboards are silently broken on every site that has `opencost.enabled: true`.
2. Investigate **#11 (`argocd-dex-server` down)** and **#12 (Argo Workflows `telemetry` endpoint down)** — both confirmed live, neither blocking, both worth a quick look.
3. Verify what git ref `mcnft-prod-1` is actually deployed from, then either delete the dead `grafana:` block (#5) or treat it as an active production bug.
4. Decide whether to finish wiring `structuredMetadataPilot` (#4) or remove the flag.
5. Confirm whether KCH sites (#6) are intentionally unmonitored.
6. Scope and schedule the vault-secrets-operator metrics work (TLS + RBAC for `kube-rbac-proxy`) — deferred from the coverage-extension MR.