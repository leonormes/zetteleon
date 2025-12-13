---
aliases: []
confidence: 
created: 2025-03-27T09:30:48Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ingress, k8s, networking]
title: Securely Exposing AWS EKS Service to Azure AKS
type: 
uid: 
updated: 
version: 
---

## Problem Statement

Expose a service named `relay` running in a private AWS EKS cluster to an Azure AKS cluster, ensuring maximum security.

## Requirements

- **Secure Communication:** Encrypted communication between AKS and EKS.
- **Mutual Authentication:** Both AKS and EKS should verify each other's identity.
- **Fine-Grained Authorization:** Control which AKS pods can access the `relay` service.
- **Minimal Exposure:** Avoid exposing unnecessary services or ports.
- **Scalability and Reliability:** The solution should be robust and scalable.

## Solution Architecture

We'll use a combination of AWS PrivateLink, an Ingress Controller, and mutual TLS (mTLS) for secure communication.

### 1. AWS Side (EKS)

1.  **Network Load Balancer (NLB) with PrivateLink:**
    - Create an NLB in your AWS VPC that targets the `relay` service.
    - Configure the NLB to listen on a specific port (e.g., 443).
    - Create a VPC endpoint service for the NLB, enabling PrivateLink.
2.  **Ingress Controller (e.g., Nginx Ingress):**
    - Deploy an Ingress Controller in your EKS cluster.
    - Configure the Ingress Controller to route traffic to the `relay` service.
    - configure the ingress to require TLS.
3.  **Mutual TLS (mTLS):**
    - Generate client and server certificates.
    - Configure the Ingress Controller to require client certificates for authentication.
    - Store the server certificate in AWS Secrets Manager for secure access.
4.  **Security Groups:**
    - Restrict NLB security group to allow traffic only from the VPC endpoint.
    - Restrict the EKS worker node security groups to only allow ingress from the NLB.

### 2. Azure Side (AKS)

1.  **VPC Endpoint Connection:**
    - In Azure, create a Private Endpoint connection to the AWS PrivateLink service.
    - This will create a private IP address in your AKS VNet that resolves to the NLB.
2.  **Ingress Configuration:**
    - configure the AKS pods to use the private endpoint as the service url.
    - configure the AKS pods to send the client certificate for mTLS.
3.  **Certificate Management:**
    - Store the client certificate in Azure Key Vault for secure access.
4.  **Network Security Groups (NSGs):**
    - Restrict AKS NSGs to only allow outbound traffic to the AWS Private Endpoint.
    - Restrict access to the Azure Keyvault, to only the pods that require the client certificate.

### Detailed Steps

#### AWS Configuration

1.  **Deploy the `relay` Service:**
    - Ensure your `relay` service is running in your EKS cluster.
2.  **Create NLB and VPC Endpoint Service:**
    - Use `kubectl expose` or create an NLB manually via the AWS console or CLI.
    - Create the VPC Endpoint Service, and take note of the service name.
3.  **Deploy Ingress Controller:**
- Use Helm to deploy Nginx Ingress Controller.
- Configure the Ingress to route traffic to the `relay` service.
- Configure the ingress to use the Server certificate stored in AWS secrets manager.
- Configure the ingress to require client certificate authentication.
- Example ingress configuration:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: relay-ingress
  annotations:
    nginx.ingress.kubernetes.io/auth-tls-secret: "default/client-ca-secret" # client certificate CA
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
spec:
  tls:
  - secretName: server-tls-secret # Server certificate and key.
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: relay
            port:
              number: 80
```

4.  **Generate and Manage Certificates:**
    - Use `openssl` or a certificate authority to generate client and server certificates.
    - Create a Kubernetes secret containing the client CA certificate and the server certificate.
    - Store the Server certificate in AWS secrets manager.
5.  **Configure Security Groups:**
    - Restrict NLB security group to allow traffic only from the Azure VPC endpoint.
    - Restrict the EKS worker node security groups to only allow ingress from the NLB.

#### Azure Configuration

1.  **Create Private Endpoint Connection:**
    - In Azure, create a Private Endpoint connection to the AWS PrivateLink service, using the service name recorded earlier.
    - Note the private IP address of the endpoint.
2.  **Configure AKS Pods:**
- configure the AKS pods to use the private IP address of the AWS private endpoint.
- configure the AKS pods to send the client certificate for mTLS.
- Example pod configuration:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: aks-relay-client
spec:
  containers:
  - name: client
    image: curlimages/curl
    command: ["curl", "--cacert", "/etc/ssl/certs/ca.pem", "--cert", "/etc/ssl/certs/client.pem", "--key", "/etc/ssl/certs/client-key.pem", "https://<private-endpoint-ip>"]
    volumeMounts:
    - name: certs
      mountPath: /etc/ssl/certs/
  volumes:
  - name: certs
    secret:
      secretName: client-tls-secret
```

3.  **Manage Certificates:**
    - Store the client certificate in Azure Key Vault.
    - Create a Kubernetes secret containing the client certificate.
