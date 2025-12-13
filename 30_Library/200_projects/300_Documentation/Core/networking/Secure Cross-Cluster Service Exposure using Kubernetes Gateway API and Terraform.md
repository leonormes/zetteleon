---
aliases: []
confidence: 
created: 2025-03-27T12:34:09Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [gateway, ingress, k8s, networking]
title: Secure Cross-Cluster Service Exposure using Kubernetes Gateway API and Terraform
type: plan
uid: 
updated: 
version: 
---

## 1\. Introduction

### Problem Statement

Organizations increasingly adopt multi-cloud strategies, deploying workloads across different cloud providers like AWS and Azure. This often necessitates secure and efficient communication between services running in disparate environments. In this specific scenario, there is a requirement to expose a service named 'relay', currently running within an AWS Elastic Kubernetes Service (EKS) cluster, to a remote Azure Kubernetes Service (AKS) cluster. The primary objectives are to achieve this connectivity in a secure and simple manner. This document outlines a spike investigation into a potential solution leveraging the Kubernetes Gateway API for traffic management and Terraform for infrastructure provisioning.

### Proposed Solution

The proposed solution centres around utilizing the Kubernetes Gateway API as the primary mechanism for exposing and routing traffic between the EKS and AKS clusters. The Gateway API offers a modern, flexible, and extensible approach to managing Kubernetes service networking, surpassing the capabilities of the older Ingress API. Complementing this, Terraform, an infrastructure-as-code tool, will be employed to provision and configure the necessary resources within both the AWS and Azure environments, ensuring consistency and repeatability. This combination aims to provide a secure and relatively straightforward method for enabling cross-cluster communication.

### Scope Of the Spike

This investigation encompasses several key areas to determine the viability and optimal implementation of the proposed solution:

- Researching the fundamental concepts and advantages of the Kubernetes Gateway API in the context of exposing services 1.
- Investigating the implementation of the Kubernetes Gateway API within an AWS EKS cluster, including the selection, installation, and configuration of a compatible Gateway controller.
- Exploring the implementation of the Kubernetes Gateway API within an Azure AKS cluster, covering the selection, installation, and configuration of a suitable Gateway controller.
- Researching secure methods for enabling cross-cluster communication between AWS EKS and Azure AKS, with a focus on approaches that integrate seamlessly with the Kubernetes Gateway API, such as TLS and mutual TLS (mTLS) 1.
- Finding examples and documentation on utilizing Terraform to provision and configure the necessary Kubernetes Gateway API resources in both AWS EKS and Azure AKS 3.
- Investigating how to configure the Gateway API to securely expose the 'relay' service from the AWS EKS cluster to the Azure AKS cluster, considering aspects like authentication and authorization 4.
- Outlining the structure and content of a Confluence document that explains the proposed solution, including an introduction, problem statement, proposed architecture using the Gateway API, implementation steps using Terraform, security considerations, and potential challenges.

The emphasis on both security and simplicity throughout these research areas will guide the selection of technologies and the design of the final solution. A balance between robust security measures and ease of implementation and management is crucial for the practical adoption of the proposed approach.

## 2\. Understanding the Kubernetes Gateway API

The Kubernetes Gateway API represents a significant evolution in Kubernetes service networking, designed to overcome the limitations of the earlier Ingress API 1. It offers a more powerful, flexible, and role-oriented approach to managing traffic within and into Kubernetes clusters 2.

### Core Concepts

The Gateway API is built upon a set of core Custom Resource Definitions (CRDs) that model different aspects of service networking 1. Understanding these concepts is essential for implementing the proposed solution.

