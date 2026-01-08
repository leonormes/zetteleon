---
aliases: ["ACM Private CA with Cert-Manager", "EKS Private Certs", "Private TLS Architecture"]
confidence: "5/5"
created: 2025-07-23T13:42:04Z
epistemic: "Technical/Architectural"
last_reviewed: 
modified: 2026-01-08T10:49:45+00:00
purpose: "To define the architecture for managing TLS certificates in private EKS clusters using AWS Private CA and Cert-Manager."
review_interval: "1 year"
see_also:
  - "[[SoT - Cloud Networking Core Components]]"
  - "[[SoT - Kubernetes Networking & DNS]]"
source_of_truth: []
status: "Active"
tags: ["aws", "cert-manager", "certificates", "eks", "security", "tls"]
title: SoT - AWS EKS Private Certificate Management
type: "SoT"
uid: 
updated: 
---

## SoT - AWS EKS Private Certificate Management

> **The Core Objective:** Secure internal traffic (East-West) and private ingress traffic (North-South) using TLS certificates issued by a Private CA, fully automated via Kubernetes-native primitives.

### 1. The Architecture

The system relies on three components working in concert:

1. **Trust Anchor:** **AWS Private CA (ACM PCA)**. The root of trust for the internal network.
2. **Automation Engine:** **cert-manager**. The Kubernetes controller that watches for certificate requests.
3. **Bridge:** **aws-privateca-issuer**. The plugin that allows cert-manager to "speak" to AWS PCA.

### 2. Implementation Mechanics

#### 2.1 The Trust Chain

- **Root CA:** Managed by AWS ACM PCA.
- **Intermediate CA:** Can be used for issuing certificates to specific clusters/regions.
- **Leaf Certificates:** Issued to individual Pods/Services.

#### 2.2 Integration (IRSA)

The `aws-privateca-issuer` Pod needs permissions to call the AWS API.

- **Mechanism:** **IAM Roles for Service Accounts (IRSA)**.
- **Policy:** `acm-pca:IssueCertificate`, `acm-pca:GetCertificate`.
- **Identity:** The Kubernetes Service Account is annotated with the IAM Role ARN.

### 3. Configuration Primitives

#### The ClusterIssuer (The Configuration)

Defines _which_ Private CA to use.

```yaml
apiVersion: awspca.cert-manager.io/v1beta1
kind: AWSPCAClusterIssuer
metadata:
  name: private-ca-issuer
spec:
  arn: <ACM_PCA_ARN>
  region: <AWS_REGION>
```

#### The Certificate (The Request)

Defines _what_ certificate is needed.

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
spec:
  secretName: my-service-tls
  dnsNames:
    - my-service.private.local
  issuerRef:
    group: awspca.cert-manager.io
    kind: AWSPCAClusterIssuer
    name: private-ca-issuer
```

### 4. Traffic Hair-pinning (NAT Loopback)

In private networking, internal clients often access services via their _public_ IP/DNS.

- **The Issue:** The router sees traffic destined for its own public IP coming from the LAN.
- **The Fix:** **NAT Hair-pinning** (Loopback). The router translates the destination (Public IP) -> (Private IP) and reflects the packet back to the LAN.
- **Relevance:** Critical for testing Ingress endpoints from within the VPC/VPN without Split-Horizon DNS.

### 5. Best Practices

- **Private Endpoints:** Ensure the EKS API server is private-only or restricted.
- **Rotation:** Let cert-manager handle rotation automatically (short-lived certs = better security).
- **Network Policies:** certificates encrypt the data, but Network Policies restrict _who_ can connect. Use both.
