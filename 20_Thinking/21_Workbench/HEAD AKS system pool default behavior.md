---
captured: "2026-03-07T16:51:58+00:00 2026-03-07T16:51:58+00:00"
created: 2026-03-07T16:51:59+00:00
modified: 2026-03-14T11:10:47+00:00
source: "https://claude.ai/chat/49eb934e-8baf-4362-9b04-37e715bb0950"
status: "processing"
tags: ["input"]
title: HEAD AKS system pool default behavior
type: "head"
---

## Raw Output / Content

I deploy kuberenetes to azure aks via terraform. In the terraform I define node pools for the cluster system pool. Do I need to do that? Does aks deploy a system pool by default?

---

## AKS System Node Pool—Do You Need to Define It?

### The Short Answer

Yes, you must define it—but not because AKS won't create one. It's because Terraform requires it as part of the resource definition.

---

### What AKS Does By Default (Without Terraform)

If you create an AKS cluster via the Azure Portal or CLI, Azure automatically provisions a system node pool for you. You don't think about it.

### What Happens in Terraform

The `azurerm_kubernetes_cluster` resource requires a `default_node_pool` block. This _is_ the system node pool—Terraform just makes it explicit.

This block is mandatory—Terraform will refuse to plan without it. It's not optional configuration layered on top of a default; it _is_ the declaration of the default.

---

### Why Does AKS Have a "System" Pool Concept At All?

AKS node pools have a `mode` property—either `System` or `User`:

- System pools are where AKS runs its own critical components: `coredns`, `metrics-server`, `konnectivity`, etc. They have a taint (`CriticalAddonsOnly=true:NoSchedule`) to prevent your workloads landing on them.
- User pools are where your application workloads go.

The `default_node_pool` in Terraform is always created as a `System` mode pool. You can add additional `azurerm_kubernetes_cluster_node_pool` resources for `User` mode pools.

---

### The Practical Implication for You

If you're defining additional node pools via `azurerm_kubernetes_cluster_node_pool`, you likely have (or should have) a deliberate split:

| Pool | Mode | Purpose |
| --- | --- | --- |
| `default_node_pool` | System | AKS internals, ArgoCD, Vault operator |
| Extra pool(s) | User | Your application workloads |

---

### Immediate Next Action

Run this to inspect your current cluster's node pool modes and confirm what you actually have deployed:

This will confirm whether your system/user split is how you think it is.

---

Role

You are a Principal Cloud Architect performing an architecture review for an enterprise Kubernetes deployment platform operating across multiple customer Azure subscriptions.

Your task is to evaluate deployment and operational architecture choices and recommend a secure, repeatable, low-friction enterprise pattern.

\---

Problem Summary

We deploy Azure Kubernetes Service (AKS) clusters into customer-owned Azure subscriptions using Terraform.

Clusters are deployed as private AKS clusters with no public Kubernetes API endpoint.

Terraform is responsible for:

- Infrastructure provisioning
- AKS deployment
- Initial cluster bootstrap using the Terraform Helm provider
- Installing ArgoCD as the GitOps controller

After bootstrap, ArgoCD manages application delivery.

\---

Environment Characteristics

Organizational Model

- Deployments occur repeatedly across many customer tenants/subscriptions
- Customers control networking and security requirements
- We must conform to customer governance rather than define it

Customer Constraints

Customers typically:

- Provide a fixed CIDR range
- Require minimal IP consumption
- Prefer approved enterprise access patterns
- Frequently mandate Azure Bastion for administrative access
- Disallow public exposure of management endpoints

\---

Technical Constraints

AKS

- Private cluster
- API server reachable only from:
	- cluster VNet
	- peered VNets
	- private connectivity paths

Terraform Execution Requirements

Terraform execution environment must:

- Reach Kubernetes API server
- Access remote Terraform state (Azure Storage backend)
- Run Helm and Kubernetes providers reliably
- Support repeatable automation across environments

Operational Goals

- Minimise infrastructure footprint
- Reduce networking complexity
- Avoid unnecessary public IP usage
- Enable deterministic deployments
- Reduce ongoing operational overhead
- Align with enterprise security expectations

\---

Architectural Options Under Evaluation

