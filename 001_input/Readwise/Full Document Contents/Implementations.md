---
aliases: []
confidence: 
created: 2025-11-22T08:22:16Z
epistemic: 
last_reviewed: 
modified: 2025-11-22T14:29:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [articles, development, service-mesh]
title: Implementations
type: 
uid: 
updated: 
---

## Implementations

![rw-book-cover](https://gateway-api.sigs.k8s.io/images/k8s-favicon.png)

### Metadata
- Author: [[k8s.io]]
- Full Title: Implementations
- Category: #articles
- Summary: Many implementations and projects provide Gateway API support for Kubernetes, including cloud providers (EKS, GKE), service meshes (Istio, Cilium, Kuma), and gateways/ingress controllers (Envoy Gateway, Contour, Traefik, Kong, NGINX, APISIX, HAProxy, LiteSpeed, BIG-IP, STUNner, Emissary, Gloo Edge). Support levels vary by project and Gateway API version, with some fully conformant and others partially implemented or in progress. Integrations like Flagger, cert-manager, and Argo Rollouts add canary, TLS, and deployment features for Gateway-managed traffic.
- URL: <https://gateway-api.sigs.k8s.io/implementations/>

### Full Document
#### Amazon Elastic Kubernetes Service

[Amazon Elastic Kubernetes Service (EKS)](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html) is a managed service that you can use to run Kubernetes on AWS without needing to install, operate, and maintain your own Kubernetes control plane or nodes. EKS's implementation of the Gateway API is through [AWS Gateway API Controller](https://github.com/aws/aws-application-networking-k8s) which provisions [Amazon VPC Lattice](https://aws.amazon.com/vpc/lattice/) Resources for gateway(s), HTTPRoute(s) in EKS clusters.

#### APISIX[¶](https://gateway-api.sigs.k8s.io/implementations/#apisix)

[Apache APISIX](https://apisix.apache.org/) is a dynamic, real-time, high-performance API Gateway. APISIX provides rich traffic management features such as load balancing, dynamic upstream, canary release, circuit breaking, authentication, observability, and more.

APISIX currently supports Gateway API `v1alpha2` version of the specification for its [Apache APISIX Ingress Controller](https://github.com/apache/apisix-ingress-controller).

#### BIG-IP Kubernetes Gateway

[BIG-IP Kubernetes Gateway](https://gateway-api.f5se.io/) is an open-source project that provides an implementation of the Gateway API using [F5 BIG-IP](https://f5.com) as the data plane. It provides enterprises with high-performance Gateway API implementation.

We are actively supporting various features of the Gateway API. For compatibility with the features of the Gateway API, please refer to [here](https://github.com/f5devcentral/bigip-kubernetes-gateway/blob/master/docs/gateway-api-compatibility.md). For any questions about this project, welcome to create [Issues](https://github.com/f5devcentral/bigip-kubernetes-gateway/issues) or [PR](https://github.com/f5devcentral/bigip-kubernetes-gateway/pulls). Also, you are welcome to connect with us in the [slack channel](https://gateway-api.f5se.io/Support-and-contact/).

#### Cilium

[Cilium](https://cilium.io) is an eBPF-based networking, observability and security solution for Kubernetes and other networking environments. It includes [Cilium Service Mesh](https://docs.cilium.io/en/stable/gettingstarted/#service-mesh), a highly efficient mesh data plane that can be run in [sidecarless mode](https://isovalent.com/blog/post/cilium-service-mesh/) to dramatically improve performance, and avoid the operational complexity of sidecars. Cilium also supports the sidecar proxy model, offering choice to users. As of [Cilium 1.13](https://isovalent.com/blog/post/cilium-release-113/), Cilium supports Gateway API, passing conformance for v0.5.1.

Cilium is open source and is a CNCF incubation project.

If you have questions about Cilium Service Mesh the #service-mesh channel on [Cilium Slack](https://cilium.io/slack) is a good place to start. For contributing to the development effort, check out the #development channel or join our [weekly developer meeting](https://github.com/cilium/cilium#weekly-developer-meeting).

#### Contour

[Contour](https://projectcontour.io) is a CNCF open source Envoy-based ingress controller for Kubernetes.

Contour implements Gateway API v0.5.1, supporting the v1alpha2 and v1beta1 API versions. All [Standard channel](https://gateway-api.sigs.k8s.io/concepts/versioning/#release-channels-eg-experimental-standard) resources (GatewayClass, Gateway, HTTPRoute), plus ReferenceGrant and TLSRoute, are supported. Contour's implementation passes all Gateway API conformance tests included in the v0.5.1 release.

See the [Contour Gateway API Guide](https://projectcontour.io/guides/gateway-api/) for information on how to deploy and use Contour's Gateway API implementation.

For help and support with Contour's implementation, [create an issue](https://github.com/projectcontour/contour/issues/new/choose) or ask for help in the [#contour channel on Kubernetes slack](https://kubernetes.slack.com/archives/C8XRH2R4J).

*Some "extended" functionality is not implemented yet, [contributions welcome!](https://github.com/projectcontour/contour/blob/main/CONTRIBUTING.md).*

#### Emissary-Ingress (Ambassador API Gateway)

[Emissary-Ingress](https://www.getambassador.io/docs/edge-stack) (formerly known as Ambassador API Gateway) is an open source CNCF project that provides an ingress controller and API gateway for Kubernetes built on top of [Envoy Proxy](https://envoyproxy.io). See [here](https://www.getambassador.io/docs/edge-stack/latest/topics/using/gateway-api/) for more details on using the Gateway API with Emissary.

#### Envoy Gateway

[Envoy Gateway](https://gateway.envoyproxy.io/) is an [Envoy](https://github.com/envoyproxy) subproject for managing Envoy-based application gateways. The supported APIs and fields of the Gateway API are outlined [here](https://gateway.envoyproxy.io/v0.4.0/design/gatewayapi-support.html). Use the [quickstart](https://gateway.envoyproxy.io/v0.4.0/user/quickstart.html) to get Envoy Gateway running with Gateway API in a few simple steps.

#### Flomesh Service Mesh (FSM)

[Flomesh Service Mesh](https://github.com/flomesh-io/fsm) is a community driven Kubernetes North-South traffic manager, and provides an implementation of Ingress controller, Gateway API, Load Balancer, and cross-cluster service registration and service discovery.

The [Flomesh.io](https://flomesh.io) team is actively working towards an implementation of the Gateway API. You can track progress of this implementation [here](https://github.com/flomesh-io/fsm/issues/18).

#### Gloo Edge

Gloo Edge 2.0 is an Istio-native, fully-featured Envoy based API gateway that brings [Gloo Edge](https://docs.solo.io/gloo-edge/) functionality to Istio. The [Solo.io](https://www.solo.io) team is actively working towards an implementation of the Gateway API.

#### Google Kubernetes Engine

[Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) is a managed Kubernetes platform offered by Google Cloud. GKE's implementation of the Gateway API is through the [GKE Gateway controller](https://cloud.google.com/kubernetes-engine/docs/concepts/gateway-api) which provisions Google Cloud Load Balancers for Pods in GKE clusters.

The GKE Gateway controller supports weighted traffic splitting, mirroring, advanced routing, multi-cluster load balancing and more. See the docs to deploy [private or public Gateways](https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-gateways) and also [multi-cluster Gateways](https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-multi-cluster-gateways).

#### HAProxy Ingress

[HAProxy Ingress](https://haproxy-ingress.github.io/) is a community driven ingress controller implementation for HAProxy.

HAProxy Ingress v0.13 partially supports the Gateway API's v1alpha1 specification. See the [controller's Gateway API documentation](https://haproxy-ingress.github.io/docs/configuration/gateway-api/) to get informed about conformance and roadmap.

#### HashiCorp Consul

[Consul](https://consul.io), by [HashiCorp](https://www.hashicorp.com), is an open source control plane for multi-cloud networking. A single Consul deployment can span bare metal, VM and container environments.

Consul service mesh works on any Kubernetes distribution, connects multiple clusters, and Consul CRDs provide a Kubernetes native workflow to manage traffic patterns and permissions in the mesh. [Consul API Gateway](https://www.consul.io/docs/api-gateway) supports Gatewway API for managing North-South traffic.

Please see the [Consul API Gateway documentation](https://www.consul.io/docs/api-gateway) for current infomation on the supported version and features of the Gateway API.

#### Istio

[Istio](https://istio.io) is an open source [service mesh](https://istio.io/latest/docs/concepts/what-is-istio/#what-is-a-service-mesh) and gateway implementation.

A light-weight minimal install of Istio can be used to provide a Beta-quality implementation of the Kubernetes Gateway API for cluster ingress traffic control. For service mesh users, the Istio implementation also lets you start trying out the experimental Gateway API [support for east-west traffic management](https://gateway-api.sigs.k8s.io/contributing/gamma/) within the mesh.

Much of Istio's documentation, including all of the [ingress tasks](https://istio.io/latest/docs/tasks/traffic-management/ingress/) and several mesh-internal traffic management tasks, already includes parallel instructions for configuring traffic using either the Gateway API or the Istio configuration API. Check out the [Gateway API task](https://istio.io/latest/docs/tasks/traffic-management/ingress/gateway-api/) for more information about the Gateway API implementation in Istio.

#### Kong

[Kong](https://konghq.com) is an open source API Gateway built for hybrid and multi-cloud environments.

Kong supports Gateway API in the [Kong Kubernetes Ingress Controller (KIC)](https://github.com/kong/kubernetes-ingress-controller), see the [Gateway API Guide](https://docs.konghq.com/kubernetes-ingress-controller/latest/guides/using-gateway-api/) for usage information.

Kong also supports Gateway API in the [Kong Gateway Operator](https://github.com/kong/gateway-operator-docs).

For help and support with Kong's implementations please feel free to [create an issue](https://github.com/Kong/kubernetes-ingress-controller/issues/new) or a [discussion](https://github.com/Kong/kubernetes-ingress-controller/discussions/new). You can also ask for help in the [#kong channel on Kubernetes slack](https://kubernetes.slack.com/archives/CDCA87FRD).

#### Kuma

[Kuma](https://kuma.io) is an open source service mesh.

Kuma is actively working on an implementation of Gateway API specification for the Kuma builtin Gateway. Check the [Gateway API Documentation](https://kuma.io/docs/latest/explore/gateway-api/) for information on how to setup a Kuma builtin gateway using the Gateway API.

#### LiteSpeed Ingress Controller

The [LiteSpeed Ingress Controller](https://litespeedtech.com/products/litespeed-web-adc/features/litespeed-ingress-controller) uses the LiteSpeed WebADC controller to operate as an Ingress Controller and Load Balancer to manage your traffic on your Kubernetes cluster. It implements the full core Gateway API including Gateway, GatewayClass, HTTPRoute and ReferenceGrant and the Gateway functions of cert-manager. Gateway is fully integrated into the LiteSpeed Ingress Controller.

- [Product documentation](https://docs.litespeedtech.com/cloud/kubernetes/).
- [Gateway specific documentation](https://docs.litespeedtech.com/cloud/kubernetes/gateway).
- Full support is available on the [LiteSpeed support web site](https://www.litespeedtech.com/support).

#### NGINX Kubernetes Gateway

[NGINX Kubernetes Gateway](https://github.com/nginxinc/nginx-kubernetes-gateway) is an open-source project that provides an implementation of the Gateway API using [NGINX](https://nginx.org/) as the data plane. The goal of this project is to implement the core Gateway API -- Gateway, GatewayClass, HTTPRoute, TCPRoute, TLSRoute, and UDPRoute -- to configure an HTTP or TCP/UDP load balancer, reverse-proxy, or API gateway for applications running on Kubernetes. NGINX Kubernetes Gateway is currently under development and supports a subset of the Gateway API.

If you have any suggestions or experience issues with NGINX Kubernetes Gateway, please [create an issue](https://github.com/nginxinc/nginx-kubernetes-gateway/issues/new) or a [discussion](https://github.com/nginxinc/nginx-kubernetes-gateway/discussions/new) on GitHub. You can also ask for help in the [#nginx-kubernetes-gateway channel on NGINX slack](https://nginxcommunity.slack.com/channels/nginx-kubernetes-gateway).

#### STUNner

[STUNner](https://github.com/l7mp/stunner) is an open source cloud-native WebRTC media gateway for Kubernetes. STUNner is purposed specifically to facilitate the seamless ingestion of WebRTC media streams into a Kubernetes cluster, with simplified NAT traversal and dynamic media routing. Meanwhile, STUNner provides improved security and monitoring for large-scale real-time communications services. The STUNner dataplane exposes a standards compliant TURN service to WebRTC clients, while the control plane supports a subset of the Gateway API.

STUNner currently supports version `v1alpha2` of the Gateway API specification. Check the [install guide](https://github.com/l7mp/stunner/blob/main/doc/INSTALL.md) for information on how to deploy and use STUNner for WebRTC media ingestion. Please direct all questions, comments and bug-reports related to STUNner to the [STUNner project](https://github.com/l7mp/stunner).

#### Traefik

[Traefik](https://traefik.io) is an open source cloud-native application proxy.

Traefik currently supports version `v1alpha2` (`v0.4.x`) of the Gateway API specification, check the [Kubernetes Gateway Documentation](https://doc.traefik.io/traefik/routing/providers/kubernetes-gateway/) for information on how to deploy and use Traefik's Gateway implementation.

Traefik is currently working on implementing UDP, and ReferenceGrant. Status updates and documentation will be provided here as the work progresses.

### Integrations

In this section you will find specific links to blog posts, documentation and other Gateway API references for specific integrations.

#### Flagger

[Flagger](https://flagger.app) is a progressive delivery tool that automates the release process for applications running on Kubernetes.

Flagger can be used to automate canary deployments and A/B testing using Gateway API. It currently supports the `v1alpha2` spec of Gateway API. You can refer to [this tutorial](https://docs.flagger.app/tutorials/gatewayapi-progressive-delivery) to use Flagger with any implementation of Gateway API.

#### Cert-manager

[cert-manager](https://cert-manager.io/) is a tool to automate certificate management in cloud native environments.

cert-manager can generate TLS certificates for Gateway resources. This is configured by adding annotations to a Gateway. It currently supports the `v1alpha2` spec of Gateway API. You can refer to the [cert-manager docs](https://cert-manager.io/docs/usage/gateway/) to try it out.

#### Argo Rollouts

[Argo Rollouts](https://argo-rollouts.readthedocs.io/en/stable/) is a progressive delivery controller for Kubernetes. It supports several advanced deployment methods such as blue/green and canaries. Argo Rollouts supports the Gateway API via [a plugin](https://github.com/argoproj-labs/rollouts-gatewayapi-trafficrouter-plugin/).
