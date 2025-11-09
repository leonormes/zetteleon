---
aliases: []
confidence: 
created: 2025-10-24T15:33:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [AKS, authentication, cloud-native, EKS, IAM, mTLS, OIDC]
title: Authentication Summary for AKS, EKS, and Terraform Cloud
type:
uid: 
updated: 
version:
---

For cloud-native environments utilizing Azure Kubernetes Service (AKS), Amazon Elastic Kubernetes Service (EKS), and Terraform Cloud, a modern authentication stack revolves around specific integrations and technologies:

- **Terraform Cloud ↔ Kubernetes (EKS/AKS):** Authentication for Terraform runs should leverage **OIDC-based dynamic provider credentials**. This allows Terraform to obtain short-lived tokens directly from the Kubernetes cluster's OIDC provider.
- **In-cluster services ↔ Cloud APIs:** Services running within Kubernetes clusters (EKS/AKS) should authenticate to cloud APIs using native identity federation. Examples include **IAM roles for service accounts (EKS)** or **AKS Managed Identity**, which provide workloads with short-lived, fine-grained access to cloud resources.
- **Inter-service within clusters:** For communication between services *within* the Kubernetes cluster, implement **mTLS via SPIFFE** or utilize **OAuth2 client credential tokens** issued by a secrets provider like Vault.

In summary, the modern authentication stack for these platforms is built upon **OIDC + OAuth2 client credentials + mTLS**, all underpinned by **short-lived, cryptographically signed tokens** (e.g., RSA/ECDSA).

Links:

- [[Recommended Best Practices for Cloud-Native Authentication]]
- Terraform Cloud OIDC Integration
- Kubernetes Service Account IAM Roles
- AKS Managed Identity
- Inter-Service mTLS in Kubernetes
- OAuth2 Client Credentials Flow
- Secret Management Solutions
- Modern Cloud-Native Authentication MOC
