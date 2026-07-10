---
created: 2026-07-10T22:20:22+00:00
modified: 2026-07-10T22:20:33+00:00
permalink: llmeon/00-inbox/aks-fleet-manager-nhs-assessment
title: AKS Fleet Manager NHS Assessment
type: note
---

## Azure Kubernetes Fleet Manager: Feasibility for NHS Private AKS Clusters

### Executive Summary

Azure Kubernetes Fleet Manager offers genuine value for managing multiple AKS clusters at scale, particularly for orchestrating Kubernetes and node image upgrades across clusters without manual effort. However, for NHS-grade private, network-isolated AKS clusters spread across separate trust Azure accounts, Fleet Manager introduces significant architectural constraints that must be understood before adoption. The short answer: Fleet Manager can help with upgrade orchestration and basic config propagation, but the private networking requirements, the same-Entra-tenant constraint, and the still-maturing Terraform provider create real blockers for a highly secure, siloed NHS deployment. ArgoCD ApplicationSets remain the stronger fit for workload GitOps in this topology.

*

### What Fleet Manager Actually Does

Azure Kubernetes Fleet Manager enables at-scale management of multiple AKS clusters by grouping them under a single control plane. It supports:[^1]

- Orchestrated upgrades: Kubernetes version and node image upgrades across multiple clusters using update runs, stages, and groups—including automatic triggering when new versions are published[^1]
- Resource placement: Intelligent propagation of Kubernetes cluster-scoped and namespace-scoped resources (ConfigMaps, RBAC, NetworkPolicies, etc.) from a central hub cluster to member clusters, using declarative placement policies and label selectors[^2]
- Multi-cluster load balancing (preview): DNS-based L4 load balancing across service endpoints on multiple member clusters via Azure Traffic Manager integration[^2]
- Automated Deployments (preview): Staging Kubernetes workloads from Git repositories to the hub cluster, ready for placement to members[^1]
- Managed Fleet Namespaces (preview): Enforcing resource quotas, network policies, and RBAC at namespace level across the fleet[^2]

Fleet Manager comes in two configurations: with a hub cluster (a managed single-node AKS cluster auto-created in an `FL_` resource group, which cannot be user-modified) and without a hub cluster (a lightweight ARM grouping entity only). Without a hub cluster, you lose workload placement, DNS load balancing, and cross-cluster networking—keeping only upgrade orchestration.[^3]

*

### The Hard Constraints for NHS / NHS Trust Accounts

#### 1. Same Microsoft Entra ID Tenant—Non-Negotiable

This is the most critical constraint for NHS Trust scenarios. Fleet Manager's official FAQ states:

> "Fleet Manager allows appropriately authorized users to add any AKS cluster in any Azure subscription and region as long as the Azure subscription is associated with the same Microsoft Entra ID tenant as the Fleet Manager."[^4]

NHS Trusts typically have separate Azure AD tenants (or at minimum, separate subscriptions with governance barriers enforcing strict isolation). If your clusters live in different Entra tenants, they cannot be joined to the same fleet—full stop. This is currently not on the supported roadmap.[^4]

If your clusters are all in the same Entra tenant (just different subscriptions or resource groups), cross-subscription joining is fully supported.[^5][^6]

#### 2. Private Hub Cluster—Substantial Networking Overhead

Fleet Manager supports a private hub cluster mode where the API server is only accessible via an Azure Virtual Network. However, this requires:[^7]

- Specifying a subnet for the hub cluster's node VMs at creation time[^1]
- The hub cluster cannot be accessed via AKS `command invoke` or private endpoints (both currently unsupported)[^3]
- Access to a private hub requires Azure Bastion (Standard or Premium SKU with native client support) configured on the hub cluster's VNet[^8]
- Private hubs on networks with user-defined routing (UDR) or firewall rules may block outbound connectivity needed for hub cluster updates[^7]
- Once set, the hub type (public/private) cannot be changed[^3]

For member clusters in separate, air-gapped NHS Trust VNets, Fleet Manager still needs network-level reachability from the hub to each member cluster's Kubernetes API server. This typically means VNet peering, Private Link, or Azure ExpressRoute between Trust network boundaries—which may conflict with the "very secure, not linked to each other" requirement.

#### 3. Member Cluster Reachability

Fleet Manager deploys a fleet-member agent on each joined AKS cluster. This agent communicates back to the Fleet Manager hub. The control plane connectivity model is fundamentally different from ArgoCD's agent model—the hub cluster needs to reach (or be reachable by) each member. For clusters with strict egress controls or no cross-cluster VNet routing, this creates a significant hurdle.[^9]

Cross-cluster networking (east-west traffic between member cluster workloads) has even tighter prerequisites: clusters must run Kubernetes v1.32+, have Advanced Container Networking Services (ACNS) with Cilium enabled, and sit on a single flat network or peered VNets. Overlay networking via tunnels is not supported.[^10]

*

### What Fleet Manager Can Realistically Offer Your Setup