- GatewayClass: This resource defines a template for creating Gateway objects, essentially representing a specific type of load balancing implementation or controller 1. It formalizes the different kinds of Gateway controllers available and their associated capabilities, making it clear to users what features they can expect 4. For instance, a cloud provider might offer a GatewayClass that provisions a native cloud load balancer 7. The GatewayClass decouples the mechanism of implementing Gateways from the end-user configuration 12.
- Gateway: A Gateway resource specifies how external traffic can enter the Kubernetes cluster 11. It acts as a network endpoint, typically associated with a specific GatewayClass, and defines listeners that specify the protocols (e.g., HTTP, HTTPS) and ports on which the Gateway will accept incoming connections 1. Multiple Gateway resources can be created, potentially utilizing different GatewayClass implementations within the same cluster 1.
- Routes: These resources define the rules for routing traffic from the Gateway to backend services within the cluster 11. The Gateway API supports protocol-specific route types, such as HTTPRoute for HTTP(S) traffic, TCPRoute for TCP traffic, TLSRoute for TLS passthrough, and GRPCRoute for gRPC traffic 1. These route objects can specify various matching criteria, including hostnames, paths, headers, and ports, allowing for granular control over traffic distribution 5.
- Listeners: Configured within a Gateway resource, listeners define the network protocols and ports that the Gateway will monitor for incoming requests 4. For example, a listener can be configured to accept HTTPS traffic on port 443, specifying TLS settings and associated certificates 5.
- ReferenceGrant: This resource plays a crucial role in security by enabling secure cross-namespace referencing 4. It allows a Route resource in one namespace to target a Gateway or Service resource in a different namespace, but only if the owner of the target resource explicitly grants this permission by creating a corresponding ReferenceGrant 5. This enhances security by preventing unauthorized cross-namespace access.

### Benefits Over Ingress

The Gateway API offers several significant advantages over the traditional Kubernetes Ingress API, making it a more suitable choice for complex networking scenarios like cross-cluster communication 1.

- More Powerful and Granular Control: Unlike Ingress, which primarily supports HTTP routing, the Gateway API provides extensive protocol support, including HTTP, HTTPS, TCP, UDP, and gRPC 1. It also offers more advanced routing capabilities, such as header-based matching and traffic weighting, which were often only achievable in Ingress through non-portable annotations 1. This finer-grained control allows for more sophisticated traffic management strategies, including canary deployments and A/B testing 5.
- More Flexible and Extensible Configuration: The Gateway API is designed to be highly extensible, allowing for custom resources and extensions to address specific use cases beyond the core specification 1. While Ingress controllers often rely on custom annotations for extending functionality, the Gateway API provides structured extension points, offering better validation and portability 6.
- Role-Oriented Design: Recognizing that Kubernetes infrastructure is often a shared resource managed by different teams with distinct responsibilities, the Gateway API adopts a role-oriented design 1. It defines distinct roles for Infrastructure Providers (managing GatewayClasses), Cluster Operators (managing Gateways), and Application Developers (managing Routes), enabling a clear separation of concerns and facilitating Role-Based Access Control (RBAC) 2. This model allows different teams to manage their respective parts of the configuration without interfering with others 5.
- Portability: The Gateway API is designed as a universal specification intended to be supported by multiple implementations 1. This portability aims to reduce vendor lock-in and allows users to potentially switch between different Gateway controllers without significant configuration changes (except for the GatewayClass) 5. Conformance tests are also part of the Gateway API project to ensure consistency across implementations 6.
- Typed Routes and Backends: The API supports typed Route resources specific to different protocols, as well as different types of backend targets beyond just Kubernetes Services, such as storage buckets or functions 2. This provides greater flexibility in how traffic is routed and where it can be directed.
- Shared Gateways and Cross-Namespace Support: The Gateway API allows for the sharing of underlying load balancers and virtual IP addresses (VIPs) by permitting independent Route resources, even from different namespaces, to attach to the same Gateway 4. This enables teams to share infrastructure safely without requiring direct coordination, improving resource utilization and simplifying management in multi-tenant environments 4.

The role-oriented design of the Gateway API is particularly relevant in the context of shared Kubernetes infrastructure. By clearly delineating responsibilities, it allows for the implementation of more granular RBAC policies. For instance, application developers can be granted permissions to manage HTTPRoute resources for their applications without having the ability to modify the underlying Gateway or GatewayClass resources, which are typically managed by cluster operators or infrastructure providers 2. This separation of concerns enhances the overall security posture of the cluster by limiting the potential for unintended or malicious configuration changes.

## 3\. Implementing Gateway API in AWS EKS

To leverage the Kubernetes Gateway API within an AWS EKS cluster, a compatible Gateway controller needs to be installed and configured 7. Several implementations are available, each with its own strengths and characteristics.

### Choosing A Gateway Controller

