---
aliases: []
author: 
confidence: 
created: 2025-03-14T17:40:18Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:48Z
purpose: 
review_interval: 
see_also: []
source: https://zeet.co/blog/kubernetes-networking-101-your-straightforward-guide-to-connecting-pods-and-services
source_of_truth: []
status: 
tags: [k8s, networking]
title: Introduction to Kubernetes Networking
type: download
uid: 
updated: 
version: 1
---

Kubernetes networking is a foundational component that enables communication between components in a Kubernetes cluster. The networking model is one of the key abstractions that Kubernetes provides out of the box.

The Kubernetes networking model is designed around the following requirements:

- All Pods should be able to communicate with one another across Node boundaries**: This enables applications to talk to each other regardless of which Node they are scheduled on.
- All Nodes can communicate with all Pods**: This allows the Kubernetes control plane to communicate with Pods for operations like health checking.
- Pods should have unique IP addresses**: This ensures each Pod has its own identity on the network which simplifies application deployment.

The fundamental networking unit in Kubernetes is a Pod. Every Pod gets its own IP address from the network CIDR range. This IP address is shared by all containers within the Pod and links are configured between containers via a virtual Ethernet bridge.

The networking implementation itself is pluggable in Kubernetes through the Container Network Interface (CNI). There are several CNI plugins like Flannel, Calico, Cilium etc that handle the actual network wiring between Pods, Nodes and the external network.

Networking was a weak point in early versions of Kubernetes but has matured over releases with the evolution of CNI. With robust networking capabilities now available, Kubernetes can provide patterns like distributed microservices out of the box.

## The Pod Network Model

Kubernetes handles networking in a unique way compared to traditional networking models. Rather than relying on hardware network interfaces and IPs, Kubernetes takes an abstracted software-defined approach to networking.

In Kubernetes, every Pod gets its own IP address. This IP address is not tied to the Node that the Pod is running on. Instead, Pods get an IP address from the Pod network range that is managed by the network provider plugin.

This means that Pods can be treated much like VMs or physical hosts from a networking perspective. Every Pod gets its own dedicated network stack and IP address. This enables Pods to communicate with each other across Nodes without Network Address Translation (NAT).

This IP-per-Pod model is a fundamental requirement for networking in Kubernetes. It ensures the following key requirements are met:

- Every Pod should be able to communicate with every other Pod in the cluster, regardless of which Node they are running on. This requires Pods to have networking visibility beyond just their local Node.
- Pods on the same Node can communicate with each other without NAT. This enables efficient networking between local Pods.
- Pods can keep their IP address when moved between Nodes. Since Pod IPs are not tied to Nodes, Pods can be rescheduled to other Nodes without changing their networking identity.

The IP-per-Pod approach provides a flexible and highly available networking model for connecting Pods. Kubernetes network providers implement this model using overlay networks, VLANs, and other software-defined networking approaches. This abstraction from the underlying network infrastructure is what enables the portability and resilience of the IP-per-Pod model.

## Cluster Networking

Kubernetes enables Pods to communicate with each other across Nodes in a cluster. This is achieved through the networking model and components in Kubernetes:

- Each Pod gets its own IP address, so Pods can communicate with each other.
- Pods on a Node can communicate with all Pods on all Nodes without NAT.
- This Pod network is implemented through networking plugins. Common options include Flannel, Calico, Canal, Weave Net.
- The plugins use CNI (Container Network Interface) to configure networking when Pods are created.
- CNI handles IP Address Management (IPAM), assigns IP addresses, and configures routes and network interfaces for Pods.
- Some CNI plugins like Calico and Canal also provide advanced features like network policy.

The networking plugin creates a software-defined network that spans all the Nodes in the Kubernetes cluster. Pods get unique IP addresses within this network, allowing them to communicate with other Pods directly.

The Pod network is established during cluster startup and enabled through the kubelet on each Node. The kubelet configures network interfaces for each Pod via CNI.

Overall, the CNI plugins and network providers implement the networking model defined by Kubernetes. This enables connectivity between Pods across Nodes, a fundamental requirement for Kubernetes applications.

## Services and Load Balancing

Kubernetes Services provide stable networking and load balancing for Pods. Services enable loose coupling between Pods so that Pods can be created, moved, scaled, and destroyed without impacting connectivity between other Pods.

Services have an IP address and DNS name that remains constant even as the set of Pods matching the Service changes. There are several types of Kubernetes Services:

