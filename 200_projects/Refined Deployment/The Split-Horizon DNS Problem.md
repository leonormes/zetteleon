---
aliases: []
confidence: 
created: 2025-09-27T12:01:04Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: The Split-Horizon DNS Problem
type:
uid: 
updated: 
version:
---

[[2025-09-27]]

Short version: your cert for cuh-poc-1.fitfile.net works because cert-manager’s DNS self-check in AKS is resolving against Azure’s built-in resolver (168.63.129.16), which can see public Cloudflare DNS. The one for cuh-poc-1.privatelink.fitfile.net fails because your VNET is linked to an Azure Private DNS zone named privatelink.fitfile.net. During cert-manager’s self-check it asks “does the TXT record exist yet?” and the query is answered by the private zone (which doesn’t contain the TXT you created via Cloudflare), so the self-check never passes and the order is abandoned—even though Let’s Encrypt would be able to see the TXT in Cloudflare just fine.

Why port 53 egress “block” didn’t stop the working one

AKS nodes query Azure’s link-local resolver 168.63.129.16 (via CoreDNS). That isn’t “egress to the Internet on :53”, so your firewall rule doesn’t apply. For .fitfile.net (no private zone), that resolver goes out and finds the TXT in Cloudflare → self-check passes. For .privatelink.fitfile.net, the same resolver prefers the private zone you attached → no TXT → self-check fails.

Fix options (pick one)

Force cert-manager to use public recursive resolvers for its self-check

Tell cert-manager to ignore your VNET/Private DNS and recurse via public DNS (Cloudflare/Google). You do this with controller flags:

## Values for the Cert-manager Helm Chart

extraArgs:

- --dns01-recursive-nameservers=1.1.1.1:53,8.8.8.8:53
- --dns01-recursive-nameservers-only=true
  :warning: Your firewall must allow the cert-manager controller pod (namespace scoped) to reach those IPs on UDP/TCP 53. This is the documented way to fix split-horizon issues

I know this is what you tried, and the reason it didn't work is because outbound traffic on port 53 is blocked from our VNET.

The security implications of allowing outbound traffic on port 53 is a potential data leak - i.e. we could send data out to a public DNS via TXT records

However, I don't think this is a concern since the whole point of FITFILE is that we send data to SDE.

So we could get TT to open up that port, and set dns01-recursive-nameservers and then the split horizon DNS will work, because cert-manager will ignore the private DNS zone we set up.

The other option I thought of is we could remove the private DNS zone all together. The only reason its there is so that CUH can access it - but if they just set up a DNS zone on premise to point to the private IP of nginx controller in our VNET, then the Azure link-local resolver 168.63.129.16 would just allow the outbound DNS traffic for the DNS01 challenge.

Ollie Rushton's message accurately diagnoses a critical DNS resolution issue impacting `cert-manager`'s ability to issue TLS certificates, particularly for domains utilizing Azure Private DNS zones. The core of the problem is "split-horizon DNS," where a domain name resolves differently depending on whether the query originates from within the private network or from the public internet.

### Ollie's Analysis Explained: The Split-Horizon DNS Problem

1. **The Problem:** `cert-manager` performs a DNS self-check (specifically, a DNS01 challenge) to verify domain ownership for certificate issuance. This involves creating a TXT record in the domain's DNS zone.
   - **`cuh-poc-1.fitfile.net` (Works):** For this domain, Azure's internal DNS resolver (`168.63.129.16`), queried by AKS's CoreDNS, can successfully reach public DNS providers like Cloudflare. It finds the TXT record created for the challenge, and the self-check passes, allowing the certificate to be issued.
   - **`cuh-poc-1.privatelink.fitfile.net` (Fails):** For this domain, the Azure VNET is linked to an Azure Private DNS zone named `privatelink.fitfile.net`. When `cert-manager` initiates its self-check, the Azure internal resolver (`168.63.129.16`) prioritizes resolution through this linked private zone. Since the TXT record was created in Cloudflare (public DNS) and not in the Azure Private DNS zone, the private zone reports the record as non-existent. Consequently, `cert-manager`'s self-check fails, and the certificate order is abandoned, even though Let's Encrypt could find the TXT record on public DNS.