- AWS Gateway API Controller: This is Amazon's native implementation of the Gateway API for EKS 7. It integrates directly with AWS Application Networking, which provisions Amazon Virtual Private Cloud (VPC) Lattice resources based on the created Gateway API objects 8. This tight integration can simplify the management of networking within the AWS environment. The controller supports HTTP and HTTPS protocols 8.
- Envoy Gateway: Based on the popular Envoy proxy, Envoy Gateway is an open-source controller that provides a feature-rich and extensible implementation of the Gateway API 1. It is a leading contributor to the Gateway API project and offers enterprise support through Tetrate 1. Envoy Gateway provides flexibility and is widely adopted in the Kubernetes ecosystem.
- NGINX Gateway Fabric: This implementation leverages the widely used NGINX proxy and aims to provide a robust solution for the Gateway API 6. While it supports all core features of the Gateway API, it is a newer project compared to NGINX Ingress Controller and might have a slightly different maturity level 6.
- HAProxy Kubernetes Ingress Controller: HAProxy, a well-established and reliable load balancer, also offers a Kubernetes Ingress Controller that supports the Gateway API alongside the traditional Ingress API 2. This provides a mature and proven option for managing traffic.

Choosing the AWS Gateway API Controller offers the benefit of seamless integration with AWS services like VPC Lattice 8. This can potentially simplify the initial setup and ongoing management of the Gateway within the AWS environment, aligning with the goal of simplicity. By leveraging VPC Lattice, the controller automatically handles network connectivity and service discovery across VPCs and accounts, as well as implementing security policies 8. However, this choice introduces a direct dependency on AWS-specific services, which might need to be considered if cross-cloud portability is a significant future requirement.

### Installation And Configuration

The installation and configuration process varies depending on the chosen Gateway controller.

- AWS Gateway API Controller: Installation typically involves deploying the controller to the EKS cluster. This can be done using Kubernetes manifests or Helm charts provided by AWS. Once deployed, the controller watches for the creation of Gateway API resources (like Gateway and HTTPRoute) and automatically provisions the corresponding resources in Amazon VPC Lattice 8. A GatewayClass resource needs to be created to identify VPC Lattice as the implementation 8.
- Other Controllers (e.g., Envoy Gateway, NGINX Gateway Fabric, HAProxy): Installation generally involves deploying the necessary Custom Resource Definitions (CRDs) for the Gateway API and then deploying the controller itself. This is often done using kubectl apply with YAML manifests or through Helm charts provided by the respective projects 1. For Envoy Gateway, Tetrate provides an enterprise-ready distribution 1.
- Configuration: After installing the controller, the next step is to create GatewayClass and Gateway resources. The GatewayClass resource specifies the controller that will manage the Gateways of that class. The Gateway resource defines the entry point for traffic, including the listeners (protocol and port) 4. For the AWS Gateway API Controller, the gatewayClassName in the Gateway resource would reference the VPC Lattice GatewayClass 8.
- Installing Gateway API CRDs: Regardless of the chosen controller, the core Gateway API CRDs need to be installed on the EKS cluster if they are not already present. These CRDs define the GatewayClass, Gateway, HTTPRoute, and other fundamental resources. The Kubernetes SIGs provide standard installation manifests for both the stable ("standard") and experimental channels of the Gateway API, which can be applied using kubectl apply 14. For example, to install the standard channel, the command is: `kubectl apply -f <https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml>`.

## 4\. Implementing Gateway API in Azure AKS

Similar to AWS EKS, implementing the Kubernetes Gateway API in Azure AKS requires selecting and installing a compatible Gateway controller 7. Several options are available that integrate with the Azure environment.

### Choosing A Gateway Controller

- Azure Application Gateway for Containers: This is Microsoft's managed application (layer 7\) load balancing solution specifically designed for Kubernetes clusters in Azure 7. It offers dynamic traffic management capabilities and supports the Kubernetes Gateway API. This provides native integration with Azure networking services.
- Istio: A popular service mesh platform that also includes Ingress Gateway functionality and supports the Gateway API 7. Istio offers advanced features for traffic management, security, and observability, making it a comprehensive solution for service networking across both ingress and service mesh layers. It can be enabled as an Azure Service Mesh (ASM) extension on AKS 9.
- Envoy Gateway: As with AWS, Envoy Gateway can also be deployed in Azure AKS, providing a consistent Gateway API implementation across different cloud providers 7.
- Traefik Proxy: This open-source Ingress controller is known for its simplicity and automatic configuration, and also supports the Kubernetes Gateway API 5.

Leveraging Azure Application Gateway for Containers might offer a more straightforward integration with Azure's managed load balancing infrastructure, similar to the AWS Gateway API Controller 7. This could simplify the setup process within the Azure environment. However, Istio presents a compelling alternative, particularly if a unified approach to service networking and security is desired across both EKS and AKS 9. While Istio's initial setup might be more involved, it provides a consistent set of features and policies that can be applied uniformly across both cloud environments, which could be advantageous for managing cross-cluster communication and security.

