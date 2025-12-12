---
aliases: []
confidence:
created: 2025-11-21T14:14:28Z
epistemic:
last_reviewed:
modified: 2025-11-22T14:13:59Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: []
title: kubernetes_ingress_aks_eks_guide
type:
uid:
updated:
---

## A Technical Guide to Kubernetes Ingress for AKS and EKS
**Publication Date: 2025-11-21**

This document provides a comprehensive technical guide to understanding, implementing, and managing Kubernetes Ingress, with a specific focus on deployments within Azure Kubernetes Service (AKS) and Amazon Elastic Kubernetes Service (EKS). It is intended for DevOps engineers, cloud architects, and system administrators responsible for designing and maintaining scalable and secure application delivery infrastructure on Kubernetes. The guide covers fundamental concepts, architectural components, API specifications, cloud-native integrations, and operational best practices.

### 1. Fundamental Concepts of Kubernetes Ingress

Kubernetes Ingress serves as a critical API object that orchestrates the management of external access to services operating within a Kubernetes cluster [1]. Its primary function is to provide a sophisticated and centralized mechanism for handling inbound HTTP and HTTPS traffic [2, 6]. Ingress allows for the definition of intelligent routing rules that direct external requests to the appropriate backend services based on criteria such as the requested hostname or URL path [5, 8]. This capability is fundamental to exposing multiple services through a single entry point, thereby simplifying network architecture and external access patterns [2, 8]. By leveraging Ingress, organizations can implement advanced functionalities including Layer 7 (L7) load balancing, SSL/TLS termination for securing communications, and name-based virtual hosting, which enables multiple domain names to be served from a single IP address [5, 6, 10].

The introduction and stabilization of the Ingress API marked a significant evolution in Kubernetes networking. Prior to its widespread adoption, exposing applications to the internet often required cumbersome and less integrated methods. A common approach involved deploying custom reverse proxies, such as NGINX or HAProxy, as dedicated `LoadBalancer` services [4]. The routing logic for these proxies was typically managed through separate `ConfigMap` objects, which had to be manually updated and reloaded, leading to a disjointed and error-prone operational workflow [4]. This method was not only complex to manage but could also become prohibitively expensive, as provisioning a dedicated cloud load balancer for each individual service or group of services incurred significant infrastructure costs [2, 8]. Ingress was designed to address these challenges directly by providing a native, declarative, and cost-effective solution for traffic management.

The strategic value of adopting Kubernetes Ingress is multifaceted. Firstly, it facilitates the **consolidation of external access points**. Instead of exposing numerous services via individual `NodePort` or `LoadBalancer` services, Ingress allows a multitude of applications to be exposed through a single, shared external IP address [5, 8]. This creates a unified and predictable entry point into the cluster, which simplifies DNS management and firewall configurations. Secondly, this consolidation leads to substantial **cost reduction**. By sharing a single external load balancer among many services, organizations can avoid the high costs associated with provisioning a dedicated load balancer for every application that requires external access [7, 8]. This is particularly impactful in large-scale microservices environments where hundreds or thousands of services may be running.

Furthermore, Ingress significantly **simplifies operational management**. It provides a centralized location for defining and managing routing rules, domain name configurations, and TLS certificate management [7]. This centralization ensures consistency across the environment, reduces administrative overhead, and minimizes the potential for configuration drift. The declarative nature of the Ingress resource allows routing logic to be version-controlled and managed as code, aligning with modern GitOps practices [8]. Lastly, Ingress enhances the **scalability and flexibility** of application deployments. It natively supports both path-based and hostname-based routing, which enables engineering teams to easily add, remove, or update services behind a stable and flexible entry point without requiring changes to the underlying network infrastructure [7]. This agility is crucial for dynamic environments where applications are frequently updated and scaled.

### 2. Ingress Architecture and Core Components

The Kubernetes Ingress architecture is elegantly designed around two distinct but interdependent components: the **Ingress Resource** and the **Ingress Controller** [5, 8]. This separation of concerns is a hallmark of Kubernetes design, allowing for a declarative definition of desired state (the Ingress resource) to be reconciled by an active, operational component (the Ingress controller). Together, these elements provide a robust framework for managing external traffic into the cluster.

The **Ingress Resource** is a standard Kubernetes API object, defined in a YAML manifest, that serves as a declarative blueprint for traffic routing [1, 5]. It does not, by itself, possess any active logic or networking capabilities [4, 10]. Instead, it is a collection of rules and configurations that specify how incoming HTTP and HTTPS requests should be handled. An administrator or developer defines an Ingress resource to map external URLs to internal services. The specification within the resource contains critical routing information, including the hostnames for name-based virtual hosting, the URL paths for path-based routing, and the backend Kubernetes Service (and its corresponding port) to which the traffic should be forwarded [1, 8]. Additionally, the Ingress resource can specify TLS configurations, referencing a Kubernetes Secret that contains the necessary certificate and private key to enable SSL/TLS termination at the ingress layer [4, 8]. It is crucial to understand that creating an Ingress resource alone has no effect; it requires the presence of an Ingress controller to be interpreted and acted upon [4, 10].

The **Ingress Controller** is the engine that brings the Ingress resource to life. It is a specialized application, typically a sophisticated reverse proxy and load balancer like NGINX, HAProxy, or Envoy, that runs as one or more Pods within the Kubernetes cluster [5, 8, 9]. The controller's primary responsibility is to watch the Kubernetes API server for the creation, modification, or deletion of Ingress resources [5, 8]. When it detects a change, it dynamically reconfigures the underlying proxy to implement the routing rules defined in those resources [5, 9]. This control loop ensures that the actual state of the network routing always matches the desired state declared in the Ingress objects. Unlike many core Kubernetes controllers that are bundled with the `kube-controller-manager`, Ingress controllers are not automatically started with a cluster [3, 4, 9]. This is an intentional design choice, as it allows users to select an Ingress controller that best fits their specific performance, feature, and integration requirements. The cluster administrator must choose, deploy, and manage the lifecycle of the Ingress controller [3].

The traffic flow for a request managed by Ingress follows a well-defined path. It begins when a user sends a request to a domain name associated with an application running in the cluster [2, 9]. The request first traverses the public internet to the cluster's edge. The domain name resolves via DNS to the external IP address of the Ingress controller [2, 9]. This external IP is typically provided by a cloud provider's load balancer (e.g., an AWS Network Load Balancer or an Azure Load Balancer) that is provisioned to sit in front of the Ingress controller Pods [4, 5, 9]. This external load balancer's job is to distribute incoming traffic across the available Ingress controller replicas for high availability and scalability.

Once the request reaches an Ingress controller Pod, the controller inspects the request's headers, particularly the `Host` header and the URL path [2, 5]. It then evaluates this information against the complete set of routing rules aggregated from all Ingress resources it is managing [5, 9]. Upon finding a matching rule, the Ingress controller acts as a reverse proxy and forwards the request to the appropriate backend Kubernetes Service specified in the rule [5, 8, 9]. The Kubernetes Service, in turn, performs its own load balancing, distributing the request to one of the healthy application Pods associated with that service [2, 5, 8]. The application Pod processes the request and sends a response back along the same path: from the Pod to the Service, from the Service to the Ingress controller, and finally, from the Ingress controller back to the original user through the external load balancer [2]. This entire process, from the edge to the application and back, is orchestrated seamlessly by the Ingress architecture.

### 3. Kubernetes API Objects: Ingress and IngressClass

The functionality of Kubernetes Ingress is formally defined through two primary API objects: `Ingress` and `IngressClass`. These resources provide the declarative framework for specifying traffic routing rules and associating them with the appropriate controller implementation. A deep understanding of their structure and interplay is essential for effective Ingress management.

The **Ingress** resource, which graduated to stable in Kubernetes v1.19 under the `networking.k8s.io/v1` API group, is the core object used to define how external HTTP and HTTPS traffic should be routed to services within the cluster [1, 16]. A minimal Ingress manifest includes the standard `apiVersion`, `kind`, and `metadata` fields, along with a `spec` field that contains the routing logic. The `spec` is the most critical part of the object and can be configured in several ways. It can define a `defaultBackend`, which acts as a catch-all, directing any traffic that does not match a specific rule to a designated service. More commonly, the `spec` contains a list of `rules`. Each rule is designed to handle traffic for a specific host. Within a rule, you can define multiple `paths`, each mapping a URL path to a backend service. The `pathType` field (`Prefix`, `Exact`, or `ImplementationSpecific`) specifies how the path matching should be performed [1]. For securing communication, the `spec` can also include a `tls` section, which associates one or more hostnames with a Kubernetes `Secret` containing the TLS certificate and private key, enabling the Ingress controller to terminate SSL/TLS connections [1].

The **IngressClass** resource was introduced to address the complexities of running multiple Ingress controllers within a single cluster [15]. Before its introduction, the selection of a controller was typically handled via a specific annotation (`kubernetes.io/ingress.class`) on the Ingress resource itself [10, 16]. This approach lacked formal structure and could lead to ambiguity. The `IngressClass` resource, also part of the `networking.k8s.io/v1` API, provides a formal, non-namespaced, cluster-wide mechanism for defining a type of Ingress and associating it with a specific controller [16].

An `IngressClass` resource has a simple but powerful structure. Its `spec` contains a `controller` field, which specifies the name of the controller that should implement Ingresses of this class (e.g., `k8s.io/ingress-nginx` or `ingress.k8s.aws/alb`) [11, 15]. This allows administrators to define multiple classes, each backed by a different controller technology, perhaps one for external traffic and another for internal traffic, or one optimized for performance and another with advanced security features. To associate an `Ingress` resource with a specific `IngressClass`, the `ingressClassName` field is set in the `Ingress` resource's `spec` [12]. This is the recommended approach for Kubernetes versions 1.18 and later, replacing the now-deprecated annotation [16].

To further streamline configuration, a cluster can have a default `IngressClass`. This is achieved by adding the annotation `ingressclass.kubernetes.io/is-default-class: "true"` to an `IngressClass` resource [3]. If an Ingress resource is created without an `ingressClassName` field specified, and a single default `IngressClass` exists in the cluster, Kubernetes will automatically associate the Ingress with that default class [3].

