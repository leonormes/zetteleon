---
date: 2026-05-29
tags: [fitfile, grafana, loki, argo-workflows, investigation, FTFL-638, solution]
source: Mechanical Lead investigation + Claude Code review
---

# FTFL-638 Follow-up: Argo Workflows Logs Missing from Grafana Loki

## Status: Fixes Identified, Pending Implementation

## Summary

After FTFL-638 merged (`feature/FTFL-638-add-labels-for-logs`, commit `015851c6`), general cluster logs (cluster=testing) are visible in Grafana, but Ollie Rushton reports **Argo Workflow pods in the `argo` namespace** still have no visible logs. Three contributing factors identified.

## Stack

| Component | Value |
|-----------|-------|
| Cluster | `fitfile-cloud-testing-aks-cluster` (AKS, UK South) |
| kubectl context | `fitfile-cloud-testing-aks-cluster` |
| gcx context | `fitfiletest` |
| ArgoCD app | `grafana-k8s-monitoring` (child of `testing`) |
| Helm chart | `grafana/k8s-monitoring` v4.1.3 |
| Monitoring ns | `monitoring` |
| Workflows ns | `argo` |
| Grafana Cloud | `fitfiletest.grafana.net` |

## Root Cause #1 — alloy-logs DaemonSet Can't Schedule on Saturated Node (BLOCKING)

**This is the primary blocker — no argo logs reach Loki at all.**

Node topology:

| Node | alias | CPU requests | alloy-logs | argo pods |
|------|-------|-------------|------------|-----------|
| `aks-system-26060640-vmss0000tq` | system | ~50% | ✅ Running | None |
| `aks-workflows-32842669-vmss0000ek` | workflows | 6% | ✅ Running (fix applied) | None |
| `aks-system-26060640-vmss0000tp` | system2 | **99%** (3852m/3860m) | ❌ Pending | **Both argo pods** |

Both argo control-plane pods (`argo-workflows-server`, `argo-workflows-workflow-controller`) are on `vmss0000tp`. The alloy-logs DaemonSet can't schedule there because CPU requests are at 99% but only 8m is free (alloy-logs requests 50m).

The node's CPU hogs are entirely ArgoCD deployments (controller 1000m, repo-server 500m, server 500m, etc.). Actual CPU usage is only ~7-35m per pod — it's a request/limit accounting mismatch, not real contention.

**Fix:** Reduce `collectors.alloy-logs.alloy.resources.requests.cpu` from `50m` to `10m` **in the ArgoCD app's values** (NOT by patching the Alloy CR — ArgoCD will revert CR patches). alloy-logs is I/O-bound; real usage is 2-8m. 10m request / 200m limit is safe for testing.

```yaml
# In ArgoCD Application spec.source.helm.values:
collectors:
  alloy-logs:
    alloy:
      resources:
        requests:
          cpu: 10m      # ← from 50m
          memory: 64Mi   # ← from 128Mi (also safe to reduce)
        limits:
          cpu: 200m
          memory: 256Mi
```

Then force ArgoCD sync: `argocd app sync grafana-k8s-monitoring --force`

## Root Cause #2 — Tolerations Missing for Workflow/Spot Nodes (PARTIALLY FIXED)

The `vmss0000ek` (workflows) node has two `NoSchedule` taints:
- `dedicated=workflows`
- `kubernetes.azure.com/scalesetpriority=spot`

The DaemonSet had zero tolerations, so it couldn't schedule there. Tolerations were added to the ArgoCD values and alloy-logs pod `j2vst` is now running on that node.