- ClusterIP - Exposes the Service on an internal cluster IP address. This makes the Service only reachable within the cluster.
- NodePort - Exposes the Service on the same port of each selected Node in the cluster using NAT. Makes a Service accessible from outside the cluster using :.
- LoadBalancer - Creates an external load balancer in the cloud provider and assigns a fixed external IP to the Service.
- ExternalName - Exposes the Service using an arbitrary name by returning a CNAME record with the name. No proxy is used.

This enables various patterns like external load balanced Services, internal only Services, and Services only accessible via DNS resolution.

Each Service gets a DNS name in the form ..svc.cluster.local which Pods can use for discovery and connectivity. The Kubernetes DNS server handles DNS queries for these Service DNS names by returning the associated ClusterIP or CNAME record.

This provides reliable service discovery and connectivity for Pods as they get created and destroyed. Pods can locate each other and communicate using the assigned Service DNS names rather than hardcoding endpoint IPs and ports.

## Ingress Controllers

In Kubernetes, Ingress provides HTTP and HTTPS routes from outside the cluster to services within the cluster. It works by routing traffic based on the request host or path to backend services such as Pods.

An Ingress controller is required for this to work. The controller monitors Ingress resources and Kubernetes Services and configures a load balancer to route traffic accordingly. This allows a single IP address to route to multiple services in the cluster.

Some common Ingress controllers include:

- NGINX Ingress Controller - The default Ingress controller. It uses NGINX as a reverse proxy and load balancer.
- Traefik - A cloud native edge router that works as an Ingress controller. It can be configured through Kubernetes Manifests.
- HAProxy Ingress - Uses the HAProxy load balancer as an Ingress controller. Provides high availability.
- GCE - The Ingress controller provided by Google Kubernetes Engine. Uses a GCP load balancer.
- Istio Ingress - Provides Ingress capabilities as part of the Istio service mesh.

The Ingress resource allows configuring rules for routing traffic to Services. This includes the hostname, path, and other routing rules. Multiple Ingress resources can be created in a cluster.

By leveraging Ingress and Ingress controllers, you can easily configure load balanced entry points into a Kubernetes cluster. Different controllers have additional capabilities like SSL/TLS termination, name-based virtual hosting, etc.

## Network Policies

Kubernetes comes with a default network policy that allows all ingress and egress traffic between Pods and Services. This provides an open network model to start with.

However, you can implement network policies to restrict traffic between Pods. Network policies let you specify what traffic is allowed based on Pod labels and IP blocks.

Some common uses for network policies include:

- Deny all ingress and egress traffic by default
- Allow traffic only between certain Pods
- Allow ingress traffic only from certain IP blocks
- Limit egress traffic to specific external IPs

To use network policies, you need to be using a network provider that supports them, such as Calico, Romana, or Weave Net. The network provider is responsible for enforcing the policies.

To create a network policy, you define a NetworkPolicy resource that specifies the ingress and egress rules. For example:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:  
  name: allow-app