### Installation And Configuration

The installation and configuration steps for the Gateway controller on Azure AKS will depend on the chosen implementation.

- Azure Application Gateway for Containers: Deployment typically involves installing the Application Gateway for Containers (ALB) controller on the AKS cluster. Microsoft provides quickstart guides and documentation for this process 7.
- Istio: Istio can be enabled as an add-on to an existing AKS cluster using the Azure CLI 9. When creating a new AKS cluster, the \--enable-azure-service-mesh flag can be used 9. After enabling the Azure Service Mesh, the Istio Ingress Gateway component needs to be enabled to utilize the Gateway API for ingress traffic 9.
- Other Controllers (e.g., Envoy Gateway, Traefik): Similar to AWS, these controllers are usually installed by applying Kubernetes manifests or Helm charts that deploy the CRDs and the controller pods to the AKS cluster 5.
- Configuration: Once the controller is installed, GatewayClass and Gateway resources need to be created. For Azure Application Gateway for Containers, a specific GatewayClass will be associated with the ALB controller. For Istio, the gatewayClassName in the Gateway resource will typically be istio 9. The Gateway resource will define the listeners for incoming traffic. For example, to create an external entry point using Istio's managed Ingress Gateway, a Gateway resource can be defined, associating it with the istio gatewayClassName and specifying the desired protocol and port 9.
- Installing Gateway API CRDs: As with AWS EKS, the core Gateway API CRDs must be installed on the Azure AKS cluster. This can be done using the same standard installation manifests provided by the Kubernetes SIGs 14.

## 5\. Secure Cross-Cluster Communication Using Gateway API

Enabling secure communication between the AWS EKS and Azure AKS clusters, particularly for exposing the 'relay' service, requires careful consideration of trust establishment and data protection 1. The Kubernetes Gateway API provides mechanisms that can be leveraged to implement these security measures.

### Establishing Trust

- TLS (Transport Layer Security): Encrypting the traffic between the client on the Azure AKS cluster and the 'relay' service on the AWS EKS cluster is fundamental for ensuring confidentiality and integrity 1. The Gateway API facilitates TLS termination at the Gateway level. This means that the incoming HTTPS connection from the Azure AKS cluster can be decrypted at the Gateway in the AWS EKS cluster, and then the traffic can be forwarded to the 'relay' service, potentially using TLS as well for end-to-end encryption.
- Mutual TLS (mTLS): For a higher level of security, mutual TLS can be implemented. This requires both the client (the service on Azure AKS accessing 'relay') and the server ('relay' service on AWS EKS) to authenticate each other using X.509 certificates 1. The client presents its certificate to the server, and the server also presents its certificate to the client. Both parties verify the validity of the certificates against a trusted Certificate Authority (CA). This ensures strong authentication and authorization at the network level, preventing unauthorized access and man-in-the-middle attacks.

### Certificate Management

Effective management of TLS certificates across both AWS and Azure is crucial for maintaining a secure cross-cluster communication channel. Several strategies can be employed:

- Common Certificate Authority (CA): Using a single, trusted CA to issue certificates for services in both the AWS EKS and Azure AKS clusters can simplify the process of establishing trust for mTLS. Both clusters would need to be configured to trust the root or intermediate CA certificate.
- Cloud-Specific Certificate Management Services: Leveraging cloud-native certificate management services like AWS Certificate Manager (ACM) and Azure Key Vault can streamline the issuance, renewal, and management of certificates within their respective environments. For cross-cluster trust, certificates issued by these services might need to be exchanged or configured appropriately.
- Kubernetes Secrets: Certificates and private keys can be stored as Kubernetes Secrets within each cluster. The Gateway controller can then be configured to use these Secrets for TLS termination and mTLS authentication.

### Leveraging ReferenceGrant for Secure Cross-Namespace References

If the 'relay' service on AWS EKS resides in a different namespace than the Gateway controller, a ReferenceGrant resource will be necessary to allow the Gateway to access the service 4. This ensures that the owner of the 'relay' service namespace explicitly grants permission for the Gateway in another namespace to target it as a backend. While the initial request is about exposing the service to a remote cluster, if internal routing within the AWS EKS cluster involves cross-namespace communication, ReferenceGrant will play a vital role in maintaining security by enforcing explicit authorization for such interactions.

