---
aliases: []
confidence: 
created: 2025-04-06T05:21:44Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Remote request config
type:
uid: 
updated: 
version:
---

Right, let's document how you can securely expose your `relay` service inside your private AWS EKS cluster in a private VPC to the `bunny` service on a remote Azure private networked AKS cluster. We'll focus on the AWS side, explaining the components from the inside out to facilitate this private and secure communication.

To achieve this, we'll leverage the Kubernetes Gateway API with the AWS Gateway API Controller and Amazon VPC Lattice for private service exposure within AWS. For secure cross-cloud communication, we'll assume a secure network bridge like a Site-to-Site VPN between your AWS VPC and the Azure VNet.

Here are the components within your AWS EKS cluster and how they work together:

- 1. The `relay` service (Inside the EKS Cluster)
    - The `relay` service itself is an independently deployable unit of software running as one or more pods within your EKS cluster. It delivers the task queue functionality.
    - To be accessible within the Kubernetes cluster, `relay` will be exposed as a standard Kubernetes Service. This Service provides a stable IP address and DNS name within the cluster, allowing other services within EKS to communicate with the `relay` pods without needing to know the individual pod IPs, which can change. This Kubernetes Service will likely be of type ClusterIP, as it's initially only intended for internal access. The AWS Gateway API Controller will later interact with this service to expose it externally (within the private network) via VPC Lattice.
- 2. Kubernetes Gateway API Resources (Defining External Access)
    - The Kubernetes Gateway API is a set of Custom Resource Definitions (CRDs) that provide a more expressive, flexible, and role-oriented way to manage external access to your Kubernetes applications compared to the older Ingress API.
    - You will define the following key Gateway API resources:
        - GatewayClass: This is a cluster-scoped resource that defines a template for creating Gateway objects and represents a specific type of gateway controller. For AWS, you will typically have a `GatewayClass` specifying the AWS implementation: `vpc-lattice.gateway.networking.k8s.io`. This tells your EKS cluster to use the AWS Gateway API Controller to manage Gateways associated with this class.
        - Gateway: This is a namespaced resource that represents an instance of a load balancer or proxy. When using the AWS Gateway API Controller with the `vpc-lattice` `GatewayClass`, creating a `Gateway` resource triggers the creation of an associated AWS VPC Lattice Service Network. The `Gateway` resource defines listeners which specify the ports and protocols (e.g., HTTP/HTTPS) that will accept incoming traffic. For secure communication with Azure, you would likely configure a listener for HTTPS on port 443.
        - HTTPRoute: This is a namespaced resource that defines routing rules for HTTP and HTTPS traffic. You will create an `HTTPRoute` that attaches to your `Gateway` and specifies how traffic arriving at the `Gateway`'s listener should be directed to your backend `relay` Kubernetes Service based on criteria like hostnames, paths, and headers. This `HTTPRoute` will translate into AWS VPC Lattice Service(s), Listeners, and Rules.
- 3. AWS Gateway API Controller (Implementing the Gateway API)
    - This is a Kubernetes controller running as one or more pods within your EKS cluster. Its primary function is to watch for Kubernetes Gateway API resources (like `GatewayClass`, `Gateway`, and `HTTPRoute`) and translate them into configurations for AWS services, specifically Amazon VPC Lattice.
    - The controller needs AWS credentials to manage these AWS resources. For a secure setup, you should use EKS Pod Identity (or IAM Roles for Service Accounts - IRSA) to grant the controller pods the necessary IAM permissions without needing to store AWS access keys as Kubernetes secrets. This involves associating the Kubernetes ServiceAccount that the controller pods run under with an IAM Role that has the required permissions to interact with VPC Lattice (e.g., `vpc-lattice:`).
    - The controller will also need to be able to communicate with the Kubernetes API server in your private VPC. Ensure that network policies or security group configurations do not restrict this communication. If your private VPC lacks direct internet access, you'll need to ensure you have configured the necessary VPC endpoints for AWS services like STS (for assuming roles) and VPC Lattice (`com.amazonaws.<region>.vpc-lattice`).