Assuming the same-Entra-tenant constraint is satisfied and you can establish private connectivity to a hub cluster, the most valuable capability for your use case is upgrade orchestration without a hub cluster—the lightweight, hub-free fleet. This configuration:

- Groups all member AKS clusters under one Fleet Manager ARM resource
- Orchestrates Kubernetes and node image upgrades with ring-based staged rollouts
- Supports auto-upgrade profiles (Rapid, Stable, NodeImage, TargetKubernetesVersion channels)[^4]
- Honors per-cluster maintenance windows[^4]
- Costs nothing for the Fleet Manager resource itself[^2]

This alone eliminates a major operational pain point: manually managing Kubernetes version upgrades across N clusters without coordinated rollout control.

| Capability | Without Hub Cluster | With Private Hub Cluster |
|---|---|---|
| K8s/node image upgrade orchestration | ✅ Full support | ✅ Full support |
| Auto-upgrade profiles | ✅ Full support | ✅ Full support |
| Workload/config placement (CRP) | ❌ Not available | ✅ Available |
| DNS load balancing | ❌ Not available | ✅ Available (preview) |
| Resource quotas/RBAC propagation | ❌ Not available | ✅ Available (preview) |
| Cross-cluster networking | ❌ Not available | ✅ Available (preview, requires ACNS+Cilium+flat VNet) |
| Networking complexity | Low | High—requires VNet+Bastion |
| NHS isolation risk | Low | Medium-High |

*

### Terraform Provider: A Real Blocker Today

Given that you use Terraform Cloud to deploy clusters, the current state of the `azurerm` provider for Fleet Manager is important to understand. As of mid-2025, the `azurerm_kubernetes_fleet_manager` resource creates hub-less fleets only—there is no first-class supported way to create a Fleet Manager with a hub cluster via `azurerm` directly. The workaround is to use the `azapi` provider:[^11]

```hcl
resource "azapi_resource" "fleet_manager" {
  name      = "fleet-manager"
  type      = "Microsoft.ContainerService/fleets@2025-03-01"
  location  = var.location
  parent_id = azurerm_resource_group.resource_group.id
  body = {
    properties = {
      hubProfile = {
        dnsPrefix = var.dns_prefix
      }
    }
  }
}
```

Additionally, update groups for Fleet Manager must be created with Azure CLI post-deploy—they are not yet Terraform-manageable. A GitHub issue requesting full `hub_profile` support in `azurerm` is open as of 2025. For a hub-less fleet (upgrade orchestration only), the existing `azurerm_kubernetes_fleet_manager` resource works fine today.[^12][^11]

*

### How This Fits With Your ArgoCD + Terraform Cloud Stack

Fleet Manager and ArgoCD serve different purposes and are genuinely complementary—they are not competitors for the same function:

| Concern | Fleet Manager | ArgoCD (ApplicationSets) |
|---|---|---|
| K8s version upgrades | ✅ Native, orchestrated | ❌ Not in scope |
| Node image patching | ✅ Auto-upgrade profiles | ❌ Not in scope |
| App/workload deployment | ❌ Placement only, no CD | ✅ Full GitOps CD |
| Config/RBAC propagation | ✅ CRP (with hub) | ✅ Via ApplicationSets |
| Private cluster support | ✅ With VNet+Bastion | ✅ Native (push or pull) |
| Cross-tenant support | ❌ Same tenant only | ✅ Any cluster with API access |
| Terraform maturity | 🟡 Partial (hub-less only) | ✅ Mature provider |

ArgoCD ApplicationSets with a cluster generator already handle GitOps-driven workload deployment to multiple private clusters—and critically, they work across tenants and across network boundaries using the ArgoCD agent pull model or inbound API server access (via private endpoints).[^13][^9]

A recommended hybrid approach for your scenario:

1. Fleet Manager (hub-less)—for upgrade orchestration and auto-upgrade profiles. Low risk, no hub networking overhead, and directly usable today via Terraform. This handles the painful multi-cluster upgrade coordination.
2. ArgoCD ApplicationSets—continue as your GitOps engine for all workload and configuration deployments. This remains the right tool for cross-trust, cross-tenant app delivery.
3. Terraform Cloud—continues to own cluster lifecycle (creation, networking, node pools) and can provision the hub-less Fleet Manager resource and member cluster joins.

*

### Security and NHS Compliance Considerations

Fleet Manager's hub cluster is explicitly exempted from Azure Policies to avoid policy interference. In an NHS environment where Azure Policy is a key compliance enforcement mechanism (e.g., CIS benchmarks, NHS DSPT requirements), this exemption needs careful governance review. The FL_ resource group containing the hub cluster cannot be modified by users and denies user-initiated mutations, which helps with tamper resistance but means you cannot apply your own security hardening to the hub.[^3]

The private hub cluster option, accessed only via Azure Bastion tunneling, does provide a reasonable security boundary. However, the requirement for Bastion Standard/Premium SKU adds cost and networking complexity, and the limitation that `az aks command invoke` does not work with private fleet hubs means your current operational tooling may need adjustment.[^8][^3]

*

### Verdict and Recommendations