Implementing mTLS using certificates offers a robust security approach for this cross-cluster communication. By requiring mutual authentication, it ensures that only verified services from the Azure AKS cluster can access the 'relay' service, and vice versa. Managing these certificates through a centralized CA or cloud-native services simplifies the operational overhead associated with certificate lifecycle management, which is essential for a secure and maintainable system.

## 6\. Terraform for Gateway API Resource Provisioning

Terraform provides an infrastructure-as-code approach to managing Kubernetes resources, including those defined by the Gateway API, across both AWS EKS and Azure AKS clusters 3. This allows for consistent and repeatable provisioning of the necessary infrastructure components.

### Terraform Providers

To interact with both Kubernetes clusters, the Kubernetes provider for Terraform will be used. This provider allows Terraform to manage resources within a Kubernetes cluster, provided with the necessary kubeconfig file for authentication. Depending on the chosen Gateway controllers and any prerequisite infrastructure, cloud-specific providers (AWS and Azure) might also be necessary. For instance, if Azure Application Gateway for Containers is used, the AzureRM provider might be needed to manage the Application Gateway resource itself.

### Provisioning GatewayClass and Gateway Resources in Both Clusters

Terraform manifests can be defined to create the GatewayClass and Gateway resources in both the AWS EKS and Azure AKS clusters. The GatewayClass resource will specify the chosen Gateway controller implementation. For example, if the AWS Gateway API Controller is used on EKS, the gatewayClassName in the Gateway resource will correspond to the VPC Lattice controller's GatewayClass. Similarly, on AKS, if Istio is used, the gatewayClassName will be set to istio.

### Provisioning Route Resources for Cross-Cluster Communication

In the Azure AKS cluster, Terraform manifests will be created to define the appropriate Route resource (likely an HTTPRoute). This route will specify how traffic should be directed to the 'relay' service running on the AWS EKS cluster. This will likely involve configuring the backend of the route to point to the external IP address or DNS name of the Gateway deployed in the AWS EKS cluster. An externalName Service within the Azure AKS cluster, pointing to the AWS EKS Gateway's external endpoint, could facilitate this routing.

### Provisioning ReferenceGrant Resources

If the 'relay' service and the Gateway on AWS EKS reside in different namespaces, a ReferenceGrant resource will need to be provisioned on the AWS EKS cluster. This can also be done using Terraform. The ReferenceGrant will explicitly allow the Gateway's namespace to reference the 'relay' service's namespace.

By using Terraform to manage the Gateway API resources, the entire configuration for exposing the 'relay' service becomes declarative and version-controlled. This not only ensures consistency across deployments but also simplifies the process of setting up, updating, and tearing down the necessary infrastructure. The automation provided by Terraform aligns well with the requirement for simplicity by reducing manual configuration steps and the potential for human error.

## 7\. Exposing the 'relay' Service Securely

To securely expose the 'relay' service from the AWS EKS cluster to the Azure AKS cluster using the Gateway API, specific configurations are required in both environments.

### Configuration On AWS EKS

1. Deploy the chosen Gateway controller: Ensure that the selected Gateway controller (e.g., AWS Gateway API Controller or Envoy Gateway) is installed and running in the AWS EKS cluster.
2. Create a Gateway resource: Define a Gateway resource that listens on a specific port, such as 443 for HTTPS, and potentially a specific hostname. This Gateway will act as the entry point for traffic destined for the 'relay' service.
3. Create a Route resource: Define an HTTPRoute (or another relevant route type) that matches incoming requests based on the desired criteria (e.g., a specific hostname or path) and forwards them to the backend Service representing the 'relay' application.
4. Configure TLS: Configure TLS on the Gateway listener to enable HTTPS. This involves specifying a TLS certificate and its associated private key. These can be stored in a Kubernetes Secret and referenced in the Gateway resource.

### Configuration On Azure AKS

1. Deploy the chosen Gateway controller: Ensure that a compatible Gateway controller (e.g., Azure Application Gateway for Containers or Istio) is installed and running in the Azure AKS cluster.
2. Create a Route resource: Define an HTTPRoute (or another relevant route type) in the Azure AKS cluster. This route will need to be configured to send traffic to the 'relay' service on the AWS EKS cluster. The backend of this route will likely point to an externalName Service within the AKS cluster, which in turn resolves to the external IP address or DNS name of the Gateway in the AWS EKS cluster.

