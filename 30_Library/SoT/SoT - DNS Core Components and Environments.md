---
aliases: [CoreDNS Configuration, DNS Architecture, Hybrid Cloud DNS, Protective DNS, Split-View DNS]
created: 2026-01-06T20:15:48+00:00
last_reviewed: '2026-03-28'
modified: 2026-07-13T08:52:45+00:00
permalink: llmeon/30-library/so-t/so-t-dns-core-components-and-environments
status: Active
tags: [aws, azure, dns, networking, security, SoftwareEngineering/Architecture]
title: SoT - DNS Core Components and Environments
type: sot
updated: null
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

> Architectural Pattern: This deployment utilizes a Split-View DNS architecture. Domain names resolve to different IP addresses depending on the origin of the query (Internal vs. External). This is achieved via reciprocal conditional forwarding between Cloud CoreDNS and On-Premise DNS servers.

## 1. Core Components

### A. SDE Hub (AWS EKS)

- Internal: CoreDNS (K8s) forwards private queries to AWS Route 53 Private Zones.
- Hybrid: Conditional forwarders resolve CUH on-premise names via CUH DNS IPs.
- External: AWS Route 53 Public Zones manage `*.eoe.fitfile.net`.

### B. CUH Spoke (Azure VNet / On-Premise)

- Azure CoreDNS: Authoritative for `*.cuh.local`; forwards `*.fitfile.internal` to On-Premise DNS.
- On-Premise DNS: Authoritative for `*.fitfile.internal`; forwards `*.cuh.local` back to Azure CoreDNS.

---

## 2. Protective DNS & Encryption (NIST 2026 Standards)

Following NIST SP 800-81r3, DNS is now treated as an active security enforcement point.

### 2.1 Encryption Protocols

To prevent eavesdropping and hijacking, internal and external flows should utilize:

- DoT (DNS over TLS): Port 853.
- DoH (DNS over HTTPS): Port 443.
- DoQ (DNS over QUIC): UDP Port 853.

### 2.2 Security Enforcement (RPZ)

Response Policy Zones (RPZ) act as a "DNS Firewall."

- Mechanism: Blocks connections to known malicious domains and filters traffic by category.
- Local Overrides: Always maintain a local RPZ to whitelist internal namespaces, preventing erroneous blocking of core service discovery.
- Logging: Integrate protective DNS logs with SIEM to correlate IP addresses with DHCP lease history for incident response.

---

## 3. Domain Strategy

| Domain | Scope | Management | Purpose |
|:--- |:--- |:--- |:--- |
| `*.eoe.fitfile.net` | Public | Cloudflare | External access; ACME DNS-01 challenges. |
| `*.fitfile.internal` | Private | CUH On-Premise | M2M communication; bypasses Azure validation. |
| `*.cuh.local` | Hybrid | Split Authority | Internal resolution for CUH-specific services. |

---

## 4. Security Constraints

1. Firewall: Port 53 (UDP/TCP) must be open between Hub and Spoke.
2. Encrypted DNS Bypass: Block unauthorized DoT traffic on Port 853 to prevent clients from bypassing local security resolvers.
3. Cert-Manager Validation: Azure's internal resolver prioritizes Private Zones. Force `cert-manager` to use public resolvers (`1.1.1.1`) for DNS-01 by setting `dns01-recursive-nameservers-only=true`.

---

## 5. Diagnostic & Identification Protocols

### 5.1 Identifying Split-Horizon

To confirm if a domain is answering from an internal (private) zone versus the public internet:

| Diagnostic Tool | Command / Indicator | Meaning |
|:--- |:--- |:--- |
| dig +trace | `dig +trace <domain>` | Performs iterative resolution from the root down, bypassing the local stub. If it shows a different IP than a normal `dig`, you have split-horizon. |
| TTL 0 | `dig <domain>` $\to$ `0 IN A` | Azure Private DNS zones always return TTL 0. Public records (e.g., Cloudflare) typically have TTL 60-300+. |
| aa flag | `flags: qr aa rd ra ad` | The `aa` (authoritative answer) flag means the resolver (e.g., Azure's `168.63.129.16`) is claiming direct authority for the zone. |

### 5.2 Discovering Upstream Resolvers

On Linux systems using `systemd-resolved`, `cat /etc/resolv.conf` usually only shows `127.0.0.53`. To find the "real" upstream resolver:

```bash
resolvectl status
```

Look for "Current DNS Server" on the primary interface.

---

## Related Documentation

- [[SoT - Cloud Networking Principles]]
