---
aliases: []
confidence: 
created: 2025-03-10T11:07:42Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [calico, gitops, k8s, networking]
title: Calico Cloud vs Kubernetes Network Policies in GitOps
type: LLM
uid: 
updated: 
version: 
---

Standard Kubernetes Network Policies are a powerful way to control traffic flow at the pod level. They operate at layers 3 and 4 of the [[OSI Model]] (network and transport layers) and allow you to define rules based on:

-   Pod Selectors: Target specific pods based on labels.
-   Namespace Selectors: Target pods within specific namespaces.
-   IP Blocks: Allow or deny traffic to/from specific IP ranges (though generally discouraged within Kubernetes clusters for portability).
-   Port and Protocol: Specify ports and protocols (TCP, UDP, SCTP) for allowed traffic.
-   Ingress and Egress Rules: Control both incoming (ingress) and outgoing (egress) traffic.

Kubernetes Network Policies are implemented as a Kubernetes API object (`NetworkPolicy`) and are declarative, fitting perfectly into a GitOps workflow. You can define them in YAML files and manage them using tools like `kubectl`, Terraform, or Helm.

## Calico (Open Source) Enhancements to Kubernetes Network Policies

Calico, including the open-source version you likely have as your CNI in AKS, extends Kubernetes Network Policies in several significant ways, all still managed via Kubernetes API objects:

-   Calico NetworkPolicy API: Calico introduces its own `NetworkPolicy` API (`projectcalico.org/v3/NetworkPolicy`) which is a superset of the standard Kubernetes `networking.k8s.io/v1/NetworkPolicy`. This API offers enhanced features:
    -   Global Network Policies: Calico allows you to create `GlobalNetworkPolicy` objects that are not namespace-scoped and apply cluster-wide, useful for infrastructure-level policies.
    -   Policy Ordering and Precedence: Calico provides mechanisms to control the order in which policies are evaluated and their precedence, crucial for complex policy sets.
    -   Rule Actions (Pass, Log, Deny, Allow): Beyond simple allow/deny, Calico policies can `Pass` traffic to the next policy in the order or `Log` traffic for auditing purposes.
    -   Service Account Selectors: Target policies based on Kubernetes Service Accounts, offering another dimension of identity-based policy.
    -   Nested Selectors (NotSelectors): More complex selector logic, including negation (`not`).
    -   Layer 7 (Application Layer) Policies (with Calico Enterprise/Cloud): While open-source Calico operates at layers 3 and 4, Calico Enterprise and Cloud extend policies to layer 7 for HTTP/HTTPS traffic inspection and control (more on this below).
    -   DNS Policies: Control access based on DNS names.
-   Calico HostEndpoints: Calico allows you to apply policies directly to the Kubernetes host nodes themselves, not just pods, for securing host-level processes.
-   IP Pools and BGP Configuration: Calico manages IP address pools for pods and integrates with BGP for routing, offering more control over the underlying networking fabric, also configurable via Kubernetes API objects (`IPPool`, `BGPConfiguration`, etc.).

Crucially, all these open-source Calico enhancements are still managed through Kubernetes API objects (CRDs - Custom Resource Definitions installed by Calico). This means you can manage them declaratively and via GitOps using Terraform and Helm, just like standard Kubernetes resources.

## Calico Cloud-Specific Features and Considerations for GitOps

Calico Cloud builds upon open-source Calico and adds several enterprise-grade features, some of which do introduce aspects that are managed outside of pure Kubernetes API objects, although they often still integrate and can be managed in a GitOps fashion:

