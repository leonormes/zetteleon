---
title: FTFL-511 — TLS Cipher Remediation & DNS Propagation
created: 2026-06-01T22:03:23+00:00
source: pieces-ltm
pieces_ids: [37e4252f-1b8e-45e5-a1e3-1908d114b3fd, ec9c756a-55c3-4760-9b16-f0da1bcf9f6c, 7e6890c9-d6bc-4390-891e-98961ae4f53f, 2e705a4f-892b-44ab-aaa4-195188d64534, 92b022c0-fd8a-4418-9442-8cca2cefe6f3, 480f2d8a-ccf4-4b1d-9d04-a75b69c29a7d, 9a572b4c-d9a1-4fb9-a5a2-51269582f7f1, be2e3a5e-3c95-46b1-a6dc-ce5b958490b7, e98472a6-f2be-477b-a36b-8d0ecf3ccde0, b023b25d-0208-4bd5-8bba-e5b2291ad098, 6ba298d9-2ca1-4ead-a773-dbf27b164efd, 001d11ea-4e94-4473-be02-3e8df852add8, 3314644d-e59b-4d73-a611-cd57e8ae2c49, 9ba83f8a-8a43-4419-bede-b79d9b8f82a2, 8e7b9778-4e55-4eac-b4bd-8e047982160f, 247ed4ba-d561-45e4-9dbb-a54b6f8ddc6f]
tags: [raw, pieces]
---
## Asset 1 (Pieces: 37e4252f-1b8e-45e5-a1e3-1908d114b3fd) — 2026-06-01T11:39

The user is asking about what "server-tokens" means in the context of nginx/ingress-nginx, and whether it's safe to disable them. This is a technical question about nginx configuration, not a memory retrieval question. I can answer this from technical knowledge directly.

Server tokens in nginx context refers to the `server_tokens` directive which controls whether nginx includes its version information and server name in response headers and error pages. This is a well-known security configuration option.

Let me answer this directly without needing to search memory, as it's a factual technical question.**Server tokens are nginx's self-identification in responses — you absolutely do not need them, and disabling them is the right call.**

### What `server-tokens` controls

In nginx, `server_tokens` controls two things:

1. **The `Server:` response header** — by default nginx sends `Server: nginx/1.27.x` (version number included). With `server-tokens: false` it sends nothing, or just `Server: nginx` if you want to keep the name without the version.

2. **Error page footers** — the `<hr><center>nginx</center>` you're seeing right now. That HTML fragment is nginx's built-in error/redirect body. `server-tokens off` removes it entirely.

### Is there anything useful in them?

No. Server tokens are purely informational for debugging. They tell an attacker:
- What software you're running ✗
- What version (making CVE lookups trivial) ✗

They provide zero functional value to clients or load balancers. Browsers and proxies don't consume them for anything meaningful.

### Is this standard practice?

Yes — disabling server tokens is explicitly recommended by:
- **Mozilla SSL Configuration Generator** (which you were using as your benchmark for FTFL-511)
- **CIS Kubernetes Benchmark**
- **OWASP** (information leakage prevention)
- The **ingress-nginx** maintainers themselves — `server-tokens: "false"` is a first-class documented config option

The pentest report (ProCheckUp) flagged FTFL-512 specifically because of this leakage. Disabling it is the direct remediation they recommended.

### Confirm: no side effects

Setting `server-tokens: false` on the ingress-nginx controller configmap:
- Does **not** affect routing, SSL, or any upstream behaviour
- Does **not** change how clients connect or how the LB operates
- Only removes the self-identification strings from nginx-generated responses

Safe to apply. Go ahead with the `kubectl patch` or `helm upgrade` from the previous message.

## Asset 2 (Pieces: ec9c756a-55c3-4760-9b16-f0da1bcf9f6c) — 2026-06-01T11:21

**Yes, fixed.** ✅

Resolves to `20.117.146.221` (nginx origin direct), only AEAD suites, no CBC, no RSA key exchange, `cipher preference: server`, least strength A. Identical clean result to the jumpbox scan.

One interesting difference worth noting — your TLS 1.3 key exchange shows `X25519MLKEM768` instead of the jumpbox's `ecdh_x25519`. That's because your local nmap 7.99 advertises the **post-quantum hybrid KEM** (X25519 + ML-KEM-768) during the handshake, and nginx accepts it. The jumpbox was running nmap 7.95 which doesn't offer it, so it fell back to plain `ecdh_x25519`. Either way it's a pass — the server is happy with both.

