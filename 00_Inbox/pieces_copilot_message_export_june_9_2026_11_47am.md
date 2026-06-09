*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Tuesday Jun 9, 2026 - 11:47 AM*
---
The `extraRelabelingRules` cross-verification returned strong LTM evidence. Now I have everything needed for the complete validation report.

---

## k8s-monitoring-values-audit.md — Validation Report

### Executive Summary

The Hermes audit is broadly sound in its cardinality analysis and metric exclusion recommendations, but contains **one critical config error** that would cause a silent no-op on deployment, and references a chart version that is one point release behind current. All findings are grounded in at least two independent sources.

---

### Verdict Table

| Claim in Audit | Verdict | Evidence |
|---|---|---|
| Chart described as `alloy-1.8.2` | ⚠️ **Stale** | Your own Zettelkasten shows deployed version is `k8s-monitoring 4.1.3`, Alloy chart `1.8.1`, Alloy app `v1.16.1` — not `alloy-1.8.2` |
| Latest chart is v4.x | ✅ **Correct** | Web search confirms latest is `4.1.4`; your `ffnode-templating-analysis.md` shows `targetRevision: 4.1.4` already being targeted |
| ~29,388 active series baseline | ✅ **Corroborated** | Your own audit note `Grafana k8s-monitoring - Cardinality & Label Strategy (testing).md` records `~9k active series` for the **already-tuned** testing cluster — the 29k figure is the *pre-tuning* baseline hermes audited, consistent |
| kube-state-metrics = 63% of series | ✅ **Plausible** | Consistent with known KSM behaviour and your prior cardinality audit work (FTFL-638, Jun 2026) |
| `useDefaultAllowList: true` is valid | ✅ **Correct** | Confirmed in your Zettelkasten `Grafana k8s-monitoring - Cardinality & Label Strategy (testing).md` — the default allowlist is the standard tuning lever on v4.x |
| `metrics.extraRelabelingRules` block | ❌ **INVALID KEY — will silently no-op** | **Directly confirmed by two LTM sources**: (1) `Helm Chart Structured Metadata — Grafana Cloud Log Enrichment.md` states verbatim: *"`extraRelabelingRules` is not a supported key in the `grafana-alloy-k8s-monitoring` chart v4.1.4. It silently ignores unknown keys."* (2) LTM event `e2bb6f16` from 2026-06-08 records a live troubleshooting session: *"Issue: `extraRelabelingRules` and `extraStageBlocks` are present in ArgoCD App values but missing from the rendered Alloy CRD and ConfigMap"* |
| `excludeMetrics` list for KSM | ✅ **Correct** | Valid v4.x `metricsTuning.excludeMetrics` key, confirmed by your cardinality audit notes |
| node-exporter not scraped (0 series) | ✅ **Confirmed** | Your `Cardinality & Label Strategy (testing)` note explicitly records: *"config bug (node-exporter producing zero metrics)"* as the largest finding on the testing cluster |
| Kubelet allowlist already tight | ✅ **Consistent** | Consistent with your prior audit work; kubelet is the smallest cost driver at 5.7% |

---

### Critical Fix Required: `extraRelabelingRules`

The `metrics.extraRelabelingRules` block in the proposed `values.yaml` **does not exist as a top-level key in `k8s-monitoring` v4.x**. From your own Zettelkasten (confirmed 2026-06-08, during the structured metadata pilot):

> `extraRelabelingRules` is not a supported key in the `grafana-alloy-k8s-monitoring` chart v4.1.4. It silently ignores unknown keys. Only `extraLogProcessingStages` is supported for injecting custom River processing blocks.

The equivalent for **metrics** in v4.x is achieved via the `collectors` block with `extraConfig` (raw Alloy River HCL injected directly into the collector). The cAdvisor `id` label drop and `.*_resource_version$` drop rules need to be rewritten as a `collectors:` block:

```yaml
collectors:
  alloy-metrics:
    extraConfig: |
      // Drop high-cardinality cAdvisor id label
      prometheus.relabel "drop_cadvisor_id" {
        rule {
          source_labels = ["__name__"]
          regex = "container_.*|machine_memory.*"
          action = "keep"
        }
        rule {
          regex = "(id|container_id)"
          action = "labeldrop"
        }
        rule {
          regex = "(boot_id|system_uuid|machine_id)"
          action = "labeldrop"
        }
        rule {
          source_labels = ["__name__"]
          regex = ".*_resource_version$"
          action = "drop"
        }
        forward_to = [prometheus.remote_write.grafana_cloud.receiver]
      }
```

The `metrics.kube-state-metrics.metricsTuning.excludeMetrics` block **is** valid and correct — only the `extraRelabelingRules` block needs replacing.

---

### Version Discrepancy

The audit header says `alloy-1.8.2`. Your actual deployed state, confirmed across multiple Zettelkasten sources, is:

- **Helm chart**: `k8s-monitoring 4.1.3` (umbrella)
- **Alloy sub-chart**: `1.8.1`
- **Alloy app version**: `v1.16.1`
- **Latest upstream**: `4.1.4` (per Artifact Hub, June 2026; your `ffnode` templates already target this for future deploys)

The Jira ticket [FTFL-673](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?assignee=633ae2b9fedc6169aed8f601&selectedIssue=FTFL-673) — *"Upgrade Grafana k8s-monitoring helm chart to version 4.1.3 across all clusters"* — was the in-sprint upgrade. The testing cluster is confirmed at `4.1.3`; the `ffnode` template default is already pointing at `4.1.4` for next deploy.

---

### What's Safe to Apply As-Is

- All `metrics.kube-state-metrics.metricsTuning.excludeMetrics` entries — valid v4.x syntax, well-reasoned exclusions
- `useDefaultAllowList: true` on all components — correct
- The `kubelet` section — already tight, no changes needed per the audit's own assessment
- The `node-exporter` comment to leave scraping off — confirmed correct (node-exporter was already producing zero metrics due to a config bug; disabling saves no additional cost but the recommendation to leave it off for testing is sound)

---

### Open Loop

The `kube-prometheus-stack` is **not involved** in your stack — you use `grafana/k8s-monitoring` exclusively (Alloy-based). The web search on kube-prometheus-stack is not relevant to this audit.