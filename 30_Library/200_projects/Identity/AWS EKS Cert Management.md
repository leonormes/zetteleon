---
aliases: []
confidence: 
created: 2025-07-23T13:42:04Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: AWS EKS Cert Management
type:
uid: 
updated: 
version:
---

**User:**

How do I learn about cert management in AWS EKS and private networking

## Initial Analysis

Your goal is to learn about certificate management in AWS EKS (Elastic Kubernetes Service) and private networking. Both are broad, technical topics with lots of moving parts, especially for a developer. To provide a comprehensive answer, I’ll break this into logical steps, ensuring you get a practical, actionable understanding.

### Step-by-Step Research Plan

1. **Clarify the Scope and Key Concepts**

- Define what “certificate management” means in the context of AWS EKS (e.g., TLS for services, Kubernetes secrets, ACM integration).
- Define “private networking” in EKS (e.g., VPC, private subnets, endpoint access).

2. **Certificate Management in AWS EKS**

- Research how certificates are typically used in EKS (internal/external traffic, service mesh, ingress controllers).
- Explore AWS-native options (like AWS Certificate Manager) and Kubernetes-native options (like cert-manager).
- Investigate best practices for automating certificate issuance, renewal, and rotation in

EKS.

3. **Private Networking in AWS EKS**

- Research how EKS clusters are deployed in private networks (VPC, subnets, NAT gateways).
- Explore how to restrict cluster/API access to private endpoints.
- Investigate best practices for securing workloads and communication within the cluster.

4. **Integrating Certificate Management with Private Networking**

- Research how private networking impacts certificate management (e.g., ACM Private CA, internal load balancers, DNS).
- Explore real-world scenarios and architectures combining both.

5. **Practical Guidance and Resources**

- Gather tutorials, AWS documentation, and open-source resources for hands-on learning.
- Summarize key takeaways and next steps for a developer to get started.

---

### The Most Critical Subtopic to Start with is

**Clarifying what certificate management means in AWS EKS, including the main use cases and tools involved.**

I’ll begin by researching this foundational subtopic.

In private networking scenarios within EKS, certificates are used to secure internal traffic, ensuring encrypted communication between services in VPCs and private subnets, while best practices include using internal load balancers and managing certificates through ACM or cert-manager.

I will explore the practical setup and automation of certificate management in a private EKS cluster, focusing on integrating ACM, cert-manager, and Kubernetes secrets effectively.

I will compile a list of high-quality resources, tutorials, and documentation to enhance your understanding of certificate management in a private EKS cluster.

## Certificate Management in AWS EKS and Private Networking: A Comprehensive Guide

This report provides an in-depth analysis and practical guidance on learning and implementing certificate management in AWS Elastic Kubernetes Service (EKS) within a private networking environment. It covers definitions, use cases, tools, detailed setup instructions, best practices, common pitfalls, and additional resources. The goal is to offer a thorough understanding enabling developers and operators to secure their Kubernetes workloads effectively in AWS.

---

## Introduction

Amazon EKS is a managed Kubernetes service that simplifies running containerized applications at scale. For secure communications between services and to protect data in transit, robust certificate management is essential. In environments where workloads run in private networks, certificate management becomes even more critical as the architecture relies on private subnets, internal load balancers, and secured endpoints. This report outlines how to manage TLS certificates using tools like AWS Certificate Manager (ACM), cert-manager, and Kubernetes Secrets while integrating with private networking components such as Virtual Private Clouds (VPC), private subnets, and internal endpoints.

---

## Certificate Management in AWS EKS

### What Is Certificate Management

At its core, certificate management involves provisioning, deploying, renewing, and revoking TLS certificates that secure communication between services and clients. Within EKS, certificates serve the following purposes:

- **Encryption in Transit:** Certificates enable HTTPS communication between services, ensuring data remains confidential.
- **Authentication:** Certificates verify the identity of communicating parties, which is pivotal for service-to-service trust.
- **Compliance:** Proper certificate management helps meet organizational, industry, and regulatory requirements for secure communications.