### Authentication And Authorization

Implementing robust authentication and authorization mechanisms is crucial for securing access to the 'relay' service. Several approaches can be considered:

- TLS/mTLS based authentication: If mTLS is implemented, the Gateway in the AWS EKS cluster can be configured to only accept connections from clients presenting a valid client certificate issued by a trusted CA. The Azure AKS cluster (or the specific service accessing 'relay') would need to be configured to present this certificate during the TLS handshake.
- JWT (JSON Web Tokens) based authentication: The 'relay' service on AWS EKS can be protected by requiring clients to present a valid JWT in the authorization header of their requests. The Gateway in the AWS EKS cluster can be configured with an authentication filter that validates the JWT against an identity provider. The service on Azure AKS would then need to obtain and include a valid JWT in its requests to 'relay'. Gateway API implementations like Envoy Gateway offer features for JWT authentication 7.
- Network Policies: Kubernetes Network Policies can be implemented in the AWS EKS cluster to restrict network access to the nodes or IP ranges from which the Azure AKS cluster will be sending traffic. This provides a network-level security control.
- Controller-specific mechanisms: Some Gateway controllers might offer their own custom authentication and authorization features. For example, Airlock Microgateway supports features like RBAC and JWT authentication 7. Investigating the specific capabilities of the chosen controllers in both EKS and AKS is important.

A multi-layered security approach, combining encryption with strong authentication and potentially network-level restrictions, will provide the most robust protection for the 'relay' service. The specific implementation details will depend on the chosen Gateway controllers and the security requirements of the application.

## 8\. Confluence Document Structure

The proposed solution will be documented in a Confluence document with the following structure:

- Introduction: (Covered in Section 1\)
- Problem Statement: (Covered in Section 1\)
- Proposed Architecture using the Gateway API:
  - A high-level diagram illustrating the AWS EKS and Azure AKS clusters, the 'relay' service in EKS, the chosen Gateway controllers in both clusters, and the flow of traffic from AKS to 'relay' via the Gateways.
  - Explanation of the key components: Gateway Controllers, Gateway resources, Route resources, and the 'relay' service.
  - Rationale for choosing specific Gateway controller implementations for both EKS and AKS, considering factors like native integration, features, and ease of use.
- Implementation Steps using Terraform:
  - Detailed, step-by-step instructions on using Terraform to provision the necessary Gateway API resources in both AWS EKS and Azure AKS.
  - Code snippets for Terraform manifests for GatewayClass, Gateway, and Route resources in both environments.
  - Guidance on configuring the Kubernetes provider for Terraform to connect to both clusters.
  - Instructions on any prerequisite steps, such as installing the chosen Gateway controllers.
- Security Considerations:
  - A comprehensive discussion of the security measures to be implemented, including TLS/mTLS configuration, the chosen certificate management strategy (e.g., using ACM/Key Vault or a common CA), the authentication and authorization mechanisms (e.g., mTLS, JWT), and any relevant network policies.
  - Explanation of how the features of the chosen Gateway API controllers contribute to the overall security posture.
- Potential Challenges:
  - Discussion of potential challenges such as network connectivity between AWS and Azure, latency considerations, the complexity of managing resources across two cloud providers, ensuring compatibility between different Gateway API implementations, and setting up monitoring and troubleshooting for cross-cluster communication.

The architectural diagram will be crucial for visualizing the proposed solution. It should clearly depict the two Kubernetes clusters, the 'relay' service residing in the AWS EKS cluster, the Gateway in the AWS EKS cluster acting as the entry point, and the flow of traffic originating from the Azure AKS cluster and reaching the 'relay' service through the configured routes and Gateways. Including the specific Gateway controller implementations chosen for each cloud will provide further clarity.

## 9\. Potential Challenges and Considerations

Implementing cross-cluster communication using the Kubernetes Gateway API and Terraform, while promising, presents several potential challenges and considerations:

