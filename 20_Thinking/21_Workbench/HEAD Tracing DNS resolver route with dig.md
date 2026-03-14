---
captured: "2026-03-07T16:54:09+00:00 2026-03-07T16:54:09+00:00"
created: 2026-03-07T16:54:10+00:00
modified: 2026-03-14T11:10:34+00:00
source: "https://claude.ai/chat/3444a31e-833f-48cf-b46f-9ccae66d767f"
status: "processing"
tags: ["input"]
title: HEAD Tracing DNS resolver route with dig
type: "head"
---

## Raw Output / Content

i am using dig on a jumpbox in private network I want to find out the dns resolver route taken and which server answers

---

Here's exactly what you need:

### 1\. Find Which Resolver You're Actually Hitting

`+trace` is the key flag—it makes `dig` perform iterative resolution from the root servers down, showing you every delegation step: root → TLD → authoritative. This reveals the full chain.

### 2\. See Which upstream Server Your Local Resolver forwards to

This tells you the configured nameserver(s) the jumpbox uses. In AWS this is typically the VPC resolver at `x.x.x.2` (e.g., `10.0.0.2`); in Azure it's usually `168.63.129.16`.

### 3\. Query a Specific Server Explicitly

The `SERVER:` line in the response confirms who actually answered. Swap in whichever IP you got from `resolv.conf`.

### 4\. Full Diagnostic in One Shot

`+all` prints all sections (answer, authority, additional) at each delegation step, so you can see the NS records and glue at every level.

### Quick Interpretation Guide

- `+trace` stops early or fails at a step?—That delegation is broken (common with private DNS zones or split-horizon setups).
- `SERVER:` line shows `127.0.0.53`?—You're hitting `systemd-resolved` locally; the real upstream is in `resolvectl status` instead of `resolv.conf`.
- Different answer from `+trace` vs normal query?—Your resolver has a cached/overridden answer (e.g., a private hosted zone in Route 53 or Azure Private DNS).

Immediate action: Run `dig +trace <your-target-hostname>` on the jumpbox right now and see where the chain goes.

---

cat /etc/resolv.conf # This is /run/systemd/resolve/stub-resolv.conf managed by man:systemd-resolved(8). # Do not edit. # # This file might be symlinked as /etc/resolv.conf. If you're looking at # /etc/resolv.conf and seeing this text, you have followed the symlink. # # This is a dynamic resolv.conf file for connecting local clients to the # internal DNS stub resolver of systemd-resolved. This file lists all # configured search domains. # # Run "resolvectl status" to see details about the uplink DNS servers # currently in use. # # Third party programs should typically not access this file directly, but only # through the symlink at /etc/resolv.conf. To manage man:resolv.conf(5) in a # different way, replace this symlink by a static file or a different symlink. # # See man:systemd-resolved.service(8) for details about the supported modes of # operation for /etc/resolv.conf. nameserver 127.0.0.53 options edns0 trust-ad search mqmpnomypeweblilpgky3mmijc.zx.internal.cloudapp.net

---

### Here's Your Full Resolution Chain

| Step | Server | What happened |
| --- | --- | --- |
| 1\. Local stub | `127.0.0.53` (systemd-resolved) | Your jumpbox's local resolver fetched the root NS list |
| 2\. Root | `192.33.4.12` (c.root-servers.net) | Delegated to `.net` gTLD servers |
| 3\. gTLD | `192.48.79.30` (j.gtld-servers.net) | Delegated to Cloudflare: `aragorn.ns.cloudflare.com` + `carioca.ns.cloudflare.com` |
| 4\. Authoritative | `108.162.193.67` (aragorn.ns.cloudflare.com) | Answered with `nnuh-prod-1.fitfile.net → 195.171.151.154` (TTL 300s) |

### Key Observations

1\. You're going out to the public internet for this record. The `+trace` bypasses your local resolver and queries iteratively, but the first hop (`SERVER: 127.0.0.53`) confirms your jumpbox uses `systemd-resolved` as its stub. The search domain `mqmpnomypeweblilpgky3mmijc.zx.internal.cloudapp.net` confirms this is an Azure VM—the VPC DNS resolver behind `127.0.0.53` is Azure's wireserver at `168.63.129.16`.

2\. IPv6 is broken on this jumpbox. Notice these lines:

`dig +trace` tried an IPv6 root server first (j.root-servers.net AAAA), failed three times, then fell back to IPv4 (`c.root-servers.net` on `192.33.4.12`). Not a problem per se, but it adds latency. If you never need IPv6, you can skip those attempts with `dig -4 +trace`.