The `IngressClass` resource also provides a mechanism for controller-specific configuration through its optional `parameters` field [14, 16]. This field can reference a custom resource that contains additional settings for the controller. The `parameters` field specifies the `apiGroup`, `kind`, and `name` of the configuration resource [14]. This allows for a clean separation between the generic Ingress definition and the implementation-specific tuning parameters, such as load balancing algorithms, timeout settings, or security policy enforcement. For example, the AWS Load Balancer Controller uses an `IngressClassParams` custom resource to enforce settings like IP address type or AWS resource tags across all Ingresses associated with that class [11]. This powerful feature enables administrators to create standardized tiers of service for ingress traffic, managed through the Kubernetes API.

### 4. Cloud-Specific Implementations: AKS and EKS

While the Kubernetes Ingress and IngressClass APIs provide a standardized specification, the actual implementation of the Ingress controller is what bridges the gap between the Kubernetes cluster and the underlying cloud provider's networking infrastructure. For Azure Kubernetes Service (AKS) and Amazon Elastic Kubernetes Service (EKS), there are powerful, cloud-native Ingress controllers that integrate deeply with their respective platforms' load balancing services, offering enhanced performance, security, and manageability.

#### Azure Kubernetes Service (AKS): Application Gateway Ingress Controller (AGIC)

For users of Azure Kubernetes Service, the **Azure Application Gateway Ingress Controller (AGIC)** provides a first-class integration with Azure's native Layer 7 load balancer, the Application Gateway [19]. AGIC runs as a pod within the AKS cluster and continuously monitors the Kubernetes API for Ingress resources [19, 21]. When it detects an Ingress resource that it is designated to manage, it translates the Ingress rules into a corresponding Application Gateway configuration and applies it to the gateway instance via Azure Resource Manager (ARM) [19]. This creates a direct and highly efficient path for traffic from the internet to the pods.

One of the most significant benefits of using AGIC is the elimination of extra network hops. In a typical setup with a generic Ingress controller like NGINX, traffic flows from the external load balancer to the Ingress controller pods, and then through Kubernetes' internal service routing (`kube-proxy`) to reach the application pods. This involves multiple layers of network address translation and proxying. AGIC streamlines this flow by allowing the Application Gateway to communicate directly with the pods using their private IP addresses within the virtual network [19]. This bypasses the need for `NodePort` or `KubeProxy` services for ingress traffic, resulting in lower latency and improved performance [19].

AGIC leverages the rich feature set of the Azure Application Gateway, including advanced URL routing, cookie-based session affinity for stateful applications, SSL/TLS termination with centralized certificate management, and end-to-end TLS encryption [19]. Crucially, it also integrates with the Azure Web Application Firewall (WAF), which can be enabled on the Application Gateway to protect applications from common web vulnerabilities and attacks, such as SQL injection and cross-site scripting [19]. AGIC is exclusively supported with the Standard_v2 and WAF_v2 SKUs of Application Gateway, which provide autoscaling capabilities, allowing the gateway to scale its capacity automatically based on traffic load [19].

There are two primary methods for deploying AGIC. The first is as an **AKS Add-On**, which is the recommended and most straightforward approach [19, 23]. When enabled, the add-on is a fully managed service provided by Azure, meaning it is automatically updated and supported by Microsoft [19]. This simplifies the lifecycle management of the controller. The second method is a manual deployment using **Helm charts** [28]. This approach offers more granular control over the controller's configuration but requires the user to manage updates and maintenance. The Helm deployment is necessary for more complex scenarios, such as running multiple AGIC instances in a single cluster or sharing an Application Gateway across multiple clusters [19].

#### Amazon Elastic Kubernetes Service (EKS): AWS Load Balancer Controller

In the Amazon Web Services ecosystem, the **AWS Load Balancer Controller** is the standard for integrating Amazon EKS clusters with Elastic Load Balancing (ELB) [29]. This controller satisfies Kubernetes Ingress resources by provisioning and managing **Application Load Balancers (ALBs)** [29, 36]. ALBs are sophisticated Layer 7 load balancers that provide advanced request routing capabilities, making them a perfect fit for implementing Ingress rules. When an Ingress resource is created in the EKS cluster, the AWS Load Balancer Controller automatically provisions an ALB, configures listeners for HTTP and HTTPS, and creates target groups that point directly to the pods running the application [31].

A key feature of the AWS Load Balancer Controller is its ability to manage both ALBs and **Network Load Balancers (NLBs)**. While it uses ALBs for `Ingress` resources, it can also provision NLBs for Kubernetes `Service` objects of type `LoadBalancer` [29, 33]. This provides a unified controller for managing both Layer 7 and Layer 4 load balancing needs. By using ALBs for Ingress, users can leverage features like path-based routing, host-based routing, SSL/TLS termination with AWS Certificate Manager (ACM) integration, and security enhancements through AWS WAF [36]. A significant advantage is the ability to share a single ALB across multiple Ingress resources within the cluster, which can lead to substantial cost savings compared to provisioning a separate load balancer for each service [31].

The controller supports two different target modes for routing traffic to pods: **Instance mode** and **IP mode** [35]. In Instance mode, the ALB routes traffic to the NodePort opened on the EC2 worker nodes, and `kube-proxy` then forwards the traffic to the appropriate pod. In IP mode, which is generally recommended, the controller registers the pods' private IP addresses directly as targets in the ALB's target groups [35]. This eliminates the extra hop through the NodePort and `kube-proxy`, resulting in better performance and preserving the client's source IP address [35].

Proper installation and configuration of the AWS Load Balancer Controller involve several prerequisite steps. This includes creating an IAM role with the necessary permissions for the controller to make API calls to AWS services like EC2 and ELB [29, 35]. This role is then associated with the controller's Kubernetes service account using IAM Roles for Service Accounts (IRSA) [35]. Additionally, the VPC subnets where the load balancers will be deployed must be tagged correctly. Public subnets for internet-facing load balancers require the tag `kubernetes.io/role/elb` with a value of `1`, while private subnets for internal load balancers need the tag `kubernetes.io/role/internal-elb` with a value of `1` [35]. Once these prerequisites are met, the controller is typically installed into the cluster using a Helm chart [30, 35].

### 5. Configuration Deep-Dive and YAML Examples

To effectively utilize Kubernetes Ingress, it is essential to understand the practical application of its API objects through YAML manifests. The following examples illustrate common configuration patterns, from basic routing to cloud-specific implementations for AKS and EKS. These configurations are declarative, allowing them to be version-controlled and applied consistently across environments.

#### Basic Path-Based Fanout Ingress

A common use case for Ingress is to route traffic to different backend services based on the URL path. This pattern, often called "fanout," allows multiple microservices to be exposed under a single domain name, each handling a different part of the application's functionality [1]. The following YAML manifest defines an Ingress resource that directs requests for `http://example.com/app-one` to a service named `app-one-service` and requests for `http://example.com/app-two` to `app-two-service`.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-fanout-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: example.com
    http:
      paths:
      - path: /app-one
        pathType: Prefix
        backend:
          service:
            name: app-one-service
            port:
              number: 80
      - path: /app-two
        pathType: Prefix
        backend:
          service:
            name: app-two-service
            port:
              number: 8080
```

In this example, the `ingressClassName` is set to `nginx`, indicating that this Ingress should be managed by an NGINX Ingress controller [12]. The single rule applies to the host `example.com`. The `paths` array defines the routing logic. The `pathType: Prefix` ensures that any request starting with `/app-one` (e.g., `/app-one/login`) will be routed to `app-one-service`. The annotation `nginx.ingress.kubernetes.io/rewrite-target: /` is specific to the NGINX controller and instructs it to rewrite the URL path to `/` before forwarding the request to the backend service, which is often necessary for applications that are not path-aware.

#### Name-Based Virtual Hosting

Another powerful feature of Ingress is name-based virtual hosting, which allows you to route traffic for different hostnames to different services, all from a single external IP address [1]. This is ideal for hosting multiple distinct websites or applications from the same Kubernetes cluster. The manifest below configures routing for `first-app.example.com` and `second-app.example.com`.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: virtual-host-example
spec:
  ingressClassName: nginx
  rules:
  - host: first-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: first-app-service
            port:
              number: 80
  - host: second-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: second-app-service
            port:
              number: 80
```

This configuration defines two separate rules, one for each host. Requests to `first-app.example.com` are directed to `first-app-service`, while requests to `second-app.example.com` are sent to `second-app-service`. This approach is highly efficient for managing multiple domains without needing a separate load balancer for each one.

#### TLS Termination

Securing web traffic with HTTPS is a critical requirement for production applications. Ingress simplifies this by allowing you to terminate TLS connections at the ingress layer [1]. The Ingress controller handles the TLS handshake, decrypts the traffic, and forwards it to the backend services as plain HTTP. This offloads the burden of certificate management from the individual applications.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-example-ingress
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - secure-app.example.com
    secretName: example-tls-secret
  rules:
  - host: secure-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-secure-app-service
            port:
              number: 80
```

The `tls` section in the `spec` is key here. It specifies that the host `secure-app.example.com` should be served over HTTPS. The `secretName` field points to a Kubernetes `Secret` named `example-tls-secret`, which must contain the TLS certificate (`tls.crt`) and private key (`tls.key`) for the domain [1]. When a user accesses `https://secure-app.example.com`, the Ingress controller will use this secret to secure the connection.

#### Cloud-Specific Example: AKS with AGIC

When using the Azure Application Gateway Ingress Controller (AGIC) on AKS, you specify the controller using an annotation. The following example shows an Ingress resource configured for AGIC.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: aks-agic-ingress
  annotations:
    kubernetes.io/ingress.class: azure/application-gateway
spec:
  rules:
  - host: aks-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-aks-app-service
            port:
              number: 80