Option A—Azure Cloud Shell

Terraform executed from Azure Cloud Shell.

Consider:

- Default Cloud Shell vs VNet-integrated Cloud Shell
- Networking reliability to private AKS
- Operational repeatability
- Suitability for enterprise automation workflows

\---

Option B—Jumpbox VM + Azure Bastion

Deploy a small VM inside the customer VNet used to run Terraform interactively.

Characteristics:

- VM has no public IP
- Accessed through Azure Bastion
- Terraform and kubectl executed locally on VM

Evaluate:

- Simplicity
- Security posture
- CIDR/IP consumption impact
- Enterprise acceptance
- Long-term maintainability

\---

Option C—Self-Hosted Automation Runner Inside VNet

Deploy a dedicated CI/CD or Terraform runner within the customer VNet.

Terraform runs non-interactively.

Evaluate:

- Separation of human vs automation access
- GitOps alignment with ArgoCD
- Security and auditability benefits
- Lifecycle and scaling considerations

\---

Key Design Questions

Provide architectural guidance addressing:

1. What is the recommended enterprise reference architecture for bootstrapping private AKS using Terraform + Helm?
2. Which execution location for Terraform is most appropriate and why?
3. Should Terraform directly manage Kubernetes resources long-term, or only bootstrap ArgoCD?
4. What pattern minimises networking exceptions across customer environments?
5. What approach best balances:
	- security
	- repeatability
	- operational simplicity
	- customer acceptance
6. Should interactive administrative access exist after cluster bootstrap?

\---

Expected Output

Provide:

- Recommended architecture decision
- Clear reasoning and tradeoff analysis
- Anti-patterns to avoid
- Enterprise-scale operational considerations
- Suggested evolution path from bootstrap → steady-state operations

---

## Architecture Review: Private AKS Bootstrap via Terraform—Enterprise Reference Pattern

---

## Executive Summary

The recommended pattern is Option C (Self-Hosted Runner) as the primary execution mechanism, with Option B (Jumpbox + Bastion) retained as a scoped, break-glass operational tool—not a deployment mechanism. Option A is unsuitable for enterprise automation at scale.

Terraform's responsibility should be strictly bounded to infrastructure and bootstrap only. Post-bootstrap, ArgoCD owns the cluster. This is the most important architectural principle in this review.

---

## Section 1—Terraform Execution Location Analysis

### Option A—Azure Cloud Shell ❌ Reject for Production

| Dimension | Assessment |
| --- | --- |
| Networking to private AKS | Requires VNet-integrated Cloud Shell, which consumes a dedicated subnet. Default Cloud Shell cannot reach private API server. |
| Repeatability | Inherently interactive and session-bound. State is fragile. Not automatable. |
| Enterprise suitability | Acceptable for exploration; unacceptable for repeatable enterprise delivery. |
| Audit trail | Minimal. Commands are not versioned or tracked. |

Verdict: Categorically an anti-pattern for production bootstrap workflows. Occasionally useful for one-off investigation, never for deployment.

---

### Option B—Jumpbox VM + Bastion ⚠️ Retain as Break-Glass Only

| Dimension | Assessment |
| --- | --- |
| Networking | VM is inside the VNet—full, reliable access to private API server. No routing exceptions needed. |
| Security posture | Strong. No public IP. Bastion provides audited, MFA-protected access. Aligns with enterprise expectations. |
| CIDR consumption | One VM private IP. Negligible. |
| Repeatability | Poor. Terraform state left on VM disk. Human-executed. No git-driven workflow. |
| Lifecycle risk | VM becomes a snowflake. Config drift. Patching burden. Who owns it long-term? |
| Enterprise acceptance | Very high. Most enterprise security teams understand and approve this model. |

Verdict: Excellent security posture, poor operational model for repeated automated deployments. Ideal as a scoped break-glass tool for emergency cluster access—not a deployment runner.

The jumpbox should be:

- Minimal size (B2s is sufficient)
- Deployed with no persistent state
- Locked to Bastion-only access
- Rebuilt from automation, not maintained manually

---

### Option C—Self-Hosted Runner Inside VNet ✅ Recommended