### Key Use Cases in AWS EKS

**Securing Service-to-Service Communication:**

Microservices often communicate via APIs that require end-to-end encryption. TLS certificates are assigned to secure both internal and external traffic.

- **Ingress Traffic Termination:** Ingress controllers (e.g., NGINX, AWS ALB Ingress) terminate TLS connections at the edge of the Kubernetes cluster. They rely on certificates to decrypt incoming traffic and forward requests securely.
- **Service Mesh Deployments:** When employing service meshes such as Istio or AWS App Mesh, mutual TLS (mTLS) is often enforced to provide both encryption and robust authentication between microservices.
- **Kubernetes Secrets Management:** Certificates can be stored securely as Kubernetes secrets. These secrets are then mounted into pods as needed, ensuring that sensitive keys are handled appropriately.

### Primary Tools and Techniques

1. **AWS Certificate Manager (ACM):**
   ACM is a managed service that handles the lifecycle of public and private TLS certificates. It integrates seamlessly with other AWS services, such as Application Load Balancers and Network Load Balancers, and simplifies the process of certificate renewal and deployment.

2. **cert-manager:**
   cert-manager is an open-source Kubernetes add-on that automates issuing and renewing certificates from various Certificate Authorities (CAs) including Let's Encrypt and ACM Private CA. It integrates tightly with Kubernetes through Custom Resource Definitions (CRDs) like Issuer, ClusterIssuer, and Certificate.

3. **Kubernetes Secrets:**
   Certificates and private keys stored as Kubernetes secrets can be injected into pods or referenced by Ingress resources. This native mechanism allows secure distribution of sensitive data to workloads running in the cluster.

---

## Private Networking in AWS EKS

### Understanding Private Networking

Running an EKS cluster within private networking confines means that all cluster components (control plane, nodes, and pods) operate within a VPC isolated from the public internet. Key elements include:

- \*\*Private Subnets
- Nodes and pods are deployed in subnets that are not directly reachable from the internet. Outbound traffic to external resources, when necessary, is routed through NAT gateways or VPC endpoints.
- **Internal Load Balancers:** Internal Application Load Balancers (ALBs) or Network Load Balancers (NLBs) are used for routing traffic within the VPC. Proper subnet tagging (for example, using `kubernetes.io/role/internal-elb`) is required to distinguish internal endpoints.
- **API Server Private Endpoints:** For additional security, the EKS API server can be configured to use a private endpoint, restricting access to within the VPC.

### Integrating Certificate Management with Private Networking

Certificate management in a private networking context must accommodate the unique architectural constraints:

- **ACM in Private Environments:**
  In clusters deployed in private subnets, ACM certificates are often used with internal load balancers. They ensure that even when services do not face the public internet, encryption remains enabled at the network edge.

- **cert-manager with Private CA:**
  Using cert-manager along with ACM Private CA allows for automated issuance and renewal of internal certificates. This is particularly useful for mTLS setups and for securing internal service communications.

- **Distribution via Kubernetes Secrets:**
  Certificates stored as secrets ensure that internal applications have access to the required keys and certificates for establishing secure channels. When pods are configured with mounted secrets, it enables seamless TLS operations without exposing sensitive data externally.

- **Networking Best Practices:**
  Private endpoints, network policies, and VPC endpoints are used collectively to limit exposure and control traffic flows between services. This creates a layered security model ensuring that both network access and certificate usage conform to best practices.

---

## Detailed Setup and Automation in Private EKS

This section outlines the practical steps to set up and automate certificate management in a private AWS EKS cluster.

### Prerequisites

- AWS account with permissions for EKS, ACM, and IAM management.
- Installation of AWS CLI, `kubectl`, `eksctl`, and Helm.
- An operational EKS cluster deployed in private subnets with the correct subnet tagging.
- Access to a registered domain and its DNS configurations, typically via AWS Route 53.