**Status:** ✅ Fixed in ArgoCD values, alloy-logs tolerates both taints now.
**Caveat:** This only helps for workflow step (argoexec) pods that land on that node. The argo control-plane pods remain on the saturated node (Root Cause #1).

## Root Cause #3 — `pod` in `structuredMetadata` (Likely Chart Bug)

The ArgoCD values have `pod` removed from `structuredMetadata`:
```yaml
podLogsViaLoki:
  structuredMetadata:
    k8s.pod.name: null
    # pod is NOT listed here — should be excluded
    service.instance.id: service.instance.id
```

But the live ConfigMap still renders:
```
stage.structured_metadata {
    values = {
        "pod" = "pod",          # ← STILL PRESENT (chart bug?)
        "service_instance_id" = "service_instance_id",
    }
}
```

**Assessment from Claude Code:** This is likely a chart v4.1.3 template hardcode — the template unconditionally emits `pod = pod` in the `stage.structured_metadata` block regardless of values. Setting `pod: null` in values only removes the user-supplied key, not the hardcoded template output.

**Impact on querying:** LOW priority. The `pod` label is also added by the discovery rule `__meta_kubernetes_pod_name → pod` and `labelsToKeep: [pod, ...]`. The `structured_metadata` stage tells Loki to ALSO store it as structured metadata — this is additive, not a removal from stream labels. The stream label `pod` should still be present and queryable.

**Fix (if needed):** Use `collectors.alloy-logs.alloy.extraConfig` to override the stage block, or upgrade the chart.

**Verification needed:** After fixing Root Cause #1, check if argo logs have `pod` as a stream label. If they do, this issue is cosmetic.

## Investigation Phases

### Phase 1 — Loki Ground Truth
- `{cluster="testing", namespace="argo"}` → **"No data"** — confirms no logs arriving
- Text search `|= "argo-workflows"` returns only **ingress-nginx access logs**, NOT actual Workflow pod logs

### Phase 2 — alloy-logs Health
- 1 of 3 DaemonSet pods stuck `Pending` (Insufficient cpu)
- No `excludeNamespaces` for `argo` in the alloy config
- Tolerations missing for workflow/spot taints (fixed)

### Phase 3 — Chart Values
- `structuredMetadata.pod: null` in values but still rendered in ConfigMap (chart bug)
- `labelsToKeep: [pod, container, namespace]` — correct
- `extraDiscoveryRules` only has a `job` rewrite, no namespace filtering

### Phase 4 — RBAC & Pod Labels
- `auth can-i get pods` → **yes**
- `auth can-i get pods/log` → **yes**
- Workflow pods exist with correct labels

### Phase 5 — Additional Concerns (from Claude Code)
- Check for `action: keep` rules on `__meta_kubernetes_namespace` that might silently drop `argo`
- Check `logs.pod_logs.namespaces` — if set as an allowlist (not just excludeNamespaces), `argo` must be included
- Transient argoexec pods on the workflows node WILL be collected once alloy-logs runs there (✅ now the case)

## Verification Steps

```bash
# 1. Verify alloy-logs DaemonSet covers all 3 nodes after CPU fix
kubectl --context fitfile-cloud-testing-aks-cluster get pods \
  -n monitoring -l app.kubernetes.io/name=alloy-logs -o wide

# 2. Verify no namespace filtering
kubectl --context fitfile-cloud-testing-aks-cluster get configmap \
  grafana-k8s-monitoring-alloy-logs -n monitoring \
  -o yaml | grep -A 5 "keep\|drop" | grep namespace

# 3. Trigger a test workflow, then check Loki
gcx logs query --context fitfiletest \
  '{cluster="testing", namespace="argo"}' \
  --since 5m --limit 10

# 4. Verify pod label is queryable
gcx logs query --context fitfiletest \
  '{cluster="testing", namespace="argo", pod=~"argo.*"}' \
  --since 5m --limit 5
```

## Related

- [[FTFL-638 Original Fix]] — labelsToKeep + extraDiscoveryRules migration
- [[grafana-k8s-monitoring Helm Chart v4.x]] — monitoring stack configuration
- [[fitfiletest Grafana Cloud Stack]]
- [[AKS Node Capacity Planning]]