2. **Why the Port 53 Egress "Block" Didn't Stop the Working One:** The firewall rule blocking outbound traffic on port 53 from the VNET did not prevent the certificate for `cuh-poc-1.fitfile.net` from being issued. This is because the DNS query from AKS nodes, via CoreDNS, was directed to Azure's internal resolver (`168.63.129.16`). This internal routing is not considered direct "egress to the Internet on :53" from the pod's perspective and thus bypassed the firewall rule. However, for the `*.privatelink.fitfile.net` domain, the internal resolution path, which prioritizes the private DNS zone, takes precedence and causes the failure, regardless of the egress block on direct internet connections.

### Ollie's Proposed Solutions

Ollie outlines two primary methods to resolve this split-horizon DNS issue:

1. **Force `cert-manager` to use public recursive resolvers:**
   - **Mechanism:** Configure `cert-manager` to bypass internal DNS resolution and query public DNS servers directly for its self-checks.
   - **Configuration:** This is achieved by adding specific flags to the `cert-manager` Helm chart's `values.yaml`:

     ```yaml
     extraArgs:
       - --dns01-recursive-nameservers=1.1.1.1:53,8.8.8.8:53
       - --dns01-recursive-nameservers-only=true
     ```

   - **Requirement:** The firewall must be configured to allow the `cert-manager` controller pods to reach these public IPs (e.g., `1.1.1.1`, `8.8.8.8`) on UDP/TCP port 53.
   - **Security Consideration:** Ollie acknowledges that opening port 53 egress might pose a potential data leak risk (sending data via TXT records). However, he deems this risk acceptable given FITFILE's purpose of sending data to SDE. This is considered the "documented way to fix split-horizon issues."

2. **Remove the Azure Private DNS zone and adjust on-premise DNS:**
   - **Mechanism:** Remove the Azure Private DNS zone (`privatelink.fitfile.net`) linked to the VNET. This eliminates the Azure resolver's prioritization of the private zone.
   - **Requirement:** CUH would need to set up an on-premise DNS zone to point to the private IP of the FITFILE Nginx controller within the VNET. Their on-premise DNS servers would then need to be configured with conditional forwarders for the `*.privatelink.fitfile.net` zone to point to the Azure DNS resolver or CoreDNS.
   - **Trade-offs:** This approach simplifies Azure infrastructure by removing the private zone but shifts DNS management responsibility to CUH and requires their cooperation in configuring conditional forwarding.

### Alignment with Your Work

Your implemented configuration directs `cert-manager` to use your internal CoreDNS server (`10.2.0.10`) as its recursive nameserver:

```yaml
extraArgs:
  - --dns01-recursive-nameservers=10.2.0.10:53
  - --dns01-recursive-nameservers-only=true
```

This approach attempts to control `cert-manager`'s DNS resolution. However, as Ollie's analysis and a deeper dive into the components reveal, this specific configuration does **not** fully resolve the issue for `*.privatelink.fitfile.net`.

**Why your current configuration fails for `privatelink.fitfile.net`:**

1. **CoreDNS Forwarding:** Your CoreDNS (`10.2.0.10`) forwards external queries to the Azure Link-Local Resolver (`168.63.129.16`).
2. **Azure Resolver Prioritization:** The Azure Link-Local Resolver (`168.63.129.16`) is configured to *prioritize* resolution using any Azure Private DNS zones linked to the VNET. In this case, it prioritizes `privatelink.fitfile.net`.
3. **Missing Record in Private Zone:** Since the TXT record for the DNS01 challenge was created in Cloudflare (public DNS) and not in the `privatelink.fitfile.net` Azure Private DNS Zone, the query to the private zone fails.
4. **Validation Failure:** This failure is propagated back, causing `cert-manager`'s self-check to fail.

**Therefore, your current configuration, while specifying an internal resolver, still routes the critical DNS01 challenge query through the Azure Link-Local Resolver, which then prioritizes the problematic private DNS zone.**

To achieve success for `*.privatelink.fitfile.net`, you need to implement one of Ollie's proposed solutions that *explicitly bypasses the Azure Private DNS Zone's prioritization* for the DNS01 challenge. This means either:

- **Configuring `cert-manager` to directly use public resolvers** (Ollie's first option), which requires opening port 53 egress.
- **Removing the Azure Private DNS zone** (Ollie's second option), which shifts DNS management to CUH.

While your internal DNS server approach is a valid strategy for controlling DNS resolution in general, it does not circumvent the specific prioritization behavior of the Azure Link-Local Resolver when a private DNS zone is linked.
