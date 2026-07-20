---
created: 2026-05-29T19:54:32+00:00
modified: 2026-07-20T16:32:58+00:00
permalink: llmeon/raw/2026-05-29-pieces-ftfl638-workflow-taints
pieces_ids: [4b065739-05db-45aa-a1f3-596ff3ef1c5e, 6c429e3c-2cb5-49dc-900a-79d52e9c56f7, 7c6fcf68-3c0e-4f47-ac18-c8d348f377e4, 9597cde8-0156-47a3-80d4-d634e7ea85bc, a839433b-9770-4a89-858f-1a49b8abd5ff, c001ed38-a688-4707-9c0f-0df644e3d719, cf74bae5-299f-4da9-86f3-c94740c77269, d8922edc-675e-44aa-a03b-b719fcf7780a, f52ff803-0036-42da-aa19-7b592e013e59]
source: pieces-ltm
tags: [1, 2, pieces, raw]
title: 2026-05-29-pieces-ftfl638-workflow-taints
---

## Asset (Pieces: d8922edc-675e-44aa-a03b-b719fcf7780a)

The workflow node has two taints—you need to tolerate both or alloy-logs will still be blocked by the second one.

```yaml
# in ffnodes/fitfile/testing/values.yaml
grafana:
  alloy-logs:
    tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "workflows"
        effect: "NoSchedule"
      - key: "kubernetes.azure.com/scalesetpriority"
        operator: "Equal"
        value: "spot"
        effect: "NoSchedule"
```

The second taint (`kubernetes.azure.com/scalesetpriority=spot:NoSchedule`) is Azure's standard taint on all Spot VM node pools. It's added automatically by AKS—any DaemonSet that needs to run on Spot nodes must explicitly tolerate it, otherwise Kubernetes blocks scheduling.

Once this plus the `pod: null` structuredMetadata removal is in and ArgoCD syncs, trigger a workflow and you should see alloy-logs schedule onto `aks-workflows-*` nodes as they come up. Verify with:

```bash
kubectl --context fitfile-cloud-testing-aks-cluster get pods \
  -n monitoring -l app.kubernetes.io/name=alloy-logs -o wide
```

You expect a third `alloy-logs` pod appearing with `NODE` set to `aks-workflows-32842669-vmss*` when the pool is non-zero.

## Asset (Pieces: cf74bae5-299f-4da9-86f3-c94740c77269)

The user ran the kubectl command and got the taint information. The workflow node has two taints:

1. `dedicated=workflows:NoSchedule`
2. `kubernetes.azure.com/scalesetpriority=spot:NoSchedule`

They need to tolerate BOTH taints for alloy-logs to schedule on the workflow nodes. Let me provide the exact values.yaml configuration needed.

## Asset (Pieces: 7c6fcf68-3c0e-4f47-ac18-c8d348f377e4)

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

## Asset (Pieces: a839433b-9770-4a89-858f-1a49b8abd5ff)

The user is asking about the next step given Hermes's report. The report identifies two root causes:

1. `pod: null` in `structuredMetadata` suppresses `pod` as a stream label (structural/config fix needed)
2. alloy-logs DaemonSet has 1 of 2 pods stuck `Pending` due to Insufficient CPU + NodeAffinity

The user adds important context:

- The workflow VM pool scales to 0 when not in use (to save money)
- K8s is set up to only use workflow nodes for workflow pods (NodeAffinity/NodeSelector)
- Root Cause 2 is almost certainly caused by this setup: when workflow nodes scale up, the alloy-logs DaemonSet tries to schedule pods there but fails because the nodes have taints/NodeAffinity that only tolerate workflow pods, leaving the alloy-logs pod stuck in Pending.