- Network Connectivity: Ensuring proper network connectivity between the AWS VPC where the EKS cluster resides and the Azure VNet hosting the AKS cluster is paramount 8. This might involve setting up VPC peering, VPN connections, or other network interconnectivity solutions to allow traffic to flow between the two environments. Firewall rules in both cloud providers will also need to be configured to permit communication on the necessary ports.
- Latency: Network latency between the two geographically separated cloud environments can impact the performance of the 'relay' service when accessed from the Azure AKS cluster. This needs to be considered in the overall design and potentially mitigated through techniques like caching or optimizing the communication protocol.
- Complexity: Managing infrastructure and applications across two different cloud providers inherently adds complexity. While Terraform helps to automate provisioning, the operational overhead of maintaining and monitoring resources in both AWS and Azure needs to be acknowledged.
- Controller Compatibility: Although the Gateway API aims for portability, the specific features and implementation details of different Gateway controllers (even if they support the same API version) might vary. Ensuring compatibility and consistent behavior across the chosen controllers in AWS and Azure will be important.
- Monitoring and Observability: Setting up comprehensive monitoring and observability for the cross-cluster communication will be essential for detecting and troubleshooting issues. This might involve configuring logging, metrics, and tracing across both clusters and potentially using cross-cloud monitoring solutions.
- Cost: The cost implications of running infrastructure and transferring data between AWS and Azure need to be considered. Network egress costs, in particular, can be significant in cross-cloud scenarios.

While the Kubernetes Gateway API offers a standardized way to manage ingress and routing, the underlying network infrastructure and the specific implementations of Gateway controllers can introduce cloud-specific challenges. For instance, establishing seamless connectivity between AWS and Azure requires careful configuration of network peering or other interconnectivity options. Similarly, while different Gateway controllers might adhere to the Gateway API specification, their specific features and how they handle cross-cluster traffic could vary, potentially requiring different configuration approaches. Addressing these potential challenges proactively will be crucial for the success of the proposed solution.

## 10\. Conclusion

The Kubernetes Gateway API presents a modern and powerful approach to exposing the 'relay' service running on AWS EKS to a remote Azure AKS cluster. Its enhanced features, role-oriented design, and portability offer significant advantages over the traditional Ingress API. By leveraging Terraform for infrastructure-as-code, the provisioning and configuration of the necessary Gateway API resources in both cloud environments can be automated, promoting consistency and simplifying management. Implementing robust security measures, such as TLS or preferably mutual TLS, along with appropriate authentication and authorization mechanisms, will ensure that the cross-cluster communication is secure. While potential challenges such as network connectivity, latency, and cross-cloud complexity need to be carefully addressed, the combination of the Kubernetes Gateway API and Terraform provides a viable and promising solution for securely and efficiently exposing services across different Kubernetes clusters in a multi-cloud environment.

| Feature | AWS EKS Gateway Controller Options | Azure AKS Gateway Controller Options |
| :---- | :---- | :---- |
| Controller Name | AWS Gateway API Controller, Envoy Gateway, NGINX Gateway Fabric, HAProxy Kubernetes Ingress Controller | Azure Application Gateway for Containers, Istio, Envoy Gateway, Traefik Proxy |
| Vendor/Project | Amazon, Envoy Project/Tetrate, NGINX, HAProxy Technologies | Microsoft, Istio Project, Envoy Project/Tetrate, Traefik Labs |
| Maturity Level | GA (AWS), GA (Envoy), Beta (NGINX), GA (HAProxy) | GA (Azure), GA (Istio), GA (Envoy), GA (Traefik) |
| Key Features (Cross-Cluster & Security) | VPC Lattice Integration, Extensibility, Advanced Routing, TLS/mTLS Support, Authentication/Authorization Features | Native Azure Integration, Service Mesh Capabilities, Advanced Traffic Management, TLS/mTLS Support, Authentication/Authorization Features |
| Ease of Use | High with AWS services, Moderate to High depending on familiarity with the controller | High with Azure services, Moderate to High depending on familiarity with the controller |
| Terraform Support (Known) | Yes (Kubernetes provider), Yes (Kubernetes provider), Yes (Kubernetes provider), Yes (Kubernetes provider) | Yes (AzureRM & Kubernetes provider), Yes (Kubernetes provider), Yes (Kubernetes provider), Yes (Kubernetes provider) |

