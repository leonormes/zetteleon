---
captured: "2026-02-16T09:38:32+00:00 2026-02-16T09:38:32+00:00"
created: 2026-02-16T09:38:35+00:00
modified: 2026-02-16T09:40:39+00:00
source: "https://chatgpt.com/c/698e5b38-9930-8392-9a8c-898f82c19b97"
status: "processing"
tags: ["input"]
title: HEAD K8s On-Prem Deployment Options
type: "head"
---

## Raw Output / Content

We deploy our applications to a k8s cluster. Usually this is either an azure Managed aks or Aws eks. A recent customer wants us to deploy to their on premise infrastructure. We are not sure what this consists of. But I want to make a plan. What are our options for either deploying some sort of kuberenetes cluster so we can deploy our app or having the customer manager a cluster that we deploy on. VMware was mentioned.

---

You've basically got two big tracks:

1. You provide a Kubernetes "target" (or a managed-ish one) on their premises, then you deploy like you do to AKS/EKS.
2. They provide the Kubernetes "target", and you standardize what "a supported cluster" means, then you deploy.

Below is a pragmatic plan + the realistic options (including VMware).

---

## Step 0: Decide what You're Willing to Own (support boundary)

Before picking tech, define the support model you'll offer:

- Customer-managed cluster: you support _your app_ on a cluster that meets your requirements. You do not support cluster lifecycle.
- Shared responsibility: you provide reference architecture + automation; they run it; you help with upgrades and incidents.
- Vendor-managed on-prem: you sell an on-prem "managed Kubernetes" experience (often via a partner product).
- You fully manage on-prem: possible, but you're now in the business of infra ops (patching, backups, DR, CVEs, etc.).

Most software vendors end up happiest with Customer-managed + clear conformance checks.

---

## Option A (most common): Customer Provides Kubernetes, You Deploy

You publish a "Supported Kubernetes Platform" matrix and a "Cluster Readiness Checklist".

### Good Customer-managed Kubernetes Choices On-prem

- VMware Tanzu Kubernetes Grid (TKG) (this is probably what "VMware was mentioned" points at)
- Red Hat OpenShift (very common in enterprise on-prem)
- Rancher (SUSE Rancher) managing RKE2/k3s (popular for on-prem + edge)
- Vanilla upstream Kubernetes via kubeadm (works, but ops maturity varies wildly)

### What You Standardize so You Can Deploy Consistently

