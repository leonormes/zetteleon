---
aliases: []
confidence: 
created: 2025-08-14T20:21:09Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:24Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: TLS tcp
type:
uid: 
updated: 
version:
---

## From TCP Connect to Encrypted Data: what Actually Happens

When your app connects to a remote server over TLS, there’s a precise sequence of networking and cryptographic steps that take you from “dial a socket” to “confidential, integrity-protected bytes flow.” Here’s a developer-focused walkthrough, emphasizing modern TLS 1.3 behavior and calling out where TLS 1.2 differs.

### 1) Name Resolution and Routing

Typically you first resolve a hostname to an IP via DNS, possibly using DNS over HTTPS/TLS for privacy. Once you have an IP, your client opens a TCP connection to the server’s port, often 443. This starts with the standard TCP three-way handshake: SYN → SYN-ACK → ACK. At this point you have a reliable byte stream to carry the TLS protocol messages. A good byte-by-byte walkthrough of the pre-TLS TCP and legacy SSL flow is here if you want to see captures and fields discussed in depth [CommandLineFanatic TLS 1.2/SSL handshake walkthroughs](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art059).

### 2) ClientHello: Propose Security Parameters

Immediately after TCP is established, the client sends a TLS ClientHello in cleartext. This message proposes what the client supports and intends to use. In TLS 1.3 this includes, among other extensions:

