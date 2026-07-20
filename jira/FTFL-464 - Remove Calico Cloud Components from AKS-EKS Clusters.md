---
assignee: Leon Ormes
created: 2026-03-10T00:00:00+00:00
epic: Infrastructure Cleanup
jira_key: FTFL-464
jira_url: https://fitfile.atlassian.net/browse/FTFL-464
labels: [calico, kubernetes, platform-engineering, tech-debt]
modified: 2026-07-20T16:33:32+00:00
permalink: llmeon/jira/ftfl-464-remove-calico-cloud-components-from-aks-eks-clusters
priority: Medium
project: FTFL (FITFILE 2026)
reporter: Ollie Rushton
status: In Progress
tags: [jira]
title: FTFL-464 - Remove Calico Cloud Components from AKS-EKS Clusters
type: Task
updated: 2026-06-23
---

## FTFL-464: Remove Calico Cloud Components from AKS/EKS Clusters

### Summary

Remove orphaned Tigera/Calico Cloud SaaS components from managed Kubernetes clusters while preserving the open-source Calico CNI networking layer. At least one Calico Cloud pod is crash-looping due to the Tigera Cloud management plane no longer being available.

### Background

FITFILE previously used a Calico Cloud (Tigera SaaS) account to manage Calico across our AKS and EKS clusters. We have since discontinued the Cloud subscription but continue to use the open-source Calico CNI for pod networking and network policy. The Tigera operator and associated Cloud-only pods remain deployed on the clusters, with at least one pod failing because it cannot reach the decommissioned management plane.

### Components to KEEP (Open-Source Calico CNI)

| Component | Namespace | Purpose |
| --- | --- | --- |
| `calico-node` DaemonSet | `calico-system` | CNI dataplane on every node |
| `calico-typha` Deployment | `calico-system` | Scales K8s API watch for calico-node |
| `calico-kube-controllers` | `calico-system` | IPAM garbage collection, policy sync |
| `tigera-operator` | `tigera-operator` | Manages the Installation CR |
| `Installation` CR | cluster-scoped | Operator config for Calico networking |

### Components to REMOVE (Calico Cloud SaaS Only)

| Component | Purpose |
| --- | --- |
| `guardian` | Management plane connector (likely the failing pod) |
| `compliance` (snapshotter, controller, reporter) | Calico Cloud compliance reporting |
| `intrusion-detection` controller | Calico Cloud IDS |
| `log-collector` | Flow log shipping to Calico Cloud SaaS |
| `cloud-core` | RBAC/roles for the Calico Cloud UI |
| `managementclusterconnection` CR | Cluster-to-Cloud link |
| Calico Cloud secrets (`tigera-managed-cluster-connection`, `tigera-voltron-linseed-certs-public`) | Auth credentials for SaaS |
| Calico Cloud-installed Prometheus/Alertmanager (if present) | Cloud monitoring stack |

### Implementation Steps

#### 1. Audit Each Cluster

```bash
# Identify which Calico Cloud components are still running
kubectl get pods -A | grep -E 'guardian|compliance|intrusion|log-collector|cloud-core'

# Check for tiered network policies (script will fail if policies exist outside default/allow-tigera tiers)
kubectl get networkpolicies.p -A
kubectl get globalnetworkpolicies.p -A

# Check if AKS addon-manager owns the Calico resources
kubectl get deployment tigera-operator -n tigera-operator -o yaml | grep 'addonmanager.kubernetes.io/mode:'
kubectl get daemonset calico-node -n kube-system -o yaml 2>/dev/null | grep 'addonmanager.kubernetes.io/mode:'
```

#### 2a. If NOT Managed by AKS AddonManager—Use Official Downgrade Script

```bash
curl -O https://installer.calicocloud.io/manifests/v3.22.1-1/downgrade.sh
chmod +x downgrade.sh
./downgrade.sh --help
# Run with appropriate flags, e.g.:
./downgrade.sh --remove-prometheus
```

The script migrates all applicable components to open-source Calico and removes Cloud-only resources.

#### 2b. If Managed by AKS AddonManager—Manual Disconnect Only

The downgrade script does not work when AKS addon-manager owns the Calico resources. Instead, remove only the three Cloud connection resources:

```bash
kubectl delete managementclusterconnection tigera-secure
kubectl delete secret -n tigera-operator tigera-managed-cluster-connection
kubectl delete secret -n tigera-operator tigera-voltron-linseed-certs-public
```

This disconnects from Calico Cloud while leaving the AKS-managed CNI untouched.

#### 3. Verify

```bash
# Confirm core CNI components are healthy
kubectl get tigerastatus

# Confirm Cloud-only components are gone
kubectl get pods -A | grep -E 'guardian|compliance|intrusion|log-collector|cloud-core'

# Confirm pod networking still works
kubectl run nettest --image=busybox --restart=Never -- sleep 3600
kubectl exec nettest -- ping -c 3 8.8.8.8
kubectl delete pod nettest
```

### Risks & Rollback

- Risk: Removing components on an AddonManager-managed cluster via the downgrade script can break the CNI entirely. The audit step (checking for the `addonmanager.kubernetes.io/mode` annotation) is critical.
- Risk: If tiered network policies exist outside `default`/`allow-tigera`, the downgrade script will exit. Policies must be moved or the `--remove-all-calico-policy` flag used (destructive).
- Rollback: If pod networking breaks post-migration, the Calico operator can be redeployed from the open-source manifests and the `Installation` CR reapplied. Node restarts may be required to reinitialise the CNI.

### Acceptance Criteria

- [ ] All Calico Cloud-only pods removed from every in-scope cluster
- [ ] No crash-looping pods related to Tigera/Calico Cloud
- [ ] `calico-node`, `calico-typha`, and `calico-kube-controllers` healthy on all clusters
- [ ] `kubectl get tigerastatus` shows `calico` AVAILABLE=True with no degraded Cloud components
- [ ] Pod-to-pod networking validated post-cleanup
- [ ] Findings and per-cluster path (script vs manual) documented in wiki

### References

- [Tigera: Uninstall Calico Cloud from a cluster](https://docs.tigera.io/calico-cloud/operations/disconnect)
- [Tigera: Remove cluster (Free Tier)](https://docs.tigera.io/calico-cloud/free/disconnect-cluster-free)
- [Tigera: Operator troubleshooting checklist](https://docs.tigera.io/calico-cloud/get-started/operator-checklist)