Fleet Manager is worth adopting, with scope limited to upgrade orchestration. Start with a hub-less fleet to get immediate value from orchestrated K8s upgrades across your NHS Trust clusters—this has the lowest security risk, the most mature Terraform support, and requires no network topology changes.

Defer the hub cluster until: (a) your trust clusters confirm same-Entra-tenant membership, (b) you have a VNet peering or Private Link architecture that allows hub-to-member API connectivity, (c) the `azurerm` Terraform provider adds full hub profile support, and (d) you have assessed the Azure Policy exemption implications against NHS DSPT obligations.

Do not replace ArgoCD with Fleet Manager for workload deployments. ArgoCD ApplicationSets with cluster generators already solve the multi-cluster GitOps problem correctly for your topology, including private clusters and cross-subscription deployments.

Key action items:

- Confirm whether all NHS Trust clusters share a single Microsoft Entra ID tenant
- Use `azurerm_kubernetes_fleet_manager` (hub-less) + `az fleet member create` for upgrade orchestration today
- Evaluate `azapi_resource` for hub cluster creation if workload placement is needed in future
- Review Azure Bastion networking requirements against your NHS Trust VNet architecture before committing to a private hub
- Monitor the [Fleet Manager roadmap on GitHub](https://github.com/Azure/AKS) for Terraform provider hub_profile support and cross-tenant cluster plans

---

### References

1. [Choosing an Azure Kubernetes Fleet Manager option | Microsoft Learn](https://learn.microsoft.com/en-us/azure/kubernetes-fleet/concepts-choosing-fleet) - When you use private hub clusters, you're required to specify the subnet in which the Fleet Manager …
2. [Azure Kubernetes Fleet Manager](https://azure.microsoft.com/en-us/products/kubernetes-fleet-manager) - Get started with Azure Kubernetes Fleet Manager to simplify multi‑cluster operations with unified an…
3. [Choosing an Azure Kubernetes Fleet Manager option](https://docs.azure.cn/en-us/kubernetes-fleet/concepts-choosing-fleet) - This article provides an overview of the various Azure Kubernetes Fleet Manager options and why you …
4. [Frequently asked questions - Azure Kubernetes Fleet Manager](https://learn.microsoft.com/en-us/azure/kubernetes-fleet/faq) - Fleet Manager allows authorized users to add any AKS, AKS Automatic, or Arc-enabled Kubernetes clust…
5. [Getting started with Azure Fleet Manager](https://techcommunity.microsoft.com/blog/appsonazureblog/getting-started-with-azure-fleet-manager/4369223) - Why? A solution to manage multiple Azure Kubernetes Service (AKS) clusters at scale. A secure and co…
6. [Azure Kubernetes Fleet Manager Demo with Terraform Code](https://techcommunity.microsoft.com/blog/appsonazureblog/azure-kubernetes-fleet-manager-demo-with-terraform-code/4408163) - Introduction Azure Kubernetes Fleet Manager (Fleet Manager) simplifies the at-scale management of mu…
7. [Fleet Manager hub cluster overview - Azure - Microsoft Learn](https://learn.microsoft.com/en-us/azure/kubernetes-fleet/concepts-lifecycle) - Network configuration: public hub clusters have a public API server, with an associated public IP ad…
8. [Access the Kubernetes API for an Azure Kubernetes Fleet Manager ...](https://learn.microsoft.com/uk-ua/azure/kubernetes-fleet/access-fleet-hub-cluster-kubernetes-api) - Learn how to access the Kubernetes API for an Azure Kubernetes Fleet Manager hub cluster.
9. [Multi-cluster GitOps with the Argo CD Agent Technology Preview](https://www.redhat.com/en/blog/multi-cluster-gitops-argo-cd-agent-openshift-gitops) - Running a single instance of Argo CD on a single cluster used to be common, but now a multi-cluster …
10. [Azure Kubernetes Fleet Manager용 클러스터 간 네트워킹(미리 보기)](https://learn.microsoft.com/ko-kr/azure/kubernetes-fleet/concepts-cross-cluster-networking) - 이 문서에서는 Azure Kubernetes Fleet Manager에 대한 클러스터 간 네트워킹에 대한 개념적 개요를 제공합니다.
11. [Support for `azurerm_kubernetes_fleet_manager` with a hub cluster · Issue #29800 · hashicorp/terraform-provider-azurerm](https://github.com/hashicorp/terraform-provider-azurerm/issues/29800) - Is there an existing issue for this? I have searched the existing issues Community Note Please vote …
12. [GitHub - saswatmohanty01/aks-fleet-manager: AKS Fleet Manager with multiple regions with Azure Front door](https://github.com/saswatmohanty01/aks-fleet-manager) - AKS Fleet Manager with multiple regions with Azure Front door - GitHub - saswatmohanty01/aks-fleet-m…
13. [Multi-Cluster Made Easy: Istio + Argo CD in a Fleet Setup](https://medium.com/@viks11021/multi-cluster-made-easy-istio-argo-cd-in-a-fleet-setup-02fcce4b1862) - Introduction: The Multi-Cluster Challenge
