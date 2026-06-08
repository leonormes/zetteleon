---
created: 2026-06-08T11:46:30+00:00
modified: 2026-06-08T11:48:10+00:00
---
*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday Jun 8, 2026 - 12:46 PM*
---
All cursors are now drained — both returned `recommendation: sufficient`. The evidence base is complete. Here is the Hermes `/goal` prompt.

---

## Hermes `/goal` prompt — structured metadata experiment

Paste this directly into `hermes --tui`:

```text
/goal Add structured metadata enrichment to Grafana Cloud logs via the ffnode Helm chart

# CONTEXT

The testing cluster (`fitfile-cloud-testing-aks-cluster`) has recently been restored after an outage
where all Grafana Alloy pods were missing (root cause: `metricsSource: prometheus` in `_grafana.tpl:126`
instead of `metricsSource: custom` — fixed in MR !792 / branch `feature/FTFL-673-fixes-for-opencost`,
now merged). Logs are now flowing again.

The current Loki log shape (example from `argocd` namespace) has these **indexed stream labels**:
  app_kubernetes_io_name, cluster, container, flags, job, k8s_cluster_name, namespace, pod,
  service_name, service_namespace, stream

And this **existing structured metadata**:
  service_instance_id: "argocd.argocd-application-controller-0.application-controller"

The goal is to enrich structured metadata with additional non-indexed context fields that make
logs richer in Grafana Explore without bloating the Loki index. This is a gated pilot scoped
to the `fitfiletest` (non-prod) stack only, controlled by a toggle in `values.yaml`.

Jira ticket context: FTFL-673 (Upgrade Grafana Alloy) — this enrichment experiment is a follow-on
to the chart upgrade already shipped.

Key gotcha from prior audit: Alloy does NOT have `stage.static_structured_metadata`. To inject
static values, use `stage.static_labels` first, then promote into `stage.structured_metadata`.

# KEY FILES

- `deployment/charts/ffnode/values.yaml` — add the pilot toggle here
- `deployment/charts/ffnode/templates/_grafana.tpl` — wire the Alloy `extraStageBlocks` here
- `deployment/ffnodes/fitfile/ff-test-a/values.yaml` — enable the pilot for fitfiletest only

# PHASE 1 — Add the pilot toggle to the base chart

In `deployment/charts/ffnode/values.yaml`, add the following under `grafanaAlloy`:

```yaml
grafanaAlloy:
  structuredMetadataPilot:
    enabled: false   # set true per-cluster in ffnodes/
    workload: ""     # informational only, e.g. "argocd"

# PHASE 2 — Wire the toggle into `_grafana.tpl`

In `deployment/charts/ffnode/templates/_grafana.tpl`, inside the `{{ define "ffnode.grafana.values" }}` block,
add a conditional `extraStageBlocks` section that activates only when the pilot flag is set:

```yaml
{{- if .Values.grafanaAlloy.structuredMetadataPilot.enabled }}
logs:
  podLogsViaLoki:
    enabled: true
    extraRelabelingRules: |
      rule {
        action = "labeldrop"
        regex  = "container|service_name|service_namespace|stream|flags"
      }
    extraStageBlocks: |
      stage.structured_metadata {
        values = {
          container        = "container",
          service_name     = "service_name",
          service_namespace = "service_namespace",
          stream           = "stream",
        }
      }
{{- end }}

This moves `container`, `service_name`, `service_namespace`, and `stream` out of indexed labels and
into non-indexed structured metadata.

# PHASE 3 — Enable the pilot for fitfiletest only

In `deployment/ffnodes/fitfile/ff-test-a/values.yaml`, add:

```yaml
grafanaAlloy:
  structuredMetadataPilot:
    enabled: true
    workload: "argocd"

Do NOT touch any other ffnodes/ cluster values files. Leave staging and prod unchanged.

# PHASE 4 — Validate before committing

1. Run `helm template deployment/charts/ffnode -f deployment/ffnodes/fitfile/ff-test-a/values.yaml`
   and confirm the rendered Alloy config contains `stage.structured_metadata` with the moved fields.
2. Confirm the rendered config does NOT contain those fields in the `extraRelabelingRules` labeldrop
   section for any cluster where `structuredMetadataPilot.enabled: false`.

# SUCCESS CRITERIA

- [x] `helm template` renders `stage.structured_metadata` for `ff-test-a` and NOT for other clusters
- [x] `{cluster="testing", namespace="argocd"}` query returns logs in Explore
- [x] `container`, `service_name`, `service_namespace`, `stream` visible in log detail panel as metadata
- [x] Indexed label count for `cluster="testing"` does not increase

# DO NOT

- Touch `staging`, `prod-1`, `barts`, `eoe`, or any CUH cluster values files
- Remove `cluster`, `namespace`, `job`, or `app_kubernetes_io_name` from indexed labels — these are the
  stable stream selectors that all existing queries and dashboards depend on
- Add `stage.static_structured_metadata` — that stage does not exist in Alloy; use `stage.static_labels`
  + `stage.structured_metadata` if you need static values
- Move `pod` back into structured metadata — prior audit (FTFL-638) confirmed `pod` must stay as an
  indexed stream label or selector queries break
- Commit without running `helm template` to validate the rendered output first
```

---

**Why these specific fields?** Based on your cardinality audit evidence: `container`, `service_name`, `service_namespace`, and `stream` are the highest-cardinality bloat candidates from the indexed label set visible in the log you shared, and they are safe to demote — you don't use them inside `{}` stream selectors, but they are useful context when you click into a log line. The fields that must stay indexed — `cluster`, `namespace`, `job`, `app_kubernetes_io_name` — are all stable, low-cardinality selectors your dashboards depend on.

**Note on the typical log you shared:** `k8s_cluster_name` is a direct duplicate of `cluster` — that's another candidate to labeldrop entirely (rather than move to structured metadata) in a follow-on pass, since it adds cardinality with zero additional information.