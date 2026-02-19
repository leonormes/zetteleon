---
created: 2025-12-04T12:02:41Z
last_reviewed: null
modified: 2026-02-16T14:59:28+00:00
status: processing
tags: [state/thinking]
title: HEAD - What PKI is Doing here
type: head
updated: null
---

Here's how PKI (certs / trust / identity) fits together in _your_ setup, with AKS private clusters across tenants, N calling L and M, Cloudflare DNS, and cert-manager.

## 1) What PKI is Doing here (in One sentence)

PKI gives (a) L/M a server identity ("I am api.l.example.com") via a TLS certificate, and optionally gives (b) N a client identity ("I am cluster N / service X") via a client certificate if you choose mTLS—while the Azure IP firewalls just decide who is allowed to connect at the network layer.

---

## 2) The Network Facts You Gave (and what They imply)

- Cluster N: private AKS, but it has public egress IP (typically via NAT Gateway / firewall).
- Clusters L and M: private AKS, but they expose something with public ingress IP protected by IP allowlist firewall.
- Traffic direction: N → L and N → M.
- DNS: Cloudflare is authoritative DNS (and maybe proxy, depending on orange-cloud vs grey-cloud).
- Certs: cert-manager issues certs inside each cluster.

Important takeaway:

The firewall on L/M doesn't "do PKI". It only ensures _only N's egress IP_ (or other allowlisted IPs) can reach TCP/443 on the public ingress.

---

## 3) The "normal" TLS Story (most common): Server-only TLS

This is the default if you're not explicitly doing mTLS.

### Step-by-step (N Calling L)

1. N resolves DNS (via Cloudflare) for something like:
    
    - service.l.example.com → public ingress IP of L (or to a Cloudflare edge IP if proxied).