spec:  podSelector:    matchLabels:      app: myapp  ingress:  - from:    - podSelector:        matchLabels:          role: frontend    ports:      - protocol: TCP        port: 6379
```

This allows ingress traffic on TCP port 6379 from Pods with the label role: frontend to Pods with the label app: myapp.

With carefully designed network policies, you can build secure, hierarchical networks within your Kubernetes cluster. Network policies open up possibilities like setting up DMZs, zero-trust networks, and enforcing fine-grained rules.

## DNS in Kubernetes

The Kubernetes DNS service provides DNS resolution for Pods and Services in the cluster. It's enabled by default and helps enable name-based discovery between Pods in the cluster.

The Kubernetes DNS service automatically assigns DNS names to Pods and Services. Pods are assigned a DNS name in this format:

`pod-ip-address.namespace.pod.cluster.local`

For example a Pod with IP address 172.17.0.3 in the default namespace would have a DNS name like:

`172-17-0-3.default.pod.cluster.local`

This allows Pods to resolve other Pods in the cluster using their DNS names instead of IP addresses.

Services are assigned a DNS name in this format:

`service-name.namespace.svc.cluster.local`

For example, a Service named myapp in the default namespace would have a DNS name like:

`myapp.default.svc.cluster.local`

Pods can lookup Services by their DNS names, which resolve to the ClusterIP of the Service.

The DNS names are based on the Pod IPs and Service ClusterIPs. If these IPs change, the DNS names are automatically updated.

The Kubernets DNS server runs as a Pod in the cluster and implements the DNS naming schema. It maintains DNS records for all Pods and Services.

DNS policies can be configured to customize the DNS resolution behavior. For example, you can configure split-horizon DNS to have Pods resolve names differently depending on whether the target Pod is headless or not.

Overall, the built-in Kubernetes DNS service provides seamless DNS-based discovery and connectivity between Pods and Services in the cluster.

## External Connectivity

Kubernetes pods are unable to access external networks by default. There are a few ways to provide external connectivity:

- NAT with kube-proxy - The kube-proxy can configure iptables rules to NAT outbound connections from pods to external IPs. This provides basic connectivity but has limitations around returning traffic to pods.
- External connectivity with CNI plugins - Many CNI plugins like Calico, Canal, and Weave Net include options to configure external connectivity. For example:
- Calico can configure NAT capabilities or BGP peering with top-of-rack routers for external connectivity.
- Canal uses Calico for policy and Flannel for networking which can provide external access.
- Weave Net sets up a virtual network that spans hosts and can connect that network to external resources.
- NodePort Services - By exposing a Service as NodePort, external clients can access the nodes IP address on the allocated port.
- LoadBalancer Services - On supported cloud providers like AWS or GCP, a load balancer can be provisioned to expose Services externally.
- Ingress Controller - Ingress controllers like Nginx, Traefik, or HAProxy running on each node can route external traffic to Services and Pods.

Choosing the right external networking approach depends on your environment and requirements. Solutions like Calico BGP peering or LoadBalancer Services provide the most seamless connectivity without NAT or port mapping. For basic external access, kube-proxy NAT or NodePort Services may be sufficient.

## IPv4/IPv6 Dual Stack

Kubernetes supports IPv4/IPv6 dual-stack networking to enable Pods and Services to use IPv4 and IPv6 addresses. This provides flexibility as some workloads may require IPv4, some IPv6, and some both.

To enable dual-stack networking:

- The Kubernetes cluster must be configured with a network provider that supports IPv4/IPv6 dual-stack. Popular options include Calico, Cilium, Kube-router, Romana, or Weave Net.
- The Pod and Service specifications must be configured with both IPv4 and IPv6 addresses in the IP families field:

ipFamilies:  - ipv4  - ipv6

- The cluster DNS must support AAAA records for IPv6 Services.

With dual-stack enabled, Pods will be assigned an IPv4 and IPv6 address. Services can be exposed on both protocols by specifying dual stack IPs. This allows workloads to communicate seamlessly via IPv4 and/or IPv6 as needed.

The key advantages of dual stack are:

- Workloads have the flexibility to use IPv4 and/or IPv6 networking.
- Applications can migrate incrementally from IPv4 to IPv6.
- Enables IPv6-only workloads to run when needed.
- Provides fault tolerance if either IPv4 or IPv6 connectivity has issues.

Dual stack networking will be increasingly important as IPv6 adoption grows. Kubernetes' support for dual stack makes it easy to run IPv4 and IPv6 workloads side-by-side.

## Troubleshooting Kubernetes Networking

Kubernetes networking can be complex, so issues inevitably arise that require troubleshooting. Here are some common networking issues and how to diagnose them:

### Connectivity Issues Between Pods

If Pods cannot communicate with each other, there may be an issue with the CNI plugin or network provider. Some things to check:

- Verify that Pods are scheduled on the same node. Pods on different nodes cannot communicate directly.
- Check that the CNI plugin is functioning correctly and Pods are assigned IP addresses.
- Look for errors in the CNI plugin logs.
- Try deleting the Pod and having it recreated to get a new IP address.

### Accessing Services

If a Pod cannot resolve a Service name or cannot connect to the Service cluster IP, investigate the kube-dns component. Potential issues include:

- The kube-dns Pod is not running or is stuck in a crash loop.
- DNS lookups are timing out or returning errors.
- The Service object was not created correctly or has the wrong selector.

### External Connectivity Failures

If Pods cannot reach external networks, the issue may be with the kube-proxy, network provider NAT or firewall rules. Steps to debug:

- Verify the kube-proxy Pod is running on each node.
- Check the iptables rules on nodes for broken NAT or missing port forwarding.
- Test connectivity to external IPs from within Pods using curl or ping.
- Look at the network provider configuration for any ACLs blocking access.

Tools like Kubernetes network utilities, tcpdump and ping can help capture traffic and trace connectivity issues. Overall, carefully inspect the various components like CNI, kube-dns, kube-proxy and the network provider to isolate the root cause.