- 4. Amazon VPC Lattice (Private Application Networking)
    - VPC Lattice is a fully managed application networking service that allows you to connect, secure, and monitor services across multiple VPCs and accounts. The AWS Gateway API Controller integrates with VPC Lattice to provide private exposure for your `relay` service.
    - When you create a `Gateway` resource with the AWS Gateway API Controller, it provisions a VPC Lattice Service Network. This acts as a logical boundary for your services. Your EKS cluster's VPC needs to be associated with this Service Network to allow traffic flow.
    - The `HTTPRoute` resources you define will lead to the creation of VPC Lattice Services within the Service Network. These services contain listeners and routing rules that dictate how incoming requests are matched and forwarded.
    - The backend of your `HTTPRoute` will point to your `relay` Kubernetes Service. The AWS Gateway API Controller will then create VPC Lattice Target Groups based on this Kubernetes Service and register the IP addresses of your `relay` pods as targets. VPC Lattice also performs health checks against these targets.
- 5. Network Configuration and Security within AWS
    - Since your EKS cluster is in a private VPC, the communication with `bunny` in Azure will require a secure network bridge, such as a Site-to-Site VPN between your AWS VPC and the Azure VNet.
    - When you associate your EKS cluster's VPC with the VPC Lattice Service Network, you must also associate one or more Security Groups. These Security Groups act as stateful firewalls at the network level, controlling the inbound traffic (based on port, protocol, source IP/CIDR/Security Group) that is allowed to enter the Service Network from your VPC. You will need to configure these Security Groups to allow inbound HTTPS traffic (port 443) from the CIDR range of your Azure VNet (specifically the subnet where the `bunny` service resides). This restricts access to your `relay` service at the network level.
    - VPC Lattice Authentication and Authorization: When you define your `Gateway` (and thus the Service Network), you can configure its authentication type. For secure cross-cloud communication where `bunny` is in Azure and not easily assuming an AWS IAM role, you might set the `AuthType` to `NONE` and rely on network-level restrictions (Security Groups) and potentially application-level authentication within the `relay` service itself. However, for more robust security within AWS, if the consuming service were also within an AWS account, you could leverage AWS IAM authentication for the Service Network, ensuring only authenticated IAM principals with the necessary permissions could access `relay`.
    - TLS Termination: You will configure TLS termination on the `Gateway` listener (port 443) by specifying a TLS certificate (ideally managed by AWS Certificate Manager - ACM). This ensures that traffic from Azure to your `relay` service is encrypted in transit.
- 6. Communication with Azure (`bunny` Service)
    - On the Azure side, you will need to configure a Site-to-Site VPN connection to your AWS VPC.
    - The `bunny` service in Azure will need to be configured to make HTTPS requests to the private DNS name generated by VPC Lattice for your `relay` service. You will need to ensure that the Azure network can resolve this DNS name. This might involve configuring DNS forwarding from Azure to AWS Route 53 Resolver Inbound Endpoints or using the private IP address (though DNS is generally preferred for stability).
    - The Azure Network Security Groups (NSGs) associated with the `bunny` service's subnet should allow outbound HTTPS traffic to the AWS VPC CIDR range over the VPN.

In summary, the flow for `bunny` to access `relay` would be:

1. `bunny` in Azure makes an HTTPS request to the private DNS name of the VPC Lattice service for `relay`.
2. Azure DNS resolves this to a private IP address within your AWS VPC (via VPN and potentially DNS forwarding).
3. The traffic travels securely over the Site-to-Site VPN.
4. The AWS Security Group associated with the VPC Lattice Service Network association allows inbound HTTPS traffic from the Azure CIDR range.
5. VPC Lattice receives the encrypted traffic and decrypts it at the `Gateway` listener.
6. VPC Lattice routes the traffic based on the `HTTPRoute` rules to one of the healthy `relay` pods in your EKS cluster.
7. The `relay` service processes the request and sends the response back along the reverse path.