### Step-by-Step Implementation

#### 1. Provisioning the EKS Cluster

If a cluster does not exist, create one using `eksctl`:

```sh
eksctl create cluster
--name eks-cluster
--version 1.24
--region us-east-1
--nodegroup-name eks-nodes
--node-type t3.medium
--nodes 2
```

After provisioning, verify the cluster:

```sh
kubectl get nodes
```

#### 2. Installing Cert-manager

cert-manager automates the certificate lifecycle. Install it using Helm:

```sh
kubectl create namespace cert-manager

helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert

-manager
--namespace cert-manager
--create-namespace
--set installCRDs=true
```

Confirm the cert-manager pods are running:

```sh
kubectl get pods -n cert-manager
```

#### 3. Configuring AWS Certificate Manager (ACM) for Private Use

1. **Creating a Private CA:**
   Use ACM Private CA to establish a private certificate authority.

```sh
aws acm-pca create-certificate-authority
 --certificate-authority-configuration file://ca-config.json
 --region us-east-1
```

2. **Downloading the CA Certificate:**
   Retrieve the certificate for reference by cert-manager.

```sh
aws acm-pca get-certificate-authority-certificate
 --certificate-authority-arn <CA_ARN>
 --region us-east-1
 --output text > ca-certificate.pem
```

3. **Setting up IAM Permissions:**
   Attach the `AWSCertificateManagerPrivateCAFullAccess` policy to the IAM role associated with your EKS worker nodes.

#### 4. Integrating the AWS Private CA Issuer with Cert-manager

1. \*\*Install the AWS

Private CA Issuer Plugin:\*\*

This plugin enables cert-manager to use ACM Private CA.

```sh
helm repo add awspca https://cert-manager.github.io/aws-privateca-issuer
helm repo update

helm install aws-privateca-issuer awspca/aws-privateca-issuer
 --namespace cert-manager
```

2. **Verify Installation:**

```sh
kubectl get pods -n cert-manager
```

#### 5. Configuring Cert-manager with ACM Private CA

Create a `ClusterIssuer` resource to tie cert-manager to your private CA. For example:

```yaml
apiVersion: awspca.cert-manager.io/v1beta1
kind: AWSPCAClusterIssuer
metadata:
name: private-ca-issuer
spec:
arn: <CA_ARN>
region: us-east-1
```

Apply the configuration:

```sh
kubectl apply -f cluster-issuer.yaml
```

Validate the issuer:

```sh
kubectl get AWSPCAClusterIssuer
```

#### 6. Issuing Certificates for Your Services

Create a `Certificate` resource to request a TLS certificate:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
name: example-cert


namespace: default
spec:
secretName: example-cert-tls
duration: 2160h   # Approximately 90 days
renewBefore: 360h # Renew 15 days before expiry
commonName: example.com
dnsNames:
- example.com
issuerRef:
name: private-ca-issuer
kind: ClusterIssuer
```

Deploy the certificate resource:

```sh
kubectl apply -f certificate.yaml
```

Inspect the certificate details:

```sh
kubectl describe certificate example-cert
```

The resulting certificate is stored as a Kubernetes secret (`example-cert-tls`).

#### 7. Using Certificates in Applications

To integrate TLS certificates into your applications:

1. **Mount the Secret into Pods:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: example-app
spec:
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - name: tls
          mountPath: /etc/tls
          readOnly: true
  volumes:
    - name: tls
      secret:
        secretName: example-cert-tls
```

Apply the changes:

```sh
kubectl

apply -f pod.yaml
```

2. **Configure Ingress with TLS:**

Use the secret in an Ingress resource for HTTPS termination:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: private-ca-issuer
spec:
  tls:
    - hosts:
        - example.com
      secretName: example-cert-tls
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: example-service
                port:
                  number: 80