- Kubernetes version support window (e.g., "latest minus 2 minor versions")
- Ingress: NGINX / HAProxy / OpenShift routes (pick what you'll support)
- Storage: CSI support and at least one supported StorageClass (e.g., vSphere CSI, Ceph/Rook, NetApp Trident, Portworx)
- Load balancer: how services of type LoadBalancer work on-prem (MetalLB, NSX ALB, F5, etc.)
- Registry access: can nodes pull from your registry? (proxy, allowlists, air-gap)
- Observability hooks: Prometheus endpoints, logs to stdout, optional OpenTelemetry
- Security: network policies (Calico/Cilium), Pod Security admission posture, RBAC model, secrets mgmt (KMS/Vault), image scanning expectations

### How You Enforce it

- Provide a "cluster validation" script (kube-bench-ish checks + your app prerequisites)
- Provide Helm charts or GitOps (Argo CD/Flux) as the supported deployment method
- Provide a supported ingress + storage reference per platform (VMware, OpenShift, etc.)

Pros: fastest; least risk; clean support boundaries.
Cons: your deployment must handle variation (ingress/storage/LB/PSA differences).

---

## Option B: You Ship a Kubernetes Distro / Reference Stack on Their Infra

You essentially deliver "Kubernetes as part of the product" (or as a packaged deployment).

### Common Ways to Do This

- RKE2 (robust "enterprise-y" Kubernetes) or k3s (lighter)
- kubeadm -based build + your own automation (Ansible/Terraform)
- Canonical Charmed Kubernetes (if they like Ubuntu tooling)
- Cluster API (if you want a more "Kubernetes-native" lifecycle, often used with vSphere)

Pros: consistent platform; fewer unknowns; easier repeatability.
Cons: you now own upgrades, CVEs, etc. unless you contractually push that to them.

A good compromise is: you provide automation + golden config, they run it, and you only support _your app_ on clusters produced by that automation.

---

## Option C: "Managed On-prem Kubernetes" via a Vendor

If they want "managed-like" experiences on-prem:

- Azure Stack HCI + AKS (AKS on Azure Stack HCI) (if they're Azure-aligned)
- AWS Outposts + EKS (EKS on Outposts) (if they're AWS-aligned)
- Google Anthos (less common but exists)

Pros: closest to AKS/EKS operational model; strong vendor story.
Cons: expensive; hardware constraints; procurement lead times; customer must already be bought in.

---

## VMware Angle: what it Might Mean (and what to ask)

"VMware" could mean any of these:

1. They just run VMs on vSphere and want you to deploy Kubernetes on top (then TKG / Rancher / kubeadm on VMs are options).
2. They already have Tanzu / TKG and want you to deploy onto it.
3. They have NSX / Avi / vSAN which impacts load balancing and storage (good news: these can be strong building blocks).

Key VMware-specific questions

- Do you already run Tanzu Kubernetes Grid (or OpenShift on vSphere)?
- What provides LoadBalancer capability? (NSX ALB/Avi, F5, MetalLB, etc.)
- What provides persistent storage? (vSAN, NetApp, Pure, Ceph, etc. via CSI)

---

## The Plan: Get to a Decision Fast (without Knowing Their Infra yet)

### 1) Send a short "discovery questionnaire" (1 page)

You want answers to these, because they determine everything:

Environment

- On-prem virtualization: vSphere? Hyper-V? bare metal?
- Network: IP ranges, DNS, outbound internet/proxy, inbound access model
- Any air-gap constraints?

Kubernetes

- Do you already have a Kubernetes cluster? If yes: distro + version + node count
- How do you do ingress and L7 routing today?
- How do you do L4 load balancing for services?

Storage

- Required persistence? RWO/RWX? backups? snapshot expectations?
- What storage platform exists and does it have CSI?

Security / compliance

- Required authn/authz (OIDC/AD), auditing, image scanning, runtime restrictions
- Secrets management preference (Vault, external KMS, etc.)

Operations

- Who patches OS and Kubernetes?
- Monitoring/logging platform (Prometheus, Splunk, ELK, etc.)
- RTO/RPO / DR needs

### 2) Decide Your "supported target" Baseline

Pick a minimum "contract" for support, for example:

- Kubernetes v1.xx–v1.yy
- Ingress: NGINX or platform-native equivalent
- StorageClass must exist + dynamic provisioning works
- DNS + TLS model defined
- Either: working LoadBalancer (MetalLB/NSX/F5) or you support NodePort behind their LB

### 3) Offer Them 2–3 Deployment Models (so They Can choose)

I'd present it like:

- Model 1 (preferred): Customer-managed Kubernetes (OpenShift / TKG / Rancher / upstream) + you provide Helm/GitOps and readiness checks.
- Model 2: You deliver a reference cluster (RKE2 on VMs) but customer runs it; you support clusters built by your automation.
- Model 3: Vendor-managed on-prem (Outposts/AKS HCI) if they already have it or want to buy it.

### 4) Create a POC Path

- One small non-prod cluster (3 control-plane + 3 workers, or smaller depending)
- Validate: ingress, TLS, storage, upgrades, backup/restore, and your app's key SLOs

---

## Practical Recommendation (what I'd Do in Your shoes)

Given you're used to AKS/EKS and you _don't yet know their infra_:

1. Make "customer-managed cluster" the default with a strict readiness checklist.
2. Support VMware TKG and OpenShift explicitly (those are common enterprise on-prem anchors).
3. Keep a fallback: RKE2-on-VMs reference build you can provide if they have no Kubernetes at all.

That gives you a clear story whether they have VMware, OpenShift, "just VMs", or something more exotic.

---

If you want, paste whatever you already know about the customer (even just "they have vSphere + X storage + F5") and I'll turn this into a concrete one-page options doc + a checklist you can send them, including what you will/won't support.