```

The critical element is the annotation `kubernetes.io/ingress.class: azure/application-gateway` [24]. This annotation signals to AGIC that it should manage this Ingress resource and configure the associated Azure Application Gateway accordingly.

#### Cloud-Specific Example: EKS with AWS Load Balancer Controller

For EKS, the modern approach is to use an `IngressClass` resource and reference it via the `ingressClassName` field. The AWS Load Balancer Controller uses the name `alb`.

First, an `IngressClass` would be defined (often done during controller installation):

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: alb
spec:
  controller: ingress.k8s.aws/alb
```

Then, the Ingress resource would reference this class:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: eks-alb-ingress
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
  - host: eks-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-eks-app-service
            port:
              name: http
```

Here, `ingressClassName: alb` links the Ingress to the AWS Load Balancer Controller [11]. The annotations provide controller-specific instructions. `alb.ingress.kubernetes.io/scheme: internet-facing` specifies that an external, public-facing Application Load Balancer should be created. `alb.ingress.kubernetes.io/target-type: ip` instructs the controller to use the more efficient IP targeting mode, routing traffic directly to pod IPs [32].

### 6. Best Practices and Advanced Considerations

Effectively leveraging Kubernetes Ingress in production environments extends beyond basic configuration. It requires adherence to security best practices, an understanding of advanced traffic management patterns, and awareness of the broader ecosystem of Ingress controllers and emerging standards. Implementing a robust ingress strategy is crucial for ensuring the security, reliability, and scalability of applications.

A foundational best practice is to enforce **TLS everywhere**. All external traffic should be encrypted using HTTPS. Ingress controllers make this straightforward by centralizing TLS termination [8]. Administrators should use strong TLS protocols (e.g., TLS 1.2 and higher) and ciphers, and automate certificate management using tools like cert-manager, which integrates with Let's Encrypt to provide free, automatically renewed certificates. For enhanced security, integrating a **Web Application Firewall (WAF)** is highly recommended. Cloud-native controllers like AGIC for AKS and the AWS Load Balancer Controller for EKS offer seamless integration with Azure WAF and AWS WAF, respectively [19, 31]. These services can inspect incoming traffic and block common web exploits and malicious requests before they reach the application.

Security within the cluster is equally important. **Role-Based Access Control (RBAC)** policies should be strictly configured to limit which users and processes have permission to create, modify, or delete Ingress and IngressClass resources [9]. This prevents unauthorized changes to traffic routing. Furthermore, **NetworkPolicies** should be used to restrict which pods the Ingress controller can communicate with [8]. By default, a pod can communicate with any other pod in the cluster. A well-defined NetworkPolicy can ensure that the Ingress controller is only allowed to forward traffic to the specific backend services it is configured to expose, thereby limiting the potential blast radius in the event of a compromise.

Beyond security, there are advanced traffic management techniques that can be implemented using Ingress, although capabilities often depend on the specific controller being used. For example, many controllers support annotations for **URL rewrites and redirects**, which are useful for refactoring application endpoints without breaking client-side links [8]. More advanced controllers, particularly those based on Envoy like Istio or Contour, can facilitate sophisticated deployment strategies such as **canary releases** and **blue-green deployments** [8]. These patterns allow new versions of an application to be rolled out to a small subset of users initially, with traffic gradually shifted over as confidence in the new version grows. While the standard Ingress API has limited support for traffic splitting, controller-specific annotations or Custom Resource Definitions (CRDs) often provide this functionality.

The choice of Ingress controller is a critical decision that impacts performance, features, and operational complexity. While cloud-native controllers for AKS and EKS offer deep integration and simplified management, a wide array of third-party controllers are available [3]. The **NGINX Ingress Controller** is a mature, battle-tested, and highly popular choice known for its stability and performance [39, 40]. **Traefik** is a modern, cloud-native controller that excels in dynamic environments due to its automatic service discovery and built-in Let's Encrypt support [39, 42]. **HAProxy Ingress** is favored in high-performance scenarios that require efficient handling of large traffic volumes [40, 42]. For organizations adopting a service mesh, the **Istio Ingress Gateway** provides a powerful entry point that integrates seamlessly with the mesh's advanced traffic management, security, and observability features, though it comes with a higher degree of complexity [39, 46].

Finally, it is important to be aware of the evolution of Kubernetes networking APIs. While Ingress is a stable and widely used API, the Kubernetes community has developed the **Gateway API** as its successor [1]. The Gateway API is a more expressive, role-oriented, and extensible set of resources designed to address the limitations of the Ingress API. It provides a more granular separation of concerns between infrastructure providers (who manage Gateways), cluster operators (who manage Routes), and application developers. Many modern Ingress controllers, including the AWS Load Balancer Controller, are adding support for the Gateway API [29]. While Ingress will remain supported for the foreseeable future, organizations planning new, complex deployments should investigate the Gateway API as a more future-proof solution for their ingress needs [1, 29].

## References
1. [Ingress - Kubernetes](https://kubernetes.io/docs/concepts/services-networking/ingress/)
2. [Understanding Ingress in Kubernetes: Key Concepts and Configuration - Medium](https://medium.com/@subhampradhan966/understanding-ingress-in-kubernetes-key-concepts-and-configuration-6d5348060598)
3. [Ingress Controllers - Kubernetes](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
4. [Kubernetes Ingress Tutorial For Beginners - DevOpsCube](https://devopscube.com/kubernetes-ingress-tutorial/)
5. [Kubernetes Ingress Explained - strongDM](https://www.strongdm.com/blog/kubernetes-ingress)
6. [What is Kubernetes Ingress? - Tigera](https://www.tigera.io/learn/guides/kubernetes-networking/kubernetes-ingress/)
7. [Ingress vs. Egress: What's the Difference? - IBM](https://www.ibm.com/think/topics/ingress-vs-egress)
8. [Ingress in Kubernetes: A Complete Guide - Plural](https://www.plural.sh/blog/ingress-in-kubernetes-guide/)
9. [Ingress Controller Architecture & Kubernetes Setup - Ecosmob](https://www.ecosmob.com/ingress-controller-architecture-kubernetes-setup/)
10. [Kubernetes Ingress Overview - Medium](https://medium.com/devops-mojo/kubernetes-ingress-overview-what-is-kubernetes-ingress-introduction-to-k8s-ingress-b0f81525ffe2)
11. [IngressClass - AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/guide/ingress/ingress_class/)
12. [Basic usage - Ingress-NGINX Controller](https://kubernetes.github.io/ingress-nginx/user-guide/basic-usage/)
13. [HAProxy IngressClass Configuration - HAProxy](https://www.haproxy.com/documentation/kubernetes-ingress/community/configuration-reference/ingressclass/)
14. [networking.v1.IngressClass - Pulumi](https://www.pulumi.com/registry/packages/kubernetes/api-docs/networking/v1/ingressclass/)
15. [What is Ingress Class Name in Kubernetes? - Medium](https://medium.com/@sijomthomas05/what-is-ingress-class-name-in-kubernetes-fb6ea1fc431c)
16. [Improvements to the Ingress API in Kubernetes 1.18 - Kubernetes Blog](https://kubernetes.io/blog/2020/04/02/improvements-to-the-ingress-api-in-kubernetes-1.18/)
17. [Ingress Controller Name for the Ingress Class - Stack Overflow](https://stackoverflow.com/questions/64781320/ingress-controller-name-for-the-ingress-class)
18. [Kubernetes Ingress with Istio Ingress Gateway - Istio](https://istio.io/latest/docs/tasks/traffic-management/ingress/kubernetes-ingress/)
19. [What is Application Gateway Ingress Controller? - Microsoft Learn](https://learn.microsoft.com/en-us/azure/application-gateway/ingress-controller-overview)
20. [Tutorial: Add an Application Gateway Ingress Controller to an existing AKS cluster - Microsoft Learn](https://learn.microsoft.com/en-us/azure/application-gateway/tutorial-ingress-controller-add-on-existing)
21. [Azure/application-gateway-kubernetes-ingress - GitHub](https://github.com/Azure/application-gateway-kubernetes-ingress)
22. [Create an AKS cluster with Application Gateway Ingress Controller - Azure Docs](https://docs.azure.cn/en-us/aks/create-k8s-cluster-with-aks-application-gateway-ingress)
23. [Tutorial: Enable Application Gateway Ingress Controller add-on for a new AKS cluster - Microsoft Learn](https://learn.microsoft.com/en-us/azure/application-gateway/tutorial-ingress-controller-add-on-new)
24. [AKS and Application Gateway Ingress Controller - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/aks-agic/aks-agic)
25. [Application Gateway Ingress Controller - AGIC Docs](https://azure.github.io/application-gateway-kubernetes-ingress/)
26. [What is Application Gateway Ingress Controller? - Azure Docs CN](https://docs.azure.cn/en-us/application-gateway/ingress-controller-overview)
27. [AKS with Application Gateway Ingress Controller - Azure Quickstart Templates](https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/aks-application-gateway-ingress-controller/)
28. [Install Application Gateway Ingress Controller - AGIC Docs](https://azure.github.io/application-gateway-kubernetes-ingress/setup/install/)
29. [AWS Load Balancer Controller - Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)
30. [Install the AWS Load Balancer Controller using Helm - Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html)
31. [Deploying AWS Load Balancer Controller on Amazon EKS - AWS Networking & Content Delivery Blog](https://aws.amazon.com/blogs/networking-and-content-delivery/deploying-aws-load-balancer-controller-on-amazon-eks/)
32. [AWS Load Balancer Controller Documentation - Kubernetes SIGs](https://kubernetes-sigs.github.io/aws-load-balancer-controller/)
33. [Exposing services with AWS Load Balancer Controller - EKS Workshop](https://www.eksworkshop.com/docs/fundamentals/exposing/aws-lb-controller)
34. [kubernetes-sigs/aws-load-balancer-controller - GitHub](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
35. [AWS Load Balancer Controller on EKS Step by Step Guide - DevOpsCube](https://devopscube.com/aws-load-balancer-controller-on-eks/)
36. [Application load balancing on Amazon EKS - Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
37. [AWS Load Balancer Controller on Amazon EKS - AWS TV](https://aws.amazon.com/awstv/watch/a186e5b770b/)
38. [Install the AWS Load Balancer Controller using Kubernetes manifests - Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/lbc-manifest.html)
39. [Best Ingress Controllers for Kubernetes - Pomerium](https://www.pomerium.com/blog/best-ingress-controllers-for-kubernetes)
40. [Comparing Ingress controllers for Kubernetes (NGINX, Traefik, HAProxy, etc.) - Palark Blog](https://blog.palark.com/comparing-ingress-controllers-for-kubernetes/)
41. [Comparing Ingress controllers for Kubernetes - Palark Blog (Duplicate)](https://palark.com/blog/comparing-ingress-controllers-for-kubernetes/)
42. [NGINX vs. Traefik vs. HAProxy: Comparing Kubernetes Ingress Controllers - vcluster.com](https://www.vcluster.com/blog/nginx-vs-traefik-vs-haproxy-comparing-kubernetes-ingress-controllers)
43. [Which ingress controller do you prefer? - Reddit](https://www.reddit.com/r/kubernetes/comments/pqm6jm/which_ingress_controller_do_you_prefer/)
44. [Comparing Ingress controllers for Kubernetes - Medium](https://medium.com/flant-com/comparing-ingress-controllers-for-kubernetes-9b397483b46b)
45. [Comparing Kubernetes Ingress Solutions: Which One is Right for You? - Kubevious](https://kubevious.io/blog/post/comparing-kubernetes-ingress-solutions-which-one-is-right-for-you/)
46. [Istio vs Traefik vs Nginx: Unlocking the Secrets to Mastering Kubernetes Ingress - DEV Community](https://dev.to/sarony11/istio-vs-traefik-vs-nginx-unlocking-the-secrets-to-mastering-kubernetes-ingress-40d)
47. [Kubernetes Ingress Controllers Explained: Nginx vs Traefik vs HAProxy (2025 Edition) - Medium](https://medium.com/@canaldoagdias/kubernetes-ingress-controllers-explained-nginx-vs-traefik-vs-haproxy-2025-edition-6e288e3f7d1a)

I need a comprehensive guide about Kubernetes Ingress, specifically tailored for deployments on Azure AKS and AWS EKS. Please structure your response with the following sections:

## 1. Fundamental Concepts

- What is Kubernetes Ingress and what problem does it solve?
- How does Ingress fit into the OSI model? Explain which layers are involved and how traffic flows through each layer.

## 2. Architecture and Components

- Core Kubernetes Ingress components (Ingress resource, Ingress Controller, etc.)
- How these components interact with each other
- The relationship between Services, Pods, and Ingress

## 3. Kubernetes API Objects

- Detailed explanation of Ingress API object specifications
- IngressClass objects and their purpose
- Related objects (Services, ConfigMaps, Secrets) and how they integrate

## 4. Cloud-Specific Implementations

For both Azure AKS and AWS EKS, explain:

- Native ingress controller options (Azure Application Gateway Ingress Controller, AWS Load Balancer Controller)
- Third-party ingress controller options (NGINX, Traefik, HAProxy, Istio Gateway, etc.)
- Pros and cons of each option
- Cost implications and performance considerations

## 5. Configuration Deep-Dive

- How to configure inbound access (the "what, where, why, how"):
    - What needs to be configured (DNS, TLS/SSL, routing rules, annotations)
    - Where configurations are applied (namespace level, cluster level, cloud provider level)
    - Why each configuration is necessary
    - How to implement them with practical examples

## 6. Best Practices

- Security considerations (TLS termination, authentication, authorization)
- High availability and scalability patterns
- Monitoring and troubleshooting approaches

Please provide practical YAML examples where relevant and explain any cloud-specific nuances between AKS and EKS implementations.

Here is a comprehensive guide about Kubernetes Ingress tailored for Azure AKS and AWS EKS deployments, structured according to your requested sections:

## 1. Fundamental Concepts

### What is Kubernetes Ingress and What Problem Does It Solve

Kubernetes Ingress is a Kubernetes API resource that manages external HTTP and HTTPS access to services within a cluster. It acts as a single entry point that routes traffic to various backend services based on defined rules such as hostnames and paths. This solves the problem of exposing multiple services externally without provisioning a dedicated load balancer for each service, thereby simplifying network management and reducing costs.

### Ingress in the OSI Model

Ingress operates mainly at Layer 7 (Application Layer) of the OSI model, where it performs HTTP/HTTPS routing and routing decisions based on host headers and paths. Ingress controllers also interact with lower layers:

- Layer 4 (Transport Layer): manages TCP/UDP connections and ports.
- Layer 3 (Network Layer): handles IP addressing and routing.
Traffic flows from external clients through the Ingress Controller, which terminates TLS/SSL (Layer 7), applies routing rules, and directs requests to Services and Pods at the application layer.

## 2. Architecture and Components

### Core Kubernetes Ingress Components

- **Ingress Resource**: A Kubernetes resource defining rules for routing external traffic to backend services.
- **Ingress Controller**: A controller implementation that watches Ingress resources and enforces the routing rules. It can be NGINX, Traefik, AWS ALB Controller, Azure Application Gateway Ingress Controller, etc.
- **Services**: Abstract access to a set of Pods, which are the actual application instances.
- **Pods**: Running instances of application containers.

### Interaction Between Components

The Ingress resource declares routing rules. The Ingress Controller monitors these resources and dynamically configures the underlying load balancer or proxy to route external HTTP(S) traffic to Services. Services then forward requests to Pods.[^4][^3][^1]

### Relationship Between Services, Pods, and Ingress

- Pods run the application containers.
- Services are stable endpoints abstracting Pods.
- Ingress routes external HTTP(S) traffic to Services, which then route internally to Pods.[^3]

## 3. Kubernetes API Objects

### Ingress API Object Specification

The Ingress object includes:

- `apiVersion`, `kind`, and `metadata`.
- `spec`, where routing rules are defined, including hosts, paths, and backend services (service name and port).
- Optional TLS settings and annotations for controller-specific features.[^5][^1]

Example:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
  tls:
  - hosts:
    - example.com
    secretName: example-tls
```

