---
aliases: []
confidence: ""
created: 2025-12-24T21:52:29Z
epistemic: ""
last_reviewed: ""
modified: 2025-12-25T18:35:31Z
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: [articles]
title: Learn about Cilium with interactive courses
type: link
uid: 
updated: 
---

## Learn about Cilium with Interactive Courses

![rw-book-cover](https://cilium.io/images/social-preview.jpg)

### Metadata

- Author: [[cilium.io]]
- Full Title: Learn about Cilium with interactive courses
- Category: #articles
- Summary: Cilium offers interactive labs that teach its networking, security, and observability features. The courses cover topics like BGP, Gateway API, IPv6, egress, Envoy L7 proxy, and Cluster Mesh. Labs show how Cilium uses eBPF to simplify Kubernetes networking and security across clusters and on-prem networks.
- URL: <https://cilium.io/labs/>

### Full Document

Deep dive into Cilium and its features with labs provided by companies within the Cilium ecosystem

[All labs](https://cilium.io/labs/)[Getting Started](https://cilium.io/labs/categories/getting-started/)[Security](https://cilium.io/labs/categories/security/)

[NetworkingFrom **Isovalent**#### Advanced BGP Features

BGP support was initially introduced in Cilium 1.10 and subsequent improvements have been made since, such as the recent introduction of IPv6 support in Cilium 1.12 and Service IP Advertisements in Cilium 1.13. Improvements are continuing in Cilium 1.14 with the introduction of BGP timers, eBGP multihop and BGP Graceful restart! In this lab, the user will learn about both these new features and how they can simplify their network connectivity operations.](<https://isovalent.com/labs/advanced-bgp-features/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### Advanced Gateway API Use Cases

This lab is a follow-up to the introductory Cilium Gateway API lab. We highly recommend you do the Cilium Gateway API lab first, if you haven’t done it already. In this one, you will learn about some additional specific use cases for Gateway API: Traffic splitting HTTP request header rewrite HTTP response header rewrite TLS Passthrough Cross-namespace routing](<https://isovalent.com/labs/advanced-gateway-api-use-cases/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### BGP on Cilium

Learn how to connect your Kubernetes Clusters with your on-premises network using BGP. As Kubernetes becomes more pervasive in on-premise environments, users increasingly have both traditional applications and Cloud Native applications in their environments. In order to connect them together and allow outside access, a mechanism to integrate Kubernetes and the existing network infrastructure running BGP is needed. Cilium offers native support for BGP, exposing Kubernetes to the outside and all the while simplifying users’ deployments.](<https://isovalent.com/labs/bgp-on-cilium/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### Cilium BIG TCP

BIG TCP–a revolutionary networking technology–is now available with Cilium to provide enhanced network performances for your nodes. In this lab, you will learn how BIG TCP can improve throughput by 40-50% in your network. Try it to learn more](<https://isovalent.com/labs/cilium-big-tcp/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### Cilium Cluster Mesh

With the rise of Kubernetes adoption, an increasing number of clusters is deployed for various needs, and it is becoming common for companies to have clusters running on multiple cloud providers, as well as on-premise. Kubernetes Federation has for a few years brought the promise of connecting these clusters into multi-zone layers, but latency issues are more often than not preventing such architectures. Cilium Cluster Mesh allows you to connect the networks of multiple clusters in such as way that pods in each cluster can discover and access services in all other clusters of the mesh, provided all the clusters run Cilium as their CNI. This allows to effectively join multiple clusters into a large unified network, regardless of the Kubernetes distribution each of them is running. In this lab, we will see how to set up Cilium Cluster Mesh, and the benefits from such an architecture.](<https://isovalent.com/labs/cilium-cluster-mesh/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### Cilium Egress Gateway

Kubernetes changes the way we think about networking. In an ideal Kubernetes world, the network would be entirely flat and all routing and security between the applications would be controlled by the Pod network, using Network Policies. In many Enterprise environments, though, the applications hosted on Kubernetes need to communicate with workloads living outside the Kubernetes cluster, which are subject to connectivity constraints and security enforcement. Because of the nature of these networks, traditional firewalling usually relies on static IP addresses (or at least IP ranges). This can make it difficult to integrate a Kubernetes cluster, which has a varying—and at times dynamic—number of nodes into such a network. Cilium’s Egress Gateway feature changes this, by allowing you to specify which nodes should be used by a pod in order to reach the outside world.](<https://isovalent.com/labs/cilium-egress-gateway/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### Cilium Envoy L7 Proxy

Envoy is a powerful L7 proxy which can be used for many Service Mesh needs. Cilium uses Envoy for L7 Network Policies, L7 observability, L7 internal load-balancing, and even allows users to configure Envoy for their own needs.](<https://isovalent.com/labs/cilium-envoy-l7-proxy/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-enterprise>)[NetworkingFrom **Isovalent**#### Cilium Gateway API

In this short lab, you will learn about Gateway API, a new Kubernetes standard on how to route traffic into a Kubernetes cluster. The Gateway API is the next generation of the Ingress API. Gateway API addresses some the Ingress limitations by providing an extensible, role-based and generic model to configure advanced L7 traffic routing capabilities into a Kubernetes cluster. In this lab, you will learn how you can use the Cilium Gateway API functionality to route HTTP and HTTPS traffic into your Kubernetes-hosted application.](<https://isovalent.com/labs/gateway-api/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[SecurityFrom **Isovalent**#### Cilium Host Firewall

Ever since its inception, Cilium has supported Kubernetes Network Policies to enforce traffic control to and from pods at L3/L4. But Cilium Network Policies even go even further: by leveraging eBPF, it can provide greater visibility into packets and enforce traffic policies at L7 and can filter traffic based on criteria such as FQDN, protocol (such as kafka, grpc), etc… Creating and manipulating these Network Policies is done declaratively using YAML manifests. What if we could apply the Kubernetes Network Policy operating model to our hosts? Wouldn’t it be nice to have a consistent security model across not just our pods, but also the hosts running the pods? Let’s look at how the Cilium Host Firewall can achieve this. In this lab, we will install SSH on the nodes of a Kind cluster, then create Cluster-wide Network Policies to regulate how the nodes can be accessed using SSH. The Control Plane node will be used as a bastion to access the other nodes in the cluster.](<https://isovalent.com/labs/cilium-host-firewall/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### Cilium IPv6 Networking and Observability

Learn how simple IPv6 can be installed and operated with Cilium and Hubble. With Kubernetes’ IPv6 support improving in recent releases and Dual Stack Generally Available in Kubernetes 1.23, it’s time to learn about IPv6 on Kubernetes. You might be wondering “How on Earth am I going to be able to operate this?” Good news–you’re in the right place. This lab will walk you through how to deploy a IPv4/IPv6 Dual Stack Kubernetes cluster and install Cilium and Hubble to benefit from their networking and observability capabilities. In particular, visibility of IPv6 flows is absolutely essential. IPv6’s slow adoption is primarily caused by fears it would be hard to operate and manage. As you will see, a tool such as Hubble will help operators visualize and understand their IPv6 network better.](<https://isovalent.com/labs/ipv6-networking-and-observability/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### Cilium Ingress Controller

You already know that Cilium accelerates networking, and provides security and observability in Kubernetes, using the power of eBPF. Now Cilium is bringing those eBPF strengths to the world of Service Mesh. Cilium Service Mesh features eBPF-powered connectivity, traffic management, security and observability. In this lab, you will learn how you can use Cilium to deploy Ingress resources to dynamically configure the Envoy proxy provided with the Cilium agent. And all of the above without any Envoy sidecar injection into your pods!](<https://isovalent.com/labs/cilium-service-mesh/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)[NetworkingFrom **Isovalent**#### Cilium LoadBalancer IPAM and BGP Service Advertisement

BGP support was initially introduced in Cilium 1.10 and subsequent improvements have been made since, such as the recent introduction of IPv6 support in Cilium 1.12. In Cilium 1.13, that support was enhanced with the introduction of Load Balancer IPAM and BGP Service address advertisements. In this lab, you will learn about both these new features and how they can simplify your network connectivity operations.](<https://isovalent.com/labs/lb-ipam-bgp-service/?utm_source=website-cilium&utm_medium=referral&utm_campaign=cilium-lab>)

- [1](https://cilium.io/labs/)
- [2](https://cilium.io/labs/2)
- [Next](https://cilium.io/labs/2)

#### Want to Add Your Lab to the List? Submit a PR here

[Submit a PR](https://github.com/cilium/cilium.io/blob/main/CONTRIBUTING.md#listing-labs)