```

Deploy the ingress:

```sh
kubectl apply -f ingress.yaml
```

---

## Best Practices for Secure Private Networking

### Using Private Endpoints

Secure the EKS API server by enabling private endpoints. Limiting access to the VPC prevents exposure to the public internet.

### Encrypting All Traffic

Ensure that every

internal communication channel, whether within microservices or through Ingress, is encrypted using TLS. This is achieved by integrating ACM or cert-manager to automate certificate lifecycles.

### Leveraging Network Policies

Configure Kubernetes Network Policies to control traffic flows between pods. This enforces a least-privilege model and reduces the attack surface.

### Tagging and VPC Endpoints

Tag private subnets (e.g., `kubernetes.io/role/internal-elb=1`) to ensure internal load balancers are provisioned correctly. Use VPC endpoints (AWS PrivateLink) for services like S3, ECR, and CloudWatch to avoid exposure via the internet.

### Automation and Monitoring

Use cert-manager’s built-in automation for certificate issuance and renewal. Monitor certificate status and expiration using logging tools like AWS CloudWatch, and set up alerts to proactively manage renewals.

---

## Common Pitfalls and Troubleshooting

- **IAM Permissions:**
  Ensure that EKS worker nodes have appropriate IAM policies for

governing access to ACM and ACM Private CA resources.

- **DNS Misconfiguration:**
  Validate that DNS records (e.g., Route 53 entries) correctly point to your internal load balancers.

- **ClusterIssuer Errors:**
  Double-check the configuration details in ClusterIssuer resources, especially ARN and region parameters, to prevent misconfigurations.

- **Ingress and Subnet Tagging Anomalies:**
  Improper annotations or missing subnet tags can prevent internal load balancers from being created. Confirm that subnets are tagged with `kubernetes.io/role/internal-elb` and that Ingress annotations align with your controller settings.

---

## Additional Resources and Tutorials

For further hands-on learning and deep dives, consider these authoritative resources:

- **Certificate Management:**
- [cert-manager on AWS EKS with Let’s Encrypt (official tutorial)](https://cert-manager.io/docs/tutorials/getting-started-aws-letsencrypt/)
- [AWS Prescriptive Guidance for end-to-end encryption in EKS](https://

docs.aws.amazon.com/prescriptive-guidance/latest/patterns/set-up-end-to-end-encryption-for-applications-on-amazon-eks-using-cert-manager-and-let-s-encrypt.html)

- [Integrating AWS Private CA with cert-manager](https://repost.aws/articles/ARaT9VMIc-QeO4iArg8S6nEg/integrating-external-pki-with-aws-private-ca-and-cert-manager-for-dynamic-cert-management-in-eks)
- [Kubernetes Certificate Signing in EKS](https://docs.aws.amazon.com/eks/latest/userguide/cert-signing.html)
- **Private Networking:**
- [AWS EKS Networking Best Practices](https://aws.github.io/aws-eks-best-practices/security/docs/network/)
- [Configuring Networking for EKS Clusters](https://docs.aws.amazon.com/eks/latest/userguide/eks-networking.html)
- [Network Security in EKS](https://docs.aws.amazon.com/eks/latest/best-practices/network-security.html)
- **Community and Workshops:**
- [AWS Blog on using private certificates in EKS](<https://aws.amazon.com/blogs/containers/use-private-certificates-to-enable-a-container-re>

pository-in-amazon-eks/)

- [EKS Security Immersion Workshop](https://aws.github.io/aws-eks-best-practices/security/docs/network/)
- [cert-manager Tutorials and Documentation](https://cert-manager.io/docs/tutorials/)

---

## Conclusion and Recommendations

Proper certificate management integrated with private networking practices is essential for securing an Amazon EKS cluster. By leveraging ACM, cert-manager, and Kubernetes secrets, and by deploying your workloads within a private VPC, you ensure that:

- Traffic is encrypted and authenticated end-to-end, whether for internal service communications or external endpoint access.
- Automation minimizes operational overhead and prevents lapses in certificate renewal.
- Network policies and private endpoints enforce strict access controls and reduce overall risk exposures.

For a seamless experience, follow best practices by meticulously configuring IAM, DNS, and network settings, and always monitor certificate status. The provided tutorials and

resources offer step-by-step guidance, enabling developers to tailor solutions to fit organizational requirements while maintaining robust security.

This comprehensive guide serves as a foundational resource for learning and applying certificate management in AWS EKS with private networking. Embrace continuous monitoring, regular reviews, and proactive updates to maintain a secure, resilient infrastructure.

---

## References

- AWS Documentation on [EKS Networking](https://docs.aws.amazon.com/eks/latest/userguide/eks-networking.html)
- AWS Documentation on [Certificate Signing in EKS](https://docs.aws.amazon.com/eks/latest/userguide/cert-signing.html)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [AWS Prescriptive Guidance for EKS Security](https://aws.github.io/aws-eks-best-practices/security/docs/network/)
- [AWS Private CA Resources](https://aws.amazon.com/private-ca/resources/)

By following the steps, best practices, and leveraging the recommended resources, you can master

certificate management in AWS EKS while ensuring robust private networking for secure, scalable container deployments.

Warning: Some URLs are invalid

- kubernetes.io/ingress.class
- docs.aws.amazon.com/prescriptive-guidance/latest/patterns/set-up-end-to-end-encryption-for-applications-on-amazon-eks-using-cert-manager-and-let-s-encrypt.html
- cert-manager.io/v1
- kubernetes.io/role/internal-elb=1
- <file://ca-config.json>
- kubernetes.io/role/internal-elb
- cert-manager.io/cluster-issuer
- networking.k8s.io/v1
- https://
- awspca.cert-manager.io/v1beta1

**User:**

In networking terminology what is traffic hair-pinning?

**Abacus AI ChatLLM:**

> Routing to Gemini 2.5 Flash

That's a great question! "Traffic hair-pinning," also known as "NAT hair-pinning," "NAT loopback," or "loopback NAT," is a networking scenario where a client on the *internal* side of a network (behind a NAT device, like a router) tries to access a server that is also on the *internal* side of the same network, but it tries to reach that server using its *external* (public) IP address or hostname.

Here's a breakdown of what happens and why it's called "hair-pinning":

## How it Works

1. **Client Request:** An internal client (e.g., your laptop) wants to connect to an internal server (e.g., a web server on your home network).
2. **External Address:** Instead of using the server's internal IP address (e.g., 192.168.1.100), the client uses the network's public IP address (e.g., 203.0.113.5) or a domain name that resolves to that public IP.
3. **Router/NAT Device:** The client's request goes to the router. The router sees that the destination IP address is its own public IP.
4. **NAT Translation:** The

router performs Network Address Translation (NAT) on the incoming request, just as it would for an external client. It translates the public IP to the internal IP of the server.

5. **Loopback:** Instead of sending the traffic out to the internet and back in (which is what would happen if an *external* client made the request), the router "loops" the traffic back internally to the server. This is where the "hair-pin" analogy comes from – the traffic goes out to the router and then immediately "pins" back into the internal network.
6. **Server Response:** The server receives the request and sends its response back to the router.
7. **Reverse NAT:** The router performs the reverse NAT translation, sending the response back to the original internal client.

## Why It's a "thing"

It often comes up when you've set up port forwarding on your router to allow external access to a service on your internal network (like a game server or a personal website). If you then try to access that same service from *within*

your network using the external IP or domain name, you're relying on hair-pinning to work.

## Potential Issues

While many modern routers support hair-pinning, some older or simpler routers might not. If a router doesn't support it, the internal client's request using the external IP will fail because the router doesn't know how to loop the traffic back.

In such cases, internal clients would need to use the server's *internal* IP address or a local DNS entry to resolve the hostname to the internal IP.

Does that make sense? It's a bit of a quirky networking concept, but quite common!

Of course. Let's break down how cert-manager works conceptually and then walk through the specific steps to set it up with AWS Private Certificate Authority.

---

## How Cert-manager Works: An Overview

At its core, cert-manager is an automated certificate lifecycle management tool for Kubernetes. Think of it as an automated administrative assistant within your cluster whose sole job is to obtain, renew, and manage TLS certificates.

It works by introducing a set of Custom Resource Definitions (CRDs) into your cluster, which become new, native-feeling parts of the Kubernetes API.

The main components in the workflow are:

1. **`Certificate`:** This is the resource you, the user, create. It's a declaration of *what* you want. It specifies details like the domain names (`dnsNames`) for the certificate, the name of the Kubernetes `Secret` where the final certificate and private key should be stored, and a reference to an `Issuer` or `ClusterIssuer` that will fulfil the request.
2. **`Issuer` or `ClusterIssuer`:** This resource represents a certificate authority (CA) and defines *how* to get the certificate. It contains the configuration for a specific CA, such as Let's Encrypt, a self-signed CA, or, in your case, AWS Private CA.
   - An `Issuer` is a namespaced resource, meaning it can only be used to sign `Certificate`s in the same namespace.
   - A `ClusterIssuer` is a cluster-scoped version that can sign `Certificate`s from any namespace.

3. **`CertificateRequest`:** This is an internal, low-level resource that cert-manager creates automatically. It represents a single, one-shot request to an `Issuer` for a signature against a specific Certificate Signing Request (CSR). You typically don't interact with this resource directly.

### The Workflow

The entire process is a chain of events triggered by the creation of a `Certificate` resource:

1. **Request:** A user creates a `Certificate` resource.
2. **CSR Generation:** The cert-manager controller sees the new `Certificate`. It generates a private key, creates a Certificate Signing Request (CSR) for the domains specified, and creates a `CertificateRequest` resource containing this CSR.
3. **Issuance:** The controller for the specified `Issuer` (e.g., the AWS Private CA issuer) sees the `CertificateRequest`. It validates the request and sends the CSR to the configured Certificate Authority (the AWS Private CA API).
4. **Signing:** The CA signs the CSR and returns a signed certificate.
5. **Storage:** The `Issuer` controller receives the signed certificate and updates the `CertificateRequest` resource's status with it.
6. **Completion:** The main `Certificate` controller sees the `CertificateRequest` is now "Ready". It retrieves the signed certificate and the initially generated private key and saves them into the target Kubernetes `Secret` defined in the `Certificate` resource.
7. **Renewal:** cert-manager continuously monitors the certificate. Before it expires (the renewal time is configurable), it automatically repeats this process to get a new certificate.

---

## Setting up Cert-manager with AWS Private CA

To use AWS Private Certificate Authority, you need an "external issuer". This is a separate controller that understands how to communicate with the AWS API. The most common one is `aws-privateca-issuer`.

Here is the step-by-step guide to get it running.

### Prerequisites

- A running Kubernetes cluster (this guide assumes Amazon EKS).
- `kubectl` and `helm` are installed and configured.
- cert-manager is already installed in your cluster.
- You have an existing **AWS Private Certificate Authority** created in your AWS account. If not, you can create one in the AWS Console under "AWS Certificate Manager" -> "Private CAs".

### Step 1: Install the AWS Private CA Issuer Plugin

This component is not part of the standard cert-manager installation and must be installed separately. It runs its own controller pod in your cluster.

Bash

```sh
# Add the Helm repository for the aws-privateca-issuer
helm repo add awspca https://cert-manager.github.io/aws-privateca-issuer