3\. `fitfile.net` is hosted on Cloudflare DNS. The authoritative answer came back with the `aa` (authoritative answer) flag set, TTL of 300s, resolving to `195.171.151.154`.

### To See the Real upstream Resolver Path (not the Trace path)

Since `+trace` does its own iterative resolution, it doesn't show you what `systemd-resolved` normally does. To see that:

This will show you which upstream DNS server(s) `systemd-resolved` is actually forwarding to (likely `168.63.129.16`—Azure's internal resolver), and whether any per-link DNS or search domains are configured.

Immediate action: Run `resolvectl status` to confirm the upstream forwarder, then compare with:

Check the `SERVER:` line in that output—it should say `127.0.0.53`, and the answer should match `195.171.151.154`. If it doesn't, you've got a split-horizon or private DNS zone overriding the public record.

---

resolvectl status Global Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported resolv.conf mode: stub Link 2 (eth0) Current Scopes: DNS Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported Current DNS Server: 168.63.129.16 DNS Servers: 168.63.129.16 DNS Domain: mqmpnomypeweblilpgky3mmijc.zx.internal.cloudapp.net dig nnuh-prod-1.fitfile.net; <<>> DiG 9.18.39-0ubuntu0.24.04.2-Ubuntu <<>> nnuh-prod-1.fitfile.net;; global options: +cmd;; Got answer:;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 33245;; flags: qr aa rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1;; OPT PSEUDOSECTION:; EDNS: version: 0, flags:; udp: 65494;; QUESTION SECTION:;nnuh-prod-1.fitfile.net. IN A;; ANSWER SECTION: nnuh-prod-1.fitfile.net. 0 IN A 192.168.200.40;; Query time: 0 msec;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP);; WHEN: Wed Feb 25 13:59:08 UTC 2026;; MSG SIZE rcvd: 68

---

### You've Got Split-horizon DNS—and This is the Important Bit

| Resolution path | Answer | IP |
| --- | --- | --- |
| `+trace` (iterative, bypasses local resolver) | Public Cloudflare authoritative | `195.171.151.154` |
| Normal query via `systemd-resolved` → `168.63.129.16` | Azure Private DNS zone | `192.168.200.40` |

Two dead giveaways in the normal dig output:

1. `TTL 0`—Azure Private DNS zones always return TTL 0. Cloudflare returned TTL 300. That's how you can instantly spot a private zone override.
2. `flags: qr aa rd ra ad`—the `aa` (authoritative answer) flag is set, meaning Azure's resolver at `168.63.129.16` is claiming to be authoritative for `fitfile.net`. It's not forwarding to Cloudflare—it's answering directly from an Azure Private DNS Zone linked to this VNet.

### The Full Picture

So `192.168.200.40` is the private/internal address for `nnuh-prod-1`—likely a VM or load balancer NIC within an Azure VNet peered to yours.

### If You Need to Verify the Private DNS Zone

Then:

That'll show you all the A records in the private zone and confirm what's overriding the public record.

---

az network private-dns zone list --output table ZoneName ResourceGroup RecordSets MaxRecordSets VirtualNetworkLinks MaxVirtualNetworkLinks VirtualNetworkLinksWithRegistration MaxVirtualNetworkLinksWithRegistration ProvisioningState ------------------------------------------------------------------ ---------------- ------------ --------------- --------------------- ------------------------ ------------------------------------- ---------------------------------------- ------------------- 725e1bce-a49c-4025-b2d7-4bd997c04024.privatelink.uksouth.azmk8s.io rg-ff-uks-gp-aks 2 25000 1 1000 0 100 Succeeded ➜ ~ az network private-dns record-set a list --zone-name fitfile.net --resource-group <rg-name> --output table zsh: no such file or directory: rg-name ➜ ~ az network private-dns record-set a list --zone-name fitfile.net --resource-group rg-ff-uks-gp-aks --output table (ParentResourceNotFound) Failed to perform 'read' on resource(s) of type 'privateDnsZones/A', because the parent resource '/subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/rg-ff-uks-gp-aks/providers/Microsoft.Network/privateDnsZones/fitfile.net' could not be found. Code: ParentResourceNotFound Message: Failed to perform 'read' on resource(s) of type 'privateDnsZones/A', because the parent resource '/subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/rg-ff-uks-gp-aks/providers/Microsoft.Network/privateDnsZones/fitfile.net' could not be found.

---

### The Zone Exists, but not in that Resource Group