Security Considerations Throughout:

- Private Networking: By using a private EKS cluster, VPC Lattice within AWS, and a VPN to Azure, you ensure that the traffic does not traverse the public internet.
- Network Segmentation: VPC Lattice Service Networks act as logical boundaries, and Security Groups provide L3/L4 filtering.
- Encryption: TLS encryption ensures data in transit is protected. Consider mutual TLS (mTLS) between `bunny` and `relay` for stronger authentication at the application layer if the complexity is warranted. This would involve managing and exchanging certificates between the two clusters. The Gateway API supports mTLS configuration.
- Authentication and Authorization: While VPC Lattice offers IAM-based authentication within AWS, for cross-cloud scenarios, you'll likely rely on network-level restrictions and potentially implement application-level authentication (e.g., API keys, tokens) within the `relay` service to verify the identity of `bunny`.
- Least Privilege: Ensure that the IAM role used by the AWS Gateway API Controller has only the necessary permissions for VPC Lattice and related services. Similarly, configure Security Groups and Network Security Groups with the principle of least privilege in mind, only allowing necessary traffic.
- Regular Audits: Regularly review your network and security configurations to identify and address any potential vulnerabilities.

By implementing this architecture using the Kubernetes Gateway API, AWS Gateway API Controller, and VPC Lattice, along with a secure network bridge to Azure, you can expose your `relay` service privately and securely to the `bunny` service. Remember to carefully configure security at each layer to meet your specific requirements.

Exposing a public endpoint over the internet for your EKS cluster handling sensitive NHS patient data, even with firewalls and encryption, is not ideal for several key reasons:

- Increased Attack Surface: A public endpoint inherently increases the attack surface of your cluster. It becomes discoverable and potentially accessible from anywhere on the internet. While firewalls can restrict traffic to specific ports and protocols, and encryption protects data in transit, the endpoint itself is a target that malicious actors can probe for vulnerabilities. For highly sensitive data like NHS patient information, minimising this exposure is a fundamental security principle.
- Complexity of Firewall Rules: Managing firewall rules to tightly control access from the public internet can become complex and error-prone. Allowing traffic based on IP addresses can be difficult to maintain, especially if the remote services accessing your `relay` service have dynamic IP addresses. Misconfigurations in firewall rules could inadvertently grant unauthorised access. While Network Security Groups (NSGs) and Network Access Control Lists (NACLs) provide network-level filtering, relying solely on them at the public internet boundary for sensitive data introduces unnecessary risk.
- Limitations of Encryption at the Perimeter: While encryption like TLS/HTTPS secures the data in transit to your public endpoint, it doesn't protect against all types of attacks. For example, vulnerabilities in the application logic or misconfigurations within your cluster could still be exploited even if the traffic is encrypted. Furthermore, the encryption ends at your public endpoint, and the internal communication within your cluster also needs to be secured.
- Regulatory and Compliance Requirements: Handling NHS patient data likely comes with stringent regulatory and compliance requirements (though not explicitly detailed in the sources). These regulations often mandate strong controls around data access and security, and exposing a public endpoint, even with security measures, might not align with the principle of minimal exposure and could make achieving compliance more challenging.
- Preference for Private Connectivity: For inter-service communication, especially when dealing with sensitive data, private networking is generally preferred. This limits the attack surface by ensuring that services can only be accessed from within authorised private networks. Solutions like AWS PrivateLink are specifically designed for this purpose, allowing you to expose services privately within your VPC without traversing the public internet. Amazon VPC Lattice also facilitates private service exposure within AWS.

Regarding your second question: would the VPC no longer be private because of the 1 endpoint?

No, having one public endpoint does not necessarily mean your entire VPC is no longer private. A VPC can contain both public and private subnets.

