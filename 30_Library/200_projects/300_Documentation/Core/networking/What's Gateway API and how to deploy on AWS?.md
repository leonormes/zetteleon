---
aliases: []
author: ["[[DEV Community]]"]
confidence: 
created: 2025-03-27T09:44:02Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source: https://dev.to/haintkit/whats-gateway-api-and-how-to-deploy-on-aws-3ma1
source_of_truth: []
status: 
tags: [gateway, k8s, networking]
title: "What's Gateway API and how to deploy on AWS?"
type: download
uid: 
updated: 
version: 
---

Co-author: [@coangha21](https://dev.to/coangha21)

Gateway API is recently standing out to be a promising project that will change the way we manage traffic in Kubernetes. It is looking forward to being the next generation of APIs used for Ingress, Load Balancing, and Service Mesh functionalities. In today's blog, we will discuss what Gateway API is, what it offers and finally we will get our hands dirty to gain better understanding of the service. Let’s get started.

**Gateway API overview**
The Gateway API is a recently graduated (version 1.0 in October 2023) official Kubernetes project that aims to revolutionize L4 and L7 traffic routing within Kubernetes. The goal is to simplify and standardize the way ingress and load balancing are configured and managed, addressing limitations of existing solutions like Ingress and Service APIs.

[![Gateway API logo](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F3cv3xwtuanmaiexbc2wd.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F3cv3xwtuanmaiexbc2wd.png)

You can see above Gateway API logo, it already speak for it self, it illustrates the dual purpose of this API, enabling routing for both North-South (Ingress) and East-West (Mesh) traffic to share the same configuration.

Now, let’s take a look at some of the key features that Gateway API offers:

***1\. Extensible and Role-oriented:***

- Unlike the single-purpose Ingress controller, Gateway API is designed with flexibility and specialization in mind.
- It offers various resource types like Gateway, GatewayClass, HTTPRoute, GRPCRoute, and Policy that work together to define specific roles and capabilities for different networking tasks.
- This allows for building sophisticated networking configurations with greater control and clarity.

[![Gateway API is aiming for RBAC](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fcaew00ny3k3w0j7dpwpn.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fcaew00ny3k3w0j7dpwpn.png)

***2\. Advanced Traffic Routing:***

- Gateway API goes beyond simple load balancing and provides powerful routing capabilities based on HTTP routing rules, path matching, headers, and even gRPC service names.
- This facilitates setting up complex traffic destinations, traffic splitting, and A/B testing scenarios.

[![Gateway API supports advance routing](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fxr7c0k8fvvrqztt62ffv.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fxr7c0k8fvvrqztt62ffv.png)

***3\. Protocol-Aware and Scalable:***

- The API supports both L4 (TCP/UDP) and L7 (HTTP/gRPC) protocols, offering a unified platform for all your networking needs.
- Additionally, it's designed for scalability and performance to handle large workloads and complex network topologies.

***4\. Community-Driven and Evolving:***

- Gateway API is a community-driven project under the Kubernetes SIG Network, actively maintained and constantly evolving.
- New features and capabilities are being added regularly, making it a future-proof solution for your Kubernetes networking needs.

From my point of view, Gateway API represents a significant leap forward in Kubernetes service networking. Its dynamic capabilities, flexible routing, and robust policy tools will empower developers and operators to manage external traffic with greater control, precision, and agility. If you have time, try it yourself, it will be “worth your time”.

**What is the differences between Gateway API and Ingress?**
While both Gateway API and Ingress manage traffic routing in Kubernetes, there are several key differences between the Gateway API and the traditional Ingress API, let’s go through some of them:
**Functionality:**

- **Ingress**: Primarily focused on exposing HTTP applications with a straightforward, declarative syntax.
- **Gateway API**: A more general API for proxying traffic, supporting various protocols like HTTP, gRPC, and even different backend targets like buckets or functions.

**Flexibility:**

- **Ingress**: Limited configuration options with heavy reliance on annotations for advanced features.
- **Gateway API**: More fine-grained control with dedicated objects for defining routes, listeners, and backends, promoting cleaner configuration and extensibility.

**Protocol Support:**

- **Ingress**: Only supports HTTP.
- **Gateway API**: Supports multiple protocols beyond HTTP, like gRPC and WebSockets.

[![Ingress support gRPC protocol](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fwubfdv1f8pve1jxz1bxv.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fwubfdv1f8pve1jxz1bxv.png)

**Scalability:**

- **Ingress:** Can become complex to scale, often requiring external load balancers or intricate configurations.
- **Gateway API:** Designed with scalability in mind, easily integrating with various data plane implementations.

**Security:**

- **Ingress:** Limited built-in security features, primarily relying on annotations for authentication and authorization.
- **Gateway API:** Supports extensions for implementing enhanced security features like authentication and authorization.

[![Ingress vs Gateway API](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fynb30534qo87901qj5ck.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fynb30534qo87901qj5ck.png)

**Other Differences:**

- **Portability:** Gateway API configurations are more portable across data planes due to its separation of concerns.
- **Management:** Gateway API allows for better cluster operator control with dedicated objects for managing various components.
- **Maturity:** Ingress is a stable, GA (General Availability) API, while Gateway API is still under development but rapidly gaining traction.

In summary, Ingress is a basic but mature solution for exposing simple HTTP applications in Kubernetes. Gateway API is a more powerful and flexible API that caters to diverse use cases, supports broader protocols, and scales more efficiently. It offers greater control and extensibility at the cost of slightly increased complexity.

"Which one should I choose?", it depends on your use case:

- For Ingress: If you need a simple solution for exposing an HTTP application and don't require advanced features.
- For Gateway API: If you need flexibility for various protocols, backends, or require extensibility for security or advanced routing features.

**Please keep in mind that, Gateway API is not meant to replace Ingress entirely, but rather provide a more comprehensive and future-proof option for complex traffic routing needs in Kubernetes.**

**How to deploy Gateway API on AWS EKS**
Finally, this is probably the part you are waiting for. Let’s deploy a Gateway API on our AWS EKS cluster. I will only show high-level steps that need to be done. For manifest deployment, please refer to [this repository](https://github.com/haicasgox/demo-gatewayapi.git).

Architecture demo: we have 02 services (user and post). We use the picture of VPC Lattice and Gateway API for your mapping overview.

You can see in the picture that the Gateway API is composed of three main components: GatewayClass(Controller), Gateway, HTTPRoute/GRPCRoute, each of them is related to VPC Lattice objects.

**How it works**
The AWS Gateway API controller (GatewayClass) integrates VPC Lattice with the Kubernetes Gateway API. When installed in your cluster, the controller watches for the creation of Gateway API resources such as gateways, routes, and provisions corresponding Amazon VPC Lattice objects. This enables users to configure VPC Lattice Service Networks using Kubernetes APIs, without needing to write custom code or manage sidecar proxies. The AWS Gateway API Controller is an open-source project and is fully supported by AWS team.

Now let’s go through step by step to set this up on our EKS cluster.

**Step by step guide:**

- **Create GatewayClass:**
	First we need to create a GatewayClass (Gateway API controller), we will using AWS Gateway API controller. Before you create the GatewayClass, you need to setup 2 following things:
- Setup security groups to allow all Pods communicating with VPC Lattice to allow traffic from the VPC Lattice managed prefix lists.
- Create IRSA for Gateway API Controller.
	For those steps, please refer to [this link](https://www.gateway-api-controller.eks.aws.dev/guides/deploy/#using-eks-cluster).

After all of that is done, we will create our first GatewayClass. You can find all manifests used in this demo [here](https://github.com/haicasgox/demo-gatewayapi.git).

The outcome should be look like this:

[![Image description](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ffbiy2or64xxnpfjwwj0j.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ffbiy2or64xxnpfjwwj0j.png)

- **Service networks (Gateway):**Next, we will create a Gateway. Gateway describes how traffic can be translated to Services within the cluster (through Load Balancer, in-cluster proxy, external hardware, etc.). In AWS, Gateway points to a [VPC Lattice service network](https://docs.aws.amazon.com/vpc-lattice/latest/ug/service-networks.html). Services associated with the service network can be authorized for discovery, connectivity, accessibility, and observability.

[![Image description](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fzwnughlmvw3xcbvo8rqx.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fzwnughlmvw3xcbvo8rqx.png)

- **Services and HTTPRoute:**Finally, we will define Services and Routes using K8s object Service and HTTPRoute to start routing traffic between services.

Service: User

[![Service: User](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fhmmkdrp16zf0fba5skyp.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fhmmkdrp16zf0fba5skyp.png)

Service: Post

[![Service: Post](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fa64plcbhouzde7xp981x.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fa64plcbhouzde7xp981x.png)

Target groups for 02 services:

[![Target groups for 02 services post and user](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fj2so8kvawrwat8yoyngy.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fj2so8kvawrwat8yoyngy.png)

- **Result:**Now let’s check if service “post” can called service “user” via domain name in VPC Lattice and vice versa.

[![Service post calls service user via DNS provided by AWS Lattice](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F4wsy2nz57wrczsid1t23.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F4wsy2nz57wrczsid1t23.png)

[![Service user calls service post via DNS provided by AWS Lattice](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fb079a8gcy5cobf4xxmsn.png)](https://media2.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fb079a8gcy5cobf4xxmsn.png)

It's worked!

**Conclusion**
Even though Gateway API is new and on it way to accomplish, it’s already showing lots of potentials. With more features and improvement coming in the future, we can expect it to be the future of APIs used for Ingress, Load Balancing, and Service Mesh functionalities.

References:

1. [Introduction - Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/)
2. [AWS Gateway API Controller](https://www.gateway-api-controller.eks.aws.dev/)