You now have two independent confirmation scans (jumpbox + local laptop, both resolving to `20.117.146.221`) with clean results. Close [FTFL-511](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?assignee=633ae2b9fedc6169aed8f601&selectedIssue=FTFL-511).

## Asset 3 (Pieces: 7e6890c9-d6bc-4390-891e-98961ae4f53f) — 2026-06-01T11:21

The user is asking if the FTFL-511 issue is fixed based on their local machine nmap scan. Let me analyze the results.

The scan from their local machine shows:
- Resolved to `20.117.146.221` (Azure LB / nginx origin, not Cloudflare)
- TLSv1.2: Only 3 AEAD suites with ECDHE (GCM + ChaCha20) - all A grade
- TLSv1.3: 3 suites - all A grade


- Server controls cipher preference with no CBC or RSA key exchange suites, all minimum strength A
- The key difference is TLS 1.3 showing `X25519MLKEM768` (post-quantum hybrid) on their newer nmap versus `ecdh_x25519` on the jumpbox's older version, which doesn't support advertising post-quantum key exchange

This is definitely fixed—the configuration is clean and secure.

## Asset 4 (Pieces: 2e705a4f-892b-44ab-aaa4-195188d64534) — 2026-06-01T11:20

from my local machine (laptop) I get nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net
zsh: correct 'nmap' to 'jmap' [nyae]? n
Starting Nmap 7.99 ( https://nmap.org ) at 2026-06-01 12:20 +0100
Nmap scan report for sandbox-testing-1.fitfile.net (20.117.146.221)
Host is up (0.015s latency).

PORT    STATE SERVICE
443/tcp open  https
| ssl-enum-ciphers:
|   TLSv1.2:
|     ciphers:
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A
|     compressors:
|       NULL
|     cipher preference: server
|   TLSv1.3:
|     ciphers:
|       TLS_AKE_WITH_AES_256_GCM_SHA384 (X25519MLKEM768) - A
|       TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 (X25519MLKEM768) - A
|       TLS_AKE_WITH_AES_128_GCM_SHA256 (X25519MLKEM768) - A
|     cipher preference: server
|_  least strength: A

Nmap done: 1 IP address (1 host up) scanned in 1.37 seconds

Is this fixed?

## Asset 5 (Pieces: 92b022c0-fd8a-4418-9442-8cca2cefe6f3) — 2026-06-01T08:53

## FTFL-511 — Remediation confirmed ✅

The scan resolved to `20.117.146.221` (your Azure LB / nginx origin) and the cipher list is exactly what it should be:

| Suite | Type | Grade |
|---|---|---|
| `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` | ECDHE + AEAD | A |
| `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384` | ECDHE + AEAD | A |
| `TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256` | ECDHE + AEAD | A |
| `TLS_AKE_WITH_AES_256_GCM_SHA384` | TLS 1.3 | A |
| `TLS_AKE_WITH_CHACHA20_POLY1305_SHA256` | TLS 1.3 | A |
| `TLS_AKE_WITH_AES_128_GCM_SHA256` | TLS 1.3 | A |

- Zero `TLS_RSA_*` suites (no RSA key exchange, no missing PFS) ✅
- Zero `*_CBC_*` suites (no padding oracle risk) ✅
- `cipher preference: server` — nginx is dictating cipher order now (better than the Friday `client` preference) ✅
- Least strength: **A** ✅

### Save the artefact and close the ticket

```bash
{
  echo "=== POST-FIX TLS CIPHERS - $(date) ==="
  nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net
} > ~/ftfl-511-post-fix-$(date +%Y%m%d).txt
```

Attach `ftfl-511-post-fix-20260601.txt` to [FTFL-511](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?assignee=633ae2b9fedc6169aed8f601&selectedIssue=FTFL-511) and mark it **Done**. The Jira comment you drafted on Friday already explains the root cause (misattributed to nginx, actually Cloudflare's edge) — this scan output is the closing evidence.

## Asset 6 (Pieces: 480f2d8a-ccf4-4b1d-9d04-a75b69c29a7d) — 2026-06-01T08:53

The user has run the nmap scan and the results are exactly what we expected. The scan now hits the origin IP (20.117.146.221) directly, and only shows modern AEAD suites - no CBC or RSA key exchange ciphers. This is a clean pass. Let me analyze the results:

TLSv1.2:
- TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 - A ✅
- TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 - A ✅


- TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 - A ✅

TLSv1.3 is showing the same strong cipher suite pattern with AES-GCM and ChaCha20-Poly1305 variants, all rated A. The absence of CBC ciphers and RSA key exchange mechanisms confirms we've successfully eliminated weak cryptography, and the server cipher preference setting means the server is controlling which cipher gets used rather than letting the client choose.

FTFL-511 is resolved now, so I should make sure the user captures this output and attaches it to the ticket.

## Asset 7 (Pieces: 9a572b4c-d9a1-4fb9-a5a2-51269582f7f1) — 2026-06-01T08:53

dig sandbox-testing-1.fitfile.net +short
20.117.146.22nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-01 08:53 UTC
Nmap scan report for sandbox-testing-1.fitfile.net (20.117.146.221)
Host is up (0.0086s latency).

PORT    STATE SERVICE
443/tcp open  https
| ssl-enum-ciphers: 
|   TLSv1.2: 
|     ciphers: 
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A
|     compressors: 
|       NULL
|     cipher preference: server
|   TLSv1.3: 
|     ciphers: 
|       TLS_AKE_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A
|       TLS_AKE_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|     cipher preference: server
|_  least strength: A

Nmap done: 1 IP address (1 host up) scanned in 0.40 seconds

## Asset 8 (Pieces: be2e3a5e-3c95-46b1-a6dc-ce5b958490b7) — 2026-06-01T08:53

DNS-only has propagated. `20.117.146.221` is your Azure Load Balancer IP — no Cloudflare in the path anymore.

Run the nmap scan now:

```bash
nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net
```

This time it will hit nginx directly. You should see **only** the 6 AEAD suites (GCM + ChaCha20) with no `TLS_RSA_*` or `*_CBC_*` entries. If that's what comes back, FTFL-511 is closed.

## Asset 9 (Pieces: e98472a6-f2be-477b-a36b-8d0ecf3ccde0) — 2026-06-01T08:53

The user has run the `dig` command and it's now returning `20.117.146.221` — their Azure origin IP, not a Cloudflare Anycast address. This means DNS-only has propagated. They should now rerun the nmap scan directly against the hostname.

## Asset 10 (Pieces: b023b25d-0208-4bd5-8bba-e5b2291ad098) — 2026-06-01T08:39

## The scan still hit Cloudflare — DNS-only hasn't taken effect yet

The resolved IP in the nmap output gives it away immediately:

```
sandbox-testing-1.fitfile.net (172.67.72.212)
Other addresses: 104.26.0.140  104.26.1.140  2606:4700:20::...
```

`172.67.72.212`, `104.26.0.140`, `104.26.1.140` are all **Cloudflare Anycast ranges** — the exact same IPs from Friday's original pentest scan. Your DNS-only change has not propagated to the resolver this jumpbox is using (or the change may not have saved correctly in the Cloudflare dashboard).

The cipher list confirms it — you're still seeing all 20 suites including the `TLS_RSA_*` and `ECDHE_*_CBC_*` ones that are Cloudflare's edge config.

### What to check now

**1. Verify the Cloudflare dashboard actually saved DNS-only**

Go to your Cloudflare DNS dashboard for `fitfile.net` and confirm the `sandbox-testing-1` A record shows a **grey cloud** (DNS only), not an orange cloud (Proxied). It's easy to accidentally not save the toggle.

**2. Check what DNS is actually returning right now from the jumpbox**

```bash
dig sandbox-testing-1.fitfile.net +short
```

- If you see `172.67.x.x` / `104.26.x.x` → still hitting Cloudflare, DNS hasn't propagated
- If you see `20.117.146.221` (your Azure LB IP) → DNS-only is live, rerun nmap

**3. Check a public resolver to separate jumpbox DNS cache from Cloudflare propagation**

```bash
dig @8.8.8.8 sandbox-testing-1.fitfile.net +short
```

If Google's resolver also still returns a Cloudflare IP, the record is still proxied or hasn't propagated yet. If `8.8.8.8` returns your origin IP but the jumpbox doesn't, it's a local DNS cache issue — flush it or wait.

**4. Force-check Cloudflare's own authoritative nameservers**

```bash
# Find Cloudflare's NS for fitfile.net first
dig NS fitfile.net +short

# Then query one directly (e.g. if NS is ada.ns.cloudflare.com)
dig @ada.ns.cloudflare.com sandbox-testing-1.fitfile.net +short
```

This bypasses all caching and tells you definitively what Cloudflare's authoritative DNS is serving right now.

### Once `dig` returns your origin IP

Rerun the nmap scan — it will now hit nginx directly and should return only the 6 AEAD suites (all graded A, no CBC or RSA-exchange entries). Then capture and attach to FTFL-511.

### Ingress-nginx version note

The Helm chart info you pasted (`ingress-nginx v4.14.1` / app `1.14.1`, deployed 2026-04-17) confirms your controller is current — there's nothing in that version that would introduce weak ciphers on the nginx side. The origin nginx config was already clean on Friday. The only thing standing between you and a passing retest is the DNS propagation.

## Asset 11 (Pieces: 6ba298d9-2ca1-4ead-a773-dbf27b164efd) — 2026-06-01T08:38

The user is sharing their nmap scan results. Let me analyze what this shows:

1. The nmap scan resolved `sandbox-testing-1.fitfile.net` to **172.67.72.212** - which is still a Cloudflare Anycast IP address (172.67.x.x range). This means the DNS-only change hasn't propagated yet, OR the DNS is still proxied through Cloudflare.

2. The scan shows 20 cipher suites - exactly the same problematic set from Friday's original pentest scan, including:
   - CBC-mode ciphers (should be removed)
   - RSA key exchange ciphers without forward secrecy (should be removed)
   - The good AEAD suites

Since the IP is still resolving to Cloudflare, the DNS change either hasn't propagated through cached resolvers yet, the record is still set to proxied mode, or there's a caching issue preventing the change from taking effect. The user needs to verify the DNS change actually went through in their Cloudflare settings and check if the resolver is picking up the new configuration. I need to see the next thinking content to rewrite it. You've provided instructions and context about my current rewritten thinking, but the "next thinking you need to rewrite" section appears to be empty.

Could you share the next thinking chunk that needs to be rewritten?

## Asset 12 (Pieces: 001d11ea-4e94-4473-be02-3e8df852add8) — 2026-06-01T08:38

NAME: ingress-nginx
CHART: ingress-nginx
VERSION: 4.14.1
APP_VERSION: 1.14.1
ANNOTATIONS: artifacthub.io/changes=- Update Ingress-Nginx version controller-v1.14.1
,artifacthub.io/prerelease=false
LABELS: modifiedAt=1776435745,name=ingress-nginx,owner=helm,status=deployed,version=1
DEPENDENCIES: 
NAMESPACE: ingress-nginx
REVISION: 1
STATUS: deployed
DEPLOYED_AT: 2026-04-17T14:21:59Z
APPLY_METHOD:nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-01 08:37 UTC
Nmap scan report for sandbox-testing-1.fitfile.net (172.67.72.212)
Host is up (0.0023s latency).
Other addresses for sandbox-testing-1.fitfile.net (not scanned): 104.26.0.140 104.26.1.140 2606:4700:20::681a:18c 2606:4700:20::ac43:48d4 2606:4700:20::681a:8c

PORT    STATE SERVICE
443/tcp open  https
| ssl-enum-ciphers: 
|   TLSv1.2: 
|     ciphers: 
|       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA (ecdh_x25519) - A
|       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 (ecdh_x25519) - A
|       TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|       TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA (ecdh_x25519) - A
|       TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 (ecdh_x25519) - A
|       TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_GCM_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_GCM_SHA384 (rsa 2048) - A
|     compressors: 
|       NULL
|     cipher preference: client
|   TLSv1.3: 
|     ciphers: 
|       TLS_AKE_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|       TLS_AKE_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A
|     cipher preference: client
|_  least strength: A

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds

## Asset 13 (Pieces: 3314644d-e59b-4d73-a611-cd57e8ae2c49) — 2026-06-01T08:27

The final pagination page returns exclusively the same previously-seen event IDs (the high-scoring FTFL-511/512 nginx/Cloudflare events, plus the Reddit/audio noise). No new material facts emerged. Memory exhaustion is complete.

---

## How to retest **FTFL-511** after switching Cloudflare to DNS-only

Here's exactly what you need to do, grounded in the commands and evidence from your Friday session (Claude chat [11e30ed6](https://claude.ai/chat/11e30ed6-eb47-4ed1-8f1c-02e53c2b76d2), Jira [FTFL-511](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?assignee=633ae2b9fedc6169aed8f601&selectedIssue=FTFL-511)).

### Why the retest is now different

When you first scanned `sandbox-testing-1.fitfile.net` the resolved IPs were Cloudflare Anycast addresses (`172.67.72.212`, `104.26.0.140`, `104.26.1.140`) — so every tool hit Cloudflare's TLS termination, not your nginx origin. Now that Cloudflare is set to **DNS-only** (grey cloud), the hostname resolves directly to your Azure Load Balancer IP (`20.117.146.221`), meaning a plain scan of the hostname will now hit nginx directly — exactly what you want.

### Step 1 — Confirm DNS now resolves to your origin (not Cloudflare)

```bash
dig sandbox-testing-1.fitfile.net +short
```

You should see your Azure LB IP (e.g. `20.117.146.221`) **not** a `172.67.x.x` or `104.26.x.x` Cloudflare range. If you still see a Cloudflare IP, DNS hasn't propagated yet — wait a few minutes and retry.

### Step 2 — Run the TLS cipher scan directly against the hostname

Now that DNS is orange→grey, you can scan the public hostname without needing `--resolve` to bypass Cloudflare:

```bash
nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net
```

**Expected passing result** — only modern AEAD suites, matching what your Friday direct-IP scan already confirmed on the origin:

```
TLSv1.2:
  TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 - A
  TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 - A
  TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 - A
TLSv1.3:
  TLS_AKE_WITH_AES_128_GCM_SHA256 - A
  TLS_AKE_WITH_AES_256_GCM_SHA384 - A
  TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 - A
```

No `TLS_RSA_WITH_*` or CBC-mode suites should appear. If they do, something other than Cloudflare is still terminating TLS in front of nginx.

### Step 3 — Save a post-fix artefact for the ticket

Use the same capture pattern from Friday:

```bash
{
  echo "=== POST-FIX TLS CIPHERS ==="
  nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net

  echo ""
  echo "=== RESPONSE HEADERS ==="
  curl -sIL https://sandbox-testing-1.fitfile.net/fitfile/api/auth/session -v 2>&1
} > ~/ftfl-511-post-fix-$(date +%Y%m%d).txt
```

Attach that file to **FTFL-511** as the remediation evidence.

### Step 4 — Optionally cross-check with openssl for a human-readable handshake

```bash
openssl s_client -connect sandbox-testing-1.fitfile.net:443 \
  -tls1_2 \
  -cipher 'TLS_RSA_WITH_AES_128_CBC_SHA' 2>&1 | grep -E "Cipher|handshake"
```

This should return a **handshake failure** — confirming the weak CBC/RSA suites are no longer accepted.

### Step 5 — Update FTFL-511 in Jira

Your Friday comment on [FTFL-511](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?assignee=633ae2b9fedc6169aed8f601&selectedIssue=FTFL-511) already correctly re-scoped the finding:

> *"This finding is misattributed to Nginx — the weak ciphers are at the Cloudflare edge, not the origin."*

Now you can close the loop: add the post-fix nmap output confirming only A-grade AEAD suites are exposed, note that the resolution was switching Cloudflare from **Proxy → DNS-only**, and move the ticket to **Done**.

### One caveat

Once you switch to DNS-only, your origin IP (`20.117.146.221`) is publicly exposed. Your Friday session also discussed restricting the Azure NSG port 443 to Cloudflare IP ranges as a follow-on hardening step — you may want to revisit whether that NSG lockdown is still appropriate now that you've gone DNS-only and traffic no longer originates from Cloudflare ranges.

## Asset 14 (Pieces: 9ba83f8a-8a43-4419-bede-b79d9b8f82a2) — 2026-06-01T08:26

The cloudflare search is now `sufficient`. The nginx pentest search is still paginating with the same content repeating (no new high-scoring candidates beyond what was already retrieved). I have all the evidence I need from the first two successful calls. Here is the full answer grounded in your Friday session.

---

## How to retest FTFL-511 after switching Cloudflare to DNS-only

### What you found on Friday (the context)

From your Friday work session ([FTFL-511 Nginx Cipher Compliance Analysis](https://claude.ai/chat/11e30ed6-eb47-4ed1-8f1c-02e53c2b76d2)):

> "This finding is misattributed to Nginx — the weak ciphers are at the Cloudflare edge, not the origin. The pentest scanned the public hostname `sandbox-testing-1.fitfile.net`, which resolves to Cloudflare. The cipher list in the report (the `TLS_RSA_*` and CBC suites) is therefore Cloudflare's edge TLS configuration, not Nginx's."

The key evidence was that the resolved IPs — `172.67.72.212`, `104.26.0.140`, `104.26.1.140` — are **Cloudflare Anycast addresses**, so every test hit Cloudflare's TLS termination layer, not your nginx origin. Scanning the origin directly (`20.117.146.221`, bypassing Cloudflare) already returned only modern AEAD suites graded A.

Now that you've set the DNS record to **DNS-only** (grey-clouded in Cloudflare), TLS is no longer terminated at the Cloudflare edge — traffic goes straight to your origin IP. The pentest tool will now talk directly to nginx. Here's how to retest.

---

### Retesting procedure

#### Step 1 — Confirm DNS is now bypassing Cloudflare

Before running the cipher scan, verify the DNS resolves to your origin IP (not a Cloudflare Anycast range):

```bash
dig sandbox-testing-1.fitfile.net +short
```

You should now see your Azure load-balancer IP (`20.117.146.221` or similar) — **not** a `172.67.x.x` / `104.26.x.x` Cloudflare address. If you still see Cloudflare IPs, DNS hasn't propagated yet (TTL-dependent, usually 1–5 mins for CF).

#### Step 2 — Re-run the exact same nmap cipher scan from the Friday baseline

This is the command you used on Friday from the FITFILEJumpbox:

```bash
nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net
```

**What to expect now:** You should only see the modern AEAD-only suites that were already coming back when you bypassed Cloudflare with `--resolve`:

```
TLSv1.2:
  TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 - A
  TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 - A
  TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 - A
TLSv1.3:
  TLS_AKE_WITH_AES_128_GCM_SHA256 - A
  TLS_AKE_WITH_AES_256_GCM_SHA384 - A
  TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 - A
```

The `TLS_RSA_*` and CBC-mode suites (the ones the pentest flagged) should be **absent**, because those were Cloudflare's.

#### Step 3 — Capture a timestamped before/after artefact for the ticket

From Friday's session you had a handy capture script — reuse the same pattern:

```bash
{
  echo "=== TLS CIPHERS POST-FIX ==="
  nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net

  echo ""
  echo "=== RESPONSE HEADERS ==="
  curl -sIL https://sandbox-testing-1.fitfile.net/fitfile/api/auth/session -v 2>&1
} > ~/ftfl-511-post-fix-$(date +%Y%m%d).txt
```

Upload the `.txt` file as evidence to [FTFL-511 on Jira](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?assignee=633ae2b9fedc6169aed8f601&selectedIssue=FTFL-511).

#### Step 4 — Optional: cross-check with `openssl s_client`

A quick sanity-check that goes straight to the TLS handshake:

```bash
echo | openssl s_client -connect sandbox-testing-1.fitfile.net:443 \
  -tls1_2 2>&1 | grep "Cipher is"
```

This should return a GCM cipher. If it returns a CBC or RSA-exchange cipher, something is still routing through Cloudflare's proxy.

---

### What to put in the FTFL-511 ticket comment

The Friday write-up already had this framing right. The comment you drafted was:

> **FTFL-511 (API-5) — Origin Nginx is not using the flagged ciphers**
> The weak cipher suites in the pentest report were served by the Cloudflare edge (the DNS record was in proxy mode at scan time). Cloudflare has now been set to DNS-only, so origin TLS is served directly by nginx. Re-scan confirms only AEAD suites with PFS are advertised. No nginx/ingress-nginx config change required.

Attach the `ftfl-511-post-fix-YYYYMMDD.txt` file and close the ticket.

---

### If the bad ciphers are still showing after DNS-only

That would mean one of two things:
- **DNS propagation hasn't finished** — wait and re-check `dig` first.
- **Your nginx/ingress-nginx config actually does have weak ciphers configured** — in that case, you'd need to add the `ssl-ciphers` and `ssl-protocols` hardening to the ingress-nginx Helm values (`controller.config`), which was the other remediation path discussed on Friday.

## Asset 15 (Pieces: 8e7b9778-4e55-4eac-b4bd-8e047982160f) — 2026-06-01T08:19

The user is asking about retesting nginx/TLS cipher pentest results after switching Cloudflare records to DNS-only mode. Let me first search their memory to find the specific context from Friday, then I can provide a well-grounded answer about retesting.

Let me search for the relevant context first.

## Asset 16 (Pieces: 247ed4ba-d561-45e4-9dbb-a54b6f8ddc6f) — 2026-06-01T08:19

on friday we worked on some nginx pentest results. there was a mistake in the results that said nginx was returning outdated tls ciphers. It turned out it was the cloudflare edge. I have switched the cloudflare records to be DNS only. How do I retest the results to see that it fixes the pentest results
