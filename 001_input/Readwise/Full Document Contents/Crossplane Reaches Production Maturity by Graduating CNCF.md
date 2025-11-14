# Crossplane Reaches Production Maturity by Graduating CNCF

![rw-book-cover](https://res.infoq.com/news/2025/11/crossplane-grad/en/headerimage/generatedHeaderImage-1762893661689.jpg)

## Metadata
- Author: [[Matt Foster]]
- Full Title: Crossplane Reaches Production Maturity by Graduating CNCF
- Category: #articles
- Summary: Crossplane has graduated from the CNCF, showing it is stable and ready for production use. It helps teams manage cloud infrastructure using Kubernetes and supports multi-cloud environments. Many big companies use Crossplane to simplify and automate their cloud operations.
- URL: https://www.infoq.com/news/2025/11/crossplane-grad/

## Full Document
The Cloud Native Computing Foundation (CNCF) has [graduated Crossplane](https://blog.crossplane.io/crossplane-cncf-graduation/), marking a major milestone for the open-source project that turns Kubernetes into a universal control plane for cloud infrastructure.

Graduation is [reserved for projects](https://www.cncf.io/projects/) that have reached operational maturity, wide adoption, and a strong governance model. For practitioners, it signals that Crossplane is no longer an experimental idea but a production-hardened foundation for building internal platforms, offering self-service APIs, and managing multi-cloud environments with a Kubernetes-native approach.

Originally created by [Upbound](https://www.upbound.io/) in 2018 and [donated](https://www.cncf.io/blog/2021/09/14/crossplane-moves-from-sandbox-to-cncf-incubator) to the CNCF in 2020, Crossplane has moved through Sandbox and Incubating stages to reach Graduation. It now counts more than [3,000 contributors across 450 companies](https://finance.yahoo.com/news/cloud-native-computing-foundation-announces-160000508.html) and has passed a security audit under a vendor-neutral governance model. The ecosystem has [expanded](https://blog.crossplane.io/community-ecosystem) from a handful of cloud providers into a marketplace of official and community-maintained packages covering major hyperscalers as well as services like Helm, Vault, and Kubernetes add-ons.

Enterprise adoption reflects that momentum. Public users include Nike, Autodesk, NASA Science Cloud, Elastic, SAP, IBM, and Nokia. The [dominant pattern](https://blog.upbound.io/why-crossplane-is-the-ideal-engine-for-internal-developer-platforms) is using Crossplane as the backbone of an internal developer platform. Platform teams expose custom APIs such as Environment, Application, or DatabaseService, while compositions handle provisioning, networking, security controls, and backups. Developers get self-service infrastructure; the organisation gets standardized configuration and policy enforcement without manual review or tickets. [Some companies](https://medium.com/%40walaaelgenidy/crossplane-the-multicloud-control-plane-for-the-modern-enterprise-episode-1-ecdfe5d02c4e) have adopted Crossplane for multi-cloud control planes, managing AWS, Azure, and GCP resources from a single Kubernetes cluster.

Crossplane extends the Kubernetes API so infrastructure can be described and managed the same way teams handle workloads. When a provider for AWS, Azure, GCP or another platform is installed, it adds custom resource types for services like VPCs, databases, buckets, or Kubernetes clusters. Platform engineers then define higher-level abstractions using Composite Resource Definitions (XRDs) and Compositions, embedding security policies and configuration defaults into reusable APIs.

From a developer’s perspective, requesting a Database becomes as simple as applying a Kubernetes manifest. Crossplane’s controllers handle provisioning and [continuously reconcile](http://blog.upbound.io/crossplane-differentiators) the underlying cloud resources, keeping configuration in Kubernetes rather than a state file. This removes the need to run plan/apply and automatically corrects drift, which has made Crossplane attractive to teams standardizing on Kubernetes and GitOps workflows.

Crossplane inevitably invites comparison to [Terraform](https://developer.hashicorp.com/terraform), [Pulumi](https://www.pulumi.com/), and [AWS CDK](https://aws.amazon.com/cdk/). Terraform remains popular for its ecosystem and simple setup: a single binary, a CLI workflow, and a mature [library of modules](http://registry.terraform.io). But is limited to reconcilng changes only when a user runs apply. Pulumi and CDK emphasize infrastructure as real programming languages, while Crossplane treats infrastructure as Kubernetes resources controlled by operators and policy. In practice, many teams [use both](https://blog.crossplane.io/crossplane-vs-terraform/): Crossplane can run Terraform modules through provider-terraform, letting organizations reuse existing code while adopting a Kubernetes-native control plane.

But Crossplane is not free of friction: Early adopters [reported](https://blog.crossplane.io/faq-1-composition-not-working) a steep learning curve and [debugging challenges](https://www.reddit.com/r/kubernetes/comments/1mqc5cw/crossplane_20_is_out) when compositions or providers misbehaved. Enterprises can also choose to pair the open-source Crossplane with vendor support or a UI layer to [simplify](https://blog.upbound.io/crossplane-graduates-from-cncf-upbound-redefines-ai-native-infrastructure) day-to-day operations.

With graduation, maintainers are [focusing](https://www.cncf.io/announcements/2025/11/06/cloud-native-computing-foundation-announces-graduation-of-crossplane/) on improved observability, faster reconciliation, and a richer ecosystem of configuration packages.