# Install the issuer into its own namespace
helm install --create-namespace -n aws-privateca-issuer aws-privateca-issuer awspca/aws-privateca-issuer
```

### Step 2: Configure AWS IAM Permissions Using IRSA

The `aws-privateca-issuer` pod needs permissions to call the AWS Private CA APIs (`acm-pca`). The most secure and standard way to grant these permissions on EKS is using **IAM Roles for Service Accounts (IRSA)**.

1. Create an IAM Policy:

   This policy grants the minimum required permissions for the issuer to function. Save this as aws-privateca-issuer-policy.json.

   JSON

   ```sh
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "acm-pca:DescribeCertificateAuthority",
                   "acm-pca:GetCertificate",
                   "acm-pca:IssueCertificate"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

   Now, create the policy in AWS:

   Bash

   ```sh
   aws iam create-policy \
       --policy-name AWSPrivateCAIssuerPolicy \
       --policy-document file://aws-privateca-issuer-policy.json
   ```

   *Take note of the returned Policy ARN.*

2. Create an IAM Role with a Trust Relationship:

   You'll need your EKS cluster's OIDC provider URL. You can find it with:

   Bash

```sh
aws eks describe-cluster --name <YOUR_CLUSTER_NAME> --query "cluster.identity.oidc.issuer" --output text
```

