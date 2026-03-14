---
captured: "2026-03-07T16:51:14+00:00 2026-03-07T16:51:14+00:00"
created: 2026-03-07T16:51:18+00:00
modified: 2026-03-14T11:10:35+00:00
source: "https://claude.ai/chat/b8b6b7db-bf79-4ea6-852c-f74660192411"
status: "processing"
tags: ["input"]
title: HEAD On-premise Kubernetes deployment options
type: "head"
---

## Raw Output / Content

We deploy our applications to a k8s cluster. Usually this is either an azure Managed aks or Aws eks. A recent customer wants us to deploy to their on premise infrastructure. We are not sure what this consists of. But I want to make a plan. What are our options for either deploying some sort of kuberenetes cluster so we can deploy our app or having the customer manager a cluster that we deploy on. VMware was mentioned.

---

## On-Premise Kubernetes: Your Options

This is a genuinely interesting problem because you're moving from "someone else manages the control plane" (AKS/EKS) to "someone has to manage the control plane." The core question is: who owns that burden?

---

## The Two Models

### Model A: Customer Provides a Cluster, You Deploy On It

Principle: You hand the customer a set of requirements (K8s version, CSI drivers, ingress, RBAC permissions, etc.) and they give you a kubeconfig. This is the least operational burden for you.

What you'd give them: A "Platform Requirements" document specifying:

- Minimum K8s version (e.g. 1.28+)
- Required cluster features (RBAC enabled, CSI driver for persistent volumes, LoadBalancer or Ingress controller)
- Namespace provisioning expectations
- Network policies / egress requirements (especially relevant for your HCP Vault connectivity)
- Resource quotas (CPU/memory for your workloads + ArgoCD + Vault Secrets Operator + monitoring stack)

Risk: You're at the mercy of their platform team's competence and responsiveness. Debugging becomes a shared-responsibility nightmare.

### Model B: You Deploy & Manage the Cluster on Their Infrastructure

Principle: You control the full stack from K8s upward. More work, but you eliminate the "it works on our cluster" finger-pointing. You'd need them to provide VMs or bare metal + networking.

---

## The Actual Technology Options

### 1\. VMware Tanzu (since VMware Was mentioned)

What it is: If the customer runs VMware vSphere, Tanzu Kubernetes Grid (TKG) lets you spin up conformant K8s clusters as first-class vSphere objects. The vSphere admin can provision clusters via the Supervisor Cluster, and you get a fairly "managed" experience on-prem.

Why it's interesting for you:

- If they already have vSphere, this is the path of least resistance for _them_
- Cluster lifecycle (upgrades, scaling) is handled through vSphere tooling
- You get a conformant cluster that behaves similarly to AKS/EKS from your workload's perspective

Watch out for:

- Tanzu licensing is not cheap, and Broadcom's acquisition of VMware has made licensing… unpredictable
- There are multiple Tanzu products (TKGs, TKGm, TKGi) and they're meaningfully different
- You'd want to confirm they're running vSphere 8+ with the Supervisor Cluster enabled

### 2\. Rancher (SUSE)

