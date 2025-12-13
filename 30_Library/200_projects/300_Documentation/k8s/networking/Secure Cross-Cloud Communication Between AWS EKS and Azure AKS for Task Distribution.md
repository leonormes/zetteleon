---
aliases: []
confidence: 
created: 2025-03-19T03:21:08Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ingress, networking]
title: Secure Cross-Cloud Communication Between AWS EKS and Azure AKS for Task Distribution
type: plan
uid: 
updated: 
version: 
---

## 1. Introduction

The secure and efficient exchange of information between services residing in different cloud environments presents a significant challenge in modern distributed systems. This report addresses the specific requirement of establishing secure communication between a privately deployed Amazon Elastic Kubernetes Service (EKS) cluster and an Azure Kubernetes Service (AKS) cluster. Within the AWS EKS cluster, a custom service named 'relay' functions as a task queue, distributing jobs to external nodes. An external node, hosted within an Azure AKS cluster and running a service called 'bunny', needs to periodically poll 'relay' for tasks and subsequently return the results of these jobs. The primary objectives are to achieve this communication while adhering to stringent security standards and maintaining the simplicity of the solution. This report will outline a detailed work plan that prioritizes security and leverages the principle of least privilege to grant the 'bunny' service the necessary access to the 'relay' service.

## 2. Understanding the Current Architecture

The current architecture involves two distinct Kubernetes clusters hosted on separate cloud platforms. A thorough understanding of the characteristics of each cluster and their interaction requirements is crucial for designing a secure and effective communication strategy.

### 2.1 Private AWS EKS Cluster

The AWS EKS cluster in question is fully private, indicating that its Kubernetes API server endpoint is not directly accessible from the public internet 1. This private nature enhances the security posture of the cluster by limiting the attack surface. Communication with the API server is restricted to within the cluster's Virtual Private Cloud (VPC) or connected networks. The 'relay' service, a custom task queue, is deployed within this secure environment. As a custom application, the access controls for 'relay' will need to be specifically configured within the Kubernetes environment to ensure only authorized entities can interact with it.

### 2.2 Azure AKS Cluster

The Azure AKS cluster hosts the 'bunny' service, which acts as a worker node. The primary function of 'bunny' is to initiate outbound connections to the 'relay' service in the AWS EKS cluster. This involves periodically querying 'relay' for new tasks that need processing. Once a task is completed, 'bunny' must also be capable of securely transmitting the results back to the 'relay' service.

### 2.3 Communication Requirements

The interaction between 'bunny' and 'relay' necessitates two primary communication flows. Firstly, 'bunny' needs to periodically poll 'relay' to discover and retrieve available tasks. This communication must be initiated from the Azure environment towards the AWS environment. Secondly, after processing a task, 'bunny' must send the results back to 'relay'. This flow also originates from Azure and targets the AWS service. Both communication channels must be established securely, ensuring the confidentiality and integrity of the data exchanged.

## 3. Establishing Secure Network Connectivity

To enable communication between the 'bunny' service in Azure and the 'relay' service in the private AWS EKS cluster, a secure network connection must be established between the two cloud environments. Two primary options can be considered: leveraging AWS PrivateLink for cross-cloud access or implementing a secure VPN connection.

### 3.1 Option 1: Leveraging AWS PrivateLink for Cross-Cloud Access

AWS PrivateLink offers a mechanism for establishing private connectivity between VPCs and services without exposing traffic to the public internet 6. This technology is particularly advantageous for cross-account and cross-VPC communication, as it ensures that network traffic remains within the secure AWS network 12.

#### 3.1.2 Creating a Network Load Balancer (NLB) for 'relay' in AWS EKS

To expose the 'relay' service through PrivateLink, a Network Load Balancer (NLB) needs to be provisioned in the AWS EKS cluster's VPC 9. This NLB should reside within the private subnets of the EKS VPC, ensuring that the 'relay' service is not directly exposed to the public internet. The NLB will be configured to listen on the appropriate port for the 'relay' service, which, for security best practices, should be an HTTPS port (e.g., 443). A target group will then be created and associated with the NLB. This target group will contain the 'relay' service's pods as targets. Depending on the networking configuration within the EKS cluster, using IP addresses as targets might be necessary to ensure direct routing to the pods. An internal NLB is recommended in this scenario to further restrict access within the private network.

#### 3.1.3 Creating an AWS PrivateLink Endpoint Service

Once the NLB is in place, an AWS PrivateLink Endpoint Service needs to be created in the AWS account hosting the EKS cluster 9. This Endpoint Service will be associated with the NLB created in the previous step. Upon creation, AWS will generate a unique Endpoint Service Name, following a format similar to `com.amazonaws.vpce.<region>.<endpoint_service_id>`. This service name will be essential for establishing the connection from the Azure side. The Endpoint Service acts as the service provider interface for PrivateLink, advertising the availability of the 'relay' service through the NLB.