| Security Aspect | Proposed Method | Implementation Details | Responsible Component(s) |
| :---- | :---- | :---- | :---- |
| Encryption | TLS 1.3 | Configure TLS listener on the AWS EKS Gateway using a certificate stored in a Kubernetes Secret. | AWS EKS Gateway |
| Authentication | Mutual TLS (mTLS) or JWT | mTLS: Configure the AWS EKS Gateway to require and verify client certificates presented by the Azure AKS cluster. JWT: Configure an authentication filter on the AWS EKS Gateway to validate JWTs. | AWS EKS Gateway |
| Certificate Management | AWS Certificate Manager (ACM) and Azure Key Vault or Common CA | Utilize ACM for certificate issuance and management on AWS. Utilize Key Vault for certificate issuance and management on Azure, or use a common trusted Certificate Authority for both clusters. | Both Clusters |
| Authorization | RBAC, Network Policies, Controller-specific policies | Implement Kubernetes RBAC policies to control access to Gateway API resources. Implement Network Policies in AWS EKS to restrict traffic sources. Explore and configure authorization features of the chosen controllers. | Both Clusters |

### Works Cited

1. What Is the Kubernetes Gateway API? \- Tetrate, accessed on March 27, 2025, [https://tetrate.io/learn/what-is-the-kubernetes-gateway-api/](https://tetrate.io/learn/what-is-the-kubernetes-gateway-api/)
2. Kubernetes Gateway API (Everything You Should Know) \- HAProxy Technologies, accessed on March 27, 2025, [https://www.haproxy.com/blog/kubernetes-gateway-api](https://www.haproxy.com/blog/kubernetes-gateway-api)
3. A Step-by-Step Guide for Private API Gateway and EKS Integration \- Searce, accessed on March 27, 2025, [https://blog.searce.com/a-step-by-step-guide-for-private-api-gateway-and-eks-integration-32f127ac1b2b](https://blog.searce.com/a-step-by-step-guide-for-private-api-gateway-and-eks-integration-32f127ac1b2b)
4. Kubernetes Gateway API: Introduction, accessed on March 27, 2025, [https://gateway-api.sigs.k8s.io/](https://gateway-api.sigs.k8s.io/)
5. Kubernetes Gateway API: What Is It And Why Do You Need It? \- Traefik Labs, accessed on March 27, 2025, [https://traefik.io/glossary/kubernetes-gateway-api/](https://traefik.io/glossary/kubernetes-gateway-api/)
6. 5 Reasons to Try the Kubernetes Gateway API \- NGINX Community Blog, accessed on March 27, 2025, [https://blog.nginx.org/blog/5-reasons-to-try-the-kubernetes-gateway-api](https://blog.nginx.org/blog/5-reasons-to-try-the-kubernetes-gateway-api)
7. Implementations \- Kubernetes Gateway API, accessed on March 27, 2025, [https://gateway-api.sigs.k8s.io/implementations/](https://gateway-api.sigs.k8s.io/implementations/)
8. Redefining AWS EKS networking with Gateway API \- DEV Community, accessed on March 27, 2025, [https://dev.to/aws-builders/redefining-aws-eks-networking-with-gateway-api-2in9](https://dev.to/aws-builders/redefining-aws-eks-networking-with-gateway-api-2in9)
9. Exploring the Gateway API with Istio ASM Extension on AKS | by Arnaud Tincelin | Medium, accessed on March 27, 2025, [https://medium.com/@arnaud.tincelin/deploying-and-exploring-the-gateway-api-with-istio-ams-extension-on-aks-3caca2393f2c](https://medium.com/@arnaud.tincelin/deploying-and-exploring-the-gateway-api-with-istio-ams-extension-on-aks-3caca2393f2c)
10. Using AKS-managed Istio External Ingress Gateway with Gateway API \- YouTube, accessed on March 27, 2025, [https://www.youtube.com/watch?v=HNSMAjaAgMo](https://www.youtube.com/watch?v=HNSMAjaAgMo)
11. Core Concepts | Envoy Gateway, accessed on March 27, 2025, [https://docs.tetrate.io/envoy-gateway/introduction/core-concepts](https://docs.tetrate.io/envoy-gateway/introduction/core-concepts)
12. A practical guide to Kubernetes Gateway API \- Spectro Cloud, accessed on March 27, 2025, [https://www.spectrocloud.com/blog/practical-guide-to-kubernetes-gateway-api](https://www.spectrocloud.com/blog/practical-guide-to-kubernetes-gateway-api)
13. Gateway API Implementations \- Determined AI Documentation, accessed on March 27, 2025, [https://docs.determined.ai/setup-cluster/k8s/controller-reviews.html](https://docs.determined.ai/setup-cluster/k8s/controller-reviews.html)
14. Getting started \- Kubernetes Gateway API, accessed on March 27, 2025, [https://gateway-api.sigs.k8s.io/guides/](https://gateway-api.sigs.k8s.io/guides/)