What it is: A multi-cluster management platform. Rancher can provision K8s clusters on bare metal, VMs, or cloud—and gives you a UI + API for lifecycle management. Under the hood it typically uses RKE2 (Rancher's hardened K8s distribution).

Why it's interesting:

- You could manage the cluster yourself via Rancher, even if it's on their infra
- RKE2 is CIS-hardened out of the box, which matters for enterprise/regulated customers
- Rancher is genuinely good at the "deploy K8s on VMs someone gave you" use case
- Free/open-source core, commercial support available

### 3\. k3s (Lightweight, Also SUSE/Rancher ecosystem)

What it is: A stripped-down, single-binary K8s distribution. Production-grade but minimal.

Why it's interesting:

- Dead simple to install: one command on each node
- Great if the customer's on-prem infra is modest
- Fully conformant K8s—your Helm charts and ArgoCD workflows would work unchanged

Watch out for: Perception. Some enterprise customers hear "lightweight" and get nervous, even though k3s is CNCF-certified and used in production widely.

### 4\. Kubeadm / Vanilla Kubernetes

What it is: The official upstream tool for bootstrapping K8s clusters.

Why it's interesting: Maximum control, no vendor lock-in, zero licensing cost.

Why you probably don't want this: You'd own _everything_—etcd backups, control plane HA, certificate rotation, upgrade orchestration. This is a full-time job. Unless you're building a platform team, avoid this.

### 5\. OpenShift (Red Hat)

What it is: Red Hat's enterprise K8s platform. It's Kubernetes underneath but with a heavy opinionated layer on top (built-in registry, CI/CD, monitoring, OAuth).

Why it's interesting:

- Very common in large enterprise on-prem environments
- If the customer already runs OpenShift, this is Model A—they give you a namespace/project

Watch out for:

- OpenShift has its own opinions about security contexts, networking, and image registries that _will_ require changes to your deployment manifests
- `SecurityContextConstraints` (SCCs) are more restrictive than vanilla K8s `PodSecurityStandards`—your existing manifests may not deploy cleanly
- Expensive licensing

### 6\. Cluster API (CAPI)

What it is: A Kubernetes-native way to declaratively provision and manage K8s clusters. You define clusters as CRDs on a management cluster.

Why it's interesting for your GitOps brain: You could potentially manage customer cluster lifecycle _through ArgoCD_ using CAPI manifests. Infrastructure as CRDs.

Watch out for: It's a power tool. Adds a layer of complexity. Best suited if you're going to do this for _multiple_ on-prem customers and want a repeatable pattern.

---

## The Decision Matrix

| Factor | Tanzu | Rancher/RKE2 | k3s | OpenShift | CAPI |
| --- | --- | --- | --- | --- | --- |
| Customer already has VMware | ✅ Best fit | Works on VMs | Works on VMs | Works on VMs | Works on VMs |
| You manage the cluster | Possible | ✅ Designed for this | ✅ Easy | Unusual | ✅ Designed for this |
| Customer manages the cluster | ✅ Natural fit | Possible | Possible | ✅ Natural fit | Unlikely |
| Your existing manifests work unchanged | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Likely needs changes | ✅ Yes |
| Licensing cost | 💰💰💰 | Free / paid support | Free | 💰💰💰 | Free |
| Operational complexity for you | Low–Medium | Medium | Low | Medium–High | High initially |

---

## My Recommendation

Given your stack (ArgoCD, Vault Secrets Operator, Helm charts, multi-namespace architecture):

1. First, find out what the customer already runs. If they have vSphere + Tanzu or OpenShift already, the answer picks itself—that's Model A.
2. If they just have "VMs and a network", Rancher + RKE2 is probably your sweet spot. It gives you cluster lifecycle management, works on vanilla VMs, and your existing K8s manifests deploy without modification.
3. The Vault question is critical. On-prem means your HCP Vault connectivity model changes entirely. They'll either need outbound internet access to HCP, or you'll need to deploy a self-hosted Vault instance. This is a separate but equally important planning track.

---

## Immediate Next Action

Draft a 5-question discovery email to the customer:

1. What hypervisor/infrastructure platform do you run? (vSphere, Hyper-V, bare metal, etc.)
2. Do you have an existing Kubernetes platform? (OpenShift, Tanzu, Rancher, other)
3. What are your network egress policies? (Can workloads reach the public internet, or is it air-gapped?)
4. Do you have a preferred model—you manage the cluster, or we manage it on your infra?
5. What compliance/security frameworks apply? (CIS, SOC2, ISO 27001, etc.)

Want me to draft that email properly?

---

\## SYSTEM ROLE: Principal Infrastructure Architect (On-Premise Specialist) You are an expert in On-Premise Kubernetes topologies, specifically specializing in transitioning cloud-native (AKS/EKS) applications to restricted, bare-metal, or VMware-based environments. You reject "it just works" assumptions and focus on the OSI layer 4-7 networking and CSI storage requirements.

\## THE USER CONTEXT The user is a Cloud-Native Developer/DevOps Engineer accustomed to managed services (AKS/EKS). They are facing a "Context Shift" where the underlying infrastructure (LoadBalancers, Persistent Volumes, DNS) is no longer provided by a cloud provider but must be defined or requested from a customer's VMWare/On-Prem environment.

\## PEDAGOGICAL/OPERATIONAL CONSTRAINTS 1. No Cloud Magic: Assume `Type: LoadBalancer` will fail unless a specific solution (MetalLB, F5 CIS, or Tanzu NSX-T) is defined. 2. Storage Strictness: You must differentiate between "HostPath" (dangerous/non-portable) and "CSI-based" (VMware vSAN/PureStorage) solutions. 3. Air-Gap Awareness: Assume the environment may have no internet access. All "solutions" must account for private registries and image bundling. 4. Minimalist vs. Enterprise: Always provide two options: a "Lightweight/Bootstrap" option (e.g., K3s/RKE2) and a "Heavyweight/Enterprise" option (e.g., VMware Tanzu).

\## IMMEDIATE GOAL The user needs a "Decision Matrix" and a "Discovery Questionnaire" to send to their customer. This must identify the customer's VMware version, networking capabilities (VLAN vs. VXLAN), and storage availability to determine if the user should install their own K8s or deploy onto a customer-managed cluster.

---

## On-Premise Kubernetes: The Reality Behind the Abstractions

## Why This Matters—The "Cloud Magic" You're About to Lose

When you deploy to AKS or EKS, three things happen invisibly that will not work on-prem without explicit solutions:

| Cloud Abstraction | What Actually Happens in AKS/EKS | What Happens On-Prem |
| --- | --- | --- |
| `Type: LoadBalancer` in a Service manifest | Cloud controller provisions an Azure LB / AWS NLB automatically | Nothing. The Service stays in `<pending>` forever. |
| `PersistentVolumeClaim` with a `StorageClass` | Cloud CSI driver provisions an Azure Disk / EBS volume | Fails. No CSI driver exists unless one is installed and configured. |
| Container image pull from a public registry | Node pulls from Docker Hub / ECR / ACR via the internet | Fails or is blocked. No egress, no images, no pods. |

Every one of these is a hard blocker, not a "nice to have." Your ArgoCD sync will show `Degraded` across the board if any of them are unresolved.

---

## Layer-by-Layer: What You Need to Discover

### Layer 1—Compute & Hypervisor

This determines _how_ K8s nodes get provisioned.

| Question | Why It Matters |
| --- | --- |
| What hypervisor is in use? (vSphere, Hyper-V, KVM/libvirt, bare metal) | Determines your cluster provisioning path. vSphere unlocks Tanzu and CAPI with vSphere provider. Bare metal means PXE boot or manual node setup. |
| What vSphere version? (7.x vs 8.x) | vSphere 7u1+ is required for Tanzu with Supervisor. vSphere 8 adds VM Classes and better TKGs integration. Below 7u1, Tanzu is off the table. |
| Is VMware NSX-T deployed, or just standard vSwitch/DVS? | This is a fork in the road for networking. NSX-T gives you software-defined load balancing and micro-segmentation. Without it, you need MetalLB or an external LB. |
| How are VMs provisioned? (manual, Terraform, vRealize) | If they can give you VMs via Terraform/API, you can automate. If it's "raise a ticket and wait 3 days," your deployment pipeline needs to account for that latency. |

### Layer 2–3—Network Fabric

This is where cloud-native teams get blindsided most often.

| Question | Why It Matters |
| --- | --- |
| What is the network topology? (Flat L2, VLAN-segmented, VXLAN/overlay) | K8s node-to-node communication and pod networking (Calico, Cilium, Antrea) behave very differently across these. A flat L2 network is simplest. VLAN segmentation means you need to know which VLANs your nodes and pods live on. |
| Is there a DHCP server on the node network, or are IPs statically assigned? | Cluster bootstrapping (especially Tanzu/CAPI) often expects DHCP for node IPs. Static assignment means more manual config or IPAM integration. |
| What CIDR ranges are available for: node IPs, pod network, service network? | You need to not collide with existing corporate ranges. Your default `10.96.0.0/12` for services or `10.244.0.0/16` for pods might clash with their internal addressing. |
| Is there a DNS server you can register entries on? (or is it locked down) | Your Ingress controller needs DNS records pointing to it. If their DNS is change-controlled with a 48h SLA, you need to plan around that. |
| Are there firewalls between network segments? What ports are open? | At minimum you need: `6443` (K8s API), `10250` (kubelet), `2379-2380` (etcd), `30000-32767` (NodePort range if used), plus whatever your apps expose. Calico/Cilium have their own port requirements (BGP on `179`, VXLAN on `4789`, WireGuard on `51820`). |

### Layer 4–7—Load Balancing & Ingress

This is the single biggest gap between cloud and on-prem.

Here are your concrete options, split by weight class:

#### Lightweight / Bootstrap Option: MetalLB

What it does: Provides `Type: LoadBalancer` support for bare-metal / VM-based K8s clusters. Assigns real IPs from a pool you define.

Two modes:

- Layer 2 mode: MetalLB uses ARP to announce IPs. Simple, no router config needed, but all traffic flows through a single leader node (no true load distribution). Fine for non-HA dev/staging, and often fine for modest production loads.
- BGP mode: MetalLB peers with the customer's network routers and announces IPs via BGP. True load distribution across nodes. Requires the customer's network team to configure a BGP peer—which is a conversation you need to have early.

Combined with an Ingress controller (e.g. ingress-nginx or Traefik), this gives you:

#### Enterprise Option: F5 BIG-IP + CIS, or NSX-T ALB

- If customer has F5 BIG-IP: The F5 Container Ingress Services (CIS) controller integrates directly with K8s. Your `Service` and `Ingress` objects can be configured to automatically create F5 Virtual Servers. This is common in enterprises that already own F5.
- If customer has NSX-T + Tanzu: NSX Advanced Load Balancer (formerly Avi Networks) provides L4/L7 load balancing natively integrated with the Tanzu Supervisor. This is the "it just works" path—_but only if NSX-T is actually deployed_.

Discovery question to add: "Do you have an existing load balancer appliance (F5, Citrix/NetScaler, HAProxy Enterprise, NSX ALB)?" This determines whether you bring MetalLB or integrate with what they have.

### Layer—Storage (CSI)

Your PVCs need something to bind to. On-prem, that "something" must be explicitly configured.

| Storage Backend | CSI Driver | Notes |
| --- | --- | --- |
| VMware vSAN / VMFS datastores | `csi.vsphere.vmware.com` (vSphere CSI driver) | Best fit if they're on vSphere. Provisions VMDKs as PVs. Requires a `Secret` with vCenter credentials and a `StorageClass` pointing to the datastore. |
| NetApp ONTAP | `csi.trident.netapp.io` (Trident) | Common in enterprise. Supports NFS and iSCSI. |
| Pure Storage | `pure-csi` | Block and file. |
| Longhorn (Rancher ecosystem) | `driver.longhorn.io` | Lightweight option. Distributed block storage that runs _on_ the K8s nodes themselves. No external SAN needed. Good for "the customer just gave us VMs with local disks." |
| NFS server (existing) | `nfs.csi.k8s.io` | Simple but single-point-of-failure unless backed by enterprise NAS. Fine for non-critical data (logs, build caches). Not recommended for databases. |
| HostPath | None (built-in) | Never use this in production. Data is local to one node, non-portable, lost on node failure. Only for testing. |

Key discovery question: "What shared storage is available to the K8s nodes? (vSAN, NFS, iSCSI SAN, nothing—just local disk)"

If the answer is "nothing," Longhorn is your escape hatch.

### Layer—Image Registry & Air-Gap

If the environment has no internet egress (or heavily filtered egress), every image your stack needs must be pre-loaded into a private registry.

Your image inventory (at minimum):

- Your application images
- ArgoCD images (controller, repo-server, redis, dex)
- Vault Secrets Operator / Vault Agent images
- Ingress controller images (nginx/traefik)
- MetalLB controller + speaker (if used)
- CSI driver images
- Any monitoring stack (Prometheus, Grafana, etc.)

Lightweight option: Stand up a simple [Harbor](https://goharbor.io/) instance inside the customer's network. Use `skopeo` or `crane` to copy images from public registries into Harbor ahead of deployment.

Enterprise option: If they already run a registry (Artifactory, Nexus, Harbor, or the vSphere Tanzu integrated registry), push to that.

Either way, your Helm charts need to support image override:

yaml

```yaml
# values-onprem.yaml
global:
  imageRegistry: customer-harbor.internal.corp:443
  imagePullSecrets:
    - name: harbor-creds
\`\`\`

If your charts don't currently support a \`global.imageRegistry\` override, that's a code change you need to make before any on-prem deployment.

---

## The Decision Matrix

This maps their answers directly to your technology choices:
\`\`\`
START
  │
  ├─ Customer has an EXISTING K8s platform? (Tanzu, OpenShift, Rancher)
  │   ├─ YES → Model A: Deploy onto their cluster
  │   │         • Get kubeconfig + namespace provisioning
  │   │         • Validate: K8s version, RBAC, StorageClass, Ingress, egress to Vault
  │   │         • ⚠️ If OpenShift: test manifests against SCCs before committing
  │   │         
  │   └─ NO → You must install K8s. Continue ↓
  │
  ├─ Customer runs vSphere 7u1+ with NSX-T?
  │   ├─ YES → Enterprise Path: VMware Tanzu (TKGs)
  │   │         • LB: NSX ALB (native)
  │   │         • Storage: vSphere CSI (native)
  │   │         • Registry: Tanzu integrated or Harbor
  │   │         • Cluster lifecycle: vSphere Supervisor
  │   │
  │   └─ NO (vSphere without NSX, or no vSphere) → Continue ↓
  │
  ├─ Customer can provide VMs (any hypervisor or bare metal)?
  │   ├─ YES → Lightweight Path: RKE2 + Rancher
  │   │         • LB: MetalLB (L2 or BGP)
  │   │         • Storage: Longhorn (if no SAN) or vSphere CSI / NFS CSI
  │   │         • Registry: Harbor
  │   │         • Cluster lifecycle: Rancher UI/API
  │   │         
  │   │         OR even lighter: K3s (single binary, same stack above)
  │   │
  │   └─ NO → 🚨 Escalate. What *can* they provide?
  │
  └─ Air-gapped?
      ├─ YES → Add: Harbor registry, image bundling pipeline, 
      │         offline Helm chart repos, air-gapped Rancher install
      └─ NO  → Standard pull-through / mirror config
```

---

## The Discovery Questionnaire

This is what you send to the customer. I've structured it so their infra team can fill it in without ambiguity:

---

> Subject: Infrastructure Discovery—Kubernetes Deployment Requirements
>
> To plan our deployment onto your infrastructure, we need to understand your environment. Could your infrastructure/platform team complete the following?
>
> ### 1\. Compute & Virtualisation
>
> - What hypervisor platform do you run? (VMware vSphere, Hyper-V, KVM, bare metal)
> - If VMware: what vSphere version and vCenter version?
> - If VMware: is VMware NSX-T deployed? What version?
> - Do you have an existing Kubernetes platform? (Tanzu, OpenShift, Rancher, other) If so, what version?
> - How are VMs provisioned? (self-service portal, Terraform, manual request/ticket)
> 
> ### 2\. Networking
>
> - What is the network topology for the environment we'd deploy into? (flat L2, VLAN-segmented, overlay/VXLAN)
> - Are IP addresses assigned via DHCP or statically?
> - What CIDR range(s) can be allocated for: Kubernetes node IPs, pod network, service network?
> - Is there a load balancer appliance available? (F5 BIG-IP, Citrix, NSX ALB, none)
> - What DNS infrastructure is used? What is the process for adding DNS records?
> - Are there firewalls between network segments? Is there a process for opening ports?
> 
> ### 3\. Storage
>
> - What shared storage is available? (VMware vSAN, NFS, iSCSI SAN with vendor name, none)
> - What capacity can be allocated for persistent application data?
> 
> ### 4\. Connectivity & Security
>
> - Does the environment have outbound internet access? If filtered, can we provide a whitelist of required endpoints?
> - Do you operate a private container image registry? (Harbor, Artifactory, Nexus, other)
> - What compliance or security frameworks apply? (CIS benchmarks, SOC 2, ISO 27001, specific hardening standards)
> - Is there a certificate authority (CA) we should use for TLS, or do you accept Let's Encrypt / self-signed for internal services?
> 
> ### 5\. Operational Model
>
> - Preferred model: Do you want to provide us with a managed Kubernetes cluster (you manage the platform, we deploy applications), or would you prefer we install and manage the Kubernetes platform on VMs you provide?
> - What is your patching/maintenance window cadence?
> - Who is the point of contact for infrastructure requests and escalations?

---

## Your Immediate Next Action

1. Open your email client.
2. Paste the questionnaire above into a new message to your customer contact.
3. Add a one-liner intro:_"Before we scope the on-prem deployment, we need to understand your infrastructure. Could your platform team fill in the attached questions? Happy to jump on a call to walk through them."_
4. Send it.

Everything else—technology selection, architecture decisions, manifest changes—is blocked until those answers come back. The questionnaire _is_ the critical path.