Now, create a file `trust-policy.json`. This policy allows the Kubernetes Service Account used by the issuer to assume this IAM Role.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/<OIDC_PROVIDER_URL>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "<OIDC_PROVIDER_URL>:sub": "system:serviceaccount:aws-privateca-issuer:aws-privateca-issuer"
        }
      }
    }
  ]
}
```

    Replace `<ACCOUNT_ID>` and `<OIDC_PROVIDER_URL>` (without the `https://`).

    Create the IAM Role and attach the policy:

    Bash

    ```
    # Create the role
    aws iam create-role --role-name AWSPrivateCAIssuerRole --assume-role-policy-document file://trust-policy.json

    # Attach the permissions policy from the previous step
    aws iam attach-role-policy --role-name AWSPrivateCAIssuerRole --policy-arn <POLICY_ARN_FROM_STEP_1>
    ```

    _Take note of the returned Role ARN._

3. Annotate the Kubernetes Service Account:

   The Helm chart has already created a Service Account named aws-privateca-issuer in the aws-privateca-issuer namespace. You just need to annotate it with the ARN of the role you just created.

   Bash

   ```sh
   kubectl annotate serviceaccount aws-privateca-issuer \
     -n aws-privateca-issuer \
     "eks.amazonaws.com/role-arn=arn:aws:iam::<ACCOUNT_ID>:role/AWSPrivateCAIssuerRole"
   ```

   After annotating, you may need to restart the issuer pod for the changes to take effect:

   Bash

   ```sh
   kubectl rollout restart deployment -n aws-privateca-issuer aws-privateca-issuer
   ```

