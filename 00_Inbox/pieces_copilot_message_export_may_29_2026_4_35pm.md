---
created: 2026-05-29T15:35:46+00:00
modified: 2026-05-29T15:36:40+00:00
tags: [1, 2]
title: pieces_copilot_message_export_may_29_2026_4_35pm
---

## Next Steps

Your clarification resolves Root Cause 2 entirely—it's not a CPU problem, it's a structural coverage gap caused by the taint/NodeAffinity on workflow nodes. The Pending alloy-logs pod has been stuck for ~6h because the workflow pool is currently at 0 (no nodes exist). When a workflow fires and a node scales up, alloy-logs still can't schedule there because the DaemonSet doesn't tolerate the workflow node taint. That means logs from any workflow pod on those nodes will always be dropped.

You need two separate PRs/changes to `ffnodes/fitfile/testing/values.yaml`.

---

## Fix 1—Remove `pod: null` from structuredMetadata (Root Cause 1)

This is the quick win. In your values file:

```yaml
# BEFORE (broken — sends pod to structuredMetadata, not queryable as a stream label)
podLogsViaLoki:
  structuredMetadata:
    k8s.pod.name: null
    pod: null              # ← DELETE THIS LINE
    service.instance.id: service.instance.id

# AFTER
podLogsViaLoki:
  structuredMetadata:
    k8s.pod.name: null
    service.instance.id: service.instance.id
```

This unblocks label-based queries like `{cluster="testing", namespace="argo", pod=~"my-workflow.*"}` working correctly once logs actually arrive.

---

## Fix 2—Add Workflow Node Taint Toleration to Alloy-logs (Root Cause 2)

### Step 1: Find the Actual Taint

```bash
kubectl --context fitfile-cloud-testing-aks-cluster get nodes -o json | \
  jq -r '.items[] | .metadata.name + ": " + (.spec.taints // [] | map(.key + "=" + (.value // "") + ":" + .effect) | join(", "))'
```

The workflow nodes will show something like `dedicated=workflows:NoSchedule` or `workloads=argo:NoSchedule`. Note the exact key, value, and effect.

### Step 2: Add the Toleration to values.yaml

In the Grafana k8s-monitoring v4.x chart, tolerations for alloy-logs go here (adjust key/value to match what you found above):

```yaml
grafana:
  alloy-logs:
    tolerations:
      - key: "dedicated"          # ← use actual taint key
        operator: "Equal"
        value: "workflows"        # ← use actual taint value
        effect: "NoSchedule"
```

This allows alloy-logs to schedule on workflow nodes when they scale up, so it is already running there before workflow pods start (DaemonSet pre-placement). When the pool scales back to 0 and the node is removed, the alloy-logs pod disappears with it—no wasted resource when idle.

---

## Why This Fixes the Architecture

| Scenario | Before fix | After fix |
|---|---|---|
| Pool at 0, no workflow nodes | alloy-logs Pending (harmless) | alloy-logs Pending (harmless, same) |
| Workflow fires, node scales up | alloy-logs can't schedule → workflow logs lost | alloy-logs schedules → collects logs from workflow pods |
| Workflow finishes, pool scales to 0 |—| alloy-logs pod terminates with the node |

The toleration does not force alloy-logs onto workflow nodes—it just grants permission. The DaemonSet controller automatically places a pod there when the node joins the cluster.

---

## Verification After Applying Both Fixes

```bash
# 1. Trigger a test workflow in the argo namespace to bring up a workflow node
# (or run any workflow that causes the pool to scale up)

# 2. Confirm alloy-logs landed on the workflow node
kubectl --context fitfile-cloud-testing-aks-cluster get pods \
  -n monitoring -l app.kubernetes.io/name=alloy-logs -o wide

# 3. Wait ~2 min, then query Loki
gcx logs query --context fitfiletest \
  '{cluster="testing", namespace="argo"}' \
  --since 5m --limit 20

# 4. Verify pod IS a stream label (not buried in structured metadata)
gcx logs query --context fitfiletest \
  '{cluster="testing", namespace="argo"}' \
  --since 5m --limit 3 -o json | \
  python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
for r in data.get('data',{}).get('result',[])[:3]:
    s = r.get('stream', {})
    print('pod in stream labels:', 'pod' in s)
    print('Labels:', list(s.keys()))
"
```

You expect `pod in stream labels: True` and `namespace=argo` appearing in the stream labels after both fixes are applied and synced.