#### 3.1.4 Creating an Interface VPC Endpoint in Azure

To consume the PrivateLink service from Azure, an Interface VPC Endpoint must be created within the Azure Virtual Network where the AKS cluster and the 'bunny' service reside 9. When creating the endpoint, the service category should be selected as "Endpoint services that use NLBs and GWLBs" 15. The Endpoint Service Name obtained from AWS will then be entered to identify the target service. The appropriate Azure VNet and subnets where the 'bunny' service is located should be selected for the endpoint. Additionally, an Azure Network Security Group should be associated with the endpoint to control the inbound and outbound traffic. This Interface Endpoint in Azure will establish a private connection to the AWS Endpoint Service, allowing 'bunny' to communicate with 'relay' without traversing the public internet.

#### 3.1.5 Granting Cross-Account Access

By default, the PrivateLink Endpoint Service in AWS is not accessible to other AWS accounts. To allow the Azure account (or specific principals within it) to connect, explicit permissions must be granted 9. This typically involves adding the Azure account ID or the Amazon Resource Names (ARNs) of specific IAM users or roles within the Azure account as allowed principals on the AWS Endpoint Service. The AWS side will then likely need to accept the connection request initiated from the Azure endpoint 9. This granular control over access ensures that only authorized entities can establish a connection through PrivateLink, enhancing the overall security.

#### 3.1.6 DNS Resolution

For the 'bunny' service in Azure to communicate with the 'relay' service via the PrivateLink endpoint, proper DNS resolution is essential. The Interface Endpoint created in Azure will be associated with private IP addresses within the Azure VNet. The 'bunny' service will need to resolve a DNS name to these private IP addresses. Private DNS options in Azure can simplify this process, allowing 'bunny' to access 'relay' using a familiar DNS name without relying on public DNS resolvers 6. This ensures seamless and secure communication using private IP addresses that are not routable over the public internet.

### 3.2 Option 2: Implementing a Secure VPN Connection

An alternative approach to establishing secure network connectivity is to implement a Site-to-Site VPN connection between the AWS and Azure virtual networks 29. This involves creating an encrypted tunnel over the public internet between the two environments. This method requires configuring VPN Gateways on both the AWS (Virtual Private Gateway) and Azure (VPN Gateway) sides.

#### 3.2.2 Configuring the AWS Virtual Private Gateway (VPG)

In the AWS account, a Virtual Private Gateway (VPG) needs to be created and attached to the EKS VPC. Subsequently, a Customer Gateway should be created in AWS, specifying the public IP address of the Azure VPN Gateway. A Site-to-Site VPN Connection is then established, linking the VPG and the Customer Gateway. This step involves configuring the tunnel settings, such as the IPsec protocol and pre-shared key. Finally, the route tables in the AWS VPC need to be updated to route traffic destined for the Azure VNet's CIDR block through the VPG.

#### 3.2.3 Configuring the Azure VPN Gateway

On the Azure side, a VPN Gateway must be created within the Azure VNet where the AKS cluster resides. A Local Network Gateway is then configured, specifying the public IP address of the AWS VPG and the AWS VPC's CIDR block. A Connection is created, linking the Azure VPN Gateway and the Local Network Gateway, with matching connection settings (IPsec, pre-shared key) as configured on the AWS side. Similar to AWS, the route tables in the Azure VNet need to be updated to route traffic destined for the AWS VPC's CIDR block through the Azure VPN Gateway.

#### 3.2.4 Security Considerations for VPN

While a VPN connection provides secure communication through encryption, it relies on traffic traversing the public internet. Therefore, it is crucial to implement strong IPsec configurations and ensure secure management of the pre-shared keys. Compared to PrivateLink, a VPN might introduce increased network complexity due to the need for managing routing configurations on both sides. For the specific use case of securely exposing a single service, PrivateLink offers a more streamlined and potentially less complex solution by providing service-level connectivity that keeps traffic within the AWS network.

### 3.3 Comparison of PrivateLink and VPN

The following table summarizes the key differences between AWS PrivateLink and a VPN connection for this scenario:

|   |   |   |
|---|---|---|
|**Feature**|**AWS PrivateLink**|**VPN Connection**|
|Connectivity|Service-level (specific service exposed)|Network-level (entire VPC or subnet)|
|Public Internet|No exposure|Traffic traverses the public internet (encrypted)|
|Complexity|Generally simpler for point-to-point service access|Can be more complex to configure and manage routes|
|Security|Strong isolation, traffic stays within AWS network|Secure with proper IPsec configuration|
|Use Cases|Ideal for exposing specific services privately|Suitable for broader network connectivity between clouds|
|Cross-Account|Built-in support|Requires careful configuration of routing and security|