2. N opens TLS to that endpoint on 443.
3. L presents a server certificate at the ingress (nginx/AGIC/Traefik/etc), issued by cert-manager.
4. N validates:
    
    - Hostname matches (SAN contains service.l.example.com)
    - Certificate chain is valid up to a trusted root (public CA like Let's Encrypt, or your private CA if you've distributed trust)
    - Not expired / revoked (revocation is usually not checked in-cluster unless you've built that in)

5. If valid: encrypted HTTPS proceeds.
6. Separately, L's firewall allowlists N's egress public IP so the connection can even reach the ingress.

### What Cert-manager is Doing here

- In L and M, cert-manager is creating/renewing the leaf TLS certs used by the ingress.
- With Cloudflare in the mix, most people use ACME DNS-01 validation:
    - cert-manager creates _acme-challenge.service.l.example.com TXT records via Cloudflare API
    - Let's Encrypt validates via DNS
    - cert-manager stores the cert in a Kubernetes Secret
    - ingress uses that Secret for TLS

Key point:

Your public egress IP (N) and public ingress allowlist (L/M) don't change the PKI mechanics—PKI still hinges on DNS name ↔ certificate SAN ↔ trusted CA chain.

---

## 4) The Cloudflare Fork in the Road: "DNS only" Vs "proxied"

Everything changes depending on whether Cloudflare is just DNS (grey cloud) or reverse proxy (orange cloud).

### A) Cloudflare as DNS only (grey cloud)

- DNS points directly to L/M public ingress IP.
- N connects directly to L/M.
- TLS cert at L/M must be valid for that hostname (usually public CA like Let's Encrypt).
- L/M firewall allowlists N's egress IP ✅ (works cleanly)

### B) Cloudflare Proxied (orange cloud)

- DNS resolves to Cloudflare edge IPs, not your ingress IP.
- N's TLS connection is to Cloudflare, not L/M.
- Then Cloudflare makes a second connection from Cloudflare → L/M ("origin").

This has two big implications:

1. Your L/M firewall cannot just allowlist N's egress IP anymore, because the inbound traffic to L/M will come from Cloudflare egress IP ranges, not from N.
    
    - So you'd need to allowlist Cloudflare IPs (or use Cloudflare Tunnel / a different pattern).

2. The cert story becomes "two-hop TLS":
    
    - N ↔ Cloudflare: cert is Cloudflare's edge cert for service.l.example.com
    - Cloudflare ↔ L/M: origin cert can be:
        - A normal publicly-trusted cert (Let's Encrypt via cert-manager), or
        - A Cloudflare Origin CA cert (trusted by Cloudflare, not by the public internet)

If you _are_ using allowlisted ingress IP firewalls and want traffic _only from N_, Cloudflare proxying often makes that awkward unless you redesign the ingress model.

---

## 5) If You want

## Cluster-to-cluster Identity

##: mTLS is the PKI Upgrade

Server-only TLS answers: "Am I talking to L?"

It does not strongly answer: "Is the caller really N (and which workload in N)?"

If you need cryptographic caller identity (beyond "came from N's egress IP"), you add mutual TLS (mTLS).

### How mTLS Looks in Your Setup

- L/M still present server certs (as above).
- N also presents a client cert during TLS handshake.
- L/M validate the client cert against a CA they trust and apply authorization rules (CN/SAN, SPIFFE ID, etc.)

### Where Do Those Client Certs come From?

Typical options:

1. A shared private CA for inter-cluster traffic
    
    - You operate an internal root/intermediate (Vault, Smallstep, cert-manager CA issuer, etc.)
    - L/M ingress trusts that CA for client cert verification
    - N issues client certs from that CA to its workloads
    - Pros: strong identity; Cons: you must run and secure CA and distribute trust

2. Service mesh identity (SPIFFE-like)
    
    - Istio/Linkerd/Consul/etc. give each workload an identity and rotate certs automatically
    - Pros: best ergonomics + rotation; Cons: more moving parts

3. Keep server-only TLS + add application auth
    
    - E.g., OAuth2/JWT between services, signed tokens, etc.
    - Pros: no client cert plumbing; Cons: different trust model, still good though

Reality check: With public ingress endpoints, mTLS is usually what "PKI in this situation" means if you want real cluster/service identity, not just encryption.

---

## 6) What Changes because the Clusters Are in Different Azure Tenants?

Almost nothing at the PKI layer.

- TLS doesn't care about Azure tenants.
- Tenants affect networking and identity integration, not the certificate math.
- Each cluster can run its own cert-manager issuers independently.
- If you introduce mTLS with a shared internal CA, you'll just be sharing trust across tenants (which is normal, but you'll want tight controls on CA keys and issuance).

---

## 7) Common Pitfalls in Exactly This Pattern

- Hostname mismatch: cert issued for service.l.example.com but N connects to an IP or different name → fails.
- Cloudflare proxy + IP allowlisting conflict: L/M see Cloudflare IPs, not N.
- Using HTTP-01 ACME from private clusters: usually fails unless solver is reachable publicly; DNS-01 is the typical fix (and you're already on Cloudflare + cert-manager, so you're likely doing this right).
- Thinking IP allowlisting = identity: it's a _coarse network control_; mTLS or tokens give identity.

---

## 8) The Clean Mental Model

Think of it as three independent layers:

1. Routing & reachability
    
    - Cloudflare DNS resolves names
    - Azure firewall on L/M allows inbound only from allowed IPs (either N's egress or Cloudflare's, depending on proxying)

2. Encryption & server identity (TLS)
    
    - L/M ingress terminates TLS using cert-manager-managed certs
    - N validates the server cert chain + hostname

3. Caller identity & authorization (optional, but often the real goal)
    
    - mTLS client certs or JWT/OAuth between services
    - Enforce "only this service in N may call this endpoint in L/M"

---

If you tell me just one detail—is Cloudflare orange-cloud (proxied) or grey-cloud (DNS only) for the L/M hostnames N calls?—I can map your exact handshake and firewall behavior precisely. But even without that, the key PKI decision point is: server-only TLS (basic) vs mTLS (strong cluster/workload identity).