### IngressClass Objects

IngressClass defines the type of Ingress Controller to use for Ingress resources. This enables multiple ingress controllers to coexist. It specifies the controller's name and parameters for the specific controller implementation.[^1]

### Related Objects

- **Services**: Define endpoints for routing.
- **ConfigMaps**: Used by some controllers for configuration settings.
- **Secrets**: Store TLS certificates for HTTPS termination.[^3][^1]

## 4. Cloud-Specific Implementations

### Azure AKS

- **Native**:
    - Azure Application Gateway Ingress Controller (AGIC): Azure-managed, features advanced traffic routing, integration with Azure Key Vault, autoscaling, and zone-resiliency.
    - Managed NGINX (Application Routing Add-on): An in-cluster NGINX controller with integration with Azure DNS and Key Vault.
- **Third-party**:
    - NGINX Ingress Controller
    - Traefik
    - HAProxy
    - Istio Gateway

**Pros/Cons**:

- AGIC: Deep Azure integration, richer features, more expensive.
- Managed NGINX: Easier setup, fine control, less Azure integration.
- Third-party offer flexibility but require more maintenance.
- Cost depends on ingress controller type; AGIC is more costly due to managed service fees, NGINX and others use node/cluster resources.[^6][^7]

### AWS EKS

- **Native**:
    - AWS Load Balancer Controller: Integrates Kubernetes ingress with AWS Application Load Balancer (ALB), supports dynamic provisioning of ALBs, automatic TLS, and WAF integration.
- **Third-party**:
    - NGINX Ingress Controller
    - Traefik
    - HAProxy
    - Istio Gateway

**Pros/Cons**:

- AWS Controller: Best for AWS-native features, automated ALB lifecycle, but limited to AWS cloud.
- Third-party controllers offer more flexibility and multi-cloud potential but may lack AWS-specific optimizations.
- Cost influenced by AWS ALB usage (managed load balancers cost on traffic/load), third-party run on cluster nodes.[^8][^9][^10]

## 5. Configuration Deep-Dive

### What to Configure

- **DNS**: Point domain or subdomains to Ingress Controller external IP or ALB DNS.
- **TLS/SSL**: Enable HTTPS termination with certificates via Kubernetes Secrets or integrated cloud services (Azure Key Vault, AWS ACM).
- **Routing rules**: Define hosts and path mappings in Ingress resources.
- **Annotations**: Configure controller-specific features like rewrite-target, timeouts, whitelist IPs.

### Where to Apply Configurations

- Namespace level: Ingress resources typically defined per namespace.
- Cluster level: IngressClass and Ingress Controller deployments are cluster-scoped.
- Cloud provider level: Managed ingress controllers (AGIC/ALB Controller) integrate with cloud resources.

### Why Configuration Is Necessary

- DNS resolves traffic to the ingress point.
- TLS secures communication.
- Routing rules direct traffic to the right backend.
- Annotations enable controller-specific behavior and optimizations.

### How to Implement (Example for AKS with NGINX)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: default
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  tls:
  - hosts:
    - myapp.contoso.com
    secretName: tls-secret
  rules:
  - host: myapp.contoso.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

AWS ALB Controller uses different annotations to specify ALB specifics like cert ARN, routing behavior.[^7][^11][^6]

## 6. Best Practices

### Security Considerations

- Enable TLS and terminate SSL at ingress.
- Use Kubernetes Secrets for cert management or cloud vault integrations.
- Set up authentication and authorization mechanisms like OAuth, JWT at ingress or upstream services.
- Use NetworkPolicies to restrict traffic.
- Integrate Web Application Firewalls (e.g., ModSecurity with NGINX).

### High Availability and Scalability

- Deploy ingress controllers in multiple replicas.
- Use cloud provider's autoscaling features.
- Use health checks and readiness probes on ingress controllers.
- For cloud-native, rely on multi-AZ (zone) deployments (AGIC, ALB).

### Monitoring and Troubleshooting

