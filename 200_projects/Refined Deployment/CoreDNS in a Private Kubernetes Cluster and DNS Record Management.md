---
aliases: []
confidence: 
created: 2025-10-11T08:08:07Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: CoreDNS in a Private Kubernetes Cluster and DNS Record Management
type:
uid: 
updated: 
version:
---

---

This curriculum assumes a foundational knowledge of Kubernetes concepts (Pods, Services, Deployments) and focuses on the deployment, configuration, and operation of CoreDNS.

**(Note: The provided sources do not contain material related to configuring or using an Azure AKS cluster specifically. The curriculum is therefore based on general Kubernetes best practices and CoreDNS configuration as described in the excerpts.)**

## Module 1: CoreDNS Fundamentals and Deployment in Kubernetes

**Goal:** Understand the role of CoreDNS, its deployment requirements, and its core integration architecture within a private cluster environment.

| Topic                            | Key Concepts and Actions                                                                                                                                                                                                                                                                                                                                                | Source Citations |
| :------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| **1.1 CoreDNS Role in K8s**      | CoreDNS is the default DNS server shipped with Kubernetes starting with version 1.13 [1]. It functions as a **service directory** for containerized environments [2]. CoreDNS is necessary because service IP addresses often change rapidly (e.g., when pods are started and stopped) [2, 3].                                                                          | [1-3]            |
| **1.2 CoreDNS Integration**      | CoreDNS integrates with Kubernetes using the `kubernetes` plug-in [4]. This plug-in operates similarly to a Kubernetes controller by using the **API server's watch feature** to monitor **Services** and **Endpoints** resources [4-6]. The DNS records are generated *on the fly* based on this cached, up-to-date data, keeping responses fast [5].                  | [4-6]            |
| **1.3 Deployment Configuration** | Standard deployment involves several K8s resources: **ServiceAccount**, **ClusterRole**, and **ClusterRoleBinding** to grant CoreDNS cluster-wide read access (list/watch) to resources like Endpoints, Services, Pods, and Namespaces [7-10]. The CoreDNS pod uses the `Default` DNS policy to enable external name resolution via the host node's configuration [11]. | [7, 10, 11]      |
| **1.4 Autoscaling**              | To handle query load, CoreDNS instances can be scaled [12]. Autoscaling is typically handled by a cluster-proportional autoscaler [12]. Alternatively, the **Horizontal Pod Autoscaler (HPA)** can be used, targeting CPU utilization (e.g., 50%) or the `coredns_health_request_duration_seconds` metric [13, 14].                                                     | [12-14]          |

---

## Module 2: Internal (Private) DNS Record Management

**Goal:** Define and verify CoreDNS configuration for managing service discovery within the private cluster network.

| Topic                                                          | Key Concepts and Actions                                                                                                                                                                                                                                                                                                                        | Source Citations |
| :------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| **2.1 Internal Naming and Zones**                              | All internal records fall under a single **cluster domain** (e.g., `cluster.local`) [15]. CoreDNS must be configured with the `kubernetes` plug-in enabled for this domain, as well as the zones for reverse lookups (`REVERSE_CIDRS` or `in-addr.arpa ip6.arpa`) [16].                                                                         | [15, 16]         |
| **2.2 Cluster IP Services (Private Load Balancing)**           | Cluster IP Services provide a **stable Virtual IP (VIP)** address [17]. The DNS specification requires an **A record** for the VIP at the name format: `service.namespace.svc.cluster-domain` [18]. PTR records should also be generated for the cluster IP [19].                                                                               | [17-19]          |
| **2.3 Headless Services (Private Client-Side Load Balancing)** | Headless Services have `clusterIP: None` and rely on the client for load balancing [20]. CoreDNS responds to queries for these services with **multiple A records** (one for each endpoint IP) and **SRV records** (for each named port) [19, 21]. SRV records use underscores (e.g., `_http._tcp.<service>...`) and include the port [21, 22]. | [19-22]          |
| **2.4 Reverse DNS Lookups (PTR)**                              | The `kubernetes` plug-in needs the service CIDR or the entire reverse zones (`in-addr.arpa`, `ip6.arpa`) configured [16]. If no match is found, the **`fallthrough`** option should be configured to pass the request down the plug-in chain [23].                                                                                              | [16, 23]         |
| **2.5 Corefile Optimization**                                  | A better configuration involves splitting the server block into two: one handling **cluster-local domains** (with `kubernetes`) and a second handling the root zone (`.`) (with `forward` and `cache`). This prevents the redundant caching of in-cluster names and improves operational efficiency [24, 25].                                   | [24, 25]         |

---

## Module 3: External (Public) DNS Record Management

**Goal:** Configure CoreDNS to resolve external domain names and expose internal services safely to an external network.

| Topic                                              | Key Concepts and Actions                                                                                                                                                                                                                                                                                                                                          | Source Citations |
| :------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| **3.1 Resolving External Names (Forwarding)**      | Queries not handled by the `kubernetes` plug-in (non-cluster-local names) are typically forwarded to external DNS servers (UPSTREAMNAMESERVER) using the **`forward`** plug-in [26, 27]. This plug-in handles forwarder health checks and policies (e.g., `random`, `round_robin`) [28, 29].                                                                      | [26-29]          |
| **3.2 Stub Domains (Specific Upstreams)**          | To forward specific external domains (e.g., corporate names) to dedicated internal name servers, configure a separate server block that matches the specific domain [30]. This block uses the `forward` plug-in to direct traffic to the desired IP address (e.g., `corp.example.com { forward . 10.0.0.10:53 }`) [31].                                           | [30, 31]         |
| **3.3 Exposing Internal Services (Public Access)** | Kubernetes services can be exposed externally using methods like **External IPs**, **NodePort**, **LoadBalancer services**, or **Ingress** [32]. To map these external IPs to recognizable domain names, the **`k8s_external`** plug-in can be used [33]. It publishes external IP addresses in a specified zone (e.g., `<service>.<namespace>.<zone>`) [33, 34]. | [32-34]          |
| **3.4 Managing External Zone Data**                | For managing static public/external DNS records, CoreDNS offers several plugins: **`file`** (for standard zone data files) [35], **`auto`** (to load many zones automatically from a directory, optionally integrating with Git for version control) [36, 37], or **`route53`** (for synchronization from AWS Route 53) [38].                                     | [35-38]          |
| **3.5 Security Recommendation**                    | It is recommended to run a **separate deployment of CoreDNS** dedicated solely to external names, protecting the internal cluster DNS from denial-of-service attacks originating outside the cluster [34].                                                                                                                                                        | [34]             |
