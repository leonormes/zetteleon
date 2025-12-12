---
aliases: []
confidence: 
created: 2025-10-24T11:41:58Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:32:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: Networking For Hackers (DNS - Domain Name System)
type:
uid: 
updated: 
version:
---

<https://youtube.com/watch?v=tmQ9EbUEv4Y>\&si=sU-HvlGgPpEo4QHL

The YouTube video **“Networking For Hackers (DNS - Domain Name System)!”** was produced by **Neurix**, a cybersecurity and networking education channel known for hands-on lab tutorials and hacker-oriented network fundamentals [^1][^2].

Published in **July 2025**, this 16‑minute video explains the **Domain Name System (DNS)** through practical demonstrations in an EVE‑NG (Emulated Virtual Environment for Networking) lab. It illustrates how DNS performs hostname-to-IP translation, how caching and resolution work, and why DNS is core to Internet functionality.

## Key Concepts Covered

- **DNS fundamentals:** Explains why DNS is the “Internet’s phonebook” that translates human-readable names like *netflix.com* into IP addresses.
- **Step-by-step resolution:** Demonstrates how a request flows from a local cache to recursive resolvers, root servers, TLD servers, and finally the authoritative name server.
- **Caching behavior:** Shows how Windows’ DNS cache works using `ipconfig /displaydns` and how entries persist until TTL (Time To Live) expiry.
- **Diagnostic tools:**
  - Uses `nslookup` to show non-authoritative DNS responses from Google Public DNS (`8.8.8.8`).
  - Uses `dig` on Kali Linux to inspect full query details including headers, latency, and message size.
- **Breaking DNS intentionally:** Edits `/etc/resolv.conf` to point to an invalid server (`8.0.8.8`) to simulate resolution failure. The video confirms network connectivity still works by directly pinging an IP address, proving DNS acts solely as a “translator.”
- **Security insights:** Concludes that understanding DNS is critical for troubleshooting and cybersecurity—referencing how misconfigurations or DNS hijacks can render networks unusable while actual connectivity remains intact.

## Sequence of Demonstrations

1. Flush and inspect DNS cache on Windows.
2. Resolve domains with `nslookup` and analyze authoritative vs. non-authoritative answers.
3. Use `dig` on Linux to view full DNS query structure and timing.
4. Simulate DNS failure by editing resolver settings.
5. Show successful direct IP access to prove DNS dependency.

## Educational Value

The video blends instruction and experimentation, reinforcing key DNS principles for **cybersecurity, networking, and DevOps learners**. It fits into Neurix’s larger “Networking For Hackers” series that also covers IP fundamentals and subnetting [^3].
