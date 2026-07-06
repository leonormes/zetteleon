---
created: Invalid date
modified: 2026-07-04T10:49:37+00:00
permalink: llmeon/raw/2026-06-01-pieces-ftfl-511-tls-retest
pieces_ids: [001d11ea-4e94-4473-be02-3e8df852add8, 38b50523-2ac9-4ca6-b1f7-dd3b23f1e5c6, 480f2d8a-ccf4-4b1d-9d04-a75b69c29a7d, 8e7b9778-4e55-4eac-b4bd-8e047982160f, 9a572b4c-d9a1-4fb9-a5a2-51269582f7f1, e98472a6-f2be-477b-a36b-8d0ecf3ccde0]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-06-01-pieces-ftfl-511-tls-retest
---

## Asset 1 (Pieces: 480f2d8a-ccf4-4b1d-9d04-a75b69c29a7d)

_Captured: 2026-06-01T08:53:31.868454Z_

The user has run the nmap scan and the results are exactly what we expected. The scan now hits the origin IP (20.117.146.221) directly, and only shows modern AEAD suites - no CBC or RSA key exchange ciphers. This is a clean pass. Let me analyze the results:

TLSv1.2:

- TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 - A ✅
- TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 - A ✅
- TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 - A ✅

TLSv1.3 is showing the same strong cipher suite pattern with AES-GCM and ChaCha20-Poly1305 variants, all rated A. The absence of CBC ciphers and RSA key exchange mechanisms confirms we've successfully eliminated weak cryptography, and the server cipher preference setting means the server is controlling which cipher gets used rather than letting the client choose.

FTFL-511 is resolved now, so I should make sure the user captures this output and attaches it to the ticket.

---

## Asset 2 (Pieces: 9a572b4c-d9a1-4fb9-a5a2-51269582f7f1)

_Captured: 2026-06-01T08:53:21.356036Z_

dig sandbox-testing-1.fitfile.net +short

20.117.146.22nmap --script ssl-enum-ciphers -p 443 sandbox-testing-1.fitfile.net

Starting Nmap 7.95 (<https://nmap.org>) at 2026-06-01 08:53 UTC

Nmap scan report for sandbox-testing-1.fitfile.net (20.117.146.221)

Host is up (0.0086s latency).

PORT STATE SERVICE

443/tcp open https

| ssl-enum-ciphers:

| TLSv1.2:

| ciphers:

| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A

| compressors:

| NULL

| cipher preference: server

| TLSv1.3:

| ciphers:

| TLS_AKE_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A

| TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A

| TLS_AKE_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A

| cipher preference: server

|_ least strength: A

Nmap done: 1 IP address (1 host up) scanned in 0.40 seconds

---

## Asset 3 (Pieces: e98472a6-f2be-477b-a36b-8d0ecf3ccde0)

_Captured: 2026-06-01T08:53:03.847117Z_

The user has run the `dig` command and it's now returning `20.117.146.221`—their Azure origin IP, not a Cloudflare Anycast address. This means DNS-only has propagated. They should now rerun the nmap scan directly against the hostname.

---

## Asset 4 (Pieces: 38b50523-2ac9-4ca6-b1f7-dd3b23f1e5c6)

_Captured: 2026-06-01T08:52:50.988648Z_

dig sandbox-testing-1.fitfile.net +short

20.117.146.221

---

## Asset 5 (Pieces: 001d11ea-4e94-4473-be02-3e8df852add8)

_Captured: 2026-06-01T08:38:22.883062Z_

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

Starting Nmap 7.95 (<https://nmap.org>) at 2026-06-01 08:37 UTC

Nmap scan report for sandbox-testing-1.fitfile.net (172.67.72.212)

Host is up (0.0023s latency).

Other addresses for sandbox-testing-1.fitfile.net (not scanned): 104.26.0.140 104.26.1.140 2606:4700:20::681a:18c 2606:4700:20::ac43:48d4 2606:4700:20::681a:8c

PORT STATE SERVICE

443/tcp open https

| ssl-enum-ciphers:

| TLSv1.2:

| ciphers:

| TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA (ecdh_x25519) - A

| TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 (ecdh_x25519) - A

| TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A

| TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA (ecdh_x25519) - A

| TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 (ecdh_x25519) - A

| TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A

| TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A

| TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A

| TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A

| TLS_RSA_WITH_AES_128_CBC_SHA256 (rsa 2048) - A

| TLS_RSA_WITH_AES_128_GCM_SHA256 (rsa 2048) - A

| TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A

| TLS_RSA_WITH_AES_256_CBC_SHA256 (rsa 2048) - A

| TLS_RSA_WITH_AES_256_GCM_SHA384 (rsa 2048) - A

| compressors:

| NULL

| cipher preference: client

| TLSv1.3:

| ciphers:

| TLS_AKE_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A

| TLS_AKE_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A

| TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A

| cipher preference: client

|_ least strength: A

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds

---

## Asset 6 (Pieces: 8e7b9778-4e55-4eac-b4bd-8e047982160f)

_Captured: 2026-06-01T08:19:47.175591Z_

The user is asking about retesting nginx/TLS cipher pentest results after switching Cloudflare records to DNS-only mode. Let me first search their memory to find the specific context from Friday, then I can provide a well-grounded answer about retesting.

Let me search for the relevant context first.
