*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday May 20, 2026 - 6:41 AM*
---
Pagination status:
- `ask_memory`: cursor expired — terminal, no more data available from that chain.
- `search_memory`: returned 50 items with `recommendation: fetchMore` — but all candidates are identical to what was already retrieved in the previous pagination pass (the same event IDs, same scores, cycling back through the same window). The `nextCursor` is the same value from the previous page, confirming the backend is looping. No new material surfaced.

The evidence corpus is exhausted. The answer previously delivered is complete and no contradicting or additive evidence was found in these final pages.

---

## Summary: What the error means and how to fix it

The screenshot shows `ExtensionOperationFailed` with this exact error chain:

> `Helm installation failed: Timed out waiting for the resource to come to a ready/completed state. Last resource not ready was dataprotection-microsoft/dataprotection-microsoft-geneva-service … InnerError [release azbkuextension failed, and has been uninstalled due to atomic being set: context deadline exceeded]`

**What is happening**: The extension's Helm chart deployed and started installing pods into the `dataprotection-microsoft` namespace, but the `dataprotection-microsoft-geneva-service` deployment never reached Ready state before the CLI timeout. Because Helm was invoked with `--atomic`, it automatically rolled back and deleted everything on timeout.

**This is not a syntax or subscription error** — the command is now correct. It's a cluster-side readiness failure.

### Immediate debug steps

Run these now to see why the pod didn't come up:

```bash
# 1. See what state the pods were left in (may be nothing if rollback cleaned up)
kubectl get pods -n dataprotection-microsoft

# 2. Check events in the namespace
kubectl get events -n dataprotection-microsoft --sort-by=.metadata.creationTimestamp

# 3. Check node pressure
kubectl describe nodes | grep -A5 "Conditions:"
kubectl top nodes

# 4. Check for image pull problems or pending pods across all namespaces
kubectl get pods -A | grep -v Running | grep -v Completed
```

### Most likely causes on `aks-ff-uks-gp-01` specifically

Your `#prod-alerts` Grafana channel shows that `dataprotection-microsoft-geneva-service` has a **history of `KubeDeploymentReplicasMismatch` alerts on the `cuh-pr...` cluster** (fired and resolved on 21 April 2026). This means the pod has struggled to stay at the expected replica count before on CUH infrastructure — pointing to **node resource pressure or scheduling constraints** rather than a transient network issue.

Specifically check:
- Are the CUH cluster nodes running with **Spot pricing** (from the sprint meeting yesterday, Oliver was discussing switching workflows node pool from Spot to Standard — Spot nodes can be evicted mid-deploy)
- Do you have enough allocatable CPU/memory? The extension pods need headroom
- Check if `dataprotection-microsoft-geneva-service` is hitting any pod disruption budgets or node selectors

### Retry once resources are confirmed healthy

```bash
# After checking nodes are healthy and have capacity, retry:
az k8s-extension create \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azbkuextension \
  --extension-type Microsoft.DataProtection.Kubernetes \
  --scope cluster \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --release-train stable \
  --configuration-settings \
    blobContainer=aksbackups \
    storageAccount=aksffuksgp01cuhbackup \
    storageAccountResourceGroup=aks-ff-uks-gp-01-backup-rg \
    storageAccountSubscriptionId=709f3d57-b6d7-48c6-8252-6b1c1174a541
```

The Spot → Standard node pool switch Oliver was discussing is the most likely fix if Spot eviction is the root cause.