The only private DNS zone in `rg-ff-uks-gp-aks` is the AKS API server zone (`*.privatelink.uksouth.azmk8s.io`). There's no `fitfile.net` zone there—but something is still answering `192.168.200.40` authoritatively. So it's elsewhere.

### Find it—search across All Resource Groups

This lists every private DNS zone across all resource groups in the current subscription.

If that comes back empty for `fitfile.net`, it might be in a different subscription:

Then iterate:

### Alternative: it Could Be a DNS Private Resolver

If there's no Private DNS Zone at all for `fitfile.net`, the other mechanism that produces the same behaviour (TTL 0, `aa` flag) is an Azure DNS Private Resolver with a forwarding ruleset pointing `fitfile.net` to a custom DNS server (e.g., a CoreDNS or BIND instance in the VNet).

Check for that:

Immediate action: Run the first command—`az network private-dns zone list --query "[].{Zone:name, RG:resourceGroup}" --output table`—and see if `fitfile.net` shows up in another resource group.

---

az network private-dns zone list --query "\[\].{Zone:name, RG:resourceGroup}" --output table Zone RG ------------------------------------------------------------------ ---------------- 725e1bce-a49c-4025-b2d7-4bd997c04024.privatelink.uksouth.azmk8s.io rg-ff-uks-gp-aks

---

### Only One Private Zone in This subscription—and It's not fitfile.net

So something else is answering. Let's narrow it down.

### 1\. Check if There's a DNS Private Resolver

### 2\. Check if the VNet Itself Has Custom DNS Servers Configured

This is a common one—the VNet might not be using Azure default DNS at all, but forwarding through a custom server that handles `fitfile.net`:

If `dnsServers` shows anything other than empty/ `[]`, that's your culprit—a custom DNS server is intercepting before `168.63.129.16`.

### 3\. Check other Subscriptions

The private zone could be in a different subscription but linked to your VNet (cross-subscription links are supported):

Then for each non-current subscription:

Immediate action: Start with the VNet DNS check—`az network vnet list --query "[].{Name:name, RG:resourceGroup, DNS:dhcpOptions.dnsServers}" --output table`—that's the most likely explanation if there's no private zone and no private resolver.

---

we set up the split horizon so we could use acme certificates with certmanager in the private network. Is this correct? Explain how it works with the dns0 challenge

---

### Yes, This is Exactly the Right Pattern. Here's why

### The Problem Split-horizon Solves

You have services on a private network (`192.168.200.40`) that need valid TLS certificates. The standard HTTP-01 ACME challenge requires Let's Encrypt to make an inbound HTTP request to your server—which is impossible when the server isn't publicly reachable. Dead end.

### Why DNS-01 is the Answer

DNS-01 doesn't require any inbound connectivity to your server at all. The validation happens entirely in the public DNS layer, which is always reachable. Here's the flow:

### Where Split-horizon Fits in

This is the elegant part. You have two parallel truths about `fitfile.net`:

| Layer | Zone | Purpose |
| --- | --- | --- |
| Public (Cloudflare) | `fitfile.net` → `195.171.151.154` | Serves `_acme-challenge` TXT records for Let's Encrypt validation. The A record here is irrelevant to the private setup. |
| Private (Azure DNS / custom) | `fitfile.net` → `192.168.200.40` | Routes traffic within the VNet to the actual private workload |

Let's Encrypt only ever sees the public Cloudflare zone. Your pods, other services, and anything inside the VNet only ever see the private zone. They never conflict because they're queried by different actors from different networks.

### Why This is the Correct Approach

- HTTP-01 is impossible—Let's Encrypt can't reach `192.168.200.40`
- DNS-01 doesn't care where the server is—it only validates domain ownership via a TXT record in public DNS
- The cert is valid everywhere—once issued, the certificate for `nnuh-prod-1.fitfile.net` is trusted by any client, whether they resolve to the public or private IP
- No firewall holes needed—zero inbound connectivity required from the internet to your private network

### The Cert-manager Side (in Your AKS cluster)

Your setup almost certainly looks something like this:

The only outbound requirement is that cert-manager can reach the Cloudflare API and the Let's Encrypt API—both over HTTPS, both outbound-only.

Key principle: DNS-01 decouples "proving domain ownership" from "where the service actually runs." Split-horizon then lets you point the same hostname to a private IP internally while keeping the public zone available for ACME validation. It's the standard pattern for TLS on private infrastructure.

---

what commands can i run from the jumpbox to validate the certificate is set up correctly

---

### Layer 1: Check Cert-manager Resources in the Cluster

