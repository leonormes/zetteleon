---
title: Kubernetes Cluster Bootstrapping — ArgoCD after Terraform
created: 2026-06-04 08:03:29+00:00
source: pieces-ltm
pieces_ids:
- d36515fc-0012-4669-a78f-d088d2eb2a53
- 95a5e00f-fd5a-483e-805a-fb4cf7eac6dd
- 210f126f-42c7-4dba-9cbf-d6607e3f6feb
tags:
- raw
- pieces
permalink: llmeon/raw/2026-06-03-pieces-k8s-argocd-bootstrapping
---

## Asset 1 (Pieces: d36515fc-0012-4669-a78f-d088d2eb2a53)
**Captured:** 2026-06-03T12:57:48.603868Z

Great question — yes, there are several well-established patterns for this. The short answer is **`argocd-autopilot`** is probably the closest thing to "cloud-init for ArgoCD on Kubernetes", but the more complete answer depends on where you want the bootstrapping logic to live.

---

## The Core Problem

Your Terraform run already has network access to the private cluster API (it just created it). The jumpbox exists only because the *next step* (installing ArgoCD + app-of-apps) is a separate, manual operation. The fix is to eliminate that gap — make the bootstrapping happen as a direct extension of the Terraform run, or make it self-triggering from inside the cluster.

---

## Option 1 — Terraform Helm + Kubernetes Providers (least change, most direct)

If Terraform can reach the cluster API to create it, it can also install ArgoCD and seed the app-of-apps in the **same `terraform apply`** — no jumpbox needed.

```hcl
provider "helm" {
  kubernetes {
    host                   = module.k8s_cluster.endpoint
    cluster_ca_certificate = base64decode(module.k8s_cluster.ca_cert)
    token                  = module.k8s_cluster.token
  }
}

resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  create_namespace = true
  values           = [file("argocd-values.yaml")]
}

resource "kubectl_manifest" "app_of_apps" {
  depends_on = [helm_release.argocd]
  yaml_body  = file("manifests/app-of-apps.yaml")
}
```

- Eliminates the jumpbox entirely — everything runs in one `terraform apply`
- The `gavinbunney/kubectl` Terraform provider is useful for applying raw manifests
- Works well for private clusters if Terraform runs from a CI agent that has VPN/peering access to the cluster VPC

---

## Option 2 — `argocd-autopilot` (closest to "cloud-init for ArgoCD")