- Public Subnets: Subnets that have a route to an Internet Gateway are considered public subnets. Resources in these subnets can have public IP addresses and can communicate directly with the internet (subject to security group and NACL rules). Your public endpoint would likely reside in a public subnet.
- Private Subnets: Subnets that do not have a direct route to an Internet Gateway are private subnets. Resources in these subnets do not have public IP addresses and cannot directly communicate with the internet. Outbound internet access for private subnets is typically achieved through a NAT Gateway or NAT Instance. Your EKS worker nodes and the `relay` service itself should ideally reside in private subnets to enhance security.

Therefore, even with a public endpoint, the majority of your cluster resources and your VPC can still maintain their private nature by being placed in private subnets with restricted routing to the internet. The key is to isolate your sensitive workloads in private subnets and control access to them through private networking solutions whenever possible.

Yes, that's a good way to understand it. The VPC is your overarching private network in AWS. Within that VPC, you can define subnets to further segment your network. EKS worker nodes are indeed deployed into these subnets.

Regarding your first point: if you use a public endpoint in the worker nodes subnet, that subnet is generally considered a public subnet, not a private one.

- A public subnet is one that has a route to an Internet Gateway. Resources within a public subnet can have public IP addresses and can directly communicate with the internet (subject to security group and NACL rules). If your worker nodes in a subnet have public IP addresses or if a service in that subnet is exposed via an Internet Gateway or a public-facing load balancer, then that subnet serves a public-facing purpose.
- Conversely, a private subnet does not have a direct route to an Internet Gateway. Resources in private subnets cannot directly communicate with the internet; outbound access is typically via a NAT Gateway or NAT Instance. For enhanced security, it's recommended to place sensitive workloads, like your EKS worker nodes and the 'relay' service itself, in private subnets.

So, if your worker nodes' subnet has a public endpoint (e.g., a public load balancer attached to services running on those nodes), that subnet is functioning as a public subnet, even if the worker nodes themselves don't have public IPs directly. The presence of a route to the internet for services within that subnet makes it publicly accessible.

Regarding your second point: exposing the k8s service 'relay' directly via a public endpoint is generally a poor choice, especially when handling sensitive data like NHS patient information. The sources outline several reasons for this:

- Increased Attack Surface: A public endpoint inherently increases the attack surface of your cluster, making it discoverable and potentially accessible from anywhere on the internet. Malicious actors can probe this endpoint for vulnerabilities.
- Complexity of Firewall Rules: Managing firewall rules to tightly control access from the public internet can become complex and error-prone. Misconfigurations could inadvertently grant unauthorised access. While Network Security Groups (NSGs) and Network Access Control Lists (NACLs) provide network-level filtering, relying solely on them at the public internet boundary for sensitive data introduces unnecessary risk.
- Limitations of Encryption at the Perimeter: While encryption like TLS/HTTPS secures data in transit to your public endpoint, it doesn't protect against all attacks. Vulnerabilities in application logic or internal misconfigurations can still be exploited. Encryption at the public endpoint doesn't secure internal cluster communication either.
- Regulatory and Compliance Requirements: Handling NHS patient data likely involves strict regulations that often mandate strong controls and minimal exposure, which a public endpoint might not align with.
- Preference for Private Connectivity: For sensitive inter-service communication, private networking is preferred to limit the attack surface. Solutions like AWS PrivateLink or Amazon VPC Lattice allow you to expose services privately within your VPC without traversing the public internet.

Instead of a direct public endpoint, the sources suggest using private networking solutions like VPC Lattice in conjunction with the AWS Gateway API Controller for exposing services privately within your AWS network. This approach keeps communication within your private AWS network, allowing you to control access using security groups and potentially authentication policies. The Gateway API allows you to define a Gateway resource that corresponds to a VPC Lattice service network and then use HTTPRoute resources to route traffic to your 'relay' service. This way, even if you need to grant access to the 'relay' service from other VPCs or accounts within the same AWS region, it can be done privately and securely using VPC Lattice.

Alternatively, for cross-VPC communication, you might consider VPC peering or AWS Transit Gateway (TGW), combined with strict security group and network ACL rules, to keep traffic within the AWS private network. Solutions involving AWS PrivateLink could also be considered to expose the service privately to other AWS accounts and VPCs.