- Supported cipher suites: in 1.3 these are pared down to AEAD suites such as AES-GCM and ChaCha20-Poly1305 with specific hashes, and they no longer encode the key exchange and signature parts as they did in 1.2, simplifying choices and removing legacy/insecure combinations [Cloudflare overview](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/).
- KeyShare: the client’s ephemeral ECDHE key share(s), commonly X25519 or P-256, sent up front to enable a 1-RTT handshake. If the server wants a different group, it can request a HelloRetryRequest to redo the share. A very detailed dissection of a real TLS 1.3 ClientHello with bytes is here [CommandLineFanatic TLS 1.3 walkthrough](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art080).
- SNI (Server Name Indication): the hostname the client is trying to reach, allowing a multi-tenant server to choose the right certificate. SNI is in cleartext in TLS 1.3; work to encrypt it exists (ECH), but that’s beyond baseline TLS 1.3. The SNI role and privacy trade-offs are discussed with examples in the 1.3 walkthrough [CommandLineFanatic TLS 1.3 walkthrough](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art080).
- ALPN (Application-Layer Protocol Negotiation): which higher-level protocol the client wants (e.g., h2 for HTTP/2 or http/1.1). This drives how your encrypted bytes will be framed after the handshake. High Performance Browser Networking’s TLS chapter covers ALPN, OCSP stapling, and performance aspects well [HPBN TLS chapter](https://hpbn.co/transport-layer-security-tls/).
- Supported versions: the explicit list of TLS versions the client accepts. TLS 1.3 introduced this to fix version-intolerance issues in middleboxes; the record/version fields may still look like older versions for compatibility until the “supported versions” extension advertises 1.3 [CommandLineFanatic TLS 1.3 walkthrough](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art080).

In TLS 1.2, by contrast, the client did not include a KeyShare; instead it listed cipher suites that implicitly specified both key exchange and bulk ciphers, and the key exchange happened later. Background and contrasts are summarized here [Cloudflare](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/) and here [Auth0 overview](https://auth0.com/blog/the-tls-handshake-explained/).

### 3) ServerHello and Shared Secret Establishment

The server responds with ServerHello, choosing parameters:

- It selects the TLS version (ideally 1.3), an AEAD cipher suite, and the matching key exchange group.
- It sends its own ephemeral ECDHE key share. With both ECDHE shares, each side derives the same Diffie-Hellman shared secret. In TLS 1.3, this immediately drives a hierarchical key schedule (HKDF-based) that yields “handshake traffic keys” and later “application traffic keys.” The shorter, cleaner 1-RTT flow and key schedule are covered in approachable terms here [Cloudflare](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/) and at byte-level detail here [The Illustrated TLS 1.3 Connection](https://tls13.xargs.org/).

Everything after ServerHello is now encrypted in TLS 1.3, including the server certificate. This is another major difference from TLS 1.2, where more of the handshake remained in cleartext. You can see why many packet-level analyses use OpenSSL’s s_client to expose the logical messages rather than try to read raw packets post-ServerHello [CommandLineFanatic TLS 1.3 walkthrough](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art080).

### 4) Server Authentication: Certificate, Chain, and Status

Inside encrypted handshake messages, the server proves its identity:

- Certificate: the server sends its certificate chain (server cert plus intermediates). The client validates the chain against its trust store, checks name/SAN matches the SNI, ensures validity periods, and enforces usage constraints.
- Certificate status (OCSP stapling): commonly the server includes a stapled OCSP response proving the CA considers the certificate good, saving a client round-trip to the CA and improving privacy [HPBN TLS chapter](https://hpbn.co/transport-layer-security-tls/).
- CertificateVerify: the server signs a transcript hash with its certificate’s private key, proving possession and binding the identity to the ongoing handshake.
- Finished: both sides exchange Finished messages that MAC the entire handshake transcript using the derived handshake keys, detecting tampering.

TLS 1.3 mandates forward-secret key exchanges (ephemeral ECDHE) and removes legacy/weak options, addressing many pitfalls of TLS 1.2’s configurability and RSA key exchange weaknesses (no PFS, private-key compromise enabling historical decryption). Good high-level comparisons are here [Cloudflare](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/) and here [Auth0](https://auth0.com/blog/the-tls-handshake-explained/).

If you use mutual TLS (mTLS), the server will also request a client certificate; the client sends its certificate and a CertificateVerify to prove possession, giving the server strong client authentication. The mechanics ride the same TLS messages.

### 5) Session Keys and Application Data

With authentication complete and Finished verified, both sides derive application traffic keys. TLS 1.3 uses HKDF to step keys forward (early secret → handshake secret → master secret → application secrets), providing key separation and making compromise of one stage insufficient to unlock others. A visual, step-by-step key schedule is shown here [The Illustrated TLS 1.3 Connection](https://tls13.xargs.org/).

Application bytes you write to the socket are now framed by the TLS record layer and encrypted with an AEAD cipher:

- AEAD (AES-GCM or ChaCha20-Poly1305) provides confidentiality and integrity in one operation. Nonces are implicit counters derived from a per-connection IV and the record sequence number; reusing nonces with the same key is catastrophic, so TLS carefully constructs them and increments sequence numbers per record. Record formatting, content types (opaque in 1.3), and padding behavior are covered in detail with diagrams here [The Illustrated TLS 1.3 Connection](https://tls13.xargs.org/).
- Integrity is verified via the AEAD tag; any tampering or truncation causes decryption failure and connection teardown.

From here up, your chosen ALPN protocol runs: HTTP/1.1 text over TLS, or HTTP/2 multiplexed frames, etc. The TLS layer is oblivious to application semantics.

### 6) Resumption and 0‑RTT

TLS 1.3 replaces legacy session IDs/tickets with PSK-based resumption:

- After a full handshake, the server may send a NewSessionTicket that the client stores. On next connect, the client offers a PSK identity and binder; if accepted, both derive keys from the PSK, skipping certificate exchange and reducing latency.
- 0-RTT data: the client can optionally send “early data” immediately with the first flight, before the server’s Finished. This is replayable by design; only use it for idempotent operations and guard with anti-replay, rate limits, and policy. Overviews and cautions are in plain language here [Cloudflare](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/) and here [Auth0](https://auth0.com/blog/the-tls-handshake-explained/).

In TLS 1.2, “session resumption” used session IDs or tickets but still required more handshake messages and didn’t unify as cleanly with the key schedule.

### 7) Key Updates, Renegotiation, and Lifecycle

TLS 1.3 supports KeyUpdate to roll application traffic keys periodically without a new handshake. Legacy renegotiation is removed; that class of features caused complexity and security issues in earlier TLS versions. Many middlebox compatibility quirks that influenced prior handshakes (like version intolerance) are explained with concrete examples here [CommandLineFanatic TLS 1.3 walkthrough](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art080).

### 8) Failure Modes and what to Log

For robust deployments, log and surface errors for:

- Certificate validation failures (name mismatch, expired, untrusted root).
- Handshake alerts (protocol version, illegal parameter, bad_record_mac).
- AEAD decryption failures (usually integrity errors or key mismatch).
- Resumption/0-RTT policy rejections.

These are often surfaced as TLS alerts on the wire and as exceptions in your TLS library.

### 9) Putting it All together (flow summary)

- TCP connects on 443.
- ClientHello advertises SNI/ALPN/versions and sends ECDHE KeyShare.
- ServerHello chooses cipher/version, returns ECDHE KeyShare; both derive handshake keys.
- Encrypted handshake: server sends certificate chain (+ OCSP stapling), proves possession; client validates chain and name; both send Finished.
- Application traffic keys derived; application data flows encrypted with AEAD and integrity-protected.
- Optional: PSK resumption and 0‑RTT on future connections; periodic KeyUpdate.

If you want a single resource that walks through “every byte” of a real TLS 1.3 connection, including the key schedule derivations and record encryption details, this one is excellent: The Illustrated TLS 1.3 Connection [tls13.xargs.org](https://tls13.xargs.org/). For broader, vendor-neutral overviews and TLS 1.2 vs 1.3 differences, see Cloudflare’s explainer [Cloudflare](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/), Auth0’s primer [Auth0](https://auth0.com/blog/the-tls-handshake-explained/), HPBN’s chapter on TLS performance features like OCSP stapling and ALPN [HPBN](https://hpbn.co/transport-layer-security-tls/), and a byte-level TLS 1.3 handshake trace with OpenSSL [CommandLineFanatic](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art080).

Want me to tailor this to your stack (language/runtime) with concrete library calls, settings for TLS 1.3, ALPN, OCSP stapling, and mTLS?