- Enable controller-specific metrics for Prometheus or cloud monitoring.
- Use detailed ingress logs and events.
- Use kubectl describe ingress and logs of ingress controllers.
- Monitor backend service health.

***

This guide should give you a strong foundational understanding and practical insights on Kubernetes Ingress across Azure AKS and AWS EKS. Specific YAML examples for ingress resources and key annotations have been included for clarity.

If you want, a follow-up with detailed Helm commands or full demo manifests can be provided. Let me know if you’d like that.

<span style="display:none">[^12][^13][^14][^15][^16][^17][^18][^19][^20]</span>

<div align="center">⁂</div>

[^1]: <https://kubernetes.io/docs/concepts/services-networking/ingress/>

[^2]: <https://konghq.com/en-gb/blog/learning-center/what-is-kubernetes-ingress>

[^3]: <https://www.plural.sh/blog/ingress-in-kubernetes-guide/>

[^4]: <https://tetrate.io/learn/kubernetes/kubernetes-ingress-example-uses-diagram>

[^5]: <https://www.solo.io/topics/api-gateway/kubernetes-ingress>

[^6]: <https://learn.microsoft.com/en-us/azure/aks/concepts-network-ingress>

[^7]: <https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/load-bal-ingress-c/create-unmanaged-ingress-controller>

[^8]: <https://aws.amazon.com/blogs/containers/exposing-kubernetes-applications-part-1-service-and-ingress-resources/>

[^9]: <https://www.strongdm.com/blog/kubernetes-ingress>

[^10]: <https://aws.amazon.com/blogs/opensource/kubernetes-ingress-aws-alb-ingress-controller/>

[^11]: <https://spacelift.io/blog/kubernetes-ingress>

[^12]: <https://www.ibm.com/think/topics/kubernetes-ingress>

[^13]: <https://dev.to/sarony11/istio-vs-traefik-vs-nginx-unlocking-the-secrets-to-mastering-kubernetes-ingress-40d>

[^14]: <https://www.vcluster.com/blog/kubernetes-nginx-ingress>

[^15]: <https://www.pulumi.com/blog/kubernetes-best-practices-i-wish-i-had-known-before/>

[^16]: <https://devopscube.com/kubernetes-ingress-tutorial/>

[^17]: <https://kubernetes.io/docs/concepts/overview/components/>

[^18]: <https://www.tigera.io/learn/guides/kubernetes-networking/kubernetes-ingress/>

[^19]: <https://www.reddit.com/r/kubernetes/comments/1gdk9vr/ingress_controllers_for_aws_eks/>

[^20]: <https://k21academy.com/docker-kubernetes/kubernetes-ingress-controllers/>
## Comprehensive Guide to Kubernetes Ingress on Azure AKS and AWS EKS

### 1. Fundamental Concepts

#### What is Kubernetes Ingress and what Problem Does it Solve

Kubernetes Ingress is an API object that manages external access to services within a cluster, typically for HTTP and HTTPS traffic[1]. It serves as a reverse proxy and load balancer at the edge of the cluster, solving the problem of exposing multiple services through a single, unified entry point without requiring a separate load balancer for each service.

Before Ingress, Kubernetes provided limited options for external access, primarily through:

- `NodePort`: Exposes a service on a static port on each cluster node
- `LoadBalancer`: Provisions an external load balancer from the cloud provider

These approaches have significant drawbacks. `NodePort` exposes services directly on node IP addresses with non-standard ports, while `LoadBalancer` creates a separate, expensive load balancer for each service, leading to cost inefficiency and management complexity.

Ingress addresses these issues by providing:

- **Protocol-aware routing**: Enables routing based on domain names, URL paths, headers, and other HTTP/HTTPS attributes
- **Single entry point**: Consolidates external access through one IP address or DNS name
- **Virtual hosting**: Allows multiple domains to be served from the same cluster via name-based virtual hosting
- **TLS termination**: Provides centralized SSL/TLS termination with certificate management
- **Load balancing**: Offers sophisticated load balancing algorithms and health checking

As stated in the official Kubernetes documentation, "The Ingress concept lets you map traffic to different backends based on rules you define via the Kubernetes API"[1]. This allows organizations to expose a wide range of microservices and applications efficiently through a single, manageable interface.

#### How Does Ingress Fit into the OSI Model? Explain Which Layers Are Involved and how Traffic Flows through Each Layer

Kubernetes Ingress operates primarily at **Layer 7 (Application Layer)** of the OSI model, with some functionality extending into Layer 4 (Transport Layer). This positioning allows it to understand and route traffic based on application-level protocols like HTTP and HTTPS.

The OSI model specifies seven layers:

1. Physical
2. Data Link
3. Network
4. Transport
5. Session
6. Presentation
7. Application

Ingress functions at the highest layer, the Application Layer, which is responsible for network services to applications. This enables it to inspect and act upon HTTP-specific information such as:

- Host headers for virtual hosting
- URL paths for routing
- Request methods (GET, POST, etc.)
- HTTP headers for advanced routing
- Cookies for session affinity

Some Ingress controllers also support Layer 4 functionality through features like TLS termination. While TLS encryption occurs at the Presentation Layer (Layer 6), the termination and re-encryption process involves Ingress controllers inspecting transport layer information during the SSL/TLS handshake.

The typical traffic flow through the OSI layers when using Kubernetes Ingress is as follows:

1. **Application Layer (L7)**: Client makes an HTTP request to a domain name (e.g., `api.example.com/v1/users`)
2. **DNS Resolution**: Domain name resolved to the Ingress controller's IP address
3. **Transport Layer (L4)**: TCP connection established to the Ingress controller on port 80 (HTTP) or 443 (HTTPS)
4. **Network Layer (L3)**: IP packets routed through the network to the Ingress controller
5. **Data Link & Physical Layers (L2/L1)**: Packets transmitted over the physical network media
6. **Application Layer (L7)**: Ingress controller receives the HTTP request and examines:
    
    - Host header (`api.example.com`)
    - URL path (`/v1/users`)
    - HTTPS certificate (if TLS is used)
7. **Ingress Controller Processing**: Based on configured rules, the controller determines the appropriate backend service
8. **Service Routing (L3/L4)**: Kubernetes Service directs traffic to available Pods using IP tables or IPVS
9. **Pod Communication**: Request is forwarded to the appropriate Pod, potentially through multiple hops depending on the networking model (CNI)

For HTTPS traffic, additional steps occur:

- The client establishes a TLS connection with the Ingress controller
- The Ingress controller terminates TLS and decrypts the request
- The decrypted HTTP request is processed according to routing rules
- The request is forwarded to the backend service, which may be over plain HTTP (edge termination) or re-encrypted for end-to-end encryption

This Layer 7 focus distinguishes Ingress from other Kubernetes service types like `NodePort` and `LoadBalancer`, which operate primarily at Layer 4. The application-aware nature of Ingress enables sophisticated routing patterns that would be impossible at lower network layers.

### 2. Architecture and Components

#### Core Kubernetes Ingress Components (Ingress Resource, Ingress Controller, etc.)

The Kubernetes Ingress architecture consists of several core components that work together to provide external access to cluster services:

##### Ingress Resource

The Ingress resource is a Kubernetes API object (`networking.k8s.io/v1/Ingress`) that defines the rules for routing external traffic to services within the cluster[1]. It acts as a declarative configuration for the desired routing behavior. The Ingress resource itself does not process traffic; it serves as a specification that the Ingress controller implements.

Key characteristics of the Ingress resource:

- Contains routing rules based on hostnames and URL paths
- Can specify TLS configuration for HTTPS termination
- Is namespace-scoped, allowing different teams to manage their own ingress rules
- Supports annotations for controller-specific configuration

##### Ingress Controller

The Ingress controller is a software component that watches for Ingress resources in the Kubernetes API and implements their routing rules[2]. It typically exposes a load balancer (either cloud-based or software-based) that receives external traffic and routes it according to the Ingress rules.

The Ingress controller:

- Runs as one or more Pods in the cluster, often in a dedicated namespace
- Watches the Kubernetes API for Ingress resources across namespaces
- Translates Ingress rules into configuration for the underlying load balancer
- Manages the lifecycle of external load balancing resources
- Handles health checking of backend services

Unlike other Kubernetes controllers that run as part of the core `kube-controller-manager`, Ingress controllers are separate components that must be explicitly deployed[2]. Popular implementations include NGINX, Traefik, AWS Load Balancer Controller, and Azure Application Gateway Ingress Controller.

##### IngressClass

Introduced in Kubernetes 1.18, the IngressClass is a cluster-scoped API object that defines the class or type of Ingress controller that should implement Ingress resources[1]. It provides a way to specify which controller should handle a particular Ingress, enabling multiple controllers to coexist in the same cluster.

The IngressClass object:

- Is a cluster-scoped resource
- References a specific Ingress controller implementation
- Can include parameters for controller-specific configuration
- Allows marking a class as default for Ingresses without an explicit class reference

This architecture enables organizations to have different Ingress controllers for different purposes (e.g., one for public internet traffic and another for internal API routing) with clear separation of concerns.

#### How These Components Interact with Each other

The interaction between Ingress components follows a clear workflow that begins with configuration and ends with traffic routing:

1. **Ingress Class Definition**: An administrator first defines one or more IngressClass resources in the cluster. These specify which Ingress controller implementation should handle Ingress resources of that class. For example, an `aws-alb` IngressClass would be configured to use the AWS Load Balancer Controller[3].
2. **Ingress Controller Deployment**: The Ingress controller is deployed to the cluster, typically using Helm charts or YAML manifests. The controller Pod(s) start running and establish connections to the Kubernetes API server to watch for Ingress resources[7].
3. **Ingress Resource Creation**: A developer or operations team creates an Ingress resource in their application namespace. This resource includes:
    
    - Routing rules (hosts, paths)
    - Reference to an IngressClass (or relies on a default)
    - TLS configuration (if needed)
    - Controller-specific annotations