In summary, exposing 'relay' via a direct public endpoint increases security risks and management complexity. Prioritising private networking solutions for such a service handling sensitive NHS data is a more secure and recommended approach.

Your plan to first configure the 'relay' service for internal cluster access and then establish a VPN connection between the private AWS and Azure networks to enable private access from an Azure pod is a sound approach, aligning well with the principles of private networking and security discussed in the sources.

Here's a breakdown of how this plan aligns with the information in the sources:

- Internal Cluster Access Control: Your first step of ensuring the 'relay' service is accessible within the EKS cluster and limiting internal access is crucial. You can achieve this using standard Kubernetes constructs such as Services and Network Policies. Network Policies allow you to control network traffic at the pod level, restricting which pods can communicate with the 'relay' service within the EKS cluster.
- VPN Connection for Private Networks: Establishing a VPN connection (like a Site-to-Site VPN) between your Azure VNet and AWS VPC is a standard method for creating a secure private network bridge. Source outlines the general steps for this:
    - Azure: You would set up a Virtual Network Gateway in your Azure VNet.
    - AWS: You would set up a Virtual Private Gateway (VGW) in your AWS VPC. Alternatively, you could consider an AWS Transit Gateway (TGW) if you anticipate more complex networking requirements in the future.
    - Connection: You would then configure a Site-to-Site VPN connection between these gateways, often using pre-shared keys or certificates for authentication.
- Routing over the VPN: Once the VPN connection is established, you'll need to configure routing in both cloud environments to ensure traffic can flow correctly:
    - Azure: You would create User Defined Routes (UDRs) in your AKS subnet's Route Table to direct traffic destined for your AWS VPC's CIDR range through the Azure Virtual Network Gateway.
    - AWS: You would update your VPC's Route Tables (associated with the subnets where your EKS nodes reside) to direct traffic destined for your Azure VNet's CIDR range through the VGW or TGW. Source provides examples of configuring route tables for VPC peering, which shares similar routing concepts with VPN connections in that you need to direct traffic destined for the other network through the connection point.
- Security Groups and Network Security Groups: To further secure the communication, you will need to configure firewall rules at both the AWS and Azure levels:
    - Azure NSG (Network Security Group): Ensure the NSGs associated with your AKS node subnets allow outbound traffic to the AWS service's private IP and port over the VPN. You should ideally restrict this to the specific IP range of your EKS worker nodes or load balancer if possible.
    - AWS Security Group (SG): Ensure the SGs associated with your EKS worker nodes (and any load balancer or VPC Lattice components if you introduce them later) allow inbound traffic on the 'relay' service's port from the CIDR range of your Azure VNet (specifically the subnet where the calling AKS pod resides, if possible).
- DNS Resolution: You'll also need to consider how the pod in Azure will resolve the address of the 'relay' service in AWS. You could use the private IP address of the 'relay' service (if it's directly exposed via a LoadBalancer with a private IP), or if you're using internal DNS within AWS, you might need to configure DNS resolution across the VPN connection. Source mentions options like using the VPC Lattice endpoint's private IP directly, configuring Azure Private DNS Zones, or setting up DNS forwarding. If you have a private hosted zone in AWS for your EKS services, source and mention enabling DNS resolution over VPC peering, which is a related concept applicable to VPNs as well.

This approach effectively keeps the communication private and leverages standard networking practices for secure cross-cloud connectivity. By controlling access within the EKS cluster first and then securing the network link, you are implementing a Defense-in-Depth strategy.

While your plan is sound, you might also want to consider the Kubernetes Gateway API and AWS VPC Lattice in the future as a more Kubernetes-native way to manage cross-VPC or even cross-cloud service exposure, although source notes that Azure's Gateway API implementation is less direct for outbound calls in this scenario. However, for establishing basic private connectivity, a VPN connection is a well-established and effective method.