This creates a catch-22 where workflow pods run on workflow nodes but alloy-logs can't run there to collect their logs. The fix requires either adding a toleration to alloy-logs so it can run on workflow nodes, or configuring it to skip those nodes entirely if they're tainted. Looking at the NodeAffinity error more carefully—the workflow nodes likely have a taint that alloy-logs doesn't tolerate, or alloy-logs has a NodeAffinity constraint that excludes those nodes. Either way, I need to configure the tolerations in the Grafana k8s-monitoring Helm chart's `podLogs` section to let alloy-logs run on workflow nodes when they scale up. But I should also keep in mind that Root Cause 1 with `structuredMetadata` still needs fixing regardless. So there are 2 system nodes running, with the alloy-logs DaemonSet having one pod running on a system node and another stuck pending. The pending pod can't schedule because one node lacks CPU and two nodes have NodeAffinity constraints preventing it—these are likely the workflow nodes that are labeled as such even when scaled to zero, or the pending pod itself has an affinity rule restricting it to system nodes only, which would explain why it can't land on the third node. The DaemonSet is trying to schedule a pod on each node, and the pending pod's error message reflects the scheduler evaluating all available nodes—one lacks sufficient CPU and two don't match the NodeAffinity requirements. So I have one pod running successfully on a system node, and another pod stuck pending because its designated node can't accommodate it due to resource constraints.

The real issue is that the alloy-logs DaemonSet lacks tolerations for the workflow node taint, so even when workflow nodes scale up, the DaemonSet can't place pods there to collect logs from workflow containers. Adding the proper tolerations would let alloy-logs run across all nodes including the workflow pool. Though the user mentioned the cluster is intentionally restricted to workflow pods only on those nodes, which creates a tension with wanting comprehensive log collection. So the immediate action items are to fix both root causes: remove the `pod: null` from structuredMetadata in the values, and add a toleration to alloy-logs for whatever taint is on the workflow nodes. The user can check what that taint actually is by describing the workflow nodes, then we'll know exactly what toleration configuration to add. Writing shell commands…

Then I need to add tolerations to the alloy-logs configuration in the values.yaml file so it can schedule on those tainted workflow nodes, adjusting the syntax based on the chart version being used. Since I already have context from the previous investigation, I can construct the answer about what the next step should be.

The core issue is that alloy-logs can't run on workflow nodes due to the taint, and the Pending pod has been stuck because the workflow pool is scaled to zero. Once the pool scales up for an active workflow, alloy-logs still won't be able to schedule there without the proper tolerations in place.

## Asset (Pieces: 9597cde8-0156-47a3-80d4-d634e7ea85bc)

here is the report from hermes. The workflow vm pool scales to 0 when not in use to save money. Also, k8s is setup to only use the workflow nodes for workflow pods. What is the next step

## FTFL-638 Follow-up: Argo Workflows Logs Missing from Grafana Loki

### Summary

After FTFL-638 merged (`feature/FTFL-638-add-labels-for-logs`, commit `015851c6`), general cluster logs (cluster=testing) are visible in Grafana, but Ollie Rushton reports Argo Workflow pods in the `argo` namespace still have no visible logs. Root cause investigation revealed two independent issues.

### Stack

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

### Root Cause 1—`structuredMetadata` Suppresses `pod` Stream Label

The ArgoCD app's inline values contain:

```yaml
podLogsViaLoki:
  structuredMetadata:
    k8s.pod.name: null     # explicitly nullified
    pod: null              # ← THIS: removes pod from stream labels
    service.instance.id: service.instance.id
```

The `pod: null` entry moves the `pod` label into Loki structured metadata instead of keeping it as a queryable stream label. In Grafana Cloud, structured metadata fields are not queryable via label filters (`{pod="…"}` returns nothing).

While `labelsToKeep: [pod, container, namespace]` correctly lists `pod`, the `structuredMetadata` block with `pod: null` takes precedence and removes it from stream labels.

Fix: Remove `pod: null` from the `structuredMetadata` block in the ArgoCD app values (or source values file).

### Root Cause 2—alloy-logs DaemonSet Coverage Gap

```bash
$ kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-logs
NAME                                      READY   STATUS    AGE
grafana-k8s-monitoring-alloy-logs-gbvjk   2/2     Running   10h
grafana-k8s-monitoring-alloy-logs-l6vxv   0/2     Pending   10h
```

The DaemonSet should run on all 3 nodes, but 1 of 2 pods is stuck `Pending` for ~6h due to:

```
0/3 nodes are available: 1 Insufficient cpu,
                           2 node(s) didn't satisfy plugin(s) [NodeAffinity]
```

Any Argo Workflow pods scheduled on the uncovered node have zero log collection coverage.

Fix: Either scale up a node, free CPU on the affected node, or reduce DaemonSet resource requests.

### Investigation Phases

#### Phase 1—Loki Ground Truth