4. **Controller Watches API**: The Ingress controller continuously watches the Kubernetes API for Ingress resources that match its class. When a new Ingress is created or an existing one is modified, the controller receives this event.
5. **Rule Translation and Provisioning**: The controller translates the Ingress rules into configuration for its underlying load balancing implementation. For cloud-native controllers, this may involve creating or updating cloud resources like AWS Application Load Balancers or Azure Application Gateways[6].
6. **Load Balancer Configuration**: The controller configures the load balancer with:
    
    - Listener rules for each hostname and path combination
    - Target groups pointing to the appropriate Kubernetes Services
    - Security policies (HTTPS, WAF rules)
    - Health checks for backend services
7. **Traffic Routing**: When external traffic arrives at the load balancer:
    
    - The load balancer receives the request at Layer 4 (TCP) or Layer 7 (HTTP/HTTPS)
    - Based on the configured rules, it forwards the request to appropriate backend service endpoints
    - The request flows through the Kubernetes Service to one or more Pod instances
    - Responses follow the reverse path back to the client
8. **Status Updates**: The Ingress controller updates the status field of the Ingress resource with information such as the allocated load balancer IP address or DNS name, making this information available to other tools or users.

This interaction sequence creates a declarative workflow where users specify their desired routing state, and the Ingress controller continuously works to make the actual state match this desired state, following Kubernetes' reconciliation model.

#### The Relationship between Services, Pods, and Ingress

The relationship between Services, Pods, and Ingress follows a clear hierarchy that enables scalable and maintainable application architectures:

##### Pod to Service Relationship

Pods are the smallest deployable units in Kubernetes, representing individual instances of an application. Services provide a stable network endpoint that abstracts over the dynamic lifecycle of Pods, which can be created, destroyed, or rescheduled at any time[1].

Key aspects of this relationship:

- Services use label selectors to identify which Pods should receive traffic
- Services provide a stable ClusterIP that doesn't change even as underlying Pods are replaced
- Services handle load balancing across multiple Pod instances
- Services can be accessed within the cluster using their DNS name (`service.namespace.svc.cluster.local`)

##### Service to Ingress Relationship

Ingress sits above Services in the networking stack, providing external access to Services that are otherwise only accessible within the cluster[1]. While Services can be exposed externally using `NodePort` or `LoadBalancer` types, Ingress provides a more sophisticated and efficient approach.

Key aspects of this relationship:

- Ingress rules reference Services by name and namespace as backend targets
- Each path rule in an Ingress specifies which Service and port should handle matching requests
- Ingress can route to different Services based on hostnames or URL paths
- Ingress serves as a single entry point for multiple Services, reducing the need for multiple external load balancers

For example, a single Ingress might route:

- Requests to `api.example.com/v1/*` to an `api-service` on port 8000
- Requests to `web.example.com/*` to a `web-service` on port 80
- Requests to `admin.example.com/*` to an `admin-service` on port 3000

All of these routes terminate at the same Ingress controller and external load balancer, but are directed to different internal Services.

##### End-to-End Flow

The complete traffic flow from external client to application Pod is:

1. **External Client**: Makes an HTTP request to a domain name (e.g., `web.example.com`)
2. **DNS**: Resolves to the Ingress controller's public IP or DNS entry
3. **Ingress Controller**: Receives the request and applies routing rules based on Ingress configuration
4. **Service**: Ingress forwards the request to the appropriate Service based on the matched rule
5. **Endpoint**: The Service uses its label selector to identify matching Pods
6. **Pod**: The request is delivered to one of the available Pod instances
7. **Response**: The response travels back through the same path to the client

This layered approach provides several benefits:

- **Abstraction**: Changes to Pod implementations don't affect external routing
- **Scalability**: Services can scale independently based on their workload
- **Flexibility**: Ingress can implement complex routing patterns across multiple Services
- **Security**: Network policies can be applied at each layer
- **Maintainability**: Different teams can manage their own Services and Ingress rules within their namespaces

The typical pattern for a production application is to expose Services internally using `ClusterIP` type and then expose them externally through Ingress rules, rather than making each Service directly accessible from outside the cluster.

### 3. Kubernetes API Objects

#### Detailed Explanation of Ingress API Object Specifications

The Kubernetes Ingress API object is a powerful configuration resource that defines how external HTTP(S) traffic should be routed to services within the cluster. The current stable version is `networking.k8s.io/v1`, which was introduced in Kubernetes 1.19[1].

A minimal Ingress specification includes the following key fields:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
spec:
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

##### Key Fields in Ingress Specification

**rules**: The primary field that defines the routing behavior. It contains one or more HTTP routing rules, each with:

- **http**: Specifies that these are HTTP routing rules (currently the only supported protocol)
- **paths**: An array of path-based rules, each containing:
    - **path**: The URL path to match (e.g., `/api/v1`, `/static`)
    - **pathType**: The matching strategy, which can be:
        - `Prefix`: Matches URL path prefixes
        - `Exact`: Matches the path exactly
        - `ImplementationSpecific`: Behavior depends on the Ingress controller
    - **backend**: Defines the service that should handle requests matching this rule, with:
        - **service.name**: The name of the Kubernetes Service
        - **service.port.number**: The port on which the service is listening

**ingressClassName**: References an IngressClass resource that specifies which controller should implement this Ingress[1]. This field replaces the older `kubernetes.io/ingress.class` annotation and allows for more sophisticated controller selection.

**tls**: Configures TLS termination for HTTPS traffic. This section includes:

- **hosts**: One or more hostnames for which TLS should be enabled
- **secretName**: The name of a Kubernetes Secret containing the TLS certificate and private key

```yaml
tls:
- hosts:
  - secure.example.com
  secretName: example-tls-secret
```

The Secret must contain `tls.crt` and `tls.key` data fields with the certificate and private key in PEM format[1]. TLS termination occurs at the Ingress controller, meaning traffic between the controller and backend services is typically unencrypted.

**defaultBackend**: Defines a backend to handle requests that don't match any of the specified rules. This is often used for custom 404 pages or global fallback services:

```yaml
defaultBackend:
  service:
    name: default-backend
    port:
      number: 80
```

If no default backend is specified, the behavior depends on the Ingress controller implementation.

##### Path Matching and Host Rules

Ingress supports sophisticated path matching through the `pathType` field. The three available path types offer different matching behaviors:

- **Prefix**: Matches based on path element prefixes. For example, a prefix of `/foo` matches `/foo`, `/foo/`, and `/foo/bar`, but not `/foobar`[1]. This is the most commonly used path type for API versioning and static file serving.
- **Exact**: Performs exact string matching with case sensitivity. A rule with `path: /foo` and `pathType: Exact` will match requests to `/foo` but not `/foo/` or `/foobar`.
- **ImplementationSpecific**: Allows the Ingress controller to define its own matching behavior, which may or may not follow the standard prefix or exact semantics.

Host-based routing allows different domains to be served from the same Ingress:

```yaml
rules:
- host: api.example.com
  http:
    paths:
    - path: /v1
      pathType: Prefix
      backend:
        service:
          name: api-v1-service
          port:
            number: 80
- host: www.example.com
  http:
    paths:
    - path: /
      pathType: Prefix
      backend:
        service:
          name: web-service
          port:
            number: 80
```

This configuration enables a single Ingress to serve both an API endpoint and a web application on different subdomains.

##### Wildcard Hosts

Ingress also supports wildcard hosts for more flexible domain matching:

```yaml
rules:
- host: "*.example.com"
  http:
    paths:
    - path: /
      pathType: Prefix
      backend:
        service:
          name: wildcard-service
          port:
            number: 80
```

Wildcard matching follows DNS conventions, where `*.example.com` matches `sub1.example.com` and `sub2.example.com`, but does not match `example.com` or `deep.sub1.example.com`[1].

#### IngressClass Objects and Their Purpose

The IngressClass API object, introduced in Kubernetes 1.19, provides a standardized way to specify which Ingress controller should implement a given Ingress resource[1]. This replaces the older, non-standard annotation-based approach and enables more robust multi-controller scenarios.

An IngressClass is defined with the following structure:

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: nginx
spec:
  controller: k8s.io/ingress-nginx
```

##### Key Components of IngressClass

**controller**: This required field specifies the implementation of the controller that should process Ingress resources with this class. The value follows the format `domain/name`, where:

- `k8s.io/ingress-nginx` for the NGINX Ingress Controller
- `ingress.k8s.aws/alb` for the AWS Load Balancer Controller
- `application-gateway.kubernetes.io/ingress-controller` for Azure Application Gateway Ingress Controller

The controller field allows cluster administrators to define exactly which software implementation will handle Ingress resources of this class[1].

**parameters**: An optional field that references additional configuration resources for the controller. This can include:

- Cluster-scoped parameters (specified with `scope: Cluster`)
- Namespaced parameters (specified with `scope: Namespace`)

```yaml
spec:
  controller: example.com/ingress-controller
  parameters:
    scope: Namespace
    apiGroup: k8s.example.com
    kind: IngressParameter
    namespace: external-configuration
    name: external-config
```

This feature allows for shared configuration across multiple Ingress classes while maintaining appropriate access controls.

**default IngressClass**: A cluster can have one IngressClass marked as default by adding the annotation `ingressclass.kubernetes.io/is-default-class: "true"`[1]. When an Ingress resource is created without an `ingressClassName` field, the default IngressClass is automatically assigned to it.

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: nginx-default
  annotations:
    ingressclass.kubernetes.io/is-default-class: "true"
spec:
  controller: k8s.io/ingress-nginx
```

Having exactly one default IngressClass is recommended to avoid ambiguity in Ingress resource handling.

##### Purpose and Benefits

The IngressClass serves several important purposes:

1. **Controller Selection**: Allows explicit selection of which Ingress controller should handle a particular Ingress resource, enabling multiple controllers to coexist in the same cluster.
2. **Standardization**: Provides a consistent, API-based mechanism for controller selection across different Kubernetes distributions and cloud providers.
3. **Flexibility**: Enables scenarios where different controllers are needed for different purposes, such as:
    
    - A cloud-native controller for public internet traffic
    - A service mesh gateway for internal traffic
    - Different controllers for different security requirements
