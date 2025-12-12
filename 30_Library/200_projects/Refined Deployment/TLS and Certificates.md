---
aliases: []
confidence: 
created: 2025-09-17T09:41:09Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [certificates, cryptography, http]
title: TLS and Certificates
type:
uid: 
updated: 
version:
---

- TLS (Transport Layer Security) is the **encryption protocol** that protects the communication channel.
- Certificates are used to **validate the server’s identity** — i.e., "is this really `bank.com` and not an imposter?"

## What Happens when the Browser doesn’t Trust the Certificate

1. **TLS negotiation still happens.**
   - The browser and server perform the cryptographic TLS handshake.
   - Encryption keys are established, so the channel itself *is* encrypted.

2. **But the validation step fails.**
   - The browser checks the server’s certificate against its trust store (collection of trusted root CAs).
   - If the certificate is **untrusted** (self-signed, expired, unknown issuer, etc.), the **identity cannot be verified**.

3. **Browser behavior.**
   - The browser does *not* silently downgrade to plaintext (HTTP).
   - Instead, it shows a **scary warning** (like "Your connection is not private" or "Potential security risk ahead").
   - If the user ignores the warning and clicks through, the connection proceeds:
     - The session is still **encrypted** (attackers can’t just read the traffic).
     - But because the server’s identity is not validated, a **man-in-the-middle (MITM)** could be impersonating the server.

## Summary

- **Encryption:** ✅ Yes, the traffic is still encrypted with TLS.
- **Authentication:** ❌ Fails, so you don’t know if you’re talking to the real server.
- **Downgrade to plaintext?:** ❌ No, browsers won’t silently fall back to unencrypted HTTP.
- **Security risk:** A MITM could present a fake certificate, and if you click through the warning, you’d be sending data (still encrypted) to the wrong party.

So: encryption remains, but without trust in the server’s identity, the connection is not *secure* in the HTTPS sense.