- `{cluster="testing", namespace="argo"}` → "No data"—confirms no logs arriving
- `argo` namespace IS in the list of indexed namespaces (from other sources)
- Text search `|= "argo-workflows"` returns only ingress-nginx access logs (job label contains the service name), NOT actual Workflow pod logs

#### Phase 2—alloy-logs Health

- 1 of 2 DaemonSet pods stuck `Pending` (Insufficient cpu + NodeAffinity)
- No errors in alloy logs related to `argo` namespace
- No `excludeNamespaces` for `argo` in the alloy config
- No RBAC issues in the drop rules

#### Phase 3—Chart Values (Smoking Gun)

- `structuredMetadata.pod: null`—confirmed
- `labelsToKeep: [pod, container, namespace]`—correct but overridden
- `extraDiscoveryRules` only has a `job` rewrite, no namespace filtering

#### Phase 4—RBAC & Pod Labels

- `auth can-i get pods` → yes
- `auth can-i get pods/log` → yes
- Workflow pods exist with correct labels (`app.kubernetes.io/name=argo-workflows-*`)

#### Phase 5—Label Verification

- Working namespace (`monitoring`) logs show `pod` as a proper stream label ✅
- No argo namespace logs to verify against (none exist)

### Verification Steps

After applying both fixes:

```bash
# 1. Verify alloy-logs DaemonSet covers all nodes
kubectl --context fitfile-cloud-testing-aks-cluster get pods \
  -n monitoring -l app.kubernetes.io/name=alloy-logs

# 2. Trigger a test workflow, then check Loki
gcx logs query --context fitfiletest \
  '{cluster="testing", namespace="argo"}' \
  --since 5m --limit 10

# 3. Verify pod is a queryable stream label
gcx logs query --context fitfiletest \
  '{cluster="testing", namespace="argo"}' \
  --since 5m --limit 3 -o json | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
for e in data.get('data',{}).get('result',[])[:3]:
    print('Stream:', e.get('stream',{}))
    assert 'pod' in e.get('stream',{}), 'pod missing from stream labels!'
"
```

### Related

- [[FTFL-638 Original Fix]]—labelsToKeep + extraDiscoveryRules migration
- [[grafana-k8s-monitoring Helm Chart]]—monitoring stack configuration
- Observability: [[fitfiletest Grafana Cloud Stack]]

### Asset (Pieces: 6c429e3c-2cb5-49dc-900a-79d52e9c56f7)

The user wants me to:

1. Search their memory for yesterday's Grafana upgrade work in the testing cluster
2. Use that context to create an LLM prompt that can be used with a Jira MCP to create a ticket for the staging cluster upgrade

Let me first get the current time to pin yesterday's date, then search memory for the Grafana work.

Yesterday would be 2026-05-28. Let me search for this work.

### Asset (Pieces: f52ff803-0036-42da-aa19-7b592e013e59)

kubectl --context fitfile-cloud-testing-aks-cluster get nodes -o json | \
  jq -r '.items[] |.metadata.name + ": " + (.spec.taints // [] | map(.key + "=" + (.value // "") + ":" +.effect) | join(", "))'

aks-system-26060640-vmss0000tp:

aks-system-26060640-vmss0000tq:

aks-workflows-32842669-vmss0000ek: dedicated=workflows:NoSchedule, kubernetes.azure.com/scalesetpriority=spot:NoSchedule

### Asset (Pieces: 4b065739-05db-45aa-a1f3-596ff3ef1c5e)

The user is asking whether adding tolerations to the alloy-logs DaemonSet will cause pods to still deploy to the non-tainted system nodes (aks-system-*). This is a straightforward Kubernetes question about how tolerations work with DaemonSets.

The answer is yes—tolerations are permissive, not restrictive. A toleration says "this pod CAN be scheduled on nodes with this taint" but it doesn't say "this pod MUST ONLY be scheduled on nodes with this taint." So the alloy-logs pods will continue to run on the system nodes (which have no taints) AND will now also be able to run on the workflow nodes (which have the two taints).

I don't need to make any tool calls here—this is purely a Kubernetes concept question.

### Asset (Pieces: c001ed38-a688-4707-9c0f-0df644e3d719)

if I add those tolerations will the pods still deploy to the other nodes that don't have them taints