4. **Configuration Management**: Supports both cluster-wide and namespace-scoped parameter management, allowing for appropriate delegation of control.
5. **Future Compatibility**: Aligns with the broader Kubernetes pattern of using CRDs for extensible functionality and prepares for integration with the newer Gateway API.

#### Related Objects (Services, ConfigMaps, Secrets) and how They Integrate

Kubernetes Ingress functionality depends on several related API objects that provide the necessary services, configuration, and security credentials. These objects integrate seamlessly to create a complete external access solution.

##### Services

Services are fundamental to Ingress operation, serving as the direct targets for traffic routing. Every path rule in an Ingress must reference a Service by name and namespace. The Service then routes traffic to appropriate Pods based on its label selector.

```yaml
# Backend Service
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP  # This is the default and recommended type
```

```yaml
# Ingress referencing the Service
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

The integration between Ingress and Services is bi-directional:

- Ingress references Services for routing decisions
- Services provide endpoints that Ingress can route to
- When Services change (e.g., new Pods are added), Ingress controllers automatically update their configuration through the Kubernetes API

While Services can be of type `LoadBalancer` or `NodePort`, it's generally best practice to use `ClusterIP` for Services that are exposed through Ingress, avoiding the creation of unnecessary external load balancers.

##### ConfigMaps

ConfigMaps are used to provide configuration to Ingress controllers, allowing customization of their behavior beyond what is possible through the Ingress resource specification. The most common use is for NGINX Ingress Controller, which uses a ConfigMap to store global configuration settings:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: ingress-nginx
data:
  # Global NGINX configuration
  client-body-buffer-size: "64k"
  client-header-buffer-size: "16k"
  server-tokens: "false"
  # Timeout settings
  proxy-connect-timeout: "30"
  proxy-send-timeout: "150"
  proxy-read-timeout: "150"
  # Compression
  gzip-level: "5"
  # Security headers
  enable-underscores-in-headers: "true"
  add-headers: |
    X-Frame-Options: DENY
    X-Content-Type-Options: nosniff
```

This ConfigMap is typically mounted into the Ingress controller Pods and loaded at startup. Different Ingress controllers have different approaches to configuration:

- NGINX Ingress Controller uses ConfigMaps for most configuration
- Traefik can use ConfigMaps, but often relies on command-line arguments or CRDs
- Cloud-native controllers (ALB, AGIC) may use ConfigMaps for specific settings but primarily rely on cloud provider configurations

ConfigMaps provide a flexible way to adjust controller behavior without requiring changes to the controller deployment itself, enabling easier management and updates.

##### Secrets

Secrets are crucial for securing Ingress with TLS/SSL, storing the sensitive certificate information that would be inappropriate for ConfigMaps. The most common use is for HTTPS termination, where a Secret contains the TLS certificate and private key:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: example-tls-secret
  namespace: default
type: kubernetes.io/tls
data:
  tls.crt: base64-encoded-certificate-data
  tls.key: base64-encoded-private-key-data
```

This Secret can then be referenced in an Ingress resource:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
spec:
  tls:
  - hosts:
    - secure.example.com
    secretName: example-tls-secret
  rules:
  - host: secure.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

Secrets integrate with Ingress in several ways:

- **TLS Termination**: As shown above, for HTTPS certificates
- **Authentication**: Some Ingress controllers support basic authentication using Secrets to store username/password pairs
- **Controller Configuration**: Ingress controllers themselves may use Secrets for configuration, such as:
    - Azure AD credentials for authentication annotations
    - ACM or Key Vault access credentials
    - OAuth client secrets for external authentication providers

The integration between Ingress and these related objects creates a comprehensive system for managing external access, with each component fulfilling a specific role:

- Ingress defines the routing rules and external interface
- Services provide the internal endpoints and Pod abstraction
- ConfigMaps configure the controller's behavior and global settings
- Secrets secure the connection with encryption and authentication

### 4. Cloud-Specific Implementations

#### Azure AKS

Azure Kubernetes Service (AKS) offers several options for Ingress, ranging from native integration with Azure services to popular third-party controllers. The choice depends on requirements for performance, security, cost, and operational complexity.

##### Native Ingress Controller Options: Azure Application Gateway Ingress Controller (AGIC)

The Azure Application Gateway Ingress Controller (AGIC) is the native solution for AKS, integrating directly with Azure Application Gateway, a Layer 7 application delivery controller[6]. AGIC enables AKS customers to leverage Azure's managed L7 load balancer to expose applications to the internet.

**Key Features and Architecture:**

- Direct pod connectivity using private IP addresses, eliminating the need for NodePort services or kube-proxy routing
- End-to-end TLS support with SNI
- Integration with Azure Web Application Firewall (WAF) for security
- URL routing, cookie-based affinity, and gzip compression
- Autoscaling capabilities when using Standard_v2 or WAF_v2 SKUs
- Support for public, private, and hybrid website scenarios

AGIC runs as a pod within the AKS cluster and continuously monitors Kubernetes resources for changes[6]. It translates Ingress resources into Application Gateway configuration via the Azure Resource Manager (ARM) API, eliminating the need for a separate load balancer or public IP address in front of the AKS cluster.

**Deployment Options:**  
AGIC can be deployed in two ways:

1. **AKS Add-on**: A fully managed service integrated directly into AKS. This is simpler to set up and automatically receives updates from Microsoft. It can be enabled with a single Azure CLI command when creating a new AKS cluster.
2. **Helm Deployment**: A self-managed deployment using Helm charts, offering more control and flexibility, including support for "ProhibitedTargets" that allows AGIC to configure Application Gateway for AKS without affecting other existing backends[6].

**Supported Networking Models:**  
AGIC supports several AKS networking options:

- Kubenet
- Azure CNI
- Azure CNI Overlay

Azure CNI and Azure CNI Overlay are recommended for better performance and VNET IP conservation. However, CNI Overlay has specific requirements:

- AGIC version v1.9.1 or later
- Application Gateway subnet must be a /24 or smaller
- Subnet delegation to Microsoft.Network/applicationGateways[6]

##### Third-party Ingress Controller Options

While AGIC is the native option, AKS supports various third-party ingress controllers for organizations that need different features or want to maintain consistency across cloud providers.

**NGINX Ingress Controller:**  
One of the most popular open-source ingress controllers, NGINX offers extensive configurability and a wide range of features:

- Customizable NGINX configuration through ConfigMaps
- Advanced routing rules with regular expressions
- Extensive annotation support
- Integration with cert-manager for automated TLS
- Extensive community and documentation

Can be deployed via Helm or YAML manifests:

```bash
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

**Traefik:**  
A modern ingress controller known for its simplicity and good observability features:

- Built-in dashboard and metrics
- Native support for Let's Encrypt
- Dynamic configuration without reloads
- Good Kubernetes integration

**HAProxy:**  
A high-performance option suitable for high-throughput scenarios:

- Excellent performance under heavy load
- Advanced load balancing algorithms
- Comprehensive health checking

**Istio Gateway:**  
For organizations using or considering a service mesh:

- Native integration with Istio service mesh
- Advanced traffic management and security policies
- Request tracing and observability
- Mutual TLS between services

##### Pros and Cons of Each Option

**AGIC (AKS Add-on):**  
*Pros:*

- Fully managed and automatically updated
- Simpler setup and operation
- Deep native integration with Azure services
- Built-in WAF and security features
- Autoscaling capabilities[6]

*Cons:*

- Less flexible than Helm deployment
- Single add-on per cluster limitation
- No support for ProhibitedTargets
- Cannot modify certain deployment values[6]

**AGIC (Helm):**  
*Pros:*

- More control over configuration
- Support for ProhibitedTargets
- Can be manually updated
- Greater flexibility in deployment scenarios[6]

*Cons:*

- Manual updates required
- More complex initial setup
- Self-managed, so operational responsibility rests with the team

**Third-party Controllers (NGINX, Traefik, etc.):**  
*Pros:*

- Cloud-agnostic, easier for multi-cloud strategies
- Extensive community support and documentation
- More customizable
- Often better integration with observability tools
- Can be consistent across different Kubernetes environments

*Cons:*

- Less native integration with Azure services
- Additional operational overhead
- May require separate load balancer provisioning
- No built-in WAF (unless using service mesh)

##### Cost Implications and Performance Considerations

**Cost Implications:**

- **Application Gateway**: Priced based on instance size (vCPU, memory), number of rules, and data processed. The Standard_v2 SKU offers autoscaling, which can optimize costs during traffic fluctuations but requires monitoring to avoid unexpected scaling.
- **WAF**: Adds additional cost on top of Application Gateway, with pricing based on throughput and rules.
- **Third-party controllers**: While the software is often free, they typically require a separate cloud load balancer (Application Load Balancer, Standard Load Balancer), incurring additional costs.
- **AGIC Add-on**: No additional licensing cost, but still subject to Application Gateway pricing.

For workloads with predictable traffic patterns, fixed-size Application Gateway instances may be more cost-effective. For variable workloads, autoscaling can provide cost savings but requires careful configuration to avoid over-provisioning.

**Performance Considerations:**

- **AGIC with Standard_v2**: Offers autoscaling from 10 to 125 instances, providing good elasticity for traffic spikes. Can handle up to 4 million concurrent connections.
- **Direct pod connectivity**: Eliminates hairpinning through nodes, reducing latency and improving performance.
- **TLS offloading**: Performing TLS termination at the Application Gateway level frees up application resources.
- **Caching**: Application Gateway provides built-in content caching capabilities.
- **Global Reach**: Can be combined with Azure Front Door for global load balancing and DDoS protection.

For high-performance scenarios, especially those requiring low latency or high throughput, careful consideration of the networking model and instance size is essential. Azure CNI Overlay can provide better performance for large clusters but has more restrictive subnet requirements.

#### AWS EKS

Amazon Elastic Kubernetes Service (EKS) provides robust Ingress capabilities through both native AWS services and integration with popular third-party controllers. The implementation follows AWS's philosophy of deep integration with native cloud services while maintaining compatibility with standard Kubernetes patterns.