4.  **Configure Network Security Groups (NSGs):**
    - Restrict AKS NSGs to only allow outbound traffic to the AWS Private Endpoint.
    - Restrict access to the Azure Keyvault, to only the pods that require the client certificate.

## Security Considerations

-   **mTLS:** Enforces mutual authentication and encrypts communication.
-   **PrivateLink:** Avoids exposing the EKS service to the public internet.
-   **Least Privilege:** Security groups and NSGs restrict network access.
-   **Certificate Management:** Securely store and manage certificates using AWS Secrets Manager and Azure Key Vault.
-   **Regular Audits:** Regularly review security configurations and logs.

## Conclusion

This architecture provides a secure and scalable way to expose your AWS EKS `relay` service to an Azure AKS cluster. By leveraging AWS PrivateLink and mTLS, you minimize the attack surface and ensure secure communication.

Yes, absolutely! Using the Kubernetes Gateway API is an excellent, modern approach that can simplify and enhance the security of exposing your EKS service. It provides a more flexible and expressive way to manage external access compared to traditional Ingress resources

Here's how you can incorporate the Gateway API into the EKS side of the solution, along with the benefits:

## Securely Exposing AWS EKS Service to Azure AKS (Gateway API)

### Using Kubernetes Gateway API in EKS

Instead of relying solely on the Nginx Ingress Controller and standard Ingress resources, we can leverage the Kubernetes Gateway API for a more robust and flexible solution.

#### Benefits of Gateway API

-   **Role-Oriented:** Separates infrastructure configuration from application routing, aligning with organizational roles.
-   **Extensible:** Supports advanced routing features and custom extensions.
-   **Portable:** Provides a standardized API for various gateway implementations.
-   **Advanced Traffic Management:** Native support for features like traffic splitting, header-based routing, and weighted routing.
-   **Improved Security:** Enables more granular control over TLS and authentication.

#### Implementing Gateway API in EKS

1.  **Install a Gateway API Implementation:**
    - Install a Gateway API implementation like Gateway API with AWS Load Balancer Controller.
    - This controller will manage the AWS resources (NLB, etc.) based on your Gateway API resources.
2.  **Define a Gateway Resource:**
    - Create a `Gateway` resource that defines the NLB and its listeners.
    - Configure the Gateway to listen on port 443 for HTTPS.
- Example `Gateway` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
  name: relay-gateway
spec:
  gatewayClassName: aws-load-balancer-controller # or your gateway implementation
  listeners:
  - protocol: HTTPS
    port: 443
    tls:
      mode: Terminate
      certificateRefs:
      - name: server-tls-secret # Server certificate and key.
        namespace: default
```

1.  **Define a `HTTPRoute` Resource:**
- Create an `HTTPRoute` resource to route traffic to the `relay` service.
- Configure mTLS requirements within the `HTTPRoute` using the `clientCertificate` filter.
- Example `HTTPRoute` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: relay-route
spec:
  parentRefs:
  - name: relay-gateway
  hostnames:
  - "relay.internal" # Internal hostname (not used for public resolution)
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    filters:
    - type: RequestHeaderModifier
      requestHeader:
        set:
        - name: X-Client-Certificate-Validated
          value: "true" # used for logging or application logic.
    - type: ClientCertificate
      parameters:
        caCertificates:
        - name: client-ca-secret
          namespace: default
    backendRefs:
    - name: relay
      port: 80
```

4.  **Configure AWS Load Balancer Controller:**
    - The AWS Load Balancer Controller will provision an NLB based on the `Gateway` resource.
    - It will also handle TLS termination using the server certificate.
5.  **PrivateLink Integration:**
    - The AWS Load Balancer Controller should configure the NLB to be used with PrivateLink, as previously outlined.

#### Integration with Azure AKS

The Azure AKS side remains largely the same:

-   Create a Private Endpoint connection to the AWS PrivateLink service.
-   Configure AKS pods to use the private endpoint IP and provide the client certificate.

#### Benefits of Using Gateway API

-   **Enhanced Security:** Native support for mTLS and certificate management.
-   **Simplified Configuration:** Easier to manage complex routing scenarios.
-   **Improved Scalability:** Leverages the AWS Load Balancer Controller for efficient NLB management.
-   **Future-Proof:** Aligns with the evolving Kubernetes networking landscape.

#### Considerations

-   **Gateway API Implementation:** Choose a Gateway API implementation that supports AWS Load Balancer Controller or other NLB management.
-   **Certificate Management:** Ensure secure storage and management of certificates.
-   **Compatibility:** Verify compatibility between your Gateway API implementation and EKS version.

By integrating the Kubernetes Gateway API, you can create a more robust, secure, and manageable solution for exposing your EKS service to Azure AKS. This approach leverages modern Kubernetes networking capabilities and aligns with best practices.

Using the Gateway API offers a more structured and powerful approach compared to the traditional Ingress resource, especially for complex routing and security requirements