If it's not `Ready`, dig into the request chain:

A stuck `Challenge` in state `pending` usually means cert-manager can't create the TXT record in Cloudflare (token issue, wrong zone ID, etc.).

### Layer 2: Check the Actual TLS Cert Being Served

What you're looking for:

- Issuer contains `Let's Encrypt` (not `Kubernetes Ingress Controller Fake Certificate` or self-signed)
- Subject Alternative Name includes `nnuh-prod-1.fitfile.net`
- Not After is in the future (cert-manager renews at 2/3 of lifetime, so ~60 days before expiry for Let's Encrypt's 90-day certs)

Quick expiry check:

### Layer 3: Validate the Full Chain

You want to see at least two certificates in the chain. A single cert with no intermediate means clients may reject it.

### Layer 4: Verify the Kubernetes Secret Exists and Has Data

You should see `tls.crt` and `tls.key`. To inspect the cert from the secret directly:

### Layer 5: Confirm DNS-01 is Actually Working (public side)

- Empty = good (cert-manager cleaned up after successful validation)
- Has a token = either a renewal is in progress, or a challenge is stuck

### One-liner Health Check

This gives you subject, issuer, validity dates, and SANs in one shot.

Immediate action: Run that one-liner first—if issuer says `Let's Encrypt` and the dates are valid, you're golden. If not, work backwards through the layers.

---

kubectl describe certificate fitfile-nnuh -n nnuh-prod-1 Name: fitfile-nnuh Namespace: nnuh-prod-1 Labels: <none> Annotations: argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true argocd.argoproj.io/tracking-id: certificates:cert-manager.io/Certificate:nnuh-prod-1/fitfile-nnuh API Version: cert-manager.io/v1 Kind: Certificate Metadata: Creation Timestamp: 2025-11-28T15:46:39Z Generation: 1 Resource Version: 35083513 UID: 841e4018-4db8-4cc3-80a1-5145d2926d03 Spec: Dns Names: nnuh-prod-1.fitfile.net Duration: 8760h Issuer Ref: Kind: ClusterIssuer Name: letsencrypt-prod Private Key: Algorithm: RSA Encoding: PKCS1 Size: 2048 Renew Before: 720h Secret Name: fitfile-nnuh-tls Status: Conditions: Last Transition Time: 2025-11-28T15:58:26Z Message: Certificate is up to date and has not expired Observed Generation: 1 Reason: Ready Status: True Type: Ready Not After: 2026-04-27T14:02:51Z Not Before: 2026-01-27T14:02:52Z Renewal Time: 2026-03-28T14:02:51Z Revision: 2 Events: <none>

---

### Everything is Green ✅

Here's the full picture:

| Check | Result | Status |
| --- | --- | --- |
| Issuer | Let's Encrypt R12 | ✅ Real cert, not a fake/self-signed |
| SAN | `DNS:nnuh-prod-1.fitfile.net` | ✅ Matches hostname |
| Chain | Leaf → R12 → ISRG Root X1 (2 certs) | ✅ Full chain present |
| TLS version | TLSv1.3, `TLS_AES_256_GCM_SHA384` | ✅ Strong cipher |
| Verification | `Verify return code: 0 (ok)` | ✅ Trusted |
| ACME challenge TXT | Empty | ✅ Cleaned up after issuance |
| cert-manager status | `Ready: True` | ✅ |
| Expiry | 27 April 2026 (~61 days out) | ✅ Plenty of time |
| Auto-renewal | Scheduled for 28 March 2026 (`renewBefore: 720h` = 30 days) | ✅ |

### Your Cert-manager Config Decoded

- Duration:`8760h` (365 days)—you're requesting a 1-year cert, but Let's Encrypt always issues 90-day certs regardless. This is fine; cert-manager handles it.
- Renew Before:`720h` (30 days)—cert-manager will trigger renewal 30 days before expiry.
- Revision 2—it's already renewed once since initial creation on 28 Nov 2025. The current cert was issued 27 Jan 2026, which is exactly 61 days after initial setup—confirming the auto-renewal pipeline is working.

The whole split-horizon + DNS-01 + cert-manager pipeline is working exactly as intended. Nothing to fix here.

---

can i check it from a remote cluster? I can log into the cluster that needs to send requests and check the public route and cert

---

Yes—from a pod in the remote cluster, you can validate both the DNS resolution path and the TLS cert it sees.

### 1\. Spin up a Debug Pod

### 2\. Check what the Remote Cluster Resolves