##### Native Ingress Controller Options: AWS Load Balancer Controller

The AWS Load Balancer Controller (ALBC) is the official, fully-supported ingress controller for EKS, managing Elastic Load Balancers for Kubernetes clusters[3]. It satisfies Kubernetes Ingress resources by creating and managing AWS Application Load Balancers (ALB), which are Layer 7 load balancers designed for HTTP/HTTPS traffic.

**Key Features and Architecture:**

- Creates Application Load Balancers (ALB) for Ingress resources
- Creates Network Load Balancers (NLB) for Services of type LoadBalancer
- Supports Gateway API from version 2.14.0, providing a more comprehensive configuration model
- Integrates with AWS Certificate Manager (ACM) for certificate management
- Works with Route 53 for DNS integration
- Supports both instance and IP target types for NLB, with version 2.3.0 or later[3]
- Uses Kubernetes annotations to configure advanced load balancer features

The controller watches for Ingress and Service resources in the cluster and creates the corresponding AWS load balancing resources. It handles the full lifecycle management, including creation, updates, and deletion.

**Deployment Options:**  
The AWS Load Balancer Controller can be installed via:

1. **Helm**: Recommended for new deployments, simplifying the installation process[19]
2. **Kubernetes Manifests**: Required for clusters with restricted access to public container registries[21]

Both methods require preliminary setup including:

- IAM permissions for the controller to manage AWS resources
- Installation of cert-manager (for webhook functionality)
- Proper network configuration

The controller has largely replaced the legacy ALB Ingress Controller and is now the default for new EKS clusters. From version 2.5 onwards, it becomes the default controller for Service resources with `type: LoadBalancer`, automatically creating NLBs instead of Classic Load Balancers[3].

##### Third-party Ingress Controller Options

EKS supports all major third-party ingress controllers, with NGINX and Traefik being particularly popular due to their maturity and feature sets.

**NGINX Ingress Controller:**  
A widely-used option that can be deployed on EKS using YAML manifests designed for AWS:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.0/deploy/static/provider/aws/deploy.yaml
```

Key AWS-specific considerations:

- Can integrate with AWS NLB through annotations
- Supports PROXY protocol to preserve client IP addresses
- Can be configured for TLS termination in the NLB rather than the controller[8]

**Traefik:**  
Provides excellent integration with Kubernetes and supports Ingress resources directly:

- Simple deployment via Helm
- Built-in observability and dashboards
- Native Let's Encrypt support
- Can be configured to work with AWS load balancer features

**HAProxy:**  
Known for high performance and reliability:

- Excellent for high-throughput, low-latency scenarios
- Advanced health checking capabilities
- Configurable via Kubernetes CRDs

**Istio Gateway:**  
For organizations implementing a service mesh:

- Full integration with Istio's traffic management features
- Advanced security policies including mutual TLS
- Request tracing and observability
- Can coexist with other ingress controllers for different traffic types

##### Pros and Cons of Each Option

**AWS Load Balancer Controller:**  
*Pros:*

- Native integration with AWS services
- Automatic ACM certificate management
- Direct Route 53 integration
- Gateway API support for advanced configuration
- Fully supported by AWS
- Eliminates the need for a separate reverse proxy layer
- Seamless integration with AWS security features (WAF, Shield)

*Cons:*

- Limited to AWS environments
- Less flexible than software-based controllers
- Requires additional IAM permissions and setup
- Configuration primarily through annotations rather than CRDs
- May be overkill for simple use cases

**Third-party Controllers:**  
*Pros:*

- Portable across cloud providers
- More extensive feature sets in some cases
- Better integration with observability tools
- Often easier to customize and extend
- Larger community support and documentation

*Cons:*

- Additional operational overhead
- May require provisioning separate AWS load balancers
- Less native integration with AWS services
- Potentially higher latency due to additional hops
- Need for separate certificate management solutions

##### Cost Implications and Performance Considerations

**Cost Implications:**

- **Application Load Balancer**: $0.0225 per ALB-hour + $0.008 per LCU-hour (Load Balancer Capacity Unit)[3]
- **Network Load Balancer**: $0.0225 per NLB-hour + data processing charges
- Costs scale with traffic volume, number of rules, and active connections
- LCU usage is the primary cost driver for ALB, with charges based on:
    - New connections per minute
    - Active connections per minute
    - Rule evaluations per second (for rules beyond the first 10)
    - Processed bytes (for first 1 GB per ALB-hour)

For cost optimization:

- Use target groups efficiently, sharing them across multiple Ingress rules when possible
- Minimize the number of routing rules, especially in ALB
- Consider using NLB for high-throughput TCP/UDP traffic, which has simpler pricing
- Monitor LCU usage carefully to avoid unexpected costs
- Use the AWS Load Balancer Controller's ability to create a single ALB for multiple Ingress resources (when they share the same host)

**Performance Considerations:**

- **ALB**: Designed for HTTP/HTTPS with advanced routing capabilities, supports host-based and path-based routing, WebSockets, and HTTP/2. Can handle millions of requests

References:  
[1]: [https://kubernetes.io/docs/concepts/services-networking/ingress/](https://kubernetes.io/docs/concepts/services-networking/ingress/)  
[2]: [https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)  
[3]: [https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)  
[4]: [https://cert-manager.io/docs/usage/ingress/](https://cert-manager.io/docs/usage/ingress/)  
[5]: [https://doc.traefik.io/traefik/reference/install-configuration/providers/kubernetes/kubernetes-ingress/](https://doc.traefik.io/traefik/reference/install-configuration/providers/kubernetes/kubernetes-ingress/)  
[6]: [https://learn.microsoft.com/en-us/azure/application-gateway/ingress-controller-overview](https://learn.microsoft.com/en-us/azure/application-gateway/ingress-controller-overview)  
[7]: [https://kubernetes.github.io/ingress-nginx/](https://kubernetes.github.io/ingress-nginx/)  
[8]: [https://kubernetes.github.io/ingress-nginx/deploy/](https://kubernetes.github.io/ingress-nginx/deploy/)  
[9]: [https://doc.traefik.io/traefik/providers/kubernetes-ingress/](https://doc.traefik.io/traefik/providers/kubernetes-ingress/)  
[10]: [https://kubernetes.io/docs/home/](https://kubernetes.io/docs/home/)  
[11]: [https://www.armosec.io/blog/kubernetes-ingress-beginners-guide/](https://www.armosec.io/blog/kubernetes-ingress-beginners-guide/)  
[12]: [https://ashadali.medium.com/ingress-hands-on-part-1-aace766f247e](https://ashadali.medium.com/ingress-hands-on-part-1-aace766f247e)  
[13]: [https://www.vcluster.com/blog/advanced-guide-to-kubernetes-ingress-controllers](https://www.vcluster.com/blog/advanced-guide-to-kubernetes-ingress-controllers)  
[14]: [https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration)  
[15]: [https://www.plural.sh/blog/ingress-kubernetes-guide/](https://www.plural.sh/blog/ingress-kubernetes-guide/)  
[16]: [https://www.cncf.io/blog/2019/05/10/kubernetes-core-concepts/](https://www.cncf.io/blog/2019/05/10/kubernetes-core-concepts/)  
[17]: [https://spacelift.io/blog/kubernetes-tutorial](https://spacelift.io/blog/kubernetes-tutorial)  
[18]: [https://kubernetes-sigs.github.io/aws-load-balancer-controller/](https://kubernetes-sigs.github.io/aws-load-balancer-controller/)  
[19]: [https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html)  
[20]: [https://docs.aws.amazon.com/eks/latest/best-practices/load-balancing.html](https://docs.aws.amazon.com/eks/latest/best-practices/load-balancing.html)  
[21]: [https://docs.aws.amazon.com/eks/latest/userguide/lbc-manifest.html](https://docs.aws.amazon.com/eks/latest/userguide/lbc-manifest.html)  
[22]: [https://github.com/kubernetes-sigs/aws-load-balancer-controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller)  
[23]: [https://www.eksworkshop.com/docs/fundamentals/exposing/aws-lb-controller](https://www.eksworkshop.com/docs/fundamentals/exposing/aws-lb-controller)  
[24]: [https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/)  
[25]: [https://repost.aws/knowledge-center/eks-alb-ingress-controller-fargate](https://repost.aws/knowledge-center/eks-alb-ingress-controller-fargate)  
[26]: [https://devopscube.com/aws-load-balancer-controller-on-eks/](https://devopscube.com/aws-load-balancer-controller-on-eks/)  
[27]: [https://cert-manager.io/docs/tutorials/acme/nginx-ingress/](https://cert-manager.io/docs/tutorials/acme/nginx-ingress/)  
[28]: [https://hbayraktar.medium.com/installing-cert-manager-and-nginx-ingress-with-lets-encrypt-on-kubernetes-fe0dff4b1924](https://hbayraktar.medium.com/installing-cert-manager-and-nginx-ingress-with-lets-encrypt-on-kubernetes-fe0dff4b1924)  
[29]: [https://dev.to/aws-builders/kubernetes-ingress-playlist-part-6-securing-the-kubernetes-ingress-using-cert-manager-with-https-cde](https://dev.to/aws-builders/kubernetes-ingress-playlist-part-6-securing-the-kubernetes-ingress-using-cert-manager-with-https-cde)  
[30]: [https://marcinkujawski.pl/how-to-secure-kubernetes-ingress-with-cert-manager-and-auto-enrolled-certificates/](https://marcinkujawski.pl/how-to-secure-kubernetes-ingress-with-cert-manager-and-auto-enrolled-certificates/)  
[31]: [https://cert-manager.io/docs/getting-started/](https://cert-manager.io/docs/getting-started/)  
[32]: [https://github.com/sebinxavi/Kubernetes-Ingress-controller-with-SSL-Cert-Manager](https://github.com/sebinxavi/Kubernetes-Ingress-controller-with-SSL-Cert-Manager)  
[33]: [https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nginx-ingress-with-cert-manager-on-digitalocean-kubernetes](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nginx-ingress-with-cert-manager-on-digitalocean-kubernetes)
