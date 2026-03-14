---
aliases: [OIDC Auth for VSO, Vault Kubernetes Authentication Best Practice, VSO JWT Auth]
created: 2026-03-12T09:30:00Z
modified: 2026-03-14T11:10:12+00:00
status: evergreen
tags: [architecture, jwt, kubernetes, oidc, security, vault, vso]
title: SoT - VSO Authentication (JWT vs AppRole)
type: SoT
updated: 2026-03-12
---

## SoT - VSO Authentication (JWT Vs AppRole)

### 1. The Context: The "Callback" Limitation

When running Vault Secrets Operator (VSO) in a Kubernetes cluster with a remote Vault instance (e.g., HCP Vault), standard Kubernetes authentication often fails.

- Standard Kubernetes Auth Method: Requires Vault to communicate back to the Kubernetes API server via the `TokenReview` API to verify the ServiceAccount token.
- The Problem: If the Kubernetes API is private or behind a firewall, HCP Vault cannot "reach back" (callback) to verify the token.

---

### 2. Comparison: JWT (OIDC) vs. AppRole

| Feature | JWT with OIDC Discovery | AppRole |
|:--- |:--- |:--- |
| Mechanism | Short-lived ServiceAccount Token | Static `RoleID` + `SecretID` |
| Connectivity | No Callback Needed. Vault verifies token locally via public OIDC/JWKS endpoint. | No Callback Needed. Vault verifies static creds directly. |
| Security | Highest (Zero Trust). No static secrets stored in K8s. Tokens are ephemeral. | Medium. Static `SecretID` must be stored as a K8s Secret ("Secret Zero" risk). |
| Maintenance | Low. Native Kubernetes identity management. | High. Requires rotation/management of `SecretID`. |

---

### 3. Why JWT (OIDC) is Best Practice

For your scenario (HCP Vault + Private AKS/EKS), JWT with OIDC Discovery is the most secure and modern option.

#### A. Eliminates "Secret Zero"

With AppRole, you have to find a way to get the `SecretID` into the cluster securely. If an attacker gains access to the Kubernetes namespace, they can steal the `SecretID` and gain persistent access to Vault. With JWT, the "credential" is the ServiceAccount itself—there is no static password to steal.

#### B. Ephemeral & Automatic

VSO automatically requests a short-lived JWT from Kubernetes and presents it to Vault. These tokens are cryptographically signed by the cluster and expire quickly. There is no manual rotation required.

#### C. Network Compatible

By configuring Vault with the cluster's OIDC Issuer URL, Vault can download the cluster's public keys (JWKS). It then validates the JWTs presented by VSO mathematically, without ever needing to talk to your Kubernetes API server.

---

### 4. How it Works (The Logic Flow)

1. Kubernetes signs a JWT for the VSO ServiceAccount.
2. VSO sends this JWT to Vault via the JWT Auth backend.
3. Vault looks at the `iss` (issuer) claim in the JWT.
4. Vault fetches the cluster's public keys from the OIDC discovery endpoint (e.g., `https://oidc.eks.us-east-1.amazonaws.com/…/.well-known/openid-configuration`).
5. Vault verifies the signature. If valid, it issues a Vault Token based on the matched Role.

---

### 5. Summary Recommendation

Continue using the JWT engine. It is significantly more secure than AppRole because it leverages native, ephemeral Kubernetes identities and eliminates the risk of static credential theft. It is the industry-standard "Zero Trust" pattern for cross-environment authentication.
