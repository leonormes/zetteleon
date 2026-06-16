---
title: Kubernetes Cluster Bootstrapping
wiki_type: dossier
entity_kind: project
created: 2026-06-04T08:05:28+00:00
modified: 2026-06-04T08:05:28+00:00
tags: [wiki, dossier]
sources: [raw/2026-06-03-pieces-k8s-argocd-bootstrapping.md]
---

## Summary

Investigation into automating ArgoCD deployment on a private Kubernetes cluster immediately after Terraform provisioning — eliminating the manual jumpbox step. The core question: "is there a cloud-init equivalent for Kubernetes?" Explored patterns including argocd-autopilot, Terraform Helm/K8s providers, Cluster API, Flux bootstrap, and Crossplane.

## Key Facts

- **Problem:** After Terraform creates a private K8s cluster, a jumpbox in the private network is needed to install ArgoCD and seed the app-of-apps pattern. This manual gap should be automated.

  > "is there such a thing as a cloud-init but for kubernetes? We use terraform to deploy a priavte k8s cluster then have to use a jumpbox in the private network to run the rest of the deployment, which is an argoccd app of apps. It would be better to have a way to automate the argocd deployment" — [[raw/2026-06-03-pieces-k8s-argocd-bootstrapping]] (Pieces: 210f126f-42c7-4dba-9cbf-d6607e3f6feb)

- **Option 1 — Terraform Helm + Kubernetes Providers:** If Terraform can reach the cluster API to create it, it can also install ArgoCD and seed the app-of-apps in the same `terraform apply` — no jumpbox needed. Uses `helm_release` and `kubectl_manifest` resources.

  > "If Terraform can reach the cluster API to create it, it can also install ArgoCD and seed the app-of-apps in the **same `terraform apply`** — no jumpbox needed." — [[raw/2026-06-03-pieces-k8s-argocd-bootstrapping]] (Pieces: d36515fc-0012-4669-a78f-d088d2eb2a53)

- **argocd-autopilot** is the closest thing to "cloud-init for ArgoCD on Kubernetes" — purpose-built for bootstrapping ArgoCD with an app-of-apps pattern.

  > "**`argocd-autopilot`** is probably the closest thing to "cloud-init for ArgoCD on Kubernetes"" — [[raw/2026-06-03-pieces-k8s-argocd-bootstrapping]] (Pieces: d36515fc-0012-4669-a78f-d088d2eb2a53)

- **Other options explored:** Cluster API (CAPI) for declarative cluster lifecycle, FluxCD `flux bootstrap` as an ArgoCD alternative, Crossplane for unified infra + app management, and `local-exec` provisioner for scripting.

  > "1. **Terraform + Helm Provider / Kubernetes Provider** ... 2. **Cluster API (CAPI)** ... 3. **Flux Bootstrap** ... 4. **ArgoCD's own bootstrapping** ... 5. **Crossplane** ... 6. **Terraform + local-exec provisioner**" — [[raw/2026-06-03-pieces-k8s-argocd-bootstrapping]] (Pieces: 95a5e00f-fd5a-483e-805a-fb4cf7eac6dd)

- **Key constraint:** For private clusters, Terraform (or the CI/CD system) needs network access to the cluster API — either via bastion/VPN or by running within the network.

  > "If the cluster is private, Terraform would need network access to reach it - either by running from within the network via a bastion or VPN, or through a CI/CD system that already has that connectivity." — [[raw/2026-06-03-pieces-k8s-argocd-bootstrapping]] (Pieces: 95a5e00f-fd5a-483e-805a-fb4cf7eac6dd)

## Timeline

- 2026-06-04: Initial exploration of Kubernetes cluster bootstrapping patterns; user asked about cloud-init equivalent for K8s

## Connections

- [[cicd-tooling-validated]] — related GitOps/ArgoCD pipeline work
- [[Azure-AKS]] — AKS cluster deployments
- [[Terraform IaC Modules]] — Terraform infrastructure provisioning

## Contradictions

_(none flagged)_

## Open Questions

- Which bootstrapping pattern is most appropriate for the FTFL private cluster setup?
- Does the Terraform runner have network access to the private cluster API after creation?
- Is argocd-autopilot compatible with the existing app-of-apps structure?