Given the requirement for securely exposing a single service ('relay') in a least privileged manner, AWS PrivateLink appears to be the more suitable option due to its service-level connectivity and the fact that it avoids exposing traffic to the public internet.

## 4. Implementing Least Privileged Access for 'bunny'

Once secure network connectivity is established, implementing least privileged access for the 'bunny' service to interact with the 'relay' service is paramount. This involves configuring appropriate authentication and authorization mechanisms.

### 4.1 Authentication Mechanisms

Authentication is the process of verifying the identity of the 'bunny' service before granting it access to 'relay' 34. Two primary authentication mechanisms can be considered: Mutual TLS (mTLS) and API Key Authentication over HTTPS.

#### 4.1.1 Mutual TLS (mTLS) Authentication

Mutual TLS (mTLS) provides a robust two-way authentication mechanism where both the client ('bunny') and the server ('relay') authenticate each other using X certificates 36. This ensures that 'relay' verifies the identity of 'bunny' before accepting requests, and 'bunny' can also verify the identity of 'relay'.

Implementation on 'relay' (AWS EKS):

Implementing mTLS on the 'relay' service within the AWS EKS cluster can be achieved through several methods. One option is to configure an Ingress controller, such as Nginx or Traefik, to handle mTLS authentication for the 'relay' service 46. This involves creating a TLS secret in Kubernetes that contains the Certificate Authority (CA) certificate used to sign 'bunny's' client certificate. The Ingress controller would then be configured to require and verify client certificates for requests to the 'relay' service. Another approach is to leverage the mTLS capabilities of a service mesh like Istio or Linkerd, if one is deployed in the cluster 41. Alternatively, mTLS can be implemented directly within the 'relay' service application itself. Regardless of the chosen method, a Certificate Authority (CA) is required to issue and manage the certificates for both 'relay' and 'bunny' 36. This could involve using AWS Private CA or a similar service in Azure. The 'relay' service must be configured to require the presentation of a client certificate from 'bunny' and to validate it against the trusted CA.

Implementation on 'bunny' (Azure AKS):

On the Azure AKS side, the 'bunny' service needs to be configured to present its client certificate when making HTTPS requests to the 'relay' service. Additionally, 'bunny' must be configured to trust the CA certificate used by the 'relay' service to ensure the authenticity of the server.

Security Benefits of mTLS:

mTLS offers strong mutual authentication, ensuring that both parties in the communication are verified. It also encrypts the traffic, providing confidentiality and protecting against man-in-the-middle attacks 38.

Complexity Considerations:

Implementing mTLS can introduce complexity related to certificate management, including issuance, rotation, and revocation 43. Proper configuration on both the 'bunny' and 'relay' sides is crucial for successful mTLS authentication.

#### 4.1.2 API Key Authentication over HTTPS

API key authentication involves the 'bunny' service including a secret API key in the headers of its HTTPS requests to the 'relay' service for authentication 50. The 'relay' service then validates this key to verify the identity of the requester.

Implementation on 'relay' (AWS EKS):

The 'relay' service within the AWS EKS cluster needs to be configured to expect and validate the API key provided by 'bunny'. This validation can be implemented at the application level, or through an API gateway or Ingress controller. The API keys should be stored securely within Kubernetes Secrets 50.

Implementation on 'bunny' (Azure AKS):

On the Azure AKS side, the 'bunny' service needs to securely store the API key and include it in the headers of its HTTPS requests to the 'relay' service.

Security Considerations:

API keys are sensitive secrets and must be protected from unauthorized access 45. Transmitting the API key over HTTPS is essential to prevent eavesdropping. For enhanced security, consider implementing API key rotation 52.

Complexity:

API key authentication is generally simpler to implement compared to mTLS, as it does not involve the complexities of certificate management.

### 4.2 Authorization Strategies (on AWS EKS for 'relay')

Once the 'bunny' service is authenticated, authorization mechanisms need to be in place on the 'relay' service to ensure that 'bunny' only has access to the necessary actions and resources 34. Kubernetes Role-Based Access Control (RBAC) and Network Policies are crucial for implementing this least privileged access.

#### 4.2.1 Kubernetes Role-Based Access Control (RBAC)

Kubernetes RBAC can be used to define granular permissions for the 'bunny' service within the AWS EKS cluster 1. This ensures that even if 'bunny' is successfully authenticated, it can only perform actions that it is explicitly authorized to do.

