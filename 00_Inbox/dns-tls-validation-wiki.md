---
created: 2026-02-25T14:42:16+00:00
modified: 2026-02-25T14:42:33+00:00
title: dns-tls-validation-wiki
---

## DNS Split-Horizon & TLS Certificate Validation: nnuh-prod-1.fitfile.net

Date: 25 February 2026

Author: Leon

Environment: Azure AKS (UK South)—Private cluster with Cloudflare public DNS

---

### Overview

This document records the validation of the split-horizon DNS configuration and Let's Encrypt TLS certificate for `nnuh-prod-1.fitfile.net`. The split-horizon architecture enables DNS-01 ACME certificate issuance for a service that is only reachable on a private network.

#### Architecture Summary

```
┌──────────────────────────────────────────────────────────┐
│                    PUBLIC PATH                           │
│                                                          │
│  Remote cluster pod                                      │
│    → CoreDNS (172.20.0.10)                               │
│      → Upstream resolver                                 │
│        → Cloudflare NS (aragorn / carioca.ns.cloudflare) │
│          → 195.171.151.154 (public IP)                   │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                   PRIVATE PATH                           │
│                                                          │
│  Jumpbox / VNet workload                                 │
│    → 127.0.0.53 (systemd-resolved stub)                  │
│      → 168.63.129.16 (Azure wireserver DNS)              │
│        → Azure Private DNS Zone (fitfile.net)            │
│          → 192.168.200.40 (private IP, TTL 0)            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│              CERTIFICATE ISSUANCE                        │
│                                                          │
│  cert-manager (in AKS cluster)                           │
│    → Requests cert from Let's Encrypt                    │
│    → Creates _acme-challenge TXT in PUBLIC Cloudflare    │
│    → Let's Encrypt validates via PUBLIC DNS              │
│    → Certificate issued and stored as K8s Secret         │
│    → Same cert served on both public and private paths   │
└──────────────────────────────────────────────────────────┘
```

#### Why This Architecture

The service at `nnuh-prod-1.fitfile.net` runs on a private network (`192.168.200.40`) and is not reachable from the public internet. HTTP-01 ACME challenges require inbound HTTP access to the server, which is impossible here. DNS-01 challenges validate domain ownership entirely via public DNS TXT records, requiring no inbound connectivity. The split-horizon ensures internal clients route to the private IP while Let's Encrypt can still validate ownership via the public Cloudflare zone.

---

### Test 1: DNS Trace from Jumpbox (`dig +trace`)

Purpose: Map the full iterative DNS resolution chain from root servers to authoritative answer.

Command:

```bash
dig +trace +all nnuh-prod-1.fitfile.net
```

#### Results

| Step | Server | IP | Action |
|------|--------|----|--------|
| Local stub | systemd-resolved | `127.0.0.53` | Fetched root NS list |
| Root | c.root-servers.net | `192.33.4.12` | Delegated to `.net` gTLD servers |
| gTLD | j.gtld-servers.net | `192.48.79.30` | Delegated to Cloudflare NS |
| Authoritative | aragorn.ns.cloudflare.com | `108.162.193.67` | Returned A record |

Public answer: `195.171.151.154` (TTL 300)

#### Observations

- IPv6 unreachable on jumpbox: `dig +trace` attempted IPv6 root server `2001:503:c27::2:30` three times before falling back to IPv4. This adds latency but does not affect resolution. Use `dig -4 +trace` to skip IPv6 attempts.
- Cloudflare is the public authoritative NS for `fitfile.net`, with nameservers `aragorn.ns.cloudflare.com` and `carioca.ns.cloudflare.com`.

---

### Test 2: Local Resolver Configuration

Purpose: Identify the upstream DNS forwarder used by the jumpbox.

#### /etc/resolv.conf

```
nameserver 127.0.0.53
options edns0 trust-ad
search mqmpnomypeweblilpgky3mmijc.zx.internal.cloudapp.net
```

The jumpbox uses `systemd-resolved` as a local stub resolver. The search domain confirms this is an Azure VM.

