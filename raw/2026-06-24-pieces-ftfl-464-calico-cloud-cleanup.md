---
created: 2026-06-24T15:30:00+00:00
modified: 2026-07-20T16:32:35+00:00
permalink: llmeon/raw/2026-06-24-pieces-ftfl-464-calico-cloud-cleanup
pieces_ids: [035d4a34-ecc7-4144-bd06-01c77567b8e3, 21881f50-4f82-40d8-a785-92e4cdb3f596, 3316032e-4e57-4b9a-bc1b-665d7c472336, 756b99ec-7f03-45fd-b0af-6048cfdc7a3e, ba5ed068-d05d-4415-bef6-fd65284a4d8c, e7f69745-5fec-4e43-94df-ee644fb8be82, ea58c91a-1bb7-4dd7-8cac-4de4da9c57e8, ef5c465b-0158-4e64-a582-b28ff42a8c9a]
source: pieces
tags: [raw]
title: 2026-06-24-pieces-ftfl-464-calico-cloud-cleanup
---

## FTFL-464—Calico Cloud Cleanup Milestone

Two-phase work on Tigera Calico Cloud removal across FITFILE clusters.

### Phase 1: Investigation—CUH AKS (13:35–13:45 UTC)

Investigated current state of Tigera Calico Cloud deployment on CUH cluster (`aks-ff-uks-gp-01`, Azure). Generated an 8-phase kubectl investigation guide covering:

1. Cluster identity (`kubectl config current-context`, `kubectl cluster-info`)
2. Tigera operator status (`kubectl get tigerastatus`)
3. Cloud namespace inventory—managed Calico Cloud namespaces via `kubectl get ns -l "projectcalico.org/name"`
4. ManagementClusterConnection (`kubectl get managementclusterconnection`)
5. Tigera license & image assurance resources
6. Remaining operator resources (ConfigMap, secrets, service accounts)
7. `tigera-guardian` namespace contents
8. Final cleanup decisions

Generated a Jira ticket comment/report for FTFL-464 based on kubectl output from CUH cluster.

### Phase 2: Execution—eoe-sde-codisc EKS (14:25–15:18 UTC)

Executed cleanup on AWS EKS cluster `eoe-sde-codisc` (ARN `arn:aws:eks:eu-west-2:135808916559:cluster/eoe-sde-codisc`, created Feb 2025, K8s 1.33, accessed via `eoe-hie` AWS profile, SSM via jumpbox).

#### Progress Timeline

- 12 of 17 Cloud namespaces fully deleted
- 5 stuck in Terminating—needed force-finalising
- `ManagementClusterConnection tigera-secure` deleted successfully (SaaS link removed)
- `tigera-guardian` namespace secret cleaned up
- Final state: Clean—all 17 Cloud namespaces gone, only `calico-system` + `tigera-operator` remain, CNI healthy
- Drafted Jira ticket comment documenting the cleanup

#### Key Commands

```
kubectl get ns
kubectl delete managementclusterconnection tigera-secure
kubectl delete secret -n tigera-guardian tigera-managed-cluster-connection
kubectl get tigerastatus
```

#### Safety Assessment

Calico CNI is deployed differently on EKS vs AKS. On EKS (`eoe-sde-codisc`), Calico was installed via the AWS managed Calico operator (not Tigera-operator for non-Cloud), so removing Tigera Cloud components preserves native Calico CNI. Confirmed via web search and LTM context.

#### Related Work

- Previous cleanup on testing/staging clusters completed 2026-06-23
- This session: CUH AKS investigation + eoe-sde-codisc EKS execution
- Ticket FTFL-464 (Remove Calico Cloud Components from AKS/EKS Clusters)