A dedicated ServiceAccount should be created for the 'bunny' service within the AWS EKS cluster. Then, a Role or ClusterRole should be defined that grants this ServiceAccount only the specific permissions required to interact with the 'relay' service. For example, if 'bunny' only needs to poll for tasks and return results via specific API endpoints, the Role should grant permissions for `get` and `post` requests on those particular paths. Finally, a RoleBinding or ClusterRoleBinding should be created to associate the defined Role or ClusterRole with the 'bunny' ServiceAccount. This binding ensures that the permissions defined in the Role are applied to the 'bunny' ServiceAccount.

#### 4.2.2 Network Policies

Kubernetes Network Policies can be implemented in the AWS EKS cluster to control the network traffic to and from the pods running the 'relay' service 54. These policies operate at Layer 3 and Layer 4 of the [[OSI Model]], allowing for fine-grained control over pod-to-pod and pod-to-external network communication.

Network Policies should be configured to allow inbound traffic to the 'relay' pods only from the specific IP range or pods associated with the Azure AKS cluster (if these are static and feasible to identify) or, more securely, through the private IP addresses associated with the AWS PrivateLink endpoint. Outbound traffic from the 'relay' pods should also be restricted to only the necessary destinations. Implementing Network Policies provides network-level segmentation, limiting the potential impact of a security breach by restricting lateral movement within the cluster.

## 5. Security Best Practices and Recommendations

To further enhance the security of the communication between 'bunny' and 'relay', several security best practices should be followed.

### 5.1 Network Segmentation

It is crucial to ensure that the EKS cluster nodes and the 'relay' service are deployed in private subnets within the AWS VPC. Security groups in both AWS and Azure should be utilized to control traffic at the instance level, allowing only necessary inbound and outbound connections. Within the EKS cluster, Kubernetes Network Policies should be implemented for pod-level network segmentation, as discussed in the previous section.

### 5.2 Secure Secrets Management

Sensitive information such as API keys and private keys used for mTLS should be stored securely using Kubernetes Secrets 50. For a more robust solution, consider using a dedicated secrets management tool like AWS Secrets Manager or HashiCorp Vault, which offers features like encryption at rest, access control, and automated secret rotation 54.

### 5.3 Least Privilege IAM Roles

The IAM roles assigned to the EKS nodes and any other AWS resources interacting with the cluster must adhere to the principle of least privilege 54. This means granting only the permissions necessary for each resource to perform its intended function. For pods requiring access to AWS services, utilize IAM Roles for Service Accounts (IRSA) to provide workload-specific IAM permissions 1.

### 5.4 Monitoring and Logging

Implement comprehensive monitoring and logging for both the AWS EKS and Azure AKS clusters. This should include network traffic logs, Kubernetes API access logs, and application logs from both the 'bunny' and 'relay' services. Set up alerts to notify administrators of any suspicious or anomalous activity.

### 5.5 Regular Security Audits

Conduct regular security audits of the entire setup, including network configurations, access control policies (IAM, RBAC, Network Policies), and application security practices. These audits help identify and address potential vulnerabilities.

### 5.6 Consider a Web Application Firewall (WAF)

If the 'relay' service exposes an HTTP/HTTPS endpoint for 'bunny' to poll, consider deploying a Web Application Firewall (WAF) such as AWS WAF or Azure WAF on Application Gateway 60. A WAF can protect the 'relay' service from common web vulnerabilities like SQL injection and cross-site scripting. The WAF could be placed in front of the NLB in AWS.

### 5.7 Secure Cross-Cloud Communication Best Practices

Always ensure that data in transit between the AWS and Azure environments is encrypted using TLS/SSL. Implement strong authentication and authorization mechanisms as detailed earlier. Minimize the attack surface by only exposing the necessary services and ports required for the 'bunny' and 'relay' interaction.

## 6. Conclusion

Establishing secure communication between the 'bunny' service in Azure AKS and the 'relay' service in a private AWS EKS cluster requires a well-defined strategy that prioritizes security and simplicity. Leveraging AWS PrivateLink for network connectivity offers a secure and efficient solution by providing service-level access without exposing traffic to the public internet. For authentication, either Mutual TLS (mTLS) or API key authentication over HTTPS can be implemented, with mTLS offering a higher level of security through two-way certificate-based authentication, albeit with increased complexity in certificate management. Regardless of the chosen authentication method, implementing Kubernetes Role-Based Access Control (RBAC) and Network Policies within the AWS EKS cluster is crucial for enforcing the principle of least privilege, ensuring that the 'bunny' service only has the necessary permissions to interact with the 'relay' service. Adhering to general security best practices, including network segmentation, secure secrets management, least privilege IAM roles, and comprehensive monitoring, will further strengthen the overall security posture of this cross-cloud communication. The recommended approach aims to provide a secure and manageable solution for the user's requirements, balancing security needs with operational considerations in a hybrid cloud environment.
