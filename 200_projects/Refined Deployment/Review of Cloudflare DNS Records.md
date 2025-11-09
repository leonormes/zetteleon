---
aliases: []
confidence:
created: 2025-09-10T08:46:12Z
epistemic:
last_reviewed:
modified: 2025-11-03T13:48:18Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [topic/technology/networking/dns]
title: Review of Cloudflare DNS Records
type:
uid:
updated:
version:
---

Based on the Cloudflare DNS export you've provided and the cert-manager issues we've been troubleshooting, let me review and align the DNS configuration with your current setup.

## Review of Cloudflare DNS Records

From your export file ([fitfile.net.txt](file:///Users/leon.ormes/Downloads/fitfile.net.txt)), I can see:

```sh
;; Domain:     fitfile.net.
;; SOA Record
fitfile.net 3600 IN SOA aragorn.ns.cloudflare.com. dns.cloudflare.com. 2050916036 10000 2400 604800 3600
```

This confirms that:

- ✅ `fitfile.net` is managed by Cloudflare (SOA: aragorn.ns.cloudflare.com)
- ✅ The domain is properly configured with Cloudflare's nameservers

## Key Findings and Alignment Issues

### 1. **Proxy Configuration is Correct**

Your cert-manager pod already has the proxy configured:

- HTTP_PROXY: `http://10.252.142.180:8080/`
- NO_PROXY includes internal networks and `10.2.0.10` (your internal DNS)

### 2. **The Real Issue: DNS Traffic Through Proxy**

The problem is that **DNS traffic (port 53) cannot go through an HTTP proxy**. When cert-manager tries to reach `173.245.59.67:53` (Cloudflare's DNS), it's attempting a direct TCP connection on port 53, which your HTTP proxy cannot handle.

### 3. **Domain Delegation Analysis**

- `fitfile.net` → Managed by Cloudflare ✅
- `privatelink.fitfile.net` → Managed by Azure Private DNS ❌ (as shown in previous queries)

## Recommended DNS Configuration Alignment

### 1. **Configure Cert-manager to Use Internal DNS resolver**

Since your internal DNS at `10.2.0.10` can successfully resolve the ACME challenges, configure cert-manager to use it:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cert-manager
  namespace: cert-manager
data:
  # Use your internal DNS server that can reach both internal and external zones
  dns01-recursive-nameservers: "10.2.0.10:53"
  dns01-recursive-nameservers-only: "true"
```

Apply this configuration:

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: cert-manager
  namespace: cert-manager
data:
  dns01-recursive-nameservers: "10.2.0.10:53"
  dns01-recursive-nameservers-only: "true"
EOF

# Restart cert-manager to pick up the changes
kubectl rollout restart deployment/cert-manager -n cert-manager
```

### 2. **DNS Zone Structure Recommendations**

Based on your [Azure DNS Private Resolver setup](https://portal.azure.com/#home) and [Hybrid Cloud DNS Resolution Flow](file:///Users/leon.ormes/path/to/file.extension), here's the recommended structure:

**Public Zones (Cloudflare):**

- `fitfile.net` - Main public domain
- `*.fitfile.net` - Public subdomains (e.g., `cuh-prod-1.fitfile.net`)

**Private Zones (Azure Private DNS):**

- `privatelink.fitfile.net` - Azure Private Link endpoints
- `internal.fitfile.net` - Internal services (consider creating this)

### 3. **Domain Usage Guidelines**

For your Kubernetes services:

| Service Type       | Recommended Domain          | DNS Provider      | Certificate Method      |
| ------------------ | --------------------------- | ----------------- | ----------------------- |
| Public APIs        | `api.fitfile.net`           | Cloudflare        | DNS-01 via cert-manager |
| Customer Endpoints | `cuh-prod-1.fitfile.net`    | Cloudflare        | DNS-01 via cert-manager |
| Private Services   | `*.internal.fitfile.net`    | Azure Private DNS | HTTP-01 or self-signed  |
| Azure Private Link | `*.privatelink.fitfile.net` | Azure Private DNS | Self-signed only        |

### 4. **Immediate Actions**

1. **For `cuh-prod-1.fitfile.net`** (currently failing due to DNS timeout):
   - Apply the ConfigMap above to use internal DNS
   - This should resolve the timeout issue since `10.2.0.10` can reach Cloudflare

2. **For `cuh-poc-1.privatelink.fitfile.net`** (NXDOMAIN issue):
   - Either switch to a different domain like `cuh-poc-1.internal.fitfile.net`
   - Or use HTTP-01 challenge if the service is publicly accessible
   - Or use self-signed certificates for this internal domain

### 5. **Long-term DNS Architecture**

Based on your [Hybrid Cloud DNS Resolution Flow](file:///Users/leon.ormes/path/to/file.extension) and [Azure DNS Private Resolver](file:///Users/leon.ormes/path/to/file.extension) setup:

```sh
┌─────────────────┐
│   Cloudflare    │ ← Public DNS (fitfile.net)
└────────┬────────┘
         │
┌────────▼────────┐
│ Azure DNS Resolver│ ← Inbound endpoint (10.250.16.52)
│  (Conditional   │
│   Forwarder)    │
└────────┬────────┘
         │
┌────────▼────────┐
│ On-Premises DNS │ ← Internal resolver (10.2.0.10)
│  (Forwarder)    │
└─────────────────┘
```

This architecture ensures:

- Public domains are resolved via Cloudflare
- Private zones stay within Azure/on-premises
- cert-manager can validate challenges through your internal DNS

The key alignment needed is configuring cert-manager to use your internal DNS resolver (`10.2.0.10`) which has access to both public and private DNS zones, rather than trying to reach external DNS servers directly through the proxy.

Based on the DNS record you've provided and the context from our previous conversation, I can see that you've successfully created the ACME challenge TXT record for `cuh-poc-1`:

```sh
_acme-challenge.cuh-poc-1
TXT
3600
jXEcL0OrSBdzt9y2zCgSg7S6ai4w56HmFBnYSaMZJ7A
```

However, this doesn't match the domain that cert-manager is trying to validate. Looking at your previous errors:

## Issue Analysis

1. **Domain Mismatch**:
   - Cert-manager is looking for: `_acme-challenge.cuh-poc-1.privatelink.fitfile.net`
   - You've created: `_acme-challenge.cuh-poc-1` (without the full domain suffix)

2. **Missing Domain Suffix**: The TXT record needs to be created with the full domain path that cert-manager expects.

## Solution

You need to create the TXT record with the correct full domain name. Based on whether you're managing DNS through Cloudflare or another provider, you should create:

### Option 1: If Using Cloudflare (for Non-privatelink domains)

```sh
Name: _acme-challenge.cuh-poc-1.fitfile.net
Type: TXT
Value: jXEcL0OrSBdzt9y2zCgSg7S6ai4w56HmFBnYSaMZJ7A
TTL: 3600
```

### Option 2: If You Must Use privatelink.fitfile.net

As I mentioned in our previous conversation, `privatelink.fitfile.net` is managed by Azure Private DNS and cannot be modified by external DNS providers. You'll need to either:

1. **Switch to HTTP-01 challenge** (recommended)
2. **Use a different domain** that you control
3. **Create the record in Azure Private DNS** (if you have access)

## Immediate Action

Since you already have the ACME challenge value (`jXEcL0OrSBdzt9y2zCgSg7S6ai4w56HmFBnYSaMZJ7A`), you need to:

1. Delete the incomplete record `_acme-challenge.cuh-poc-1`
2. Create the correct record with the full domain path
3. Ensure cert-manager can reach the DNS servers to validate it (addressing the timeout issue from your previous error)

## Verify DNS Propagation

Once you've created the correct record, verify it's propagating:

```bash
# From within your cluster
kubectl exec -n cert-manager deployment/cert-manager -- nslookup -type=TXT _acme-challenge.cuh-poc-1.fitfile.net

# Or from your jumpbox
dig TXT _acme-challenge.cuh-poc-1.fitfile.net @10.2.0.10
```

The TXT record value looks correct for an ACME challenge, but it needs to be placed at the correct domain location for cert-manager to find and validate it.