-   Centralized Management UI: Calico Cloud provides a web-based UI for visualizing, creating, and managing network policies. While convenient, direct UI configuration might bypass your GitOps workflow if not carefully managed. However, Calico Cloud typically offers mechanisms to export configurations as code.
-   Layer 7 Application Layer Policies (HTTP/HTTPS): Calico Cloud extends policy enforcement to layer 7, allowing you to inspect and filter HTTP/HTTPS traffic based on headers, methods, and paths. These policies are often configured through Calico Cloud's specific APIs or CRDs, which can be incorporated into GitOps.
-   Threat Detection and Prevention (Intrusion Detection/Prevention - IDS/IPS): Calico Cloud includes security features like IDS/IPS, which may involve configurations and rule sets managed outside of standard Kubernetes NetworkPolicy objects. However, these are often also declaratively configurable through Calico Cloud's APIs or CRDs.
-   Compliance and Auditing: Calico Cloud offers features for compliance reporting and audit logs, which might involve specific Calico Cloud APIs for querying and exporting data.
-   Service Graph Visualization: Calico Cloud can visualize network traffic flow in a service graph, which is primarily a monitoring and visualization feature and doesn't directly impact policy deployment via GitOps.
-   Dynamic Service and Workload Context: Calico Cloud can integrate with service meshes and workload metadata for more dynamic and context-aware policies. Configuration for these integrations might involve Calico Cloud specific settings or CRDs.

Does Calico Cloud do anything that can't be done with normal Kubernetes API objects?

-   Strictly speaking, no, at the Kubernetes API object level for layer 3/4 policies. Open-source Calico extends Kubernetes Network Policies using Kubernetes CRDs, which are still Kubernetes API objects. You can manage these with GitOps.
-   Yes, for Layer 7 and advanced security features. Calico Cloud's layer 7 policies and advanced security features (IDS/IPS, etc.) are extensions beyond standard Kubernetes Network Policies. While they often integrate with Kubernetes and can be managed declaratively, they are not part of the core `networking.k8s.io/v1/NetworkPolicy` API. Calico Cloud uses its own APIs and potentially CRDs to manage these advanced features.

GitOps and Calico Cloud

The key for GitOps with Calico Cloud is to:

1.  Prioritize Declarative Configuration: Whenever possible, favor declarative configuration over UI-driven configuration. Calico Cloud often provides APIs or CRDs to represent its features as code.
2.  Identify Calico Cloud CRDs: Understand which CRDs Calico Cloud installs for its extended features. These are your primary targets for GitOps management.
3.  Terraform and Helm Integration:
    -   Terraform: Terraform can manage Kubernetes resources, including CRDs. You can use the Kubernetes provider in Terraform to define Calico `NetworkPolicy`, `GlobalNetworkPolicy`, and potentially Calico Cloud-specific CRDs.
    -   Helm: If Calico Cloud provides Helm charts (or if you can create your own), you can use Helm to deploy and manage Calico Cloud components and their configurations, including CRDs and potentially some initial policy sets.
4.  Export and Version Control UI Configurations (If Necessary): If you use the Calico Cloud UI for initial policy creation or certain features, investigate if Calico Cloud allows you to export these configurations as YAML or JSON that you can then import into your GitOps repository and manage via Terraform or Helm going forward.
5.  Automate Policy Updates: Set up CI/CD pipelines to automatically apply changes to your network policy definitions whenever you update your GitOps repository.

In summary:

-   Open-source Calico enhances Kubernetes Network Policies using Kubernetes API objects (CRDs), making it fully GitOps-compatible with tools like Terraform and Helm.
-   Calico Cloud builds on this and adds layer 7 and advanced security features that are often managed via Calico Cloud's own APIs and potentially CRDs. While these are extensions, they are often also declaratively configurable and can be integrated into a GitOps workflow.
-   To maximize GitOps with Calico Cloud, focus on declarative configuration (CRDs, APIs), use Terraform and Helm to manage these configurations, and automate policy updates through CI/CD. Avoid relying solely on UI-driven configuration if you want a true GitOps approach.

By focusing on managing Calico and Calico Cloud configurations as code, you can maintain your GitOps principles while leveraging the enhanced networking and security features Calico Cloud offers. Remember to consult Calico Cloud's documentation for specific details on their APIs, CRDs, and GitOps best practices.
