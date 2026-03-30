*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday Mar 30, 2026 - 4:31 PM*
---
# NWSDE → LCRCA Connectivity Report
**Date:** Monday, March 30, 2026 — Testing conducted ~3:26 PM – 4:30 PM  
**Tested from:** Netshoot pod in NWSDE cluster (`kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- bash`)  
**Target:** `lca-prd-2.fitfile.net:11001` (LCRCA production ingress via hub DNAT)  
**Related ticket:** [FTFL-420](https://fitfile.atlassian.net/browse/FTFL-420)

---

## Executive Summary

**The network path from NWSDE to LCRCA is fully operational.** DNS, egress, TCP, TLS, and HTTP all work correctly through the hub's DNAT on port 11001. However, the LCRCA application returns a `302` redirect to a URL that **drops the `:11001` port**, causing any follow-on requests to hang. This is an **ingress/application configuration issue**, not a networking issue.

---

## Network Path Under Test

| Hop | Value | Status |
|---|---|---|
| NWSDE cluster egress IP | `20.68.120.178` | ✅ Confirmed |
| Hub public IP | `4.158.64.255` | ✅ Confirmed |
| Hub inbound port | `11001` | ✅ Open & accepting |
| DNAT destination | `10.200.80.50:443` (lca-prd-2 internal ingress) | ✅ Functioning |

---

## Layer-by-Layer Results

### 1. DNS Resolution ✅

```
dig lca-prd-2.fitfile.net +short → 4.158.64.255
```

- Resolves correctly to the hub public IP
- Query time: **4ms** (from cluster DNS at `10.2.0.10`)
- TTL: 30 seconds

### 2. Egress IP Verification ✅

```
curl -s https://ifconfig.me → 20.68.120.178
```

- Matches the expected NWSDE egress IP that should be whitelisted on the hub firewall
- Confirms the pod is egressing through the correct NAT gateway

### 3. TCP Connectivity ✅ (inferred)

- The `nc -zv` tests failed due to a syntax issue (netshoot ships `ncat` which uses `--wait` not `-w`) — **this is a tool incompatibility, not a connectivity failure**
- TCP is **proven working** by the successful TLS handshake and HTTP response (you can't get either without a TCP connection)

### 4. TLS Handshake ✅

```
CONNECTION ESTABLISHED
Protocol version: TLSv1.3
Ciphersuite: TLS_AES_256_GCM_SHA384
Peer certificate: CN=lca-prd-2.fitfile.net
```

- TLS 1.3 with strong cipher suite
- Certificate CN matches the target hostname — **no cert mismatch**
- The DNAT correctly lands on the LCRCA ingress, and the ingress is serving the right certificate

### 5. HTTP Response ✅ (with caveat)

```
HTTP_CODE: 302
TIME_CONNECT: 0.009321 (9ms)
TIME_STARTTRANSFER: 0.027243 (27ms)
TIME_TOTAL: 0.027340 (27ms)
```

- **The LCRCA application responds to requests** — this is a real HTTP response, not a timeout or error
- The 302 is the application's own redirect behaviour (likely directing to the main UI)

### 6. The Redirect Problem ⚠️

```
HTTP/2 302
location: https://lca-prd-2.fitfile.net/fitfile
```

**This confirms the issue I predicted.** The `Location` header redirects to `https://lca-prd-2.fitfile.net/fitfile` — note the **missing `:11001`**. This means:

- The initial request to `:11001` → succeeds (DNAT translates to `:443` internally)
- The backend generates a redirect URL assuming port `443` (the port it actually received the request on)
- Following that redirect hits `lca-prd-2.fitfile.net:443` directly — which **is not DNAT'd** through the hub
- Result: the `-L` (follow redirect) curl hangs indefinitely, which is exactly what you experienced

---

## Diagnosis

| Component | Verdict |
|---|---|
| DNS | ✅ Working |
| NWSDE egress NAT | ✅ Correct IP (`20.68.120.178`) |
| Hub firewall (source allow) | ✅ Traffic passes |
| Hub DNAT (`11001→443`) | ✅ Translating correctly |
| LCRCA ingress controller | ✅ Accepting connections, valid TLS |
| LCRCA application | ✅ Responding with HTTP 302 |
| **Redirect URL port** | ⚠️ **Drops `:11001`** — redirects to default 443 |

**Root cause:** The LCRCA ingress is unaware that external clients arrive on port `11001`. It generates redirect URLs using the port it sees internally (443), which is unreachable from outside the cluster.

---

## Recommended Fixes

In priority order:

### Option 1: Ingress Annotation Fix (preferred)
Add `proxy-redirect` annotations to the **LCRCA ingress** to rewrite `Location` headers:

```yaml
nginx.ingress.kubernetes.io/proxy-redirect-from: "https://lca-prd-2.fitfile.net/"
nginx.ingress.kubernetes.io/proxy-redirect-to: "https://lca-prd-2.fitfile.net:11001/"
```

This transparently rewrites all redirect URLs to include the correct external port.

### Option 2: X-Forwarded-Port Header
Configure the ingress to pass the original port to the backend:

```yaml
nginx.ingress.kubernetes.io/x-forwarded-port: "11001"
```

This requires the backend application to honour `X-Forwarded-Port` when generating URLs.

### Option 3: Hub-side port 443 DNAT
Ask J Davitt / Jaimie Wade to also DNAT `443→443` through the hub. Simplest but broadest — may not be desirable from a security standpoint.

---

## Suggested Ticket Update for [FTFL-420](https://fitfile.atlassian.net/browse/FTFL-420)

> **NWSDE → LCRCA connectivity confirmed working** (tested 30 Mar 2026, ~4:30 PM).
>
> Full path validated: NWSDE egress (`20.68.120.178`) → Hub (`4.158.64.255:11001`) → DNAT → LCRCA ingress (`10.200.80.50:443`). DNS, TCP, TLS (v1.3, correct cert CN), and HTTP all pass. Initial request returns `HTTP 302` in 27ms.
>
> **Remaining issue:** The 302 redirect `Location` header is `https://lca-prd-2.fitfile.net/fitfile` — missing the `:11001` port suffix. This causes follow-on requests to target port 443 directly, which is not exposed through the hub DNAT, resulting in timeouts. 
>
> **Fix required:** LCRCA ingress needs `proxy-redirect` annotations to rewrite Location headers with the correct external port (`:11001`). This is an ingress configuration change, not a networking change.

---

This should give Robin Mofakham everything he needs to either apply the ingress fix himself or hand it to whoever manages the LCRCA ingress config. The networking blocker he raised on Friday is effectively cleared — it's now an application-layer fix.