This tells you whether the remote cluster hits the public IP (`195.171.151.154` via Cloudflare) or a private IP (`192.168.200.40` via a private zone / VNet peering). The `SERVER:` line shows you which resolver answered.

### 3\. Validate the Cert from the Remote Cluster's Perspective

Using the hostname (not the IP) here is important—it follows whatever DNS resolution path the remote cluster uses, which is exactly what your application will do.

### 4\. Full Connectivity + TLS Check in One Shot

This shows you:

- Which IP it connected to (public or private)
- TLS handshake details
- Whether the cert is trusted (curl will error if not)
- HTTP response code (confirms the service is actually responding)

### 5\. If the Remote Cluster Goes via the Public IP

You might see a different cert or a different service entirely at `195.171.151.154`, since that's the Cloudflare public record. If the remote cluster needs to reach the private service, you'll need either VNet peering with a shared private DNS zone, or a connectivity path (VPN, ExpressRoute, etc.) to the `192.168.200.40` network.

Immediate action:`kubectl run debug --image=nicolaka/netshoot -it --rm -- bash`, then run the `dig` to see which IP the remote cluster resolves to. That determines everything else.

---

dig nnuh-prod-1.fitfile.net; <<>> DiG 9.20.17 <<>> nnuh-prod-1.fitfile.net;; global options: +cmd;; Got answer:;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 49115;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1;; OPT PSEUDOSECTION:; EDNS: version: 0, flags:; udp: 1232; COOKIE: a8ff565a5e3f42d0 (echoed);; QUESTION SECTION:;nnuh-prod-1.fitfile.net. IN A;; ANSWER SECTION: nnuh-prod-1.fitfile.net. 30 IN A 195.171.151.154;; Query time: 10 msec;; SERVER: 172.20.0.10#53(172.20.0.10) (UDP);; WHEN: Wed Feb 25 14:25:23 UTC 2026;; MSG SIZE rcvd: 103 tmp-shel:~# dig nnuh-prod-1.fitfile.net^C tmp-shel:~# openssl s\_client -connect nnuh-prod-1.fitfile.net:443 -servername nnuh-prod-1.fitfile.net </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates -ext subjectAltName subject=CN=nnuh-prod-1.fitfile.net issuer=C=US, O=Let's Encrypt, CN=R12 notBefore=Jan 27 14:02:52 2026 GMT notAfter=Apr 27 14:02:51 2026 GMT X509v3 Subject Alternative Name: DNS:nnuh-prod-1.fitfile.net tmp-shel:~# curl -vI [https://nnuh-prod-1.fitfile.net](https://nnuh-prod-1.fitfile.net/) 2>&1 | grep -E "Connected to|SSL connection|subject:|issuer:|expire|HTTP/" \* SSL connection using TLSv1.3 / TLS\_AES\_256\_GCM\_SHA384 / x25519 / RSASSA-PSS \* subject: CN=nnuh-prod-1.fitfile.net \* expire date: Apr 27 14:02:51 2026 GMT \* issuer: C=US; O=Let's Encrypt; CN=R12 \* using HTTP/2 \* \[HTTP/2\] \[1\] OPENED stream for [https://nnuh-prod-1.fitfile.net/](https://nnuh-prod-1.fitfile.net/) \* \[HTTP/2\] \[1\] \[:method: HEAD\] \* \[HTTP/2\] \[1\] \[:scheme: https\] \* \[HTTP/2\] \[1\] \[:authority: nnuh-prod-1.fitfile.net\] \* \[HTTP/2\] \[1\] \[:path: /\] \* \[HTTP/2\] \[1\] \[user-agent: curl/8.18.0\] \* \[HTTP/2\] \[1\] \[accept: \*/\*\] > HEAD / HTTP/2 < HTTP/2 302 HTTP/2 302

---

### Remote cluster—all Good ✅

### So the Full Traffic Flow from the Remote Cluster is

The remote cluster has no split-horizon—it goes straight out to the public internet, hits the public IP, and gets a valid trusted cert. That's exactly what you'd expect.

Both paths are working:

- Internal (jumpbox / private VNet): `192.168.200.40` via Azure Private DNS → valid cert
- External (remote cluster): `195.171.151.154` via Cloudflare → same valid cert

The `195.171.151.154` public endpoint is presumably fronted by something (Cloudflare proxy, Azure Front Door, or an NVA) that routes traffic back to the private service. The cert is the same on both paths because it's the same Let's Encrypt cert served by the same ingress—just reached via different network routes.

---

write a single wiki page with all the results from these test

---

A markdown file is the right format for a wiki page. Let me put this together.
