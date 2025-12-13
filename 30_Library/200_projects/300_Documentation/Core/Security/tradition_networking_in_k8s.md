---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: tradition_networking_in_k8s
type:
uid: 
updated: 
version:
---

## Tradition Networking in K8s

### Traditional Networking Concepts in Kubernetes

The sources discuss how Kubernetes leverages and interacts with various traditional networking components and concepts:

- Container Network Interface (CNI): Kubernetes uses a pluggable interface called the Container Network Interface (CNI) to allow third-party vendors to implement the pod network. This means that Kubernetes itself does not implement the networking layer, but instead relies on external plugins to handle the complexities of pod-to-pod and pod-to-external communication.
- Overlay Networks: The sources explain that overlay networks are commonly used to create a flat Layer-2 network that spans all nodes in a Kubernetes cluster. This allows pods to communicate directly with each other regardless of their physical location. Overlay networks abstract the underlying physical network topology and provide a simplified networking environment for Kubernetes workloads.
- BGP (Border Gateway Protocol): BGP, a core routing protocol of the internet, is also utilised in Kubernetes networking, particularly in scenarios where integration with existing network infrastructure or more complex routing requirements are needed. Some CNI plugins support BGP to allow Kubernetes pods to be advertised as routable entities within a larger network. This enables seamless integration with on-premises networks or multi-cloud environments.
- Service Discovery and Load Balancing: Kubernetes relies on service discovery mechanisms to allow applications to locate and communicate with each other. The sources mention several service types, including ClusterIP, NodePort, and LoadBalancer, which provide different ways to expose services within and outside the cluster. Kubernetes also uses kube-proxy, a component running on each worker node, to implement service discovery and load balancing.
- ClusterIP: The most basic service type, ClusterIP, provides a stable internal IP address and port for a service within the cluster. This IP address is only accessible within the cluster's internal network and allows other pods to communicate with the service.
- NodePort: NodePort services build upon ClusterIP services and additionally expose the service on a specific port on each worker node in the cluster. This allows external clients to access the service through any worker node's IP address and the assigned NodePort.
- LoadBalancer: LoadBalancer services take service exposure a step further by integrating with cloud provider load balancers. They create an external load balancer (e.g., an AWS ELB or Azure Load Balancer) and automatically configure it to distribute traffic to the pods backing the service. This provides a highly available and scalable way to expose services to the internet.
- DNS (Domain Name System): Kubernetes utilises DNS for internal service discovery. Each service is assigned a DNS name, and pods can use this name to resolve the service's IP address and communicate with it.
- Network Policies: Kubernetes network policies provide a mechanism to control traffic flow between pods and namespaces. They are analogous to traditional firewall rules and allow administrators to specify which pods are allowed to communicate with each other based on labels, ports, and other criteria. Network policies enforce network segmentation and enhance security within the cluster.
- Ingress: Ingress is a Kubernetes resource that manages external access to services within the cluster. It acts as a reverse proxy and load balancer, routing incoming traffic to the appropriate services based on rules defined in the ingress configuration. Ingress allows you to consolidate routing rules and manage external access to multiple services through a single entry point.
- Service Meshes: The sources mention service meshes as a way to enhance network functionality and security within a Kubernetes cluster. Service meshes, such as Istio and Linkerd, introduce a dedicated infrastructure layer for managing service-to-service communication. They provide features like traffic management, security (e.g., mutual TLS encryption), observability, and resilience.

In addition to the components and concepts mentioned in the sources, Kubernetes can also utilise other traditional networking elements, including:

- Virtual Private Clouds (VPCs): When running Kubernetes in a cloud environment like AWS or Azure, the cluster typically resides within a VPC. VPCs provide a logically isolated network within the cloud provider's infrastructure and allow you to define subnets, routing tables, and security groups to control network traffic. This information regarding VPCs is not explicitly mentioned in the sources, but it is a common practice when deploying Kubernetes in the cloud, and you may want to independently verify it.
- Network Address Translation (NAT): Kubernetes can utilise NAT to allow pods with private IP addresses to communicate with external networks. Kube-proxy, the component responsible for service networking, often employs NAT to map service IP addresses to pod IP addresses. This allows external clients to access services without needing to know the internal IP addresses of the pods.

Kubernetes leverages traditional networking concepts and components to provide a flexible, scalable, and secure networking environment for containerised applications. By integrating with existing networking infrastructure and utilising well-established protocols, Kubernetes allows you to deploy and manage complex distributed systems efficiently.