| Dimension | Assessment |
| --- | --- |
| Networking | Runner is VNet-resident. Consistent, reliable private API access. |
| Repeatability | Fully deterministic. Git-triggered. No human variance. |
| Security | No public IP required. Identity via Managed Identity (not credentials). Audit trail in pipeline logs. |
| GitOps alignment | Runner executes Terraform from git. Matches the declarative, versioned intent of ArgoCD downstream. |
| Separation of concerns | Human access (Bastion + jumpbox) is cleanly separated from automation access (runner). |
| Lifecycle | Runner can be containerised, ephemeral, and rebuilt on demand. |

Verdict: The only option that supports enterprise-scale, repeatable, auditable deployment. Should be the default.

---

## Section 2—Recommended Reference Architecture

### Conceptual Topology

```
┌─────────────────────────────────────────────────────────┐
│                  Customer Azure Subscription             │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │                  Customer VNet                    │   │
│  │                                                   │   │
│  │  ┌─────────────┐    ┌──────────────────────────┐ │   │
│  │  │  Runner     │    │   AKS Private Cluster    │ │   │
│  │  │  Subnet     │───▶│   (No public API)        │ │   │
│  │  │             │    │                          │ │   │
│  │  │  [Runner VM │    │  ┌────────────────────┐  │ │   │
│  │  │   or ACI]   │    │  │ ArgoCD             │  │ │   │
│  │  └─────────────┘    │  │ (post-bootstrap)   │  │ │   │
│  │                     │  └────────────────────┘  │ │   │
│  │  ┌─────────────┐    └──────────────────────────┘ │   │
│  │  │  Bastion    │                                  │   │
│  │  │  Subnet     │    ┌──────────────────────────┐  │   │
│  │  │  (AzureBast │    │  Jumpbox VM (Break-Glass)│  │   │
│  │  │  ionSubnet) │───▶│  No Public IP            │  │   │
│  │  └─────────────┘    └──────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Azure Storage Account (Terraform State)          │   │
│  │  Private Endpoint / Service Endpoint              │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

         ▲
         │  Git push triggers pipeline
         │
┌─────────────────┐
│  Your Platform  │
│  CI/CD System   │
│  (GitLab/GitHub │
│   /ADO)         │
└─────────────────┘
```

---

### Subnet Requirements (Minimal Footprint)

| Subnet | CIDR | Notes |
| --- | --- | --- |
| AKS Node Pool | Customer-defined | Largest allocation |
| `AzureBastionSubnet` | `/26` minimum (Azure-mandated) | Fixed name required |
| Runner Subnet | `/29` (6 usable) | Small; runner + optional jumpbox |

This is the minimum viable subnet model. No additional subnets needed unless customer requires further segmentation.

---

### Identity Model—No Credentials, Only Managed Identity

The runner VM must authenticate to Azure without stored credentials:

hcl

```
# Runner VM identity
resource "azurerm_linux_virtual_machine" "runner" {
  identity {
    type = "SystemAssigned"
  }
}

# Grant scoped permissions to the runner's identity
resource "azurerm_role_assignment" "runner_aks_contributor" {
  scope                = azurerm_kubernetes_cluster.this.id
  role_definition_name = "Azure Kubernetes Service Cluster Admin Role"
  principal_id         = azurerm_linux_virtual_machine.runner.identity[0].principal_id
}

resource "azurerm_role_assignment" "runner_state_blob" {
  scope                = azurerm_storage_account.tfstate.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_virtual_machine.runner.identity[0].principal_id
}
\`\`\`

Terraform uses \`azurerm\` with \`use_msi = true\`. No service principal secrets. No credential rotation problem.

---

## Section 3 — Terraform Responsibility Boundary

This is the most critical architectural decision. Get this wrong and you create long-term operational debt.

### The Principle: Terraform Owns Infrastructure, ArgoCD Owns Cluster State
\`\`\`
┌─────────────────────────────────────────────────┐
│              Terraform Responsibility            │
│                                                 │
│  ✅ AKS cluster (azurerm_kubernetes_cluster)   │
│  ✅ Node pools                                  │
│  ✅ VNet, subnets, NSGs                         │
│  ✅ Azure resources (Vault, ACR, storage, etc.) │
│  ✅ ArgoCD Helm install (bootstrap only)        │
│  ✅ Initial ArgoCD App-of-Apps or root app      │
│                                                 │
└─────────────────────────────────────────────────┘
             │
             │  Terraform installs ArgoCD, then
             │  hands off control
             ▼
┌─────────────────────────────────────────────────┐
│              ArgoCD Responsibility              │
│                                                 │
│  ✅ All application deployments                 │
│  ✅ Cluster add-ons (cert-manager, ingress, etc)│
│  ✅ RBAC and namespace management              │
│  ✅ Secrets operator configuration             │
│  ✅ Ongoing Helm chart lifecycle               │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Why Terraform Must Not Manage Kubernetes Resources Long-Term

- The `kubernetes` and `helm` Terraform providers have known instability with cluster lifecycle events (upgrades, node pool changes, credential rotation). They attempt to connect to the API during `plan`, which causes cascading failures.
- Kubernetes resources in Terraform state create tight coupling between infrastructure changes and cluster state—a `terraform apply` for a VNet change should not need a healthy Kubernetes API.
- ArgoCD provides drift detection, self-healing, and rollback that Terraform cannot. Using Terraform for ongoing cluster resources duplicates and conflicts with this.

### The Clean Bootstrap Handoff Pattern

hcl

```
# 1. Deploy AKS
resource "azurerm_kubernetes_cluster" "this" { ... }

