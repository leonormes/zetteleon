---
alias:
- Cross-Cluster HTTPS
- DNS-IP Ownership Model
- External Ingress SSL
created: 2026-02-05 00:00:00+00:00
modified: 2026-07-04 10:51:00+00:00
permalink: llmeon/30-library/so-t/so-t-external-ingress-ssl-architecture
tags:
- cert-manager
- cloudflare
- ingress
- kubernetes
- sot
- ssl
title: SoT - External Ingress & SSL Architecture
prodos:
  kind: sot
  lifecycle: stable
---


## Minimum Viable Understanding (MVU)

When deploying FITFILE clusters behind customer-managed infrastructure, the core architectural principle is the decoupling of IP ownership from DNS control. Even if a customer owns the Public IP and firewall, FITFILE can maintain SSL integrity and automated certificate rotation (Let's Encrypt) using a centralized Cloudflare DNS model.

---

## 1. The Ownership Model: IP vs. DNS

A common friction point in customer onboarding is the assumption that the IP owner must also manage the DNS and Certificates. This is incorrect.

| Component | Owner | Responsibility |
|:--- |:--- |:--- |
| Public IP | Customer | Routing traffic from Internet/Cluster-B to the Cluster-A LoadBalancer. |
| Firewall | Customer | Allowing Port 443 (HTTPS) and Port 80 (for ACME HTTP-01 challenges). |
| Domain/DNS | FITFILE | Managing A-records in Cloudflare pointing to the Customer IP. |
| Certificates | FITFILE | Automating issuance via `cert-manager` inside the cluster. |

---

## 2. Certificate Options

For cluster-to-cluster (A $\to$ B) communication, the following certificate strategies are available:

| Strategy | Mechanism | Best For |
|:--- |:--- |:--- |
| Let's Encrypt | Public DNS (Cloudflare) + ACME. | Production (Gold Standard). Fully automated and globally trusted. |
| Private CA | Organization-internal CA. | Environments with strict air-gap requirements where Cluster-B already trusts the CA. |
| Self-Signed | Cluster-local issuance. | Dev/Testing only. Requires disabling SSL verification in Cluster-B (Security Risk). |

---

## 3. Implementation: Let's Encrypt Path

### A. DNS Configuration (Cloudflare)

Create an A-record pointing your managed domain to the customer's IP:

- `cluster-a.fitfile.net` $\to$ `195.171.151.154`

### B. Cert-Manager Configuration

Deploy a `ClusterIssuer` using the HTTP-01 solver. Note that the customer must allow inbound traffic on Port 80 from Let's Encrypt servers for this validation to succeed.

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: devops@fitfile.net
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - http01:
        ingress:
          class: nginx
```

### C. Ingress Definition

Annotate the Ingress resource to trigger certificate issuance. The resulting secret is stored in the local namespace and consumed by the NGINX Ingress Controller.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: external-service-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts: ["cluster-a.fitfile.net"]
    secretName: cluster-a-tls-cert
  rules:
  - host: "cluster-a.fitfile.net"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: destination-service
            port: { number: 80 }
```

---

## 4. The DNS-01 & Split-Horizon Pattern

For services on a private network (e.g., `192.168.x.x`), the standard HTTP-01 challenge is impossible because Let's Encrypt cannot reach the internal server.

### 4.1 The Elegant Solution: DNS-01

DNS-01 decouples "proving domain ownership" from "where the service runs." Validation happens entirely in the Public DNS layer (Cloudflare), which is always reachable by Let's Encrypt.

### 4.2 Split-Horizon Architecture

To make this work seamlessly, two parallel truths about the domain must exist:

| Layer | Zone | Purpose |
|:--- |:--- |:--- |
| Public (Cloudflare) | `fitfile.net` $\to$ Public IP | Serves `_acme-challenge` TXT records for Let's Encrypt. |
| Private (Azure/CoreDNS) | `fitfile.net` $\to$ Private IP | Routes internal traffic to the actual private workload. |

### 4.3 Why This Works

- No Firewall Holes: Zero inbound connectivity required from the internet to the private network.
- Trusted Everywhere: Once issued, the certificate is globally trusted by any client (internal or external).
- Automation: `cert-manager` updates the public TXT record via API, obtains the cert, and then cleans up.

---

## Related Knowledge

- [[SoT - FITFILE Secret Management Architecture]] (How cert secrets are synced/managed).
- [[Protocol - HIE--NNUH Network Debugging]] (Diagnostic steps for ingress timeouts).