#### Resolvectl Status

```
Global
         Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
  resolv.conf mode: stub

Link 2 (eth0)
    Current Scopes: DNS
    Current DNS Server: 168.63.129.16
           DNS Servers: 168.63.129.16
            DNS Domain: mqmpnomypeweblilpgky3mmijc.zx.internal.cloudapp.net
```

Upstream resolver: `168.63.129.16` (Azure wireserver DNS). This is the resolver that intercepts queries and checks Azure Private DNS Zones before forwarding to public DNS.

---

### Test 3: Normal Resolution from Jumpbox (Split-Horizon Validation)

Purpose: Confirm the private DNS zone overrides the public record for internal clients.

Command:

```bash
dig nnuh-prod-1.fitfile.net
```

#### Result

```
nnuh-prod-1.fitfile.net. 0  IN  A  192.168.200.40
```

- SERVER: `127.0.0.53` (systemd-resolved → `168.63.129.16`)
- TTL: `0`—characteristic of Azure Private DNS Zones
- Flags: `qr aa rd ra ad`—the `aa` (authoritative answer) flag confirms Azure's resolver is answering directly from a Private DNS Zone, not forwarding to Cloudflare

#### Split-Horizon Comparison

| Path | Answer | TTL | Source |
|------|--------|-----|--------|
| `+trace` (iterative, public) | `195.171.151.154` | 300 | Cloudflare authoritative NS |
| Normal query (via Azure DNS) | `192.168.200.40` | 0 | Azure Private DNS Zone |

Split-horizon confirmed. Internal VNet traffic resolves to the private IP; external traffic resolves to the public IP.

---

### Test 4: Azure Private DNS Zone Lookup

Purpose: Locate the Private DNS Zone responsible for the override.

Command:

```bash
az network private-dns zone list --query "[].{Zone:name, RG:resourceGroup}" --output table
```

#### Result

| Zone | Resource Group |
|------|----------------|
| `725e1bce-a49c-4025-b2d7-4bd997c04024.privatelink.uksouth.azmk8s.io` | `rg-ff-uks-gp-aks` |

Note: No `fitfile.net` Private DNS Zone was found in this subscription. The zone answering `192.168.200.40` is either in a different subscription (cross-subscription VNet link), served by a DNS Private Resolver with a forwarding ruleset, or configured via custom DNS on the VNet. Further investigation required to locate the exact source.

---

### Test 5: TLS Certificate Validation from Jumpbox (Private Path)

Purpose: Verify the Let's Encrypt certificate is correctly served on the private endpoint.

Command:

```bash
openssl s_client -connect 192.168.200.40:443 \
  -servername nnuh-prod-1.fitfile.net </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

#### Result

| Field | Value |
|-------|-------|
| Subject | `CN=nnuh-prod-1.fitfile.net` |
| Issuer | `C=US, O=Let's Encrypt, CN=R12` |
| Not Before | 27 January 2026 14:02:52 UTC |
| Not After | 27 April 2026 14:02:51 UTC |
| SAN | `DNS:nnuh-prod-1.fitfile.net` |

#### Certificate Chain

```
0: CN=nnuh-prod-1.fitfile.net        ← Leaf (Let's Encrypt R12)
1: CN=R12, O=Let's Encrypt           ← Intermediate (signed by ISRG Root X1)
```

Full chain present (2 certificates). No missing intermediates.

#### TLS Details

| Property | Value |
|----------|-------|
| Protocol | TLSv1.3 |
| Cipher | `TLS_AES_256_GCM_SHA384` |
| Key Exchange | X25519 (253 bits) |
| Server Key | RSA 2048 bit |
| Verification | `OK (return code: 0)` |

---

### Test 6: ACME Challenge Cleanup

Purpose: Confirm no lingering DNS-01 challenge TXT records exist after issuance.

Command:

```bash
dig +short TXT _acme-challenge.nnuh-prod-1.fitfile.net @1.1.1.1
```

Result: Empty (no TXT record). cert-manager cleaned up the challenge record after successful validation.

---