### Step 3: Create an `AWSPCAClusterIssuer`

Now, you can create the `ClusterIssuer` resource in Kubernetes that tells cert-manager how to use your AWS Private CA.

YAML

```sh
# awspca-cluster-issuer.yaml
apiVersion: awspca.cert-manager.io/v1beta1
kind: AWSPCAClusterIssuer
metadata:
  name: "aws-private-ca"
spec:
  # The ARN of your AWS Private Certificate Authority
  arn: "arn:aws:acm-pca:eu-west-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012"
  # The AWS region your Private CA is in
  region: "eu-west-1"
```

Replace the `arn` and `region` with your specific values and apply it:

```sh
kubectl apply -f awspca-cluster-issuer.yaml
```

Check its status to ensure it's `Ready`:

```sh
kubectl describe awspcaclusterissuer aws-private-ca
```

### Step 4: Request a Certificate

You are now ready to request a certificate. Create a `Certificate` resource that references your new `AWSPCAClusterIssuer`.

```yaml
# my-app-certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-app-tls
  namespace: my-app
spec:
  secretName: my-app-tls-secret
  dnsNames:
    - my-app.mydomain.co.uk
  issuerRef:
    name: "aws-private-ca"
    kind: AWSPCAClusterIssuer
    group: awspca.cert-manager.io
```

Apply the file. cert-manager will now follow the workflow described above. After a few moments, a new `Secret` named `my-app-tls-secret` will be created in the `my-app` namespace containing the signed certificate and private key, ready to be mounted into your application's pods.