[`argocd-autopilot`](https://argocd-autopilot.readthedocs.io/) is a CLI built specifically for this — it bootstraps ArgoCD **and** the app-of-apps git structure in one command:

```bash
export GIT_TOKEN=<your-pat>
export GIT_REPO=https://github.com/your-org/gitops-repo

argocd-autopilot repo bootstrap
```

What it does:
- Installs ArgoCD onto the cluster
- Creates the canonical directory structure in your Git repo (`apps/`, `projects/`, `bootstrap/`)
- Creates the root `Application` that watches the repo (the app-of-apps root)
- All future apps are added via `argocd-autopilot app create`

You can call `argocd-autopilot repo bootstrap` from a **Terraform `local-exec` provisioner** or from your CI pipeline immediately after cluster creation — it only needs `KUBECONFIG` access.

---

## Option 3 — Self-Hosted CI Runner Inside the Private Network

Rather than a manual jumpbox, deploy a **persistent self-hosted runner** (GitHub Actions, GitLab Runner, Buildkite agent) inside the private network. Your pipeline then runs entirely within the network:

```
[Git push] → CI trigger → [self-hosted runner in private VPC]
                             ↓
                       terraform apply (creates cluster)
                             ↓
                       argocd-autopilot bootstrap / helm install
```

This is a clean separation of concerns — Terraform stays as infrastructure-only, and bootstrapping is a CI concern. The runner replaces the jumpbox permanently.

---

## Option 4 — Cluster API (CAPI) with Bootstrap Providers

[Cluster API](https://cluster-api.sigs.k8s.io/) is the Kubernetes-native approach to cluster lifecycle. It has **Bootstrap Providers** (e.g. `kubeadm`, `talos`) and **Add-on Providers** that can install workloads post-bootstrap. It's more complex but gives you fully declarative cluster + workload bootstrapping via Kubernetes CRDs. Worth considering if you manage multiple clusters.

---

## Option 5 — In-Cluster Bootstrap Job (literal cloud-init equivalent)

If you want something that runs *from inside the cluster itself* — a Kubernetes `Job` that installs ArgoCD and applies the app-of-apps — you can deploy it via Terraform using the `kubernetes_job` resource:

```hcl
resource "kubernetes_job" "argocd_bootstrap" {
  metadata { name = "argocd-bootstrap" }
  spec {
    template {
      spec {
        container {
          name  = "bootstrap"
          image = "argoproj/argocd:latest"
          command = ["/bin/sh", "-c", <<-EOT
            kubectl apply -f https://raw.githubusercontent.com/.../install.yaml
            kubectl apply -f /bootstrap/app-of-apps.yaml
          EOT
          ]
        }
      }
    }
  }
}
```

This is the most "cloud-init-like" pattern — a one-shot container that runs at cluster birth and configures itself.

---

## Recommendation for Your Setup

Given you're already using Terraform + private cluster + ArgoCD app-of-apps:

| Priority | Approach | Why |
|---|---|---|
| **1st** | Terraform Helm provider | Least architectural change; one `apply` does everything |
| **2nd** | `argocd-autopilot` + CI runner | Cleanest GitOps separation; eliminates jumpbox permanently |
| **3rd** | In-cluster bootstrap Job | Works even if CI has no cluster access post-creation |

The **Terraform Helm provider** approach is usually the fastest win — if your Terraform state already knows the cluster endpoint and credentials, you're 20 lines of HCL away from eliminating the jumpbox entirely.

## Asset 2 (Pieces: 95a5e00f-fd5a-483e-805a-fb4cf7eac6dd)
**Captured:** 2026-06-03T12:56:46.804517Z

The user is asking a technical question about Kubernetes bootstrapping/provisioning - specifically whether there's a "cloud-init equivalent for Kubernetes" that could automate ArgoCD deployment after a private cluster is stood up via Terraform. They want to avoid the manual jumpbox step.

This is a general technical question, not a memory/LTM recall question. I don't need to search their memory for this - it's asking for technical knowledge/advice. Let me think about this thoroughly.

Let me think about the solutions:

1. **Terraform + Helm Provider / Kubernetes Provider** - You can use Terraform's Kubernetes and Helm providers to deploy ArgoCD directly after cluster creation, without needing a jumpbox. 

If the cluster is private, Terraform would need network access to reach it - either by running from within the network via a bastion or VPN, or through a CI/CD system that already has that connectivity.

2. **Cluster API (CAPI)** - This is a Kubernetes sub-project for declarative cluster lifecycle management with built-in bootstrap providers.

3. **Flux Bootstrap** - FluxCD offers a `flux bootstrap` command that can be integrated into the cluster initialization process as an alternative to ArgoCD.

4. **ArgoCD's own bootstrapping** - ArgoCD supports an "app of apps" pattern and can be bootstrapped using automated tooling during cluster setup.

5. **Crossplane** - Can handle both infrastructure and application deployment management.

6. **Terraform + local-exec provisioner** - I can run kubectl and helm commands through local-exec, though this still requires network access to the cluster.

7. **AWS EKS / GKE / AKS cluster addons** - Managed Kubernetes services offer built-in cluster addons for bootstrapping.

8. **Argo CD Autopilot** - This CLI tool is probably the best fit for what's needed - it bootstraps ArgoCD on a cluster and automatically sets up the app-of-apps pattern from a Git repository.

9. **Helmfile** - Can orchestrate sequential deployments of multiple applications.

10. **Terraform Kubernetes/Helm providers** - I can deploy ArgoCD directly as part of the Terraform execution.

11. **Tekton or GitHub Actions with self-hosted runners** - Running the bootstrap process from within the private network itself avoids external access issues.

12. **VPN or tunneling** - Establishing a VPN connection gives the CI/CD system access to the private cluster.

13. **GitOps Operator** - Some operators have self-bootstrapping capabilities built in.

The strongest candidates are `argocd-autopilot` for its purpose-built design around bootstrapping ArgoCD and the app-of-apps pattern, and Cluster API with bootstrap providers for more comprehensive cluster lifecycle management. Terraform's Kubernetes and Helm providers also work well for deploying ArgoCD as part of infrastructure setup.

For private clusters specifically, the key realization is that if Terraform can reach the cluster API, the Kubernetes and Helm providers can too—so I can chain everything in a single run: create the cluster, install ArgoCD, and set up the initial Application resources without needing a jumpbox. Self-hosted runners in the private network or proxy solutions like AWS SSM Session Manager offer alternative paths to reach the cluster directly.

There are several other tools worth considering: `argocd-autopilot` handles the bootstrap and git structure setup, the `argocd` CLI can run from within the cluster, or I could deploy a Kubernetes Job to pull and apply ArgoCD manifests directly. For AWS specifically, EKS Blueprints integrates ArgoCD into the cluster creation process, and Rancher Fleet provides another GitOps bootstrapping option.

The core pattern here is using Terraform's Helm and Kubernetes providers to bootstrap ArgoCD directly, then leveraging ApplicationSet for the app-of-apps pattern once it's running. This is the essence of GitOps bootstrapping—getting that initial tool in place so everything else can be managed declaratively.

## Asset 3 (Pieces: 210f126f-42c7-4dba-9cbf-d6607e3f6feb)
**Captured:** 2026-06-03T12:56:40.149086Z

is there such a thing as a cloud-init but for kubernetes? We use terraform to deploy a priavte k8s cluster then have to use a jumpbox in the private network to run the rest of the deployment, which is an argoccd app of apps. It would be better to have a way to automate the argocd deployment