# 2. Install ArgoCD via Helm (bootstrap only)
resource "helm_release" "argocd" {
  depends_on = [azurerm_kubernetes_cluster.this]
  
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  create_namespace = true
  
  values = [file("${path.module}/argocd-values.yaml")]
}

# 3. Deploy root App-of-Apps to hand over cluster management
resource "kubectl_manifest" "root_app" {
  depends_on = [helm_release.argocd]
  
  yaml_body = templatefile("${path.module}/root-app.yaml", {
    cluster_name = var.cluster_name
    git_repo     = var.gitops_repo_url
  })
}

# After this point — Terraform does not touch the cluster again
# unless AKS infrastructure itself changes
\`\`\`

After \`root_app\` is applied, ArgoCD reconciles everything else from git. Terraform's Kubernetes/Helm involvement ends.

---

## Section 4 — Networking Pattern for Minimal Customer Friction

### The Core Problem

Every customer environment has different firewall rules, peering topologies, and security policies. You cannot own the network, so you must minimise your dependency on it.

### Recommended Pattern: Locality

Everything that needs to talk to the private API server lives inside the same VNet or a directly peered VNet:

- Runner VM → AKS API: same VNet, no firewall exception needed
- ArgoCD → Git repositories: outbound HTTPS (port 443), almost universally permitted
- ArgoCD → ACR/OCI: outbound HTTPS (port 443)

This eliminates the need for inbound networking exceptions, which are the hardest to get approved in customer environments.

### What to Avoid

- NAT Gateway + public IP for runner: Adds cost and IP consumption. Not needed if runner is VNet-local.
- VNet peering back to your platform's VNet for Terraform execution: Creates a persistent network dependency and raises customer governance questions about data sovereignty and cross-tenant access.
- Running Terraform from your platform's CI/CD system directly: Requires either a VPN/peering to the customer VNet or an exception to expose the API server — both are problematic.

### Preferred Egress Model
\`\`\`
Runner → (same VNet) → AKS Private API        # No exceptions needed
Runner → (Service Endpoint) → Azure Storage   # Terraform state
ArgoCD → HTTPS → Git / OCI / ACR              # Outbound only
\`\`\`

---

## Section 5 — Balancing the Four Constraints

| Concern | How the Pattern Addresses It |
|---|---|
| Security | Managed Identity (no secrets), no public IPs, Bastion for human access, runner is ephemeral |
| Repeatability | Git-triggered pipeline, idempotent Terraform, ArgoCD reconciles drift |
| Operational Simplicity | Terraform owns infrastructure only; ArgoCD owns cluster; clear responsibility boundary |
| Customer Acceptance | Runner is a small VM in their VNet; Bastion is an approved enterprise pattern; no public exposure |

---

## Section 6 — Post-Bootstrap Interactive Access

### Should It Exist?

Yes, but scoped, audited, and break-glass in nature — not a default operational pattern.

### Recommended Model
\`\`\`
Day-to-day operations:
  ArgoCD UI  ──▶ cluster state (read/apply via GitOps)
  Metrics/Alerting ──▶ Prometheus/Grafana via ingress (internal)

Break-glass (incident response only):
  Engineer ──▶ Azure Bastion ──▶ Jumpbox VM ──▶ kubectl

Prohibited:
  Direct kubectl apply from engineer's laptop
  Any change made outside of git
\`\`\`

The jumpbox should have:
- \`kubectl\` and \`helm\` installed
- Kubeconfig populated via \`az aks get-credentials\` (using the engineer's own Entra ID identity)
- No standing access — consider Just-In-Time (JIT) VM access via Microsoft Defender for Cloud
- All Bastion sessions logged to Log Analytics

---

## Section 7 — Anti-Patterns to Avoid

### 🚫 Long-lived Terraform management of Kubernetes resources
Causes plan failures during cluster upgrades and creates state coupling between infrastructure and application layers.

### 🚫 Storing kubeconfig or service principal credentials in Terraform state
State files in Azure Storage are encrypted at rest, but credentials in state are still a liability. Use Managed Identity.

### 🚫 Using Cloud Shell as a deployment mechanism
No audit trail, session-bound, not repeatable, not automatable.

### 🚫 Opening the AKS private API server to public internet "temporarily"
Customers will notice. It often can't be undone quickly. Always prefer VNet-local access.

### 🚫 Running Terraform Helm provider for ongoing application lifecycle
The Helm provider is appropriate for bootstrap only. It has no drift detection, no self-healing, and creates race conditions with ArgoCD.

### 🚫 Jumpbox as a permanent, manually maintained VM
It will drift. It will become a snowflake. It will be forgotten. Define it in Terraform, keep it minimal, restrict it to Bastion access.

---

## Section 8 — Evolution Path: Bootstrap → Steady State
\`\`\`
Phase 1 — Bootstrap (Terraform owns everything temporarily)
────────────────────────────────────────────────────────
  terraform apply
    └── AKS cluster
    └── Networking
    └── Azure resources
    └── ArgoCD (Helm, bootstrap only)
    └── Root App-of-Apps (hands control to ArgoCD)

Phase 2 — Handoff (ArgoCD takes control)
────────────────────────────────────────────────────────
  ArgoCD syncs root app from git
    └── Installs cluster add-ons
    └── Deploys namespaces and RBAC
    └── Configures Vault Secrets Operator
    └── Deploys application workloads

Phase 3 — Steady State (Terraform is infrastructure-only)
────────────────────────────────────────────────────────
  terraform apply only triggered for:
    └── Node pool changes
    └── AKS version upgrades
    └── Azure resource changes (networking, Vault, ACR)
    └── Never for Kubernetes objects

  Human access only via:
    └── Bastion → Jumpbox → kubectl (break-glass)
    └── ArgoCD UI (day-to-day)

Phase 4 — Maturity (Runner lifecycle improvements)
────────────────────────────────────────────────────────
  Runner VM → Azure Container Instances (ephemeral)
  Add Terraform plan approval gates in pipeline
  Add OPA/Conftest policy checks on Terraform plans
  Centralise runner image into your platform's ACR
```

---

## Recommended Decision Summary

| Decision | Recommendation |
| --- | --- |
| Terraform execution location | Self-hosted runner VM inside customer VNet |
| Runner identity | System-assigned Managed Identity |
| Human access mechanism | Azure Bastion + Jumpbox (break-glass only) |
| Terraform Kubernetes scope | Bootstrap ArgoCD only; no ongoing K8s resources |
| Networking model | VNet-local runner; outbound HTTPS for ArgoCD |
| Long-term cluster management | ArgoCD exclusively, driven from git |
| Interactive access post-bootstrap | JIT-scoped, Bastion-audited, break-glass only |

---

### Immediate Next Action

Define your runner VM as a Terraform resource in a shared module that deploys alongside every cluster. Start with this skeleton:

This makes the runner a first-class, reproducible infrastructure component rather than a manually created afterthought—and it signals to customers that the access model is deliberate and governed.
