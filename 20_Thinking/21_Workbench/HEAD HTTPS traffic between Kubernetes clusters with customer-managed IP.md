---
title: "HTTPS traffic between Kubernetes clusters with customer-managed IP"
source: "https://claude.ai/chat/d245c6eb-a011-4ace-bc8f-5bb33d730abe"
captured: "2026-02-05T11:09:45+00:00 2026-02-05T11:09:45+00:00"
status: "processing"
tags:
  - "input"
type: "head"
created: 2026-02-05T11:09:47+00:00
modified: 2026-02-05T11:10:08+00:00
---
## Raw Output / Content
I have 2 k8s clusters, A and B. B needs to send A some https traffic. A has a public IP for ingress. 195.171.151.154. This IP is managed by our customer, along with the firewall and routing to our private clusters LB ingress. Explain the different Certificate options in this scenario. If they own the IP do they have to set up the DNS record? Can I do it with our cloudflare account? Can I then use letsencrypt to create the cert? Where does the private cert go? Our nginx-ingress controller?

Great question! Let me break down the certificate options and DNS/IP ownership considerations for your setup.

## Certificate Options

### 1. **Let's Encrypt with Public DNS (Recommended)**

- **How it works**: You create a DNS record pointing to 195.171.151.154, Let's Encrypt validates domain ownership via HTTP-01 or DNS-01 challenge, issues cert
- **Where cert goes**: Yes, the private key + cert go in your nginx-ingress controller (as a Kubernetes Secret, referenced by your Ingress resource)
- **Pros**: Free, automated renewal, trusted by all clients
- **Cons**: Requires public DNS record and Let's Encrypt being able to reach your endpoint

### 2. **Self-Signed Certificate**

- **How it works**: Generate your own cert/key pair, install in nginx-ingress
- **Pros**: No DNS needed, works immediately, full control
- **Cons**: Cluster B needs to trust the cert (add to trust store or disable verification - not ideal for production)

### 3. **Private CA Certificate**

- **How it works**: Use your organization's internal CA to issue the cert
- **Pros**: Trusted within your org if CA is already distributed
- **Cons**: Cluster B must trust your private CA

### 4. **Commercial Certificate**

- **How it works**: Buy cert from DigiCert, etc., similar flow to Let's Encrypt
- **Pros**: May be required by some enterprise policies
- **Cons**: Costs money, manual renewal processes

## DNS and IP Ownership - Key Points

**Critical distinction**: IP ownership ≠ DNS control

- **Your customer owns the IP** (195.171.151.154) but that doesn't mean they control DNS
- **DNS is separate**: Whoever owns the domain name controls the DNS records
- **You CAN use your Cloudflare account** if:
    - You own/control the domain name (e.g., `yourcompany.com`)
    - You want to create `cluster-a.yourcompany.com` → 195.171.151.154

**Your customer does NOT need to set up DNS** unless you're using their domain name.

## Typical Setup (Let's Encrypt Path)

```yaml
# 1. In Cloudflare (your account):
#    Create A record: cluster-a.yourcompany.com → 195.171.151.154

# 2. In Cluster A, install cert-manager
# 3. Create ClusterIssuer for Let's Encrypt:
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@yourcompany.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx

# 4. Create Ingress with TLS:
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - cluster-a.yourcompany.com
    secretName: cluster-a-tls  # cert-manager creates this
  rules:
  - host: cluster-a.yourcompany.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

## What Needs to Happen

**Customer side:**

- Ensure firewall allows traffic from Cluster B → 195.171.151.154:443
- Route traffic to your cluster's LoadBalancer
- For Let's Encrypt HTTP-01 challenge: allow traffic from Let's Encrypt servers (0.0.0.0/0:80) temporarily during cert issuance

**Your side:**

- Create DNS record in Cloudflare pointing to customer's IP
- Install cert-manager in Cluster A
- Configure Ingress with TLS + cert-manager annotations
- Private key stays in Cluster A (never leaves) as a Kubernetes Secret

**Cluster B:**

- Just needs to trust public CAs (default) if using Let's Encrypt
- Or needs your self-signed cert added to trust store

The beauty of this setup: you control the DNS (via Cloudflare), they control the IP/routing, and Let's Encrypt bridges the gap by validating you control the domain name.