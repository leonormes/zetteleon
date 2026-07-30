---
created: 2026-07-28T09:25:06+00:00
modified: 2026-07-28T09:29:45+00:00
permalink: llmeon/00-inbox/we-have-kubernetes-on-eks-and-aks.-the-versions-se
title: We have kubernetes on EKS and AKS. The versions se
type: note
---

## We Have Kubernetes on EKS and AKS. The Versions Seem to Refer to the k8s Version (1.33,1.34…) in both Azure and Aws. Are They Literaly the Same k8s Versions or Do Azure and Aws Modify Them? If Our Apps Run in the AKS Version Would that Mean They Will in Aws

I have enough to answer clearly and directly without needing a full report format for this technical question.

### Same Upstream Core, Different Wrapper

Both AKS and EKS run the unmodified upstream Kubernetes control plane binaries (kube-apiserver, kube-controller-manager, kube-scheduler, kubelet, etc.) for a given version number like 1.33 or 1.34—they don't fork or rewrite Kubernetes core logic. When AKS says "1.33.0" it means the actual open-source `kube-apiserver` v1.33.0, patched only for security/CVE fixes, same as EKS's v1.33.0 build. AWS actually builds and publishes its own patch set for each version as the "Amazon EKS Distro" (EKS-D), which applies small backport patches (e.g., STS client tweaks, IAM authenticator integration) on top of vanilla upstream Kubernetes, then rebuilds the same version tag. Azure does the same conceptually—AKS documents its own component versioning showing exactly which upstream Kubernetes version each control plane build tracks, with "breaking changes from Kubernetes X.Y.0" listed explicitly per release.[^1][^2][^3][^4][^5]

So the core API surface, resource semantics, and API groups for "Kubernetes 1.33" are the same across AKS, EKS, and GKE—this is enforced by the CNCF Kubernetes Conformance Program, which both cloud vendors' managed offerings are certified against. That conformance certification is precisely what guarantees your workloads should behave identically at the raw API level.[^6]

### Where the Real Divergence Happens

The version number is the same, but everything around that core is provider-specific and this is where compatibility issues actually arise:

- Cloud controller/provider components: AKS ships `cloud-provider-node-manager` and Azure CNI/Cilium networking layers built specifically for Azure; EKS ships the AWS VPC CNI and its own cloud-controller-manager—these are not interchangeable and your networking manifests (NetworkPolicies, LoadBalancer services, ingress annotations) will need provider-specific config.[^4][^1]
- Add-ons and defaults: AKS bundles Azure-specific add-ons (Azure Policy/Gatekeeper, Azure Monitor, Secrets Store CSI with Azure Key Vault provider, Cilium/Retina networking stack) that don't exist on EKS at all. EKS has its own equivalents (AWS Load Balancer Controller, EBS/EFS CSI drivers, IAM Roles for Service Accounts).[^1]
- Storage classes: `managed-csi` (Azure Disk) vs `gp2`/`gp3` (EBS)—any PVC referencing a StorageClass by name will fail on the other cloud.
- Node OS/image and container runtime versions: AKS uses specific Ubuntu 22.04 or Azure Linux 3.0 builds with pinned containerd/runc versions; EKS uses Amazon Linux 2023/Bottlerocket with its own pinned runtime versions. Kernel-level behavior (e.g., cgroup v2 handling, sysctl defaults) can differ subtly.[^3][^1]
- IAM/identity integration: Azure AD Workload Identity vs AWS IAM Roles for Service Accounts (IRSA)—any manifest tied to identity/RBAC bindings for cloud resource access is not portable as-is.
- Ingress controllers and DNS: default ingress class names, cert-manager integration patterns, and external-dns provider configs differ.

### Practical Answer to Your Question

If your apps run cleanly on AKS 1.33/1.34 and use no Azure-specific resources (no Azure-only StorageClasses, no Azure CNI-specific NetworkPolicy features, no Azure AD-bound ServiceAccounts, no Azure Monitor sidecar dependencies), then yes—they will very likely run on EKS at the same Kubernetes version, because the core API behavior is conformant and identical. This is the entire premise behind portable Kubernetes-native apps and tools like Helm charts designed to be cloud-agnostic.[^5][^6]

However, in practice almost every real-world AKS deployment has at least a few Azure-coupled dependencies (StorageClass names, LoadBalancer service annotations, identity bindings, CSI drivers). The safest verification approach:

1. Audit your manifests for any `storageClassName`, ingress/service `annotations`, and CSI driver references—grep for `azure`, `disk.csi`, `file.csi`.
2. Check for Azure Workload Identity or pod-managed identity annotations on ServiceAccounts.
3. Run `kubectl api-resources` on both a test AKS and EKS cluster at the same version and diff the output—this reveals any provider-injected CRDs/APIs your app might implicitly depend on.
4. Test in a real EKS cluster at the matching version (1.33.x or 1.34.x) before assuming portability—conformance guarantees the core API works, but it doesn't guarantee your specific manifest has no cloud-specific references baked in.

```bash
# Quick audit for Azure-coupled resources in your manifests
grep -rEi "storageClassName|azure|disk\.csi|file\.csi|workload\.identity|azure\.com" ./k8s-manifests/
```

<span style="display:none">[^7][^8][^9][^10][^11][^12][^13][^14][^15]</span>

<div align="center">⁂</div>

[^1]: <https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions>
[^2]: <https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions-extended.html>
[^3]: <https://distro.eks.amazonaws.com/releases/1-21/7/CHANGELOG-v1-21-eks-7/>
[^4]: <https://docs.azure.cn/en-us/aks/aks-component-versioning>
[^5]: <https://stackoverflow.com/questions/68135823/is-the-kubernetes-version-and-aks-distributed-kubernetes-version-the-same>
[^6]: <https://securityboulevard.com/2020/02/eks-vs-gke-vs-aks-evaluating-kubernetes-in-the-cloud/>
[^7]: <https://komodor.com/learn/aks-version-what-k8s-version-is-supported-and-how-to-upgrade-your-clusters/>
[^8]: <https://securityboulevard.com/2020/08/eks-vs-gke-vs-aks-august-2020-update/>
[^9]: <https://www.pjlewis.com/posts/best-practices-for-upgrading-updating-your-aks-clusters/>
[^10]: <https://cloud.google.com/kubernetes-engine/enterprise/docs/version-and-upgrade-support?hl=fr>
[^11]: <https://learn.microsoft.com/en-us/answers/questions/5497149/aks-cluster-upgrade-assistance-(auto-upgrade)>
[^12]: <https://aws.amazon.com/blogs/containers/planning-kubernetes-upgrades-with-amazon-eks/>
[^13]: <https://blog.csdn.net/Rong_Toa/article/details/120250673>
[^14]: <https://anywhere.eks.amazonaws.com/docs/whatsnew/changelog/>
[^15]: <https://www.devopsschool.com/blog/kubernetes-as-a-service-with-comparison-of-eks-vs-aks-vs-gke/>