### Test 7: Cert-manager Certificate Resource

Purpose: Verify the Kubernetes Certificate resource is in a healthy state.

Command:

```bash
kubectl describe certificate fitfile-nnuh -n nnuh-prod-1
```

#### Status

| Field | Value |
|-------|-------|
| Ready | `True` |
| Message | Certificate is up to date and has not expired |
| Not Before | 27 January 2026 14:02:52 UTC |
| Not After | 27 April 2026 14:02:51 UTC |
| Renewal Time | 28 March 2026 14:02:51 UTC |
| Revision | 2 |
| Secret | `fitfile-nnuh-tls` |

#### Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Issuer | `letsencrypt-prod` (ClusterIssuer) | DNS-01 solver via Cloudflare API |
| Duration | `8760h` (365 days) | Requested duration; Let's Encrypt always issues 90-day certs |
| Renew Before | `720h` (30 days) | Renewal triggers 30 days before expiry |
| Private Key | RSA 2048, PKCS1 | Standard key configuration |

Revision 2 confirms the certificate has already been successfully renewed once since initial creation on 28 November 2025. The auto-renewal pipeline is operational.

---

### Test 8: TLS Certificate Validation from Remote Cluster (Public Path)

Purpose: Verify the certificate is valid and trusted when accessed via the public DNS path from a remote cluster.

Commands run from a debug pod (`nicolaka/netshoot`) in the remote cluster:

#### DNS Resolution

```bash
dig nnuh-prod-1.fitfile.net
```

| Field | Value |
|-------|-------|
| Answer | `195.171.151.154` (public IP) |
| TTL | 30 |
| Server | `172.20.0.10` (CoreDNS / kube-dns) |

No private DNS zone override in the remote cluster—resolution goes to the public Cloudflare record as expected.

#### Certificate Check

```bash
openssl s_client -connect nnuh-prod-1.fitfile.net:443 \
  -servername nnuh-prod-1.fitfile.net </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

| Field | Value |
|-------|-------|
| Subject | `CN=nnuh-prod-1.fitfile.net` |
| Issuer | `C=US, O=Let's Encrypt, CN=R12` |
| Not Before | 27 January 2026 14:02:52 UTC |
| Not After | 27 April 2026 14:02:51 UTC |
| SAN | `DNS:nnuh-prod-1.fitfile.net` |

Same certificate served on both the public and private paths.

#### HTTP Connectivity

```bash
curl -vI https://nnuh-prod-1.fitfile.net
```

| Property | Value |
|----------|-------|
| TLS | TLSv1.3 / `TLS_AES_256_GCM_SHA384` / X25519 / RSASSA-PSS |
| HTTP | HTTP/2 302 |
| Certificate trusted | Yes |

Service is reachable and responding with a redirect (302), confirming end-to-end connectivity.

---

### Summary

| Test | Status | Notes |
|------|--------|-------|
| DNS trace (public chain) | ✅ Pass | Root →.net → Cloudflare → `195.171.151.154` |
| Split-horizon (private override) | ✅ Pass | Azure DNS returns `192.168.200.40` (TTL 0) |
| TLS cert—private path | ✅ Pass | Let's Encrypt R12, valid, full chain |
| TLS cert—public path | ✅ Pass | Same cert, same chain |
| ACME challenge cleanup | ✅ Pass | No lingering TXT records |
| cert-manager status | ✅ Pass | Ready, revision 2, auto-renewal scheduled 28 March 2026 |
| Remote cluster connectivity | ✅ Pass | HTTP/2 302 via public IP, TLSv1.3 |

#### Next Renewal

cert-manager will automatically renew the certificate on 28 March 2026 (30 days before the 27 April 2026 expiry). No manual action required.

#### Open Item

The Azure Private DNS Zone serving `fitfile.net` → `192.168.200.40` was not found in the current subscription (`4ae8fd93-d084-481f-ba6e-370b7d4d8d0d`). It may reside in a different subscription with a cross-subscription VNet link, or be served by a DNS Private Resolver / custom DNS configuration. This should be documented separately for operational clarity.
